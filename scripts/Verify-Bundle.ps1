# Verify the complete extracted bundle without a network connection.
param([string]$Root = (Split-Path -Parent $PSScriptRoot))
$ErrorActionPreference = 'Stop'
$bundleRoot = (Resolve-Path -LiteralPath $Root).Path
$prefix = $bundleRoot.TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar
$checked = 0
foreach ($line in Get-Content -LiteralPath (Join-Path $bundleRoot 'SHA256SUMS.txt')) {
    if ($line -notmatch '^([0-9a-f]{64})  (.+)$') { throw "Invalid checksum entry" }
    $expected = $Matches[1]
    $relative = $Matches[2]
    $path = [IO.Path]::GetFullPath((Join-Path $bundleRoot $relative))
    if (-not $path.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) { throw "Path outside bundle: $relative" }
    $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    if ($actual -ne $expected) { throw "Checksum mismatch: $relative" }
    $checked++
}
Write-Output "Verified $checked files. All SHA-256 checksums match."
