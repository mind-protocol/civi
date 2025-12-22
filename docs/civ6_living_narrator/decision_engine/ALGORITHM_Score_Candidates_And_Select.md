# decision_engine — Algorithm: Score candidates and select

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Rhythm_NonSpam_Diversity.md
THIS:           ./ALGORITHM_Score_Candidates_And_Select.md
VALIDATION:     ./VALIDATION_Budget_Cooldown_Diversity.md
IMPLEMENTATION: ./IMPLEMENTATION_Candidate_Pipeline_And_Explainability.md
HEALTH:         ./HEALTH_SpeechRate_Suppression_Reasons.md
SYNC:           ./SYNC_Rhythm_And_Selection.md
```

---

## OVERVIEW

Build candidate lines, score them, apply gating, and select at most one output per turn.

---

## STEPS

1. Build candidate list from events, moments, challenges, and leader prompts.
2. For each candidate, compute score components:
   - importance
   - surprise
   - moment_relevance
   - diversity_penalty
   - cooldown_penalty
3. Apply silence gate: if top score < MIN_DELTA_VALUE over baseline, suppress.
4. Enforce budgets and cooldowns; drop candidates that violate constraints.
5. Select best remaining candidate and emit explainability payload.

---

## OUTPUTS

- Selected line or silence.
- Suppression reasons with counts.
- Top candidates with score breakdown.
