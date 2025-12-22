# llm_router — Validation: Output schema and max words

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
PATTERNS:       ./PATTERNS_Strict_JSON_And_Repair.md
ALGORITHM:      ./ALGORITHM_ContextPack_Truncation_Repair.md
THIS:           ./VALIDATION_Output_Schema_And_MaxWords.md
IMPLEMENTATION: ./IMPLEMENTATION_Prompt_Templates_And_Cache.md
HEALTH:         ./HEALTH_InvalidRate_Latency_Cost.md
SYNC:           ./SYNC_JSON_Contracts_And_Fallbacks.md
```

---

## INVARIANTS

### V1: JSON schema validated

```
LLM output parses as JSON and matches schema
```

**Checked by:** `test_llm_json_fuzz_and_fallback.py`

### V2: Max words enforced

```
Output word count <= max_words
```

**Checked by:** NOT YET VERIFIED

### V3: Repair pass succeeds or falls back

```
Invalid JSON triggers a single repair attempt; failure yields fallback
```

**Checked by:** `test_llm_json_fuzz_and_fallback.py`

---

## VERIFICATION PROCEDURE

```bash
pytest tests/test_llm_json_fuzz_and_fallback.py
```
