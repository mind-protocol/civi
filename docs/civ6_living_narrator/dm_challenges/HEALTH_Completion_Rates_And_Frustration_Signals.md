# dm_challenges — Health: Completion rates and frustration signals

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## SIGNALS

| Signal | Target | Notes |
|--------|--------|-------|
| challenge_completion_rate | stable | Low rate indicates frustration |
| refusal_rate | low | High refusal may indicate mis-tuned challenges |
| reminder_count | low | Too many reminders break pacing |

---

## ALERTS

- refusal_rate spikes above threshold.
- reminder_count exceeds limit per 10 turns.
