# decision_engine — Implementation: Candidate pipeline and explainability

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## FILE MAP

| Responsibility | File |
|----------------|------|
| Budgets and cooldowns | `src/decision_engine/narrative_budget_and_cooldown_enforcer.py` |
| Candidate builder | `src/decision_engine/candidate_builder_for_speakers.py` |
| Ranker and selector | `src/decision_engine/candidate_ranker_and_selector_with_explainability.py` |

---

## DATA FLOW

1. Candidate builder assembles proposals.
2. Budget enforcer filters by pacing rules.
3. Ranker scores and selects final line.
4. Explainability payload records top candidates and reasons.

---

## CONFIG

- `config/config.yaml`: budgets, cooldowns, gating thresholds.
- `config/config.yaml`: diversity blocking and min_delta_value.

---

## NOTES

Expose suppression reasons in telemetry for overlay.
