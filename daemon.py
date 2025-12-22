#!/usr/bin/env python3
"""
Living Narrator Daemon
Orchestrates Claude Code invocations for Civ 6 narration.
"""

import time
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Paths
STATE_DIR = Path("narrator/state")
STATUS_FILE = STATE_DIR / "status.json"
CURSOR_FILE = STATE_DIR / "cursor.json"
CONFIG_FILE = STATE_DIR / "config.json"

# Timing
CHECK_INTERVAL = 10  # seconds between daemon checks
MIN_NARRATION_INTERVAL = 30  # minimum seconds between narrations
TARGET_NARRATION_INTERVAL = 120  # target ~2 min between narrations
CLAUDE_TIMEOUT = 300  # 5 min max for a Claude run

# Events that bypass timing restrictions
URGENT_EVENTS = {
    "WAR_DECLARED",
    "CITY_CAPTURED",
    "CAPITAL_CAPTURED",
    "PLAYER_ELIMINATED",
    "WONDER_COMPLETED",
    "PEACE_MADE"
}


def get_civ6_path() -> Path:
    """Get the path to Civ 6 state directory from config."""
    if CONFIG_FILE.exists():
        config = json.loads(CONFIG_FILE.read_text())
        windows_path = config.get("windows_state_path", "")
        if windows_path:
            return Path(windows_path)
    # Fallback from .env
    return Path("/mnt/c/Users/Nicolas/Documents/Civ6Narrator")


def get_events_path() -> Path:
    """Get the path to events.jsonl."""
    return get_civ6_path() / "events.jsonl"


def get_game_state_path() -> Path:
    """Get the path to game_state.json."""
    return get_civ6_path() / "game_state.json"


def read_status() -> dict:
    """Read daemon/Claude status."""
    if STATUS_FILE.exists():
        try:
            return json.loads(STATUS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"claude_running": False, "last_narration_ts": None}


def write_status(status: dict):
    """Write daemon/Claude status."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATUS_FILE.write_text(json.dumps(status, indent=2))


def read_cursor() -> dict:
    """Read event cursor (last processed position)."""
    if CURSOR_FILE.exists():
        try:
            return json.loads(CURSOR_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"last_line": 0}


def get_new_events() -> list:
    """Get events since last cursor position."""
    events_file = get_events_path()
    if not events_file.exists():
        return []

    cursor = read_cursor()
    last_line = cursor.get("last_line", 0)

    try:
        lines = events_file.read_text().strip().split("\n")
    except Exception:
        return []

    new_lines = lines[last_line:] if last_line < len(lines) else []

    events = []
    for line in new_lines:
        if line.strip():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return events


def has_urgent_event(events: list) -> bool:
    """Check if any event is urgent (bypasses timing)."""
    return any(e.get("type") in URGENT_EVENTS for e in events)


def should_narrate(status: dict, events: list) -> bool:
    """Decide if we should invoke Claude for narration."""
    # Urgent event = always go
    if has_urgent_event(events):
        print(f"  → Urgent event detected: {[e.get('type') for e in events if e.get('type') in URGENT_EVENTS]}")
        return True

    # Check timing
    last_ts = status.get("last_narration_ts")
    if not last_ts:
        # First narration of session
        return True

    try:
        last_dt = datetime.fromisoformat(last_ts)
        elapsed = (datetime.now() - last_dt).total_seconds()
    except (ValueError, TypeError):
        return True

    # Too soon
    if elapsed < MIN_NARRATION_INTERVAL:
        return False

    # Time's up
    if elapsed >= TARGET_NARRATION_INTERVAL:
        return True

    # Between min and target: go if there are events worth mentioning
    return len(events) > 0


def run_claude():
    """Invoke Claude Code for narration."""
    try:
        result = subprocess.run(
            ["claude", "--continue", "-p", "narrator"],
            cwd=Path(__file__).parent,
            timeout=CLAUDE_TIMEOUT,
            capture_output=False
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⚠️  Claude timed out")
        return False
    except Exception as e:
        print(f"❌ Error running Claude: {e}")
        return False


def main():
    print("🎭 Living Narrator daemon started")
    print(f"   Check interval: {CHECK_INTERVAL}s")
    print(f"   Target narration interval: {TARGET_NARRATION_INTERVAL}s")
    print(f"   Civ6 path: {get_civ6_path()}")
    print(f"   Events: {get_events_path()}")
    print(f"   State:  {get_game_state_path()}")
    print()

    while True:
        try:
            status = read_status()
            now = datetime.now()

            # Check if Claude is already running (with timeout protection)
            if status.get("claude_running"):
                start_ts = status.get("last_run_start")
                if start_ts:
                    try:
                        start_dt = datetime.fromisoformat(start_ts)
                        elapsed = (now - start_dt).total_seconds()
                        if elapsed > CLAUDE_TIMEOUT:
                            print("⚠️  Claude timeout detected, resetting status")
                            status["claude_running"] = False
                            write_status(status)
                        else:
                            time.sleep(CHECK_INTERVAL)
                            continue
                    except (ValueError, TypeError):
                        status["claude_running"] = False
                        write_status(status)
                else:
                    time.sleep(CHECK_INTERVAL)
                    continue

            # Check for new events
            events = get_new_events()

            # Decide if we should narrate
            if should_narrate(status, events):
                event_count = len(events)
                print(f"🎬 [{now.strftime('%H:%M:%S')}] Triggering narration ({event_count} new events)")

                # Update status: Claude running
                status["claude_running"] = True
                status["last_run_start"] = now.isoformat()
                write_status(status)

                # Run Claude
                success = run_claude()

                # Update status: Claude done
                status = read_status()  # Re-read in case Claude updated it
                status["claude_running"] = False
                status["last_run_end"] = datetime.now().isoformat()
                if success:
                    status["last_narration_ts"] = datetime.now().isoformat()
                write_status(status)

                if success:
                    print(f"✅ Narration complete")
                else:
                    print(f"⚠️  Narration may have failed")

        except KeyboardInterrupt:
            print("\n👋 Daemon stopped")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")
            # Reset status on error
            write_status({"claude_running": False, "error": str(e), "error_ts": datetime.now().isoformat()})

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
