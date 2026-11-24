## TR-300 v4.5.1

```sh
mount_dir=$(mktemp -d)
hdiutil attach -readonly -nobrowse -mountpoint "$mount_dir" "./tr300-universal-apple-darwin.dmg" &&
  sudo /usr/sbin/installer -pkg "$mount_dir/tr300.pkg" -target /
hdiutil detach "$mount_dir" && rmdir "$mount_dir"
```
