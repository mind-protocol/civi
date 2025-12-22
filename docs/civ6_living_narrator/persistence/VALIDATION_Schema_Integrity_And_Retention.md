# persistence — Validation: Schema integrity and retention

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
THIS:           ./VALIDATION_Schema_Integrity_And_Retention.md
IMPLEMENTATION: ./IMPLEMENTATION_Sqlite_Schema_And_Adapters.md
HEALTH:         ./HEALTH_Db_Size_And_Error_Rate.md
SYNC:           ./SYNC_Persistence_Stores_And_Migrations.md
```

---

## INVARIANTS

### V1: Schema version tracked

```
Schema_version table records latest migration
```

**Checked by:** `test_persistence_schema_and_adapters.py`

### V2: Retention applied

```
Rows older than retention window are pruned
```

**Checked by:** `test_persistence_schema_and_adapters.py`

---

## VERIFICATION PROCEDURE

```bash
# TODO: add persistence tests
```
