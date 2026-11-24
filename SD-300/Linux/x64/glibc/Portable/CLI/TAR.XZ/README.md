## SD-300 v4.1.0

```sh
dest="$HOME/.local/opt/qubetx/sd300/4.1.0/cli"
mkdir -p "$dest" &&
  tar -xf "./tr300-tui-x86_64-unknown-linux-gnu.tar.xz" -C "$dest" &&
  "$dest/tr300-tui-x86_64-unknown-linux-gnu/sd300" --version
```
