#!/usr/bin/env python3
"""
Screen capture launcher for Living Narrator.
Runs the PowerShell capture script on Windows from WSL.
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
PS_SCRIPT = SCRIPT_DIR / "capture_screen.ps1"
WIN_SCREENSHOT_DIR = Path("/mnt/c/Temp/NarratorScreenshots")
WIN_SCREENSHOT_DIR_STR = "C:\\Temp\\NarratorScreenshots"


def capture_once() -> Path | None:
    """Take a single screenshot and return the path (WSL path)."""
    # Ensure screenshot dir exists
    WIN_SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    # Convert script path to Windows path
    ps_script_win = str(PS_SCRIPT).replace("/mnt/c", "C:").replace("/", "\\")

    try:
        result = subprocess.run(
            [
                "powershell.exe",
                "-ExecutionPolicy", "Bypass",
                "-File", ps_script_win,
                "-Once",
                "-OutputDir", WIN_SCREENSHOT_DIR_STR
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            # Find the latest screenshot
            screenshots = sorted(WIN_SCREENSHOT_DIR.glob("screen_*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
            if screenshots:
                print(f"Captured: {screenshots[0]}")
                return screenshots[0]
        else:
            print(f"Capture failed: {result.stderr}", file=sys.stderr)

    except subprocess.TimeoutExpired:
        print("Screenshot capture timed out", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

    return None


def get_latest_screenshot() -> Path | None:
    """Get the most recent screenshot without capturing a new one."""
    if not WIN_SCREENSHOT_DIR.exists():
        return None

    screenshots = sorted(
        WIN_SCREENSHOT_DIR.glob("screen_*.png"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    return screenshots[0] if screenshots else None


def start_continuous(interval: int = 60) -> subprocess.Popen:
    """Start continuous capture in background."""
    ps_script_win = str(PS_SCRIPT).replace("/mnt/c", "C:").replace("/", "\\")

    proc = subprocess.Popen(
        [
            "powershell.exe",
            "-ExecutionPolicy", "Bypass",
            "-File", ps_script_win,
            "-IntervalSeconds", str(interval),
            "-OutputDir", WIN_SCREENSHOT_DIR_STR
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print(f"Started continuous capture (PID: {proc.pid}, interval: {interval}s)")
    return proc


def is_fresh(path: Path, max_age_seconds: int = 120) -> bool:
    """Check if a screenshot is recent enough to be useful."""
    if not path or not path.exists():
        return False

    age = datetime.now().timestamp() - path.stat().st_mtime
    return age < max_age_seconds


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Screen capture for Living Narrator")
    parser.add_argument("--once", action="store_true", help="Take a single screenshot")
    parser.add_argument("--latest", action="store_true", help="Print path to latest screenshot")
    parser.add_argument("--start", action="store_true", help="Start continuous capture")
    parser.add_argument("--interval", type=int, default=60, help="Capture interval in seconds")
    parser.add_argument("--check-fresh", type=int, metavar="SECONDS",
                       help="Check if latest screenshot is within N seconds")

    args = parser.parse_args()

    if args.once:
        path = capture_once()
        if path:
            print(path)
            sys.exit(0)
        sys.exit(1)

    elif args.latest:
        path = get_latest_screenshot()
        if path:
            print(path)
            sys.exit(0)
        print("No screenshots found", file=sys.stderr)
        sys.exit(1)

    elif args.check_fresh:
        path = get_latest_screenshot()
        if is_fresh(path, args.check_fresh):
            print(path)
            sys.exit(0)
        sys.exit(1)

    elif args.start:
        proc = start_continuous(args.interval)
        try:
            proc.wait()
        except KeyboardInterrupt:
            proc.terminate()
            print("\nStopped")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
