# llm_router — Health: Invalid rate, latency, cost

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## SIGNALS

| Signal | Target | Notes |
|--------|--------|-------|
| invalid_json_rate | < 0.05 | Repair needed too often if higher |
| repair_attempt_rate | low | Indicates prompt contract issues |
| router_latency_ms | < 2000 | End-to-end request time |
| token_cost_per_turn | within budget | Track API cost |

---

## ALERTS

- invalid_json_rate > 0.1 for 5 windows.
- router_latency_ms spikes above threshold.
