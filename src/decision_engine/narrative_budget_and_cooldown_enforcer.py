"""Budget and cooldown enforcement for narration selection."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class BudgetState:
    spoken_turns: List[Tuple[int, str]] = field(default_factory=list)
    last_spoken_turn: Dict[str, int] = field(default_factory=dict)


def is_budget_exceeded(turn: int, state: BudgetState, max_budget: int, window: int) -> bool:
    cutoff = turn - window + 1
    recent = [t for t, _ in state.spoken_turns if t >= cutoff]
    return len(recent) >= max_budget


def is_cooldown_active(
    turn: int, state: BudgetState, speaker_key: str, cooldown_turns: int
) -> bool:
    last_turn = state.last_spoken_turn.get(speaker_key)
    if last_turn is None:
        return False
    return (turn - last_turn) <= cooldown_turns


def record_spoken(turn: int, state: BudgetState, speaker_key: str) -> None:
    state.spoken_turns.append((turn, speaker_key))
    state.last_spoken_turn[speaker_key] = turn
