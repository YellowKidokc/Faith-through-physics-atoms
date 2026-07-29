param(
  [string]$ProjectRoot = ".",
  [string]$Output = ""
)

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Guard = Join-Path $Here "canon_guard\canon_guard.py"
$Manifest = Join-Path $Here "canon_guard\canon-manifest.toml"

if ($Output -ne "") {
  python $Guard $ProjectRoot -m $Manifest --format json -o $Output
} else {
  python $Guard $ProjectRoot -m $Manifest
}
