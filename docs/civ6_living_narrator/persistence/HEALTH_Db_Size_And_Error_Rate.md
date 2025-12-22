# persistence — Health: DB size and error rate

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## SIGNALS

| Signal | Target | Notes |
|--------|--------|-------|
| db_size_mb | steady | Growth indicates retention issues |
| db_error_rate | 0 | Non-zero indicates write/read failures |
| migration_failures | 0 | Detect schema issues |

---

## ALERTS

- db_size_mb grows above threshold.
- db_error_rate spikes.
