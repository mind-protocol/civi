#!/usr/bin/env python3
"""
Test script for Living Narrator components.
Run from the civi/ directory.
"""

import sys
import json
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_env():
    """Test environment configuration."""
    print("\n=== Testing .env configuration ===")
    from dotenv import load_dotenv
    import os
    
    load_dotenv(PROJECT_ROOT / ".env")
    
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "")
    civ_path = os.environ.get("WINDOWS_CIV6_PATH", "")
    
    results = {
        "ELEVENLABS_API_KEY": "✅ Set" if api_key else "❌ Missing",
        "ELEVENLABS_VOICE_ID": "✅ Set" if voice_id else "⚠️ Missing (TTS won't work)",
        "WINDOWS_CIV6_PATH": f"✅ {civ_path}" if civ_path else "⚠️ Missing",
    }
    
    for key, status in results.items():
        print(f"  {key}: {status}")
    
    return bool(api_key)


def test_narrator_state():
    """Test narrator state files."""
    print("\n=== Testing narrator state files ===")
    
    state_dir = PROJECT_ROOT / "narrator" / "state"
    files = [
        "status.json",
        "config.json", 
        "cursor.json",
        "history.json",
        "moments.json",
        "threads.json",
        "ideas.json",
    ]
    
    all_ok = True
    for f in files:
        path = state_dir / f
        if path.exists():
            try:
                content = json.loads(path.read_text())
                print(f"  ✅ {f} ({len(json.dumps(content))} bytes)")
            except json.JSONDecodeError:
                print(f"  ⚠️ {f} exists but invalid JSON")
                all_ok = False
        else:
            print(f"  ❌ {f} missing")
            all_ok = False
    
    return all_ok


def test_civ6_path():
    """Test Civ 6 state path."""
    print("\n=== Testing Civ 6 state path ===")
    
    from dotenv import load_dotenv
    import os
    
    load_dotenv(PROJECT_ROOT / ".env")
    
    civ_path = Path(os.environ.get("WINDOWS_CIV6_PATH", "/mnt/c/Users/Nicolas/Documents/Civ6Narrator"))
    
    print(f"  Path: {civ_path}")
    
    if civ_path.exists():
        print(f"  ✅ Directory exists")
        
        events_file = civ_path / "events.jsonl"
        state_file = civ_path / "game_state.json"
        
        if events_file.exists():
            lines = events_file.read_text().strip().split("\n")
            print(f"  ✅ events.jsonl ({len(lines)} events)")
            if lines:
                try:
                    last = json.loads(lines[-1])
                    print(f"     Last event: {last.get('event_type', last.get('type', '?'))}")
                except:
                    pass
        else:
            print(f"  ⚠️ events.jsonl not found (run Civ 6 with mod first)")
        
        if state_file.exists():
            try:
                state = json.loads(state_file.read_text())
                players = state.get("players", [])
                print(f"  ✅ game_state.json (turn {state.get('turn', '?')}, {len(players)} players)")
            except:
                print(f"  ⚠️ game_state.json exists but invalid")
        else:
            print(f"  ⚠️ game_state.json not found (run Civ 6 with mod first)")
        
        return True
    else:
        print(f"  ❌ Directory does not exist")
        print(f"     Run Civ 6 with the LivingNarrator mod to create it")
        return False


def test_elevenlabs_api():
    """Test Eleven Labs API connection."""
    print("\n=== Testing Eleven Labs API ===")
    
    from dotenv import load_dotenv
    import os
    import requests
    
    load_dotenv(PROJECT_ROOT / ".env")
    
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        print("  ❌ API key not set")
        return False
    
    try:
        response = requests.get(
            "https://api.elevenlabs.io/v1/user",
            headers={"xi-api-key": api_key},
            timeout=10
        )
        
        if response.status_code == 200:
            user = response.json()
            subscription = user.get("subscription", {})
            char_count = subscription.get("character_count", 0)
            char_limit = subscription.get("character_limit", 0)
            print(f"  ✅ API connected")
            print(f"     Characters used: {char_count:,} / {char_limit:,}")
            return True
        else:
            print(f"  ❌ API error: {response.status_code}")
            print(f"     {response.text[:100]}")
            return False
            
    except Exception as e:
        print(f"  ❌ Connection error: {e}")
        return False


def list_french_voices():
    """List available French voices."""
    print("\n=== French Voices Available ===")
    
    from dotenv import load_dotenv
    import os
    import requests
    
    load_dotenv(PROJECT_ROOT / ".env")
    
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        return
    
    try:
        response = requests.get(
            "https://api.elevenlabs.io/v1/voices",
            headers={"xi-api-key": api_key},
            timeout=10
        )
        
        if response.status_code == 200:
            voices = response.json().get("voices", [])
            french_voices = []
            
            for v in voices:
                labels = v.get("labels", {})
                lang = labels.get("language", "").lower()
                accent = labels.get("accent", "").lower()
                
                if "french" in lang or "french" in accent or "français" in lang.lower():
                    french_voices.append({
                        "id": v["voice_id"],
                        "name": v["name"],
                        "gender": labels.get("gender", "?"),
                        "age": labels.get("age", "?"),
                    })
            
            if french_voices:
                print(f"  Found {len(french_voices)} French voices:")
                for v in french_voices[:5]:
                    print(f"    {v['id'][:20]}...  {v['name']:<15} [{v['gender']}, {v['age']}]")
                print()
                print("  💡 Add to .env:")
                print(f"     ELEVENLABS_VOICE_ID={french_voices[0]['id']}")
            else:
                print("  ⚠️ No French voices found in your account")
                print("     Get one from https://elevenlabs.io/voice-library")
                
    except Exception as e:
        print(f"  Error: {e}")


def test_tts():
    """Test TTS with a short phrase."""
    print("\n=== Testing TTS ===")
    
    from dotenv import load_dotenv
    import os
    
    load_dotenv(PROJECT_ROOT / ".env")
    
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "")
    if not voice_id:
        print("  ⚠️ ELEVENLABS_VOICE_ID not set, skipping TTS test")
        print("     Run with --list-voices to see available voices")
        return False
    
    try:
        from scripts.speak import speak
        
        test_text = "Test du narrateur. Bienvenue dans la partie."
        print(f"  Speaking: '{test_text}'")
        
        success = speak(test_text)
        
        if success:
            print("  ✅ TTS working")
            return True
        else:
            print("  ❌ TTS failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    print("=" * 50)
    print("Living Narrator - Component Test")
    print("=" * 50)
    
    results = {}
    
    # Test environment
    results["env"] = test_env()
    
    # Test narrator state
    results["state"] = test_narrator_state()
    
    # Test Civ 6 path
    results["civ6"] = test_civ6_path()
    
    # Test Eleven Labs API
    results["api"] = test_elevenlabs_api()
    
    # List French voices
    if "--list-voices" in sys.argv or not results.get("api"):
        list_french_voices()
    
    # Test TTS if requested
    if "--tts" in sys.argv:
        results["tts"] = test_tts()
    
    # Summary
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    
    all_ok = True
    for name, ok in results.items():
        status = "✅" if ok else "❌"
        print(f"  {status} {name}")
        if not ok:
            all_ok = False
    
    if not all_ok:
        print("\n⚠️ Some tests failed. Check the output above.")
    else:
        print("\n✅ All tests passed!")
    
    print("\nNext steps:")
    print("  1. If VOICE_ID missing: python test_narrator.py --list-voices")
    print("  2. To test TTS: python test_narrator.py --tts")
    print("  3. Install Civ 6 mod and play a few turns")
    print("  4. Run daemon: python daemon.py")


if __name__ == "__main__":
    main()
