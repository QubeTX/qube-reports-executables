#!/bin/bash
set -euo pipefail
root="$RUNNER_TEMP/qubetx-offline-bundle"
profile='(version 1)(allow default)(deny network-outbound (remote ip "*:*"))'
restricted() { /usr/bin/sandbox-exec -p "$profile" "$@"; }
curl --noproxy '*' -fsS --max-time 8 https://api.github.com/zen >/dev/null
if restricted curl --noproxy '*' -fsS --max-time 3 https://api.github.com/zen >/dev/null; then exit 1; fi
for product in TR-300 ND-300 SD-300; do
    localdir="$root/$product/macOS/Universal/Standard"
    pkg=$(find "$localdir/PKG" -name '*.pkg' -type f)
    case "$product" in
        TR-300) cmd=tr300; commands='tr300 report'; version=4.5.1 ;;
        ND-300) cmd=nd300; commands='nd300 speedqx'; version=4.0.2 ;;
        SD-300) cmd=sd300; commands='sd300'; version=4.1.0 ;;
    esac
    if [[ -d "$localdir/DMG" ]]; then
        mount=$(mktemp -d)
        restricted hdiutil attach -readonly -nobrowse -mountpoint "$mount" "$localdir"/DMG/*.dmg
        cmp "$pkg" "$mount/$cmd.pkg"
        hdiutil detach "$mount"
        rmdir "$mount"
    fi
    sudo /usr/bin/sandbox-exec -p "$profile" /usr/sbin/installer -pkg "$pkg" -target /
    for bin in $commands; do
        actual=$(restricted "/usr/local/bin/$bin" --version)
        [[ "$actual" == *"$version"* ]]
        echo "INSTALLED FROM LOCAL PKG $(uname -m) /usr/local/bin/$bin $actual"
    done
done
restricted /Applications/SD-300.app/Contents/MacOS/sd300-gui --self-test --json | jq -e '.success and .product_version == "4.1.0"'
