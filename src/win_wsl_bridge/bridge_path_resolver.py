"""Resolve bridge paths across Windows and WSL."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class BridgePaths:
    windows_root: str
    wsl_root: str
    events_dir: str

    def windows_session_file(self, session_id: str) -> str:
        return os.path.join(self.windows_root, "events", f"events_{session_id}.jsonl")

    def wsl_session_file(self, session_id: str) -> str:
        return os.path.join(self.wsl_root, "events", f"events_{session_id}.jsonl")


def resolve_bridge_paths(windows_root: str, wsl_root: str) -> BridgePaths:
    return BridgePaths(windows_root=windows_root, wsl_root=wsl_root, events_dir="events")
