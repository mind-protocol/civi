# Check debug.log for Living Narrator events
# Run from PowerShell: .\check_output.ps1

$LogPath = "$env:USERPROFILE\Documents\Paradox Interactive\Crusader Kings III\logs\debug.log"

if (!(Test-Path $LogPath)) {
    Write-Host "ERROR: debug.log not found at $LogPath" -ForegroundColor Red
    Write-Host "Have you launched CK3 yet?"
    exit 1
}

Write-Host "=== Living Narrator Events in debug.log ===" -ForegroundColor Cyan
Write-Host "Log file: $LogPath"
Write-Host ""

# Find all LN_EVENT and LN_TEST lines
$Events = Get-Content $LogPath | Where-Object { $_ -match "\[LN_" }

if ($Events.Count -eq 0) {
    Write-Host "No Living Narrator events found." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Possible reasons:"
    Write-Host "  1. Mod not installed/enabled"
    Write-Host "  2. Haven't started a new game yet"
    Write-Host "  3. debug_log doesn't work without -debug_mode"
    Write-Host ""
    Write-Host "Try launching CK3 with -debug_mode to confirm:"
    Write-Host "  Steam > CK3 > Properties > Launch Options > -debug_mode"
} else {
    Write-Host "Found $($Events.Count) events:" -ForegroundColor Green
    Write-Host ""
    $Events | ForEach-Object { Write-Host $_ }
}
