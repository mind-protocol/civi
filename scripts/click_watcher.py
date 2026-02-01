#!/usr/bin/env python3
"""
Click Watcher for Living Narrator.
Captures screenshots at the moment of each click to record decisions.
"""

import subprocess
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

# Try to import required libraries
try:
    from pynput import mouse
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False
    print("Warning: pynput not installed. Install with: pip install pynput", file=sys.stderr)

try:
    import pytesseract
    from PIL import Image, ImageGrab, ImageFilter, ImageOps
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
STATE_DIR = PROJECT_DIR / "narrator" / "state"
DECISIONS_FILE = STATE_DIR / "decisions.jsonl"
CLICK_SCREENSHOTS_DIR = Path("/mnt/c/Temp/NarratorScreenshots/clicks")

# Configuration
CLICK_COOLDOWN = 0.5  # Minimum seconds between recorded clicks
OCR_REGION_SIZE = 400  # Pixels around click to OCR
TESSERACT_CONFIG = '--oem 3 --psm 6 -l eng+fra'


@dataclass
class Decision:
    """A recorded decision (click)."""
    timestamp: str
    x: int
    y: int
    screen_width: int
    screen_height: int
    screenshot_path: str
    ocr_text: str
    region_ocr: str  # Text specifically around the click


def capture_screen_at_click(x: int, y: int) -> Optional[Path]:
    """Capture screenshot immediately when click detected."""
    CLICK_SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
    filename = f"click_{timestamp}_{x}_{y}.png"
    filepath = CLICK_SCREENSHOTS_DIR / filename

    try:
        # Use PIL ImageGrab for fast capture
        screenshot = ImageGrab.grab()
        screenshot.save(str(filepath))
        return filepath
    except Exception as e:
        print(f"Screenshot error: {e}", file=sys.stderr)
        return None


def ocr_region_around_click(image_path: Path, x: int, y: int, region_size: int = OCR_REGION_SIZE) -> str:
    """Extract text from region around click point."""
    if not HAS_PIL:
        return ""

    try:
        img = Image.open(image_path)
        width, height = img.size

        # Calculate region bounds (centered on click)
        half = region_size // 2
        left = max(0, x - half)
        top = max(0, y - half)
        right = min(width, x + half)
        bottom = min(height, y + half)

        # Crop region
        region = img.crop((left, top, right, bottom))

        # Preprocess for OCR
        region = region.convert('L')  # Grayscale
        region = ImageOps.autocontrast(region)
        region = region.filter(ImageFilter.SHARPEN)
        region = region.resize((region.width * 2, region.height * 2), Image.LANCZOS)

        # OCR
        text = pytesseract.image_to_string(region, config=TESSERACT_CONFIG)
        return text.strip()
    except Exception as e:
        print(f"OCR error: {e}", file=sys.stderr)
        return ""


def ocr_full_screen(image_path: Path) -> str:
    """Extract text from full screenshot (simplified)."""
    if not HAS_PIL:
        return ""

    try:
        img = Image.open(image_path)
        # Just get center region (likely event popup)
        width, height = img.size
        center_region = img.crop((
            width // 4,
            height // 6,
            3 * width // 4,
            5 * height // 6
        ))

        center_region = center_region.convert('L')
        center_region = ImageOps.autocontrast(center_region)

        text = pytesseract.image_to_string(center_region, config=TESSERACT_CONFIG)
        return text.strip()[:500]  # Limit length
    except Exception:
        return ""


def record_decision(x: int, y: int):
    """Record a decision (click) with screenshot and OCR."""
    # Capture immediately
    screenshot_path = capture_screen_at_click(x, y)
    if not screenshot_path:
        return

    # Get screen dimensions
    try:
        img = Image.open(screenshot_path)
        screen_width, screen_height = img.size
    except:
        screen_width, screen_height = 1920, 1080

    # OCR the region around click
    region_text = ocr_region_around_click(screenshot_path, x, y)

    # OCR full screen (center, where popups appear)
    full_text = ocr_full_screen(screenshot_path)

    # Create decision record
    decision = Decision(
        timestamp=datetime.now().isoformat(),
        x=x,
        y=y,
        screen_width=screen_width,
        screen_height=screen_height,
        screenshot_path=str(screenshot_path),
        ocr_text=full_text,
        region_ocr=region_text
    )

    # Append to decisions file
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(DECISIONS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(decision), ensure_ascii=False) + "\n")

    # Log
    region_preview = region_text[:50].replace('\n', ' ') if region_text else "(no text)"
    print(f"[{decision.timestamp}] Click ({x}, {y}): {region_preview}...")


class ClickWatcher:
    """Watches for mouse clicks and records decisions."""

    def __init__(self):
        self.last_click_time = 0
        self.listener = None

    def on_click(self, x: int, y: int, button, pressed: bool):
        """Handle mouse click event."""
        if not pressed:  # Only on button press, not release
            return

        # Cooldown to avoid recording rapid clicks
        now = time.time()
        if now - self.last_click_time < CLICK_COOLDOWN:
            return
        self.last_click_time = now

        # Record the decision
        record_decision(int(x), int(y))

    def start(self):
        """Start watching for clicks."""
        if not HAS_PYNPUT:
            print("Error: pynput required. Install with: pip install pynput")
            sys.exit(1)

        print("🖱️  Click Watcher started")
        print(f"   Decisions file: {DECISIONS_FILE}")
        print(f"   Screenshots: {CLICK_SCREENSHOTS_DIR}")
        print(f"   Cooldown: {CLICK_COOLDOWN}s")
        print()
        print("Watching for clicks... (Ctrl+C to stop)")

        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

        try:
            self.listener.join()
        except KeyboardInterrupt:
            print("\nStopped.")

    def stop(self):
        """Stop watching."""
        if self.listener:
            self.listener.stop()


def get_recent_decisions(since_ts: float = 0, limit: int = 10) -> list[dict]:
    """Get recent decisions for Claude."""
    if not DECISIONS_FILE.exists():
        return []

    decisions = []
    with open(DECISIONS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line)
                ts = datetime.fromisoformat(d["timestamp"]).timestamp()
                if ts > since_ts:
                    decisions.append(d)
            except:
                continue

    # Return most recent, sorted by time
    decisions.sort(key=lambda d: d["timestamp"], reverse=True)
    return decisions[:limit]


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Click watcher for decision recording")
    parser.add_argument("--test", action="store_true", help="Test single capture at current mouse position")
    parser.add_argument("--recent", type=int, metavar="N", help="Show N recent decisions")

    args = parser.parse_args()

    if args.test:
        # Test capture at center of screen
        print("Test capture at (960, 540)...")
        record_decision(960, 540)
        print("Done.")

    elif args.recent:
        decisions = get_recent_decisions(limit=args.recent)
        for d in decisions:
            print(f"[{d['timestamp']}] ({d['x']}, {d['y']})")
            if d.get('region_ocr'):
                print(f"  Text: {d['region_ocr'][:100]}...")
            print()

    else:
        watcher = ClickWatcher()
        watcher.start()


if __name__ == "__main__":
    main()
