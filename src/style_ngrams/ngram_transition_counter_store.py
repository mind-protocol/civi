"""Store n-gram transition counts by scope."""

from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Dict, Tuple


class NgramCounterStore:
    def __init__(self) -> None:
        self._counts: DefaultDict[str, DefaultDict[Tuple[str, str], int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self._totals: DefaultDict[str, DefaultDict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )

    def update(self, scope_key: str, prev_token: str, next_token: str) -> None:
        self._counts[scope_key][(prev_token, next_token)] += 1
        self._totals[scope_key][prev_token] += 1

    def counts_for(self, scope_key: str, prev_token: str) -> Dict[str, int]:
        result: Dict[str, int] = {}
        for (prev, nxt), count in self._counts[scope_key].items():
            if prev == prev_token:
                result[nxt] = count
        return result

    def total_for(self, scope_key: str, prev_token: str) -> int:
        return self._totals[scope_key].get(prev_token, 0)


def leader_scope(leader_id: str) -> str:
    return f"BY_LEADER:{leader_id}"


def phase_scope(phase: str) -> str:
    return f"BY_PHASE:{phase}"


def global_scope() -> str:
    return "GLOBAL"
