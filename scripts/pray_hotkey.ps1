# Pray Hotkey - F9 to invoke the Chronicler
# Captures screen and signals the narrator for immediate response
# Run: powershell -ExecutionPolicy Bypass -File pray_hotkey.ps1

param(
    [string]$OutputDir = "C:\Temp\NarratorScreenshots",
    [string]$SignalDir = "\\wsl.localhost\Ubuntu-22.04\home\mind-protocol\duoai\narrator\state"
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Keyboard state detection
Add-Type @"
using System;
using System.Runtime.InteropServices;

public class KeyState {
    [DllImport("user32.dll")]
    public static extern short GetAsyncKeyState(int vKey);

    public static bool IsKeyDown(int vKey) {
        return (GetAsyncKeyState(vKey) & 0x8000) != 0;
    }
}
"@

# Create directories
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

function Capture-Screen {
    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $filename = Join-Path $OutputDir "prayer_$timestamp.png"

    $screen = [System.Windows.Forms.Screen]::PrimaryScreen
    $bounds = $screen.Bounds

    $bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    $bitmap.Save($filename, [System.Drawing.Imaging.ImageFormat]::Png)

    $graphics.Dispose()
    $bitmap.Dispose()

    return $filename
}

function Send-Prayer {
    param(
        [string]$ScreenshotPath,
        [string]$Message = ""
    )

    $timestamp = Get-Date -Format "o"

    # Convert Windows path to WSL path for the screenshot
    $wslScreenshot = $ScreenshotPath -replace "C:\\", "/mnt/c/" -replace "\\", "/"

    $prayer = @{
        timestamp = $timestamp
        type = "prayer_request"
        screenshot = $wslScreenshot
        screenshot_win = $ScreenshotPath
        message = if ($Message) { $Message } else { "Le joueur invoque le chroniqueur" }
    }

    # Write signal file (daemon watches this)
    # Use UTF8NoBOM to avoid BOM that breaks JSON parsing
    $signalFile = Join-Path $SignalDir "prayer_request.json"
    $jsonContent = $prayer | ConvertTo-Json
    [System.IO.File]::WriteAllText($signalFile, $jsonContent)

    # Also append to prayers log (no BOM)
    $prayersLog = Join-Path $SignalDir "prayers.jsonl"
    $jsonLine = ($prayer | ConvertTo-Json -Compress) + "`n"
    [System.IO.File]::AppendAllText($prayersLog, $jsonLine)

    return $signalFile
}

function Play-Chime {
    [Console]::Beep(600, 100)
    [Console]::Beep(800, 100)
    [Console]::Beep(1000, 150)
}

# Key codes
$VK_F9 = 0x78
$VK_ESC = 0x1B

# Main loop
Write-Host ""
Write-Host "  ========================================" -ForegroundColor Cyan
Write-Host "     LIVING NARRATOR - PRAY HOTKEY" -ForegroundColor Cyan
Write-Host "  ========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "     F9  = Prier (capture + narration)" -ForegroundColor Yellow
Write-Host "     ESC = Quitter" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Screenshots: $OutputDir"
Write-Host "  Signal: $SignalDir"
Write-Host ""
Write-Host "  En attente de prieres..." -ForegroundColor Green
Write-Host ""

$f9WasDown = $false
$prayerCount = 0

while ($true) {
    $f9Down = [KeyState]::IsKeyDown($VK_F9)
    $escDown = [KeyState]::IsKeyDown($VK_ESC)

    if ($escDown) {
        Write-Host ""
        Write-Host "  Que Dieu vous garde." -ForegroundColor Cyan
        break
    }

    # Detect F9 press (not hold)
    if ($f9Down -and -not $f9WasDown) {
        $prayerCount++
        $time = Get-Date -Format "HH:mm:ss"

        Write-Host "  [$time] " -NoNewline -ForegroundColor DarkGray
        Write-Host "F9 " -NoNewline -ForegroundColor Yellow
        Write-Host "- Priere #$prayerCount detectee" -ForegroundColor White

        # Capture screen
        Write-Host "           Capture en cours... " -NoNewline
        $screenshot = Capture-Screen
        Write-Host "OK" -ForegroundColor Green

        # Send signal
        Write-Host "           Signal envoye... " -NoNewline
        $signal = Send-Prayer -ScreenshotPath $screenshot
        Write-Host "OK" -ForegroundColor Green

        # Audio feedback
        Play-Chime

        Write-Host "           Le chroniqueur a entendu votre appel." -ForegroundColor Cyan
        Write-Host ""
    }

    $f9WasDown = $f9Down
    Start-Sleep -Milliseconds 50
}
