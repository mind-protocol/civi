"""Select mythic callbacks based on tag overlap or time gate."""

from __future__ import annotations

from typing import Iterable, Optional, Set

from moment_graph.moment_creator_and_merger import Moment


def _tag_overlap(tags_a: Set[str], tags_b: Set[str]) -> float:
    if not tags_a or not tags_b:
        return 0.0
    overlap = tags_a.intersection(tags_b)
    return len(overlap) / max(len(tags_a), len(tags_b))


def select_callback(
    moments: Iterable[Moment],
    current_turn: int,
    tags: Optional[Iterable[str]] = None,
    overlap_threshold: float = 0.5,
    time_gate: int = 15,
) -> Optional[Moment]:
    tag_set = set(tags or [])
    candidates = []
    for moment in moments:
        if not moment.is_myth:
            continue
        overlap = _tag_overlap(tag_set, moment.tags)
        time_ok = moment.last_callback_turn is None or (
            current_turn - moment.last_callback_turn >= time_gate
        )
        if overlap >= overlap_threshold or time_ok:
            candidates.append((moment.charge, overlap, moment))
    if not candidates:
        return None
    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    selected = candidates[0][2]
    selected.last_callback_turn = current_turn
    return selected
