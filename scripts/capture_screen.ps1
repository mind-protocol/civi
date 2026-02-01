# Capture Screen for Living Narrator
# Takes periodic screenshots of the game for Claude to analyze

param(
    [int]$IntervalSeconds = 60,
    [string]$OutputDir = "C:\Temp\NarratorScreenshots",
    [switch]$Once,
    [int]$MaxFiles = 10
)

# Create output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

function Capture-Screen {
    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $filename = Join-Path $OutputDir "screen_$timestamp.png"

    # Get screen bounds
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen
    $bounds = $screen.Bounds

    # Create bitmap
    $bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)

    # Capture screen
    $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)

    # Save as PNG
    $bitmap.Save($filename, [System.Drawing.Imaging.ImageFormat]::Png)

    # Cleanup
    $graphics.Dispose()
    $bitmap.Dispose()

    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Captured: $filename"

    # Write latest path to a marker file
    $timestamp | Out-File -FilePath (Join-Path $OutputDir "latest.txt") -NoNewline

    # Cleanup old files (keep only MaxFiles most recent)
    $files = Get-ChildItem -Path $OutputDir -Filter "screen_*.png" | Sort-Object LastWriteTime -Descending
    if ($files.Count -gt $MaxFiles) {
        $files | Select-Object -Skip $MaxFiles | Remove-Item -Force
        Write-Host "  Cleaned up old screenshots (keeping last $MaxFiles)"
    }

    return $filename
}

if ($Once) {
    # Single capture mode
    $path = Capture-Screen
    Write-Host $path
    exit 0
}

# Continuous capture mode
Write-Host "=== Living Narrator Screen Capture ==="
Write-Host "Output: $OutputDir"
Write-Host "Interval: ${IntervalSeconds}s"
Write-Host "Max files: $MaxFiles"
Write-Host "Press Ctrl+C to stop"
Write-Host ""

while ($true) {
    Capture-Screen
    Start-Sleep -Seconds $IntervalSeconds
}
