# persistence — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- SQLite-backed storage for counts, moments, challenges.
- Schema migrations tracked in one place.

**What's still being designed:**
- Retention policy and cleanup routines.

**What's proposed (v2+):**
- Remote storage for long sessions.

---

## CURRENT STATE

Persistence now includes a SQLite schema migrator and basic adapters with tests.

---

## IN PROGRESS

### Store schema and adapters

- **Started:** 2025-12-21
- **By:** codex
- **Status:** in progress
- **Context:** Define tables for counts, moments, challenges, and migrations.

---

## RECENT CHANGES

### 2025-12-21: Seed persistence docs

- **What:** Added initial objectives, algorithm, validation, implementation, and health notes.
- **Why:** Document storage boundaries before code.
- **Files:** `docs/civ6_living_narrator/persistence/`
- **Struggles/Insights:** Keep schema minimal and clear.

### 2025-12-21: Implement SQLite schema and adapters

- **What:** Added schema migrator, adapters for counts/moments/challenges, and tests.
- **Why:** Provide a durable local store for core state.
- **Files:** `src/persistence/sqlite_store_schema_and_migrator.py`, `src/persistence/store_adapters_for_counts_moments_challenges.py`, `tests/test_persistence_schema_and_adapters.py`
- **Struggles/Insights:** Migration table must be initialized before inserts.

### 2025-12-21: Add session pruning helper

- **What:** Added per-session prune helper and test coverage.
- **Why:** Retention and session scoping require explicit deletion paths.
- **Files:** `src/persistence/store_adapters_for_counts_moments_challenges.py`, `tests/test_persistence_schema_and_adapters.py`
- **Struggles/Insights:** Pruning currently covers moments and challenges only.

---

## KNOWN ISSUES

### Migration strategy undefined

- **Severity:** medium
- **Symptom:** No version tracking for schema updates.
- **Suspected cause:** Schema not drafted.
- **Attempted:** None yet.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `.ngram/views/VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** SQLite schema and adapter baseline with tests are in place.

**What you need to understand:**
Schema should support counts, moments, challenges with minimal joins.

**Watch out for:**
Keep migrations forward-only.

**Open questions I had:**
Should stores be per-session or global?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
SQLite schema migrator and adapters now exist with tests.

**Decisions made:**
Use SQLite with explicit migrations.

**Needs your input:**
Confirm retention policy and session scoping.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: add retention pruning for counts and migration-based retention windows.

### Tests to Run

```bash
pytest tests/test_persistence_schema_and_adapters.py
```

### Immediate

- [ ] Define schema tables and migration format.
- [ ] Define retention policy.

### Later

- [ ] Add backup/restore tooling.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:** Focused, early-stage.

**Threads I was holding:**
Balance schema normalization with query simplicity.

**Intuitions:**
Per-session scoping keeps size manageable.

**What I wish I'd known at the start:**
Expected storage volume per hour.

---

## POINTERS

| What | Where |
|------|-------|
| Schema stub | `src/persistence/sqlite_store_schema_and_migrator.py` |
| Adapter stub | `src/persistence/store_adapters_for_counts_moments_challenges.py` |
