"""Build a context pack and apply truncation rules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ContextPack:
    history: List[Dict[str, Any]]
    signals: List[Dict[str, Any]]
    max_tokens: int


def truncate_context(pack: ContextPack, max_history: int, max_signals: int) -> ContextPack:
    history = pack.history[-max_history:] if max_history > 0 else []
    signals = pack.signals[:max_signals] if max_signals > 0 else []
    return ContextPack(history=history, signals=signals, max_tokens=pack.max_tokens)
