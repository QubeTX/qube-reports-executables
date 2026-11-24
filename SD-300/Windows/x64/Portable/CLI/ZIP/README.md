## SD-300 v4.1.0

```powershell
& { $dest = Join-Path $env:LOCALAPPDATA "QubeTX\Portable\sd300\4.1.0\cli"; Expand-Archive -LiteralPath ".\tr300-tui-x86_64-pc-windows-msvc.zip" -DestinationPath $dest -ErrorAction Stop; & "$dest\sd300.exe" --version }
```
