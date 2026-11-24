## ND-300 v4.0.2

```sh
mount_dir=$(mktemp -d)
hdiutil attach -readonly -nobrowse -mountpoint "$mount_dir" "./nd300-universal-apple-darwin.dmg" &&
  sudo /usr/sbin/installer -pkg "$mount_dir/nd300.pkg" -target /
hdiutil detach "$mount_dir" && rmdir "$mount_dir"
```
