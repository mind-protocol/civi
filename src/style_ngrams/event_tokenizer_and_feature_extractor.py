"""Tokenize events for style n-gram tracking."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, Tuple


@dataclass(frozen=True)
class TokenizationResult:
    token: str
    leader_id: Optional[str]
    phase: Optional[str]


def _compress_token(token: str, known_tokens: Optional[Set[str]] = None) -> str:
    if known_tokens is None:
        return token
    return token if token in known_tokens else "::ANY"


def tokenize_event(
    event: Dict[str, object],
    token_map: Optional[Dict[str, str]] = None,
    known_tokens: Optional[Set[str]] = None,
) -> TokenizationResult:
    raw_token = str(event.get("event_type") or "UNKNOWN")
    mapped = token_map.get(raw_token, raw_token) if token_map else raw_token
    token = _compress_token(mapped, known_tokens)
    leader_id = event.get("leader_id")
    phase = event.get("phase")
    return TokenizationResult(token=token, leader_id=str(leader_id) if leader_id else None, phase=str(phase) if phase else None)
