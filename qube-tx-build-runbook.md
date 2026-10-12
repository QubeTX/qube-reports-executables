# QubeTX offline bundle release runbook

Current snapshot: **3.0.0, October 11, 2026**. The bundle includes only TR-300, ND-300/SpeedQX, and SD-300. Do not add retired products to the allowlist.

## Refresh

1. Inspect the public latest stable release of each included source repository. Read that release's README, changelog, CLI definitions and packaging source; local development branches may describe unpublished behavior.
2. Update `bundle-spec.json` with exact tags, resolved commit SHAs, and explicit asset names. Keep official MSI/EXE/PKG files unchanged. Include SD-300 CLI and GUI artifacts for each supported target, matching licenses, and both companion commands. Omit online installers, compatibility DMGs, duplicate legacy native packages, debug symbols, and unpublished artifacts.
3. Run `python scripts/build_bundle.py --output <new-empty-staging-directory>`. Python 3.10+ and authenticated GitHub CLI are required to rebuild; the destination user's installation needs neither. Public download bytes are compared against upstream SHA-256 sidecars and GitHub digests. A failed build never overwrites an existing snapshot.
4. Inspect archive membership, manifests, platform requirements and licenses. Smoke-test extracted Windows commands with `--version` and `--help`; do not launch native installers on the maintainer's working machine. Check MSI metadata read-only. Native installed GUI, UAC and non-Windows execution require separate platform acceptance; checksum verification alone does not prove those behaviors.
5. Copy the verified product directories and manifest into this repository. Remove obsolete product payloads deliberately; `--verify` rejects unexpected files in each product directory. Update README, the install guide, technical/human changelogs and the website's bundled-version data together.
6. Run `python scripts/build_bundle.py --verify .`, then `python scripts/package_bundle.py --zip <outside-repo>/qubetx-offline-bundle.zip`. The packager creates `index.html`, `SHA256SUMS.txt`, the curated ZIP and its sidecar. Run `scripts/Verify-Bundle.ps1` and verify the ZIP can be extracted and rechecked. All runtime artifacts and embedded dependencies remain unchanged.
7. Stage explicit paths; inspect the staged diff and ensure no private files, credentials, local test results or temporary extracted executables enter this public repository. Commit and push the distribution snapshot.
8. Create a draft tagged release with the ZIP, its `.sha256`, and `bundle-manifest.json`. Verify uploaded bytes before making the release public. Use a new version for a correction, never silently replace a published snapshot. Stable user download: `releases/latest/download/qubetx-offline-bundle.zip`.
9. Update and deploy the website's offline download page and guide after the bundle is public. Download the public release ZIP, verify its hash, extracted checksums, product list, docs and links. Confirm live website metadata matches the published manifest.

## Reproducibility and exclusions

The spec pins tags and commits; the manifest pins the actual payload digests. ZIP timestamps use the snapshot date and paths are sorted. Rebuilding with unchanged sources and inputs produces identical bytes. The release ZIP deliberately excludes `.git`, repository maintenance history, caches, and unrelated products. `DISCOVERIES.md` records the original process and is historical only.

Product install/update semantics are owned by upstream. This bundle must never build substitute packages, strip signatures, advertise endpoint-policy bypasses, or turn network-requiring tests into an "everything works offline" claim.
