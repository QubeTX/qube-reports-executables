# Qube TX — Cross-Platform Build & Distribution Runbook

**Author:** Emmett Shaughnessy / Qube TX  
**Last Updated:** February 25, 2026  
**Build Mothership:** macOS (Apple Silicon)  
**Secondary Build Machine:** Windows (for .msi only)

---

## Quick Path — Download Pre-Built Releases (Recommended)

> **You probably don't need to build anything locally.** All three repos have cargo-dist CI configured and publish complete release artifacts to GitHub on every tagged release. This section covers how to grab those artifacts directly.

### Available Releases

| Tool | Repo | Version | Artifacts |
|------|------|---------|-----------|
| **TR300** | `QubeTX/qube-machine-report` | v3.6.0 | 6 platform binaries + MSI + installers |
| **ND300** | `QubeTX/qube-network-diagnostics` | v2.6.0 | 6 platform binaries + MSI + installers |
| **SD300** | `QubeTX/qube-system-diagnostics` | v1.2.1 | 6 platform binaries + MSI + installers |

Each release includes:
- **macOS**: aarch64 (Apple Silicon) + x86_64 (Intel) `.tar.xz`
- **Windows**: x86_64 `.msi` installer + `.zip` portable archive
- **Linux**: aarch64 (glibc) + x86_64 (glibc) + x86_64 (musl/Alpine) `.tar.xz`
- **Installer scripts**: shell script (macOS/Linux) + PowerShell script (Windows)
- **SHA256 checksums** for integrity verification

### Download Commands

```bash
# TR300
gh release download v3.6.0 --repo QubeTX/qube-machine-report --dir ./tr300-release

# ND300
gh release download v2.6.0 --repo QubeTX/qube-network-diagnostics --dir ./nd300-release

# SD300
gh release download v1.2.1 --repo QubeTX/qube-system-diagnostics --dir ./sd300-release
```

### macOS Code Signing (Post-Download)

The CI-built macOS binaries are **unsigned**. If you have a Developer ID certificate, sign them locally for a better user experience (no Gatekeeper quarantine):

```bash
# Extract the binary
tar -xf tr-300-aarch64-apple-darwin.tar.xz
cd tr-300-aarch64-apple-darwin

# Sign with your Developer ID (enables hardened runtime)
codesign --sign "Developer ID Application: YOUR NAME (TEAMID)" --options runtime --force tr300
codesign --verify --verbose tr300

# Package as a DMG for easy distribution
mkdir staging && cp tr300 staging/
hdiutil create -volname "TR300-AppleSilicon" -srcfolder staging -ov -format UDZO tr300-aarch64.dmg
codesign --sign "Developer ID Application: YOUR NAME (TEAMID)" tr300-aarch64.dmg
```

If notarization is set up (`xcrun notarytool store-credentials`), you can also notarize the DMG to eliminate all Gatekeeper warnings:

```bash
xcrun notarytool submit tr300-aarch64.dmg --keychain-profile "notarytool-profile" --wait
xcrun stapler staple tr300-aarch64.dmg
```

### When to Use the Full Build Pipeline (Below)

The rest of this runbook (Phases 1–5) is only needed if you:
- Want to build from source for a modified or patched version
- Need installer formats not produced by cargo-dist (`.deb`, `.AppImage`, NSIS `.exe`)
- Want Windows ARM64 builds (not included in CI releases)
- Need to set up your own CI/CD pipeline

For most distribution scenarios, the pre-built releases above are the recommended approach.

---

## Overview

This runbook covers the full packaging pipeline for three Qube TX CLI tools:

| Codename | Crate Name | Description |
|----------|------------|-------------|
| **TR300** | `qube-machine-report` | Machine reporting tool |
| **ND300** | `qube-network-diagnostics` | Network diagnostics tool |
| **SD300** | `qube-system-diagnostics` | System diagnostics tool |

All three are built from the Mac, packaged into offline installers for every major OS and architecture, then collected into a single distribution repository. The only exception is `.msi` (Windows Installer), which requires WiX Toolset on a Windows machine.

---

## Target Matrix

| OS | Architecture | Format | Built From |
|----|-------------|--------|------------|
| macOS | Intel (x86_64) | `.dmg` | Mac |
| macOS | Apple Silicon (aarch64) | `.dmg` | Mac |
| Windows | x86_64 | `.exe` (NSIS) | Mac |
| Windows | x86_64 | `.msi` (WiX) | **Windows** |
| Windows | aarch64 (ARM64) | `.exe` (NSIS) | Mac |
| Linux | x86_64 | `.deb` | Mac (via `cross`) |
| Linux | x86_64 | `.AppImage` | Mac (via `cross`) |
| Linux | aarch64 (ARM64/RPi) | `.deb` | Mac (via `cross`) |
| Linux | aarch64 (ARM64/RPi) | `.AppImage` | Mac (via `cross`) |

