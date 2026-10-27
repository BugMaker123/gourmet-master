# ==============================================================================
# Gourmet Master Skill - Windows One-Click Installer for Gemini / Antigravity
# ==============================================================================

$ErrorActionPreference = "Stop"

$skillName = "gourmet-master"
$targetDir = Join-Path $env:USERPROFILE ".gemini\config\skills\$skillName"
$repoUrl = "https://github.com/BugMaker123/gourmet-master.git"

Write-Host ">>> [1/3] Checking target directory: $targetDir" -ForegroundColor Cyan

if (Test-Path $targetDir) {
    Write-Host ">>> Updating existing skill directory..." -ForegroundColor Yellow
    Set-Location $targetDir
    if (Test-Path (Join-Path $targetDir ".git")) {
        git pull origin main
    } else {
        Write-Host "Removing old non-git directory..."
        Remove-Item -Path $targetDir -Recurse -Force
        git clone $repoUrl $targetDir
    }
} else {
    Write-Host ">>> [2/3] Cloning skill repository..." -ForegroundColor Cyan
    $parentDir = Split-Path $targetDir -Parent
    if (!(Test-Path $parentDir)) {
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
    }
    git clone $repoUrl $targetDir
}

Write-Host ">>> [3/3] Installation successful!" -ForegroundColor Green
Write-Host "---------------------------------------------------------" -ForegroundColor Green
Write-Host "Skill 'gourmet-master' is now installed and active!" -ForegroundColor Green
Write-Host "Location: $targetDir" -ForegroundColor Green
Write-Host "You can now ask Gemini / Antigravity for fitness diets, Chinese, Western, and cult foods!" -ForegroundColor Green
Write-Host "---------------------------------------------------------" -ForegroundColor Green
