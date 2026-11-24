param([switch]$InsideGuest, [switch]$FullVM)
$ErrorActionPreference = 'Stop'
if (!$InsideGuest -and !$FullVM) {
    $root = Join-Path $env:RUNNER_TEMP 'qubetx-offline-bundle'
    $scripts = $PSScriptRoot
    $image = 'mcr.microsoft.com/windows/server:ltsc2022'
    docker pull $image
    if ($LASTEXITCODE -ne 0) { throw 'Could not prepare the base OS' }
    docker run --rm --network none --mount "type=bind,source=$root,target=C:\kit,readonly" --mount "type=bind,source=$scripts,target=C:\audit,readonly" --env "EDITION=$env:EDITION" --env "FORMAT=$env:FORMAT" $image powershell -NoProfile -ExecutionPolicy Bypass -File C:\audit\test-offline-windows.ps1 -InsideGuest
    exit $LASTEXITCODE
}
$root = if ($FullVM) { Join-Path $env:RUNNER_TEMP 'qubetx-offline-bundle' } else { 'C:\kit' }
if (!$FullVM -and ([Net.NetworkInformation.NetworkInterface]::GetAllNetworkInterfaces() | Where-Object { $_.OperationalStatus -eq 'Up' -and $_.NetworkInterfaceType -ne 'Loopback' -and $_.GetIPProperties().GatewayAddresses.Count -gt 0 })) { throw 'Unexpected network gateway' }
$products = (Get-Content (Join-Path $root 'bundle-manifest.json') -Raw | ConvertFrom-Json).products
$failures = @()
foreach ($p in $products) {
  try {
    $folder = Join-Path $root "$($p.id)/Windows/x64/$env:EDITION/$env:FORMAT"
    $file = (Get-ChildItem $folder -Filter "*.$env:FORMAT").FullName
    $log = Join-Path $env:TEMP "$($p.id)-offline.log"
    if ($env:FORMAT -eq 'MSI') {
        $proc = Start-Process msiexec.exe -ArgumentList "/i ""$file"" /qn /norestart /l*v ""$log""" -Wait -PassThru
    } else {
        $proc = Start-Process $file -ArgumentList "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /LOG=""$log""" -Wait -PassThru
    }
    if ($proc.ExitCode -notin 0,3010) {
        Select-String -LiteralPath $log -Pattern 'Return value 3','PrepareToInstall failed','CustomAction .* returned','Error [1-9][0-9]{3}' -Context 4,2 | Select-Object -First 12
        if ($p.id -eq 'TR-300') {
            $portable = Join-Path $env:TEMP 'preflight-probe'
            $zip = Get-ChildItem (Join-Path $root 'TR-300/Windows/x64/Portable/CLI/ZIP') -Filter '*.zip'
            Expand-Archive $zip.FullName $portable
            & (Join-Path $portable 'tr300.exe') --version
            $dest = if ($env:EDITION -eq 'Corporate') { Join-Path $env:LOCALAPPDATA 'Programs/tr300/bin/tr300.exe' } else { Join-Path $env:ProgramFiles 'tr300/bin/tr300.exe' }
            & (Join-Path $portable 'tr300.exe') migrate-cleanup --strict --dry-run --cargo-copy --native-destination $dest
        }
        throw "$($p.id) $env:FORMAT installer exit $($proc.ExitCode)"
    }
    $base = if ($env:EDITION -eq 'Corporate') { Join-Path $env:LOCALAPPDATA 'Programs' } else { $env:ProgramFiles }
    $tool = Join-Path $base $p.commands[0]
    foreach ($cmd in $p.commands) {
        $exe = Join-Path $tool "bin/$cmd.exe"
        $version = & $exe --version | Out-String
        if ($LASTEXITCODE -ne 0 -or !$version.Contains($p.tag.Substring(1))) { throw "$cmd version failed" }
        Write-Output "INSTALLED FROM LOCAL MEDIA $env:EDITION $env:FORMAT $exe $version"
    }
    if ($p.id -eq 'SD-300') {
        $stdout = Join-Path $env:TEMP 'desktop-self-test.json'
        $process = Start-Process -FilePath (Join-Path $tool 'app/sd300-gui.exe') -ArgumentList '--self-test','--json' -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput $stdout -RedirectStandardError "$stdout.err"
        $result = Get-Content $stdout -Raw | ConvertFrom-Json
        if ($process.ExitCode -ne 0 -or !$result.success -or $result.product_version -ne '4.1.0') { throw 'SD-300 desktop self-test failed' }
        Write-Output "LOCAL DESKTOP SELF-TEST PASSED $($result.product_version)"
    }
  } catch {
    $failures += "$($p.id): $_"
    Write-Output $failures[-1]
  }
}
if ($failures.Count -gt 0) { throw ($failures -join ', ') }
