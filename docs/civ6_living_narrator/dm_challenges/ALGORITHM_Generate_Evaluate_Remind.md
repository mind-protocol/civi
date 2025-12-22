# dm_challenges — Algorithm: Generate, evaluate, remind

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Agency_Contracts_Temptation.md
THIS:           ./ALGORITHM_Generate_Evaluate_Remind.md
VALIDATION:     ./VALIDATION_OneActive_And_Clarity.md
IMPLEMENTATION: ./IMPLEMENTATION_Challenge_Catalog_And_Runtime.md
HEALTH:         ./HEALTH_Completion_Rates_And_Frustration_Signals.md
SYNC:           ./SYNC_Challenge_Contract_System.md
```

---

## OVERVIEW

Select a challenge from the catalog, track acceptance/refusal, and remind sparingly.

---

## STEPS

1. Load challenge catalog and filter by eligibility.
2. Select a candidate based on player style and pacing rules.
3. Emit challenge offer with clear conditions and refusal_line.
4. Track active challenge state.
5. Evaluate completion or refusal signals.
6. Remind only if cooldown elapsed and challenge still active.

---

## OUTPUTS

- Challenge offer event with id, conditions, refusal_line.
- Challenge state updates (accepted, refused, completed).
