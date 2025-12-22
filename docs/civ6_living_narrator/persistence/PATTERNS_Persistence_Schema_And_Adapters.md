# persistence — Patterns: Schema and adapters

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Persistence_Schema_And_Adapters.md
ALGORITHM:      ./ALGORITHM_Schema_Migrate_Query.md
VALIDATION:     ./VALIDATION_Schema_Integrity_And_Retention.md
IMPLEMENTATION: ./IMPLEMENTATION_Sqlite_Schema_And_Adapters.md
HEALTH:         ./HEALTH_Db_Size_And_Error_Rate.md
SYNC:           ./SYNC_Persistence_Stores_And_Migrations.md
```

---

## THE PROBLEM

We need a durable local store for counts, moments, and challenges without a heavy dependency.

---

## THE PATTERN

- Use SQLite with explicit schema migrations.
- Keep tables minimal and read-friendly.
- Provide adapters per domain object.

---

## PRINCIPLES

### Principle 1: Minimal schema

Only store what the pipeline needs.

### Principle 2: Forward-only migrations

Schema changes append new migrations, never rewrite history.

### Principle 3: Session-aware storage

Store session id on rows to enable pruning.
