# Qube TX 300 Series User Install Guide

This guide installs the tools from the offline bundle. No internet connection
or package manager is required on the destination computer.

| Tool | What it does | Snapshot version |
|------|--------------|------------------|
| **TR300** | Machine reporting | v4.2.2 |
| **ND300** | Network diagnostics | v3.7.3 |
| **SD300** | System diagnostics and live monitoring | v2.0.2 |

## 1. Choose a Product Folder

1. `TR300-qube-machine-report`
2. `ND300-qube-network-diagnostics`
3. `SD300-qube-system-diagnostics`

SD300 is listed immediately after ND300 throughout this bundle.

## 2. Choose the Platform File

### macOS

The universal PKG works on both Apple Silicon and Intel Macs.

| Product | File in `macos/` |
|---------|------------------|
| TR300 | `tr300-universal-apple-darwin.pkg` |
| ND300 | `nd300-universal-apple-darwin.pkg` |
| SD300 | `sd300-macos-universal.pkg` |

### Windows

Choose one channel. Global is the normal machine-wide installer and can request
administrator approval. Corporate is the per-user/no-admin channel. MSI and EXE
are equivalent installer formats within the selected channel. ZIP is portable.

| Product | Global MSI | Corporate MSI | Portable ZIP |
|---------|------------|---------------|--------------|
| TR300 | `tr300-x86_64-pc-windows-msvc.msi` | `tr300-x86_64-pc-windows-msvc-corporate.msi` | `tr300-x86_64-pc-windows-msvc.zip` |
| ND300 | `nd300-x86_64-pc-windows-msvc.msi` | `nd300-x86_64-pc-windows-msvc-corporate.msi` | `nd300-x86_64-pc-windows-msvc.zip` |
| SD300 | `sd300-windows-x64-global.msi` | `sd300-windows-x64-corporate.msi` | `tr300-tui-x86_64-pc-windows-msvc.zip` |

The same `windows/` folder also contains Global and Corporate `.exe` installers.

### Linux

Run `uname -m` in a terminal:

- `x86_64`: choose the `x86_64-unknown-linux-gnu` archive for most distributions.
- `aarch64`: choose the `aarch64-unknown-linux-gnu` archive.
- Alpine/musl on x86_64: choose `x86_64-unknown-linux-musl`.

TR300 archive names start with `tr300-`, ND300 with `nd300-`, and SD300 with
`tr300-tui-`. The executable inside the SD300 archive is still named `sd300`.

## 3. Install

### macOS PKG

1. Double-click the product's `.pkg` file.
2. Follow Apple Installer.
3. Open Terminal and run `tr300`, `nd300`, or `sd300`.

The packages are signed, notarized, and stapled. A later CLI update remains on
the same PKG channel.

### Windows MSI or EXE

1. Double-click the selected installer.
2. Approve the publisher and elevation prompt when the selected channel requires it.
3. Finish the installer and open a new PowerShell or Command Prompt window.
4. Run `tr300`, `nd300`, or `sd300`.

Do not bypass a publisher warning blindly. Verify the SHA-256 sidecar and confirm
that the file came from this bundle or the product's official GitHub Release.
A later CLI update remains on the same Global/Corporate and MSI/EXE channel.

### Windows Portable ZIP

1. Right-click the ZIP and select **Extract All**.
2. Open a terminal in the extracted folder.
3. Run `tr300.exe`, `nd300.exe`, or `sd300.exe`.

### Linux Archive

```bash
tar -xf <exact-downloaded-filename>.tar.xz
find . -type f \( -name tr300 -o -name nd300 -o -name sd300 \)
chmod +x ./<extracted-directory>/<command>
./<extracted-directory>/<command>
```

To make the command available system-wide:

```bash
sudo install -m 0755 ./<extracted-directory>/<command> /usr/local/bin/<command>
```

## Update and Uninstall

Installed releases support their product lifecycle commands:

```text
tr300 update       tr300 uninstall
nd300 update       nd300 uninstall
sd300 update       sd300 uninstall
```

The updater reuses the proven install channel. Deliberately launching another
official installer is treated as the user's latest install choice when the
transition can be completed safely; conflicting ownership stops before the
working installation is changed.

## Verify a Download

Every artifact has a `.sha256` sidecar, and each product folder has a complete
`sha256.sum` file. See [README.md](./README.md#verify-checksums) for commands.
