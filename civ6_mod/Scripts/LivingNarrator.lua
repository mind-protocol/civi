-- LivingNarrator.lua - SINGLE FILE VERSION v2.5
-- All-in-one: JSON + FileWriter + Events
-- No dependencies, no include(), no ExposedMembers

print("========================================")
print("[LivingNarrator] Loading v2.5...")
print("========================================")

-- ============================================================================
-- JSON SERIALIZER (inline)
-- ============================================================================

local function EscapeString(s)
    if s == nil then return "" end
    s = tostring(s)
    s = s:gsub('\\', '\\\\')
    s = s:gsub('"', '\\"')
    s = s:gsub('\n', '\\n')
    s = s:gsub('\r', '\\r')
    s = s:gsub('\t', '\\t')
    return s
end

local function IsArray(t)
    if type(t) ~= "table" then return false end
    local count = 0
    for k, v in pairs(t) do
        if type(k) ~= "number" or k <= 0 or math.floor(k) ~= k then
            return false
        end
        count = count + 1
    end
    for i = 1, count do
        if t[i] == nil then return false end
    end
    return true
end

local SerializeValue
SerializeValue = function(value)
    local t = type(value)
    if t == "nil" then
        return "null"
    elseif t == "boolean" then
        return value and "true" or "false"
    elseif t == "number" then
        if value ~= value then return "null" end
        if value == math.huge or value == -math.huge then return "null" end
        if math.floor(value) == value then
            return string.format("%d", value)
        else
            return string.format("%.6g", value)
        end
    elseif t == "string" then
        return '"' .. EscapeString(value) .. '"'
    elseif t == "table" then
        local parts = {}
        if IsArray(value) then
            for i, v in ipairs(value) do
                parts[i] = SerializeValue(v)
            end
            return "[" .. table.concat(parts, ",") .. "]"
        else
            local keys = {}
            for k in pairs(value) do
                if type(k) == "string" then
                    table.insert(keys, k)
                end
            end
            table.sort(keys)
            for _, k in ipairs(keys) do
                table.insert(parts, '"' .. EscapeString(k) .. '":' .. SerializeValue(value[k]))
            end
            return "{" .. table.concat(parts, ",") .. "}"
        end
    else
        return "null"
    end
end

local function SerializeToJSON(obj)
    local ok, result = pcall(function() return SerializeValue(obj) end)
    if ok then return result else return '{"error":"serialize_failed"}' end
end

print("[LivingNarrator] JSON OK")

-- ============================================================================
-- FILE WRITER (Print Mode - outputs to Lua.log)
-- ============================================================================

local g_Initialized = false
local g_WriteCount = 0

local function InitializeFiles()
    if g_Initialized then return true end
    g_Initialized = true
    print("[LivingNarrator] Event logging initialized (Print Mode)")
    return true
end

local function AppendEvent(eventData)
    if not g_Initialized then
        if not InitializeFiles() then return false end
    end
    local json = SerializeToJSON(eventData)
    print("[LN_EVENT]" .. json)
    g_WriteCount = g_WriteCount + 1
    return true
end

print("[LivingNarrator] FileWriter OK")

-- ============================================================================
-- HELPERS
-- ============================================================================

local g_GameID = "game_" .. os.time()
local g_Turn = 0

local function GetCivName(playerID)
    if playerID == nil or playerID < 0 then return "Unknown" end
    local ok, result = pcall(function()
        local cfg = PlayerConfigurations[playerID]
        if cfg then
            local name = cfg:GetCivilizationShortDescription()
            if name then return Locale.Lookup(name) end
        end
        return "Player" .. playerID
    end)
    return ok and result or "Player" .. playerID
end

local function GetLeaderName(playerID)
    if playerID == nil or playerID < 0 then return "Unknown" end
    local ok, result = pcall(function()
        local cfg = PlayerConfigurations[playerID]
        if cfg then
            local name = cfg:GetLeaderName()
            if name then return Locale.Lookup(name) end
        end
        return "Leader" .. playerID
    end)
    return ok and result or "Leader" .. playerID
end

