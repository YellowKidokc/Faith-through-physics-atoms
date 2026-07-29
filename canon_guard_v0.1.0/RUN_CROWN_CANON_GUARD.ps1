$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Guard = Join-Path $PSScriptRoot "canon_guard\canon_guard.py"
$Manifest = Join-Path $PSScriptRoot "canon_guard\crown-canon-manifest.toml"
$OutDir = Join-Path $Root "_runtime\canon_guard"

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$TextReport = Join-Path $OutDir "crown-canon-report.txt"
$JsonReport = Join-Path $OutDir "crown-canon-report.json"
$ReviewPacket = Join-Path $OutDir "crown-canon-review-packet.json"

python $Guard $Root -m $Manifest -o $TextReport
$ExitCode = $LASTEXITCODE

python $Guard $Root -m $Manifest --format json -o $JsonReport --review-packet $ReviewPacket
if ($LASTEXITCODE -gt $ExitCode) {
  $ExitCode = $LASTEXITCODE
}

Write-Host "Crown Canon Guard report:"
Write-Host $TextReport
Write-Host $JsonReport
Write-Host $ReviewPacket

exit $ExitCode

