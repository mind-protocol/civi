# ingest — Validation: Event schemas and signatures

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
THIS:           ./VALIDATION_Event_Schemas_And_Signatures.md
IMPLEMENTATION: ./IMPLEMENTATION_File_Watcher_And_Parsers.md
HEALTH:         ./HEALTH_Ingest_Lag_And_Error_Rates.md
SYNC:           ./SYNC_Ingest_And_Normalization.md
```

---

## INVARIANTS

### V1: EventNormalized required fields

```
EventNormalized contains: event_type, turn, timestamp, payload
```

**Checked by:** `test_parse_and_normalize_events.py`

**Schema source:** `config/event_schema.yaml`

### V2: Dedup signature is stable

```
Same event inputs produce the same signature
```

**Checked by:** `test_parse_and_normalize_events.py`

### V3: Partial line yields no output

```
Incomplete JSON lines do not emit events
```

**Checked by:** `test_windows_bridge_rotation_and_tail.py`

### V4: Unknown fields are mapped

```
Unknown raw fields are captured under payload._unknown_fields
```

**Checked by:** `test_parse_and_normalize_events.py`

---

## ERROR CONDITIONS

### E1: Malformed JSON

```
WHEN:    json.loads fails
THEN:    drop line and increment invalid counter
SYMPTOM: invalid_jsonl_line_count increments
```

**Verified by:** NOT YET VERIFIED

---

## VERIFICATION PROCEDURE

```bash
pytest tests/test_parse_and_normalize_events.py
pytest tests/test_windows_bridge_rotation_and_tail.py
```
