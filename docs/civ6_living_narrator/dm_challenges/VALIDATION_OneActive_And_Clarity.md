# dm_challenges — Validation: One active and clarity

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Agency_Contracts_Temptation.md
ALGORITHM:      ./ALGORITHM_Generate_Evaluate_Remind.md
THIS:           ./VALIDATION_OneActive_And_Clarity.md
IMPLEMENTATION: ./IMPLEMENTATION_Challenge_Catalog_And_Runtime.md
HEALTH:         ./HEALTH_Completion_Rates_And_Frustration_Signals.md
SYNC:           ./SYNC_Challenge_Contract_System.md
```

---

## INVARIANTS

### V1: One active challenge

```
active_challenge_count <= 1
```

**Checked by:** `test_dm_challenge_offers_and_state.py`

### V2: Refusal line present

```
Challenge offers include refusal_line
```

**Checked by:** `test_challenge_catalog_loader.py`

---

## VERIFICATION PROCEDURE

```bash
pytest tests/test_budget_and_selection_invariants.py
```
