# OBJECTIFS — style_ngrams

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

## PRIMARY OBJECTIVES (ranked)
1. Detect player style patterns for credible commentary.
2. Provide stable predictions with scope backoff.
3. Keep vocabulary compact to avoid sparsity.

## NON-OBJECTIVES
- Perfect prediction accuracy.
- Exhaustive action modeling.

## TRADEOFFS (canonical decisions)
- When scope is too sparse, back off to broader scope.
- Accept compression errors to preserve stability.

## SUCCESS SIGNALS (observable)
- prediction_source is always populated.
- Surprise scores remain stable across sessions.
