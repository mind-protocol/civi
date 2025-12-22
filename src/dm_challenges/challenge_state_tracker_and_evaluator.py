"""Track active challenges and evaluate completion/refusal."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ChallengeState:
    active_id: Optional[str] = None
    status: str = "none"
    last_updated_turn: Optional[int] = None


def activate_challenge(state: ChallengeState, challenge_id: str, turn: int) -> ChallengeState:
    return ChallengeState(active_id=challenge_id, status="active", last_updated_turn=turn)


def mark_completed(state: ChallengeState, turn: int) -> ChallengeState:
    return ChallengeState(active_id=state.active_id, status="completed", last_updated_turn=turn)


def mark_refused(state: ChallengeState, turn: int) -> ChallengeState:
    return ChallengeState(active_id=state.active_id, status="refused", last_updated_turn=turn)


def can_offer(state: ChallengeState) -> bool:
    return state.active_id is None or state.status in {"completed", "refused"}
