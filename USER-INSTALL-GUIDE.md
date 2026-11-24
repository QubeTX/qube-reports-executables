# Install the QubeTX offline toolkit

This November 24, 2026 snapshot contains TR-300 4.5.1, ND-300 4.0.2 with SpeedQX, and SD-300 4.1.0 with its desktop app. You can install any one tool independently.

1. Download the ZIP and its checksum on a connected computer. [Check the download and extracted files](README.md#verify-the-download).
2. Extract the whole ZIP. Open `index.html` for the local file picker, or open `TR-300/`, `ND-300/`, or `SD-300/`.
3. Choose the destination computer’s OS and processor. Choose an edition and format where offered. Open a terminal **in the folder that contains the installer or archive** and run the commands in its `README.md`.

## Windows

All three tools target Windows x64. Under your tool’s `Windows/x64/` folder, choose **Standard** (called Global by the publisher) to install for all users with administrator approval, or **Corporate** for a current-user installation. Both editions offer MSI and EXE. Pick one format. For upgrades, match the edition and format already installed.

SD-300 Desktop requires the Microsoft Visual C++ x64 runtime. If the DLL is missing, the Windows command guides open the local runtime installer from the extracted toolkit. Installing this system prerequisite can require administrator approval, including for a Corporate or portable desktop deployment. IT can provision it in advance using the [local runtime commands](SD-300/Windows/x64/Runtime/README.md). The CLI runs independently. On Windows N, provision the matching Windows Media Feature Pack from your organization's Windows offline servicing media before using the desktop app.

| Corporate MSI commands | Corporate EXE commands |
| --- | --- |
| [TR-300 MSI](TR-300/Windows/x64/Corporate/MSI/README.md) | [TR-300 EXE](TR-300/Windows/x64/Corporate/EXE/README.md) |
| [ND-300 MSI](ND-300/Windows/x64/Corporate/MSI/README.md) | [ND-300 EXE](ND-300/Windows/x64/Corporate/EXE/README.md) |
| [SD-300 MSI](SD-300/Windows/x64/Corporate/MSI/README.md) | [SD-300 EXE](SD-300/Windows/x64/Corporate/EXE/README.md) |

Open a new terminal after installation and check the command with `--version`. SD-300 native installers also install its desktop app. Launch it from Start or with `sd300 gui`. Endpoint policy still applies to per-user installations.

Portable ZIP commands extract into a versioned directory under `%LOCALAPPDATA%\QubeTX\Portable`. Choose CLI for terminal use or SD-300’s Desktop ZIP for the app. Keep each archive’s files together.

## macOS

Use `macOS/Universal/Standard/PKG/` for the native installer on Intel or Apple Silicon. The SD-300 PKG installs the CLI and app. TR-300 and ND-300 also publish compatibility DMGs containing their signed PKGs. Use either native format once.

For a portable CLI, choose `Apple-Silicon` for Apple chips or `Intel-x64` for Intel. For SD-300’s portable desktop app, use `Universal/Portable/Desktop/ZIP/`. Its commands preserve the app bundle. For a native upgrade, follow the ownership instructions in the product manual, particularly when switching from a managed command-line installation.

## Linux

Use `uname -m` to identify the processor. `x86_64` corresponds to **x64** and `aarch64` to **ARM64**. Under x64, choose **glibc** for distributions such as Debian, Ubuntu, or Fedora, or **musl** for distributions such as Alpine. ARM64 packages are published for glibc.

Choose **Portable/CLI** for terminal use, or **Portable/Desktop** for the SD-300 app. Commands extract the entire archive into a versioned directory under `$HOME/.local/opt/qubetx`. The desktop command uses the launcher in `sd300/bin/` with its bundled private runtime. A compatible system and graphical desktop are required.

## Upgrades and removal

For an offline native upgrade, run the included installer for the existing product, edition and format. This is especially important for SD-300 upgrades from 3.x to 4.x. Its older updater may reject the new desktop components. Preserve the entire portable distribution when upgrading, including TR-300’s `report` and ND-300’s `speedqx` companion commands.

Native installations support `tr300 uninstall`, `nd300 uninstall`, and `sd300 uninstall`. Portable files are separate from registered installations. Close the portable program and remove its own extracted directory to uninstall it. Online self-updates and internet speed tests require connectivity.

Each product folder contains `Manuals/upstream/README.md`, its license, and `Manuals/RELEASE-NOTES.md` for the exact included release.
