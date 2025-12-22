# style_ngrams — Sync: Current State

```
LAST_UPDATED: 2025-12-21
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- N-gram counters track player action transitions.
- Backoff from leader -> phase -> global.

**What's still being designed:**
- Surprise normalization with quantiles.
- Token compression rules for rare tokens.

**What's proposed (v2+):**
- Persona-specific predictors.

---

## CURRENT STATE

Style n-gram module now includes tokenization, count store, probability estimation, and backoff prediction helpers with tests.

---

## IN PROGRESS

### Backoff and surprise scoring

- **Started:** 2025-12-21
- **By:** codex
- **Status:** in progress
- **Context:** Define backoff rules and surprise normalization.

---

## RECENT CHANGES

### 2025-12-21: Seed style_ngrams docs

- **What:** Added initial objectives, algorithm, validation, implementation, and health notes.
- **Why:** Codify profiling and prediction boundaries before code.
- **Files:** `docs/civ6_living_narrator/style_ngrams/`
- **Struggles/Insights:** Keep vocab compression explicit.

### 2025-12-21: Implement n-gram update and backoff baseline

- **What:** Added tokenizer, counter store, probability estimation, backoff predictor, token map config, and tests.
- **Why:** Establish profiling and prediction source rules required by the spec.
- **Files:** `src/style_ngrams/event_tokenizer_and_feature_extractor.py`, `src/style_ngrams/ngram_transition_counter_store.py`, `src/style_ngrams/ngram_probability_estimator_and_surprise_scorer.py`, `src/style_ngrams/ngram_scope_backoff_predictor.py`, `config/token_map.yaml`, `tests/test_ngram_update_and_surprise.py`
- **Struggles/Insights:** Compression uses explicit mappings; rarity thresholds still need integration.

---

## KNOWN ISSUES

### Token compression undefined

- **Severity:** medium
- **Symptom:** Rare tokens may explode state.
- **Suspected cause:** Missing ::ANY mapping rules.
- **Attempted:** None yet.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `.ngram/views/VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** Baseline n-gram implementation and tests are in place.

**What you need to understand:**
Backoff must return prediction_source so downstream can explain why.

**Watch out for:**
Without compression, counters will blow up.

**Open questions I had:**
How to define phase buckets for backoff?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Style n-grams now have tokenization, counts, backoff prediction, and tests for prediction_source/compression.

**Decisions made:**
Backoff is leader -> phase -> global; prediction_source must be recorded.

**Needs your input:**
Confirm phase taxonomy and compression thresholds.

---

## TODO

### Doc/Impl Drift

- [ ] DOCS->IMPL: add rarity thresholding and quantile tracking for surprise.

### Tests to Run

```bash
pytest tests/test_ngram_update_and_surprise.py
```

### Immediate

- [ ] Define ::ANY token compression rules.
- [ ] Define phase buckets.

### Later

- [ ] Add quantile tracking for surprise normalization.

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:** Focused, early-stage.

**Threads I was holding:**
Need to prevent sparse scopes from skewing predictions.

**Intuitions:**
Backoff should bias toward global rather than no prediction.

**What I wish I'd known at the start:**
Expected event taxonomy for tokenization.

---

## POINTERS

| What | Where |
|------|-------|
| Tokenizer stub | `src/style_ngrams/event_tokenizer_and_feature_extractor.py` |
| Counter store stub | `src/style_ngrams/ngram_transition_counter_store.py` |
| Surprise scorer stub | `src/style_ngrams/ngram_probability_estimator_and_surprise_scorer.py` |
| Backoff predictor stub | `src/style_ngrams/ngram_scope_backoff_predictor.py` |
