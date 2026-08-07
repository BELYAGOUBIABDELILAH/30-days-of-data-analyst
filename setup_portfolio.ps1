# Portfolio Setup Script
# This script structures all 30 days properly for BELYAGOUBIABDELILAH

$ErrorActionPreference = "Stop"

# Mapping of day numbers to project names (from README.md)
$dayProjects = @{
    1 = "Tesla-Stock-Analysis"
    2 = "Zomato-Restaurant-Analysis"
    3 = "Amazon-Electronics-Analysis"
    4 = "Global-GDP-Analysis"
    5 = "Spotify-Music-Analysis"
    6 = "Sales-Dashboard"
    7 = "Insurance-Analysis"
    8 = "Twitter-Analysis"
    9 = "Economy-Indicators"
    10 = "Bank-Bankruptcy-Analysis"
    11 = "Clustering-Analysis"
    12 = "Sales-Performance-Analysis"
    13 = "Sales-Team-Performance"
    14 = "Supermarket-Analysis"
    15 = "Romanian-Energy-Prices"
    16 = "Credit-Card-Analysis"
    17 = "Sports-Rankings"
    18 = "Delhi-Air-Quality"
    19 = "YouTube-Channels-Analysis"
    20 = "Movie-Analysis"
    21 = "Cisco-Stock-Analysis"
    22 = "Emergency-Calls-Analysis"
    23 = "Global-Terrorism-Analysis"
    24 = "Global-Terrorism-Dashboard"
    25 = "Horror-Movies-Analysis"
    26 = "Billionaire-Analysis"
    27 = "COVID-Analysis"
    28 = "Medical-Conditions-Analysis"
    29 = "Retail-Analytics"
    30 = "Used-Car-Analysis"
}

Write-Host "Starting portfolio restructure..." -ForegroundColor Cyan

foreach ($day in 1..30) {
    $projectName = $dayProjects[$day]
    $targetFolder = "Day $day -$projectName"
    
    # Find source folder (handle inconsistent naming)
    $sourceFolder = $null
    $possibleSources = @(
        "temp_source/Day $day",
        "temp_source/Day_$day",
        "temp_source/Day$day"
    )
    
    foreach ($src in $possibleSources) {
        if (Test-Path $src) {
            $sourceFolder = $src
            break
        }
    }
    
    if (-not $sourceFolder) {
        Write-Host "WARNING: Day $day source not found, skipping..." -ForegroundColor Yellow
        continue
    }
    
    Write-Host "`nProcessing Day $day - $projectName" -ForegroundColor Green
    
    # Create target folder structure
    New-Item -ItemType Directory -Path $targetFolder -Force | Out-Null
    New-Item -ItemType Directory -Path "$targetFolder/data" -Force | Out-Null
    
    # Copy and process files
    $files = Get-ChildItem -Path $sourceFolder -File
    
    foreach ($file in $files) {
        $fileName = $file.Name
        
        # Skip unnecessary files
        if ($fileName -match "\.log$|untitled\.txt|\.py$|clean_data|\.pdf$|\.pbit$") {
            Write-Host "  Skipping: $fileName" -ForegroundColor Gray
            continue
        }
        
        # Rename notebooks to standard format
        if ($fileName -match "\.ipynb$") {
            $newName = "Day-$day.ipynb"
            Copy-Item $file.FullName "$targetFolder/$newName" -Force
            Write-Host "  Copied notebook as: $newName" -ForegroundColor White
        }
        # Move data files to data folder
        elseif ($fileName -match "\.(csv|xlsx|json)$") {
            Copy-Item $file.FullName "$targetFolder/data/$fileName" -Force
            Write-Host "  Moved data: $fileName" -ForegroundColor White
        }
        # Copy Power BI files
        elseif ($fileName -match "\.pbix$") {
            Copy-Item $file.FullName "$targetFolder/$fileName" -Force
            Write-Host "  Copied: $fileName" -ForegroundColor White
        }
        # Copy SQL files
        elseif ($fileName -match "\.sql$") {
            Copy-Item $file.FullName "$targetFolder/$fileName" -Force
            Write-Host "  Copied: $fileName" -ForegroundColor White
        }
    }
    
    # Handle nested Data folders (like Day 6 and Day 12)
    if (Test-Path "$sourceFolder/Data") {
        $dataFiles = Get-ChildItem -Path "$sourceFolder/Data" -File -Recurse
        foreach ($dataFile in $dataFiles) {
            if ($dataFile.Name -match "\.(csv|xlsx|json)$") {
                Copy-Item $dataFile.FullName "$targetFolder/data/$($dataFile.Name)" -Force
                Write-Host "  Moved data: $($dataFile.Name)" -ForegroundColor White
            }
        }
    }
    
    if (Test-Path "$sourceFolder/Data_csv") {
        $dataFiles = Get-ChildItem -Path "$sourceFolder/Data_csv" -File -Recurse
        foreach ($dataFile in $dataFiles) {
            if ($dataFile.Name -match "\.(csv|xlsx|json)$") {
                Copy-Item $dataFile.FullName "$targetFolder/data/$($dataFile.Name)" -Force
                Write-Host "  Moved data: $($dataFile.Name)" -ForegroundColor White
            }
        }
    }
    
    # Create README.md for each day
    $readmeContent = @"
# Day $day - $($projectName -replace '-', ' ')

## Overview
Data analysis project focusing on $($projectName -replace '-', ' ' | ForEach-Object { $_.ToLower() }).

## Files
- ``Day-$day.ipynb`` - Main analysis notebook
- ``data/`` - Dataset(s) used in analysis

## Tools & Libraries
- Python 3
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn

## Author
[BELYAGOUBIABDELILAH](https://github.com/BELYAGOUBIABDELILAH)
"@
    
    Set-Content -Path "$targetFolder/README.md" -Value $readmeContent -Force
    Write-Host "  Created README.md" -ForegroundColor White
}

Write-Host "`n--- Portfolio restructure complete! ---" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Review the folders"
Write-Host "2. Clean up references in notebooks"
Write-Host "3. Delete temp_source folder"
