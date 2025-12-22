# OBJECTIFS — decision_engine

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

## PRIMARY OBJECTIVES (ranked)
1. Silence-first pacing — speak only when value clears the gate.
2. Diversity of speakers — avoid repetitive leader or narrator runs.
3. Explainable selection — log why a line was chosen or suppressed.

## NON-OBJECTIVES
- Maximizing narration quantity.
- Perfect prediction of player intent.

## TRADEOFFS (canonical decisions)
- When pacing conflicts with coverage, choose pacing.
- Accept skipped candidates to preserve speaker diversity.

## SUCCESS SIGNALS (observable)
- speech_suppressed_count includes reason tags per turn.
- No consecutive leader lines without a pivot trigger.
