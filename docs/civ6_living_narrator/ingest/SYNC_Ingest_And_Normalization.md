# ingest — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Append-only JSONL intake from Civ 6 Lua mod.
- Tail reader tolerates partial lines and retries.

**What's still being designed:**
- Coalescing rules for minor events.
- Dedup signature format.

**What's proposed (v2+):**
- Multi-source ingest (mods, telemetry, overlay).

---

## CURRENT STATE

Baseline ingest implementation now exists with tailing, normalization, schema validation, and dedup/coalesce helpers plus tests for partial lines and rotation.

---

## IN PROGRESS

### Ingest invariants and schemas

- **Started:** 2025-12-21
- **By:** codex
- **Status:** in progress
- **Context:** Define minimal event schema, dedup signatures, and partial line handling.

---

## RECENT CHANGES

### 2025-12-21: Seed ingest module docs

- **What:** Added initial behaviors, algorithm, validation, implementation, and health notes.
- **Why:** Provide module boundaries before code work.
- **Files:** `docs/civ6_living_narrator/ingest/`
- **Struggles/Insights:** Keep JSONL partial handling explicit.

### 2025-12-21: Implement tailing, normalization, and dedup helpers

- **What:** Added a tail reader with partial-line buffering, a JSON parser/normalizer, and a dedup/coalesce helper plus tests.
- **Why:** Establish the ingest baseline described in the module docs and validation targets.
- **Files:** `src/ingest/civ6_jsonl_tail_reader.py`, `src/ingest/raw_event_parser_and_normalizer.py`, `src/ingest/event_deduplicator_and_coalescer.py`, `tests/test_parse_and_normalize_events.py`, `tests/test_windows_bridge_rotation_and_tail.py`
- **Struggles/Insights:** Rotation detection relies on size shrink or session id change.

### 2025-12-21: Add schema and coalescing configuration

- **What:** Added event schema YAML, schema loader, and configurable coalescing rules with tests.
- **Why:** The spec requires schema validation and configurable coalescing to reduce noise.
- **Files:** `config/event_schema.yaml`, `config/config.yaml`, `src/ingest/raw_event_parser_and_normalizer.py`, `src/ingest/event_deduplicator_and_coalescer.py`, `tests/test_parse_and_normalize_events.py`
- **Struggles/Insights:** YAML parser is minimal and supports only lists and simple maps.

---

## KNOWN ISSUES

### No schema validator yet

- **Severity:** medium
- **Symptom:** Unknown fields would pass through unbounded.
- **Suspected cause:** Schema not implemented.
- **Attempted:** None yet.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `.ngram/views/VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Baseline ingest implementation and tests are in place.

**What you need to understand:**
Ingest must tolerate partial JSONL lines, dedup across short windows, and coalesce noisy events.

**Watch out for:**
Do not lock the events file; use tailing with retry for partial lines.

**Open questions I had:**
Should coalescing be per-turn or per-time window?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Ingest now includes tailing, normalization, and dedup helpers with tests for partial lines and rotation.

**Decisions made:**
Append-only JSONL with partial-line tolerance is the base contract.

**Needs your input:**
Confirm event schema fields and coalescing rules.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: add strict schema enforcement and coalescing rule loading from config.

### Tests to Run

```bash
pytest tests/test_parse_and_normalize_events.py
pytest tests/test_windows_bridge_rotation_and_tail.py
```

### Immediate

- [ ] Draft event schema and dedup signature rules.
- [ ] Define coalescing config format.

### Later

- [ ] Add replay harness for JSONL traces.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:** Focused, early-stage.

**Threads I was holding:**
Partial line handling and session rotation interplay.

**Intuitions:**
Coalescing should be config-driven to avoid hardcoded logic.

**What I wish I'd known at the start:**
Exact event payload fields from the Lua mod.

---

## POINTERS

| What | Where |
|------|-------|
| Tail reader | `src/ingest/civ6_jsonl_tail_reader.py` |
| Event parser | `src/ingest/raw_event_parser_and_normalizer.py` |
| Dedup helper | `src/ingest/event_deduplicator_and_coalescer.py` |
