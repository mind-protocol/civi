# llm_router — Implementation: Prompt templates and cache

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## FILE MAP

| Responsibility | File |
|----------------|------|
| Context pack builder | `src/llm_router/context_pack_builder_and_truncator.py` |
| JSON validator + repair | `src/llm_router/strict_json_output_validator_and_repair_pass.py` |
| Prompt templates | `src/llm_router/prompt_template_loader.py` |

---

## DATA FLOW

1. Build context pack with truncation rules.
2. Render prompt template.
3. Validate JSON output and repair if needed.
4. Optional cache keyed by context pack hash.

---

## CONFIG

- `config/config.yaml`: token budgets, max words, cache toggle.

---

## NOTES

Cache should be deterministic for replay.
