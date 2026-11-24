## ND-300 v4.0.2

```powershell
& { $dest = Join-Path $env:LOCALAPPDATA "QubeTX\Portable\nd300\4.0.2\cli"; Expand-Archive -LiteralPath ".\nd300-x86_64-pc-windows-msvc.zip" -DestinationPath $dest -ErrorAction Stop; & "$dest\nd300.exe" --version }
```
