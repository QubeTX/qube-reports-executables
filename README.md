# Qube TX 300 Series — Offline Installers

Pre-built, offline-ready executables and installers for the three Qube TX CLI tools. Download the file for your OS and architecture, and run it — no package manager or internet connection required.

> **New here?** See the **[User Install Guide](./USER-INSTALL-GUIDE.md)** for plain-English, step-by-step instructions on picking the right file and installing it — no technical background needed.

| Tool | Version | Description |
|------|---------|-------------|
| **TR300** (`tr300`) | v3.6.0 | Machine reporting tool |
| **ND300** (`nd300`) | v2.6.0 | Network diagnostics tool |
| **SD300** (`sd300`) | v1.2.1 | System diagnostics tool |

---

## Repository Structure

```
qube-reports-executables/
├── ND300-qube-network-diagnostics/
│   ├── linux/
│   │   ├── nd-300-aarch64-unknown-linux-gnu.tar.xz          # ARM64 (RPi, Graviton)
│   │   ├── nd-300-aarch64-unknown-linux-gnu.tar.xz.sha256
│   │   ├── nd-300-x86_64-unknown-linux-gnu.tar.xz           # x86_64 (glibc)
│   │   ├── nd-300-x86_64-unknown-linux-gnu.tar.xz.sha256
│   │   ├── nd-300-x86_64-unknown-linux-musl.tar.xz          # x86_64 (musl/Alpine)
│   │   └── nd-300-x86_64-unknown-linux-musl.tar.xz.sha256
│   ├── macos/
│   │   ├── nd300-aarch64-apple-darwin.dmg                    # Apple Silicon (M1/M2/M3/M4)
│   │   └── nd300-x86_64-apple-darwin.dmg                     # Intel Mac
│   ├── windows/
│   │   ├── nd-300-x86_64-pc-windows-msvc.msi                # MSI installer
│   │   ├── nd-300-x86_64-pc-windows-msvc.msi.sha256
│   │   ├── nd-300-x86_64-pc-windows-msvc.zip                # Portable zip
│   │   └── nd-300-x86_64-pc-windows-msvc.zip.sha256
│   └── sha256.sum                                            # Checksums for all release files
├── SD300-qube-system-diagnostics/
│   └── (same structure as ND300, with sd-300 / sd300 prefixes)
├── TR300-qube-machine-report/
│   └── (same structure as ND300, with tr-300 / tr300 prefixes)
├── CHANGELOG.md
├── DISCOVERIES.md
├── README.md
├── USER-INSTALL-GUIDE.md
└── qube-tx-build-runbook.md

13 directories, 39 binary files + 5 docs
```

---

## Installation Instructions

### macOS

The `.dmg` files contain binaries **signed with Developer ID** (ES Development LLC, Team ID: M9D5379H93) and hardened runtime enabled. The full certificate chain is: `Developer ID Application → Developer ID Certification Authority → Apple Root CA`.

1. **Download** the correct `.dmg` for your Mac:
   - **Apple Silicon** (M1/M2/M3/M4): `*-aarch64-apple-darwin.dmg`
   - **Intel**: `*-x86_64-apple-darwin.dmg`

   > Not sure which you have? Click Apple menu () → "About This Mac". If it says "Apple M1" (or M2/M3/M4), use the `aarch64` version. If it says "Intel", use `x86_64`.

2. **Double-click** the `.dmg` to mount it.

3. **Copy the binary** to a convenient location:
   ```bash
   # Option A: Copy to your Desktop
   cp /Volumes/TR300-AppleSilicon/tr300 ~/Desktop/

   # Option B: Copy to /usr/local/bin (available system-wide)
   sudo cp /Volumes/TR300-AppleSilicon/tr300 /usr/local/bin/
   ```

4. **First launch** — since the binaries are signed but not notarized, macOS may still show a Gatekeeper dialog on first run. Either:
   - Right-click the binary in Finder → **Open**, then confirm the dialog (one-time only), or
   - Remove the quarantine attribute: `xattr -d com.apple.quarantine ~/Desktop/tr300`

5. **Run it:**
   ```bash
   ./tr300
   # or if installed to /usr/local/bin:
   tr300
   ```

6. **Eject** the DMG when done (drag to Trash or `hdiutil detach /Volumes/TR300-AppleSilicon`).

---

### Windows

Two options: **MSI installer** (recommended) or **portable zip**.

#### Option A: MSI Installer (Recommended)

1. **Double-click** `tr-300-x86_64-pc-windows-msvc.msi`.
2. Follow the installation wizard. The binary will be added to your PATH automatically.
3. Open **Command Prompt** or **PowerShell** and run:
   ```
   tr300
   ```

> If Windows SmartScreen blocks the installer, click "More info" → "Run anyway".

#### Option B: Portable Zip

1. **Extract** `tr-300-x86_64-pc-windows-msvc.zip` to any folder.
2. Open a terminal in that folder and run:
   ```
   .\tr300.exe
   ```

---

### Linux

1. **Extract** the archive for your architecture:
   ```bash
   # x86_64 (most desktops/servers)
   tar -xf tr-300-x86_64-unknown-linux-gnu.tar.xz

   # x86_64 on Alpine/musl-based distros
   tar -xf tr-300-x86_64-unknown-linux-musl.tar.xz

   # ARM64 (Raspberry Pi 4/5, AWS Graviton, etc.)
   tar -xf tr-300-aarch64-unknown-linux-gnu.tar.xz
   ```

