# telemetry — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Health snapshot builder emits core signals.
- Overlay payload includes last event, last spoken, budget, queue depth.

**What's still being designed:**
- Health endpoint contract.
- Overlay rendering details.

**What's proposed (v2+):**
- Remote telemetry streaming.

---

## CURRENT STATE

Telemetry now has health snapshot, overlay payload, and structured log helpers with tests.

---

## IN PROGRESS

### Health signals and overlay payload

- **Started:** 2025-12-21
- **By:** codex
- **Status:** in progress
- **Context:** Define health snapshot schema and overlay payload fields.

---

## RECENT CHANGES

### 2025-12-21: Seed telemetry docs

- **What:** Added initial objectives, algorithm, validation, implementation, and health notes.
- **Why:** Document observability boundaries before code.
- **Files:** `docs/civ6_living_narrator/telemetry/`
- **Struggles/Insights:** Keep overlay minimal and informative.

### 2025-12-21: Implement telemetry helpers

- **What:** Added health snapshot builder, overlay payload builder, structured logger, and tests.
- **Why:** Provide minimal observability for pacing, ingest lag, and queue depth.
- **Files:** `src/telemetry/health_snapshot_builder.py`, `src/telemetry/overlay_payload_emitter.py`, `src/telemetry/structured_logger.py`, `tests/test_telemetry_health_and_overlay.py`
- **Struggles/Insights:** Keep alert logic minimal (OK/DEGRADED).

---

## KNOWN ISSUES

### Health endpoint undefined

- **Severity:** medium
- **Symptom:** No contract for /health response.
- **Suspected cause:** Not designed yet.
- **Attempted:** None yet.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `.ngram/views/VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Telemetry helpers and tests are in place.

**What you need to understand:**
Overlay should surface last event, last spoken, active challenge, budget, lag, queue depth.

**Watch out for:**
Avoid heavy UI in v1.

**Open questions I had:**
Should health endpoint be JSON only or also plain text?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Telemetry helpers now produce health snapshots and overlay payloads with tests.

**Decisions made:**
Minimal overlay and /health endpoint are required.

**Needs your input:**
Confirm endpoint format and overlay delivery.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: implement /health endpoint wiring and overlay transport.

### Tests to Run

```bash
pytest tests/test_telemetry_health_and_overlay.py
```

### Immediate

- [ ] Define /health response schema.
- [ ] Define overlay payload fields.

### Later

- [ ] Add structured logging for pipeline stages.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:** Focused, early-stage.

**Threads I was holding:**
Need to keep overlay useful without clutter.

**Intuitions:**
Health snapshot should reflect suppression reasons and lag.

**What I wish I'd known at the start:**
Preferred overlay rendering method on Windows.

---

## POINTERS

| What | Where |
|------|-------|
| Health snapshot stub | `src/telemetry/health_snapshot_builder.py` |
| Overlay emitter stub | `src/telemetry/overlay_payload_emitter.py` |
| Logger stub | `src/telemetry/structured_logger.py` |
