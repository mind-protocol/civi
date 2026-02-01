# Install Living Narrator Test Mod for CK3
# Run from PowerShell: .\install.ps1

$ModName = "ln_test"
$CK3ModsPath = "$env:USERPROFILE\Documents\Paradox Interactive\Crusader Kings III\mod"

# Create mods directory if it doesn't exist
if (!(Test-Path $CK3ModsPath)) {
    New-Item -ItemType Directory -Path $CK3ModsPath -Force
    Write-Host "Created mods directory: $CK3ModsPath"
}

# Get the script's directory (where the mod files are)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ModSourcePath = $ScriptDir

# Create mod folder in CK3 mods directory
$ModDestPath = Join-Path $CK3ModsPath $ModName
if (Test-Path $ModDestPath) {
    Remove-Item -Recurse -Force $ModDestPath
    Write-Host "Removed old mod installation"
}

# Copy mod folder
Copy-Item -Recurse $ModSourcePath $ModDestPath
Write-Host "Copied mod to: $ModDestPath"

# Copy the .mod file to the mods root
$ModFileSrc = Join-Path $ModSourcePath "$ModName.mod"
$ModFileDst = Join-Path $CK3ModsPath "$ModName.mod"
Copy-Item $ModFileSrc $ModFileDst -Force
Write-Host "Installed .mod file: $ModFileDst"

Write-Host ""
Write-Host "=== Installation Complete ==="
Write-Host "1. Launch CK3"
Write-Host "2. Go to Game Rules / Mods"
Write-Host "3. Enable 'Living Narrator Test'"
Write-Host "4. Start a game (can be Ironman)"
Write-Host "5. Click the 'Test Living Narrator Log' decision"
Write-Host "6. Check: $env:USERPROFILE\Documents\Paradox Interactive\Crusader Kings III\logs\debug.log"
Write-Host ""
Write-Host "Look for lines starting with [LN_EVENT] or [LN_TEST]"
