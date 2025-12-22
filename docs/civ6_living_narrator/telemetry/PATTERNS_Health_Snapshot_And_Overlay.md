# telemetry — Patterns: Health snapshot and overlay

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Health_Snapshot_And_Overlay.md
ALGORITHM:      ./ALGORITHM_Emit_Health_And_Overlay.md
VALIDATION:     ./VALIDATION_Health_Schema_And_Alerts.md
IMPLEMENTATION: ./IMPLEMENTATION_Health_Snapshot_And_Emitter.md
HEALTH:         ./HEALTH_Overlay_And_Log_Rates.md
SYNC:           ./SYNC_Telemetry_Health_And_Overlay.md
```

---

## THE PROBLEM

The system needs observability without overwhelming the user.

---

## THE PATTERN

- Build a minimal health snapshot each tick.
- Emit overlay payload for real-time debugging.
- Use structured logging for postmortems.

---

## PRINCIPLES

### Principle 1: Minimal payload

Only include what helps debug pacing and ingest.

### Principle 2: Human-readable

Overlay and logs should be interpretable without tooling.
