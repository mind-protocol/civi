#!/usr/bin/env python3
"""
TTS wrapper for Living Narrator.
Uses Eleven Labs API to generate French speech and plays it.
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load .env from project root
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Config from environment
ELEVEN_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "")
MODEL_ID = "eleven_multilingual_v2"

# Audio cache directory
AUDIO_CACHE = PROJECT_ROOT / "audio"


def speak(text: str, cache: bool = False) -> bool:
    """
    Convert text to speech and play it.

    Args:
        text: French text to speak
        cache: If True, cache the audio file

    Returns:
        True if successful, False otherwise
    """
    if not ELEVEN_API_KEY:
        print("❌ ELEVENLABS_API_KEY not set in .env")
        return False

    if not VOICE_ID:
        print("❌ ELEVENLABS_VOICE_ID not set in .env")
        print("   Find French voices at: https://elevenlabs.io/voice-library")
        print("   Or create custom at: https://elevenlabs.io/voice-design")
        return False

    if not text.strip():
        print("⚠️  Empty text, nothing to speak")
        return False

    print(f"🎙️  Speaking: {text[:60]}..." if len(text) > 60 else f"🎙️  Speaking: {text}")

    # Call Eleven Labs API
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ API error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text[:200]}")
        return False

    # Save audio
    if cache:
        AUDIO_CACHE.mkdir(parents=True, exist_ok=True)
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
        audio_path = AUDIO_CACHE / f"{text_hash}.mp3"
        audio_path.write_bytes(response.content)
    else:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(response.content)
            audio_path = Path(f.name)

    # Play audio
    success = play_audio(audio_path)

    # Cleanup temp file
    if not cache and audio_path.exists():
        try:
            audio_path.unlink()
        except Exception:
            pass

    return success


def play_audio(path: Path) -> bool:
    """
    Play an audio file.
    Tries multiple methods for cross-platform support.
    """
    path_str = str(path)

    # Convert to Windows path if needed (for WSL playing on Windows)
    if path_str.startswith("/tmp"):
        # For temp files, copy to a location accessible from Windows
        win_tmp = Path("/mnt/c/Temp")
        if win_tmp.exists():
            win_path = win_tmp / path.name
            win_path.write_bytes(path.read_bytes())
            path_str = f"C:\\Temp\\{path.name}"
            path = win_path

    players = [
        # Windows via PowerShell (for WSL)
        ["powershell.exe", "-c", f"Add-Type -AssemblyName PresentationCore; $player = New-Object System.Windows.Media.MediaPlayer; $player.Open('{path_str}'); $player.Play(); Start-Sleep -Seconds 10; $player.Close()"],
        # Alternative Windows player
        ["powershell.exe", "-c", f"(New-Object Media.SoundPlayer '{path_str}').PlaySync()"],
        # Linux with ffplay
        ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", str(path)],
        # Linux with mpv
        ["mpv", "--no-video", "--really-quiet", str(path)],
        # Mac
        ["afplay", str(path)],
    ]

    for player_cmd in players:
        try:
            result = subprocess.run(
                player_cmd,
                capture_output=True,
                timeout=60
            )
            if result.returncode == 0:
                print("🔊 Audio played")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue

    print("⚠️  Could not play audio - no suitable player found")
    print(f"   Audio saved at: {path}")
    return False


def list_voices():
    """List available voices from Eleven Labs."""
    if not ELEVEN_API_KEY:
        print("❌ ELEVENLABS_API_KEY not set")
        return

    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": ELEVEN_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        voices = response.json().get("voices", [])

        print(f"\n📢 Available voices ({len(voices)}):\n")
        for v in voices:
            labels = v.get("labels", {})
            lang = labels.get("language", "?")
            accent = labels.get("accent", "")
            gender = labels.get("gender", "")
            age = labels.get("age", "")

            print(f"  {v['voice_id'][:12]}...  {v['name']:<20} [{lang}] {gender} {age} {accent}")

        print(f"\n💡 Set ELEVENLABS_VOICE_ID in .env with your chosen voice ID")

    except Exception as e:
        print(f"❌ Error listing voices: {e}")


def main():
    if len(sys.argv) < 2:
        print("Living Narrator TTS")
        print()
        print("Usage:")
        print("  python speak.py 'Text to speak in French'")
        print("  python speak.py --list-voices")
        print()
        print("Config (.env):")
        print(f"  ELEVENLABS_API_KEY: {'✓ Set' if ELEVEN_API_KEY else '✗ Missing'}")
        print(f"  ELEVENLABS_VOICE_ID: {'✓ Set' if VOICE_ID else '✗ Missing'}")
        sys.exit(1)

    if sys.argv[1] == "--list-voices":
        list_voices()
        sys.exit(0)

    text = " ".join(sys.argv[1:])
    success = speak(text)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
