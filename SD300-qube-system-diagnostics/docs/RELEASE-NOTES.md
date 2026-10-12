## A clearer system overview



SD-300 4.1.0 makes the overview easier to scan, with compact cards for Graphics, CPU, Memory, Disk, Network and Thermals, followed by running processes and actionable findings.



- See the busiest resources at a glance and open any card to investigate its detailed page.

- Read graphics adapters in clearly separated groups, with utilization and video memory kept apart. Dual-GPU laptops retain a stable adapter order.

- Spot disk and network activity through larger readings and adjacent units. Free space names its volume, and network traffic identifies its combined-interface scope.

- Read temperatures in aligned rows, with explicit labels when a sensor is unavailable.

- See the largest CPU and memory consumers from the complete process inventory.

- Keep missing, delayed and previous readings visible instead of displaying missing data as zero.

- Reduce repeated drawing and text-measurement work while preserving the Warm Carbon appearance.



The overview populates directly after launch, supports narrower windows, and keeps the detailed sidebar pages as the destinations for deeper inspection. Existing settings and CLI/export interfaces are preserved.



### Update



Use **Update now** in the app, or run:



```sh

sd300 update

```



### Known limitations



Some native frame/input timings and the measured Windows overview CPU cost remain above the original engineering targets. Physical Windows 200% display scaling and the remaining full resource matrix are still unverified. These are documented follow-up items accepted for this release only; functional, shutdown, installer and release-integrity checks remain required. See [the release decision](https://github.com/QubeTX/qube-system-diagnostics/blob/1d66a461b3e499e067b6c15658b04a8cde89671d/docs/adr/0025-overview-release-acceptance.md) and [qualification evidence](https://github.com/QubeTX/qube-system-diagnostics/blob/1d66a461b3e499e067b6c15658b04a8cde89671d/docs/qualification/overview-4.1.0.md).



The [technical changelog](https://github.com/QubeTX/qube-system-diagnostics/blob/1d66a461b3e499e067b6c15658b04a8cde89671d/CHANGELOG.md) contains the implementation details.





## Install SD-300 (latest)



### Install prebuilt binaries via shell script



```sh

curl --proto '=https' --tlsv1.2 -LsSf https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/sd300-cli-installer.sh | sh

```



### Install prebuilt binaries via powershell script



```sh

powershell -ExecutionPolicy Bypass -c "irm https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/sd300-cli-installer.ps1 | iex"

```



## Download SD-300 (latest)



|  File  | Platform | Checksum |

|--------|----------|----------|

| [tr300-tui-aarch64-apple-darwin.tar.xz](https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/tr300-tui-aarch64-apple-darwin.tar.xz) | Apple Silicon macOS | [checksum](https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/tr300-tui-aarch64-apple-darwin.tar.xz.sha256) |

| [tr300-tui-x86_64-apple-darwin.tar.xz](https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/tr300-tui-x86_64-apple-darwin.tar.xz) | Intel macOS | [checksum](https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/tr300-tui-x86_64-apple-darwin.tar.xz.sha256) |

| [tr300-tui-x86_64-pc-windows-msvc.zip](https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/tr300-tui-x86_64-pc-windows-msvc.zip) | x64 Windows | [checksum](https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/tr300-tui-x86_64-pc-windows-msvc.zip.sha256) |

| [tr300-tui-aarch64-unknown-linux-gnu.tar.xz](https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/tr300-tui-aarch64-unknown-linux-gnu.tar.xz) | ARM64 Linux | [checksum](https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/tr300-tui-aarch64-unknown-linux-gnu.tar.xz.sha256) |

| [tr300-tui-x86_64-unknown-linux-gnu.tar.xz](https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/tr300-tui-x86_64-unknown-linux-gnu.tar.xz) | x64 Linux | [checksum](https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/tr300-tui-x86_64-unknown-linux-gnu.tar.xz.sha256) |

| [tr300-tui-x86_64-unknown-linux-musl.tar.xz](https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/tr300-tui-x86_64-unknown-linux-musl.tar.xz) | x64 MUSL Linux | [checksum](https://github.com/QubeTX/qube-system-diagnostics/releases/latest/download/tr300-tui-x86_64-unknown-linux-musl.tar.xz.sha256) |







