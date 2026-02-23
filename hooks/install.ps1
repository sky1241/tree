# WINTER TREE — Install git hooks (Windows)
$hookSrc = Join-Path $PSScriptRoot "pre-commit"
$hookDst = Join-Path (git rev-parse --git-dir) "hooks" "pre-commit"
Copy-Item $hookSrc $hookDst -Force
Write-Host "[winter-tree] Hook installe: $hookDst" -ForegroundColor Green
