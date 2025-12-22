# telemetry — Health: Overlay and log rates

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## SIGNALS

| Signal | Target | Notes |
|--------|--------|-------|
| overlay_emit_rate | <= 1 per turn | Avoid spam |
| health_status | OK/DEGRADED | Derived from alerts |
| log_error_rate | 0 | Structured log errors |

---

## ALERTS

- overlay_emit_rate exceeds limit.
- log_error_rate spikes.
