## ND-300 v4.0.2

```sh
(mount_dir=$(mktemp -d) && trap 'rmdir "$mount_dir" || exit 1' 0 && hdiutil attach -readonly -nobrowse -mountpoint "$mount_dir" "./nd300-universal-apple-darwin.dmg" && trap 'hdiutil detach "$mount_dir" && rmdir "$mount_dir" || exit 1' 0 && sudo /usr/sbin/installer -pkg "$mount_dir/nd300.pkg" -target /)
```
