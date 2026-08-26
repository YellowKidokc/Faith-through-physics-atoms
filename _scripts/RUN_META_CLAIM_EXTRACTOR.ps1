param(
    [string]$InputFile = "C:\theophysics\OPUS\CANON_ASSEMBLY\CANON_ASSEMBLED.md",
    [string]$Work = "",
    [int]$Turn = -1,
    [int]$Limit = 0,
    [switch]$Plan,
    [switch]$KeepGoing
)

$ErrorActionPreference = "Stop"
$Repo = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$Script = Join-Path $Repo "_scripts\meta_claim_extractor.py"

$argsList = @("--input", $InputFile)
if ($Work) { $argsList += @("--work", $Work) }
if ($Turn -ge 0) { $argsList += @("--turn", "$Turn") }
if ($Limit -gt 0) { $argsList += @("--limit", "$Limit") }
if ($Plan) { $argsList += "--plan" }
if ($KeepGoing) { $argsList += "--keep-going" }

python $Script @argsList
