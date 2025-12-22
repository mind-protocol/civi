-- DOCS: docs/civ6_living_narrator/lua_mod/IMPLEMENTATION_Mod_Files_And_Hooks.md
-- LivingNarrator.lua - Main event handler for Civ 6 Living Narrator
--
-- Captures game events and exports them as JSONL for external AI narration.
-- Events are written to: Documents/Civ6LivingNarrator/events/events.jsonl

-- Include dependencies (loaded via modinfo)
include("JSONSerializer")
include("FileWriter")

-- ============================================================================
-- CONFIGURATION
-- ============================================================================

local CONFIG = {
    -- Enable/disable specific event categories
    EVENTS = {
        TURNS = true,
        CITIES = true,
        WONDERS = true,
        DIPLOMACY = true,
        COMBAT = true,
        RESEARCH = true,
        GREAT_PEOPLE = true,
        RELIGION = true,
        TRADE = true,
    },
    -- Debug mode
    DEBUG = false,
    -- Version
    VERSION = "1.0.0",
}

-- ============================================================================
-- STATE
-- ============================================================================

local g_CurrentTurn = 0
local g_GameID = nil
local g_LocalPlayerID = nil
local g_EventCount = 0

-- ============================================================================
-- HELPERS
-- ============================================================================

-- Generate a unique game session ID
local function GenerateGameID()
    return string.format("game_%d_%d", os.time(), math.random(1000, 9999))
end

-- Get map dimensions
local function GetMapSize()
    local mapWidth, mapHeight = Map.GetGridSize()
    return mapWidth, mapHeight
end

-- Get civilization name for a player
local function GetCivName(playerID)
    if playerID == nil or playerID < 0 then
        return "Unknown"
    end

    local pPlayerConfig = PlayerConfigurations[playerID]
    if pPlayerConfig then
        local civName = pPlayerConfig:GetCivilizationShortDescription()
        if civName then
            return Locale.Lookup(civName)
        end
    end
    return "Player " .. tostring(playerID)
end

-- Get leader name for a player
local function GetLeaderName(playerID)
    if playerID == nil or playerID < 0 then
        return "Unknown"
    end

    local pPlayerConfig = PlayerConfigurations[playerID]
    if pPlayerConfig then
        local leaderName = pPlayerConfig:GetLeaderName()
        if leaderName then
            return Locale.Lookup(leaderName)
        end
    end
    return "Leader " .. tostring(playerID)
end

-- Get city name by ID
local function GetCityName(playerID, cityID)
    local pPlayer = Players[playerID]
    if pPlayer then
        local pCities = pPlayer:GetCities()
        if pCities then
            local pCity = pCities:FindID(cityID)
            if pCity then
                return pCity:GetName()
            end
        end
    end
    return "Unknown City"
end

-- Check if player is human
local function IsHumanPlayer(playerID)
    local pPlayerConfig = PlayerConfigurations[playerID]
    if pPlayerConfig then
        return pPlayerConfig:IsHuman()
    end
    return false
end

-- ============================================================================
-- STATE COLLECTOR
-- ============================================================================

-- Collect unit data for a player
local function CollectUnits(pPlayer)
    local units = {}
    local pUnits = pPlayer:GetUnits()
    if pUnits then
        for i, pUnit in pUnits:Members() do
            local unitInfo = GameInfo.Units[pUnit:GetType()]
            table.insert(units, {
                id = pUnit:GetID(),
                type = unitInfo and Locale.Lookup(unitInfo.Name) or "Unknown",
                x = pUnit:GetX(),
                y = pUnit:GetY(),
                hp = pUnit:GetDamage() and (100 - pUnit:GetDamage()) or 100,
                max_hp = 100,
                movement = pUnit:GetMovesRemaining(),
            })
        end
    end
    return units
end

-- Collect city data for a player
local function CollectCities(pPlayer)
    local cities = {}
    local pCities = pPlayer:GetCities()
    if pCities then
        for i, pCity in pCities:Members() do
            local cityData = {
                id = pCity:GetID(),
                name = pCity:GetName(),
                x = pCity:GetX(),
                y = pCity:GetY(),
                population = pCity:GetPopulation(),
                is_capital = pCity:IsCapital(),
            }

            -- Production info
            local pBuildQueue = pCity:GetBuildQueue()
            if pBuildQueue then
                local currentProduction = pBuildQueue:CurrentlyBuilding()
                if currentProduction then
                    cityData.producing = currentProduction
                    cityData.turns_left = pBuildQueue:GetTurnsLeft()
                end
            end

            table.insert(cities, cityData)
        end
    end
    return cities
end

