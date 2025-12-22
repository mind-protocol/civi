"""Generate challenge offers from catalog and current state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


@dataclass(frozen=True)
class ChallengeOffer:
    challenge_id: str
    title: str
    conditions: str
    refusal_line: str


def choose_challenge(
    catalog: Iterable[Dict[str, str]],
    used_ids: Optional[Iterable[str]] = None,
) -> Optional[ChallengeOffer]:
    used = set(used_ids or [])
    for challenge in catalog:
        if challenge.get("id") in used:
            continue
        if not challenge.get("refusal_line"):
            continue
        return ChallengeOffer(
            challenge_id=challenge.get("id", ""),
            title=challenge.get("title", ""),
            conditions=challenge.get("conditions", ""),
            refusal_line=challenge.get("refusal_line", ""),
        )
    return None
