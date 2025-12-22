# llm_router — Sync: Current State

```
LAST_UPDATED: 2025-12-22
UPDATED_BY: gemini
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Strict JSON output validation with one repair pass.
- Fallback to silence on invalid output.
- Basic multi-model CLI support (Claude/Gemini via env var).

**What's still being designed:**
- Context pack truncation strategy.
- Cache strategy for replay.
- Dynamic model routing based on task type.

**What's proposed (v2+):**
- Advanced multi-model routing (per-task model selection).

---

## CURRENT STATE

LLM router now supports both Claude and Gemini CLIs via environment variable configuration. Baseline JSON validation is in place.

---

## IN PROGRESS

### JSON contracts and repair

- **Started:** 2025-12-21
- **By:** codex
- **Status:** in progress
- **Context:** Define schema validation and repair pass contract.

---

## RECENT CHANGES

### 2025-12-22: Implement Gemini CLI Support

- **What:** Refactored `simple_llm_client.py` to `LLMCLIClient`. Added support for Gemini CLI using `SELECTED_MODEL` from `.env`.
- **Why:** Enable use of Gemini models.
- **Files:** `src/llm_router/simple_llm_client.py`, `src/main.py`
- **Impact:** User can switch models via `.env`.

### 2025-12-21: Seed llm_router docs

- **What:** Added initial patterns, algorithm, validation, implementation, and health notes.
- **Why:** Define strict JSON boundaries and fallback behavior.
- **Files:** `docs/civ6_living_narrator/llm_router/`
- **Struggles/Insights:** Keep repair pass minimal to avoid drift.

### 2025-12-21: Implement JSON validation and repair baseline

- **What:** Added JSON validator, repair pass helper, context pack truncation stub, and prompt template loader plus tests.
- **Why:** Enforce strict JSON output and a single repair attempt as required by the spec.
- **Files:** `src/llm_router/strict_json_output_validator_and_repair_pass.py`, `src/llm_router/context_pack_builder_and_truncator.py`, `src/llm_router/prompt_template_loader.py`, `tests/test_llm_json_fuzz_and_fallback.py`
- **Struggles/Insights:** Schema is minimal (text + speaker) pending expansion.

---

## KNOWN ISSUES

### Context truncation undefined

- **Severity:** medium
- **Symptom:** Risk of oversize prompts.
- **Suspected cause:** Missing truncation rules.
- **Attempted:** None yet.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `.ngram/views/VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Baseline JSON validation and repair helpers with tests are in place.

**What you need to understand:**
Only one repair attempt allowed; otherwise fallback to silence.

**Watch out for:**
Repair prompt must return JSON only.

**Open questions I had:**
How to structure cache keys for replay?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
LLM router now enforces strict JSON validation with a single repair attempt and tests.

**Decisions made:**
One repair attempt max; fallback to silence on failure.

**Needs your input:**
Confirm truncation priorities and caching scope.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: expand schema and implement truncation priorities and cache.

### Tests to Run

```bash
pytest tests/test_llm_json_fuzz_and_fallback.py
```

### Immediate

- [ ] Define truncation order and max token budget.
- [ ] Define cache key hashing rules.

### Later

- [ ] Add replay cache storage.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:** Focused, early-stage.

**Threads I was holding:**
Need to keep schema strict without frequent false failures.

**Intuitions:**
Truncate history before signals to preserve schema.

**What I wish I'd known at the start:**
Expected token budgets for prompt and response.

---

## POINTERS

| What | Where |
|------|-------|
| Context pack stub | `src/llm_router/context_pack_builder_and_truncator.py` |
| JSON validator stub | `src/llm_router/strict_json_output_validator_and_repair_pass.py` |
| Prompt loader stub | `src/llm_router/prompt_template_loader.py` |
