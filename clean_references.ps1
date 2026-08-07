# Clean all HARSHKUMAR65 references and replace with BELYAGOUBIABDELILAH

$ErrorActionPreference = "Stop"

$yourName = "BELYAGOUBIABDELILAH"
$yourGithub = "https://github.com/BELYAGOUBIABDELILAH"
$yourProfile = "[BELYAGOUBIABDELILAH](https://github.com/BELYAGOUBIABDELILAH)"

Write-Host "Cleaning references in all notebooks..." -ForegroundColor Cyan

$notebooks = Get-ChildItem -Path "Day *" -Recurse -Filter "*.ipynb"

foreach ($notebook in $notebooks) {
    Write-Host "Processing: $($notebook.FullName)" -ForegroundColor White
    
    $content = Get-Content $notebook.FullName -Raw -Encoding UTF8
    $changed = $false
    
    # Replace HARSHKUMAR65 with BELYAGOUBIABDELILAH
    if ($content -match "HARSHKUMAR65") {
        $content = $content -replace "HARSHKUMAR65", $yourName
        $changed = $true
        Write-Host "  Replaced HARSHKUMAR65" -ForegroundColor Yellow
    }
    
    # Replace harsh kumar variations
    if ($content -match "harsh kumar|Harsh Kumar|HARSH KUMAR") {
        $content = $content -replace "harsh kumar|Harsh Kumar|HARSH KUMAR", $yourName
        $changed = $true
        Write-Host "  Replaced Harsh Kumar" -ForegroundColor Yellow
    }
    
    # Replace old GitHub links
    if ($content -match "github\.com/HARSHKUMAR65") {
        $content = $content -replace "github\.com/HARSHKUMAR65", "github.com/$yourName"
        $changed = $true
        Write-Host "  Replaced GitHub link" -ForegroundColor Yellow
    }
    
    # Remove external links to Kaggle, other repos, etc.
    if ($content -match "kaggle\.com|\\[.*?\\]\\(http[^)]+\\)" -and $content -notmatch "github\.com/BELYAGOUBIABDELILAH") {
        # This is complex - will handle manually if needed
        Write-Host "  WARNING: External links found - review manually" -ForegroundColor Red
    }
    
    if ($changed) {
        Set-Content -Path $notebook.FullName -Value $content -Encoding UTF8 -NoNewline
        Write-Host "  Saved changes" -ForegroundColor Green
    }
}

Write-Host "`n--- Cleaning complete! ---" -ForegroundColor Green
Write-Host "Please manually review notebooks for any remaining external references."
