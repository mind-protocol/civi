#!/usr/bin/env python3
"""
Voice capture for Living Narrator.
Records audio from microphone, detects speech, and transcribes.
Runs on Windows via PowerShell for mic access.
"""

import subprocess
import sys
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

import requests
from dotenv import load_dotenv

# Load .env
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Config
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
AUDIO_DIR = Path("/mnt/c/Temp/NarratorAudio")
TRANSCRIPT_FILE = PROJECT_ROOT / "narrator" / "state" / "voice_transcript.jsonl"

# Recording settings
SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 10  # Record in chunks
SILENCE_THRESHOLD = 0.02  # RMS threshold for silence detection
MIN_SPEECH_DURATION = 0.5  # Minimum seconds of speech to keep


def record_audio_windows(output_path: str, duration: int = 10) -> bool:
    """Record audio using PowerShell on Windows."""

    ps_script = f'''
Add-Type -AssemblyName System.Speech
Add-Type @"
using System;
using System.IO;
using System.Runtime.InteropServices;

public class AudioRecorder {{
    [DllImport("winmm.dll")]
    public static extern int waveInGetNumDevs();

    public static bool HasMicrophone() {{
        return waveInGetNumDevs() > 0;
    }}
}}
"@

# Check for microphone
if (-not [AudioRecorder]::HasMicrophone()) {{
    Write-Error "No microphone found"
    exit 1
}}

# Use ffmpeg for recording (more reliable)
$duration = {duration}
$output = "{output_path}"

# Record using ffmpeg with default audio device
& ffmpeg -y -f dshow -i audio="Microphone Array (Realtek(R) Audio)" -t $duration -ar 16000 -ac 1 $output 2>$null

if (Test-Path $output) {{
    Write-Host "OK"
}} else {{
    Write-Error "Recording failed"
    exit 1
}}
'''

    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=duration + 10
        )
        return result.returncode == 0 and "OK" in result.stdout
    except Exception as e:
        print(f"Recording error: {e}", file=sys.stderr)
        return False


def record_audio_powershell(output_path: Path, duration: int = 10) -> bool:
    """Record audio using PowerShell with NAudio or Windows built-in."""

    # Convert to Windows path
    win_path = str(output_path).replace("/mnt/c", "C:").replace("/", "\\")

    # PowerShell script using Windows Voice Recorder approach
    ps_script = f'''
$ErrorActionPreference = "Stop"

# Create output directory if needed
$dir = Split-Path "{win_path}" -Parent
if (-not (Test-Path $dir)) {{ New-Item -ItemType Directory -Path $dir -Force | Out-Null }}

# Use SoundRecorder via command line (Windows built-in)
# Alternative: Use .NET SpeechRecognitionEngine for audio capture
Add-Type -AssemblyName System.Speech

try {{
    # Create a simple audio recorder using .NET
    Add-Type @"
using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading;

public class SimpleRecorder {{
    [DllImport("winmm.dll", EntryPoint = "mciSendStringA", CharSet = CharSet.Ansi)]
    private static extern int mciSendString(string command, System.Text.StringBuilder buffer, int bufferSize, IntPtr callback);

    public static bool Record(string filename, int durationMs) {{
        try {{
            mciSendString("open new Type waveaudio Alias recsound", null, 0, IntPtr.Zero);
            mciSendString("record recsound", null, 0, IntPtr.Zero);
            Thread.Sleep(durationMs);
            mciSendString("save recsound " + filename, null, 0, IntPtr.Zero);
            mciSendString("close recsound", null, 0, IntPtr.Zero);
            return File.Exists(filename);
        }} catch {{
            return false;
        }}
    }}
}}
"@

    $result = [SimpleRecorder]::Record("{win_path}", {duration * 1000})
    if ($result) {{ Write-Host "OK" }} else {{ Write-Host "FAIL" }}
}} catch {{
    Write-Host "ERROR: $_"
}}
'''

    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=duration + 15,
            errors='replace'  # Handle encoding issues
        )

        success = "OK" in result.stdout and output_path.exists()
        if not success and result.stderr:
            print(f"PowerShell stderr: {result.stderr[:200]}", file=sys.stderr)
        return success

    except subprocess.TimeoutExpired:
        print("Recording timed out", file=sys.stderr)
        return False
    except Exception as e:
        print(f"PowerShell recording error: {e}", file=sys.stderr)
        return False


