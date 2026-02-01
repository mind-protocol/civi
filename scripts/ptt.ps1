# Push-to-Talk for Living Narrator (PowerShell/Windows)
# Hold a key to record, release to transcribe

param(
    [string]$HotKey = "F12",  # Key to hold for recording
    [string]$TranscriptFile = "\\wsl.localhost\Ubuntu-22.04\home\mind-protocol\civi\narrator\state\voice_transcript.jsonl",
    [string]$AudioDir = "C:\Temp\NarratorAudio",
    [string]$OpenAIKey = $env:OPENAI_API_KEY
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName PresentationCore

# Ensure directories exist
if (-not (Test-Path $AudioDir)) {
    New-Item -ItemType Directory -Path $AudioDir -Force | Out-Null
}

# Check for OpenAI key
if (-not $OpenAIKey) {
    # Try to read from .env
    $envFile = "\\wsl.localhost\Ubuntu-22.04\home\mind-protocol\civi\.env"
    if (Test-Path $envFile) {
        Get-Content $envFile | ForEach-Object {
            if ($_ -match "^OPENAI_API_KEY=(.+)$") {
                $OpenAIKey = $matches[1].Trim('"').Trim("'")
            }
        }
    }
}

if (-not $OpenAIKey) {
    Write-Host "⚠️  OPENAI_API_KEY not found - transcription won't work" -ForegroundColor Yellow
    Write-Host "   Set it in environment or .env file"
}

# MCI functions for audio recording
Add-Type @"
using System;
using System.IO;
using System.Text;
using System.Runtime.InteropServices;
using System.Threading;

public class AudioRecorder {
    [DllImport("winmm.dll", EntryPoint = "mciSendStringA", CharSet = CharSet.Ansi)]
    private static extern int mciSendString(string command, StringBuilder buffer, int bufferSize, IntPtr callback);

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

    public static bool IsRecording() {
        return isRecording;
    }
}
"@

# Keyboard hook for detecting key state
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

function Get-VirtualKeyCode {
    param([string]$KeyName)

    $keyCodes = @{
        "F1" = 0x70; "F2" = 0x71; "F3" = 0x72; "F4" = 0x73
        "F5" = 0x74; "F6" = 0x75; "F7" = 0x76; "F8" = 0x77
        "F9" = 0x78; "F10" = 0x79; "F11" = 0x7A; "F12" = 0x7B
        "Insert" = 0x2D; "Delete" = 0x2E
        "Home" = 0x24; "End" = 0x23
        "PageUp" = 0x21; "PageDown" = 0x22
        "CapsLock" = 0x14; "ScrollLock" = 0x91
        "Pause" = 0x13
    }

    if ($keyCodes.ContainsKey($KeyName)) {
        return $keyCodes[$KeyName]
    }
    return 0x7B  # Default to F12
}

function Transcribe-Audio {
    param([string]$AudioPath)

    if (-not $OpenAIKey) { return $null }
    if (-not (Test-Path $AudioPath)) { return $null }

    $fileSize = (Get-Item $AudioPath).Length
    if ($fileSize -lt 10000) {
        # Too small, probably silence
        return $null
    }

    try {
        $uri = "https://api.openai.com/v1/audio/transcriptions"

        # Build multipart form data
        $boundary = [System.Guid]::NewGuid().ToString()
        $LF = "`r`n"

        $audioBytes = [System.IO.File]::ReadAllBytes($AudioPath)
        $audioBase64 = [Convert]::ToBase64String($audioBytes)

        # Use Invoke-RestMethod with file upload
        $headers = @{
            "Authorization" = "Bearer $OpenAIKey"
        }

        # Create form data
        $form = @{
            file = Get-Item -Path $AudioPath
            model = "whisper-1"
            language = "fr"
        }

        $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Form $form -TimeoutSec 30

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

function Save-Transcript {
    param([string]$Text, [string]$Speaker = "player")

    $entry = @{
        ts = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fff")
        speaker = $Speaker
        text = $Text
        type = "ptt"
    } | ConvertTo-Json -Compress

    Add-Content -Path $TranscriptFile -Value $entry -Encoding UTF8
}

# Main PTT loop
$vkCode = Get-VirtualKeyCode $HotKey
$keyEnum = [System.Windows.Forms.Keys]$vkCode

Write-Host "🎤 Push-to-Talk started"
Write-Host "   Hotkey: $HotKey (hold to record)"
Write-Host "   Transcripts: $TranscriptFile"
Write-Host "   Audio dir: $AudioDir"
Write-Host ""
Write-Host "Press and HOLD $HotKey to record, release to transcribe"
Write-Host "Press Ctrl+C to stop"
Write-Host ""

$wasPressed = $false
$recordingStartTime = $null

while ($true) {
    $isPressed = [KeyboardState]::IsKeyDown($keyEnum)

    if ($isPressed -and -not $wasPressed) {
        # Key just pressed - start recording
        $timestamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
        $audioFile = Join-Path $AudioDir "ptt_$timestamp.wav"

        Write-Host "🔴 Recording... " -NoNewline -ForegroundColor Red
        [AudioRecorder]::StartRecording($audioFile) | Out-Null
        $recordingStartTime = Get-Date
    }
    elseif (-not $isPressed -and $wasPressed) {
        # Key just released - stop recording and transcribe
        $duration = ((Get-Date) - $recordingStartTime).TotalSeconds

        if ([AudioRecorder]::StopRecording()) {
            Write-Host "stopped ($([math]::Round($duration, 1))s)" -ForegroundColor Green

            if ($duration -ge 0.5) {
                Write-Host "📝 Transcribing... " -NoNewline
                $text = Transcribe-Audio $audioFile

                if ($text) {
                    Write-Host "✓" -ForegroundColor Green
                    Write-Host "   ""$text""" -ForegroundColor Cyan
                    Save-Transcript $text "player"
                }
                else {
                    Write-Host "(silence or error)" -ForegroundColor DarkGray
                }
            }
            else {
                Write-Host "   (too short, skipped)" -ForegroundColor DarkGray
            }

            # Cleanup audio file
            Remove-Item $audioFile -Force -ErrorAction SilentlyContinue
        }
        else {
            Write-Host "failed" -ForegroundColor Red
        }

        Write-Host ""
    }

    $wasPressed = $isPressed
    Start-Sleep -Milliseconds 50
}
