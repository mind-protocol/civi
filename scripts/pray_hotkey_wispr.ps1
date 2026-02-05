# Manemus - Wispr Integration
# Flow: Wispr -> Copy from Wispr app -> F9 sends clipboard
# F8/F10/F11/F12 = change mode

param(
    [string]$OutputDir = "C:\Temp\NarratorScreenshots",
    [string]$SignalDir = "\\wsl.localhost\Ubuntu-22.04\home\mind-protocol\manemus\shrine\state"
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
        [string]$VoiceText = "",
        [string]$Mode = "partner"
    )

    $timestamp = Get-Date -Format "o"
    $wslScreenshot = $ScreenshotPath -replace "C:\\", "/mnt/c/" -replace "\\", "/"

    $prayer = @{
        timestamp = $timestamp
        hotkey = "F9"
        screenshot = $wslScreenshot
        screenshot_win = $ScreenshotPath
        voice_text = $VoiceText
        mode = $Mode
        source = "wispr"
    }

    # Append to queue file (JSONL format)
    $queueFile = Join-Path $SignalDir "message_queue.jsonl"
    $jsonLine = ($prayer | ConvertTo-Json -Compress) + "`n"
    [System.IO.File]::AppendAllText($queueFile, $jsonLine)
}

function Play-Chime {
    [Console]::Beep(600, 100)
    [Console]::Beep(800, 100)
    [Console]::Beep(1000, 150)
}

function Get-ClipboardText {
    try {
        return [System.Windows.Forms.Clipboard]::GetText()
    } catch {
        return ""
    }
}

# Key codes
$VK_F8 = 0x77
$VK_F9 = 0x78
$VK_F10 = 0x79
$VK_F11 = 0x7A
$VK_F12 = 0x7B
$VK_ESC = 0x1B

# State
$script:currentMode = "partner"
$script:invokeCount = 0
$f8Was = $false
$f9Was = $false
$f10Was = $false
$f11Was = $false
$f12Was = $false

# Colors
$ModeColors = @{
    "partner" = "Yellow"
    "witness" = "Blue"
    "rubber_duck" = "Green"
    "critic" = "Red"
    "architect" = "Magenta"
}

# Display
Clear-Host
Write-Host ""
Write-Host "  MANEMUS + WISPR" -ForegroundColor Cyan
Write-Host "  ===============" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. Ctrl+Win = parle (Wispr)" -ForegroundColor White
Write-Host "  2. Copie depuis Wispr app" -ForegroundColor White
Write-Host "  3. F9 = envoie clipboard + screenshot" -ForegroundColor Yellow
Write-Host ""
Write-Host "  F8=Architect F10=Witness F11=Duck F12=Critic" -ForegroundColor DarkGray
Write-Host "  ESC=Quit" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Mode: $($script:currentMode)" -ForegroundColor $ModeColors[$script:currentMode]
Write-Host ""

# Main loop
try {
    while ($true) {
        # ESC
        if ([KeyState]::IsKeyDown($VK_ESC)) {
            Write-Host "  Manemus." -ForegroundColor Cyan
            break
        }

        # F9 = send clipboard + screenshot
        $f9Now = [KeyState]::IsKeyDown($VK_F9)
        if ($f9Now -and -not $f9Was) {
            $script:invokeCount++
            $time = Get-Date -Format "HH:mm:ss"
            $color = $ModeColors[$script:currentMode]

            # Get clipboard
            $text = Get-ClipboardText

            Write-Host "  [$time] F9 -> $($script:currentMode)" -ForegroundColor $color

            # Capture
            $screenshot = Capture-Screen
            Write-Host "    Screenshot OK" -ForegroundColor Green

            # Send
            Send-Prayer -ScreenshotPath $screenshot -VoiceText $text -Mode $script:currentMode
            Write-Host "    Sent!" -ForegroundColor Green

            if ($text) {
                Write-Host "    Text: $text" -ForegroundColor White
            } else {
                Write-Host "    (no text)" -ForegroundColor DarkGray
            }

            Play-Chime
            Write-Host ""
        }
        $f9Was = $f9Now

        # Mode switches
        $f8Now = [KeyState]::IsKeyDown($VK_F8)
        if ($f8Now -and -not $f8Was) {
            $script:currentMode = "architect"
            Write-Host "  Mode: architect" -ForegroundColor Magenta
        }
        $f8Was = $f8Now

        $f10Now = [KeyState]::IsKeyDown($VK_F10)
        if ($f10Now -and -not $f10Was) {
            $script:currentMode = "witness"
            Write-Host "  Mode: witness" -ForegroundColor Blue
        }
        $f10Was = $f10Now

        $f11Now = [KeyState]::IsKeyDown($VK_F11)
        if ($f11Now -and -not $f11Was) {
            $script:currentMode = "rubber_duck"
            Write-Host "  Mode: rubber_duck" -ForegroundColor Green
        }
        $f11Was = $f11Now

        $f12Now = [KeyState]::IsKeyDown($VK_F12)
        if ($f12Now -and -not $f12Was) {
            $script:currentMode = "critic"
            Write-Host "  Mode: critic" -ForegroundColor Red
        }
        $f12Was = $f12Now

        Start-Sleep -Milliseconds 50
    }
} finally {
    # Cleanup
}
