import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from ingest.raw_event_parser_and_normalizer import (
    load_event_schema,
    normalize_event,
    parse_json_line,
)
from ingest.event_deduplicator_and_coalescer import EventDeduplicator, coalesce_events


def test_parse_and_normalize_event():
    raw = {"event_type": "CITY_CAPTURED", "turn": 10, "timestamp": 123.0}
    normalized = normalize_event(raw)
    assert normalized is not None
    assert normalized["event_type"] == "CITY_CAPTURED"
    assert normalized["turn"] == 10
    assert normalized["timestamp"] == 123.0
    assert normalized["payload"] == raw


def test_normalize_missing_fields():
    raw = {"timestamp": 123.0}
    assert normalize_event(raw) is None


def test_parse_json_line():
    line = '{"event_type": "TURN", "turn": 1}'
    parsed = parse_json_line(line)
    assert parsed["event_type"] == "TURN"


def test_deduplicator_drops_duplicates():
    dedup = EventDeduplicator(window_size=4)
    event = {"event_type": "TURN", "turn": 1, "payload": {"entity_id": 1}}
    assert not dedup.is_duplicate(event)
    dedup.remember(event)
    assert dedup.is_duplicate(event)


def test_schema_loads_unknown_fields():
    schema = load_event_schema(str(ROOT / "config" / "event_schema.yaml"))
    raw = {"event_type": "TURN", "turn": 2, "new_field": 42}
    normalized = normalize_event(raw, schema=schema)
    assert normalized is not None
    assert "_unknown_fields" in normalized["payload"]
    assert "new_field" in normalized["payload"]["_unknown_fields"]


def test_coalesce_rules_respect_min_count():
    events = [
        {"event_type": "UNIT_KILL_MINOR", "turn": 1, "timestamp": 1, "payload": {}},
        {"event_type": "UNIT_KILL_MINOR", "turn": 1, "timestamp": 2, "payload": {}},
        {"event_type": "UNIT_KILL_MINOR", "turn": 1, "timestamp": 3, "payload": {}},
    ]
    rules = [{"event_type": "UNIT_KILL_MINOR", "min_count": 3}]
    result = coalesce_events(events, rules=rules)
    assert len(result) == 1
    assert result[0]["event_type"] == "COALESCED_UNIT_KILL_MINOR"
