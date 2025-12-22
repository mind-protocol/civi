# Lua Mod — Health: Event Lag and File Growth

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
VALIDATION:     ./VALIDATION_Event_Schema_And_File_Integrity.md
IMPLEMENTATION: ./IMPLEMENTATION_Mod_Files_And_Hooks.md
THIS:           ./HEALTH_Event_Lag_And_File_Growth.md
SYNC:           ./SYNC_Lua_Mod_Status.md

IMPL:           (not yet created)
```

---

## OVERVIEW

Health signals for the Lua mod focus on two concerns:
1. **Performance** — mod must not impact game responsiveness
2. **File integrity** — events file must remain valid and manageable

---

## HEALTH SIGNALS

### H1: Write Latency

```yaml
signal: lua_mod.write_latency_ms
source: timing around AppendLine() call
threshold:
  healthy: < 1ms
  warning: 1-5ms
  critical: > 5ms
rationale: >
  Writes over 5ms may cause perceptible stutter.
  Normal SSD writes should be sub-millisecond.
```

**Measurement:**
```lua
local start = os.clock()
AppendLine(json)
local elapsed = (os.clock() - start) * 1000
if elapsed > 5 then
    print("[LivingNarrator] WARN: Slow write: " .. elapsed .. "ms")
end
```

### H2: Events Per Turn

```yaml
signal: lua_mod.events_per_turn
source: count of EmitEvent() calls per turn
threshold:
  healthy: 1-20
  warning: 20-50
  critical: > 50
rationale: >
  Unusually high event counts may indicate
  duplicate emissions or unfiltered spam.
```

### H3: File Size

```yaml
signal: lua_mod.file_size_mb
source: events.jsonl file size
threshold:
  healthy: < 10MB
  warning: 10-50MB
  critical: > 50MB
rationale: >
  Large files may slow down pipeline tailing.
  Rotation should be considered at warning level.
```

**Measurement:**
```bash
# Check file size
ls -lh ~/Documents/Civ6LivingNarrator/events/events.jsonl
```

### H4: File Integrity

```yaml
signal: lua_mod.file_valid
source: JSON parse of all lines
threshold:
  healthy: 100% valid lines
  warning: any invalid lines
  critical: file unreadable
rationale: >
  Invalid JSON lines break the pipeline.
  Any corruption requires investigation.
```

**Measurement:**
```bash
# Validate all lines
python -c "import json; [json.loads(l) for l in open('events.jsonl')]" && echo "OK"
```

### H5: Event Coverage

```yaml
signal: lua_mod.event_types_seen
source: distinct event_type values in file
threshold:
  healthy: >= 5 event types
  warning: 1-4 event types
  critical: 0 event types
rationale: >
  A working mod should emit multiple event types.
  Single-type or empty files suggest broken hooks.
```

**Measurement:**
```bash
# Count distinct event types
jq -r '.event_type' events.jsonl | sort -u | wc -l
```

---

## HEALTH CHECK PROCEDURE

### Manual Check

```bash
#!/bin/bash
# health_check_lua_mod.sh

FILE="$HOME/Documents/Civ6LivingNarrator/events/events.jsonl"

echo "=== Lua Mod Health Check ==="

# 1. File exists
if [ -f "$FILE" ]; then
    echo "[OK] File exists"
else
    echo "[CRITICAL] File not found"
    exit 1
fi

# 2. File size
SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE")
SIZE_MB=$((SIZE / 1024 / 1024))
echo "[INFO] File size: ${SIZE_MB}MB"
if [ $SIZE_MB -gt 50 ]; then
    echo "[CRITICAL] File too large"
elif [ $SIZE_MB -gt 10 ]; then
    echo "[WARNING] File growing large"
else
    echo "[OK] File size healthy"
fi

# 3. JSON validity
if python -c "import json; [json.loads(l) for l in open('$FILE')]" 2>/dev/null; then
    echo "[OK] All lines valid JSON"
else
    echo "[CRITICAL] Invalid JSON detected"
fi

# 4. Event types
TYPES=$(jq -r '.event_type' "$FILE" 2>/dev/null | sort -u | wc -l)
echo "[INFO] Distinct event types: $TYPES"
if [ $TYPES -ge 5 ]; then
    echo "[OK] Good event coverage"
elif [ $TYPES -ge 1 ]; then
    echo "[WARNING] Limited event types"
else
    echo "[CRITICAL] No events"
fi

# 5. Recent activity
LAST_MOD=$(stat -c %Y "$FILE" 2>/dev/null || stat -f %m "$FILE")
NOW=$(date +%s)
AGE=$((NOW - LAST_MOD))
if [ $AGE -lt 300 ]; then
    echo "[OK] File recently modified (${AGE}s ago)"
else
    echo "[WARNING] File stale (${AGE}s since last write)"
fi

echo "=== Check Complete ==="
```

---

## MONITORING DASHBOARD

| Metric | Source | Update Frequency |
|--------|--------|------------------|
| File size | `stat events.jsonl` | Every 5 min |
| Line count | `wc -l events.jsonl` | Every 5 min |
| Last modified | File mtime | Every 1 min |
| Event type distribution | `jq .event_type \| uniq -c` | Every 10 min |

---

## FAILURE MODES

### F1: File Handle Lost

```
Symptom: Events stop appearing despite game activity
Cause: File handle closed or path invalid
Recovery: Restart game, check mod initialization logs
```

### F2: Disk Full

```
Symptom: Write errors in game console
Cause: Disk space exhausted
Recovery: Clear old files, implement rotation
```

### F3: Permission Denied

```
Symptom: Mod fails to create events directory
Cause: Restricted Documents folder
Recovery: Run game as admin or change output path
```

### F4: JSON Serialization Crash

```
Symptom: Game crash or event loss
Cause: Unexpected data type in event payload
Recovery: Add type guards in SerializeToJSON()
```

---

## CURRENT STATUS

```yaml
status: NOT_IMPLEMENTED
last_check: n/a
notes: >
  Module exists only as documentation.
  Lua mod not yet created.
```

---

## MARKERS

<!-- @ngram:todo Implement health check script -->
<!-- @ngram:todo Add in-game logging for debug mode -->
