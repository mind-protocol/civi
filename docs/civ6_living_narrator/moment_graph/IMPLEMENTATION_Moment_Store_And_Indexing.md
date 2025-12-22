# moment_graph — Implementation: Moment store and indexing

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## FILE MAP

| Responsibility | File |
|----------------|------|
| Moment creation and merge | `src/moment_graph/moment_creator_and_merger.py` |
| Lifecycle and decay | `src/moment_graph/moment_lifecycle_promoter_and_decayer.py` |
| Query and callback selection | `src/moment_graph/moment_query_and_callback_selector.py` |

---

## DATA FLOW

1. Event stream feeds moment creator.
2. Lifecycle updater adjusts charge and myth status.
3. Query selector returns callback candidates with refs.

---

## CONFIG

- `config/config.yaml`: thresholds for create, merge, promote, decay, callback gate.

---

## NOTES

Moment storage should allow efficient tag overlap queries.
