# Discoveries & Process Notes

Notes, findings, and lessons learned during the creation of the `qube-reports-executables` distribution repository. This documents what we discovered about the QubeTX build pipeline, macOS code signing, and the decisions made along the way.

**Date:** February 25, 2026
**Author:** Emmett Shaughnessy / ES Development LLC

---

## Table of Contents

1. [The Big Discovery: cargo-dist CI Already Does Everything](#1-the-big-discovery-cargo-dist-ci-already-does-everything)
2. [Artifact Inventory from GitHub Releases](#2-artifact-inventory-from-github-releases)
3. [Runbook vs. Reality](#3-runbook-vs-reality)
4. [macOS Code Signing Deep Dive](#4-macos-code-signing-deep-dive)
5. [DMG Packaging Process](#5-dmg-packaging-process)
6. [File Naming Conventions in cargo-dist](#6-file-naming-conventions-in-cargo-dist)
7. [SHA256 Checksum Strategy](#7-sha256-checksum-strategy)
8. [Platform Coverage Analysis](#8-platform-coverage-analysis)
9. [Installer Scripts from cargo-dist](#9-installer-scripts-from-cargo-dist)
10. [Recommendations for Future Releases](#10-recommendations-for-future-releases)

---

## 1. The Big Discovery: cargo-dist CI Already Does Everything

The original `qube-tx-build-runbook.md` laid out a comprehensive 5-phase local cross-compilation pipeline involving:
- Rust cross-compilation toolchains
- Docker + `cross` for Linux builds
- NSIS for Windows `.exe` installers
- `cargo-packager` for `.dmg`, `.deb`, `.AppImage` formats
- A separate Windows machine for `.msi` builds via WiX

**What we found:** All three QubeTX repos already have **cargo-dist** configured in their CI/CD pipelines. Every tagged release automatically builds and publishes complete binary artifacts for 6 target platforms — no local build infrastructure needed at all.

The entire local build pipeline described in the runbook is unnecessary for standard distribution. A simple `gh release download` pulls everything needed.

### How cargo-dist Works

[cargo-dist](https://opensource.axo.dev/cargo-dist/) is a Rust tool that automates binary distribution. When configured in a repo, it:

1. Hooks into GitHub Actions (or other CI)
2. On tagged releases, builds the Rust binary for multiple target triples
3. Packages each into platform-appropriate archives (`.tar.xz` for Unix, `.zip`/`.msi` for Windows)
4. Generates installer scripts (shell + PowerShell)
5. Computes SHA256 checksums
6. Uploads everything as GitHub Release assets

The QubeTX repos had this fully configured and working — it just wasn't documented in the distribution runbook.

---

## 2. Artifact Inventory from GitHub Releases

### TR300 — qube-machine-report v3.6.0

| File | Size | Platform |
|------|------|----------|
| `tr-300-aarch64-apple-darwin.tar.xz` | 419 KB | macOS Apple Silicon |
| `tr-300-x86_64-apple-darwin.tar.xz` | 465 KB | macOS Intel |
| `tr-300-x86_64-pc-windows-msvc.msi` | 900 KB | Windows x86_64 MSI |
| `tr-300-x86_64-pc-windows-msvc.zip` | 653 KB | Windows x86_64 portable |
| `tr-300-aarch64-unknown-linux-gnu.tar.xz` | 494 KB | Linux ARM64 (glibc) |
| `tr-300-x86_64-unknown-linux-gnu.tar.xz` | 547 KB | Linux x86_64 (glibc) |
| `tr-300-x86_64-unknown-linux-musl.tar.xz` | 604 KB | Linux x86_64 (musl) |
| `tr-300-installer.sh` | 52 KB | Shell installer |
| `tr-300-installer.ps1` | 21 KB | PowerShell installer |
| `sha256.sum` | 799 B | Checksums |
| `dist-manifest.json` | 25 KB | cargo-dist metadata (not distributed) |
| `source.tar.gz` | 139 KB | Source archive (not distributed) |

### ND300 — qube-network-diagnostics v2.6.0

| File | Size | Platform |
|------|------|----------|
| `nd-300-aarch64-apple-darwin.tar.xz` | 1.7 MB | macOS Apple Silicon |
| `nd-300-x86_64-apple-darwin.tar.xz` | 1.9 MB | macOS Intel |
| `nd-300-x86_64-pc-windows-msvc.msi` | 2.8 MB | Windows x86_64 MSI |
| `nd-300-x86_64-pc-windows-msvc.zip` | 2.6 MB | Windows x86_64 portable |
| `nd-300-aarch64-unknown-linux-gnu.tar.xz` | 1.9 MB | Linux ARM64 (glibc) |
| `nd-300-x86_64-unknown-linux-gnu.tar.xz` | 2.1 MB | Linux x86_64 (glibc) |
| `nd-300-x86_64-unknown-linux-musl.tar.xz` | 2.2 MB | Linux x86_64 (musl) |
| `nd-300-installer.sh` | 52 KB | Shell installer |
| `nd-300-installer.ps1` | 21 KB | PowerShell installer |
| `sha256.sum` | 799 B | Checksums |

### SD300 — qube-system-diagnostics v1.2.1

| File | Size | Platform |
|------|------|----------|
| `sd-300-aarch64-apple-darwin.tar.xz` | 676 KB | macOS Apple Silicon |
| `sd-300-x86_64-apple-darwin.tar.xz` | 745 KB | macOS Intel |
| `sd-300-x86_64-pc-windows-msvc.msi` | 1.2 MB | Windows x86_64 MSI |
| `sd-300-x86_64-pc-windows-msvc.zip` | 996 KB | Windows x86_64 portable |
| `sd-300-aarch64-unknown-linux-gnu.tar.xz` | 759 KB | Linux ARM64 (glibc) |
| `sd-300-x86_64-unknown-linux-gnu.tar.xz` | 833 KB | Linux x86_64 (glibc) |
| `sd-300-x86_64-unknown-linux-musl.tar.xz` | 907 KB | Linux x86_64 (musl) |
| `sd-300-installer.sh` | 52 KB | Shell installer |
| `sd-300-installer.ps1` | 21 KB | PowerShell installer |
| `sha256.sum` | 799 B | Checksums |

### Size Comparison

ND300 is significantly larger than TR300 and SD300 — likely due to network-related dependencies (DNS resolution, TLS, HTTP client libraries). TR300 is the smallest.

---

## 3. Runbook vs. Reality

The runbook envisioned a specific set of output formats. Here's how cargo-dist's output compares:

| Runbook Format | cargo-dist Output | Assessment |
|---------------|-------------------|------------|
| `.dmg` (macOS) | `.tar.xz` → locally signed `.dmg` | Achieved (signed locally) |
| `.exe` NSIS (Windows) | Not produced | Not needed — `.msi` is better |
| `.msi` WiX (Windows) | `.msi` from cargo-dist CI | Identical to what runbook wanted |
| `.deb` (Linux) | Not produced | `.tar.xz` is sufficient — extract and run |
| `.AppImage` (Linux) | Not produced | `.tar.xz` is sufficient — extract and run |
| Windows ARM64 | Not produced | OK — x86_64 runs under Windows emulation |
| musl/Alpine Linux | `.tar.xz` (musl) | Bonus — not in original runbook |
| SHA256 checksums | Full checksum files | Bonus — not in original runbook |
| Installer scripts | Shell + PowerShell | Bonus — not in original runbook |

### Key Insight

The runbook over-engineered the problem. For CLI tools destined for technical users (IT staff running diagnostics), the extract-and-run `.tar.xz` format is perfectly adequate for Linux. The `.deb` and `.AppImage` formats add complexity without much benefit for this use case.

The `.msi` installer from cargo-dist is actually **better** than the NSIS `.exe` approach — MSI is the native Windows packaging format and integrates with Group Policy, SCCM, and enterprise deployment tools.

---

## 4. macOS Code Signing Deep Dive

### Why Sign?

Unsigned macOS binaries downloaded from the internet get quarantined by Gatekeeper. Users see scary "this app is from an unidentified developer" warnings and must navigate System Settings → Privacy & Security to allow execution. Signed binaries show the developer name and can be approved with a simple right-click → Open.

### The Certificate Chain Issue

During the initial signing attempt, all `codesign` operations failed with:

```
Warning: unable to build chain to self-signed root for signer
  "Developer ID Application: ES Development LLC (M9D5379H93)"
errSecInternalComponent
```

**Root cause:** The Apple Worldwide Developer Relations (WWDR) intermediate certificate in the local keychain was expired or missing. macOS needs this certificate to build the trust chain from the Developer ID certificate up to Apple's root CA.

**Fix:** Regenerated local development certificates from the root CA. After this, codesign worked but hit a second issue:

```
Developer ID Application: ES Development LLC (M9D5379H93): ambiguous
  (matches "Developer ID Application: ES Development LLC (M9D5379H93)" and
   "Developer ID Application: ES Development LLC (M9D5379H93)"
   in /Users/realemmetts/Library/Keychains/login.keychain-db)
```

**Root cause:** The keychain contained both the old certificate (hash `739B045...`) and the newly generated one (hash `D4918C7...`). Both had the same common name, so `codesign` couldn't choose between them.

**Fix:** Used the specific SHA-1 hash of the new certificate instead of the name string:

```bash
# Instead of:
codesign --sign "Developer ID Application: ES Development LLC (M9D5379H93)" ...

# Use the specific cert hash:
codesign --sign "D4918C7D3C56B0C14571251824383D15145607BC" ...
```

### Signing Results

After resolving both issues, all 6 binaries were signed successfully:

```
Authority=Developer ID Application: ES Development LLC (M9D5379H93)
Authority=Developer ID Certification Authority
Authority=Apple Root CA
Timestamp=Feb 25, 2026 at 1:41:xx AM
TeamIdentifier=M9D5379H93
Runtime Version=14.5.0  (aarch64) / 15.5.0 (x86_64)
```

The different `Runtime Version` values (14.5 vs 15.5) reflect the SDK version the binaries were originally compiled against in CI, not the local signing environment.

### Notarization Status

The binaries are **signed but not notarized**. Notarization requires:
1. An app-specific password from Apple ID
2. Storing credentials via `xcrun notarytool store-credentials`
3. Submitting each binary/DMG to Apple's notary service
4. Waiting for Apple's automated scan (usually 2–15 minutes)
5. Stapling the notarization ticket to the binary/DMG

Notarized binaries can run without any Gatekeeper warnings at all. For signed-but-not-notarized binaries, users see a dialog but can proceed via right-click → Open. This is acceptable for internal distribution to technical users.

### Lessons Learned for Future Signing

1. **Always use the cert hash** when multiple certs with the same name exist in the keychain
2. **Check the WWDR intermediate cert** — it expires periodically and must be renewed from Apple
3. **The `--options runtime` flag is critical** — without it, hardened runtime isn't enabled and future notarization will fail
4. **`codesign` exit code can be misleading** — it may return 0 even when signing partially fails. Always verify with `codesign -dvv` afterward
5. **Signing DMG containers** requires a separate codesign call after hdiutil create — signing the binary alone doesn't sign the container

---

## 5. DMG Packaging Process

### Steps Per Binary

1. **Extract** binary from cargo-dist's `.tar.xz`:
   ```bash
   tar -xf tr-300-aarch64-apple-darwin.tar.xz -C /tmp/work
   # Produces: /tmp/work/tr-300-aarch64-apple-darwin/tr300
   ```

2. **Sign** the extracted binary:
   ```bash
   codesign --sign "D4918C7D3C56B0C14571251824383D15145607BC" \
     --options runtime --force /tmp/work/.../tr300
   ```

3. **Stage** into a clean directory (DMG source):
   ```bash
   mkdir staging && cp tr300 staging/
   ```

4. **Create DMG** with descriptive volume name:
   ```bash
   hdiutil create -volname "TR300-AppleSilicon" \
     -srcfolder staging -ov -format UDZO output.dmg
   ```

5. **Sign the DMG container**:
   ```bash
   codesign --sign "D4918C7D3C56B0C14571251824383D15145607BC" output.dmg
   ```

### Volume Naming Convention

Volume names follow the pattern `{TOOLNAME}-{ArchDescription}`:
- `TR300-AppleSilicon`, `TR300-Intel`
- `ND300-AppleSilicon`, `ND300-Intel`
- `SD300-AppleSilicon`, `SD300-Intel`

This makes it immediately clear to the user what's inside when they mount the DMG.

### DMG Format Choice

We used `UDZO` (zlib-compressed read-only) which is the standard format for distributable DMGs. Other options considered:
- `UDBZ` (bzip2): Slightly smaller but slower to mount
- `ULFO` (lzfse): Apple-only compression, not universally supported
- `UDRO` (uncompressed read-only): Larger files, no benefit

---

## 6. File Naming Conventions in cargo-dist

cargo-dist uses a consistent naming scheme:

```
{binary-name}-{target-triple}.{ext}
```

Where:
- `binary-name` is derived from the Cargo.toml binary name (e.g., `tr-300`)
- `target-triple` follows Rust's target naming (e.g., `x86_64-apple-darwin`)
- Extensions: `.tar.xz` (Unix), `.zip` (Windows portable), `.msi` (Windows installer)

**Note:** The binary name inside the archive differs from the archive name:
- Archive: `tr-300-aarch64-apple-darwin.tar.xz`
- Binary inside: `tr300` (no hyphen)

This is because the Rust crate name uses hyphens (`qube-machine-report`, binary name `tr-300`) but the compiled binary may use a different name configured in `Cargo.toml` (`tr300`). This is a potential source of confusion for users.

### What We Excluded

cargo-dist also produces files we didn't include in this distribution:
- `dist-manifest.json` — Internal cargo-dist metadata describing the release structure. Useful for tooling but not for end users.
- `source.tar.gz` + `source.tar.gz.sha256` — Source code archive. Users who want source code should clone the repo directly.

---

## 7. SHA256 Checksum Strategy

### Two Checksum Formats

cargo-dist provides checksums in two formats:

1. **`sha256.sum`** — A single file with checksums for all artifacts in the release, in `sha256sum -c` compatible format:
   ```
   3d25f40001ee1e7f41b622f1be9ddf492ec15568 *tr-300-aarch64-apple-darwin.tar.xz
   14f6d5d00d45fa3ccbe289b419a3cddb2dbaf39f *tr-300-aarch64-unknown-linux-gnu.tar.xz
   ...
   ```

2. **Individual `.sha256` files** — One per artifact (e.g., `tr-300-x86_64-pc-windows-msvc.msi.sha256`), each containing just the hash and filename.

### Verification Note

The `sha256.sum` files contain checksums for the **original** CI artifacts (`.tar.xz` files), not the locally-created `.dmg` files. This means the macOS DMGs cannot be verified against `sha256.sum` — they were created locally from the extracted and re-signed binaries.

For Linux and Windows artifacts, checksums can be verified directly since those files are unmodified from the CI output.

---

## 8. Platform Coverage Analysis

### What We Have

| Platform | Architecture | Status |
|----------|-------------|--------|
| macOS Apple Silicon (aarch64) | arm64 | Full support (signed DMG) |
| macOS Intel (x86_64) | x86_64 | Full support (signed DMG) |
| Windows x86_64 | x86_64 | Full support (MSI + ZIP) |
| Linux x86_64 glibc | x86_64 | Full support |
| Linux x86_64 musl | x86_64 | Full support (Alpine/container-friendly) |
| Linux ARM64 glibc | aarch64 | Full support (RPi, Graviton) |

### What We Don't Have (and Why It's OK)

| Platform | Why Not Included | Workaround |
|----------|-----------------|------------|
| Windows ARM64 | Rust target `aarch64-pc-windows-msvc` is tier 2; cargo-dist doesn't build it | x86_64 MSI runs under Windows' built-in x86 emulation |
| Linux ARM64 musl | Uncommon combination; not built by cargo-dist | Use glibc ARM64 build or compile from source |
| Linux `.deb` packages | cargo-dist doesn't produce these | `tar.xz` extract-and-run is adequate for CLI tools |
| Linux `.rpm` packages | cargo-dist doesn't produce these | Same as above |
| Linux AppImage | cargo-dist doesn't produce these | Same as above |
| FreeBSD | No CI target configured | Compile from source |

### The musl Bonus

The musl builds are a nice bonus from cargo-dist. They're statically linked against musl libc, making them ideal for:
- Alpine Linux containers (common in Docker/Kubernetes)
- Minimal Linux environments without glibc
- Environments where you can't install shared libraries

---

## 9. Installer Scripts from cargo-dist

### Shell Installer (`*-installer.sh`)

Each tool includes a ~52 KB shell installer script. These scripts:
- Detect the user's OS and architecture
- Download the appropriate binary from GitHub Releases
- Install it to `~/.cargo/bin/` or a user-specified location
- Add the install directory to `$PATH` if needed

**Caveat for offline use:** These scripts are designed to download binaries from GitHub. For offline distribution, users should use the DMGs (macOS), MSIs (Windows), or tar.xz archives (Linux) directly instead.

### PowerShell Installer (`*-installer.ps1`)

Similar to the shell installer but for Windows. Each is ~21 KB and handles:
- Architecture detection
- Download from GitHub Releases
- Installation to the user's local app data directory
- PATH modification

Same offline caveat applies.

---

## 10. Recommendations for Future Releases

### Updating This Repository

When new versions of TR300, ND300, or SD300 are released:

1. Download new artifacts: `gh release download vX.Y.Z --repo QubeTX/{repo} --dir /tmp/{tool}-dl`
2. Sort into OS folders (same pattern as the initial population)
3. Sign macOS binaries using the cert hash (not name) to avoid ambiguity:
   ```bash
   codesign --sign "D4918C7D3C56B0C14571251824383D15145607BC" --options runtime --force <binary>
   ```
4. Create DMGs with `hdiutil create`
5. Update version numbers in README.md and CHANGELOG.md
6. Commit and push

### Setting Up Notarization

To eliminate Gatekeeper warnings entirely:

1. Generate an app-specific password at https://appleid.apple.com/account/manage
2. Store credentials:
   ```bash
   xcrun notarytool store-credentials "notarytool-profile" \
     --apple-id "your@email.com" \
     --team-id "M9D5379H93" \
     --password "xxxx-xxxx-xxxx-xxxx"
   ```
3. After creating DMGs, submit for notarization:
   ```bash
   xcrun notarytool submit output.dmg --keychain-profile "notarytool-profile" --wait
   xcrun stapler staple output.dmg
   ```

### Cleaning Up Old Certificates

The keychain currently has duplicate Developer ID certificates (old hash `739B045...` and new hash `D4918C7...`). To avoid future ambiguity issues, consider removing the old certificate:

1. Open Keychain Access
2. Search for "Developer ID Application"
3. Identify the old cert (check expiry dates)
4. Delete the expired/old one

Or continue using the specific hash `D4918C7D3C56B0C14571251824383D15145607BC` in all codesign commands.

### Automating the Workflow

The entire process (download → sign → DMG → commit) could be scripted. Key considerations:
- Use `gh release download` for fetching
- Use cert hash for signing (avoids ambiguity)
- Verify signatures after signing (`codesign -dvv`)
- Run checksum verification on non-macOS artifacts
- Generate updated CHANGELOG entries automatically

### Adding cargo-dist to the CI of This Repo

This distribution repo itself doesn't need cargo-dist (it's not a Rust project). But if we wanted automated releases, we could add a GitHub Action that:
1. Monitors the three source repos for new releases
2. Downloads artifacts automatically
3. Signs macOS binaries (would need a code signing certificate in CI secrets)
4. Creates a new release on this repo

This would fully automate the distribution pipeline.