> **Note on Windows ARM64:** The `aarch64-pc-windows-gnullvm` target is available but still considered tier 2 in Rust. NSIS can wrap it, but test on actual ARM Windows hardware before distributing. If it causes issues, drop it and note that ARM Windows users can run the x86_64 `.exe` under emulation.

---

## Distribution Repo Structure

The distribution repo is `qube-reports-executables`:

```
qube-reports-executables/
├── README.md                          # Install instructions per OS
├── TR300-qube-machine-report/
│   ├── macos/
│   │   ├── qube-machine-report-x86_64.dmg
│   │   └── qube-machine-report-aarch64.dmg
│   ├── windows/
│   │   ├── qube-machine-report-x86_64-setup.exe
│   │   ├── qube-machine-report-x86_64.msi
│   │   └── qube-machine-report-aarch64-setup.exe   # if viable
│   └── linux/
│       ├── qube-machine-report-x86_64.deb
│       ├── qube-machine-report-x86_64.AppImage
│       ├── qube-machine-report-aarch64.deb
│       └── qube-machine-report-aarch64.AppImage
├── ND300-qube-network-diagnostics/
│   ├── macos/
│   ├── windows/
│   └── linux/
└── SD300-qube-system-diagnostics/
    ├── macos/
    ├── windows/
    └── linux/
```

---

## Phase 1: One-Time Mac Setup

### 1.1 — Install System Dependencies

```bash
# Cross-compilation toolchains and packaging utilities
brew install nsis dpkg mingw-w64

# Docker Desktop is REQUIRED for Linux cross-compilation
# Download from: https://www.docker.com/products/docker-desktop/
# Make sure Docker is running before any `cross` commands
```

### 1.2 — Install Rust Tooling

```bash
# The packager itself
cargo install cargo-packager --locked

# Docker-based cross-compiler for Linux targets
cargo install cross --git https://github.com/cross-rs/cross

# Add all target architectures
rustup target add x86_64-apple-darwin        # Mac Intel
rustup target add aarch64-apple-darwin       # Mac Silicon (you likely already have this)
rustup target add x86_64-pc-windows-gnu      # Windows x86_64
rustup target add aarch64-pc-windows-gnullvm # Windows ARM64
rustup target add x86_64-unknown-linux-gnu   # Linux x86_64
rustup target add aarch64-unknown-linux-gnu  # Linux ARM64 (RPi 4/5, edge devices)
```

### 1.3 — macOS Code Signing Setup

Since you have an Apple Developer account, CLI signing is straightforward and prevents Gatekeeper warnings for recipients:

```bash
# List your available signing identities
security find-identity -v -p codesigning

# You should see something like:
#   1) ABCDEF1234... "Developer ID Application: Your Name (TEAMID)"
#
# Note the full identity string — you'll need it below.
```

If you DON'T see a "Developer ID Application" certificate:
1. Open Xcode → Settings → Accounts → Manage Certificates
2. Click `+` → "Developer ID Application"
3. Or generate via Apple Developer portal → Certificates, Identifiers & Profiles

