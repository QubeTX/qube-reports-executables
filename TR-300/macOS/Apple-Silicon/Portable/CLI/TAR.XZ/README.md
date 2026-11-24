## TR-300 v4.5.1

```sh
dest="$HOME/.local/opt/qubetx/tr300/4.5.1/cli"
mkdir -p "$dest" &&
  tar -xf "./tr300-aarch64-apple-darwin.tar.xz" -C "$dest" &&
  "$dest/tr300-aarch64-apple-darwin/tr300" --version
```
