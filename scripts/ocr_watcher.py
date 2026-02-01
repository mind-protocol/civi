#!/usr/bin/env python3
"""
OCR Watcher for Living Narrator.
Captures screenshots frequently, runs local OCR, detects changes.
Outputs a stream of text diffs for the narrator to consume.
"""

import subprocess
import sys
import json
import time
import hashlib
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional
from difflib import unified_diff

# Try to import OCR libraries
try:
    import pytesseract
    from PIL import Image, ImageFilter, ImageOps
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False
    print("Warning: pytesseract/PIL not installed. Install with: pip install pytesseract pillow", file=sys.stderr)

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
STATE_DIR = PROJECT_DIR / "narrator" / "state"
OCR_STATE_FILE = STATE_DIR / "ocr_state.json"
OCR_DIFFS_FILE = STATE_DIR / "ocr_diffs.jsonl"
SCREENSHOT_DIR = Path("/mnt/c/Temp/NarratorScreenshots")

# OCR Configuration
OCR_INTERVAL = 5  # seconds between OCR runs
MIN_CHANGE_THRESHOLD = 50  # minimum characters changed to report
TESSERACT_CONFIG = '--oem 3 --psm 6 -l eng+fra'  # OCR engine mode 3, page segmentation 6


@dataclass
class ScreenRegion:
    """A region of the screen to OCR."""
    name: str
    x: float  # 0-1 percentage from left
    y: float  # 0-1 percentage from top
    w: float  # width as percentage
    h: float  # height as percentage
    priority: int = 1  # higher = more important changes


@dataclass
class OCRResult:
    """Result of OCR on a region."""
    region: str
    text: str
    hash: str
    timestamp: str


@dataclass
class TextDiff:
    """A detected text change."""
    timestamp: str
    region: str
    change_type: str  # 'new', 'removed', 'changed'
    old_text: str
    new_text: str
    summary: str  # human-readable summary
    priority: int


# CK3-specific screen regions (approximate, may need tuning)
CK3_REGIONS = [
    # Event popup (center of screen) - most narrative content
    ScreenRegion("event_popup", 0.25, 0.15, 0.50, 0.60, priority=10),

    # Top bar - resources
    ScreenRegion("top_bar", 0.0, 0.0, 1.0, 0.05, priority=3),

    # Character panel (right side when open)
    ScreenRegion("character_panel", 0.65, 0.10, 0.35, 0.80, priority=5),

    # Notifications (top right)
    ScreenRegion("notifications", 0.75, 0.05, 0.25, 0.30, priority=7),

    # Bottom left - current character info
    ScreenRegion("player_info", 0.0, 0.85, 0.25, 0.15, priority=4),

    # Center bottom - speed/pause, date
    ScreenRegion("game_info", 0.40, 0.92, 0.20, 0.08, priority=2),
]

# Civ6-specific regions
CIV6_REGIONS = [
    # Top bar - civics/tech/gold/etc
    ScreenRegion("top_bar", 0.0, 0.0, 1.0, 0.08, priority=3),

    # Unit panel (bottom left)
    ScreenRegion("unit_panel", 0.0, 0.70, 0.25, 0.30, priority=4),

    # City panel (when city selected)
    ScreenRegion("city_panel", 0.0, 0.0, 0.30, 0.50, priority=5),

    # Notifications (right side)
    ScreenRegion("notifications", 0.85, 0.10, 0.15, 0.60, priority=6),

    # Great works/gossip popups
    ScreenRegion("popup_center", 0.25, 0.20, 0.50, 0.50, priority=8),

    # Turn indicator
    ScreenRegion("turn_info", 0.45, 0.0, 0.10, 0.05, priority=2),
]


def get_regions_for_game(game: str) -> list[ScreenRegion]:
    """Get screen regions for a specific game."""
    if game == "ck3":
        return CK3_REGIONS
    elif game == "civ6":
        return CIV6_REGIONS
    else:
        # Generic - just do full screen
        return [ScreenRegion("full_screen", 0, 0, 1, 1, priority=5)]


def load_ocr_state() -> dict:
    """Load previous OCR state."""
    if OCR_STATE_FILE.exists():
        try:
            return json.loads(OCR_STATE_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"last_results": {}, "last_update": None}


