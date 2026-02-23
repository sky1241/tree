# WINTER TREE — Installe les hooks dans TOUS les repos
# Usage: powershell scripts/install_all_hooks.ps1
#
# Lit repos.json, copie le hook dans chaque repo/.git/hooks/pre-commit

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (!(Test-Path (Join-Path $root "repos.json"))) {
    # On est peut-être appelé depuis la racine
    $root = Split-Path -Parent $PSScriptRoot
    if (!(Test-Path (Join-Path $root "repos.json"))) {
        $root = $PSScriptRoot
        if (!(Test-Path (Join-Path $root "repos.json"))) {
            Write-Host "❌ repos.json introuvable" -ForegroundColor Red
            exit 1
        }
    }
}

$reposJson = Get-Content (Join-Path $root "repos.json") | ConvertFrom-Json
$hookTemplate = Join-Path $root "hooks" "repo-hook-template.py"
$treeHook = Join-Path $root "hooks" "pre-commit"

if (!(Test-Path $hookTemplate)) {
    Write-Host "❌ hooks/repo-hook-template.py introuvable" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "  🌲 INSTALL ALL HOOKS" -ForegroundColor Green
Write-Host "  $('─' * 50)"

$installed = 0
$skipped = 0

foreach ($repo in $reposJson.repos) {
    if (!$repo.active) { continue }
    
    $name = $repo.name
    $localPath = $repo.local_path
    
    if (!$localPath -or !(Test-Path $localPath)) {
        Write-Host "  ⚠️  ${name}: chemin invalide → skip" -ForegroundColor Yellow
        $skipped++
        continue
    }
    
    $gitHooks = Join-Path $localPath ".git" "hooks"
    if (!(Test-Path $gitHooks)) {
        Write-Host "  ⚠️  ${name}: pas de .git/hooks → skip" -ForegroundColor Yellow
        $skipped++
        continue
    }
    
    $target = Join-Path $gitHooks "pre-commit"
    
    if ($name -eq "tree") {
        Copy-Item $treeHook $target -Force
        Write-Host "  ✅ ${name}: hook tree" -ForegroundColor Green
    } else {
        Copy-Item $hookTemplate $target -Force
        Write-Host "  ✅ ${name}: hook template" -ForegroundColor Green
    }
    $installed++
}

Write-Host ""
Write-Host "  $('─' * 50)"
Write-Host "  ✅ $installed installés | ⚠️ $skipped skippés" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════
# BONUS: Ajouter la fonction tree-sync au profil PowerShell
# ═══════════════════════════════════════════════════════

Write-Host "  💡 Pour avoir la commande 'tree-sync' partout:" -ForegroundColor Cyan
Write-Host "     Ajoute ceci à ton profil PowerShell ($PROFILE):" -ForegroundColor Cyan
Write-Host ""
Write-Host "     function tree-sync {" -ForegroundColor DarkGray
Write-Host "         python '$root\scripts\sync_all.py' @args" -ForegroundColor DarkGray
Write-Host "     }" -ForegroundColor DarkGray
Write-Host ""
Write-Host "     Puis: tree-sync              # sync tout" -ForegroundColor DarkGray
Write-Host "           tree-sync --one shazam  # sync un seul" -ForegroundColor DarkGray
Write-Host "           tree-sync --github      # via GitHub API" -ForegroundColor DarkGray
Write-Host "           tree-sync --clean       # nettoie doublons" -ForegroundColor DarkGray
