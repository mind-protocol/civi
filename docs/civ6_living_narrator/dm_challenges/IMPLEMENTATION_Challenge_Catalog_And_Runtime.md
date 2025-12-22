# dm_challenges — Implementation: Challenge catalog and runtime

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## FILE MAP

| Responsibility | File |
|----------------|------|
| Catalog loader | `src/dm_challenges/challenge_catalog_loader_and_validator.py` |
| Offer generator | `src/dm_challenges/challenge_offer_generator.py` |
| State tracker | `src/dm_challenges/challenge_state_tracker_and_evaluator.py` |

---

## DATA FLOW

1. Load challenge catalog from YAML.
2. Offer generator selects a challenge candidate.
3. State tracker updates acceptance/refusal/completion.

---

## CONFIG

- `config/challenge_catalog.yaml`: catalog definitions.
- `config/config.yaml`: pacing and cooldown settings.

---

## NOTES

Keep refusal lines optional but required for offers.
