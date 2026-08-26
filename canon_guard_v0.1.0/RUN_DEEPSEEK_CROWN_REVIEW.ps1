$ErrorActionPreference = "Stop"

$Script = Join-Path $PSScriptRoot "canon_guard\deepseek_crown_review.py"
python $Script

