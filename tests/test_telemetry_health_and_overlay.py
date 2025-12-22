import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from telemetry.health_snapshot_builder import build_health_snapshot
from telemetry.overlay_payload_emitter import build_overlay_payload
from telemetry.structured_logger import format_log


def test_health_snapshot_ok():
    snapshot = build_health_snapshot(
        {"ingest_lag_ms": 100, "speech_rate_per_10_turns": 1, "invalid_json_rate": 0.0, "queue_depth": 0}
    )
    assert snapshot.status == "OK"


def test_health_snapshot_degraded():
    snapshot = build_health_snapshot(
        {"ingest_lag_ms": 6000, "speech_rate_per_10_turns": 1, "invalid_json_rate": 0.0, "queue_depth": 0}
    )
    assert snapshot.status == "DEGRADED"


def test_overlay_payload_builder():
    payload = build_overlay_payload("e1", "s1", "c1", 2, 100, 1)
    assert payload.last_event == "e1"
    assert payload.queue_depth == 1


def test_structured_logger_format():
    line = format_log("event", {"a": 1})
    assert line == '{"event":"event","payload":{"a":1}}'
