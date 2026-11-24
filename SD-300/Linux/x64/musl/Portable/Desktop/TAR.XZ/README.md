## SD-300 v4.1.0

```sh
dest="$HOME/.local/opt/qubetx/sd300/4.1.0/desktop"
mkdir -p "$dest" &&
  tar -xf "./sd300-gui-linux-musl-x86_64.tar.xz" -C "$dest" &&
  "$dest/sd300/bin/sd300-gui"
```
