param(
    [int]$Port = 8787,
    [switch]$NoBrowser
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$url = "http://127.0.0.1:$Port"

if (-not $NoBrowser) {
    Start-Process $url
}

python (Join-Path $repo '_scripts\claim_pipeline_service.py') --host 127.0.0.1 --port $Port