2. **Make executable and run:**
   ```bash
   chmod +x tr300
   ./tr300
   ```

3. **Optional — install system-wide:**
   ```bash
   sudo cp tr300 /usr/local/bin/
   tr300
   ```

---

## Verifying Integrity (SHA256)

Each tool folder contains a `sha256.sum` file with checksums for the original release artifacts.

```bash
# Linux/macOS
cd TR300-qube-machine-report
sha256sum -c sha256.sum

# macOS (if sha256sum not available)
shasum -a 256 -c sha256.sum
```

Individual `.sha256` files are also provided alongside each artifact for quick single-file verification.

---

## Platform Support Summary

| Platform | Architecture | Format | Notes |
|----------|-------------|--------|-------|
| macOS | Apple Silicon (aarch64) | `.dmg` | Signed with Developer ID, hardened runtime |
| macOS | Intel (x86_64) | `.dmg` | Signed with Developer ID, hardened runtime |
| Windows | x86_64 | `.msi` | Standard Windows installer |
| Windows | x86_64 | `.zip` | Portable, no install needed |
| Linux | x86_64 (glibc) | `.tar.xz` | Most distros (Ubuntu, Fedora, etc.) |
| Linux | x86_64 (musl) | `.tar.xz` | Alpine Linux, Docker alpine images |
| Linux | ARM64 (aarch64) | `.tar.xz` | Raspberry Pi, Graviton, etc. |

> **Windows ARM64 note:** No native ARM64 build is included. The x86_64 `.msi` and `.exe` will run under Windows' built-in x86 emulation with no issues.

---

## Source Repos

These binaries are built from the following repositories by cargo-dist CI:

- [QubeTX/qube-machine-report](https://github.com/QubeTX/qube-machine-report) — TR300 v3.6.0
- [QubeTX/qube-network-diagnostics](https://github.com/QubeTX/qube-network-diagnostics) — ND300 v2.6.0
- [QubeTX/qube-system-diagnostics](https://github.com/QubeTX/qube-system-diagnostics) — SD300 v1.2.1

---

## Artifact Details

### macOS DMGs

Each macOS `.dmg` is a UDZO-compressed disk image containing a single signed CLI binary. The binaries were extracted from the upstream cargo-dist `.tar.xz` archives, signed locally with Apple's `codesign` tool, then packaged into DMGs using `hdiutil`.

**Signing details:**
- **Identity:** Developer ID Application: ES Development LLC (M9D5379H93)
- **Certificate chain:** Developer ID Application → Developer ID Certification Authority → Apple Root CA
- **Hardened runtime:** Enabled (`--options runtime`)
- **Timestamp:** Apple's secure timestamp server (embedded in signature)
- **Notarization:** Not notarized — users will see a Gatekeeper dialog on first launch that can be dismissed via right-click → Open

**DMG volume names:**
| File | Volume Name |
|------|-------------|
| `tr300-aarch64-apple-darwin.dmg` | TR300-AppleSilicon |
| `tr300-x86_64-apple-darwin.dmg` | TR300-Intel |
| `nd300-aarch64-apple-darwin.dmg` | ND300-AppleSilicon |
| `nd300-x86_64-apple-darwin.dmg` | ND300-Intel |
| `sd300-aarch64-apple-darwin.dmg` | SD300-AppleSilicon |
| `sd300-x86_64-apple-darwin.dmg` | SD300-Intel |

### Windows MSI Installers

The `.msi` files are produced by cargo-dist's CI pipeline using the WiX toolset. They provide a standard Windows Installer experience: double-click to install, adds the binary to PATH, and supports standard uninstall via Add/Remove Programs.

The `.zip` files are portable alternatives — extract and run, no installation required.

### Linux Archives

The `.tar.xz` archives each contain a directory with the binary and associated files (README, license). Three variants per tool:

- **`gnu` (glibc):** For standard Linux distributions (Ubuntu, Debian, Fedora, RHEL, etc.)
- **`musl`:** For Alpine Linux, Docker alpine-based images, and other musl-libc systems
- **`aarch64-gnu`:** For ARM64 Linux devices (Raspberry Pi 4/5, AWS Graviton, Oracle Ampere, etc.)

---

## File Inventory

**39 files total** across 3 tools and 3 platforms:

| Category | Per Tool | Total |
|----------|---------|-------|
| macOS DMGs | 2 (aarch64 + x86_64) | 6 |
| Windows MSIs | 1 (x86_64) | 3 |
| Windows ZIPs | 1 (x86_64) | 3 |
| Windows MSI checksums | 1 | 3 |
| Windows ZIP checksums | 1 | 3 |
| Linux tar.xz (glibc) | 2 (aarch64 + x86_64) | 6 |
| Linux tar.xz (musl) | 1 (x86_64) | 3 |
| Linux checksums | 3 | 9 |
| SHA256 sum file | 1 | 3 |
| **Total per tool** | **13** | **39** |

---

## Additional Documentation

- **[USER-INSTALL-GUIDE.md](./USER-INSTALL-GUIDE.md)** — Plain-English install guide for non-technical users (start here if you just need to install a tool)
- **[CHANGELOG.md](./CHANGELOG.md)** — Release history and version tracking
- **[DISCOVERIES.md](./DISCOVERIES.md)** — Detailed notes on the build/packaging process, findings about cargo-dist CI, macOS signing, and lessons learned
- **[qube-tx-build-runbook.md](./qube-tx-build-runbook.md)** — Full runbook for building from source or creating custom installer formats (includes a "Quick Path" section for downloading pre-built releases)
