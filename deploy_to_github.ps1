# ==============================================================================
# OmniTrack | Automated Git & GitHub Deployment Script
# ==============================================================================

$env:Path = "C:\Users\promoth\AppData\Local\MinGit\cmd;C:\Users\promoth\AppData\Local\MinGit\mingw64\bin;" + $env:Path

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " OmniTrack: Deploying to Git and GitHub                          " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

$projectDir = "C:\Users\promoth\.gemini\antigravity\scratch\marketing_analytics_attribution"
Set-Location $projectDir

Write-Host "`n[1/4] Verifying local Git repository..." -ForegroundColor Yellow
git status

Write-Host "`n[2/4] Setting default branch to main..." -ForegroundColor Yellow
git branch -M main

# Check if remote origin already exists
$existingRemote = git remote get-url origin 2>$null
if (-not $existingRemote) {
    Write-Host "`n[3/4] Adding GitHub remote origin..." -ForegroundColor Yellow
    $repoUrl = "https://github.com/promoth96/marketing-analytics-attribution.git"
    git remote add origin $repoUrl
    Write-Host "Added remote: $repoUrl" -ForegroundColor Green
} else {
    Write-Host "`n[3/4] Remote origin already set to: $existingRemote" -ForegroundColor Green
}

Write-Host "`n[4/4] Pushing code to GitHub (main branch)..." -ForegroundColor Yellow
Write-Host "Note: If prompted, sign in via your browser in the pop-up window." -ForegroundColor Gray

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=================================================================" -ForegroundColor Green
    Write-Host " [SUCCESS] Code successfully pushed to GitHub!                  " -ForegroundColor Green
    Write-Host " Repository URL: https://github.com/promoth96/marketing-analytics-attribution" -ForegroundColor Green
    Write-Host "=================================================================" -ForegroundColor Green
    Write-Host "`nTo activate GitHub Pages:" -ForegroundColor Cyan
    Write-Host "1. Open https://github.com/promoth96/marketing-analytics-attribution/settings/pages"
    Write-Host "2. Under 'Source', select 'Deploy from a branch'."
    Write-Host "3. Select branch: 'main' and folder: '/ (root)'."
    Write-Host "4. Click Save. Your dashboard will be live at:"
    Write-Host "   https://promoth96.github.io/marketing-analytics-attribution/" -ForegroundColor Green
} else {
    Write-Host "`n[!] Push incomplete. Please ensure:" -ForegroundColor Red
    Write-Host "1. You have created the repository 'marketing-analytics-attribution' on https://github.com/new"
    Write-Host "2. You are logged into GitHub with account 'promoth96'"
}

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
