# moment_graph — Health: Moment count and charge distribution

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## SIGNALS

| Signal | Target | Notes |
|--------|--------|-------|
| moment_count | <= max_moments | Keep memory sparse |
| myth_count | low | Myth should be rare |
| average_charge | stable | Detect drift or decay issues |

---

## ALERTS

- moment_count exceeds max_moments for 3 turns.
- myth_count spikes above threshold.
