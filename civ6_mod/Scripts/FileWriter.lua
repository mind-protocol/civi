-- FileWriter.lua - Event output for Civ 6
print("[LN] FileWriter loading...")

local g_Initialized = false
local g_WriteCount = 0

-- Initialize (Print Mode - outputs to Lua.log)
function InitializeEventFile()
    g_Initialized = true
    print("[LN] Event logging initialized (Print Mode)")
    return true
end

-- Append event as JSON line to Lua.log
function AppendLine(json_line)
    print("[LN_EVENT]" .. json_line)
    g_WriteCount = g_WriteCount + 1
    return true
end

-- Write game state (no-op in print mode)
function WriteGameState(stateObj)
    return true
end

-- Get stats
function GetFileStats()
    return {
        initialized = g_Initialized,
        writes = g_WriteCount,
    }
end

-- Expose via ExposedMembers for cross-context access
ExposedMembers = ExposedMembers or {}
ExposedMembers.LN = ExposedMembers.LN or {}
ExposedMembers.LN.InitializeEventFile = InitializeEventFile
ExposedMembers.LN.AppendLine = AppendLine
ExposedMembers.LN.WriteGameState = WriteGameState
ExposedMembers.LN.GetFileStats = GetFileStats

print("[LN] FileWriter ready")
