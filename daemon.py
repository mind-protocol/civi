#!/usr/bin/env python3
"""
Living Narrator Daemon
Orchestrates Claude Code invocations for game narration.
Supports multiple games: Civ6, CK3, and more via game profiles.
"""

import time
import json
import subprocess
import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from game_profile_loader import load_game_profile, get_persona_path, detect_game_from_config, GameProfile

# Setup logging
LOG_FILE = Path("narrator/logs/daemon.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)
logger = logging.getLogger("daemon")

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

# Default events that bypass timing (overridden by game profile)
URGENT_EVENTS = {
    "GAME_START",
    "WAR_DECLARED",
    "CITY_CAPTURED",
    "CAPITAL_CAPTURED",
    "PLAYER_ELIMINATED",
    "WONDER_COMPLETED",
    "WONDER_STARTED",
    "PEACE_MADE",
    "DENOUNCEMENT",
    "ALLIANCE_FORMED"
}

# Current game profile (loaded at startup)
GAME_PROFILE: Optional[GameProfile] = None
PLAYTHROUGH: Optional[str] = None  # e.g., "ck3_jesus"

# Visual mode settings
SCREENSHOT_DIR = Path("/mnt/c/Temp/NarratorScreenshots")
SCREENSHOT_INTERVAL = 20  # seconds between captures (tripled frequency)
SCREENSHOT_MAX_AGE = 180  # max age in seconds for screenshots to consider

# Voice capture settings
VOICE_TRANSCRIPT_FILE = STATE_DIR / "voice_transcript.jsonl"
VOICE_TRANSCRIPT_MAX_AGE = 300  # 5 minutes

# OCR settings
OCR_DIFFS_FILE = STATE_DIR / "ocr_diffs.jsonl"
OCR_CURSOR_FILE = STATE_DIR / "ocr_cursor.json"
OCR_MAX_AGE = 300  # 5 minutes

# Decision capture settings (click watcher)
DECISIONS_FILE = STATE_DIR / "decisions.jsonl"
DECISIONS_CURSOR_FILE = STATE_DIR / "decisions_cursor.json"
DECISIONS_MAX_AGE = 600  # 10 minutes

# Prayer settings (text input from player)
PRAYERS_FILE = STATE_DIR / "prayers.jsonl"
PRAYERS_CURSOR_FILE = STATE_DIR / "prayers_cursor.json"
PRAYERS_MAX_AGE = 3600  # 1 hour (prayers persist longer)

# Prayer request signal (F9 hotkey triggers immediate narration)
PRAYER_REQUEST_FILE = STATE_DIR / "prayer_request.json"


def check_prayer_request() -> Optional[dict]:
    """Check if there's a pending prayer request (F9 hotkey).
    Returns the request data and deletes the signal file if found.
    """
    if not PRAYER_REQUEST_FILE.exists():
        return None

    try:
        # Use utf-8-sig to handle BOM from PowerShell
        content = PRAYER_REQUEST_FILE.read_text(encoding="utf-8-sig")
        data = json.loads(content)
        PRAYER_REQUEST_FILE.unlink()  # Consume the signal
        logger.info("🙏 Prayer request detected (F9 hotkey)")
        return data
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"Error reading prayer request: {e}")
        try:
            PRAYER_REQUEST_FILE.unlink()
        except OSError:
            pass
        return None