local function IsHumanPlayer(playerID)
    if playerID == nil or playerID < 0 then return false end
    local ok, result = pcall(function()
        local cfg = PlayerConfigurations[playerID]
        if cfg and cfg.IsHuman then
            return cfg:IsHuman()
        end
        return false
    end)
    return ok and result or false
end

local function EmitEvent(eventType, data)
    local event = {
        type = eventType,
        turn = g_Turn,
        ts = os.time(),
        game_id = g_GameID
    }
    if data then
        for k, v in pairs(data) do
            event[k] = v
        end
    end

    local ok = AppendEvent(event)
    if ok then
        print("[LivingNarrator] Event: " .. eventType)
    end
    return ok
end

local function GetUnitTypeName(unitType)
    local ok, result = pcall(function()
        local info = GameInfo.Units[unitType]
        if info then
            return Locale.Lookup(info.Name)
        end
        return "Unit"
    end)
    return ok and result or "Unit"
end

local function CountPlayerUnits(playerID)
    local ok, result = pcall(function()
        local player = Players[playerID]
        if not player then return {military = 0, civilian = 0} end
        local units = player:GetUnits()
        if not units then return {military = 0, civilian = 0} end

        local military = 0
        local civilian = 0
        for i, unit in units:Members() do
            local unitType = unit:GetType()
            local info = GameInfo.Units[unitType]
            if info and info.Combat and info.Combat > 0 then
                military = military + 1
            else
                civilian = civilian + 1
            end
        end
        return {military = military, civilian = civilian}
    end)
    return ok and result or {military = 0, civilian = 0}
end

-- ============================================================================
-- EVENT HANDLERS
-- ============================================================================

local function OnTurnBegin(playerID)
    local ok, err = pcall(function()
        g_Turn = Game.GetCurrentGameTurn()
        if IsHumanPlayer(playerID) then
            EmitEvent("TURN_START", {
                player_id = playerID,
                player_civ = GetCivName(playerID)
            })
            -- Emit turn summary with unit counts
            local counts = CountPlayerUnits(playerID)
            local player = Players[playerID]
            local cityCount = 0
            if player and player.GetCities then
                local cities = player:GetCities()
                if cities then cityCount = cities:GetCount() end
            end
            EmitEvent("TURN_SUMMARY", {
                player_id = playerID,
                player_civ = GetCivName(playerID),
                military_units = counts.military,
                civilian_units = counts.civilian,
                cities = cityCount
            })
        end
    end)
    if not ok then print("[LivingNarrator] OnTurnBegin error: " .. tostring(err)) end
end

local function OnTurnEnd(playerID)
    local ok, err = pcall(function()
        if IsHumanPlayer(playerID) then
            EmitEvent("TURN_END", {
                player_id = playerID,
                player_civ = GetCivName(playerID)
            })
        end
    end)
    if not ok then print("[LivingNarrator] OnTurnEnd error: " .. tostring(err)) end
end

local function OnCityBuilt(playerID, cityID, x, y)
    local ok, err = pcall(function()
        local cityName = "City"
        local player = Players[playerID]
        if player then
            local city = player:GetCities():FindID(cityID)
            if city then
                local rawName = city:GetName()
                cityName = Locale.Lookup(rawName) or rawName
            end
        end
        EmitEvent("CITY_BUILT", {
            city = cityName,
            player_id = playerID,
            player_civ = GetCivName(playerID),
            x = x, y = y
        })
    end)
    if not ok then print("[LivingNarrator] OnCityBuilt error: " .. tostring(err)) end
end

local function OnCityCaptured(newOwner, oldOwner, cityID)
    local ok, err = pcall(function()
        EmitEvent("CITY_CAPTURED", {
            new_owner = GetCivName(newOwner),
            old_owner = GetCivName(oldOwner)
        })
    end)
    if not ok then print("[LivingNarrator] OnCityCaptured error: " .. tostring(err)) end
end

local function OnWonderCompleted(x, y, buildingID, playerID)
    local ok, err = pcall(function()
        local info = GameInfo.Buildings[buildingID]
        EmitEvent("WONDER_COMPLETED", {
            wonder = info and Locale.Lookup(info.Name) or "Wonder",
            player_civ = GetCivName(playerID)
        })
    end)
    if not ok then print("[LivingNarrator] OnWonderCompleted error: " .. tostring(err)) end
