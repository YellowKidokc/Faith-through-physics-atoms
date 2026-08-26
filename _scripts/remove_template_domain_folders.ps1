<#
.SYNOPSIS
Finds and optionally removes bogus _TEMPLATE_DOMAIN directories.

.DESCRIPTION
Dry-run by default. Pass -Delete to remove matches. The script only targets
directories whose leaf name is exactly "_TEMPLATE_DOMAIN".

.EXAMPLE
powershell -ExecutionPolicy Bypass -File _scripts/remove_template_domain_folders.ps1 -Root C:\theophysics

.EXAMPLE
powershell -ExecutionPolicy Bypass -File _scripts/remove_template_domain_folders.ps1 -Root C:\theophysics -Delete
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $false)]
    [string]$Root = "C:\theophysics",

    [Parameter(Mandatory = $false)]
    [switch]$Delete
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-ExistingDirectory {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        throw "Root does not exist or is not a directory: $Path"
    }

    return (Resolve-Path -LiteralPath $Path).ProviderPath
}

$resolvedRoot = Resolve-ExistingDirectory -Path $Root

if ($resolvedRoot -match '^[A-Za-z]:\\?$') {
    throw "Refusing to scan an entire drive root: $resolvedRoot"
}

$matches = Get-ChildItem -LiteralPath $resolvedRoot -Directory -Recurse -Force -Filter "_TEMPLATE_DOMAIN" -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -ceq "_TEMPLATE_DOMAIN" } |
    Sort-Object FullName

if (-not $matches) {
    Write-Output "No _TEMPLATE_DOMAIN directories found under $resolvedRoot"
    exit 0
}

foreach ($match in $matches) {
    $fullName = $match.FullName
    if (-not $fullName.StartsWith($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Resolved match escaped root. Refusing to continue: $fullName"
    }

    $fileCount = @(Get-ChildItem -LiteralPath $fullName -Recurse -Force -File -ErrorAction SilentlyContinue).Count
    $dirCount = @(Get-ChildItem -LiteralPath $fullName -Recurse -Force -Directory -ErrorAction SilentlyContinue).Count

    if ($Delete) {
        if ($PSCmdlet.ShouldProcess($fullName, "Remove _TEMPLATE_DOMAIN directory with $dirCount subdirectories and $fileCount files")) {
            Remove-Item -LiteralPath $fullName -Recurse -Force
            Write-Output "Removed: $fullName ($dirCount dirs, $fileCount files)"
        }
    }
    else {
        Write-Output "Found: $fullName ($dirCount dirs, $fileCount files)"
    }
}

if (-not $Delete) {
    Write-Output "Dry run only. Re-run with -Delete to remove these directories."
}