-- Collect full game state
local function CollectGameState()
    local state = {
        turn = g_CurrentTurn,
        timestamp = os.time(),
        game_id = g_GameID,
        players = {},
    }

    -- Collect all human players
    for playerID = 0, 63 do
        local pPlayer = Players[playerID]
        if pPlayer and pPlayer:IsAlive() then
            local pConfig = PlayerConfigurations[playerID]
            local isHuman = pConfig and pConfig:IsHuman() or false

            -- Include humans and major AI civs
            if isHuman or (pPlayer:IsMajor and pPlayer:IsMajor()) then
                local playerData = {
                    id = playerID,
                    civ = GetCivName(playerID),
                    leader = GetLeaderName(playerID),
                    is_human = isHuman,
                    cities = CollectCities(pPlayer),
                    units = CollectUnits(pPlayer),
                }

                -- Gold
                local pTreasury = pPlayer:GetTreasury()
                if pTreasury then
                    playerData.gold = pTreasury:GetGoldBalance()
                end

                -- Science/Culture progress
                local pTechs = pPlayer:GetTechs()
                if pTechs then
                    playerData.techs_researched = pTechs:GetNumTechsResearched()
                end

                local pCulture = pPlayer:GetCulture()
                if pCulture then
                    playerData.civics_researched = pCulture:GetNumCivicsUnlocked()
                end

                table.insert(state.players, playerData)
            end
        end
    end

    return state
end

-- Write game state to file
local function UpdateGameState()
    local state = CollectGameState()
    WriteGameState(state)
end

-- ============================================================================
-- CORE EVENT EMISSION
-- ============================================================================

local function EmitEvent(eventType, data)
    -- Build base event
    local event = {
        event_type = eventType,
        turn = g_CurrentTurn,
        timestamp = os.time(),
        game_id = g_GameID,
    }

    -- Merge event-specific data
    if data then
        for k, v in pairs(data) do
            event[k] = v
        end
    end

    -- Serialize and write
    local json = SerializeToJSON(event)
    local success = AppendLine(json)

    if success then
        g_EventCount = g_EventCount + 1
        if CONFIG.DEBUG then
            print("[LivingNarrator] Event #" .. g_EventCount .. ": " .. eventType)
        end
    end

    return success
end

-- ============================================================================
-- EVENT HANDLERS: TURNS
-- ============================================================================

local function OnTurnBegin(playerID)
    if not CONFIG.EVENTS.TURNS then return end

    -- Update current turn
    g_CurrentTurn = Game.GetCurrentGameTurn()

    -- Only emit for human players
    if IsHumanPlayer(playerID) then
        -- Update full game state at turn start
        UpdateGameState()

        EmitEvent("TURN_START", {
            player_id = playerID,
            player_civ = GetCivName(playerID),
            player_leader = GetLeaderName(playerID),
            is_local = (playerID == g_LocalPlayerID),
        })
    end
end

local function OnTurnEnd(playerID)
    if not CONFIG.EVENTS.TURNS then return end

    if IsHumanPlayer(playerID) then
        EmitEvent("TURN_END", {
            player_id = playerID,
            player_civ = GetCivName(playerID),
        })
    end
end

-- ============================================================================
-- EVENT HANDLERS: CITIES
-- ============================================================================

local function OnCityInitialized(playerID, cityID, x, y)
    if not CONFIG.EVENTS.CITIES then return end

    EmitEvent("CITY_BUILT", {
        city_name = GetCityName(playerID, cityID),
        city_id = cityID,
        player_id = playerID,
        player_civ = GetCivName(playerID),
        x = x,
        y = y,
        is_human = IsHumanPlayer(playerID),
    })
end

local function OnCityConquered(newOwnerID, oldOwnerID, cityID)
    if not CONFIG.EVENTS.CITIES then return end

    EmitEvent("CITY_CAPTURED", {
        city_id = cityID,
        new_owner_id = newOwnerID,
        new_owner_civ = GetCivName(newOwnerID),
        old_owner_id = oldOwnerID,
        old_owner_civ = GetCivName(oldOwnerID),
    })
end

local function OnCityRazed(playerID, cityName)
    if not CONFIG.EVENTS.CITIES then return end

    EmitEvent("CITY_RAZED", {
        city_name = cityName,
        player_id = playerID,
        player_civ = GetCivName(playerID),
    })
end

local function OnCityPopulationChanged(playerID, cityID, newPop)
    if not CONFIG.EVENTS.CITIES then return end

    -- Only emit for significant changes (growth, not decline from combat)
    EmitEvent("CITY_GREW", {
        city_name = GetCityName(playerID, cityID),
        city_id = cityID,
        player_id = playerID,
        population = newPop,
    })