def save_ocr_state(state: dict):
    """Save OCR state."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    OCR_STATE_FILE.write_text(json.dumps(state, indent=2))


def append_diff(diff: TextDiff):
    """Append a diff to the diffs file."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(OCR_DIFFS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(diff)) + "\n")


def get_latest_screenshot() -> Optional[Path]:
    """Get the most recent screenshot."""
    if not SCREENSHOT_DIR.exists():
        return None

    screenshots = sorted(
        SCREENSHOT_DIR.glob("screen_*.png"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    return screenshots[0] if screenshots else None


def crop_region(img: Image.Image, region: ScreenRegion) -> Image.Image:
    """Crop an image to a specific region."""
    w, h = img.size
    left = int(w * region.x)
    top = int(h * region.y)
    right = int(w * (region.x + region.w))
    bottom = int(h * (region.y + region.h))
    return img.crop((left, top, right, bottom))


def preprocess_for_ocr(img: Image.Image) -> Image.Image:
    """Preprocess image for better OCR results."""
    # Convert to grayscale
    img = img.convert('L')

    # Increase contrast
    img = ImageOps.autocontrast(img, cutoff=2)

    # Slight sharpen
    img = img.filter(ImageFilter.SHARPEN)

    # Scale up for better OCR (2x)
    w, h = img.size
    img = img.resize((w * 2, h * 2), Image.Resampling.LANCZOS)

    return img


def ocr_region(img: Image.Image, region: ScreenRegion) -> OCRResult:
    """Run OCR on a specific region of an image."""
    # Crop to region
    region_img = crop_region(img, region)

    # Preprocess
    processed = preprocess_for_ocr(region_img)

    # Run OCR
    try:
        text = pytesseract.image_to_string(processed, config=TESSERACT_CONFIG)
        text = text.strip()
        # Clean up common OCR artifacts
        text = re.sub(r'\n{3,}', '\n\n', text)  # Reduce multiple newlines
        text = re.sub(r'[|]{2,}', '', text)  # Remove OCR noise
    except Exception as e:
        text = f"[OCR Error: {e}]"

    # Hash for change detection
    text_hash = hashlib.md5(text.encode()).hexdigest()[:12]

    return OCRResult(
        region=region.name,
        text=text,
        hash=text_hash,
        timestamp=datetime.now().isoformat()
    )


def summarize_change(old_text: str, new_text: str, region: str) -> str:
    """Create a human-readable summary of a text change."""
    if not old_text:
        # New content appeared
        preview = new_text[:100].replace('\n', ' ')
        return f"[{region}] New: {preview}..."

    if not new_text:
        # Content disappeared
        return f"[{region}] Closed/cleared"

    # Content changed - find key differences
    old_words = set(old_text.lower().split())
    new_words = set(new_text.lower().split())

    added = new_words - old_words
    removed = old_words - new_words

    parts = []
    if added:
        parts.append(f"+{len(added)} words")
    if removed:
        parts.append(f"-{len(removed)} words")

    # Try to extract key info (numbers, names)
    numbers_old = set(re.findall(r'\d+', old_text))
    numbers_new = set(re.findall(r'\d+', new_text))
    new_numbers = numbers_new - numbers_old
    if new_numbers:
        parts.append(f"new numbers: {', '.join(list(new_numbers)[:3])}")

    return f"[{region}] {'; '.join(parts)}" if parts else f"[{region}] Minor change"


def detect_changes(
    current_results: dict[str, OCRResult],
    previous_results: dict[str, OCRResult],
    regions: list[ScreenRegion]
) -> list[TextDiff]:
    """Detect changes between OCR results."""
    diffs = []
    region_priority = {r.name: r.priority for r in regions}

    for region_name, current in current_results.items():
        previous = previous_results.get(region_name)
        priority = region_priority.get(region_name, 1)

        if previous is None:
            # New region appeared
            if len(current.text) > MIN_CHANGE_THRESHOLD:
                diffs.append(TextDiff(
                    timestamp=current.timestamp,
                    region=region_name,
                    change_type="new",
                    old_text="",
                    new_text=current.text,
                    summary=summarize_change("", current.text, region_name),
                    priority=priority
                ))
        elif current.hash != previous.hash:
            # Content changed
            change_size = abs(len(current.text) - len(previous.text))
            if change_size > MIN_CHANGE_THRESHOLD or priority >= 7:
                diffs.append(TextDiff(
                    timestamp=current.timestamp,
                    region=region_name,
                    change_type="changed",
                    old_text=previous.text,
                    new_text=current.text,
                    summary=summarize_change(previous.text, current.text, region_name),
                    priority=priority
                ))

    # Check for regions that disappeared
    for region_name, previous in previous_results.items():
        if region_name not in current_results:
            diffs.append(TextDiff(
                timestamp=datetime.now().isoformat(),
                region=region_name,
                change_type="removed",
                old_text=previous.text,
                new_text="",
                summary=f"[{region_name}] Closed",
                priority=region_priority.get(region_name, 1)
            ))

    # Sort by priority (highest first)
    diffs.sort(key=lambda d: -d.priority)

    return diffs


def run_ocr_cycle(game: str = "ck3") -> list[TextDiff]:
    """Run one OCR cycle: capture, OCR, detect changes."""
    if not HAS_TESSERACT:
        print("Tesseract not available", file=sys.stderr)
        return []

    # Get latest screenshot
    screenshot = get_latest_screenshot()
    if not screenshot:
        return []

    # Check if screenshot is fresh (within last 30 seconds)
    age = time.time() - screenshot.stat().st_mtime
    if age > 30:
        return []  # Screenshot too old

    # Load image
    try:
        img = Image.open(screenshot)
    except Exception as e:
        print(f"Error loading image: {e}", file=sys.stderr)
        return []

    # Load previous state
    state = load_ocr_state()
    previous_results = {
        name: OCRResult(**data)
        for name, data in state.get("last_results", {}).items()
    }

    # Get regions for this game
    regions = get_regions_for_game(game)

    # Run OCR on each region
    current_results = {}
    for region in regions:
        result = ocr_region(img, region)
        if result.text:  # Only store non-empty results
            current_results[region.name] = result

    # Detect changes
    diffs = detect_changes(current_results, previous_results, regions)

    # Save state
    state["last_results"] = {
        name: asdict(result) for name, result in current_results.items()
    }
    state["last_update"] = datetime.now().isoformat()
    state["screenshot"] = str(screenshot)
    save_ocr_state(state)

    # Append diffs to file
    for diff in diffs:
        append_diff(diff)
        print(f"  {diff.summary}")

    return diffs


def watch_loop(game: str = "ck3", interval: int = OCR_INTERVAL):
    """Run continuous OCR watching."""
    print(f"OCR Watcher started for {game}")
    print(f"  Interval: {interval}s")
    print(f"  Regions: {len(get_regions_for_game(game))}")
    print(f"  Output: {OCR_DIFFS_FILE}")
    print()

    while True:
        try:
            diffs = run_ocr_cycle(game)
            if diffs:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {len(diffs)} changes detected")
        except KeyboardInterrupt:
            print("\nStopped")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

        time.sleep(interval)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="OCR Watcher for Living Narrator")
    parser.add_argument("--game", choices=["ck3", "civ6"], default="ck3",
                       help="Game to watch (affects screen regions)")
    parser.add_argument("--interval", type=int, default=OCR_INTERVAL,
                       help="Seconds between OCR cycles")
    parser.add_argument("--once", action="store_true",
                       help="Run once and exit")
    parser.add_argument("--show-regions", action="store_true",
                       help="Show region definitions and exit")

    args = parser.parse_args()

    if args.show_regions:
        print(f"Regions for {args.game}:")
        for r in get_regions_for_game(args.game):
            print(f"  {r.name}: ({r.x:.0%}, {r.y:.0%}) {r.w:.0%}x{r.h:.0%} [priority={r.priority}]")
        return

    if not HAS_TESSERACT:
        print("Error: pytesseract not installed")
        print("Install with: pip install pytesseract pillow")
        print("Also install Tesseract OCR: sudo apt install tesseract-ocr tesseract-ocr-fra")
        sys.exit(1)

    if args.once:
        diffs = run_ocr_cycle(args.game)
        print(f"Found {len(diffs)} changes")
    else:
        watch_loop(args.game, args.interval)


if __name__ == "__main__":
    main()
