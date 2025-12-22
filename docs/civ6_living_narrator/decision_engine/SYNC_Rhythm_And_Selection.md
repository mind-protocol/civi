# decision_engine — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Silence-first gating with budgets and cooldowns.
- Candidate scoring and selection with explainability.

**What's still being designed:**
- Diversity rules for speakers.
- Thresholds for foreshadow and myth callbacks.

**What's proposed (v2+):**
- Adaptive pacing by phase and difficulty.

---

## CURRENT STATE

Decision engine now has baseline budget/cooldown enforcement and candidate selection helpers with tests.

---

## IN PROGRESS

### Rhythm and selection rules

- **Started:** 2025-12-21
- **By:** codex
- **Status:** in progress
- **Context:** Define gating thresholds, diversity rules, and explainability payload.

---

## RECENT CHANGES

### 2025-12-21: Seed decision_engine docs

- **What:** Added initial objectives, algorithm, validation, implementation, and health notes.
- **Why:** Codify silence-first rhythm and selection boundaries before code.
- **Files:** `docs/civ6_living_narrator/decision_engine/`
- **Struggles/Insights:** Avoid hardcoding thresholds without config.

### 2025-12-21: Implement selection and gating baseline

- **What:** Added candidate structures, budget/cooldown enforcement, selection logic, and tests for budget, cooldown, diversity, and low-value gating.
- **Why:** Establish baseline pacing and suppression behavior as required by the spec.
- **Files:** `src/decision_engine/narrative_budget_and_cooldown_enforcer.py`, `src/decision_engine/candidate_builder_for_speakers.py`, `src/decision_engine/candidate_ranker_and_selector_with_explainability.py`, `tests/test_budget_and_selection_invariants.py`, `config/config.yaml`
- **Struggles/Insights:** Cooldown and diversity suppression ordering can hide diversity signals if not tested explicitly.

---

## KNOWN ISSUES

### Thresholds undefined

- **Severity:** medium
- **Symptom:** No MIN_DELTA_VALUE yet for silence gating.
- **Suspected cause:** Config schema not drafted.
- **Attempted:** None yet.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `.ngram/views/VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Baseline selection implementation and tests are in place.

**What you need to understand:**
Silence-first gating is non-negotiable; selection must emit suppression reasons.

**Watch out for:**
Keep speaker diversity in scoring rather than hard bans unless pivot.

**Open questions I had:**
What is the baseline for MIN_DELTA_VALUE and how to tune it?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Decision engine now has baseline selection logic with budget, cooldown, diversity, and silence gating tests.

**Decisions made:**
Budgets and cooldowns gate all narration; suppress reasons are logged.

**Needs your input:**
Confirm diversity rules and initial thresholds.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: add configurable scoring weights and explainability payload output format.

### Tests to Run

```bash
pytest tests/test_budget_and_selection_invariants.py
```

### Immediate

- [ ] Define candidate score breakdown fields.
- [ ] Set initial silence gating threshold in config.

### Later

- [ ] Add foreshadow candidate type and gating.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:** Focused, early-stage.

**Threads I was holding:**
Need to log suppression reasons for debug overlay.

**Intuitions:**
Diversity should be a penalty with pivot exception.

**What I wish I'd known at the start:**
Expected narration rate per 10 turns.

---

## POINTERS

| What | Where |
|------|-------|
| Budget enforcer stub | `src/decision_engine/narrative_budget_and_cooldown_enforcer.py` |
| Candidate builder stub | `src/decision_engine/candidate_builder_for_speakers.py` |
| Ranker stub | `src/decision_engine/candidate_ranker_and_selector_with_explainability.py` |
