"""Build health snapshots for /health endpoint."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class HealthSnapshot:
    status: str
    ingest_lag_ms: int
    speech_rate_per_10_turns: float
    invalid_json_rate: float
    queue_depth: int


def build_health_snapshot(metrics: Dict[str, object]) -> HealthSnapshot:
    ingest_lag_ms = int(metrics.get("ingest_lag_ms", 0))
    speech_rate = float(metrics.get("speech_rate_per_10_turns", 0.0))
    invalid_rate = float(metrics.get("invalid_json_rate", 0.0))
    queue_depth = int(metrics.get("queue_depth", 0))

    status = "OK"
    if ingest_lag_ms > 5000 or invalid_rate > 0.1:
        status = "DEGRADED"

    return HealthSnapshot(
        status=status,
        ingest_lag_ms=ingest_lag_ms,
        speech_rate_per_10_turns=speech_rate,
        invalid_json_rate=invalid_rate,
        queue_depth=queue_depth,
    )
