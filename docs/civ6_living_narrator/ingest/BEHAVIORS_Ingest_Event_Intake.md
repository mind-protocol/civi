# ingest — Behaviors: Event intake and normalization

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
BEHAVIORS:      ./BEHAVIORS_Ingest_Event_Intake.md
ALGORITHM:      ./ALGORITHM_Tail_Parse_Dedup_Coalesce.md
VALIDATION:     ./VALIDATION_Event_Schemas_And_Signatures.md
IMPLEMENTATION: ./IMPLEMENTATION_File_Watcher_And_Parsers.md
HEALTH:         ./HEALTH_Ingest_Lag_And_Error_Rates.md
SYNC:           ./SYNC_Ingest_And_Normalization.md
```

---

## BEHAVIORS

### B1: Tail append-only JSONL

The ingest layer tails a growing JSONL file and emits events in order.

### B2: Tolerate partial lines

If a line is truncated, ingest waits and retries until the JSON is complete.

### B3: Normalize raw events

Raw fields are mapped into a stable EventNormalized schema.

### B4: Deduplicate near-duplicate events

Events with the same signature in a short window are dropped or coalesced.

### B5: Coalesce noisy events

Multiple minor events in a single turn are merged into a summary event.

---

## ANTI-BEHAVIORS

- A1: Crashing on malformed JSONL input.
- A2: Emitting duplicate events that cause narration spam.
- A3: Blocking on file locks or partial lines.
