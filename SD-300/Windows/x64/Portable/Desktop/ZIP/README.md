## SD-300 v4.1.0

```powershell
$dest = Join-Path $env:LOCALAPPDATA "QubeTX\Portable\sd300\4.1.0\desktop"
Expand-Archive -LiteralPath ".\sd300-gui-windows-x86_64.zip" -DestinationPath $dest -ErrorAction Stop
& "$dest\sd300-gui.exe"
```
