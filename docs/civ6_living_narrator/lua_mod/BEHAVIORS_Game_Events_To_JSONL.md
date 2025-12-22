# BEHAVIORS — Lua Mod: Game Events to JSONL

```
STATUS: DRAFT
CREATED: 2025-12-22
VERIFIED: n/a (not yet implemented)
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_Event_Extraction_And_Emission.md
THIS:           ./BEHAVIORS_Game_Events_To_JSONL.md
PATTERNS:       ./PATTERNS_Append_Only_Event_Stream.md
ALGORITHM:      ./ALGORITHM_Hook_Serialize_Append.md
VALIDATION:     ./VALIDATION_Event_Schema_And_File_Integrity.md
IMPLEMENTATION: ./IMPLEMENTATION_Mod_Files_And_Hooks.md
HEALTH:         ./HEALTH_Event_Lag_And_File_Growth.md
SYNC:           ./SYNC_Lua_Mod_Status.md

IMPL:           (not yet created)
```

---

## OBSERVABLE BEHAVIORS

### B1: Turn events are captured

```
WHEN:   A new turn begins (player or AI)
THEN:   A TURN_START event is appended to events.jsonl
AND:    The event includes turn number and timestamp
```

### B2: City events are captured

```
WHEN:   A city is founded, captured, or razed
THEN:   A CITY_BUILT, CITY_CAPTURED, or CITY_RAZED event is appended
AND:    The event includes city name and owner civilization
```

### B3: Wonder events are captured

```
WHEN:   A wonder is completed (by player or AI)
THEN:   A WONDER_COMPLETED event is appended
AND:    The event includes wonder name and builder civilization
```

### B4: War and peace events are captured

```
WHEN:   War is declared or peace is made
THEN:   A WAR_DECLARED or PEACE_MADE event is appended
AND:    The event includes both civilizations involved
```

### B5: Great person events are captured

```
WHEN:   A great person is earned or recruited
THEN:   A GREAT_PERSON_EARNED event is appended
AND:    The event includes person type and name
```

### B6: Technology and civic events are captured

```
WHEN:   A technology or civic is completed
THEN:   A TECH_COMPLETED or CIVIC_COMPLETED event is appended
AND:    The event includes the tech/civic name
```

### B7: Victory proximity events are captured

```
WHEN:   A civilization is close to a victory condition
THEN:   A VICTORY_PROXIMITY event is appended
AND:    The event includes victory type and progress indicator
```

---

## ANTI-BEHAVIORS (what must NOT happen)

### A1: No blocking on file I/O

```
NEVER:  Cause the game to freeze or stutter during event writing
```

### A2: No file corruption

```
NEVER:  Write partial JSON lines or corrupt the events file
```

### A3: No event loss on game save/load

```
NEVER:  Lose events when the player saves and reloads
```

---

## BEHAVIOR VERIFICATION

| Behavior | Test Method | Pass Criteria |
|----------|-------------|---------------|
| B1 | Start new turn, check file | TURN_START line present |
| B2 | Found a city, check file | CITY_BUILT line present |
| B3 | Complete wonder, check file | WONDER_COMPLETED line present |
| B4 | Declare war, check file | WAR_DECLARED line present |
| A1 | Profile game with mod | FPS unchanged |
| A2 | Read file after 100 turns | All lines valid JSON |
