# Civ6 Living Narrator — Algorithm: End-to-end pipeline

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Product_And_Feelings.md
BEHAVIORS:      ./BEHAVIORS_System_Experience_And_Rhythm.md
PATTERNS:       ./PATTERNS_System_Architecture_And_Boundaries.md
THIS:           ./ALGORITHM_End_To_End_Pipeline.md
VALIDATION:     ./VALIDATION_Global_Invariants_And_Budgets.md
IMPLEMENTATION: ./IMPLEMENTATION_Repo_Structure_And_Entry_Points.md
HEALTH:         ./HEALTH_Global_System_Signals.md
SYNC:           ./SYNC_Project_State.md

IMPL:           src/
```

---

## OVERVIEW

Ingest events from JSONL, normalize and dedup, update style and moment systems, build candidates, and select narration with silence-first gates.

---

## STEPS

1. Tail and parse JSONL events for the active session.
2. Normalize events and deduplicate/coalesce.
3. Update n-gram style profile and moment graph.
4. Build candidate narration lines.
5. Apply budgets, cooldowns, diversity, and silence gate.
6. If selected, send line to LLM router and audio runtime.
7. Emit telemetry and overlay payload.

---

## DATA FLOW

```
JSONL -> Ingest -> Normalized events
    -> Style N-grams + Moment Graph
    -> Decision Engine
    -> LLM Router
    -> Audio Runtime
    -> Telemetry
```

---

## KEY DECISIONS

### D1: Silence gate

```
IF top_score < MIN_DELTA_VALUE:
    suppress narration
ELSE:
    emit best candidate
```

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| src/ingest | tail + normalize | EventNormalized stream |
| src/decision_engine | select_candidate | chosen line or silence |
| src/llm_router | render_json_line | strict JSON output |
| runtime_windows/audio_player | play queue | audio playback |
