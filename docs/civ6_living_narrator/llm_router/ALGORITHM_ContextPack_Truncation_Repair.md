# llm_router — Algorithm: Context pack, truncation, repair

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Strict_JSON_And_Repair.md
THIS:           ./ALGORITHM_ContextPack_Truncation_Repair.md
VALIDATION:     ./VALIDATION_Output_Schema_And_MaxWords.md
IMPLEMENTATION: ./IMPLEMENTATION_Prompt_Templates_And_Cache.md
HEALTH:         ./HEALTH_InvalidRate_Latency_Cost.md
SYNC:           ./SYNC_JSON_Contracts_And_Fallbacks.md
```

---

## OVERVIEW

Build a context pack, truncate by priority, request JSON, and repair once if needed.

---

## STEPS

1. Assemble context pack: recent events, active moments, challenges, style hints.
2. If over token budget, truncate in order:
   - drop oldest history
   - drop lowest-priority signals
   - shorten text fields
3. Send prompt with strict JSON contract and max words.
4. Validate JSON; if invalid, send repair prompt requesting JSON only.
5. If still invalid, return silence with invalid_json reason.

---

## OUTPUTS

- Valid JSON line or silence fallback.
