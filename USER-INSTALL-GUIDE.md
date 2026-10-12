# Install the QubeTX offline toolkit

Snapshot: October 11, 2026. Included releases: TR-300 4.4.0, ND-300 4.0.1, SD-300 4.1.0.

## 1. Extract and verify

Download `qubetx-offline-bundle.zip` on a connected computer, copy it to the destination, and extract the entire folder. Open `index.html` for the local file picker. Keep the folder layout intact. Verify the root `SHA256SUMS.txt` as explained in README.md.

The included installers do not need Rust or a package manager. Network tests and self-updates still need connectivity. The bundle targets Windows x64, macOS Intel/Apple Silicon, and Linux x64 GNU, ARM64 GNU, and x64 musl. Native Windows ARM64 packages are not included or qualified here.

## 2. Choose the product and platform

| Product folder | Commands | What's new since the previous bundle |
|---|---|---|
| `TR300-qube-machine-report` | `tr300`, `report` | A real companion command, safer paired updates, current installer license and ownership handling |
| `ND300-qube-network-diagnostics` | `nd300`, `speedqx` | Methodology v5 sustained-throughput measurement, Quick/Deep modes, explicit partial and single-source results |
| `SD300-qube-system-diagnostics` | `sd300` | Native desktop app plus terminal monitor, timestamped measurements, snapshots and current lifecycle handling |

### macOS

Use the universal `.pkg` in the product's `macos/` folder for a native installation:

- TR-300: `tr300-universal-apple-darwin.pkg`
- ND-300: `nd300-universal-apple-darwin.pkg`
- SD-300: `sd300-macos-universal.pkg`

Each supports both Apple Silicon and Intel. Double-click it, follow Apple Installer, and open a new Terminal. The packages are the unchanged signed/notarized/stapled upstream releases. SD-300 also installs its app in Applications. Run `sd300 gui` or open the app yourself; installation does not launch it automatically.

For portable command-line use, choose `aarch64-apple-darwin` for Apple Silicon or `x86_64-apple-darwin` for Intel. Extract with `tar -xf <filename>.tar.xz`, enter the archive's top-level directory, and run `./tr300`, `./nd300`, or `./sd300`. Preserve executable permissions. Keep `report` beside `tr300`, and `speedqx` beside `nd300`.

For the portable SD-300 app, extract `sd300-gui-macos-universal.zip` and open the contained app bundle. Do not pull the executable out of the app bundle.

### Windows

Choose **one** installer format and edition for each product:

- **Global:** machine-wide installation, administrator approval required.
- **Corporate:** current-user installation, no administrator approval required.
- **MSI or EXE:** choose the format that matches your existing installation or deployment policy.

| Product | Global MSI / EXE | Corporate MSI / EXE |
|---|---|---|
| TR-300 | `tr300-x86_64-pc-windows-msvc.msi` / `tr300-x86_64-pc-windows-msvc-setup.exe` | `tr300-x86_64-pc-windows-msvc-corporate.msi` / `tr300-x86_64-pc-windows-msvc-corporate-setup.exe` |
| ND-300 | `nd300-x86_64-pc-windows-msvc.msi` / `nd300-x86_64-pc-windows-msvc-setup.exe` | `nd300-x86_64-pc-windows-msvc-corporate.msi` / `nd300-x86_64-pc-windows-msvc-corporate-setup.exe` |
| SD-300 | `sd300-windows-x64-global.msi` / `sd300-windows-x64-global.exe` | `sd300-windows-x64-corporate.msi` / `sd300-windows-x64-corporate.exe` |

Double-click the chosen file and follow its prompts. Open a fresh terminal after installation. SD-300's native installers contain both the CLI/TUI and desktop app; use Start > SD-300 or `sd300 gui` to open it.

If Windows or endpoint policy blocks the installer, verify its source, hash, and publisher. Keep the diagnostic and ask your administrator where appropriate. Do not assume a SmartScreen warning is merely because an app is outside the Microsoft Store, or disable security controls to continue.

**Portable CLI:** extract the product's `*-x86_64-pc-windows-msvc.zip`. Open PowerShell in the extracted folder and run `./tr300.exe`, `./nd300.exe`, `./speedqx.exe`, or `./sd300.exe`. SD-300's CLI ZIP starts with `tr300-tui-`; this is its historical package name.

