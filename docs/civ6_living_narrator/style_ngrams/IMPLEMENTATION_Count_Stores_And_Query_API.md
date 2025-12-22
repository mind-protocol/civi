# style_ngrams — Implementation: Count stores and query API

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## FILE MAP

| Responsibility | File |
|----------------|------|
| Tokenizer | `src/style_ngrams/event_tokenizer_and_feature_extractor.py` |
| Count store | `src/style_ngrams/ngram_transition_counter_store.py` |
| Surprise scorer | `src/style_ngrams/ngram_probability_estimator_and_surprise_scorer.py` |
| Backoff predictor | `src/style_ngrams/ngram_scope_backoff_predictor.py` |

---

## DATA FLOW

1. Tokenizer emits action tokens per event.
2. Counter store updates per scope.
3. Surprise scorer estimates probability and surprise.
4. Backoff predictor selects scope and prediction.

---

## CONFIG

- `config/token_map.yaml`: compression mappings and rarity thresholds.
  - mapping: explicit token mapping, including ::ANY fallback.

---

## NOTES

Store quantiles per scope to normalize surprise over time.
