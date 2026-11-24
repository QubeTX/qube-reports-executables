## TR-300 v4.5.1

```powershell
& { $dest = Join-Path $env:LOCALAPPDATA "QubeTX\Portable\tr300\4.5.1\cli"; Expand-Archive -LiteralPath ".\tr300-x86_64-pc-windows-msvc.zip" -DestinationPath $dest -ErrorAction Stop; & "$dest\tr300.exe" --version }
```
