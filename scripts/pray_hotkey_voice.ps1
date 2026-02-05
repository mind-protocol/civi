# Pray Hotkey with Voice Capture
# F9 to invoke the Chronicler with voice + screenshot
# Continuously records audio between prayers

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

$AudioDir = Join-Path $OutputDir "audio"
if (-not (Test-Path $AudioDir)) {
    New-Item -ItemType Directory -Path $AudioDir -Force | Out-Null
}

# Check for ffmpeg
$ffmpegPath = $null
$testPaths = @("ffmpeg", "C:\ffmpeg\bin\ffmpeg.exe", "C:\Program Files\ffmpeg\bin\ffmpeg.exe")
foreach ($path in $testPaths) {
    try {
        $null = & $path -version 2>&1
        $ffmpegPath = $path
        break
    } catch {}
}

$audioEnabled = $ffmpegPath -ne $null

# Global state
$script:ffmpegJob = $null
$script:currentAudioFile = $null
$script:recordingStartTime = $null
$script:activeMic = $null

function Get-AudioDevices {
    if (-not $ffmpegPath) { return @() }
    $output = & $ffmpegPath -list_devices true -f dshow -i dummy 2>&1 | Out-String
    $devices = @()
    $lines = $output -split "`n"
    foreach ($line in $lines) {
        if ($line -match '"([^"]+)" \(audio\)') {
            $devices += $matches[1]
        }
    }
    return $devices
}

function Start-AudioRecording {
    param([string]$MicName)

    if (-not $audioEnabled) { return $false }
    if (-not $MicName) { return $false }

    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $script:currentAudioFile = Join-Path $AudioDir "voice_$timestamp.wav"
    $script:recordingStartTime = Get-Date

    # Start ffmpeg as a background job
    $audioFile = $script:currentAudioFile
    $ffmpeg = $ffmpegPath

    $script:ffmpegJob = Start-Job -ScriptBlock {
        param($ff, $mic, $outFile)
        & $ff -y -f dshow -i "audio=$mic" -ac 1 -ar 16000 -acodec pcm_s16le $outFile 2>&1
    } -ArgumentList $ffmpeg, $MicName, $audioFile

    Start-Sleep -Milliseconds 500

    if ($script:ffmpegJob.State -eq "Running") {
        $script:activeMic = $MicName
        return $true
    }
    return $false
}

function Stop-AudioRecording {
    $savedFile = $script:currentAudioFile

    if ($script:ffmpegJob) {
        # Stop the job (this kills ffmpeg)
        Stop-Job -Job $script:ffmpegJob -ErrorAction SilentlyContinue
        Remove-Job -Job $script:ffmpegJob -Force -ErrorAction SilentlyContinue
        $script:ffmpegJob = $null
    }

    Start-Sleep -Milliseconds 300

    $script:currentAudioFile = $null

    # Check if file exists and has content
    if ($savedFile -and (Test-Path $savedFile)) {
        $fileInfo = Get-Item $savedFile
        if ($fileInfo.Length -gt 1000) {
            return $savedFile
        } else {
            Write-Host "(${fileInfo.Length} bytes) " -NoNewline -ForegroundColor DarkGray
        }
    }
    return $null
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
        [string]$AudioPath = "",
        [string]$Hotkey = "F9"
    )

    $timestamp = Get-Date -Format "o"

    # Convert Windows paths to WSL paths
    $wslScreenshot = $ScreenshotPath -replace "C:\\", "/mnt/c/" -replace "\\", "/"
    $wslAudio = ""
    if ($AudioPath) {
        $wslAudio = $AudioPath -replace "C:\\", "/mnt/c/" -replace "\\", "/"
    }

    $prayer = @{
        timestamp = $timestamp
        type = "prayer_request"
        screenshot = $wslScreenshot
        screenshot_win = $ScreenshotPath
        audio = $wslAudio
        audio_win = $AudioPath
        hotkey = $Hotkey
        mode = $HotkeyModes[$Hotkey]
        message = ""
    }

    $signalFile = Join-Path $SignalDir "prayer_request.json"
    $jsonContent = $prayer | ConvertTo-Json
    [System.IO.File]::WriteAllText($signalFile, $jsonContent)

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

