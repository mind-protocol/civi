# Civ6 Living Narrator — Health: Global system signals

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## SIGNALS

| Signal | Target | Notes |
|--------|--------|-------|
| ingest_lag_ms | < 2000 | Tail within 2s of append |
| speech_rate_per_10_turns | 0-3 | Silence-first pacing |
| invalid_json_rate | < 0.05 | LLM JSON contract health |
| queue_depth | low | Audio backlog control |

---

## ALERTS

- ingest_lag_ms > 5000 for 3 intervals.
- speech_rate_per_10_turns spikes above threshold.
- invalid_json_rate exceeds 0.1.
