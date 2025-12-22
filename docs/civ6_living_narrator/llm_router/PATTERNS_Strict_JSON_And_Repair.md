# llm_router — Patterns: Strict JSON and repair

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
VALIDATION:     ./VALIDATION_Output_Schema_And_MaxWords.md
IMPLEMENTATION: ./IMPLEMENTATION_Prompt_Templates_And_Cache.md
HEALTH:         ./HEALTH_InvalidRate_Latency_Cost.md
SYNC:           ./SYNC_JSON_Contracts_And_Fallbacks.md
```

---

## THE PROBLEM

LLM output can be invalid JSON or verbose. The router must enforce strict schema and recover once.

---

## THE PATTERN

- Send context pack with strict JSON contract.
- Validate response; if invalid, run a single repair prompt.
- On second failure, fallback to silence and log.

---

## PRINCIPLES

### Principle 1: JSON only

Responses must parse as JSON; no extra text.

### Principle 2: Single repair pass

One retry prevents loops and keeps latency bounded.

### Principle 3: Budgeted context

Truncate context by priority without breaking schema.
