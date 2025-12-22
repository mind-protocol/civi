# persistence — Algorithm: Schema, migrate, query

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Persistence_Schema_And_Adapters.md
THIS:           ./ALGORITHM_Schema_Migrate_Query.md
VALIDATION:     ./VALIDATION_Schema_Integrity_And_Retention.md
IMPLEMENTATION: ./IMPLEMENTATION_Sqlite_Schema_And_Adapters.md
HEALTH:         ./HEALTH_Db_Size_And_Error_Rate.md
SYNC:           ./SYNC_Persistence_Stores_And_Migrations.md
```

---

## OVERVIEW

Apply migrations, then serve reads/writes through adapters.

---

## STEPS

1. On startup, open SQLite database file.
2. Apply pending migrations in order.
3. Use adapters for reads and writes by domain.
4. Periodically prune rows outside retention window.

---

## OUTPUTS

- Stable schema with version tracking.
- Stored counts, moments, challenges per session.
