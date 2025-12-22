# telemetry — Implementation: Health snapshot and emitter

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## FILE MAP

| Responsibility | File |
|----------------|------|
| Health snapshot | `src/telemetry/health_snapshot_builder.py` |
| Overlay emitter | `src/telemetry/overlay_payload_emitter.py` |
| Structured logger | `src/telemetry/structured_logger.py` |

---

## DATA FLOW

1. Health snapshot builder aggregates metrics.
2. Overlay emitter sends compact payload.
3. Logger writes structured events.

---

## CONFIG

- `config/config.yaml`: overlay and health endpoint settings.

---

## NOTES

Keep overlay payload stable for UI consumption.