end

local function OnWarDeclared(attacker, defender)
    local ok, err = pcall(function()
        EmitEvent("WAR_DECLARED", {
            attacker = GetCivName(attacker),
            defender = GetCivName(defender)
        })
    end)
    if not ok then print("[LivingNarrator] OnWarDeclared error: " .. tostring(err)) end
end

local function OnPeace(p1, p2)
    local ok, err = pcall(function()
        EmitEvent("PEACE_MADE", {
            player1 = GetCivName(p1),
            player2 = GetCivName(p2)
        })
    end)
    if not ok then print("[LivingNarrator] OnPeace error: " .. tostring(err)) end
end

local function OnTechCompleted(playerID, techID)
    local ok, err = pcall(function()
        if IsHumanPlayer(playerID) then
            local info = GameInfo.Technologies[techID]
            EmitEvent("TECH_COMPLETED", {
                tech = info and Locale.Lookup(info.Name) or "Tech",
                player_civ = GetCivName(playerID)
            })
        end
    end)
    if not ok then print("[LivingNarrator] OnTechCompleted error: " .. tostring(err)) end
end

local function OnCivicCompleted(playerID, civicID)
    local ok, err = pcall(function()
        if IsHumanPlayer(playerID) then
            local info = GameInfo.Civics[civicID]
            EmitEvent("CIVIC_COMPLETED", {
                civic = info and Locale.Lookup(info.Name) or "Civic",
                player_civ = GetCivName(playerID)
            })
        end
    end)
    if not ok then print("[LivingNarrator] OnCivicCompleted error: " .. tostring(err)) end
end

local function OnUnitKilled(killedPlayer, killedUnitID, killerPlayer, killerUnitID)
    local ok, err = pcall(function()
        if IsHumanPlayer(killedPlayer) or IsHumanPlayer(killerPlayer) then
            -- Get unit details if available
            local killedName = "Unit"
            local killerName = "Unit"
            local x, y = 0, 0

            local killedPlayerObj = Players[killedPlayer]
            if killedPlayerObj then
                local unit = killedPlayerObj:GetUnits():FindID(killedUnitID)
                if unit then
                    killedName = GetUnitTypeName(unit:GetType())
                    x, y = unit:GetX(), unit:GetY()
                end
            end

            local killerPlayerObj = Players[killerPlayer]
            if killerPlayerObj then
                local unit = killerPlayerObj:GetUnits():FindID(killerUnitID)
                if unit then
                    killerName = GetUnitTypeName(unit:GetType())
                end
            end

            EmitEvent("UNIT_KILLED", {
                killed_civ = GetCivName(killedPlayer),
                killed_unit = killedName,
                killer_civ = GetCivName(killerPlayer),
                killer_unit = killerName,
                x = x, y = y
            })
        end
    end)
    if not ok then print("[LivingNarrator] OnUnitKilled error: " .. tostring(err)) end
end

local function OnWonderStarted(x, y, buildingID, playerID)
    local ok, err = pcall(function()
        local info = GameInfo.Buildings[buildingID]
        if info and info.IsWonder then
            EmitEvent("WONDER_STARTED", {
                wonder = Locale.Lookup(info.Name),
                player_civ = GetCivName(playerID),
                x = x, y = y
            })
        end
    end)
    if not ok then print("[LivingNarrator] OnWonderStarted error: " .. tostring(err)) end
end

local function OnDenounce(actingPlayer, targetPlayer)
    local ok, err = pcall(function()
        EmitEvent("DENOUNCEMENT", {
            actor = GetCivName(actingPlayer),
            target = GetCivName(targetPlayer)
        })
    end)
    if not ok then print("[LivingNarrator] OnDenounce error: " .. tostring(err)) end
end

local function OnAlliance(player1, player2, allianceType)
    local ok, err = pcall(function()
        EmitEvent("ALLIANCE_FORMED", {
            player1 = GetCivName(player1),
            player2 = GetCivName(player2),
            alliance_type = allianceType or "unknown"
        })
    end)
    if not ok then print("[LivingNarrator] OnAlliance error: " .. tostring(err)) end
