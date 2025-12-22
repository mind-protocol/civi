# Lua Mod — Implementation: Mod Files and Hooks

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
THIS:           ./IMPLEMENTATION_Mod_Files_And_Hooks.md
HEALTH:         ./HEALTH_Event_Lag_And_File_Growth.md
SYNC:           ./SYNC_Lua_Mod_Status.md

IMPL:           (not yet created)
```

### Bidirectional Contract

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## DIRECTORY STRUCTURE

```
civ6_living_narrator_mod/
├── LivingNarrator.modinfo          # Mod metadata for Civ 6
├── Scripts/
│   ├── LivingNarrator.lua          # Main event handler
│   ├── JSONSerializer.lua          # JSON serialization utils
│   └── FileWriter.lua              # File I/O wrapper
└── README.md                       # Installation instructions
```

**Installation path:**
```
%USERPROFILE%\Documents\My Games\Sid Meier's Civilization VI\Mods\LivingNarrator\
```

---

## FILE DESCRIPTIONS

### LivingNarrator.modinfo

```xml
<?xml version="1.0" encoding="utf-8"?>
<Mod id="living-narrator" version="1.0">
    <Properties>
        <Name>Living Narrator</Name>
        <Description>Exports game events for external narration</Description>
        <Authors>civ6-living-narrator</Authors>
    </Properties>
    <Components>
        <GameplayScripts>
            <File>Scripts/LivingNarrator.lua</File>
        </GameplayScripts>
    </Components>
</Mod>
```

### LivingNarrator.lua (entry point)

```lua
-- DOCS: docs/civ6_living_narrator/lua_mod/IMPLEMENTATION_Mod_Files_And_Hooks.md

include("JSONSerializer")
include("FileWriter")

-- Initialize on game load
function Initialize()
    print("[LivingNarrator] Initializing...")
    InitializeEventFile()
    RegisterEventHandlers()
    print("[LivingNarrator] Ready")
end

function RegisterEventHandlers()
    -- Turn events
    Events.TurnBegin.Add(OnTurnBegin)

    -- City events
    Events.CityInitialized.Add(OnCityFounded)
    Events.CityConquered.Add(OnCityCaptured)

    -- Wonder events
    Events.WonderCompleted.Add(OnWonderCompleted)

    -- Diplomacy events
    Events.DiplomacyDeclareWar.Add(OnWarDeclared)
    Events.DiplomacyMakePeace.Add(OnPeaceMade)

    -- Research events
    Events.ResearchCompleted.Add(OnTechCompleted)
    Events.CivicCompleted.Add(OnCivicCompleted)

    -- Great person events
    Events.UnitGreatPersonActivated.Add(OnGreatPersonEarned)
end

-- Event handlers
function OnTurnBegin(playerID)
    if playerID == Game.GetLocalPlayer() then
        EmitEvent("TURN_START", {
            player_id = playerID,
            player_civ = GetCivName(playerID)
        })
    end
end

function OnCityFounded(playerID, cityID, x, y)
    local city = CityManager.GetCity(playerID, cityID)
    EmitEvent("CITY_BUILT", {
        city_name = city:GetName(),
        player_id = playerID,
        player_civ = GetCivName(playerID),
        x = x,
        y = y
    })
end

-- ... additional handlers ...

-- Core emission function
function EmitEvent(eventType, data)
    local event = {
        event_type = eventType,
        turn = Game.GetCurrentGameTurn(),
        timestamp = os.time()
    }

    for k, v in pairs(data) do
        event[k] = v
    end

    local json = SerializeToJSON(event)
    AppendLine(json)
end

-- Helper
function GetCivName(playerID)
    local config = PlayerConfigurations[playerID]
    if config then
        return Locale.Lookup(config:GetCivilizationShortDescription())
    end
    return "Unknown"
end

-- Start
Initialize()
```

---

## DATA FLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                      Civ 6 Game Engine                          │
│                                                                 │
│   Events.TurnBegin ─────┐                                       │
│   Events.CityInitialized ──┼───▶ LivingNarrator.lua            │
│   Events.WonderCompleted ──┘           │                        │
│                                        ▼                        │
│                              ┌──────────────────┐               │
│                              │  EmitEvent()     │               │
│                              │  - Build payload │               │
│                              │  - Add metadata  │               │
│                              └────────┬─────────┘               │
│                                       ▼                         │
│                              ┌──────────────────┐               │
│                              │ SerializeToJSON()│               │
│                              └────────┬─────────┘               │
│                                       ▼                         │
│                              ┌──────────────────┐               │
│                              │  AppendLine()    │               │
│                              │  - Write to file │               │
│                              │  - Flush         │               │
│                              └────────┬─────────┘               │
└───────────────────────────────────────┼─────────────────────────┘
                                        ▼
                    ┌─────────────────────────────────────┐
                    │  events.jsonl                       │
                    │  Documents/Civ6LivingNarrator/      │
                    └─────────────────────────────────────┘
```

---

## CIV 6 LUA API REFERENCE

### Key Events

| Event | Parameters | When Fired |
|-------|------------|------------|
| `Events.TurnBegin` | `playerID` | Start of each player's turn |
| `Events.CityInitialized` | `playerID, cityID, x, y` | City founded |
| `Events.CityConquered` | `newOwnerID, oldOwnerID, cityID` | City captured |
| `Events.WonderCompleted` | `x, y, buildingID, playerID` | Wonder finished |
| `Events.DiplomacyDeclareWar` | `attackerID, defenderID` | War declared |
| `Events.ResearchCompleted` | `playerID, techID` | Tech researched |
| `Events.CivicCompleted` | `playerID, civicID` | Civic completed |

### Key Functions

| Function | Returns | Purpose |
|----------|---------|---------|
| `Game.GetCurrentGameTurn()` | integer | Current turn number |
| `Game.GetLocalPlayer()` | playerID | Human player ID |
| `CityManager.GetCity(playerID, cityID)` | City | City object |
| `PlayerConfigurations[playerID]` | Config | Player config |

---

## ERROR HANDLING

```lua
-- Wrap all emissions in pcall for safety
function SafeEmitEvent(eventType, data)
    local success, err = pcall(function()
        EmitEvent(eventType, data)
    end)

    if not success then
        print("[LivingNarrator] Error: " .. tostring(err))
    end
end
```

---

## INSTALLATION

1. Copy mod folder to Civ 6 mods directory
2. Enable mod in Additional Content menu
3. Start a new game or load existing save
4. Events will appear in `Documents/Civ6LivingNarrator/events/events.jsonl`

---

## MARKERS

<!-- @ngram:todo Create actual Lua files from this spec -->
<!-- @ngram:todo Test with Civ 6 Gathering Storm expansion -->
<!-- @ngram:escalation Verify mod compatibility with latest Civ 6 patch -->
