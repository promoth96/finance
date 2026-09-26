# ==============================================================================
# OmniTrack | Push & Deploy to promoth96/finance on GitHub
# ==============================================================================

$env:Path = "C:\Users\promoth\AppData\Local\MinGit\cmd;C:\Users\promoth\AppData\Local\MinGit\mingw64\bin;" + $env:Path

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " OmniTrack: Deploying to GitHub Repository: promoth96/finance    " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

$projectDir = "C:\Users\promoth\.gemini\antigravity\scratch\marketing_analytics_attribution"
Set-Location $projectDir

Write-Host "`n[1/3] Setting remote origin to https://github.com/promoth96/finance.git..." -ForegroundColor Yellow
git remote set-url origin https://github.com/promoth96/finance.git

Write-Host "`n[2/3] Checking Git status..." -ForegroundColor Yellow
git status

Write-Host "`n[3/3] Pushing to main branch..." -ForegroundColor Yellow
Write-Host "If the Git Credential Manager window pops up, click 'Sign in with your browser'." -ForegroundColor Cyan

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=================================================================" -ForegroundColor Green
    Write-Host " [SUCCESS] Successfully pushed to https://github.com/promoth96/finance" -ForegroundColor Green
    Write-Host "=================================================================" -ForegroundColor Green
    Write-Host "`nTo enable GitHub Pages for the web dashboard:" -ForegroundColor Cyan
    Write-Host "1. Go to https://github.com/promoth96/finance/settings/pages"
    Write-Host "2. Under 'Source', select 'Deploy from a branch'."
    Write-Host "3. Select branch 'main' and folder '/ (root)'."
    Write-Host "4. Click Save. Dashboard will be live at:"
    Write-Host "   https://promoth96.github.io/finance/" -ForegroundColor Green
} else {
    Write-Host "`n[!] Push requires authentication." -ForegroundColor Red
    Write-Host "If you have a Personal Access Token (PAT), you can run:" -ForegroundColor Yellow
    Write-Host "git push https://<YOUR_TOKEN>@github.com/promoth96/finance.git main" -ForegroundColor Yellow
}

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
