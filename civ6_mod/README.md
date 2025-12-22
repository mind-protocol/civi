# Living Narrator - Civ 6 Event Exporter Mod

This mod captures Civilization VI game events and exports them to a JSONL file for consumption by the Living Narrator AI system.

## Installation

### 1. Locate Your Mods Folder

```
Windows: %USERPROFILE%\Documents\My Games\Sid Meier's Civilization VI\Mods\
```

Typical path:
```
C:\Users\YourName\Documents\My Games\Sid Meier's Civilization VI\Mods\
```

### 2. Copy the Mod

Copy the entire `civ6_mod` folder to your Mods directory and rename it:

```
Mods\
└── LivingNarrator\
    ├── LivingNarrator.modinfo
    └── Scripts\
        ├── JSONSerializer.lua
        ├── FileWriter.lua
        └── LivingNarrator.lua
```

### 3. Enable the Mod

1. Launch Civilization VI
2. Go to **Additional Content**
3. Find **Living Narrator - Event Exporter**
4. Enable it
5. Start a new game (or load an existing save)

## Output

Events are written to:
```
%USERPROFILE%\Documents\Civ6LivingNarrator\events\events.jsonl
```

Example path:
```
C:\Users\YourName\Documents\Civ6LivingNarrator\events\events.jsonl
```

## Event Types

| Event | When Fired |
|-------|------------|
| `GAME_START` | Game loaded with mod |
| `TURN_START` | Human player's turn begins |
| `TURN_END` | Human player's turn ends |
| `CITY_BUILT` | Any city founded |
| `CITY_CAPTURED` | City changes hands |
| `CITY_RAZED` | City destroyed |
| `WONDER_COMPLETED` | Wonder finished |
| `WAR_DECLARED` | War breaks out |
| `PEACE_MADE` | Peace treaty signed |
| `TECH_COMPLETED` | Human player researches tech |
| `CIVIC_COMPLETED` | Human player completes civic |
| `GREAT_PERSON_EARNED` | Great person recruited |
| `RELIGION_FOUNDED` | New religion created |
| `UNIT_KILLED` | Combat involving human player |

## Event Format

Each line is a JSON object:

```json
{"event_type":"TURN_START","turn":42,"timestamp":1703275200,"game_id":"game_1703275100_4521","player_id":0,"player_civ":"Egypt","player_leader":"Cleopatra","is_local":true}
```

Base fields (all events):
- `event_type`: String identifying the event
- `turn`: Current game turn number
- `timestamp`: Unix timestamp (seconds)
- `game_id`: Unique session identifier

## Console Commands

In-game Lua console (` key), you can run:

```lua
LN_Status()     -- Show mod status and statistics
LN_TestEvent()  -- Emit a test event
```

## Troubleshooting

### Mod Not Loading

- Check that the folder structure is correct
- Ensure `LivingNarrator.modinfo` is in the root of the mod folder
- Try disabling other mods that might conflict

### No Events File

- Check `Documents\Civ6LivingNarrator\events\` exists
- The mod creates the directory on first run
- Run `LN_Status()` in console to check file path

### Events Not Appearing

- Wait for actual game events (start a turn, found a city)
- Check file modification time to see if writes are happening
- Run `LN_TestEvent()` to force a test event

## Integration with Narrator

The WSL narrator pipeline tails this file:

```bash
# From WSL, the file is accessible at:
/mnt/c/Users/YourName/Documents/Civ6LivingNarrator/events/events.jsonl
```

The pipeline (`src/main.py`) will automatically pick up new events.

## Compatibility

- Civilization VI (base game)
- Rise and Fall expansion
- Gathering Storm expansion
- New Frontier Pass

Note: Some events may not be available in older game versions.

## License

Part of the civ6-living-narrator project.
