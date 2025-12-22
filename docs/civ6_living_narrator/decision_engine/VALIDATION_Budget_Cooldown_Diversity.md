# decision_engine — Validation: Budget, cooldown, diversity

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Rhythm_NonSpam_Diversity.md
ALGORITHM:      ./ALGORITHM_Score_Candidates_And_Select.md
THIS:           ./VALIDATION_Budget_Cooldown_Diversity.md
IMPLEMENTATION: ./IMPLEMENTATION_Candidate_Pipeline_And_Explainability.md
HEALTH:         ./HEALTH_SpeechRate_Suppression_Reasons.md
SYNC:           ./SYNC_Rhythm_And_Selection.md
```

---

## INVARIANTS

### V1: Budget enforced

```
Spoken lines per window <= max_speech_budget
```

**Checked by:** `test_budget_and_selection_invariants.py`

### V2: Cooldown enforced

```
No speaker emits while cooldown_active
```

**Checked by:** `test_budget_and_selection_invariants.py`

### V3: Diversity penalty applied

```
Consecutive leader lines are blocked unless pivot
```

**Checked by:** `test_budget_and_selection_invariants.py`

---

## VERIFICATION PROCEDURE

```bash
pytest tests/test_budget_and_selection_invariants.py
```