end

-- ============================================================================
-- EVENT HANDLERS: WONDERS
-- ============================================================================

local function OnWonderCompleted(x, y, buildingID, playerID)
    if not CONFIG.EVENTS.WONDERS then return end

    local buildingInfo = GameInfo.Buildings[buildingID]
    local wonderName = buildingInfo and Locale.Lookup(buildingInfo.Name) or "Unknown Wonder"

    EmitEvent("WONDER_COMPLETED", {
        wonder = wonderName,
        wonder_id = buildingID,
        player_id = playerID,
        player_civ = GetCivName(playerID),
        x = x,
        y = y,
        is_human = IsHumanPlayer(playerID),
    })
end

-- ============================================================================
-- EVENT HANDLERS: DIPLOMACY
-- ============================================================================

local function OnDeclareWar(attackerID, defenderID)
    if not CONFIG.EVENTS.DIPLOMACY then return end

    EmitEvent("WAR_DECLARED", {
        attacker_id = attackerID,
        attacker_civ = GetCivName(attackerID),
        attacker_leader = GetLeaderName(attackerID),
        defender_id = defenderID,
        defender_civ = GetCivName(defenderID),
        defender_leader = GetLeaderName(defenderID),
    })
end

local function OnMakePeace(playerID1, playerID2)
    if not CONFIG.EVENTS.DIPLOMACY then return end

    EmitEvent("PEACE_MADE", {
        player1_id = playerID1,
        player1_civ = GetCivName(playerID1),
        player2_id = playerID2,
        player2_civ = GetCivName(playerID2),
    })
end

local function OnDenounce(denouncerID, denouncedID)
    if not CONFIG.EVENTS.DIPLOMACY then return end

    EmitEvent("DENOUNCEMENT", {
        denouncer_id = denouncerID,
        denouncer_civ = GetCivName(denouncerID),
        denounced_id = denouncedID,
        denounced_civ = GetCivName(denouncedID),
    })
end

local function OnAllianceFormed(playerID1, playerID2, allianceType)
    if not CONFIG.EVENTS.DIPLOMACY then return end

    EmitEvent("ALLIANCE_FORMED", {
        player1_id = playerID1,
        player1_civ = GetCivName(playerID1),
        player2_id = playerID2,
        player2_civ = GetCivName(playerID2),
        alliance_type = allianceType,
    })
end

-- ============================================================================
-- EVENT HANDLERS: COMBAT
-- ============================================================================

local function OnUnitKilled(killedPlayerID, killedUnitID, killerPlayerID, killerUnitID)
    if not CONFIG.EVENTS.COMBAT then return end

    -- Only log significant combat (involving humans)
    if IsHumanPlayer(killedPlayerID) or IsHumanPlayer(killerPlayerID) then
        EmitEvent("UNIT_KILLED", {
            killed_player_id = killedPlayerID,
            killed_player_civ = GetCivName(killedPlayerID),
            killer_player_id = killerPlayerID,
            killer_player_civ = GetCivName(killerPlayerID),
        })
    end
end

-- ============================================================================
-- EVENT HANDLERS: RESEARCH
-- ============================================================================

local function OnResearchCompleted(playerID, techID)
    if not CONFIG.EVENTS.RESEARCH then return end

    if IsHumanPlayer(playerID) then
        local techInfo = GameInfo.Technologies[techID]
        local techName = techInfo and Locale.Lookup(techInfo.Name) or "Unknown Tech"

        EmitEvent("TECH_COMPLETED", {
            tech = techName,
            tech_id = techID,
            player_id = playerID,
            player_civ = GetCivName(playerID),
        })
    end
end

local function OnCivicCompleted(playerID, civicID)
    if not CONFIG.EVENTS.RESEARCH then return end

    if IsHumanPlayer(playerID) then
        local civicInfo = GameInfo.Civics[civicID]
        local civicName = civicInfo and Locale.Lookup(civicInfo.Name) or "Unknown Civic"

        EmitEvent("CIVIC_COMPLETED", {
            civic = civicName,
            civic_id = civicID,
            player_id = playerID,
            player_civ = GetCivName(playerID),
        })
    end
end

-- ============================================================================
-- EVENT HANDLERS: GREAT PEOPLE
-- ============================================================================

