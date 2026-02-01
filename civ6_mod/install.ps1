# install.ps1 - Installation simplifiée
# Exécuter depuis PowerShell Windows

$ModName = "LivingNarrator"

# Trouver le dossier Documents
$docs = [Environment]::GetFolderPath('MyDocuments')
Write-Host "Documents folder: $docs"

# Dossier Civ 6
$civBase = Join-Path $docs "My Games\Sid Meier's Civilization VI"
$modsDir = Join-Path $civBase "Mods"

if (-not (Test-Path $civBase)) {
    Write-Host "ERROR: Civ 6 folder not found at $civBase" -ForegroundColor Red
    Write-Host ""
    Write-Host "Trying alternative locations..."
    
    # Try OneDrive
    $oneDrive = $env:OneDrive
    if ($oneDrive) {
        $alt = Join-Path $oneDrive "Documents\My Games\Sid Meier's Civilization VI"
        if (Test-Path $alt) {
            $civBase = $alt
            $modsDir = Join-Path $civBase "Mods"
            Write-Host "Found at: $civBase" -ForegroundColor Green
        }
    }
}

if (-not (Test-Path $civBase)) {
    Write-Host ""
    Write-Host "Cannot find Civ 6 folder. Please enter the path manually:"
    Write-Host "Example: C:\Users\YourName\Documents\My Games\Sid Meier's Civilization VI"
    $civBase = Read-Host "Path"
    $modsDir = Join-Path $civBase "Mods"
}

Write-Host ""
Write-Host "=== Installing Living Narrator ===" -ForegroundColor Cyan

# Source (WSL path)
$wslSrc = "\\wsl.localhost\Ubuntu-22.04\home\mind-protocol\civi\civ6_mod"

# Destination
$dest = Join-Path $modsDir $ModName

# Create mod folder
Write-Host "Creating $dest ..."
New-Item -ItemType Directory -Path $dest -Force | Out-Null
New-Item -ItemType Directory -Path "$dest\Scripts" -Force | Out-Null

# Copy files
Write-Host "Copying files..."
Copy-Item "$wslSrc\LivingNarrator.modinfo" $dest -Force
Copy-Item "$wslSrc\Scripts\LivingNarrator.lua" "$dest\Scripts\" -Force

# Create output folder
$outputDir = Join-Path $docs "Civ6Narrator"
Write-Host "Creating output folder: $outputDir"
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

# Clear cache
Write-Host "Clearing mod cache..."
$cache = Join-Path $civBase "Cache"
$modsDb = Join-Path $civBase "Mods.sqlite"
Remove-Item $cache -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $modsDb -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "=== DONE ===" -ForegroundColor Green
Write-Host ""
Write-Host "Installed files:"
Get-ChildItem $dest -Recurse | ForEach-Object { Write-Host "  $($_.FullName)" }
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Launch Civ 6"
Write-Host "  2. Additional Content -> Enable 'Living Narrator'"
Write-Host "  3. Start a new game"
Write-Host "  4. Check: $outputDir\events.jsonl"
