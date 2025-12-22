"""Deduplicate and coalesce normalized events to reduce noise."""

from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Iterable, List, Optional, Tuple


class EventDeduplicator:
    def __init__(self, window_size: int = 128) -> None:
        self._window_size = window_size
        self._recent: Deque[str] = deque()
        self._recent_set = set()

    def _signature(self, event: Dict[str, object]) -> str:
        payload = event.get("payload") or {}
        entity_id = payload.get("entity_id") if isinstance(payload, dict) else None
        target_id = payload.get("target_id") if isinstance(payload, dict) else None
        return f"{event.get('event_type')}|{event.get('turn')}|{entity_id}|{target_id}"

    def is_duplicate(self, event: Dict[str, object]) -> bool:
        signature = self._signature(event)
        return signature in self._recent_set

    def remember(self, event: Dict[str, object]) -> None:
        signature = self._signature(event)
        if signature in self._recent_set:
            return
        self._recent.append(signature)
        self._recent_set.add(signature)
        if len(self._recent) > self._window_size:
            old = self._recent.popleft()
            self._recent_set.discard(old)


def _rules_from_types(coalesce_types: Optional[List[str]]) -> List[Dict[str, object]]:
    if not coalesce_types:
        return []
    return [{"event_type": event_type, "min_count": 2} for event_type in coalesce_types]


def coalesce_events(
    events: Iterable[Dict[str, object]],
    coalesce_types: Optional[List[str]] = None,
    rules: Optional[List[Dict[str, object]]] = None,
) -> List[Dict[str, object]]:
    rules = rules or _rules_from_types(coalesce_types)
    if not rules:
        return list(events)

    rules_by_type = {
        str(rule.get("event_type")): int(rule.get("min_count", 2)) for rule in rules
    }
    grouped: Dict[Tuple[int, str], List[Dict[str, object]]] = {}
    passthrough: List[Dict[str, object]] = []
    for event in events:
        event_type = event.get("event_type")
        if str(event_type) not in rules_by_type:
            passthrough.append(event)
            continue
        turn = int(event.get("turn") or 0)
        key = (turn, str(event_type))
        grouped.setdefault(key, []).append(event)

    coalesced: List[Dict[str, object]] = []
    for (turn, event_type), bucket in grouped.items():
        min_count = rules_by_type.get(event_type, 2)
        if len(bucket) < min_count:
            coalesced.extend(bucket)
            continue
        coalesced.append(
            {
                "event_type": f"COALESCED_{event_type}",
                "turn": turn,
                "timestamp": bucket[-1].get("timestamp"),
                "payload": {
                    "count": len(bucket),
                    "events": bucket,
                },
                "session_id": bucket[-1].get("session_id"),
            }
        )

    return passthrough + coalesced
