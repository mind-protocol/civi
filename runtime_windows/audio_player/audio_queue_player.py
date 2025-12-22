"""Simple in-process audio queue stub for Windows runtime."""

from __future__ import annotations

from dataclasses import dataclass
import subprocess
import shutil
import logging
import threading
import time
from typing import List, Optional

logger = logging.getLogger("audio_queue")


@dataclass
class AudioItem:
    path: str
    voice: Optional[str] = None


class AudioQueue:
    def __init__(self):
        self.queue: List[AudioItem] = []
        self.current: Optional[AudioItem] = None
        self.last_played: Optional[AudioItem] = None
        self._stop_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start the background worker thread."""
        if self._worker_thread is None or not self._worker_thread.is_alive():
            self._stop_event.clear()
            self._worker_thread = threading.Thread(target=self._process_queue, daemon=True)
            self._worker_thread.start()

    def enqueue(self, item: AudioItem) -> None:
        logger.info(f"Enqueued audio: {item.path}")
        self.queue.append(item)

    def next_item(self) -> Optional[AudioItem]:
        """Get next item from queue (for sync/test usage)."""
        if self.queue:
            self.current = self.queue.pop(0)
            self.last_played = self.current
            return self.current
        self.current = None
        return None

    def replay(self) -> Optional[AudioItem]:
        """Replay the last played item."""
        if self.last_played:
            self.current = self.last_played
            return self.current
        return None

    def _process_queue(self) -> None:
        """Background loop to play items sequentially."""
        while not self._stop_event.is_set():
            if self.queue:
                item = self.next_item()
                if item:
                    self._play_item(item)
            else:
                time.sleep(0.1)

    def _play_item(self, item: AudioItem) -> bool:
        """Play the audio item using available system tools (blocking call)."""
        logger.info(f"Playing audio: {item.path}")

        # Try ffplay first
        if shutil.which("ffplay"):
            try:
                subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", item.path], check=True)
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"ffplay failed: {e}")

        # Fallback to mpg123
        if shutil.which("mpg123"):
            try:
                subprocess.run(["mpg123", "-q", item.path], check=True)
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"mpg123 failed: {e}")

        logger.error("No suitable audio player found (ffplay or mpg123)")
        return False

    def stop(self) -> None:
        self._stop_event.set()
        self.queue.clear()
        self.current = None
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=1.0)
