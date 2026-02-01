# Living Narrator - Unified Capture Launcher
# Consolidates: screenshots, click watcher, push-to-talk
# Usage: .\narrator_capture.ps1 [-NoScreenshots] [-NoClicks] [-NoPTT]

param(
    [switch]$NoScreenshots,
    [switch]$NoClicks,
    [switch]$NoPTT,
    [string]$PTTKey = "F12",
    [double]$ScreenshotInterval = 30,
    [double]$ClickCooldown = 0.5,
    [string]$WSLPath = "\\wsl.localhost\Ubuntu-22.04\home\mind-protocol\civi"
)

# ============================================================
# CONFIGURATION
# ============================================================

$Config = @{
    Screenshots = @{
        Enabled = -not $NoScreenshots
        Interval = $ScreenshotInterval
        OutputDir = "C:\Temp\NarratorScreenshots"
        LastCapture = [DateTime]::MinValue
    }
    Clicks = @{
        Enabled = -not $NoClicks
        Cooldown = $ClickCooldown
        OutputDir = "C:\Temp\NarratorScreenshots\clicks"
        DecisionsFile = "$WSLPath\narrator\state\decisions.jsonl"
        LastClick = [DateTime]::MinValue
        LastState = [System.Windows.Forms.MouseButtons]::None
    }
    PTT = @{
        Enabled = -not $NoPTT
        HotKey = $PTTKey
        AudioDir = "C:\Temp\NarratorAudio"
        TranscriptFile = "$WSLPath\narrator\state\voice_transcript.jsonl"
        IsRecording = $false
        RecordingStart = $null
    }
}

# ============================================================
# DEPENDENCIES
# ============================================================

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Audio recording via MCI
Add-Type @"
using System;
using System.IO;
using System.Runtime.InteropServices;

public class AudioRecorder {
    [DllImport("winmm.dll", EntryPoint = "mciSendStringA", CharSet = CharSet.Ansi)]
    private static extern int mciSendString(string command, System.Text.StringBuilder buffer, int bufferSize, IntPtr callback);

    private static bool isRecording = false;
    private static string currentFile = "";

    public static bool StartRecording(string filename) {
        if (isRecording) return false;
        currentFile = filename;
        mciSendString("open new Type waveaudio Alias pttrecord", null, 0, IntPtr.Zero);
        int result = mciSendString("record pttrecord", null, 0, IntPtr.Zero);
        isRecording = (result == 0);
        return isRecording;
    }

    public static bool StopRecording() {
        if (!isRecording) return false;
        mciSendString("stop pttrecord", null, 0, IntPtr.Zero);
        mciSendString("save pttrecord " + currentFile, null, 0, IntPtr.Zero);
        mciSendString("close pttrecord", null, 0, IntPtr.Zero);
        isRecording = false;
        return File.Exists(currentFile);
    }

    public static bool IsRecording() { return isRecording; }
}
"@

# Keyboard state detection
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;

public class KeyboardState {
    [DllImport("user32.dll")]
    private static extern short GetAsyncKeyState(int vKey);

    public static bool IsKeyDown(Keys key) {
        return (GetAsyncKeyState((int)key) & 0x8000) != 0;
    }
}
"@

# ============================================================
# HELPER FUNCTIONS
# ============================================================

$VKeyCodes = @{
    "F1" = 0x70; "F2" = 0x71; "F3" = 0x72; "F4" = 0x73
    "F5" = 0x74; "F6" = 0x75; "F7" = 0x76; "F8" = 0x77
    "F9" = 0x78; "F10" = 0x79; "F11" = 0x7A; "F12" = 0x7B
    "Insert" = 0x2D; "Delete" = 0x2E; "Home" = 0x24; "End" = 0x23
    "PageUp" = 0x21; "PageDown" = 0x22; "CapsLock" = 0x14
    "ScrollLock" = 0x91; "Pause" = 0x13
}

# Decision zones for click filtering (CK3)
$DecisionZones = @(
    @{ Name="event_popup"; X1=0.20; Y1=0.10; X2=0.80; Y2=0.85 }
    @{ Name="character_panel"; X1=0.0; Y1=0.15; X2=0.25; Y2=0.85 }
)

$IgnoreZones = @(
    @{ Name="top_bar"; X1=0.0; Y1=0.0; X2=1.0; Y2=0.05 }
    @{ Name="bottom_bar"; X1=0.0; Y1=0.95; X2=1.0; Y2=1.0 }
    @{ Name="minimap"; X1=0.85; Y1=0.0; X2=1.0; Y2=0.25 }
    @{ Name="close_buttons"; X1=0.75; Y1=0.0; X2=0.85; Y2=0.10 }
)

function Test-InZone($X, $Y, $Width, $Height, $Zone) {
    $nx = $X / $Width
    $ny = $Y / $Height
    return ($nx -ge $Zone.X1 -and $nx -le $Zone.X2 -and $ny -ge $Zone.Y1 -and $ny -le $Zone.Y2)
}

