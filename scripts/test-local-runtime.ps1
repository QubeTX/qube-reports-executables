param([switch]$Guest)
$ErrorActionPreference = 'Stop'
if (!$Guest) {
    $image = 'mcr.microsoft.com/windows/servercore:ltsc2022'
    docker pull $image
    if ($LASTEXITCODE) { throw 'Could not prepare the guest OS' }
    $runtime = Join-Path $env:RUNNER_TEMP 'qubetx-offline-bundle/SD-300/Windows/x64/Runtime'
    docker run --rm --network none --mount "type=bind,source=$runtime,target=C:\media,readonly" --mount "type=bind,source=$PSScriptRoot,target=C:\audit,readonly" $image powershell -NoProfile -File C:\audit\test-local-runtime.ps1 -Guest
    exit $LASTEXITCODE
}
$dll = Join-Path $env:WINDIR 'System32\vcruntime140.dll'
$before = if (Test-Path $dll) { (Get-Item $dll).VersionInfo.FileVersion } else { 'absent' }
Write-Output "Runtime before installation: $before"
$p = Start-Process -FilePath C:\media\vc_redist.x64.exe -ArgumentList '/install','/quiet','/norestart','/log','C:\runtime-install.log' -Wait -PassThru -WindowStyle Hidden
if ($p.ExitCode -notin 0,3010) {
    Select-String -Path C:\runtime-install.log -Pattern 'Error 0x','Apply complete' | Select-Object -Last 10
    throw "Runtime installer exited $($p.ExitCode)"
}
$after = (Get-Item $dll).VersionInfo.FileVersion
if ($after -ne '14.52.37029.0') { throw "Unexpected runtime version $after" }
Write-Output "Installed signed x64 runtime from local media with networking disabled: $after"
