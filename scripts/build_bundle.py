#!/usr/bin/env python3
"""Build a fresh, pinned offline snapshot; never install or execute its payloads."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile
import time
import urllib.request
import zipfile

from bundle_layout import command_guides, platform_path


ROOT = Path(__file__).resolve().parents[1]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', path], encoding='utf-8'))


def download(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=120) as response:
                return response.read()
        except (OSError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def safe_member(name):
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name:
        raise ValueError(f'Unsafe archive member: {name}')


def inspect_archive(name, data):
    """Check archive integrity without extracting executable files."""
    if name.endswith('.zip'):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for member in archive.namelist():
                safe_member(member)
            bad = archive.testzip()
            if bad:
                raise ValueError(f'Corrupt ZIP member in {name}: {bad}')
    elif name.endswith('.tar.xz'):
        with tarfile.open(fileobj=io.BytesIO(data), mode='r:xz') as archive:
            for member in archive:
                safe_member(member.name)
                if member.isfile():
                    archive.extractfile(member).read()


def verified_asset(asset, sidecar):
    data, checksum = download(asset['browser_download_url']), download(sidecar['browser_download_url'])
    actual = sha256(data)
    expected = checksum.decode('utf-8-sig').strip().split()[0].lower()
    if not re.fullmatch(r'[0-9a-f]{64}', expected) or actual != expected:
        raise ValueError(f"SHA-256 mismatch: {asset['name']}")
    for item, contents in [(asset, data), (sidecar, checksum)]:
        if len(contents) != item['size']:
            raise ValueError(f"Size mismatch: {item['name']}")
        digest = item.get('digest')
        if digest and digest != 'sha256:' + sha256(contents):
            raise ValueError(f"GitHub digest mismatch: {item['name']}")
    inspect_archive(asset['name'], data)
    return data, checksum


def save_docs(product, output, folder):
    """Mirror release-tag Markdown/manuals, so core documentation works offline."""
    url = f"https://codeload.github.com/{product['repo']}/tar.gz/{product['commit']}"
    docs = []
    with tarfile.open(fileobj=io.BytesIO(download(url)), mode='r:gz') as archive:
        for member in archive:
            if not member.isfile():
                continue
            parts = PurePosixPath(member.name).parts[1:]
            if not parts:
                continue
            relative = PurePosixPath(*parts)
            include = str(relative) in ['README.md', 'CHANGELOG.md', 'HUMAN_CHANGELOG.md', 'METHODOLOGY.md', product['license']]
            include |= parts[0] == 'docs' and relative.suffix.lower() in ['.md', '.txt']
            include |= parts[0] == 'man' and relative.suffix in ['.1', '.md']
            # Operator handoffs and exploratory notes are not end-user manuals.
            if len(parts) > 1 and parts[0] == 'docs' and parts[1] in ['agents', 'thinking', 'research']:
                include = False
            if str(relative) == 'docs/qualification/v4/device-inventory.md':
                include = False
            if not include:
                continue
            safe_member(str(relative))
            data = archive.extractfile(member).read()
            destination = folder / 'upstream' / str(relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            docs.append(dict(path=destination.relative_to(output).as_posix(), sha256=sha256(data), bytes=len(data)))
    for required in ['README.md', 'CHANGELOG.md', product['license']]:
        if not (folder / 'upstream' / required).is_file():
            raise ValueError(f"Missing {product['id']} documentation: {required}")
    return sorted(docs, key=lambda item: item['path'])


def build(spec, output):
    if spec['schema_version'] != 2:
        raise ValueError('Rebuild historical schemas with the build script from their release tag.')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output must be a new or empty directory; an existing bundle is never overwritten.')
    output.mkdir(parents=True, exist_ok=True)
    manifest = {key: spec[key] for key in ['schema_version', 'bundle_version', 'snapshot_date']}
    if 'guide_format' in spec:
        manifest['guide_format'] = spec['guide_format']
    manifest['products'] = []
    for product in spec['products']:
        safe_member(product['id'])
        repo, tag = product['repo'], product['tag']
        release = api(f'repos/{repo}/releases/tags/{tag}')
        commit = api(f'repos/{repo}/commits/{tag}')['sha']
        if release['draft'] or release['prerelease'] or commit != product['commit']:
            raise ValueError(f'Unqualified or moved release tag: {repo} {tag}')
        assets = {asset['name']: asset for asset in release['assets']}
        for name in product['assets']:
            safe_member(name)
            if name not in assets or name + '.sha256' not in assets:
                raise ValueError(f'Missing release asset/checksum: {repo} {name}')
        # Keep the complete installable release matrix visible when upstream adds formats.
        payloads = {name for name in assets if name != 'source.tar.gz' and not name.endswith(
            ('.sha256', '.json', '.sum', '.txt', '.wixpdb', '.sh', '.ps1'))}
        aliases = product.get('identical_aliases', {})
        expected_assets = set(product['assets']) | aliases.keys()
        if payloads != expected_assets:
            raise ValueError(f'Offline inventory differs from {repo} {tag}: '
                             f'{payloads.symmetric_difference(expected_assets)}')
        for alias, canonical in aliases.items():
            digest = assets[canonical].get('digest')
            if canonical not in product['assets'] or not digest or assets[alias].get('digest') != digest:
                raise ValueError(f'Compatibility filename differs from its canonical package: {alias}')
        corporate = [name for name in product['assets'] if '-corporate' in name]
        if sorted(Path(name).suffix for name in corporate) != ['.exe', '.msi']:
            raise ValueError(f'Missing Corporate MSI or EXE: {repo}')
        folder = output / product['id'] / 'Manuals'
        folder.mkdir(parents=True)
        inventory = {key: product[key] for key in ['id', 'repo', 'tag', 'commit', 'commands']}
        if aliases:
            inventory['identical_aliases'] = aliases
        inventory.update(release_url=release['html_url'], published_at=release['published_at'], assets=[])

        def fetch(name):
            data, checksum = verified_asset(assets[name], assets[name + '.sha256'])
            relative = (PurePosixPath(product['id']) / platform_path(name)).as_posix()
            target = output / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            target.with_name(name + '.sha256').write_bytes(checksum)
            return dict(path=relative, bytes=len(data), sha256=sha256(data),
                        source_url=assets[name]['browser_download_url'],
                        sidecar_sha256=sha256(checksum), github_digest=assets[name].get('digest'))

        with ThreadPoolExecutor(max_workers=4) as pool:
            inventory['assets'] = sorted(pool.map(fetch, product['assets']), key=lambda item: item['path'])
        inventory['documentation'] = save_docs(product, output, folder)
        notes = folder / 'RELEASE-NOTES.md'
        notes.write_text(release.get('body') or 'No release notes supplied.', encoding='utf-8', newline='\n')
        data = notes.read_bytes()
        inventory['documentation'].append(dict(path=notes.relative_to(output).as_posix(), sha256=sha256(data), bytes=len(data)))
        manifest['products'].append(inventory)
        print(f"Verified {product['id']} {tag}: {len(inventory['assets'])} payloads, {len(inventory['documentation'])} documents", flush=True)
    if spec.get('prerequisites'):
        manifest['prerequisites'] = spec['prerequisites']
        for prerequisite in manifest['prerequisites']:
            relative = prerequisite['path']
            safe_member(relative)
            contents = download(prerequisite['source_url'])
            if len(contents) != prerequisite['bytes'] or sha256(contents) != prerequisite['sha256']:
                raise ValueError(f'Prerequisite checksum mismatch: {relative}')
            destination = output / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(contents)
    for relative, contents in command_guides(manifest).items():
        (output / relative).write_text(contents, encoding='utf-8', newline='\n')
    (output / 'bundle-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')
    return manifest


def verify_legacy(directory, manifest):
    checked = 0
    for product in manifest['products']:
        safe_member(product['folder'])
        folder = directory / product['folder']
        expected_files = set()
        for line in (folder / 'sha256.sum').read_text(encoding='utf-8').splitlines():
            expected, relative = line.split('  ', 1)
            safe_member(relative)
            path = folder / relative
            if sha256(path.read_bytes()) != expected:
                raise ValueError(f'Checksum mismatch: {path}')
            expected_files.add(relative)
            checked += 1
        actual_files = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
        if actual_files != expected_files | {'sha256.sum'}:
            raise ValueError(f'Unexpected or missing files in {folder}')
        for asset in product['assets']:
            safe_member(asset['path'])
            data = (folder / asset['path']).read_bytes()
            if sha256(data) != asset['sha256'] or len(data) != asset['bytes']:
                raise ValueError(f"Manifest mismatch: {asset['path']}")
            inspect_archive(asset['path'], data)
        for document in product['documentation']:
            safe_member(document['path'])
            data = (folder / document['path']).read_bytes()
            if sha256(data) != document['sha256'] or len(data) != document['bytes']:
                raise ValueError(f"Documentation manifest mismatch: {document['path']}")
    print(f'Verified {checked} files against product checksums and manifest.', flush=True)


def verify(directory):
    manifest = json.loads((directory / 'bundle-manifest.json').read_bytes())
    if manifest.get('schema_version', 1) == 1:
        return verify_legacy(directory, manifest)
    if manifest['schema_version'] != 2:
        raise ValueError('Unsupported manifest schema')
    expected = set()

    def checked(relative, digest, size=None):
        safe_member(relative)
        data = (directory / relative).read_bytes()
        if relative in expected or sha256(data) != digest or (size is not None and len(data) != size):
            raise ValueError(f'Duplicate or mismatched manifest entry: {relative}')
        expected.add(relative)
        return data

    for product in manifest['products']:
        if not re.fullmatch(r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*', product['id']):
            raise ValueError('Invalid product directory')
        for asset in product['assets']:
            path = asset['path']
            expected_path = PurePosixPath(product['id']) / platform_path(PurePosixPath(path).name)
            if expected_path.as_posix() != path:
                raise ValueError(f'Incorrect platform folder: {path}')
            data = checked(path, asset['sha256'], asset['bytes'])
            sidecar = checked(path + '.sha256', asset['sidecar_sha256'])
            if sidecar.decode('utf-8-sig').split()[0].lower() != asset['sha256']:
                raise ValueError(f'Upstream sidecar mismatch: {path}')
            inspect_archive(path, data)
        for document in product['documentation']:
            checked(document['path'], document['sha256'], document['bytes'])
    for prerequisite in manifest.get('prerequisites', []):
        checked(prerequisite['path'], prerequisite['sha256'], prerequisite['bytes'])
    for relative, content in command_guides(manifest).items():
        checked(relative, sha256(content.encode('utf-8')))
    actual = {p.relative_to(directory).as_posix()
              for product in manifest['products']
              for p in (directory / product['id']).rglob('*') if p.is_file()}
    if actual != expected:
        raise ValueError(f'Unexpected or missing files: {actual.symmetric_difference(expected)}')
    print(f'Verified {len(expected)} files against release hashes and platform guides.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', type=Path, default=ROOT / 'bundle-spec.json')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output', type=Path, help='Build into this new/empty directory')
    group.add_argument('--verify', type=Path, help='Verify an existing snapshot without network access')
    args = parser.parse_args()
    if args.verify:
        verify(args.verify.resolve())
    else:
        output = args.output.resolve()
        build(json.loads(args.spec.read_text(encoding='utf-8')), output)
        verify(output)


if __name__ == '__main__':
    main()