def load_config() -> dict:
    """Load daemon configuration."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def get_lua_log_path() -> Path:
    """Get the path to Civ 6 Lua.log."""
    config = load_config()
    return Path(config.get("lua_log_path", "/mnt/c/Users/reyno/AppData/Local/Firaxis Games/Sid Meier's Civilization VI/Logs/Lua.log"))


def get_events_path() -> Path:
    """Get the path to extracted events.jsonl."""
    config = load_config()
    return Path(config.get("events_file", "narrator/state/events.jsonl"))


def is_visual_mode_enabled() -> bool:
    """Check if visual mode is enabled (from game profile or config)."""
    global GAME_PROFILE
    if GAME_PROFILE:
        return GAME_PROFILE.uses_visual
    config = load_config()
    return config.get("visual_mode", False)


def is_visual_primary() -> bool:
    """Check if visual mode is the primary input (no events needed)."""
    global GAME_PROFILE
    if GAME_PROFILE:
        return GAME_PROFILE.visual_primary
    return False


def uses_lua_log() -> bool:
    """Check if this game uses Lua log events."""
    global GAME_PROFILE
    if GAME_PROFILE:
        return GAME_PROFILE.uses_lua_log
    return True  # Default to Civ6 behavior


def get_urgent_events() -> set:
    """Get the set of urgent events for the current game."""
    global GAME_PROFILE
    if GAME_PROFILE and GAME_PROFILE.urgent_events:
        return set(GAME_PROFILE.urgent_events)
    return URGENT_EVENTS


SCREENSHOT_CURSOR_FILE = STATE_DIR / "screenshot_cursor.json"
VOICE_CURSOR_FILE = STATE_DIR / "voice_cursor.json"


def get_recent_voice_transcripts() -> tuple[list[dict], float]:
    """Get recent voice transcripts that haven't been seen."""
    if not VOICE_TRANSCRIPT_FILE.exists():
        return [], 0

    # Read cursor
    last_seen_ts = 0
    if VOICE_CURSOR_FILE.exists():
        try:
            cursor = json.loads(VOICE_CURSOR_FILE.read_text())
            last_seen_ts = cursor.get("last_seen_ts", 0)
        except:
            pass

    transcripts = []
    cutoff = datetime.now().timestamp() - VOICE_TRANSCRIPT_MAX_AGE
    latest_ts = last_seen_ts

    try:
        with open(VOICE_TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_ts = datetime.fromisoformat(entry["ts"]).timestamp()
                    if entry_ts > last_seen_ts and entry_ts > cutoff:
                        transcripts.append(entry)
                        latest_ts = max(latest_ts, entry_ts)
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue
    except Exception:
        pass

    return transcripts, latest_ts


def mark_voice_transcripts_seen(latest_ts: float):
    """Mark voice transcripts as seen."""
    VOICE_CURSOR_FILE.write_text(json.dumps({
        "last_seen_ts": latest_ts,
        "last_update": datetime.now().isoformat()
    }))


def get_recent_ocr_diffs() -> tuple[list[dict], float]:
    """Get recent OCR diffs that haven't been seen."""
    if not OCR_DIFFS_FILE.exists():
        return [], 0

    # Read cursor
    last_seen_ts = 0
    if OCR_CURSOR_FILE.exists():
        try:
            cursor = json.loads(OCR_CURSOR_FILE.read_text())
            last_seen_ts = cursor.get("last_seen_ts", 0)
        except:
            pass

    diffs = []
    cutoff = datetime.now().timestamp() - OCR_MAX_AGE
    latest_ts = last_seen_ts

    try:
        with open(OCR_DIFFS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_ts = datetime.fromisoformat(entry["timestamp"]).timestamp()
                    if entry_ts > last_seen_ts and entry_ts > cutoff:
                        diffs.append(entry)
                        latest_ts = max(latest_ts, entry_ts)
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue
    except Exception:
        pass

    # Sort by priority (highest first) then by time
    diffs.sort(key=lambda d: (-d.get("priority", 0), d.get("timestamp", "")))

    return diffs, latest_ts


def mark_ocr_diffs_seen(latest_ts: float):
    """Mark OCR diffs as seen."""
    OCR_CURSOR_FILE.write_text(json.dumps({
        "last_seen_ts": latest_ts,
        "last_update": datetime.now().isoformat()
    }))


def get_recent_decisions() -> tuple[list[dict], float]:
    """Get recent player decisions (clicks) since last seen."""
    if not DECISIONS_FILE.exists():
        return [], 0

    # Read cursor
    last_seen_ts = 0
    if DECISIONS_CURSOR_FILE.exists():
        try:
            cursor = json.loads(DECISIONS_CURSOR_FILE.read_text())
            last_seen_ts = cursor.get("last_seen_ts", 0)
        except json.JSONDecodeError:
            pass

    cutoff = datetime.now().timestamp() - DECISIONS_MAX_AGE
    decisions = []
    latest_ts = last_seen_ts

    try:
        with open(DECISIONS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_ts = datetime.fromisoformat(entry["timestamp"]).timestamp()
                    if entry_ts > last_seen_ts and entry_ts > cutoff:
                        decisions.append(entry)
                        latest_ts = max(latest_ts, entry_ts)
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue
    except Exception:
        pass

    # Sort by time (oldest first, so we see decisions in order)
    decisions.sort(key=lambda d: d.get("timestamp", ""))

    return decisions, latest_ts


def mark_decisions_seen(latest_ts: float):
    """Mark decisions as seen."""
    DECISIONS_CURSOR_FILE.write_text(json.dumps({
        "last_seen_ts": latest_ts,
        "last_update": datetime.now().isoformat()
    }))


def get_recent_prayers() -> tuple[list[dict], float]:
    """Get recent prayers from player since last seen."""
    if not PRAYERS_FILE.exists():
        return [], 0

    # Read cursor
    last_seen_ts = 0
    if PRAYERS_CURSOR_FILE.exists():
        try:
            cursor = json.loads(PRAYERS_CURSOR_FILE.read_text())
            last_seen_ts = cursor.get("last_seen_ts", 0)
        except json.JSONDecodeError:
            pass

    cutoff = datetime.now().timestamp() - PRAYERS_MAX_AGE
    prayers = []
    latest_ts = last_seen_ts

    try:
        with open(PRAYERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_ts = datetime.fromisoformat(entry["timestamp"]).timestamp()
                    if entry_ts > last_seen_ts and entry_ts > cutoff:
                        prayers.append(entry)
                        latest_ts = max(latest_ts, entry_ts)
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue
    except Exception:
        pass

    # Sort by time (oldest first)
    prayers.sort(key=lambda p: p.get("timestamp", ""))

    return prayers, latest_ts


def mark_prayers_seen(latest_ts: float):
    """Mark prayers as seen."""
    PRAYERS_CURSOR_FILE.write_text(json.dumps({
        "last_seen_ts": latest_ts,
        "last_update": datetime.now().isoformat()
    }))


def read_screenshot_cursor() -> dict:
    """Read the last seen screenshot timestamp."""
    if SCREENSHOT_CURSOR_FILE.exists():
        try:
            return json.loads(SCREENSHOT_CURSOR_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"last_seen_ts": 0}


def write_screenshot_cursor(cursor: dict):
    """Write screenshot cursor."""
    SCREENSHOT_CURSOR_FILE.write_text(json.dumps(cursor, indent=2))


def get_unseen_screenshots() -> list[Path]:
    """Get all screenshots that haven't been seen yet."""
    if not SCREENSHOT_DIR.exists():
        return []

    cursor = read_screenshot_cursor()
    last_seen_ts = cursor.get("last_seen_ts", 0)

    screenshots = sorted(
        SCREENSHOT_DIR.glob("screen_*.png"),
        key=lambda p: p.stat().st_mtime
    )

    # Filter to unseen and not too old
    now = datetime.now().timestamp()
    unseen = []
    for s in screenshots:
        mtime = s.stat().st_mtime
        if mtime > last_seen_ts and (now - mtime) < SCREENSHOT_MAX_AGE:
            unseen.append(s)

    return unseen


def mark_screenshots_seen(screenshots: list[Path]):
    """Mark screenshots as seen by updating cursor."""
    if not screenshots:
        return
    latest_ts = max(s.stat().st_mtime for s in screenshots)
    write_screenshot_cursor({"last_seen_ts": latest_ts, "last_update": datetime.now().isoformat()})


def get_latest_screenshot() -> Optional[Path]:
    """Get the most recent screenshot if it exists and is fresh enough."""
    if not SCREENSHOT_DIR.exists():
        return None

    screenshots = sorted(
        SCREENSHOT_DIR.glob("screen_*.png"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not screenshots:
        return None

    latest = screenshots[0]
    age = datetime.now().timestamp() - latest.stat().st_mtime

    if age > SCREENSHOT_MAX_AGE:
        return None  # Too old

    return latest


def capture_screenshot() -> Optional[Path]:
    """Capture a new screenshot via PowerShell."""
    capture_script = Path(__file__).parent / "scripts" / "capture.py"

    if not capture_script.exists():
        logger.warning(f"capture.py not found at {capture_script}")
        return None

    try:
        result = subprocess.run(
            ["python3", str(capture_script), "--once"],
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode == 0:
            path = Path(result.stdout.strip().split("\n")[-1])
            if path.exists():
                logger.info(f"Screenshot captured: {path.name}")
                return path
        else:
            logger.warning(f"Screenshot capture failed: {result.stderr}")

    except subprocess.TimeoutExpired:
        logger.warning("Screenshot capture timed out")
    except Exception as e:
        logger.error(f"Screenshot error: {e}")

    return None


def ensure_fresh_screenshot() -> Optional[Path]:
    """Get a fresh screenshot, capturing if needed."""
    # Check for existing fresh screenshot
    latest = get_latest_screenshot()
    if latest:
        return latest

    # Capture a new one if visual mode is enabled
    if is_visual_mode_enabled():
        return capture_screenshot()

    return None


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
    """Read event cursor (last processed byte offset in Lua.log)."""
    if CURSOR_FILE.exists():
        try:
            return json.loads(CURSOR_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"byte_offset": 0, "events_written": 0}


def write_cursor(cursor: dict):
    """Write event cursor."""
    CURSOR_FILE.write_text(json.dumps(cursor, indent=2))


def sync_events_from_lua_log() -> list:
    """Extract [LN_EVENT] lines from Lua.log and append to events.jsonl."""
    lua_log = get_lua_log_path()
    events_file = get_events_path()

    if not lua_log.exists():
        return []

    cursor = read_cursor()
    byte_offset = cursor.get("byte_offset", 0)

    # Check if file was truncated (new game session)
    try:
        file_size = lua_log.stat().st_size
        if file_size < byte_offset:
            byte_offset = 0  # Reset - file was truncated
    except Exception:
        return []

    # Read new content from Lua.log
    try:
        with open(lua_log, "r", encoding="utf-8", errors="ignore") as f:
            f.seek(byte_offset)
            new_content = f.read()
            new_offset = f.tell()
    except Exception as e:
        logger.info(f"Error reading Lua.log: {e}")
        return []

    if not new_content:
        return []

    # Extract [LN_EVENT] lines
    events = []
    for line in new_content.split("\n"):
        if "[LN_EVENT]" in line:
            try:
                _, json_str = line.split("[LN_EVENT]", 1)
                event = json.loads(json_str.strip())
                events.append(event)
            except (ValueError, json.JSONDecodeError):
                continue

    # Append to events.jsonl
    if events:
        events_file.parent.mkdir(parents=True, exist_ok=True)
        with open(events_file, "a", encoding="utf-8") as f:
            for event in events:
                f.write(json.dumps(event) + "\n")

    # Update cursor
    write_cursor({
        "byte_offset": new_offset,
        "events_written": cursor.get("events_written", 0) + len(events),
        "last_sync": datetime.now().isoformat()
    })

    return events


def get_new_events() -> list:
    """Sync from Lua.log and return new events (if applicable)."""
    if not uses_lua_log():
        return []  # Pure visual mode - no event extraction
    return sync_events_from_lua_log()


def has_urgent_event(events: list) -> bool:
    """Check if any event is urgent (bypasses timing)."""
    urgent = get_urgent_events()
    return any(e.get("type") in urgent for e in events)


def should_narrate(status: dict, events: list) -> bool:
    """Decide if we should invoke Claude for narration."""
    # Check timing first
    last_ts = status.get("last_narration_ts")
    if not last_ts:
        # First narration of session
        return True

    try:
        last_dt = datetime.fromisoformat(last_ts)
        elapsed = (datetime.now() - last_dt).total_seconds()
    except (ValueError, TypeError):
        return True

    # Too soon (always respect minimum)
    if elapsed < MIN_NARRATION_INTERVAL:
        return False

    # Urgent event = always go (if we use events)
    if events and has_urgent_event(events):
        urgent = get_urgent_events()
        logger.info(f"  → Urgent event detected: {[e.get('type') for e in events if e.get('type') in urgent]}")
        return True

    # Pure visual mode (CK3): narrate based on time + screenshots alone
    if is_visual_primary():
        # Check if there are new screenshots to analyze
        screenshots = get_unseen_screenshots()
        if screenshots and elapsed >= MIN_NARRATION_INTERVAL:
            return True
        # Or if enough time has passed
        if elapsed >= TARGET_NARRATION_INTERVAL:
            return True
        return False

    # Time's up
    if elapsed >= TARGET_NARRATION_INTERVAL:
        return True

    # Visual mode (Civ6): can narrate based on time alone (no events needed)
    if is_visual_mode_enabled() and elapsed >= MIN_NARRATION_INTERVAL:
        return True

    # Between min and target: go if there are events worth mentioning
    return len(events) > 0


def build_narrator_prompt(
    events: list,
    screenshots: list[Path] = None,
    voice_transcripts: list[dict] = None,
    ocr_diffs: list[dict] = None,
    decisions: list[dict] = None,
    prayers: list[dict] = None
) -> str:
    """Build the prompt message for Claude narrator."""
    screenshots = screenshots or []
    voice_transcripts = voice_transcripts or []
    ocr_diffs = ocr_diffs or []
    decisions = decisions or []
    prayers = prayers or []
    events_summary = []
    last_summary = None

    for e in events[-15:]:  # Last 15 events
        e_type = e.get("type", "?")
        if e_type == "GAME_START":
            events_summary.append(f"- Nouvelle partie: {e.get('local_civ', '?')}")
        elif e_type == "TURN_START":
            events_summary.append(f"- Tour {e.get('turn')} commence")
        elif e_type == "TURN_SUMMARY":
            last_summary = e  # Keep only the most recent summary
        elif e_type == "CITY_BUILT":
            events_summary.append(f"- {e.get('player_civ', '?')} fonde {e.get('city', '?')}")
        elif e_type == "WAR_DECLARED":
            events_summary.append(f"- GUERRE: {e.get('attacker', '?')} vs {e.get('defender', '?')}")
        elif e_type == "CITY_CAPTURED":
            events_summary.append(f"- CONQUÊTE: {e.get('new_owner', '?')} prend une ville de {e.get('old_owner', '?')}")
        elif e_type == "WONDER_COMPLETED":
            events_summary.append(f"- MERVEILLE: {e.get('player_civ', '?')} construit {e.get('wonder', '?')}")
        elif e_type == "TECH_COMPLETED":
            events_summary.append(f"- {e.get('player_civ', '?')} découvre {e.get('tech', '?')}")
        elif e_type == "CIVIC_COMPLETED":
            events_summary.append(f"- {e.get('player_civ', '?')} adopte {e.get('civic', '?')}")
        elif e_type == "UNIT_KILLED":
            events_summary.append(f"- Combat: {e.get('killer_unit', 'unité')} ({e.get('killer_civ', '?')}) tue {e.get('killed_unit', 'unité')} ({e.get('killed_civ', '?')})")
        elif e_type == "UNIT_CREATED":
            unit = e.get('unit_name', '?')
            civ = e.get('player_civ', '?')
            if e.get('is_military'):
                events_summary.append(f"- {civ} recrute: {unit}")
        elif e_type == "PEACE_MADE":
            events_summary.append(f"- Paix entre {e.get('player1', '?')} et {e.get('player2', '?')}")
        elif e_type == "WONDER_STARTED":
            events_summary.append(f"- {e.get('player_civ', '?')} commence: {e.get('wonder', '?')}")
        elif e_type == "DENOUNCEMENT":
            events_summary.append(f"- {e.get('actor', '?')} dénonce {e.get('target', '?')}")
        elif e_type == "ALLIANCE_FORMED":
            events_summary.append(f"- Alliance: {e.get('player1', '?')} + {e.get('player2', '?')}")

    events_text = "\n".join(events_summary) if events_summary else "Aucun événement récent"

    # Add turn summary if available
    forces_text = ""
    if last_summary:
        mil = last_summary.get('military_units', 0)
        civ = last_summary.get('civilian_units', 0)
        cities = last_summary.get('cities', 0)
        forces_text = f"\n\nÉtat des forces de {last_summary.get('player_civ', '?')}: {mil} unités militaires, {civ} civiles, {cities} villes"

    # Add screenshot info if available
    screenshot_text = ""
    if screenshots:
        paths_list = "\n".join(f"  - {s}" for s in screenshots)
        screenshot_text = f"""

CAPTURES D'ÉCRAN ({len(screenshots)} nouvelles):
{paths_list}

Lis TOUTES ces captures avec ton outil Read pour voir l'évolution du jeu !"""

    # Add voice transcripts if available
    voice_text = ""
    if voice_transcripts:
        voice_lines = []
        for t in voice_transcripts:
            ts = t.get("ts", "")[:19]  # Truncate to seconds
            speaker = t.get("speaker", "?")
            text = t.get("text", "")
            voice_lines.append(f"  [{ts}] {speaker}: \"{text}\"")
        voice_text = f"""

CE QUE LES JOUEURS ONT DIT ({len(voice_transcripts)} messages):
{chr(10).join(voice_lines)}

Tu peux réagir à ce qu'ils disent, leur répondre, rebondir sur leurs conversations !"""

    # Add OCR diffs if available (text changes detected on screen)
    ocr_text = ""
    if ocr_diffs:
        # Group by priority
        high_priority = [d for d in ocr_diffs if d.get("priority", 0) >= 7]
        other = [d for d in ocr_diffs if d.get("priority", 0) < 7]

        ocr_lines = []

        if high_priority:
            ocr_lines.append("CHANGEMENTS IMPORTANTS:")
            for d in high_priority[:5]:  # Max 5 high priority
                region = d.get("region", "?")
                summary = d.get("summary", "")
                new_text = d.get("new_text", "")[:200]
                if d.get("change_type") == "new" and new_text:
                    ocr_lines.append(f"  [{region}] NOUVEAU: {new_text}...")
                else:
                    ocr_lines.append(f"  {summary}")

        if other:
            ocr_lines.append("\nAutres changements:")
            for d in other[:5]:  # Max 5 other
                ocr_lines.append(f"  {d.get('summary', '?')}")

        ocr_text = f"""

TEXTE DÉTECTÉ À L'ÉCRAN (OCR - {len(ocr_diffs)} changements):
{chr(10).join(ocr_lines)}

Ces changements ont été détectés automatiquement. Ils te donnent du contexte sur ce qui se passe !"""

    # Add decisions if available (clicks with context)
    decisions_text = ""
    if decisions:
        decision_lines = []
        for d in decisions[-5:]:  # Last 5 decisions
            ts = d.get("timestamp", "")[:19]
            x, y = d.get("x", 0), d.get("y", 0)
            region_text = d.get("region_ocr", "").strip()[:150]
            screenshot = d.get("screenshot_path", "")

            if region_text:
                decision_lines.append(f"  [{ts}] Clic ({x}, {y}): \"{region_text}...\"")
            else:
                decision_lines.append(f"  [{ts}] Clic ({x}, {y})")

            if screenshot:
                decision_lines.append(f"    Screenshot: {screenshot}")

        decisions_text = f"""

DÉCISIONS DU JOUEUR ({len(decisions)} clics capturés):
{chr(10).join(decision_lines)}

Ces clics montrent les choix que Jésus a faits. Tu peux lire les screenshots pour voir le contexte complet de chaque décision !"""

    # Add prayers if available (text questions from player)
    prayers_text = ""
    if prayers:
        prayer_lines = []
        for p in prayers:
            ts = p.get("timestamp", "")[:19]
            text = p.get("text", "").strip()
            prayer_lines.append(f"  [{ts}] \"{text}\"")

        prayers_text = f"""

🙏 PRIÈRES DE JÉSUS ({len(prayers)} messages):
{chr(10).join(prayer_lines)}

Jésus t'adresse ces questions directement. En tant que Dieu, tu dois y répondre avec sagesse - parfois clairement, parfois par une parabole, parfois par le silence. Ta réponse peut être dans ta narration ou dans les événements que tu fais advenir."""

    # Visual-only mode: different prompt structure
    if screenshots and not events_summary:
        return f"""MODE VISUEL - {len(screenshots)} captures d'écran à analyser !
{screenshot_text}{decisions_text}{prayers_text}{ocr_text}{voice_text}

Regarde les captures et commente ce que tu vois :
- Évolution entre les captures (mouvements, changements)
- Positions des unités, troupes en mouvement
- État des villes, constructions, frontières
- Menaces, opportunités, situations intéressantes

Les DÉCISIONS montrent les choix du joueur - c'est crucial pour comprendre ses intentions !
Les PRIÈRES sont des questions directes de Jésus - réponds-y avec sagesse divine !
L'OCR te donne du contexte sur les textes à l'écran.

Écris ta narration dans state/last_narration.txt.
N'oublie pas de mettre à jour state/status.json à la fin."""

    return f"""Nouveaux événements depuis ta dernière narration:

{events_text}{forces_text}{screenshot_text}{decisions_text}{prayers_text}{ocr_text}{voice_text}

Décide si tu veux narrer quelque chose et écris dans state/last_narration.txt.
N'oublie pas de mettre à jour state/status.json à la fin."""


def get_narration_file() -> Path:
    """Get the path to the narration file (depends on playthrough)."""
    global PLAYTHROUGH
    if PLAYTHROUGH:
        return Path(__file__).parent / "playthroughs" / PLAYTHROUGH / "state" / "last_narration.txt"
    return STATE_DIR / "last_narration.txt"


def speak_text(text: str) -> bool:
    """Call speak.py to play the narration."""
    speak_script = Path(__file__).parent / "scripts" / "speak.py"
    if not speak_script.exists():
        logger.warning(f"speak.py not found at {speak_script}")
        return False

    try:
        logger.info(f"🎙️  Speaking: {text[:60]}...")
        result = subprocess.run(
            ["python3", str(speak_script), text],
            cwd=Path(__file__).parent,
            timeout=60,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info("🔊 Audio played")
            return True
        else:
            logger.warning(f"speak.py failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.warning("speak.py timed out")
        return False
    except Exception as e:
        logger.error(f"Error calling speak.py: {e}")
        return False


def get_persona_file() -> str:
    """Get the persona file to use for Claude."""
    global GAME_PROFILE
    if GAME_PROFILE:
        return GAME_PROFILE.persona_file
    return "CLAUDE.md"


def run_claude(events: list):
    """Invoke Claude Code for narration."""
    global GAME_PROFILE, PLAYTHROUGH
    base_dir = Path(__file__).parent

    # Use playthrough folder if specified, otherwise default narrator folder
    if PLAYTHROUGH:
        narrator_dir = base_dir / "playthroughs" / PLAYTHROUGH
        if not narrator_dir.exists():
            logger.warning(f"Playthrough folder not found: {narrator_dir}, falling back to narrator/")
            narrator_dir = base_dir / "narrator"
    else:
        narrator_dir = base_dir / "narrator"

    # Get all unseen screenshots if visual mode is enabled
    screenshots = []
    if is_visual_mode_enabled():
        # First capture a new one
        new_capture = capture_screenshot()

        # Get all unseen screenshots
        screenshots = get_unseen_screenshots()
        if screenshots:
            mode_name = "Pure visual" if is_visual_primary() else "Visual"
            logger.info(f"{mode_name} mode: {len(screenshots)} screenshots to analyze")
            for s in screenshots:
                logger.info(f"  - {s.name}")

    # Get voice transcripts
    voice_transcripts, voice_latest_ts = get_recent_voice_transcripts()
    if voice_transcripts:
        logger.info(f"Voice: {len(voice_transcripts)} new messages from players")
        for t in voice_transcripts:
            logger.info(f"  - {t.get('speaker', '?')}: {t.get('text', '')[:50]}...")

    # Get OCR diffs (text changes detected on screen)
    ocr_diffs, ocr_latest_ts = get_recent_ocr_diffs()
    if ocr_diffs:
        high_priority = sum(1 for d in ocr_diffs if d.get("priority", 0) >= 7)
        logger.info(f"OCR: {len(ocr_diffs)} text changes ({high_priority} high priority)")
        for d in ocr_diffs[:3]:  # Log first 3
            logger.info(f"  - {d.get('summary', '?')}")

    # Get player decisions (clicks with context)
    decisions, decisions_latest_ts = get_recent_decisions()
    if decisions:
        logger.info(f"Decisions: {len(decisions)} player clicks captured")
        for d in decisions[:3]:  # Log first 3
            region_preview = d.get('region_ocr', '')[:30] or '(no text)'
            logger.info(f"  - ({d.get('x')}, {d.get('y')}): {region_preview}...")

    # Get prayers (text questions from player)
    prayers, prayers_latest_ts = get_recent_prayers()
    if prayers:
        logger.info(f"🙏 Prayers: {len(prayers)} messages from Jesus")
        for p in prayers:
            logger.info(f"  - \"{p.get('text', '')[:50]}...\"")

    prompt = build_narrator_prompt(events, screenshots, voice_transcripts, ocr_diffs, decisions, prayers)

    # Clear previous narration
    if get_narration_file().exists():
        get_narration_file().unlink()

    try:
        result = subprocess.run(
            [
                "claude",
                "-p", prompt,
                "--continue",
                "--dangerously-skip-permissions",
                "--add-dir", str(Path(__file__).parent)
            ],
            cwd=narrator_dir,
            timeout=CLAUDE_TIMEOUT,
            capture_output=False
        )

        # Check if Claude wrote a narration
        if get_narration_file().exists():
            narration = get_narration_file().read_text().strip()
            if narration:
                speak_text(narration)

        # Mark screenshots as seen
        if screenshots:
            mark_screenshots_seen(screenshots)

        # Mark voice transcripts as seen
        if voice_transcripts:
            mark_voice_transcripts_seen(voice_latest_ts)

        # Mark OCR diffs as seen
        if ocr_diffs:
            mark_ocr_diffs_seen(ocr_latest_ts)

        # Mark decisions as seen
        if decisions:
            mark_decisions_seen(decisions_latest_ts)

        # Mark prayers as seen
        if prayers:
            mark_prayers_seen(prayers_latest_ts)

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        logger.info("⚠️  Claude timed out")
        # Still mark as seen to avoid reprocessing on timeout
        if screenshots:
            mark_screenshots_seen(screenshots)
        if voice_transcripts:
            mark_voice_transcripts_seen(voice_latest_ts)
        if ocr_diffs:
            mark_ocr_diffs_seen(ocr_latest_ts)
        if decisions:
            mark_decisions_seen(decisions_latest_ts)
        if prayers:
            mark_prayers_seen(prayers_latest_ts)
        return False
    except Exception as e:
        logger.info(f"❌ Error running Claude: {e}")
        return False


def load_game_profile_from_config():
    """Load game profile based on config."""
    global GAME_PROFILE, SCREENSHOT_INTERVAL, PLAYTHROUGH

    config = load_config()
    game_id = detect_game_from_config(config)
    PLAYTHROUGH = config.get("playthrough")  # e.g., "ck3_jesus"

    try:
        GAME_PROFILE = load_game_profile(game_id)
        SCREENSHOT_INTERVAL = GAME_PROFILE.screenshot_interval
        logger.info(f"🎮 Game profile loaded: {GAME_PROFILE.game_name}")
        if PLAYTHROUGH:
            logger.info(f"🎭 Playthrough: {PLAYTHROUGH}")
        return True
    except FileNotFoundError:
        logger.warning(f"Game profile not found for '{game_id}', using defaults")
        GAME_PROFILE = None
        return False


def main():
    global GAME_PROFILE

    logger.info("🎭 Living Narrator daemon started")

    # Load game profile
    load_game_profile_from_config()

    if GAME_PROFILE:
        config = load_config()
        logger.info(f"   Game: {GAME_PROFILE.game_name}")
        if PLAYTHROUGH:
            persona_path = Path(__file__).parent / "playthroughs" / PLAYTHROUGH / "CLAUDE.md"
            logger.info(f"   Playthrough: {PLAYTHROUGH}")
            logger.info(f"   Persona: {persona_path}")
        else:
            logger.info(f"   Persona: {GAME_PROFILE.persona_file}")
        # Allow config to override role (for special playthroughs like ck3_jesus)
        role = config.get("narrator_role", GAME_PROFILE.narrator_role)
        logger.info(f"   Role: {role}")

    logger.info(f"   Check interval: {CHECK_INTERVAL}s")
    logger.info(f"   Target narration interval: {TARGET_NARRATION_INTERVAL}s")

    if is_visual_primary():
        logger.info(f"   📸 PURE VISUAL MODE (screenshots are primary input)")
        logger.info(f"   Screenshots: {SCREENSHOT_DIR}")
        logger.info(f"   Capture interval: {SCREENSHOT_INTERVAL}s")
        logger.info(f"   No event extraction (visual analysis only)")
    elif is_visual_mode_enabled():
        logger.info(f"   📸 Visual mode: ENABLED (screenshots every {SCREENSHOT_INTERVAL}s)")
        logger.info(f"   Screenshots: {SCREENSHOT_DIR}")
        logger.info(f"   Lua events: optional (will use if available)")
    else:
        logger.info(f"   Lua.log: {get_lua_log_path()}")
        logger.info(f"   Events: {get_events_path()}")
        logger.info(f"   📸 Visual mode: disabled (set visual_mode: true in config.json)")

    # Reset status on daemon startup (clears stale claude_running from previous crashes)
    write_status({"claude_running": False, "daemon_start": datetime.now().isoformat()})
    logger.info("   ✓ Status reset on daemon startup")

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
                            logger.info("⚠️  Claude timeout detected, resetting status")
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

            # Check for prayer request (F9 hotkey - bypasses timing)
            prayer_request = check_prayer_request()
            if prayer_request:
                logger.info(f"🙏 [{now.strftime('%H:%M:%S')}] Player invoked the chronicler!")

                # Update status: Claude running
                status["claude_running"] = True
                status["last_run_start"] = now.isoformat()
                write_status(status)

                # Run Claude immediately with prayer context
                events = get_new_events()  # Still get events for context
                success = run_claude(events)

                # Update status: Claude done
                status = read_status()
                status["claude_running"] = False
                status["last_run_end"] = datetime.now().isoformat()
                if success:
                    status["last_narration_ts"] = datetime.now().isoformat()
                write_status(status)

                time.sleep(CHECK_INTERVAL)
                continue

            # Check for new events
            events = get_new_events()

            # Decide if we should narrate
            if should_narrate(status, events):
                event_count = len(events)
                logger.info(f"🎬 [{now.strftime('%H:%M:%S')}] Triggering narration ({event_count} new events)")

                # Update status: Claude running
                status["claude_running"] = True
                status["last_run_start"] = now.isoformat()
                write_status(status)

                # Run Claude
                success = run_claude(events)

                # Update status: Claude done
                status = read_status()  # Re-read in case Claude updated it
                status["claude_running"] = False
                status["last_run_end"] = datetime.now().isoformat()
                if success:
                    status["last_narration_ts"] = datetime.now().isoformat()
                write_status(status)

                if success:
                    logger.info(f"✅ Narration complete")
                else:
                    logger.info(f"⚠️  Narration may have failed")

        except KeyboardInterrupt:
            logger.info("\n👋 Daemon stopped")
            sys.exit(0)
        except Exception as e:
            logger.info(f"❌ Error: {e}")
            # Reset status on error
            write_status({"claude_running": False, "error": str(e), "error_ts": datetime.now().isoformat()})

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
