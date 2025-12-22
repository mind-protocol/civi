# win_wsl_bridge — Health: Restart survivability

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## SIGNALS

| Signal | Target | Notes |
|--------|--------|-------|
| restart_recover_time_ms | < 2000 | Time to resume tail after restart |
| session_mismatch_count | 0 steady | Non-zero indicates rotation bugs |
| bridge_path_errors | 0 steady | Missing folder or invalid paths |

---

## ALERTS

- restart_recover_time_ms > 5000 for 2 restarts.
- session_mismatch_count increases across turns.
