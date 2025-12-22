# style_ngrams — Validation: Scope backoff and vocab compression

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Style_Profiling_And_Anticipation.md
ALGORITHM:      ./ALGORITHM_Ngram_Update_Smoothing_Surprise.md
THIS:           ./VALIDATION_Scope_Backoff_And_Vocab_Compression.md
IMPLEMENTATION: ./IMPLEMENTATION_Count_Stores_And_Query_API.md
HEALTH:         ./HEALTH_Sparsity_Quantiles_And_Drift.md
SYNC:           ./SYNC_Style_Ngram_Graph.md
```

---

## INVARIANTS

### V1: Backoff always returns a prediction source

```
Prediction source is one of BY_LEADER, BY_PHASE, GLOBAL
```

**Checked by:** `test_ngram_update_and_surprise.py`

### V2: Compression maps rare tokens

```
Tokens below rarity threshold map to ::ANY
```

**Checked by:** `test_ngram_update_and_surprise.py`

---

## VERIFICATION PROCEDURE

```bash
pytest tests/test_ngram_update_and_surprise.py
```
