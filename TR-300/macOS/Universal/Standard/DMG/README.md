## TR-300 v4.5.1

```sh
(mount_dir=$(mktemp -d) && trap 'rmdir "$mount_dir" || exit 1' 0 && hdiutil attach -readonly -nobrowse -mountpoint "$mount_dir" "./tr300-universal-apple-darwin.dmg" && trap 'hdiutil detach "$mount_dir" && rmdir "$mount_dir" || exit 1' 0 && sudo /usr/sbin/installer -pkg "$mount_dir/tr300.pkg" -target /)
```
