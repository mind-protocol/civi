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
        [string]$Message = "",
        [string]$Hotkey = "F9"
    )

    $timestamp = Get-Date -Format "o"

    # Convert Windows path to WSL path for the screenshot
    $wslScreenshot = $ScreenshotPath -replace "C:\\", "/mnt/c/" -replace "\\", "/"

    $prayer = @{
        timestamp = $timestamp
        type = "prayer_request"
        screenshot = $wslScreenshot
        screenshot_win = $ScreenshotPath
        hotkey = $Hotkey
        mode = $HotkeyModes[$Hotkey]
        message = if ($Message) { $Message } else { "" }
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

# Key codes - Mode hotkeys
$VK_F8 = 0x77   # Architect
$VK_F9 = 0x78   # Partner (default)
$VK_F10 = 0x79  # Witness
$VK_F11 = 0x7A  # Rubber Duck
$VK_F12 = 0x7B  # Critic
$VK_ESC = 0x1B

# Hotkey to mode mapping
$HotkeyModes = @{
    "F8" = "architect"
    "F9" = "partner"
    "F10" = "witness"
    "F11" = "rubber_duck"
    "F12" = "critic"
}

# Mode colors for display
$ModeColors = @{
    "F8" = "Magenta"
    "F9" = "Yellow"
    "F10" = "Blue"
    "F11" = "Green"
    "F12" = "Red"
}

# Main loop
Write-Host ""
Write-Host "  ========================================" -ForegroundColor Cyan
Write-Host "         MANEMUS - PRAY HOTKEY" -ForegroundColor Cyan
Write-Host "  ========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "     F8  = Architect (zoom out)" -ForegroundColor Magenta
Write-Host "     F9  = Partner (default)" -ForegroundColor Yellow
Write-Host "     F10 = Witness (presence)" -ForegroundColor Blue
Write-Host "     F11 = Rubber Duck (listen)" -ForegroundColor Green
Write-Host "     F12 = Critic (stress-test)" -ForegroundColor Red
Write-Host ""
Write-Host "     ESC = Quitter" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Screenshots: $OutputDir"
Write-Host "  Signal: $SignalDir"
Write-Host ""
Write-Host "  En attente..." -ForegroundColor Green
Write-Host ""

# Track key states
$keyStates = @{
    "F8" = $false
    "F9" = $false
    "F10" = $false
    "F11" = $false
    "F12" = $false
}
$prayerCount = 0

while ($true) {
    $escDown = [KeyState]::IsKeyDown($VK_ESC)

    if ($escDown) {
        Write-Host ""
        Write-Host "  Manemus." -ForegroundColor Cyan
        break
    }

    # Check all mode hotkeys
    $keysDown = @{
        "F8" = [KeyState]::IsKeyDown($VK_F8)
        "F9" = [KeyState]::IsKeyDown($VK_F9)
        "F10" = [KeyState]::IsKeyDown($VK_F10)
        "F11" = [KeyState]::IsKeyDown($VK_F11)
        "F12" = [KeyState]::IsKeyDown($VK_F12)
    }

    # Detect any new key press
    $pressedKey = $null
    foreach ($key in $keysDown.Keys) {
        if ($keysDown[$key] -and -not $keyStates[$key]) {
            $pressedKey = $key
            break
        }
    }

    if ($pressedKey) {
        $prayerCount++
        $time = Get-Date -Format "HH:mm:ss"
        $mode = $HotkeyModes[$pressedKey]
        $color = $ModeColors[$pressedKey]

        Write-Host "  [$time] " -NoNewline -ForegroundColor DarkGray
        Write-Host "$pressedKey " -NoNewline -ForegroundColor $color
        Write-Host "- $mode #$prayerCount" -ForegroundColor White

        # Capture screen
        Write-Host "           Capture... " -NoNewline
        $screenshot = Capture-Screen
        Write-Host "OK" -ForegroundColor Green

        # Send signal with hotkey
        Write-Host "           Signal... " -NoNewline
        Send-Prayer -ScreenshotPath $screenshot -Hotkey $pressedKey | Out-Null
        Write-Host "OK" -ForegroundColor Green

        Play-Chime
        Write-Host "           Mode: $mode" -ForegroundColor $color
        Write-Host ""
    }

    # Update key states
    foreach ($key in $keysDown.Keys) {
        $keyStates[$key] = $keysDown[$key]
    }

    Start-Sleep -Milliseconds 50
}
