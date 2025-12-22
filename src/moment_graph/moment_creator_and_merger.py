"""Create or merge moments from normalized events."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set, Tuple


@dataclass
class Moment:
    moment_id: str
    tags: Set[str]
    charge: float
    turn_created: int
    last_turn: int
    is_myth: bool = False
    last_callback_turn: Optional[int] = None
    data: Dict[str, object] = field(default_factory=dict)


def _tag_overlap(tags_a: Set[str], tags_b: Set[str]) -> float:
    if not tags_a or not tags_b:
        return 0.0
    overlap = tags_a.intersection(tags_b)
    return len(overlap) / max(len(tags_a), len(tags_b))


def create_or_merge_moment(
    moments: List[Moment],
    tags: Iterable[str],
    importance: float,
    turn: int,
    merge_window: int,
    overlap_threshold: float,
    data: Optional[Dict[str, object]] = None,
) -> Moment:
    tag_set = set(tags)
    for moment in moments:
        if turn - moment.last_turn > merge_window:
            continue
        overlap = _tag_overlap(tag_set, moment.tags)
        if overlap >= overlap_threshold:
            moment.tags.update(tag_set)
            moment.charge += importance
            moment.last_turn = turn
            if data:
                moment.data.update(data)
            return moment

    moment_id = f"m{len(moments) + 1}"
    moment = Moment(
        moment_id=moment_id,
        tags=tag_set,
        charge=importance,
        turn_created=turn,
        last_turn=turn,
        data=data or {},
    )
    moments.append(moment)
    return moment
