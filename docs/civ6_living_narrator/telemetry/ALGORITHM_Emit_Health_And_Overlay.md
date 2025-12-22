# telemetry — Algorithm: Emit health and overlay

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Health_Snapshot_And_Overlay.md
THIS:           ./ALGORITHM_Emit_Health_And_Overlay.md
VALIDATION:     ./VALIDATION_Health_Schema_And_Alerts.md
IMPLEMENTATION: ./IMPLEMENTATION_Health_Snapshot_And_Emitter.md
HEALTH:         ./HEALTH_Overlay_And_Log_Rates.md
SYNC:           ./SYNC_Telemetry_Health_And_Overlay.md
```

---

## OVERVIEW

Collect metrics from ingest, decision engine, and audio, then emit a compact snapshot.

---

## STEPS

1. Pull latest metrics (lag, budget, cooldown, queue depth).
2. Assemble health snapshot payload.
3. Emit overlay payload for UI/debug.
4. Write structured log entry.

---

## OUTPUTS

- /health JSON response.
- Overlay payload message.
- Structured log line.
