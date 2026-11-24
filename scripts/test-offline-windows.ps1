param([switch]$InsideGuest)
$ErrorActionPreference = 'Stop'
if (!$InsideGuest) {
    $root = Join-Path $env:RUNNER_TEMP 'qubetx-offline-bundle'
    $scripts = $PSScriptRoot
    $image = 'mcr.microsoft.com/windows/servercore:ltsc2022'
    docker pull $image
    if ($LASTEXITCODE -ne 0) { throw 'Could not prepare the base OS' }
    docker run --rm --network none --mount "type=bind,source=$root,target=C:\kit,readonly" --mount "type=bind,source=$scripts,target=C:\audit,readonly" --env "EDITION=$env:EDITION" --env "FORMAT=$env:FORMAT" $image powershell -NoProfile -ExecutionPolicy Bypass -File C:\audit\test-offline-windows.ps1 -InsideGuest
    exit $LASTEXITCODE
}
$root = 'C:\kit'
if ([Net.NetworkInformation.NetworkInterface]::GetAllNetworkInterfaces() | Where-Object { $_.OperationalStatus -eq 'Up' -and $_.NetworkInterfaceType -ne 'Loopback' -and $_.GetIPProperties().GatewayAddresses.Count -gt 0 }) { throw 'Unexpected network gateway' }
$products = (Get-Content (Join-Path $root 'bundle-manifest.json') -Raw | ConvertFrom-Json).products
foreach ($p in $products) {
    $folder = Join-Path $root "$($p.id)/Windows/x64/$env:EDITION/$env:FORMAT"
    $file = (Get-ChildItem $folder -Filter "*.$env:FORMAT").FullName
    $log = Join-Path $env:TEMP "$($p.id)-offline.log"
    if ($env:FORMAT -eq 'MSI') {
        $proc = Start-Process msiexec.exe -ArgumentList "/i ""$file"" /qn /norestart /l*v ""$log""" -Wait -PassThru
    } else {
        $proc = Start-Process $file -ArgumentList "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /LOG=""$log""" -Wait -PassThru
    }
    if ($proc.ExitCode -notin 0,3010) {
        Get-Content $log -Tail 50
        throw "$($p.id) $env:FORMAT installer exit $($proc.ExitCode)"
    }
    $base = if ($env:EDITION -eq 'Corporate') { Join-Path $env:LOCALAPPDATA 'Programs' } else { $env:ProgramFiles }
    $tool = Join-Path $base $p.commands[0]
    foreach ($cmd in $p.commands) {
        $exe = Join-Path $tool "bin/$cmd.exe"
        $version = & $exe --version | Out-String
        if ($LASTEXITCODE -ne 0 -or !$version.Contains($p.tag.Substring(1))) { throw "$cmd version failed" }
        Write-Output "OFFLINE INSTALLED $env:EDITION $env:FORMAT $exe $version"
    }
    if ($p.id -eq 'SD-300' -and !(Test-Path (Join-Path $tool 'app/sd300-gui.exe'))) { throw 'Missing installed desktop app' }
}