**Portable SD-300 GUI:** extract `sd300-gui-windows-x86_64.zip` into its own folder and open `sd300-gui.exe`. Keep `sd300_engine.dll`, assets, licenses, and `install-manifest.json` alongside it. Extract the CLI ZIP separately if you also want terminal commands. These extractions do not create PATH entries, menu shortcuts, or a managed-install receipt.

### Linux

Check `uname -m`. Use `x86_64-unknown-linux-gnu` on a compatible x64 GNU/Linux distribution, `aarch64-unknown-linux-gnu` on ARM64 GNU/Linux, or `x86_64-unknown-linux-musl` for x64 musl/Alpine. An ARM64 musl build is not included.

For a CLI archive:

```sh
tar -xf tr300-x86_64-unknown-linux-gnu.tar.xz
cd tr300-x86_64-unknown-linux-gnu
./tr300 --help
./tr300
```

Use the actual directory listed by `tar -tf <archive>` if it differs. Other tools use the matching archive and command names. TR-300 ships `tr300` and `report`; ND-300 ships `nd300` and `speedqx`; SD-300 CLI ships `sd300`. Keep companion binaries together. Manual copying does not establish a managed receipt; keep track of where you put portable files.

**SD-300 desktop:** choose the corresponding GUI archive:

| Target | GUI archive |
|---|---|
| x64 GNU | `sd300-gui-linux-gnu-x86_64.tar.xz` |
| ARM64 GNU | `sd300-gui-linux-gnu-arm64.tar.xz` |
| x64 musl | `sd300-gui-linux-musl-x86_64.tar.xz` |

Extract into its own directory, keep the entire `sd300/` tree, and run `./sd300/bin/sd300-gui`. The launcher sets up the included private runtime. Do not launch `libexec/sd300-gui` directly or copy just that binary. A working graphical desktop, compatible system libc, kernel and display/driver support remain necessary. Extract the separate CLI archive for terminal use. Portable extraction creates no menu entry or managed-install receipt.

## 3. Use the tools

```text
tr300                       Show a machine report; no file is created
report --fast               Show a quick report
tr300 --json                Write JSON to terminal/stdout
tr300 --report              Explicitly save a Markdown report
nd300 --help                See diagnostic and recovery options
speedqx --help              See speed-test modes and limits
sd300                       Open the terminal mode chooser
sd300 gui                   Open the installed desktop monitor
sd300 snapshot --json       Export a redacted diagnostic snapshot
sd300 capabilities --json   Show available diagnostic capabilities
```

Keep remote throughput tests distinct from local inspection. Offline or blocked network checks can report unavailable or incomplete results. SD-300's optional ND-300 integration needs the companion tool available; installing SD-300 alone does not install ND-300.

## 4. Upgrade and remove

For an **offline upgrade**, run the included official native installer matching the existing channel, format and edition. Use the bundled installer directly for **SD-300 3.x to 4.x**: older updaters can reject the new GUI ABI/schema and restore the old CLI. Avoid replacing individual managed files or mixing versions inside a GUI folder.

For portable use, extract into a new version-specific folder and keep the old folder until the new one works. A portable copy has no native installer registration. Do not overwrite a managed installation with an extracted portable binary.

With internet available, `tr300 update`, `nd300 update` / `speedqx update`, and `sd300 update` follow the proven installed channel. Ownership conflicts or policy blocks can stop a transition; retain the working installation and follow the diagnostic's recovery path. The bundle does not bypass these checks.

Installed products expose `tr300 uninstall`, `nd300 uninstall`, and `sd300 uninstall`. SD-300 uninstall removes its installed CLI and GUI together and remains a CLI action. For an unregistered portable folder, close its processes and remove only that extracted folder rather than invoking lifecycle commands against another managed copy on PATH.

## 5. Read the matching documentation

Each product's `docs/upstream/README.md`, changelog, license, supporting Markdown documents and available man pages are from that exact release commit. `docs/RELEASE-NOTES.md` contains its published release notes. These are readable offline in a text editor. Links to websites, images and remote downloads still need internet. Historical plans and qualification notes are context, not new feature promises.
