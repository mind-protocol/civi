# ingest — Health: Ingest lag and error rates

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## SIGNALS

| Signal | Target | Notes |
|--------|--------|-------|
| ingest_lag_ms | < 2000 | Tail is within 2s of file append |
| invalid_jsonl_line_count | 0 steady | Spikes indicate malformed lines |
| dedup_drop_rate | < 0.3 | High rate suggests over-dedup |
| coalesce_count | baseline | Tracks noise reduction |

---

## ALERTS

- ingest_lag_ms > 5000 for 3 intervals.
- invalid_jsonl_line_count increases continuously.
