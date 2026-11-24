#!/bin/bash
set -euo pipefail
root="$RUNNER_TEMP/qubetx-offline-bundle"
arch=x64
if [[ "$(uname -m)" == aarch64 ]]; then arch=ARM64; fi
if [[ "$arch" == x64 ]]; then docker pull alpine:3.22; fi
smoke='
set -eu
for product in TR-300 ND-300 SD-300; do
    cd "$1/$product/Linux/$2/$3/Portable/CLI/TAR.XZ"
    sed -n "/^dest=/,/--version$/p" README.md > /tmp/qubetx-cli-guide.sh
    test -s /tmp/qubetx-cli-guide.sh
    sh -e /tmp/qubetx-cli-guide.sh
    echo "OFFLINE INSTALLED $product $2 $3"
done
cd "$1/SD-300/Linux/$2/$3/Portable/Desktop/TAR.XZ"
mkdir -p "$HOME/desktop"
tar -xf ./*.tar.xz -C "$HOME/desktop"
"$HOME/desktop/sd300/bin/sd300-gui" --self-test --json > /tmp/desktop-check.json
grep -Eq '"'"'"success"[[:space:]]*:[[:space:]]*true'"'"' /tmp/desktop-check.json
cat /tmp/desktop-check.json
'
sudo unshare --net -- env HOME="$RUNNER_TEMP/gnu-home" sh -c "$smoke" audit "$root" "$arch" glibc
if [[ "$arch" == x64 ]]; then
    docker run --rm --network none -v "$root:/bundle:ro" alpine:3.22 sh -c "$smoke" audit /bundle x64 musl
fi
