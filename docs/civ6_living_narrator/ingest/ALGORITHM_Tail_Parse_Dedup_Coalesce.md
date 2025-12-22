# ingest — Algorithm: Tail, parse, dedup, coalesce

```
STATUS: DRAFT
CREATED: 2025-12-21
VERIFIED: 2025-12-21 against TBD
```

---

## CHAIN

```
BEHAVIORS:      ./BEHAVIORS_Ingest_Event_Intake.md
THIS:           ./ALGORITHM_Tail_Parse_Dedup_Coalesce.md
VALIDATION:     ./VALIDATION_Event_Schemas_And_Signatures.md
IMPLEMENTATION: ./IMPLEMENTATION_File_Watcher_And_Parsers.md
HEALTH:         ./HEALTH_Ingest_Lag_And_Error_Rates.md
SYNC:           ./SYNC_Ingest_And_Normalization.md
```

---

## OVERVIEW

Continuously tail the session JSONL file, parse lines into raw events, normalize fields, and drop or coalesce duplicates.

---

## STEPS

1. Open the JSONL file in read-only mode with a persistent file handle.
2. Seek to the last known offset and read new bytes.
3. Split into lines. If the last line is incomplete, store it as a carryover buffer.
4. For each complete line:
   - Parse JSON.
   - Map to EventNormalized schema.
   - Compute signature (event_type + entity ids + turn + optional hash of payload).
   - If signature seen within dedup window, drop or coalesce.
5. Emit normalized events and update tail offset.

---

## EDGE CASES

- Partial line: keep buffer and retry on next read.
- Rotation: if session_id changes, reopen the active file.
- Unknown fields: map to metadata and log.

---

## OUTPUTS

- Stream of EventNormalized records for downstream modules.
