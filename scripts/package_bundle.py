#!/usr/bin/env python3
"""Create the offline landing page, full checksum list, and reproducible release ZIP."""
import argparse
import hashlib
from collections import defaultdict
from html import escape
import json
from pathlib import Path, PurePosixPath
import zipfile

from build_bundle import verify

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = ['README.md', 'USER-INSTALL-GUIDE.md', 'CHANGELOG.md', 'HUMAN_CHANGELOG.md',
              'bundle-manifest.json', 'bundle-spec.json', 'index.html', 'assets/offline-toolkit.svg', 'qube-tx-build-runbook.md']


def landing(manifest):
    folders = defaultdict(list)
    for product in manifest['products']:
        for asset in product['assets']:
            path = PurePosixPath(asset['path'])
            folders[path.parent].append(
                f'<li><a href="{escape(path.as_posix())}">{escape(product["id"])} · {escape(path.name)}</a>'
                f' <small>{asset["bytes"] / 1048576:.1f} MiB</small></li>')
    sections = []
    for product in manifest['products']:
        options = []
        for folder, links in sorted(folders.items()):
            if folder.parts[0] != product['id']:
                continue
            label = ' / '.join(folder.parts[1:])
            options.append(f'<details><summary>{escape(label)}</summary>'
                           f'<p><a href="{escape(folder.as_posix())}/README.md">Terminal install command</a></p>'
                           f'<ul>{"".join(links)}</ul></details>')
        sections.append(f'<section><h2>{product["id"]} {product["tag"]}</h2>{"".join(options)}</section>')
    manuals = ''.join(f'<li><a href="{p["id"]}/Manuals/upstream/README.md">{p["id"]} {p["tag"]} manual</a>'
                      f' · <a href="{p["id"]}/Manuals/RELEASE-NOTES.md">Release notes</a></li>'
                      for p in manifest['products'])
    runtime = ''
    if manifest.get('prerequisites'):
        runtime = ('<p>SD-300 Desktop on Windows uses the Microsoft Visual C++ x64 runtime. '
                   'If your computer needs it, the Windows command guides open the '
                   '<a href="SD-300/Windows/x64/Runtime/README.md">included offline runtime installer</a>. '
                   'IT can install this prerequisite before a Corporate deployment. Windows N also requires '
                   'the Media Feature Pack for your Windows release.</p>')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>QubeTX offline bundle {manifest['bundle_version']}</title>
<style>body{{max-width:1040px;margin:auto;padding:32px 24px;background:#faf9f6;color:#222;font:17px/1.65 system-ui,sans-serif}}h1,h2,h3{{line-height:1.2}}h1{{font-size:clamp(32px,6vw,54px);margin-bottom:12px}}h2{{margin-top:0}}small{{font-size:.8em;color:#555}}a{{color:#653166;text-underline-offset:3px;overflow-wrap:anywhere}}code,pre{{font:14px/1.6 ui-monospace,monospace}}pre{{padding:16px;background:#eee;overflow:auto}}header{{padding-bottom:24px;border-bottom:2px solid #222}}section{{border-bottom:1px solid #ccc;padding:28px 0}}details{{padding:10px 0}}summary{{cursor:pointer;font-weight:600}}li{{margin:8px 0}}.note{{padding:18px 22px;background:#f0e9f0;border-left:4px solid #653166}}footer{{padding-top:24px}}</style></head>
<body><header><img src="assets/offline-toolkit.svg" width="64" height="64" alt=""><p>QUBETX · Snapshot {manifest['snapshot_date']} · Bundle {manifest['bundle_version']}</p>
<h1>Your offline toolkit</h1><p>TR-300, ND-300 with SpeedQX, and SD-300 with its desktop app. Open this page from the extracted folder; it needs no internet, JavaScript, or external fonts.</p></header>
<section><h2>Choose your installer</h2>
<p>Choose your tool, then the destination computer’s operating system and processor. On Windows, choose Standard (Global) for all users or Corporate for your account, then MSI or EXE. For upgrades, use the same edition and format as your existing installation.</p>
<p>On Mac, the universal PKG supports both Intel and Apple Silicon. The TR-300 and ND-300 compatibility DMGs contain the same PKGs. On Linux, match the processor and C library. Portable CLI and Desktop downloads have separate folders.</p>
<p>Extract the entire ZIP. Open PowerShell on Windows or a terminal on macOS or Linux in the folder containing your chosen file. Paste the single line from its README and press Enter. SD-300 native installers include its desktop app.</p>
{runtime}<p><a href="USER-INSTALL-GUIDE.md">Installation and upgrade guide</a> · <a href="SHA256SUMS.txt">Checksums</a></p></section>
{''.join(sections)}
<section><h2>Product manuals</h2><ul>{manuals}</ul>
<p>The manuals, licenses and command guides are available offline. Internet speed tests, public connectivity checks and self-updates need a network connection.</p></section>
<footer><a href="README.md">Bundle inventory and verification</a></footer></body></html>
'''


def package(root, destination):
    if destination.exists():
        raise ValueError('Release ZIP already exists; choose a fresh output path.')
    verify(root)
    manifest = json.loads((root / 'bundle-manifest.json').read_text(encoding='utf-8'))
    (root / 'index.html').write_text(landing(manifest), encoding='utf-8', newline='\n')
    files = [root / name for name in ROOT_FILES]
    files += [root / 'scripts' / name for name in
              ['Verify-Bundle.ps1', 'build_bundle.py', 'bundle_layout.py', 'package_bundle.py']]
    for product in manifest['products']:
        files += [p for p in (root / product['id']).rglob('*') if p.is_file()]
    files = sorted(files, key=lambda p: p.relative_to(root).as_posix())
    checksums = ''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root).as_posix()}\n' for p in files)
    (root / 'SHA256SUMS.txt').write_text(checksums, encoding='utf-8', newline='\n')
    files.append(root / 'SHA256SUMS.txt')
    destination.parent.mkdir(parents=True, exist_ok=True)
    year, month, day = map(int, manifest['snapshot_date'].split('-'))
    prefix = 'qubetx-offline-bundle/'
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in files:
            info = zipfile.ZipInfo(prefix + path.relative_to(root).as_posix(), (year, month, day, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    destination.with_name(destination.name + '.sha256').write_text(f'{digest}  {destination.name}\n', encoding='utf-8', newline='\n')
    print(f'Packaged {len(files)} files, {destination.stat().st_size / 1048576:.1f} MiB, SHA-256 {digest}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--zip', type=Path, required=True)
    args = parser.parse_args()
    package(args.root.resolve(), args.zip.resolve())
