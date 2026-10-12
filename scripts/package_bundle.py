#!/usr/bin/env python3
"""Create the offline landing page, full checksum list, and reproducible release ZIP."""
import argparse
import hashlib
from html import escape
import json
from pathlib import Path
import zipfile

from build_bundle import verify

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = ['README.md', 'USER-INSTALL-GUIDE.md', 'CHANGELOG.md', 'HUMAN_CHANGELOG.md',
              'bundle-manifest.json', 'bundle-spec.json', 'index.html', 'qube-tx-build-runbook.md']


def landing(manifest):
    sections = []
    descriptions = {
        'TR-300': 'System reports, JSON export, and the report companion command.',
        'ND-300': 'Network diagnostics and the SpeedQX throughput test.',
        'SD-300': 'Terminal diagnostics and the native desktop monitor.',
    }
    for product in manifest['products']:
        folder = product['folder']
        details = []
        for platform, label in [('windows', 'Windows x64'), ('macos', 'macOS: Apple Silicon and Intel'), ('linux', 'Linux: x64 and ARM64')]:
            files = [item for item in product['assets'] if item['path'].startswith(platform + '/')]
            links = ''.join(f'<li><a href="{escape(folder + "/" + item["path"])}">{escape(Path(item["path"]).name)}</a> <small>{item["bytes"] / 1048576:.1f} MiB</small></li>' for item in files)
            details.append(f'<details><summary>{label}</summary><ul>{links}</ul></details>')
        docs = f'{folder}/docs/upstream'
        sections.append(f'''<section><h2>{product['id']} <small>{product['tag']}</small></h2>
<p>{descriptions[product['id']]}</p><p>Commands: <code>{', '.join(product['commands'])}</code></p>
{''.join(details)}<p><a href="{docs}/README.md">Product manual</a> · <a href="{docs}/CHANGELOG.md">Product changes</a> · <a href="{folder}/sha256.sum">Checksums</a></p></section>''')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>QubeTX offline bundle {manifest['bundle_version']}</title>
<style>body{{max-width:1040px;margin:auto;padding:32px 24px;background:#faf9f6;color:#222;font:17px/1.65 system-ui,sans-serif}}h1,h2,h3{{line-height:1.2}}h1{{font-size:clamp(32px,6vw,54px);margin-bottom:12px}}h2{{margin-top:0}}small{{font-size:.8em;color:#555}}a{{color:#653166;text-underline-offset:3px;overflow-wrap:anywhere}}code,pre{{font:14px/1.6 ui-monospace,monospace}}pre{{padding:16px;background:#eee;overflow:auto}}header{{padding-bottom:24px;border-bottom:2px solid #222}}section{{border-bottom:1px solid #ccc;padding:28px 0}}details{{padding:10px 0}}summary{{cursor:pointer;font-weight:600}}li{{margin:8px 0}}.note{{padding:18px 22px;background:#f0e9f0;border-left:4px solid #653166}}footer{{padding-top:24px}}</style></head>
<body><header><p>QUBETX · Snapshot {manifest['snapshot_date']} · Bundle {manifest['bundle_version']}</p>
<h1>Your offline toolkit</h1><p>TR-300, ND-300 with SpeedQX, and SD-300 with its desktop app. Open this page from the extracted folder; it needs no internet, JavaScript, or external fonts.</p></header>
<section><h2>Start here</h2><ol><li>Extract the entire bundle first. Keep its folders together.</li><li>Choose a tool below and the files for your operating system.</li><li>Windows: use one MSI or EXE edition. Global needs administrator access; Corporate installs for the current user. macOS: use the universal PKG. Linux: extract the matching archive.</li><li>Open a fresh terminal after installation. Run <code>tr300</code>, <code>nd300</code>, <code>speedqx</code>, or <code>sd300</code>. Native SD-300 installers also install the desktop app; open it from the application menu or run <code>sd300 gui</code>.</li></ol>
<p><a href="USER-INSTALL-GUIDE.md">Full installation and upgrade guide</a> · <a href="README.md">Bundle inventory</a> · <a href="SHA256SUMS.txt">All file checksums</a></p>
<div class="note">Offline refers to installing these files and reading the included documentation. Internet throughput tests, public connectivity checks, downloads, and self-updates still need a network connection. Local measurements remain subject to operating-system permissions and available hardware.</div></section>
{''.join(sections)}
<section><h2>SD-300 portable desktop app</h2><p>The native Windows MSI/EXE and macOS PKG include both terminal and desktop tools. Separate portable GUI archives are also provided for all supported targets.</p>
<ul><li>Windows: extract <code>sd300-gui-windows-x86_64.zip</code> into its own folder. Keep the DLL, assets, licenses and manifest beside <code>sd300-gui.exe</code>, then open that executable.</li><li>macOS: extract <code>sd300-gui-macos-universal.zip</code> and open the app bundle.</li><li>Linux: extract the matching <code>sd300-gui-linux-…tar.xz</code> archive and run <code>./sd300/bin/sd300-gui</code>. Keep the whole <code>sd300/</code> directory. A working graphical desktop and compatible system libc are required.</li></ul>
<p>The CLI archive is separate from these portable GUI files. Extract it separately for terminal use. Portable extraction does not create a managed-install receipt, PATH entry, or application-menu shortcut.</p></section>
<section><h2>Keep companion commands together</h2><p>TR-300 archives contain <code>tr300</code> and <code>report</code>. ND-300 archives contain <code>nd300</code> and <code>speedqx</code>. Extract both companions together. SD-300 CLI archives retain their historical <code>tr300-tui-</code> filename prefix; the command inside is <code>sd300</code>.</p>
<h3>Upgrades</h3><p>For an offline upgrade, run the included official installer matching the existing format and edition. This is particularly important for SD-300 3.x to 4.x. Do not mix MSI and EXE registrations or replace just one file in a managed SD-300 installation. Use the current product guide for ownership conflicts. Self-update commands need internet access.</p>
<h3>Verify before installing</h3><p>Compare a downloaded file's SHA-256 hash with its adjacent <code>.sha256</code> file. The root checksum list covers every file in this bundle except itself. Verification needs no network:</p>
<pre>Linux:   sha256sum -c SHA256SUMS.txt
macOS:   shasum -a 256 -c SHA256SUMS.txt
Windows: .\\scripts\\Verify-Bundle.ps1</pre>
<p>If your operating system or organization blocks an installer, keep that diagnostic and verify the source and checksum. These files do not bypass endpoint policy. Windows packages target x64; ARM64 Windows is not qualified by this bundle.</p></section>
<footer><p>Release binaries are unchanged from their official tagged releases. Product manuals, release notes, licenses, and supporting Markdown documents are included under each product's <code>docs/</code> folder. They can be opened in a text editor; external links and linked media may require internet. The pinned versions and source hashes are recorded in <code>bundle-manifest.json</code>.</p></footer></body></html>
'''


def package(root, destination):
    if destination.exists():
        raise ValueError('Release ZIP already exists; choose a fresh output path.')
    verify(root)
    manifest = json.loads((root / 'bundle-manifest.json').read_text(encoding='utf-8'))
    (root / 'index.html').write_text(landing(manifest), encoding='utf-8', newline='\n')
    files = [root / name for name in ROOT_FILES]
    files += [root / 'scripts/Verify-Bundle.ps1', root / 'scripts/build_bundle.py', root / 'scripts/package_bundle.py']
    for product in manifest['products']:
        files += [p for p in (root / product['folder']).rglob('*') if p.is_file()]
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
