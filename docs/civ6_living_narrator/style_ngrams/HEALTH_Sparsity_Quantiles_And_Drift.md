# style_ngrams — Health: Sparsity, quantiles, drift

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## SIGNALS

| Signal | Target | Notes |
|--------|--------|-------|
| sparse_scope_rate | < 0.3 | Frequency of backoff needed |
| any_token_rate | stable | Too high indicates over-compression |
| surprise_quantile_shift | low | Detects drift over long sessions |

---

## ALERTS

- sparse_scope_rate > 0.6 for 3 windows.
- surprise_quantile_shift spikes above threshold.
