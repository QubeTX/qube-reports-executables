## ND-300 v4.0.2

```sh
dest="$HOME/.local/opt/qubetx/nd300/4.0.2/cli"
mkdir -p "$dest" &&
  tar -xf "./nd300-x86_64-apple-darwin.tar.xz" -C "$dest" &&
  "$dest/nd300-x86_64-apple-darwin/nd300" --version
```
