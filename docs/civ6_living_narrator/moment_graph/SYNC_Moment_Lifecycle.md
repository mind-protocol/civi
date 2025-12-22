# moment_graph — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Moments are created from events and can become mythic.
- Callbacks require explicit moment_refs.

**What's still being designed:**
- Promotion and decay thresholds.
- Tag overlap rules for callbacks.

**What's proposed (v2+):**
- Multi-turn myth arcs and leader-specific memory.

---

## CURRENT STATE

Moment graph now has baseline creation/merge, promotion/decay, and callback selection helpers with tests.

---

## IN PROGRESS

### Moment lifecycle rules

- **Started:** 2025-12-21
- **By:** codex
- **Status:** in progress
- **Context:** Define create, merge, promote, decay, and myth rules.

---

## RECENT CHANGES

### 2025-12-21: Seed moment_graph docs

- **What:** Added initial objectives, behaviors, algorithm, validation, implementation, and health notes.
- **Why:** Capture memory and mythification boundaries.
- **Files:** `docs/civ6_living_narrator/moment_graph/`
- **Struggles/Insights:** Keep moment counts low to avoid noise.

### 2025-12-21: Implement moment lifecycle helpers

- **What:** Added moment creation/merge, promotion/decay, callback selection, and tests for lifecycle invariants.
- **Why:** Establish myth promotion and callback rules required by the spec.
- **Files:** `src/moment_graph/moment_creator_and_merger.py`, `src/moment_graph/moment_lifecycle_promoter_and_decayer.py`, `src/moment_graph/moment_query_and_callback_selector.py`, `tests/test_moment_lifecycle_rules.py`, `config/config.yaml`
- **Struggles/Insights:** Callbacks rely on both tag overlap and time gate.

---

## KNOWN ISSUES

### Promotion thresholds undefined

- **Severity:** medium
- **Symptom:** No thresholds for myth promotion yet.
- **Suspected cause:** Requires event taxonomy.
- **Attempted:** None yet.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `.ngram/views/VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Baseline lifecycle implementation and tests are in place.

**What you need to understand:**
Moments must be sparse; callbacks only when tags overlap or time gate triggers.

**Watch out for:**
Never mark a moment as spoken without moment_refs in output.

**Open questions I had:**
How to weight tags for overlap scoring?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Moment graph now has lifecycle helpers with tests for promotion, decay, merge, and callbacks.

**Decisions made:**
Moments are sparse and callbacks require explicit references.

**Needs your input:**
Confirm promotion/decay thresholds and tag taxonomy.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: add configurable thresholds and persistence integration.

### Tests to Run

```bash
pytest tests/test_moment_lifecycle_rules.py
```

### Immediate

- [ ] Define tag overlap rule and decay schedule.
- [ ] Specify myth promotion thresholds.

### Later

- [ ] Add callback selection with time gates.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:** Focused, early-stage.

**Threads I was holding:**
Need to keep moment count low to preserve mythic weight.

**Intuitions:**
Myth promotion should require multiple signals, not one event.

**What I wish I'd known at the start:**
Expected event taxonomy for tags.

---

## POINTERS

| What | Where |
|------|-------|
| Moment creator stub | `src/moment_graph/moment_creator_and_merger.py` |
| Lifecycle stub | `src/moment_graph/moment_lifecycle_promoter_and_decayer.py` |
| Query selector stub | `src/moment_graph/moment_query_and_callback_selector.py` |