# Main display
Write-Host ""
Write-Host "  ========================================" -ForegroundColor Cyan
Write-Host "         MANEMUS - VOICE + VISION" -ForegroundColor Cyan
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
Write-Host "  Audio: $AudioDir"
Write-Host ""

if (-not $audioEnabled) {
    Write-Host "  [VOICE DISABLED] ffmpeg not found" -ForegroundColor Red
    Write-Host ""
} else {
    Write-Host "  [VOICE ENABLED]" -ForegroundColor Green
    Write-Host ""

    # Detect microphones
    $mics = Get-AudioDevices
    Write-Host "  Microphones detectes:" -ForegroundColor DarkGray
    foreach ($mic in $mics) {
        Write-Host "    - $mic" -ForegroundColor White
    }
    Write-Host ""

    # Try to start recording with first available mic
    $recordingStarted = $false
    foreach ($mic in $mics) {
        Write-Host "  Tentative: $mic... " -NoNewline
        if (Start-AudioRecording -MicName $mic) {
            Write-Host "OK" -ForegroundColor Green
            $recordingStarted = $true
            break
        } else {
            Write-Host "ECHEC" -ForegroundColor Red
        }
    }

    if ($recordingStarted) {
        Write-Host ""
        Write-Host "  [RECORDING] " -NoNewline -ForegroundColor Green
        Write-Host $script:activeMic -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "  [WARNING] Aucun micro ne fonctionne" -ForegroundColor Yellow
        $audioEnabled = $false
    }
}

Write-Host ""
Write-Host "  En attente de prieres..." -ForegroundColor Green
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

# Mode colors for display
$ModeColors = @{
    "F8" = "Magenta"
    "F9" = "Yellow"
    "F10" = "Blue"
    "F11" = "Green"
    "F12" = "Red"
}

try {
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

            # Capture screen FIRST (immediate snapshot)
            Write-Host "           Capture... " -NoNewline
            $screenshot = Capture-Screen
            Write-Host "OK" -ForegroundColor Green

            # Then stop audio and get file
            $audioFile = $null
            if ($audioEnabled -and $script:activeMic) {
                Write-Host "           Audio... " -NoNewline
                $audioFile = Stop-AudioRecording
                if ($audioFile) {
                    $duration = [math]::Round(((Get-Date) - $script:recordingStartTime).TotalSeconds, 1)
                    Write-Host "OK (${duration}s)" -ForegroundColor Green
                } else {
                    Write-Host "SKIP" -ForegroundColor Yellow
                }
            }

            # Send signal with hotkey
            Write-Host "           Signal... " -NoNewline
            Send-Prayer -ScreenshotPath $screenshot -AudioPath $audioFile -Hotkey $pressedKey | Out-Null
            Write-Host "OK" -ForegroundColor Green

            Play-Chime
            Write-Host "           Mode: $mode" -ForegroundColor $color
            Write-Host ""

            # Restart recording
            if ($audioEnabled -and $script:activeMic) {
                Start-Sleep -Milliseconds 200
                Start-AudioRecording -MicName $script:activeMic | Out-Null
                Write-Host "  [RECORDING...]" -ForegroundColor DarkGray
                Write-Host ""
            }
        }

        # Update key states
        foreach ($key in $keysDown.Keys) {
            $keyStates[$key] = $keysDown[$key]
        }

        Start-Sleep -Milliseconds 50
    }
} finally {
    Stop-AudioRecording | Out-Null
    Get-Job | Stop-Job -ErrorAction SilentlyContinue
    Get-Job | Remove-Job -Force -ErrorAction SilentlyContinue
}
