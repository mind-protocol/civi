# Lua Mod — Algorithm: Hook, Serialize, Append

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
THIS:           ./ALGORITHM_Hook_Serialize_Append.md
VALIDATION:     ./VALIDATION_Event_Schema_And_File_Integrity.md
IMPLEMENTATION: ./IMPLEMENTATION_Mod_Files_And_Hooks.md
HEALTH:         ./HEALTH_Event_Lag_And_File_Growth.md
SYNC:           ./SYNC_Lua_Mod_Status.md

IMPL:           (not yet created)
```

### Bidirectional Contract

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC.

---

## OVERVIEW

The mod lifecycle: initialize once, then respond to game events by appending JSON lines.

```
STARTUP:
  1. Resolve output file path
  2. Register event handlers with Civ 6 API
  3. Open file handle in append mode

RUNTIME (per event):
  1. Receive event from game
  2. Build event payload
  3. Serialize to JSON
  4. Append line to file
  5. Flush (optional, for low-latency)

SHUTDOWN:
  1. Close file handle (automatic on game exit)
```

---

## ALGORITHM: Event Emission

### Inputs

- Game event callback with event-specific parameters
- Current game state (turn number, player info)

### Outputs

- One JSON line appended to `events.jsonl`

### Procedure

```lua
function OnGameEvent(eventType, eventData)
    -- 1. Build base event structure
    local event = {
        event_type = eventType,
        turn = Game.GetCurrentGameTurn(),
        timestamp = os.time(),
        game_id = GetGameID()  -- session identifier
    }

    -- 2. Merge event-specific data
    for key, value in pairs(eventData) do
        event[key] = value
    end

    -- 3. Serialize to JSON
    local json_line = SerializeToJSON(event)

    -- 4. Append to file
    AppendLine(json_line)
end
```

---

## ALGORITHM: JSON Serialization

Civ 6 Lua doesn't have native JSON support. Use a minimal serializer.

```lua
function SerializeToJSON(obj)
    if type(obj) == "string" then
        -- Escape special characters
        return '"' .. EscapeString(obj) .. '"'
    elseif type(obj) == "number" then
        return tostring(obj)
    elseif type(obj) == "boolean" then
        return obj and "true" or "false"
    elseif type(obj) == "nil" then
        return "null"
    elseif type(obj) == "table" then
        -- Check if array or object
        if IsArray(obj) then
            return SerializeArray(obj)
        else
            return SerializeObject(obj)
        end
    end
end

function EscapeString(s)
    return s:gsub('\\', '\\\\')
            :gsub('"', '\\"')
            :gsub('\n', '\\n')
            :gsub('\r', '\\r')
            :gsub('\t', '\\t')
end
```

---

## ALGORITHM: File Append

```lua
-- Global file handle (opened once at startup)
local g_EventFile = nil
local g_FilePath = nil

function InitializeEventFile()
    -- Resolve path: Documents/Civ6LivingNarrator/events/events.jsonl
    local docs = os.getenv("USERPROFILE") .. "\\Documents"
    g_FilePath = docs .. "\\Civ6LivingNarrator\\events\\events.jsonl"

    -- Ensure directory exists
    os.execute('mkdir "' .. docs .. '\\Civ6LivingNarrator\\events" 2>nul')

    -- Open in append mode
    g_EventFile = io.open(g_FilePath, "a")
end

function AppendLine(json_line)
    if g_EventFile then
        g_EventFile:write(json_line .. "\n")
        g_EventFile:flush()  -- Ensure immediate visibility
    end
end
```

---

## EVENT TYPE HANDLERS

### Turn Start

```lua
Events.TurnBegin.Add(function(player)
    if player == Game.GetLocalPlayer() then
        OnGameEvent("TURN_START", {
            player_id = player,
            player_civ = GetPlayerCivName(player)
        })
    end
end)
```

### City Founded

```lua
Events.CityInitialized.Add(function(playerID, cityID)
    local city = Cities.GetCityInPlot(cityID)
    OnGameEvent("CITY_BUILT", {
        city_name = city:GetName(),
        player_id = playerID,
        player_civ = GetPlayerCivName(playerID),
        x = city:GetX(),
        y = city:GetY()
    })
end)
```

### Wonder Completed

```lua
Events.WonderCompleted.Add(function(x, y, buildingID, playerID)
    OnGameEvent("WONDER_COMPLETED", {
        wonder = GameInfo.Buildings[buildingID].Name,
        player_id = playerID,
        player_civ = GetPlayerCivName(playerID),
        x = x,
        y = y
    })
end)
```

### War Declared

```lua
Events.DiplomacyDeclareWar.Add(function(attackerID, defenderID)
    OnGameEvent("WAR_DECLARED", {
        attacker_id = attackerID,
        attacker_civ = GetPlayerCivName(attackerID),
        defender_id = defenderID,
        defender_civ = GetPlayerCivName(defenderID)
    })
end)
```

---

## ERROR HANDLING

```lua
function SafeAppendLine(json_line)
    local success, err = pcall(function()
        AppendLine(json_line)
    end)

    if not success then
        -- Log to Civ 6 console, don't crash the game
        print("[LivingNarrator] Write error: " .. tostring(err))

        -- Try to reopen file
        if g_EventFile then
            g_EventFile:close()
        end
        g_EventFile = io.open(g_FilePath, "a")
    end
end
```

---

## COMPLEXITY

- Time: O(1) per event (JSON serialization is linear in event size, but events are small)
- Space: O(1) memory (no event buffering)
- File growth: O(n) where n = number of events

---

## MARKERS

<!-- @ngram:todo Verify all Civ 6 Lua API event names are correct -->
<!-- @ngram:todo Test JSON serialization with edge cases (unicode, special chars) -->
