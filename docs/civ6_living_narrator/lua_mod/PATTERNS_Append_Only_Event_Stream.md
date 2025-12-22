# Lua Mod — Patterns: Append-Only Event Stream

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
THIS:           ./PATTERNS_Append_Only_Event_Stream.md
ALGORITHM:      ./ALGORITHM_Hook_Serialize_Append.md
VALIDATION:     ./VALIDATION_Event_Schema_And_File_Integrity.md
IMPLEMENTATION: ./IMPLEMENTATION_Mod_Files_And_Hooks.md
HEALTH:         ./HEALTH_Event_Lag_And_File_Growth.md
SYNC:           ./SYNC_Lua_Mod_Status.md

IMPL:           (not yet created)
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_*.md: "Docs updated, implementation needs: {what}"

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_*.md: "Implementation changed, docs need: {what}"

---

## THE PROBLEM

The narrator pipeline runs on WSL but needs real-time access to Civ 6 game events.
Civ 6 runs on Windows. The two environments can't share memory or sockets easily.

Without a bridge, the narrator is blind to what's happening in the game.

---

## THE PATTERN

Use an **append-only JSONL file** as a one-way channel from game to pipeline.

```
┌─────────────────────────────────────────────────────────────────┐
│                         WINDOWS                                  │
│  ┌─────────────┐     ┌──────────────────────────────────────┐   │
│  │   Civ 6     │────▶│  events.jsonl                        │   │
│  │  (Lua mod)  │     │  C:\Users\X\Documents\Civ6Narrator\  │   │
│  └─────────────┘     └──────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    │ (file visible via /mnt/c/)
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                           WSL                                    │
│  ┌──────────────────────────────────────────┐                   │
│  │  Pipeline (tail -f equivalent)           │                   │
│  │  /mnt/c/Users/X/Documents/.../events.jsonl                   │
│  └──────────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

**Key insight:** File append is atomic at the line level. Each event is one line.
The pipeline tails the file and sees new lines as they appear.

---

## BEHAVIORS SUPPORTED

- B1-B7: All event capture behaviors — Lua hooks write to the file
- Pipeline integration — file tailing is a solved problem

## BEHAVIORS PREVENTED

- A1: No blocking — file append is fast and non-blocking in Lua
- A2: No corruption — one complete JSON object per line, atomic writes

---

## PRINCIPLES

### Principle 1: One event, one line

Each game event becomes exactly one line in the JSONL file.
No multi-line JSON. No streaming within a line.
This makes tailing trivial and parsing robust.

### Principle 2: Emit first, filter later

The mod should emit events generously.
The decision engine downstream will decide what's worth narrating.
This keeps the mod simple and the intelligence in Python.

### Principle 3: Timestamped and typed

Every event carries:
- `event_type`: string identifying the event category
- `turn`: current game turn number
- `timestamp`: game timestamp or real-world time
- Type-specific payload fields

This enables the pipeline to order, dedupe, and contextualize.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `C:\Users\{user}\Documents\Civ6LivingNarrator\events\events.jsonl` | FILE | Append-only event stream |
| Civ 6 game state | RUNTIME | Source of all event data |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| Civ 6 Lua API | Provides game event hooks |
| Civ 6 mod system | Loads and runs our Lua code |

---

## INSPIRATIONS

- Unix philosophy: plain text as universal interface
- Kafka-style append-only logs
- systemd journal (structured logging)

---

## SCOPE

### In Scope

- Hooking into Civ 6 game events
- Serializing events to JSON
- Appending to the events file
- Basic event schema definition

### Out of Scope

- Event filtering or importance scoring → see: decision_engine
- Reading events or tailing the file → see: ingest
- File rotation or cleanup → see: win_wsl_bridge
- Audio or TTS → see: audio_runtime_windows

---

## MARKERS

<!-- @ngram:todo Implement the Lua mod with core event hooks -->
<!-- @ngram:todo Define complete event schema for all supported event types -->
<!-- @ngram:escalation Need to verify Civ 6 Lua API availability for all desired events -->
