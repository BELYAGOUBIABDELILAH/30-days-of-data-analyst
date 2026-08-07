# =============================================================
# setup_branches.ps1
# Run this ONCE when you are ready to go live.
# It will:
#   1. Create a 'staging' branch with all 30 day folders
#   2. Strip 'main' to only README.md, progress.json, workflow
#   3. Print instructions to push both branches
# =============================================================

$ErrorActionPreference = "Stop"
$repo = "c:\Users\RAM Tech\Desktop\30-days-of-data-analyst-"
Set-Location $repo

Write-Host "`n=== Step 1: Create 'staging' branch from current main ===" -ForegroundColor Cyan
git checkout -b staging
if ($LASTEXITCODE -ne 0) {
    Write-Host "Branch 'staging' may already exist, switching to it..." -ForegroundColor Yellow
    git checkout staging
}

Write-Host "`n=== Step 2: Add all 30 day folders to staging and commit ===" -ForegroundColor Cyan
git add "Day 1 -Tesla-Stock-Analysis"
git add "Day 2 -Zomato-Restaurant-Analysis"
git add "Day 3 -Amazon-Electronics-Analysis"
git add "Day 4 -Global-GDP-Analysis"
git add "Day 5 -Spotify-Music-Analysis"
git add "Day 6 -Sales-Dashboard"
git add "Day 7 -Insurance-Analysis"
git add "Day 8 -Twitter-Analysis"
git add "Day 9 -Economy-Indicators"
git add "Day 10 -Bank-Bankruptcy-Analysis"
git add "Day 11 -Clustering-Analysis"
git add "Day 12 -Sales-Performance-Analysis"
git add "Day 13 -Sales-Team-Performance"
git add "Day 14 -Supermarket-Analysis"
git add "Day 15 -Romanian-Energy-Prices"
git add "Day 16 -Credit-Card-Analysis"
git add "Day 17 -Sports-Rankings"
git add "Day 18 -Delhi-Air-Quality"
git add "Day 19 -YouTube-Channels-Analysis"
git add "Day 20 -Movie-Analysis"
git add "Day 21 -Cisco-Stock-Analysis"
git add "Day 22 -Emergency-Calls-Analysis"
git add "Day 23 -Global-Terrorism-Analysis"
git add "Day 24 -Global-Terrorism-Dashboard"
git add "Day 25 -Horror-Movies-Analysis"
git add "Day 26 -Billionaire-Analysis"
git add "Day 27 -COVID-Analysis"
git add "Day 28 -Medical-Conditions-Analysis"
git add "Day 29 -Retail-Analytics"
git add "Day 30 -Used-Car-Analysis"
git add "README.md"
git add "progress.json"
git add ".github"

$stagedCount = (git diff --cached --name-only | Measure-Object -Line).Lines
if ($stagedCount -gt 0) {
    git commit -m "chore: add all 30 days to staging branch"
    Write-Host "Committed $stagedCount files to staging." -ForegroundColor Green
} else {
    Write-Host "Nothing new to commit on staging (already up to date)." -ForegroundColor Yellow
}

Write-Host "`n=== Step 3: Switch back to main and clean it up ===" -ForegroundColor Cyan
git checkout main

# Remove all day folders from main (they will be added daily by the Action)
$dayFolders = Get-ChildItem -Directory -Filter "Day *"
foreach ($folder in $dayFolders) {
    Write-Host "  Removing from main: $($folder.Name)" -ForegroundColor Gray
    git rm -r --cached "$($folder.Name)" 2>$null
    Remove-Item -Recurse -Force $folder.FullName -ErrorAction SilentlyContinue
}

# Make sure the workflow and progress file exist on main
if (-Not (Test-Path ".github\workflows\daily-release.yml")) {
    Write-Host "ERROR: workflow file missing!" -ForegroundColor Red
    exit 1
}

git add README.md progress.json .github
git add -u  # Stage all removals

$stagedMain = (git diff --cached --name-only | Measure-Object -Line).Lines
if ($stagedMain -gt 0) {
    git commit -m "chore: strip day folders from main (automated daily release active)"
    Write-Host "Main branch cleaned." -ForegroundColor Green
} else {
    Write-Host "Main already clean." -ForegroundColor Yellow
}

Write-Host "`n=== DONE ===" -ForegroundColor Green
Write-Host ""
Write-Host "When you are ready to go live, run these two commands:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  git push origin main" -ForegroundColor White
Write-Host "  git push origin staging" -ForegroundColor White
Write-Host ""
Write-Host "GitHub Actions will release Day 1 tonight at 7 PM (UTC+1)." -ForegroundColor Cyan
Write-Host "To test manually: go to GitHub > Actions > Daily Release > Run workflow" -ForegroundColor Cyan
