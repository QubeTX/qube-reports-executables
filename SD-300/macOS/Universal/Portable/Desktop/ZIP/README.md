## SD-300 v4.1.0

```sh
dest="$HOME/.local/opt/qubetx/sd300/4.1.0/desktop"
mkdir -p "$dest" &&
  ditto -x -k "./sd300-gui-macos-universal.zip" "$dest" &&
  open "$dest/SD-300.app"
```