def record_audio_ffmpeg(output_path: Path, duration: int = 10) -> bool:
    """Record audio using ffmpeg if available."""
    # Try PowerShell method first (more reliable)
    return record_audio_powershell(output_path, duration)


def transcribe_audio(audio_path: Path) -> Optional[str]:
    """Transcribe audio using OpenAI Whisper API."""

    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY not set", file=sys.stderr)
        return None

    if not audio_path.exists():
        return None

    # Check file size (skip if too small = silence)
    if audio_path.stat().st_size < 10000:  # Less than 10KB probably silence
        return None

    try:
        with open(audio_path, "rb") as f:
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                files={"file": (audio_path.name, f, "audio/wav")},
                data={
                    "model": "whisper-1",
                    "language": "fr",
                    "response_format": "json"
                },
                timeout=30
            )

        if response.status_code == 200:
            result = response.json()
            text = result.get("text", "").strip()
            # Filter out empty or very short transcriptions
            if len(text) > 3:
                return text
        else:
            print(f"Whisper API error: {response.status_code} - {response.text[:200]}", file=sys.stderr)

    except Exception as e:
        print(f"Transcription error: {e}", file=sys.stderr)

    return None


def save_transcript(text: str, speaker: str = "unknown"):
    """Save transcript to JSONL file."""
    TRANSCRIPT_FILE.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "ts": datetime.now().isoformat(),
        "speaker": speaker,
        "text": text
    }

    with open(TRANSCRIPT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"[{speaker}] {text}")


def get_recent_transcripts(max_age_seconds: int = 300, limit: int = 20) -> list[dict]:
    """Get recent voice transcripts."""
    if not TRANSCRIPT_FILE.exists():
        return []

    transcripts = []
    cutoff = datetime.now().timestamp() - max_age_seconds

    try:
        with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_ts = datetime.fromisoformat(entry["ts"]).timestamp()
                    if entry_ts > cutoff:
                        transcripts.append(entry)
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue
    except Exception:
        pass

    return transcripts[-limit:]


def listen_loop(duration: int = 10, continuous: bool = True):
    """Main listening loop."""
    print("🎤 Voice capture started")
    print(f"   Recording chunks of {duration}s")
    print(f"   Transcripts: {TRANSCRIPT_FILE}")
    print("   Press Ctrl+C to stop")
    print()

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    while True:
        try:
            # Generate temp filename
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_file = AUDIO_DIR / f"voice_{ts}.wav"

            # Record
            print(f"🔴 Recording...", end=" ", flush=True)
            success = record_audio_ffmpeg(audio_file, duration)

            if not success:
                print("❌ Recording failed")
                if not continuous:
                    break
                continue

            print(f"✓", end=" ", flush=True)

            # Transcribe
            print(f"📝 Transcribing...", end=" ", flush=True)
            text = transcribe_audio(audio_file)

            if text:
                print(f"✓")
                save_transcript(text, speaker="player")
            else:
                print("(silence)")

            # Cleanup audio file
            try:
                audio_file.unlink()
            except:
                pass

            if not continuous:
                break

        except KeyboardInterrupt:
            print("\n👋 Stopped")
            break


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Voice capture for Living Narrator")
    parser.add_argument("--once", action="store_true", help="Record once and exit")
    parser.add_argument("--duration", type=int, default=10, help="Recording duration in seconds")
    parser.add_argument("--recent", action="store_true", help="Show recent transcripts")
    parser.add_argument("--test-mic", action="store_true", help="Test microphone access")

    args = parser.parse_args()

    if args.recent:
        transcripts = get_recent_transcripts()
        if transcripts:
            for t in transcripts:
                print(f"[{t['ts'][:19]}] {t.get('speaker', '?')}: {t['text']}")
        else:
            print("No recent transcripts")
        return

    if args.test_mic:
        print("Testing microphone access...")
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        test_file = AUDIO_DIR / "test_mic.wav"
        if record_audio_ffmpeg(test_file, 3):
            print(f"✓ Microphone working! Test file: {test_file}")
            size = test_file.stat().st_size
            print(f"  File size: {size} bytes")
        else:
            print("❌ Microphone test failed")
        return

    # Check API key
    if not OPENAI_API_KEY:
        print("⚠️  OPENAI_API_KEY not set - transcription won't work")
        print("   Add it to .env file")

    listen_loop(duration=args.duration, continuous=not args.once)


if __name__ == "__main__":
    main()