end

local function OnUnitCreated(playerID, unitID)
    local ok, err = pcall(function()
        local player = Players[playerID]
        if player then
            local unit = player:GetUnits():FindID(unitID)
            if unit then
                local unitType = unit:GetType()
                local unitName = GetUnitTypeName(unitType)
                local info = GameInfo.Units[unitType]
                local isMilitary = info and info.Combat and info.Combat > 0
                EmitEvent("UNIT_CREATED", {
                    player_id = playerID,
                    player_civ = GetCivName(playerID),
                    unit_name = unitName,
                    is_military = isMilitary or false
                })
            end
        end
    end)
    if not ok then print("[LivingNarrator] OnUnitCreated error: " .. tostring(err)) end
end

-- ============================================================================
-- SAFE EVENT REGISTRATION
-- ============================================================================

local function SafeAdd(eventTable, handler, name)
    if eventTable and eventTable.Add then
        local ok, err = pcall(function()
            eventTable.Add(handler)
        end)
        if ok then
            print("[LivingNarrator] + " .. name)
            return true
        else
            print("[LivingNarrator] - " .. name .. " (error: " .. tostring(err) .. ")")
            return false
        end
    else
        print("[LivingNarrator] - " .. name .. " (not available)")
        return false
    end
end

local function RegisterEventHandlers()
    print("[LivingNarrator] Registering events...")

    local count = 0

    if SafeAdd(Events.TurnBegin, OnTurnBegin, "TurnBegin") then count = count + 1 end
    if SafeAdd(Events.TurnEnd, OnTurnEnd, "TurnEnd") then count = count + 1 end
    if SafeAdd(Events.CityInitialized, OnCityBuilt, "CityInitialized") then count = count + 1 end
    if SafeAdd(Events.CityConquered, OnCityCaptured, "CityConquered") then count = count + 1 end
    if SafeAdd(Events.WonderCompleted, OnWonderCompleted, "WonderCompleted") then count = count + 1 end
    if SafeAdd(Events.DiplomacyDeclareWar, OnWarDeclared, "DiplomacyDeclareWar") then count = count + 1 end
    if SafeAdd(Events.DiplomacyMakePeace, OnPeace, "DiplomacyMakePeace") then count = count + 1 end
    if SafeAdd(Events.ResearchCompleted, OnTechCompleted, "ResearchCompleted") then count = count + 1 end
    if SafeAdd(Events.CivicCompleted, OnCivicCompleted, "CivicCompleted") then count = count + 1 end
    if SafeAdd(Events.UnitKilledInCombat, OnUnitKilled, "UnitKilledInCombat") then count = count + 1 end
    if SafeAdd(Events.UnitAddedToMap, OnUnitCreated, "UnitAddedToMap") then count = count + 1 end
    if SafeAdd(Events.BuildingAddedToMap, OnWonderStarted, "BuildingAddedToMap") then count = count + 1 end
    if SafeAdd(Events.DiplomacyDenounce, OnDenounce, "DiplomacyDenounce") then count = count + 1 end
    if SafeAdd(Events.DiplomacyRelationshipChanged, OnAlliance, "DiplomacyRelationshipChanged") then count = count + 1 end

    print("[LivingNarrator] " .. count .. " events registered")
end

-- ============================================================================
-- INITIALIZATION
-- ============================================================================

local function Initialize()
    print("[LivingNarrator] Init...")

    if not InitializeFiles() then
        print("[LivingNarrator] FATAL: Cannot init files")
        return
    end

    local ok, err = pcall(function()
        g_Turn = Game.GetCurrentGameTurn()
    end)
    if not ok then
        g_Turn = 0
    end

    RegisterEventHandlers()

    local localPlayer = -1
    ok, err = pcall(function()
        localPlayer = Game.GetLocalPlayer()
    end)

    EmitEvent("GAME_START", {
        local_player = localPlayer,
        local_civ = GetCivName(localPlayer),
        version = "2.5"
    })

    print("========================================")
    print("[LivingNarrator] READY! v2.5")
    print("========================================")
end

Initialize()
