"""Launcher contracts for session id and ports."""

from __future__ import annotations

import os
from typing import Optional


SESSION_ID_ENV = "CIV6_LIVING_NARRATOR_SESSION_ID"
BRIDGE_ROOT_ENV = "CIV6_LIVING_NARRATOR_BRIDGE_ROOT"


def read_session_id(fallback: Optional[str] = None) -> Optional[str]:
    return os.environ.get(SESSION_ID_ENV, fallback)


def read_bridge_root(fallback: Optional[str] = None) -> Optional[str]:
    return os.environ.get(BRIDGE_ROOT_ENV, fallback)
