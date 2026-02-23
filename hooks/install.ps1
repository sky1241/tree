# WINTER TREE — Installe le hook dans le repo tree
# Usage: powershell hooks/install.ps1

$hookSrc = Join-Path $PSScriptRoot "pre-commit"
$hookDst = Join-Path $PSScriptRoot ".." ".git" "hooks" "pre-commit"

if (!(Test-Path $hookSrc)) {
    Write-Host "❌ hooks/pre-commit introuvable" -ForegroundColor Red
    exit 1
}

Copy-Item $hookSrc $hookDst -Force
Write-Host "✅ Hook installé dans tree/.git/hooks/pre-commit" -ForegroundColor Green
