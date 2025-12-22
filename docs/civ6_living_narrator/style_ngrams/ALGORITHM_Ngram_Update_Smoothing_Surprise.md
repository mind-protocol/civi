# style_ngrams — Algorithm: N-gram update, smoothing, surprise

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Style_Profiling_And_Anticipation.md
THIS:           ./ALGORITHM_Ngram_Update_Smoothing_Surprise.md
VALIDATION:     ./VALIDATION_Scope_Backoff_And_Vocab_Compression.md
IMPLEMENTATION: ./IMPLEMENTATION_Count_Stores_And_Query_API.md
HEALTH:         ./HEALTH_Sparsity_Quantiles_And_Drift.md
SYNC:           ./SYNC_Style_Ngram_Graph.md
```

---

## OVERVIEW

Update n-gram counts per scope, smooth probabilities, compute surprise, and backoff when sparse.

---

## STEPS

1. Tokenize normalized events into action tokens.
2. Apply compression: map rare tokens to ::ANY.
3. Update transition counts per scope (BY_LEADER, BY_PHASE, GLOBAL).
4. Estimate transition probabilities with smoothing.
5. Compute surprise and predicted next token per scope.
6. Back off to broader scope if counts below threshold; record prediction_source.

---

## OUTPUTS

- Transition counts and smoothed probabilities.
- Surprise score for each event.
- Predicted next token with prediction_source.
