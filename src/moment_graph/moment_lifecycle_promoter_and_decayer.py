"""Promote moments to myth and decay charges over time."""

from __future__ import annotations

from typing import List

from moment_graph.moment_creator_and_merger import Moment


def promote_and_decay(
    moments: List[Moment],
    current_turn: int,
    promote_threshold: float,
    decay_per_turn: float,
    decay_floor: float,
) -> List[Moment]:
    updated: List[Moment] = []
    for moment in moments:
        turns_since = max(0, current_turn - moment.last_turn)
        moment.charge -= turns_since * decay_per_turn
        if moment.charge < decay_floor:
            continue
        if moment.charge >= promote_threshold:
            moment.is_myth = True
        updated.append(moment)
    return updated
