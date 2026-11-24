## Release Notes

### Security

- Serialize the Linux dhcpcd Wi-Fi fallback with hexadecimal SSIDs and derived WPA-PSKs instead of interpolating quoted credentials. Validate SSID/passphrase limits, preserve printable password punctuation, and report configuration write/reload failures without claiming connectivity.
- Resolve built-in repair and diagnostic utilities from fixed system locations, obtain the Windows system directory from the OS, and give children a trusted utility search path. Missing utilities fail without falling back to caller-controlled PATH/current directories; proven installer/provider paths and invoking-user Cargo ownership remain intact.
- Constrain inherited PowerShell module paths and shell startup/function hooks. A recognized VPN whose provider CLI is unavailable now requires manual disconnection instead of substituting a generic adapter-disable operation.
- Use only OS-resolved native Windows PowerShell for standalone Windows updates; retire the optional PATH-discovered PowerShell 7 fallback. If the native launcher is unavailable, report failure with same-channel manual recovery guidance.
- Verify cargo-dist, WiX and Inno downloads against pinned publisher SHA-256 digests before use, and pin the Context7 MCP package in both agent configurations. Preserve the protected Apple signing and publication gates.
- Update locked rustls to 0.23.46, rustls-webpki to 0.103.16, webpki-roots to 1.0.10 and optional quinn-proto to 0.11.18. Clear the current RustSec audit findings, including TLS secret logging, handshake handling, distrusted intermediates and QUIC denial-of-service advisories, without adding exceptions.
- Restrict Apple signing credentials to the GitHub `apple-signing` environment and protected source refs. Pull requests build without signing secrets; every main push automatically qualifies signed native archives and the universal PKG/compatibility DMG on Intel and Apple Silicon. Exact-SHA qualification gates release signing without a recurring approval step. Preserve all 32 release assets, checksums, attestations, native lifecycle and legacy updater checks.

### Development

- Permit GPT-6.1 Sol at xhigh for Codex subagents alongside the existing Opus/Sonnet model choices, keeping AGENTS.md and CLAUDE.md guidance aligned.

## Install nd300 4.0.2

### Install prebuilt binaries via shell script

```sh
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-installer.sh | sh
```

### Install prebuilt binaries via powershell script

```sh
powershell -ExecutionPolicy Bypass -c "irm https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-installer.ps1 | iex"
```

## Download nd300 4.0.2

|  File  | Platform | Checksum |
|--------|----------|----------|
| [nd300-aarch64-apple-darwin.tar.xz](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-aarch64-apple-darwin.tar.xz) | Apple Silicon macOS | [checksum](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-aarch64-apple-darwin.tar.xz.sha256) |
| [nd300-x86_64-apple-darwin.tar.xz](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-x86_64-apple-darwin.tar.xz) | Intel macOS | [checksum](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-x86_64-apple-darwin.tar.xz.sha256) |
| [nd300-x86_64-pc-windows-msvc.zip](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-x86_64-pc-windows-msvc.zip) | x64 Windows | [checksum](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-x86_64-pc-windows-msvc.zip.sha256) |
| [nd300-x86_64-pc-windows-msvc.msi](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-x86_64-pc-windows-msvc.msi) | x64 Windows | [checksum](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-x86_64-pc-windows-msvc.msi.sha256) |
| [nd300-aarch64-unknown-linux-gnu.tar.xz](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-aarch64-unknown-linux-gnu.tar.xz) | ARM64 Linux | [checksum](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-aarch64-unknown-linux-gnu.tar.xz.sha256) |
| [nd300-x86_64-unknown-linux-gnu.tar.xz](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-x86_64-unknown-linux-gnu.tar.xz) | x64 Linux | [checksum](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-x86_64-unknown-linux-gnu.tar.xz.sha256) |
| [nd300-x86_64-unknown-linux-musl.tar.xz](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-x86_64-unknown-linux-musl.tar.xz) | x64 MUSL Linux | [checksum](https://github.com/QubeTX/qube-network-diagnostics/releases/download/v4.0.2/nd300-x86_64-unknown-linux-musl.tar.xz.sha256) |