For **notarization** (so users don't even need to right-click > Open):

```bash
# Store your Apple ID credentials in the keychain (one-time)
xcrun notarytool store-credentials "notarytool-profile" \
  --apple-id "your@email.com" \
  --team-id "YOUR_TEAM_ID" \
  --password "app-specific-password"
```

Generate the app-specific password at https://appleid.apple.com/account/manage → Sign-In and Security → App-Specific Passwords.

---

## Phase 2: Configure Each Repo's Cargo.toml

Add this block to each project's `Cargo.toml`. Adjust `product-name` and `identifier` per project.

### TR300 — qube-machine-report

```toml
[package.metadata.packager]
product-name = "Qube Machine Report"
identifier = "com.qubetx.machine-report"
description = "TR300 — Machine reporting and diagnostics tool by Qube TX"
publisher = "Qube TX"
out-dir = "installers"

# macOS code signing (remove if not signing)
[package.metadata.packager.macos]
signing-identity = "Developer ID Application: Your Name (TEAMID)"

[package.metadata.packager.nsis]
install-mode = "currentUser"
```

### ND300 — qube-network-diagnostics

```toml
[package.metadata.packager]
product-name = "Qube Network Diagnostics"
identifier = "com.qubetx.network-diagnostics"
description = "ND300 — Network diagnostics and analysis tool by Qube TX"
publisher = "Qube TX"
out-dir = "installers"

[package.metadata.packager.macos]
signing-identity = "Developer ID Application: Your Name (TEAMID)"

[package.metadata.packager.nsis]
install-mode = "currentUser"
```

### SD300 — qube-system-diagnostics

```toml
[package.metadata.packager]
product-name = "Qube System Diagnostics"
identifier = "com.qubetx.system-diagnostics"
description = "SD300 — System diagnostics and health check tool by Qube TX"
publisher = "Qube TX"
out-dir = "installers"

[package.metadata.packager.macos]
signing-identity = "Developer ID Application: Your Name (TEAMID)"

[package.metadata.packager.nsis]
install-mode = "currentUser"
```

---

## Phase 3: Build Script (Run From Mac)

For efficiency, here's a shell script you can drop into each repo (or adapt into one master script). Run it from the project root.

### `build-all.sh`

```bash
#!/bin/bash
set -e

PROJECT_NAME=$(cargo metadata --no-deps --format-version 1 | jq -r '.packages[0].name')
echo "========================================="
echo " Building installers for: $PROJECT_NAME"
echo "========================================="

# Ensure Docker is running (needed for cross/Linux builds)
if ! docker info > /dev/null 2>&1; then
  echo "ERROR: Docker is not running. Start Docker Desktop and try again."
  exit 1
fi

mkdir -p installers

# ── macOS ──────────────────────────────────────────────
echo ""
echo "▸ Building macOS (Apple Silicon)..."
cargo packager --release --target aarch64-apple-darwin --formats dmg

echo "▸ Building macOS (Intel)..."
cargo packager --release --target x86_64-apple-darwin --formats dmg

# ── Windows (NSIS .exe) ───────────────────────────────
echo ""
echo "▸ Building Windows x86_64 (NSIS)..."
cargo packager --release --target x86_64-pc-windows-gnu --formats nsis

echo "▸ Building Windows ARM64 (NSIS)..."
cargo packager --release --target aarch64-pc-windows-gnullvm --formats nsis

# ── Linux (via cross + Docker) ────────────────────────
echo ""
echo "▸ Building Linux x86_64 (.deb + .AppImage)..."
cross build --release --target x86_64-unknown-linux-gnu
cargo packager --release --target x86_64-unknown-linux-gnu --formats deb,app-image

echo "▸ Building Linux ARM64 (.deb + .AppImage)..."
cross build --release --target aarch64-unknown-linux-gnu
cargo packager --release --target aarch64-unknown-linux-gnu --formats deb,app-image

# ── Optional: Notarize macOS builds ───────────────────
echo ""
echo "▸ Notarizing macOS builds..."
for dmg in installers/*.dmg; do
  if [ -f "$dmg" ]; then
    echo "  Submitting $dmg for notarization..."
    xcrun notarytool submit "$dmg" --keychain-profile "notarytool-profile" --wait
    xcrun stapler staple "$dmg"
    echo "  ✓ $dmg notarized and stapled"
  fi
done

echo ""
echo "========================================="
echo " All builds complete for: $PROJECT_NAME"
echo " Output: ./installers/"
echo "========================================="
ls -lh installers/
```

Make it executable:

```bash
chmod +x build-all.sh
```

### Running It

```bash
# From each project root:
cd ~/repos/qube-machine-report && ./build-all.sh
cd ~/repos/qube-network-diagnostics && ./build-all.sh
cd ~/repos/qube-system-diagnostics && ./build-all.sh
```

---

## Phase 4: Collect Into Distribution Repo

After all three projects have built, copy the outputs into the distribution repo.

### `collect-releases.sh` (run from anywhere)

```bash
#!/bin/bash
set -e

DIST_REPO="$HOME/repos/qube-reports-executables"
PROJECTS=(
  "TR300-qube-machine-report:$HOME/repos/qube-machine-report"
  "ND300-qube-network-diagnostics:$HOME/repos/qube-network-diagnostics"
  "SD300-qube-system-diagnostics:$HOME/repos/qube-system-diagnostics"
)

for entry in "${PROJECTS[@]}"; do
  DIST_NAME="${entry%%:*}"
  SRC_DIR="${entry##*:}"
  
  echo "Collecting $DIST_NAME..."
  
  # Create directory structure
  mkdir -p "$DIST_REPO/$DIST_NAME/macos"
  mkdir -p "$DIST_REPO/$DIST_NAME/windows"
  mkdir -p "$DIST_REPO/$DIST_NAME/linux"
  
  # Copy by file extension into correct OS folders
  cp "$SRC_DIR"/installers/*.dmg       "$DIST_REPO/$DIST_NAME/macos/"    2>/dev/null || echo "  (no .dmg files)"
  cp "$SRC_DIR"/installers/*.exe       "$DIST_REPO/$DIST_NAME/windows/"  2>/dev/null || echo "  (no .exe files)"
  cp "$SRC_DIR"/installers/*.deb       "$DIST_REPO/$DIST_NAME/linux/"    2>/dev/null || echo "  (no .deb files)"
  cp "$SRC_DIR"/installers/*.AppImage  "$DIST_REPO/$DIST_NAME/linux/"    2>/dev/null || echo "  (no .AppImage files)"
done

echo ""
echo "Distribution repo populated at: $DIST_REPO"
echo ""
find "$DIST_REPO" -type f -name "*.dmg" -o -name "*.exe" -o -name "*.deb" -o -name "*.AppImage" | sort
```

Then push:

```bash
cd $DIST_REPO
git add -A
git commit -m "Release: TR300, ND300, SD300 — all platforms (except .msi)"
git push
```

---

## Phase 5: Windows Machine — .msi Build

This is the only step that requires your Windows machine. Do this last.

### 5.1 — One-Time Windows Setup

1. **Install Rust** (if not already): https://rustup.rs
2. **Install WiX Toolset v3** (v4 has compatibility issues with cargo-packager as of early 2026):
   - Download from https://wixtoolset.org/docs/wix3/
   - Or via `winget install WixToolset.WiX`
3. **Install cargo-packager:**
   ```powershell
   cargo install cargo-packager --locked
   ```

### 5.2 — Build the .msi Files

```powershell
# Pull each source repo
cd C:\repos\qube-machine-report
git pull
cargo packager --release --formats wix

cd C:\repos\qube-network-diagnostics
git pull
cargo packager --release --formats wix

cd C:\repos\qube-system-diagnostics
git pull
cargo packager --release --formats wix
```

### 5.3 — Add .msi to Distribution Repo

```powershell
cd C:\repos\qube-reports-executables
git pull

# Copy .msi files into the correct locations
copy C:\repos\qube-machine-report\installers\*.msi .\TR300-qube-machine-report\windows\
copy C:\repos\qube-network-diagnostics\installers\*.msi .\ND300-qube-network-diagnostics\windows\
copy C:\repos\qube-system-diagnostics\installers\*.msi .\SD300-qube-system-diagnostics\windows\

git add -A
git commit -m "Release: Add .msi installers for TR300, ND300, SD300"
git push
```

---

## Troubleshooting & Gotchas

### macOS Signing Issues
- If `codesign` fails, make sure your Developer ID certificate is in your login keychain (not System)
- If notarization fails with "invalid signature," you may need to add `--options runtime` to the codesign step — check if cargo-packager supports hardened runtime flags in its config

### Windows ARM64 (.exe)
- The `aarch64-pc-windows-gnullvm` target is **tier 2** in Rust — it compiles but isn't guaranteed to work perfectly
- Test on actual ARM Windows hardware (Surface Pro X, etc.) before distributing
- Fallback: ARM Windows can run x86_64 `.exe` under emulation with minimal performance hit

### Linux Cross-Compilation
- If `cross build` fails, make sure Docker Desktop is running and has enough memory allocated (4GB+ recommended)
- For ARM64 Linux: `cross` uses QEMU emulation inside Docker — builds will be slower than native x86_64
- If AppImage creation fails for ARM targets, fall back to `.deb` only for ARM Linux

### cargo-packager Versions
- The tool is still evolving. If something breaks, pin a specific version: `cargo install cargo-packager@0.x.x --locked`
- Check https://docs.rs/cargo-packager for the latest config schema — field names occasionally change between versions

### File Naming
- cargo-packager may auto-name files differently than expected. After builds, check the `installers/` directory and rename files to match the distribution repo naming convention if needed
- The `collect-releases.sh` script uses glob patterns — adjust if the packager output names don't match

---

## Quick Reference: Full Command Cheat Sheet

### From Mac (all at once per project):
```bash
./build-all.sh
```

### From Windows (per project):
```powershell
cargo packager --release --formats wix
```

### Collect & push:
```bash
./collect-releases.sh
cd ~/repos/qube-reports-executables && git add -A && git commit -m "Release vX.Y.Z" && git push
```

### Then on Windows:
```powershell
# Build .msi, copy to dist repo, push
```
