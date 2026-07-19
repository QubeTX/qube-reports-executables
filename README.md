# Qube TX 300 Series Offline Installers

This repository is an offline snapshot of the native installers and portable
archives for the Qube TX 300-series CLI tools. Download the repository ZIP,
open the product folder, and choose the file for the target platform.

For the normal online install, use each product's versionless managed command
from [reports.qubetx.com](https://reports.qubetx.com). The files here are for
offline deployment, removable media, and manual recovery.

| Tool | Snapshot version | Description |
|------|------------------|-------------|
| **TR300** (`tr300`) | v4.2.2 | Machine reporting |
| **ND300** (`nd300`, `speedqx`) | v3.7.3 | Network diagnostics |
| **SD300** (`sd300`) | v2.0.2 | System diagnostics and live hardware monitoring |

See [USER-INSTALL-GUIDE.md](./USER-INSTALL-GUIDE.md) for step-by-step install
instructions.

## Folder Layout

Each product folder contains:

- `macos/`: one signed, notarized universal `.pkg` for Apple Silicon and Intel.
- `windows/`: Global and Corporate MSI/EXE installers plus a portable ZIP.
- `linux/`: x86_64 GNU, x86_64 musl, and ARM64 GNU archives.
- `sha256.sum`: checksums for every bundled artifact and sidecar.

Products appear in this order throughout the bundle:

1. `TR300-qube-machine-report/`
2. `ND300-qube-network-diagnostics/`
3. `SD300-qube-system-diagnostics/`

## Stable Artifact Names

Release numbers are intentionally absent from installer and archive filenames.
The upstream `releases/latest/download/...` URLs therefore stay stable while
new releases replace the bytes behind the latest channel.

### TR300 v4.2.2

- macOS: `tr300-universal-apple-darwin.pkg`
- Windows Global: `tr300-x86_64-pc-windows-msvc.msi` or `tr300-x86_64-pc-windows-msvc-setup.exe`
- Windows Corporate: `tr300-x86_64-pc-windows-msvc-corporate.msi` or `tr300-x86_64-pc-windows-msvc-corporate-setup.exe`
- Windows portable: `tr300-x86_64-pc-windows-msvc.zip`
- Linux: `tr300-{x86_64,aarch64}-unknown-linux-*.tar.xz`

### ND300 v3.7.3

- macOS: `nd300-universal-apple-darwin.pkg`
- Windows Global: `nd300-x86_64-pc-windows-msvc.msi` or `nd300-x86_64-pc-windows-msvc-setup.exe`
- Windows Corporate: `nd300-x86_64-pc-windows-msvc-corporate.msi` or `nd300-x86_64-pc-windows-msvc-corporate-setup.exe`
- Windows portable: `nd300-x86_64-pc-windows-msvc.zip`
- Linux: `nd300-{x86_64,aarch64}-unknown-linux-*.tar.xz`

### SD300 v2.0.2

- macOS: `sd300-macos-universal.pkg`
- Windows Global: `sd300-windows-x64-global.msi` or `sd300-windows-x64-global.exe`
- Windows Corporate: `sd300-windows-x64-corporate.msi` or `sd300-windows-x64-corporate.exe`
- Windows portable: `tr300-tui-x86_64-pc-windows-msvc.zip`
- Linux: `tr300-tui-{x86_64,aarch64}-unknown-linux-*.tar.xz`

The `tr300-tui` archive prefix is SD300's historical crates.io package name;
the executable inside remains `sd300`.

## Install Behavior

Native installations retain their owner and channel. Running `tr300 update`,
`nd300 update`, or `sd300 update` from an MSI, EXE, or PKG installation fetches
and runs the same channel again. A deliberate fresh official install represents
the user's newest intent, including a reinstall or downgrade, when ownership
and scope can be resolved safely.

Use Global installers for a machine-wide deployment that can request
administrator approval. Use Corporate installers for the per-user/no-admin
channel. The portable ZIP and Linux archives do not create a native installer
registration.

## Verify Checksums

From inside a product folder:

```bash
# Linux
sha256sum -c sha256.sum

# macOS
shasum -a 256 -c sha256.sum
```

On Windows PowerShell, compare a file with its sidecar:

```powershell
(Get-FileHash .\windows\sd300-windows-x64-global.msi -Algorithm SHA256).Hash
Get-Content .\windows\sd300-windows-x64-global.msi.sha256
```

## Sources

- [QubeTX/qube-machine-report](https://github.com/QubeTX/qube-machine-report)
- [QubeTX/qube-network-diagnostics](https://github.com/QubeTX/qube-network-diagnostics)
- [QubeTX/qube-system-diagnostics](https://github.com/QubeTX/qube-system-diagnostics)

All bundled bytes are downloaded from the corresponding public GitHub Release
and verified against its adjacent SHA-256 sidecar before this snapshot is
published.
