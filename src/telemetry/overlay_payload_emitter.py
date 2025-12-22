"""Emit overlay payloads for debugging."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class OverlayPayload:
    last_event: Optional[str]
    last_spoken: Optional[str]
    active_challenge: Optional[str]
    speech_budget_remaining: int
    ingest_lag_ms: int
    queue_depth: int


def build_overlay_payload(
    last_event: Optional[str],
    last_spoken: Optional[str],
    active_challenge: Optional[str],
    speech_budget_remaining: int,
    ingest_lag_ms: int,
    queue_depth: int,
) -> OverlayPayload:
    return OverlayPayload(
        last_event=last_event,
        last_spoken=last_spoken,
        active_challenge=active_challenge,
        speech_budget_remaining=speech_budget_remaining,
        ingest_lag_ms=ingest_lag_ms,
        queue_depth=queue_depth,
    )
