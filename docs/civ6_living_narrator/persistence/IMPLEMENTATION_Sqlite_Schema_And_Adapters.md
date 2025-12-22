# persistence — Implementation: SQLite schema and adapters

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## FILE MAP

| Responsibility | File |
|----------------|------|
| Schema + migrations | `src/persistence/sqlite_store_schema_and_migrator.py` |
| Domain adapters | `src/persistence/store_adapters_for_counts_moments_challenges.py` |

---

## SCHEMA SUMMARY

- schema_version(version INTEGER)
- moments(moment_id TEXT PRIMARY KEY, session_id TEXT, tags TEXT, charge REAL, is_myth INTEGER, last_turn INTEGER)
- counts(scope TEXT, prev_token TEXT, next_token TEXT, count INTEGER)
- challenges(challenge_id TEXT PRIMARY KEY, session_id TEXT, status TEXT, last_updated INTEGER)

---

## DATA FLOW

1. Schema migrator sets up tables.
2. Adapters read/write per domain.
3. Retention job prunes old rows or per-session data.

---

## CONFIG

- `config/config.yaml`: database path, retention window.

---

## NOTES

Keep schema minimal to avoid migration churn.
