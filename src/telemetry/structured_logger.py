"""Emit structured log lines for pipeline events."""

from __future__ import annotations

import json
from typing import Dict


def format_log(event: str, payload: Dict[str, object]) -> str:
    return json.dumps({"event": event, "payload": payload}, separators=(",", ":"))