function Test-IsDecisionClick($X, $Y, $Width, $Height) {
    foreach ($zone in $IgnoreZones) {
        if (Test-InZone $X $Y $Width $Height $zone) {
            return @{ IsDecision=$false; Reason="ignore:$($zone.Name)" }
        }
    }
    foreach ($zone in $DecisionZones) {
        if (Test-InZone $X $Y $Width $Height $zone) {
            return @{ IsDecision=$true; Zone=$zone.Name }
        }
    }
    return @{ IsDecision=$false; Reason="outside_zones" }
}

function Get-OpenAIKey {
    $key = $env:OPENAI_API_KEY
    if (-not $key) {
        $envFile = "$WSLPath\.env"
        if (Test-Path $envFile) {
            Get-Content $envFile | ForEach-Object {
                if ($_ -match "^OPENAI_API_KEY=(.+)$") {
                    $key = $matches[1].Trim('"').Trim("'")
                }
            }
        }
    }
    return $key
}

function Transcribe-Audio($AudioPath) {
    $key = Get-OpenAIKey
    if (-not $key) { return $null }
    if (-not (Test-Path $AudioPath)) { return $null }

    $fileSize = (Get-Item $AudioPath).Length
    if ($fileSize -lt 10000) { return $null }  # Too small

    try {
        $headers = @{ "Authorization" = "Bearer $key" }
        $form = @{
            file = Get-Item -Path $AudioPath
            model = "whisper-1"
            language = "fr"
        }
        $response = Invoke-RestMethod -Uri "https://api.openai.com/v1/audio/transcriptions" `
            -Method Post -Headers $headers -Form $form -TimeoutSec 30

        $text = $response.text
        if ($text -and $text.Length -gt 3) {
            return $text.Trim()
        }
    }
    catch {
        Write-Host "  Transcription error: $_" -ForegroundColor Red
    }
    return $null
}

# ============================================================
# CAPTURE FUNCTIONS
# ============================================================

function Capture-Screenshot {
    $now = Get-Date
    $elapsed = ($now - $script:Config.Screenshots.LastCapture).TotalSeconds
    if ($elapsed -lt $script:Config.Screenshots.Interval) { return }

    $screen = [System.Windows.Forms.Screen]::PrimaryScreen
    $bounds = $screen.Bounds

    $timestamp = $now.ToString("yyyy-MM-dd_HH-mm-ss")
    $filename = "screen_$timestamp.png"
    $filepath = Join-Path $script:Config.Screenshots.OutputDir $filename

    try {
        $bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
        $bitmap.Save($filepath)
        $graphics.Dispose()
        $bitmap.Dispose()

        $script:Config.Screenshots.LastCapture = $now
        Write-Host "[$($now.ToString('HH:mm:ss'))] " -NoNewline
        Write-Host "Screenshot" -ForegroundColor Blue -NoNewline
        Write-Host " -> $filename"
    }
    catch {
        Write-Host "Screenshot error: $_" -ForegroundColor Red
    }
}

function Capture-Click($X, $Y) {
    $now = Get-Date
    $elapsed = ($now - $script:Config.Clicks.LastClick).TotalSeconds
    if ($elapsed -lt $script:Config.Clicks.Cooldown) { return }

    $screen = [System.Windows.Forms.Screen]::PrimaryScreen
    $width = $screen.Bounds.Width
    $height = $screen.Bounds.Height

    $result = Test-IsDecisionClick $X $Y $width $height
    if (-not $result.IsDecision) {
        Write-Host "[$($now.ToString('HH:mm:ss'))] Skip click ($X,$Y) - $($result.Reason)" -ForegroundColor DarkGray
        return
    }

    $script:Config.Clicks.LastClick = $now
    $zone = $result.Zone

    $timestamp = $now.ToString("yyyy-MM-dd_HH-mm-ss-fff")
    $filename = "click_${timestamp}_${X}_${Y}.png"
    $filepath = Join-Path $script:Config.Clicks.OutputDir $filename

    try {
        $bitmap = New-Object System.Drawing.Bitmap($width, $height)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen($screen.Bounds.Location, [System.Drawing.Point]::Empty, $screen.Bounds.Size)
        $bitmap.Save($filepath)
        $graphics.Dispose()
        $bitmap.Dispose()

        $decision = @{
            timestamp = $now.ToString("yyyy-MM-ddTHH:mm:ss.fff")
            x = $X; y = $Y
            screen_width = $width; screen_height = $height
            screenshot_path = $filepath
            zone = $zone
            ocr_text = ""; region_ocr = ""
        }

        $json = $decision | ConvertTo-Json -Compress
        Add-Content -Path $script:Config.Clicks.DecisionsFile -Value $json -Encoding UTF8

        Write-Host "[$($now.ToString('HH:mm:ss'))] " -NoNewline
        Write-Host "Decision" -ForegroundColor Green -NoNewline
        Write-Host " ($X,$Y) [$zone]"
    }
    catch {
        Write-Host "Click capture error: $_" -ForegroundColor Red
    }
}

function Handle-PTT {
    $vkCode = if ($VKeyCodes.ContainsKey($script:Config.PTT.HotKey)) {
        $VKeyCodes[$script:Config.PTT.HotKey]
    } else { 0x7B }

    $keyEnum = [System.Windows.Forms.Keys]$vkCode
    $isPressed = [KeyboardState]::IsKeyDown($keyEnum)

    if ($isPressed -and -not $script:Config.PTT.IsRecording) {
        # Start recording
        $timestamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
        $script:currentAudioFile = Join-Path $script:Config.PTT.AudioDir "ptt_$timestamp.wav"

        Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] " -NoNewline
        Write-Host "Recording..." -ForegroundColor Red -NoNewline

        [AudioRecorder]::StartRecording($script:currentAudioFile) | Out-Null
        $script:Config.PTT.IsRecording = $true
        $script:Config.PTT.RecordingStart = Get-Date
    }
    elseif (-not $isPressed -and $script:Config.PTT.IsRecording) {
        # Stop recording
        $duration = ((Get-Date) - $script:Config.PTT.RecordingStart).TotalSeconds

        if ([AudioRecorder]::StopRecording()) {
            Write-Host " stopped ($([math]::Round($duration, 1))s)" -ForegroundColor Green

            if ($duration -ge 0.5) {
                Write-Host "  Transcribing... " -NoNewline
                $text = Transcribe-Audio $script:currentAudioFile

                if ($text) {
                    Write-Host "OK" -ForegroundColor Green
                    Write-Host "  ""$text""" -ForegroundColor Cyan

                    # Save transcript
                    $entry = @{
                        ts = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fff")
                        speaker = "player"
                        text = $text
                        type = "ptt"
                    } | ConvertTo-Json -Compress

                    Add-Content -Path $script:Config.PTT.TranscriptFile -Value $entry -Encoding UTF8
                }
                else {
                    Write-Host "(silence)" -ForegroundColor DarkGray
                }
            }
            else {
                Write-Host "  (too short)" -ForegroundColor DarkGray
            }

            Remove-Item $script:currentAudioFile -Force -ErrorAction SilentlyContinue
        }
        else {
            Write-Host " failed" -ForegroundColor Red
        }

        $script:Config.PTT.IsRecording = $false
    }
}

# ============================================================
# MAIN LOOP
# ============================================================

# Create directories
@($Config.Screenshots.OutputDir, $Config.Clicks.OutputDir, $Config.PTT.AudioDir) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }
}

# Display startup info
Write-Host ""
Write-Host "=== Living Narrator Capture ===" -ForegroundColor Cyan
Write-Host ""

$enabledCount = 0

if ($Config.Screenshots.Enabled) {
    Write-Host "[ON]  " -ForegroundColor Green -NoNewline
    Write-Host "Screenshots" -NoNewline
    Write-Host " (every $($Config.Screenshots.Interval)s)" -ForegroundColor DarkGray
    $enabledCount++
} else {
    Write-Host "[OFF] " -ForegroundColor Red -NoNewline
    Write-Host "Screenshots"
}

if ($Config.Clicks.Enabled) {
    Write-Host "[ON]  " -ForegroundColor Green -NoNewline
    Write-Host "Click Watcher" -NoNewline
    Write-Host " (decisions only)" -ForegroundColor DarkGray
    $enabledCount++
} else {
    Write-Host "[OFF] " -ForegroundColor Red -NoNewline
    Write-Host "Click Watcher"
}

if ($Config.PTT.Enabled) {
    $keyStatus = if (Get-OpenAIKey) { "ready" } else { "NO API KEY" }
    $keyColor = if (Get-OpenAIKey) { "DarkGray" } else { "Yellow" }
    Write-Host "[ON]  " -ForegroundColor Green -NoNewline
    Write-Host "Push-to-Talk" -NoNewline
    Write-Host " ($($Config.PTT.HotKey) = record, $keyStatus)" -ForegroundColor $keyColor
    $enabledCount++
} else {
    Write-Host "[OFF] " -ForegroundColor Red -NoNewline
    Write-Host "Push-to-Talk"
}

Write-Host ""

if ($enabledCount -eq 0) {
    Write-Host "Nothing enabled! Use without -No* flags." -ForegroundColor Yellow
    exit 1
}

Write-Host "Press Ctrl+C to stop" -ForegroundColor DarkGray
Write-Host ""

# Main loop
while ($true) {
    # Screenshots (timed)
    if ($Config.Screenshots.Enabled) {
        Capture-Screenshot
    }

    # Click detection (polling)
    if ($Config.Clicks.Enabled) {
        $currentState = [System.Windows.Forms.Control]::MouseButtons
        if ($currentState -eq [System.Windows.Forms.MouseButtons]::Left -and
            $Config.Clicks.LastState -eq [System.Windows.Forms.MouseButtons]::None) {
            $point = [System.Windows.Forms.Cursor]::Position
            Capture-Click -X $point.X -Y $point.Y
        }
        $Config.Clicks.LastState = $currentState
    }

    # PTT (key state)
    if ($Config.PTT.Enabled) {
        Handle-PTT
    }

    Start-Sleep -Milliseconds 50
}
