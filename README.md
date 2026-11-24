# QubeTX Offline Toolkit

**Bundle 4.0.1 · November 24, 2026**

[Download the offline ZIP](https://github.com/QubeTX/qube-reports-executables/releases/latest/download/qubetx-offline-bundle.zip) and its [SHA-256 checksum](https://github.com/QubeTX/qube-reports-executables/releases/latest/download/qubetx-offline-bundle.zip.sha256). Copy the ZIP to the destination computer, extract it, and open **index.html** or open the folder for **TR-300**, **ND-300**, or **SD-300**. The start page works entirely offline.

| Included tool | Release | Commands |
| --- | --- | --- |
| TR-300 machine report | [4.5.1](https://github.com/QubeTX/qube-machine-report/releases/tag/v4.5.1) | `tr300`, `report` |
| ND-300 network diagnostics | [4.0.2](https://github.com/QubeTX/qube-network-diagnostics/releases/tag/v4.0.2) | `nd300`, `speedqx` |
| SD-300 system diagnostics | [4.1.0](https://github.com/QubeTX/qube-system-diagnostics/releases/tag/v4.1.0) | `sd300`, plus the desktop app |

## Find the right file

Inside your chosen product, use the folders below. Portable desktop packages belong to SD-300.

| Folder | What to choose |
| --- | --- |
| `Windows/x64/` | **Standard** (the upstream Global edition, all users) or **Corporate** (current user), then **MSI** or **EXE**. **Portable** has separate CLI and desktop ZIPs. |
| `macOS/Universal/` | **Standard/PKG** installs on Intel and Apple Silicon. **Standard/DMG** has the TR-300 and ND-300 compatibility images containing the same PKGs. **Portable/Desktop/ZIP** contains the SD-300 app. |
| `macOS/Apple-Silicon/` or `macOS/Intel-x64/` | Portable command-line archives for that processor. |
| `Linux/x64/` or `Linux/ARM64/` | Choose **glibc** or **musl** as published for your processor, then **Portable/CLI** or **Portable/Desktop**. ARM64 has glibc builds. |
| `Manuals/` | Matching product manuals, licenses, release notes and available man pages. |

**Every folder containing installers or archives has a command-only `README.md`.** Open a terminal in that folder and run its command block. For example, see the [TR-300 Corporate MSI commands](TR-300/Windows/x64/Corporate/MSI/README.md). For upgrades and platform requirements, see the [installation guide](USER-INSTALL-GUIDE.md).

The 40 distinct packages are the original, unmodified upstream downloads. SD-300’s legacy MSI filename is a byte-identical alias of its Standard MSI. The manifest records that alias. Corporate editions are published for Windows x64. SD-300 native installers include both the CLI and desktop app. The ZIP includes Microsoft's signed x64 Visual C++ runtime installer under SD-300/Windows/x64/Runtime. If the runtime is missing, the desktop installation commands open that local file. IT can provision this system prerequisite before a per-user deployment.

## Verify the download

Compare the SHA-256 of the ZIP with its published checksum before extraction. Then run the command for your OS from the extracted bundle root to verify individual files.

**Windows PowerShell**

```powershell
.\scripts\Verify-Bundle.ps1
```

**macOS**

```sh
shasum -a 256 -c SHA256SUMS.txt
```

**Linux**

```sh
sha256sum -c SHA256SUMS.txt
```

The ZIP checksum can also be verified on macOS with `shasum -a 256 -c qubetx-offline-bundle.zip.sha256`, or on Linux with `sha256sum -c qubetx-offline-bundle.zip.sha256`, in the folder holding both downloads. Each package has its original upstream checksum alongside it. The [manifest](bundle-manifest.json) lists exact source commits, tagged URLs, file sizes and digests.

Installation uses local files and needs no Rust toolchain or package manager. Internet speed tests, public DNS and IP checks, and self-updates require connectivity. Local diagnostics depend on available hardware and OS permissions.

Maintainers can reproduce the snapshot with the [release runbook](qube-tx-build-runbook.md).