local function OnGreatPersonActivated(playerID, unitID, greatPersonClassID, greatPersonIndividualID)
    if not CONFIG.EVENTS.GREAT_PEOPLE then return end

    local gpInfo = GameInfo.GreatPersonIndividuals[greatPersonIndividualID]
    local gpName = gpInfo and Locale.Lookup(gpInfo.Name) or "Unknown Great Person"
    local gpClass = GameInfo.GreatPersonClasses[greatPersonClassID]
    local gpType = gpClass and Locale.Lookup(gpClass.Name) or "Unknown Type"

    EmitEvent("GREAT_PERSON_EARNED", {
        person_name = gpName,
        person_type = gpType,
        player_id = playerID,
        player_civ = GetCivName(playerID),
        is_human = IsHumanPlayer(playerID),
    })
end

-- ============================================================================
-- EVENT HANDLERS: RELIGION
-- ============================================================================

local function OnReligionFounded(playerID, religionID)
    if not CONFIG.EVENTS.RELIGION then return end

    local religionInfo = GameInfo.Religions[religionID]
    local religionName = religionInfo and Locale.Lookup(religionInfo.Name) or "Unknown Religion"

    EmitEvent("RELIGION_FOUNDED", {
        religion = religionName,
        religion_id = religionID,
        player_id = playerID,
        player_civ = GetCivName(playerID),
        is_human = IsHumanPlayer(playerID),
    })
end

-- ============================================================================
-- REGISTRATION
-- ============================================================================

local function RegisterEventHandlers()
    print("[LivingNarrator] Registering event handlers...")

    -- Turn events
    Events.TurnBegin.Add(OnTurnBegin)
    Events.TurnEnd.Add(OnTurnEnd)

    -- City events
    Events.CityInitialized.Add(OnCityInitialized)
    Events.CityConquered.Add(OnCityConquered)
    -- Events.CityRazed not always available, may need alternative

    -- Wonder events
    Events.WonderCompleted.Add(OnWonderCompleted)

    -- Diplomacy events
    Events.DiplomacyDeclareWar.Add(OnDeclareWar)
    Events.DiplomacyMakePeace.Add(OnMakePeace)
    -- Events.DiplomacyDenounce may vary by game version

    -- Combat events
    Events.UnitKilledInCombat.Add(OnUnitKilled)

    -- Research events
    Events.ResearchCompleted.Add(OnResearchCompleted)
    Events.CivicCompleted.Add(OnCivicCompleted)

    -- Great People
    Events.UnitGreatPersonActivated.Add(OnGreatPersonActivated)

    -- Religion
    if Events.ReligionFounded then
        Events.ReligionFounded.Add(OnReligionFounded)
    end

    print("[LivingNarrator] Event handlers registered")
end

-- ============================================================================
-- INITIALIZATION
-- ============================================================================

local function Initialize()
    print("========================================")
    print("[LivingNarrator] Initializing v" .. CONFIG.VERSION)
    print("========================================")

    -- Generate game session ID
    g_GameID = GenerateGameID()
    g_LocalPlayerID = Game.GetLocalPlayer()
    g_CurrentTurn = Game.GetCurrentGameTurn()

    print("[LivingNarrator] Game ID: " .. g_GameID)
    print("[LivingNarrator] Local Player: " .. tostring(g_LocalPlayerID))

    -- Initialize file writer
    if InitializeEventFile() then
        -- Emit game start event
        EmitEvent("GAME_START", {
            local_player_id = g_LocalPlayerID,
            local_player_civ = GetCivName(g_LocalPlayerID),
            local_player_leader = GetLeaderName(g_LocalPlayerID),
            starting_turn = g_CurrentTurn,
            version = CONFIG.VERSION,
        })

        -- Register all event handlers
        RegisterEventHandlers()

        print("[LivingNarrator] Ready!")
    else
        print("[LivingNarrator] ERROR: Failed to initialize. Events will not be recorded.")
    end
end

-- ============================================================================
-- CONSOLE COMMANDS (for debugging)
-- ============================================================================

function LN_Status()
    local stats = GetFileStats()
    print("========================================")
    print("[LivingNarrator] Status")
    print("  Version: " .. CONFIG.VERSION)
    print("  Game ID: " .. tostring(g_GameID))
    print("  Turn: " .. tostring(g_CurrentTurn))
    print("  Events: " .. tostring(g_EventCount))
    print("  File: " .. tostring(stats.path))
    print("  Writes: " .. tostring(stats.writes))
    print("  Errors: " .. tostring(stats.errors))
    print("========================================")
end

function LN_TestEvent()
    EmitEvent("TEST_EVENT", {
        message = "Manual test event",
        triggered_by = "console",
    })
    print("[LivingNarrator] Test event emitted")
end

function LN_DumpState()
    UpdateGameState()
    print("[LivingNarrator] Game state written to file")
end

-- ============================================================================
-- START
-- ============================================================================

Initialize()
