# decision_engine — Health: Speech rate and suppression reasons

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## SIGNALS

| Signal | Target | Notes |
|--------|--------|-------|
| speech_rate_per_10_turns | 0-3 | Higher indicates spam risk |
| speech_suppressed_count | tracked | Reasons: cooldown, budget, low_value |
| diversity_block_count | 0-1 | Consecutive leader blocks |

---

## ALERTS

- speech_rate_per_10_turns > 4 for 3 windows.
- low_value suppression spikes.
