## SD-300 v4.1.0

```powershell
& { $system = if ([Environment]::Is64BitProcess) { "System32" } else { "Sysnative" }; $runtime = Join-Path $env:WINDIR "$system\vcruntime140.dll"; if (-not (Test-Path -LiteralPath $runtime)) { $setup = Start-Process -FilePath "..\..\..\Runtime\vc_redist.x64.exe" -Wait -ErrorAction Stop -PassThru; if ($setup.ExitCode -notin (0, 3010) -or -not (Test-Path -LiteralPath $runtime)) { throw "The Microsoft x64 runtime is required for SD-300 Desktop." } }; $dest = Join-Path $env:LOCALAPPDATA "QubeTX\Portable\sd300\4.1.0\desktop"; Expand-Archive -LiteralPath ".\sd300-gui-windows-x86_64.zip" -DestinationPath $dest -ErrorAction Stop; & "$dest\sd300-gui.exe" }
```
