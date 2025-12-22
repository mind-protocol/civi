# Lua Mod — Validation: Event Schema and File Integrity

```
STATUS: DRAFT
CREATED: 2025-12-22
VERIFIED: n/a (not yet implemented)
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Event_Extraction_And_Emission.md
BEHAVIORS:      ./BEHAVIORS_Game_Events_To_JSONL.md
PATTERNS:       ./PATTERNS_Append_Only_Event_Stream.md
ALGORITHM:      ./ALGORITHM_Hook_Serialize_Append.md
THIS:           ./VALIDATION_Event_Schema_And_File_Integrity.md
IMPLEMENTATION: ./IMPLEMENTATION_Mod_Files_And_Hooks.md
HEALTH:         ./HEALTH_Event_Lag_And_File_Growth.md
SYNC:           ./SYNC_Lua_Mod_Status.md

IMPL:           (not yet created)
```

### Bidirectional Contract

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## INVARIANTS

### V1: Every line is valid JSON

```
ALWAYS: Each line in events.jsonl parses as valid JSON
NEVER:  Partial lines, truncated objects, or syntax errors
```

**Verification:**
```python
def verify_file_integrity(path):
    with open(path) as f:
        for i, line in enumerate(f, 1):
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                raise AssertionError(f"Line {i} invalid: {e}")
```

### V2: Every event has required base fields

```
ALWAYS: event_type (string), turn (integer), timestamp (integer)
NEVER:  Missing or null base fields
```

**Schema:**
```json
{
    "event_type": "string, required, non-empty",
    "turn": "integer, required, >= 0",
    "timestamp": "integer, required, unix epoch",
    "game_id": "string, optional, session identifier"
}
```

### V3: Event types match defined schema

| Event Type | Required Fields |
|------------|-----------------|
| `TURN_START` | `player_id`, `player_civ` |
| `CITY_BUILT` | `city_name`, `player_id`, `player_civ` |
| `CITY_CAPTURED` | `city_name`, `old_owner_id`, `new_owner_id` |
| `WONDER_COMPLETED` | `wonder`, `player_id`, `player_civ` |
| `WAR_DECLARED` | `attacker_id`, `attacker_civ`, `defender_id`, `defender_civ` |
| `PEACE_MADE` | `player1_id`, `player1_civ`, `player2_id`, `player2_civ` |
| `TECH_COMPLETED` | `tech`, `player_id` |
| `CIVIC_COMPLETED` | `civic`, `player_id` |
| `GREAT_PERSON_EARNED` | `person_type`, `person_name`, `player_id` |
| `VICTORY_PROXIMITY` | `victory_type`, `progress`, `player_id` |

### V4: File only grows (append-only)

```
ALWAYS: File size at time T+1 >= file size at time T
NEVER:  File truncation or rewrite during game session
```

### V5: No blocking during write

```
ALWAYS: Event write completes in < 1ms
NEVER:  Visible game stutter caused by event emission
```

---

## EDGE CASES

### E1: Unicode in city/civilization names

```
INPUT:  City named "北京" or civilization "Österreich"
EXPECT: Valid JSON with properly escaped unicode
```

### E2: Special characters in strings

```
INPUT:  Text containing quotes, backslashes, newlines
EXPECT: Properly escaped: \" \\ \n
```

### E3: Very long game (1000+ turns)

```
EXPECT: File remains valid, no overflow errors
EXPECT: Reasonable file size (< 100MB for typical game)
```

### E4: Rapid events (multiple per second)

```
EXPECT: All events captured in order
EXPECT: No race conditions or lost events
```

### E5: Game save/load cycle

```
EXPECT: New events append correctly after load
EXPECT: No duplicate events from reload
```

---

## TEST CASES

### Unit Tests

```lua
-- Test JSON serialization
assert(SerializeToJSON({a = 1, b = "test"}) == '{"a":1,"b":"test"}')
assert(SerializeToJSON("quote\"test") == '"quote\\"test"')
assert(SerializeToJSON(true) == "true")
assert(SerializeToJSON(nil) == "null")
```

### Integration Tests

```python
# Test file integrity after simulated game
def test_file_integrity():
    # Simulate 100 turns
    simulate_game(turns=100)

    # Verify all lines valid
    with open("events.jsonl") as f:
        events = [json.loads(line) for line in f]

    # Verify turn ordering
    turns = [e["turn"] for e in events if e["event_type"] == "TURN_START"]
    assert turns == sorted(turns)
```

---

## VERIFICATION COMMANDS

```bash
# Verify file integrity
python -c "import json; [json.loads(l) for l in open('events.jsonl')]"

# Count events by type
jq -r '.event_type' events.jsonl | sort | uniq -c

# Check for missing required fields
jq 'select(.event_type == null or .turn == null)' events.jsonl
```

---

## BUDGET CONSTRAINTS

| Metric | Limit | Rationale |
|--------|-------|-----------|
| Write latency | < 1ms | No perceptible game lag |
| File size per turn | < 1KB average | Reasonable disk usage |
| Memory usage | < 1MB | Minimal mod footprint |
| Events per turn | No hard limit | Emit all, filter downstream |

---

## MARKERS

<!-- @ngram:todo Add JSON schema validation to ingest module -->
<!-- @ngram:todo Define rotation strategy for very long games -->
