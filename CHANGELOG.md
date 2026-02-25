# Changelog

All notable changes to the `qube-reports-executables` distribution repository are documented in this file.

---

## [1.0.0] — 2026-02-25

### Summary

Initial population of the distribution repository with offline installers for all three Qube TX 300 Series CLI tools, covering macOS (Apple Silicon + Intel), Windows (x86_64), and Linux (x86_64 glibc/musl + ARM64 glibc).

### Added

#### Binaries & Installers (45 files total)

**TR300 — qube-machine-report v3.6.0**
- `macos/tr300-aarch64-apple-darwin.dmg` — Apple Silicon DMG, Developer ID signed
- `macos/tr300-x86_64-apple-darwin.dmg` — Intel Mac DMG, Developer ID signed
- `windows/tr-300-x86_64-pc-windows-msvc.msi` — Windows MSI installer
- `windows/tr-300-x86_64-pc-windows-msvc.zip` — Windows portable archive
- `windows/tr-300-installer.ps1` — PowerShell installer script
- `linux/tr-300-x86_64-unknown-linux-gnu.tar.xz` — Linux x86_64 (glibc)
- `linux/tr-300-x86_64-unknown-linux-musl.tar.xz` — Linux x86_64 (musl/Alpine)
- `linux/tr-300-aarch64-unknown-linux-gnu.tar.xz` — Linux ARM64
- `tr-300-installer.sh` — Shell installer script (macOS/Linux)
- `sha256.sum` — SHA256 checksums for all upstream release artifacts
- Per-artifact `.sha256` checksum files for Linux and Windows archives

**ND300 — qube-network-diagnostics v2.6.0**
- Same set of artifacts as TR300 with `nd-300`/`nd300` naming convention

**SD300 — qube-system-diagnostics v1.2.1**
- Same set of artifacts as TR300 with `sd-300`/`sd300` naming convention

#### macOS Code Signing

All 6 macOS binaries (2 per tool) were signed locally after downloading from GitHub Releases:
- **Signing identity:** Developer ID Application: ES Development LLC (M9D5379H93)
- **Certificate chain:** Developer ID Application → Developer ID Certification Authority → Apple Root CA
- **Hardened runtime:** Enabled (required for future notarization)
- **Timestamps:** Apple's secure timestamp server
- **Format:** Binaries extracted from CI-built `.tar.xz`, signed with `codesign`, packaged into `.dmg` via `hdiutil`

#### Documentation

- `README.md` — Comprehensive install instructions for all platforms with architecture guidance
- `CHANGELOG.md` — This file
- `DISCOVERIES.md` — Detailed process notes, findings, and lessons learned

#### Runbook Update

- Added "Quick Path — Download Pre-Built Releases" section to `qube-tx-build-runbook.md`
- Documents the discovery that cargo-dist CI already produces all needed artifacts
- Includes `gh release download` commands and local macOS signing instructions
- Clarifies that the full local build pipeline (Phases 1–5) is only needed for custom formats

### Source Versions

| Tool | Source Repo | Version | GitHub Release |
|------|-------------|---------|----------------|
| TR300 | `QubeTX/qube-machine-report` | v3.6.0 | [Release](https://github.com/QubeTX/qube-machine-report/releases/tag/v3.6.0) |
| ND300 | `QubeTX/qube-network-diagnostics` | v2.6.0 | [Release](https://github.com/QubeTX/qube-network-diagnostics/releases/tag/v2.6.0) |
| SD300 | `QubeTX/qube-system-diagnostics` | v1.2.1 | [Release](https://github.com/QubeTX/qube-system-diagnostics/releases/tag/v1.2.1) |

### Build Environment

- **Build host:** macOS (Apple Silicon)
- **Download method:** `gh release download` from QubeTX GitHub org
- **Signing tool:** macOS `codesign` (Xcode Command Line Tools)
- **DMG creation:** `hdiutil create` (UDZO compressed)
- **Upstream CI:** cargo-dist (Rust binary distribution toolkit)
