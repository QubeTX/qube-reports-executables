## TR-300 v4.5.1

```sh
dest="$HOME/.local/opt/qubetx/tr300/4.5.1/cli"
mkdir -p "$dest" &&
  tar -xf "./tr300-x86_64-unknown-linux-musl.tar.xz" -C "$dest" &&
  "$dest/tr300-x86_64-unknown-linux-musl/tr300" --version
```
