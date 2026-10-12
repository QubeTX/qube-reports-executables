## Release Notes

### Fixed
- Both Windows MSI editions now embed the complete PolyForm Noncommercial
  1.0.0 license, including the required copyright notice, instead of WiX's
  placeholder EULA. The EXE installers already use `LICENSE`; the macOS
  PKG/compatibility DMG has no license dialog to replace. (#eula)
- Installer and cleanup preflights require positive ownership of the new
  companion; older single-binary receipts cannot authorize deleting an
  unrelated `report`. Native installers reject collisions before payload
  mutation, and managed wrappers validate Cargo/receipt inventories.
- Concurrent Windows updates preserve recovery files belonging to active transactions.
- Windows updates stage both loaded executables and restore both on failure.
  Ambiguous partial rollback preserves unproven files and reports recovery
  paths instead of claiming complete restoration. Unix `report` replaces
  itself with the canonical process to preserve signals and avoid file locks.

### Added
- **Every supported distribution now installs a real `report` command beside
  `tr300`.** The new binary is included in cargo-dist archives/installers, both
  Windows MSI editions, both Inno Setup editions, the signed/notarized macOS
  PKG/DMG, Cargo installs, and the managed shell/PowerShell channels. Bare
  `report` produces the normal full report; `--fast`, `--full`, `--json`,
  `--ascii`, title/color/elevation controls, and explicit Markdown saving are
  supported.
- **`report` is a full alias for `tr300`.** Every argument, including install,
  update, and uninstall, is forwarded to the exact adjacent `tr300` payload
  without a shell or PATH lookup. Help, version, output, and exit status use
  the canonical CLI implementation.
- **Both commands now have generated command references.** `tr300(1)` covers
  the full reporting and lifecycle surface, while the new `report(1)` page
  contains the same reporting and maintenance options. The `-h` and `--help` forms for
  both commands are release-tested against their complete visible surfaces.

### Changed
- **Shell profiles no longer create a TR-300-owned `report` alias.** Rerunning
  `tr300 install` refreshes the owned auto-run block and retires the legacy
  alias. Foreign aliases, functions, and executables remain untouched and
  receive a shadowing warning.
- **Install, update, migration, rollback, and Complete uninstall treat
  `tr300` plus `report` as one product payload.** Transactions snapshot both
  commands, packages verify both versions and matching help output,
  and hosted Windows/macOS lifecycle gates require both files to install,
  update, and uninstall together. The public asset count remains 34 because
  the companion lives inside existing archives and packages.
- **`tr300 config` remains intentionally unsupported.** Runtime configuration
  is still CLI-driven, and the invalid positional word exits with clap's
  argument error rather than silently doing nothing.

### Security
- Update the locked rustls dependency to 0.23.45 (and rustls-webpki to
  0.103.15), resolving RUSTSEC-2026-0285. The release dependency audit passes.
- **Windows deferred self-uninstall now launches the OS-owned absolute
  `cmd.exe`.** It no longer relies on PATH to resolve the helper that removes
  the two exact packaged siblings after the running image exits.

## Install tr300 (latest)

### Install prebuilt binaries via shell script

```sh
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-installer.sh | sh
```

### Install prebuilt binaries via powershell script

```sh
powershell -ExecutionPolicy Bypass -c "irm https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-installer.ps1 | iex"
```

## Download tr300 (latest)

|  File  | Platform | Checksum |
|--------|----------|----------|
| [tr300-aarch64-apple-darwin.tar.xz](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-aarch64-apple-darwin.tar.xz) | Apple Silicon macOS | [checksum](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-aarch64-apple-darwin.tar.xz.sha256) |
| [tr300-x86_64-apple-darwin.tar.xz](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-x86_64-apple-darwin.tar.xz) | Intel macOS | [checksum](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-x86_64-apple-darwin.tar.xz.sha256) |
| [tr300-x86_64-pc-windows-msvc.zip](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-x86_64-pc-windows-msvc.zip) | x64 Windows | [checksum](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-x86_64-pc-windows-msvc.zip.sha256) |
| [tr300-x86_64-pc-windows-msvc.msi](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-x86_64-pc-windows-msvc.msi) | x64 Windows | [checksum](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-x86_64-pc-windows-msvc.msi.sha256) |
| [tr300-aarch64-unknown-linux-gnu.tar.xz](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-aarch64-unknown-linux-gnu.tar.xz) | ARM64 Linux | [checksum](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-aarch64-unknown-linux-gnu.tar.xz.sha256) |
| [tr300-x86_64-unknown-linux-gnu.tar.xz](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-x86_64-unknown-linux-gnu.tar.xz) | x64 Linux | [checksum](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-x86_64-unknown-linux-gnu.tar.xz.sha256) |
| [tr300-x86_64-unknown-linux-musl.tar.xz](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-x86_64-unknown-linux-musl.tar.xz) | x64 MUSL Linux | [checksum](https://github.com/QubeTX/qube-machine-report/releases/latest/download/tr300-x86_64-unknown-linux-musl.tar.xz.sha256) |


