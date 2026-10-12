# QubeTX Offline Toolkit

**Bundle 3.0.0 · October 11, 2026**

Download [qubetx-offline-bundle.zip](https://github.com/QubeTX/qube-reports-executables/releases/latest/download/qubetx-offline-bundle.zip), extract it, and open **index.html**. This local start page uses no external services, fonts, or JavaScript. The ZIP includes official installers, portable archives, matching documentation, licenses, and checksums.

| Product | Included release | Commands and purpose |
|---|---|---|
| TR-300 | **4.4.0** | `tr300`, `report`: system reports and explicit JSON/Markdown export |
| ND-300 | **4.0.1** | `nd300`, `speedqx`: network diagnostics and Methodology v5 throughput tests |
| SD-300 | **4.1.0** | `sd300`: terminal diagnostics, snapshots, and the native desktop monitor |

This is a dated snapshot, not a live mirror. WB-300 and Shaughv OS are not included. These binaries come from the exact published tags recorded in `bundle-manifest.json`; no local development build is substituted.

## What's inside

Each product has `windows/`, `macos/`, `linux/`, `docs/`, and a product-level `sha256.sum`.

- **Windows x64:** Global and Corporate MSI/EXE installers plus a portable command-line ZIP. Global installs machine-wide and requires administrator approval; Corporate installs per user. SD-300 also includes a separate portable GUI ZIP.
- **macOS:** a universal PKG for Intel and Apple Silicon, plus architecture-specific command-line archives. SD-300 also includes the universal GUI app ZIP. Legacy compatibility DMGs are intentionally omitted.
- **Linux:** command-line archives for x64 GNU, ARM64 GNU, and x64 musl. SD-300 includes matching GUI archives with their private runtime. Use a compatible distribution and graphical desktop for the GUI; system libc, kernel, display, and driver support still come from the host.
- **Documentation:** each product's published README, changelog, license, release notes, Markdown documents, and available man pages are stored locally. Supporting images and external links are not mirrored. The current bundle install guide is the authority for offline setup; upstream READMEs also describe online installation.
- **Integrity:** original upstream `.sha256` sidecars accompany all 38 payloads. The manifest records immutable source URLs, release commits, sizes, and SHA-256 hashes. `SHA256SUMS.txt` covers the complete curated bundle except itself.

Product folders are `TR300-qube-machine-report`, `ND300-qube-network-diagnostics`, and `SD300-qube-system-diagnostics`.

## Offline scope

No package manager or Rust toolchain is needed to install the included prebuilt files. Initial download requires a connected computer; copy the extracted folder or ZIP to the destination computer.

Offline installation does **not** make network services work without connectivity. ND-300 can inspect available local state, but public DNS, public-IP lookups, remote routes, throughput tests, and network recovery verification require the relevant network. SpeedQX needs internet for its remote tests. Self-update and downloading replacement assets also need internet. TR-300 and SD-300 local readings remain subject to available hardware and OS permissions.

SD-300 native MSI/EXE/PKG installers contain both the CLI and desktop app. Separate portable GUI archives can be opened directly while preserving their full folder structure; they do not establish managed ownership. Terminal-only use remains available through the CLI archive.

Read [USER-INSTALL-GUIDE.md](USER-INSTALL-GUIDE.md) before upgrading an existing managed installation, particularly SD-300 3.x to 4.x.

## Verify integrity

The release ZIP has a sibling `qubetx-offline-bundle.zip.sha256` file. Verify that before extraction when possible. After extraction, run from the bundle folder:

```sh
# Linux
sha256sum -c SHA256SUMS.txt
# macOS
shasum -a 256 -c SHA256SUMS.txt
```

```powershell
# Windows; uses only the local checksum list and local files
.\scripts\Verify-Bundle.ps1
```

If your policy prevents running scripts, compare an individual file manually:

```powershell
(Get-FileHash .\TR300-qube-machine-report\windows\tr300-x86_64-pc-windows-msvc.msi -Algorithm SHA256).Hash
Get-Content .\TR300-qube-machine-report\windows\tr300-x86_64-pc-windows-msvc.msi.sha256
```

Checksums detect changed bytes; they are not a substitute for trusting the source or checking the publisher. Do not bypass OS or organizational restrictions to install these tools.

## Rebuilding and future refreshes

See [qube-tx-build-runbook.md](qube-tx-build-runbook.md). `bundle-spec.json` is an explicit product/asset allowlist. `scripts/build_bundle.py` verifies upstream checksums and GitHub digests, validates archives, and copies documentation from the pinned release commit. `scripts/package_bundle.py` generates the local start page and a deterministic ZIP from a curated file list, excluding Git data and historical build notes.

## Sources and licenses

- [TR-300 v4.4.0](https://github.com/QubeTX/qube-machine-report/releases/tag/v4.4.0)
- [ND-300 v4.0.1](https://github.com/QubeTX/qube-network-diagnostics/releases/tag/v4.0.1)
- [SD-300 v4.1.0](https://github.com/QubeTX/qube-system-diagnostics/releases/tag/v4.1.0)

Each product retains its upstream license; bundled GUI dependencies retain the notices inside their official archive. Binaries are redistributed unchanged, without re-signing or repackaging their inner installers.
