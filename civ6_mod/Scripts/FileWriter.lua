-- DOCS: docs/civ6_living_narrator/lua_mod/ALGORITHM_Hook_Serialize_Append.md
-- FileWriter.lua - File I/O for event export
--
-- Handles writing events to the JSONL file.
-- Uses append mode and flushes after each write for immediate visibility.

-- Configuration
local CONFIG = {
    -- Base directory under user's Documents (matches daemon expectation)
    BASE_DIR = "Civ6Narrator",
    -- Output filename
    FILENAME = "events.jsonl",
    -- Game state filename
    STATE_FILENAME = "game_state.json",
    -- Enable debug logging
    DEBUG = false,
}

-- State
local g_FilePath = nil
local g_StatePath = nil
local g_BaseDir = nil
local g_FileHandle = nil
local g_Initialized = false
local g_WriteCount = 0
local g_ErrorCount = 0

-- Get the Documents path (Windows)
local function GetDocumentsPath()
    -- Try USERPROFILE environment variable
    local userprofile = os.getenv("USERPROFILE")
    if userprofile then
        return userprofile .. "\\Documents"
    end

    -- Fallback: try HOME (for non-Windows or WSL)
    local home = os.getenv("HOME")
    if home then
        return home .. "/Documents"
    end

    -- Last resort
    return "."
end

-- Ensure directory exists (Windows-compatible)
local function EnsureDirectory(path)
    -- Use mkdir with error suppression
    -- On Windows: mkdir "path" 2>nul
    -- On Unix: mkdir -p "path" 2>/dev/null
    local cmd
    if package.config:sub(1,1) == '\\' then
        -- Windows
        cmd = 'mkdir "' .. path .. '" 2>nul'
    else
        -- Unix
        cmd = 'mkdir -p "' .. path .. '" 2>/dev/null'
    end
    os.execute(cmd)
end

-- Initialize the event file
function InitializeEventFile()
    if g_Initialized then
        return true
    end

    local success, err = pcall(function()
        -- Build path - directly in Documents/Civ6Narrator/
        local docs = GetDocumentsPath()
        g_BaseDir = docs .. "\\" .. CONFIG.BASE_DIR
        g_FilePath = g_BaseDir .. "\\" .. CONFIG.FILENAME
        g_StatePath = g_BaseDir .. "\\" .. CONFIG.STATE_FILENAME

        -- Ensure directory exists
        EnsureDirectory(g_BaseDir)

        -- Open file in append mode
        g_FileHandle = io.open(g_FilePath, "a")

        if g_FileHandle then
            g_Initialized = true
            print("[LivingNarrator] Event file initialized: " .. g_FilePath)
            print("[LivingNarrator] Game state path: " .. g_StatePath)

            -- Write startup marker
            local startup = {
                event_type = "_NARRATOR_STARTUP",
                timestamp = os.time(),
                version = "1.0.0",
            }
            AppendLine(SerializeToJSON(startup))
        else
            print("[LivingNarrator] ERROR: Could not open event file: " .. g_FilePath)
        end
    end)

    if not success then
        print("[LivingNarrator] ERROR initializing file: " .. tostring(err))
        return false
    end

    return g_Initialized
end

-- Append a line to the event file
function AppendLine(json_line)
    if not g_Initialized then
        if not InitializeEventFile() then
            g_ErrorCount = g_ErrorCount + 1
            return false
        end
    end

    local success, err = pcall(function()
        if g_FileHandle then
            g_FileHandle:write(json_line .. "\n")
            g_FileHandle:flush()
            g_WriteCount = g_WriteCount + 1

            if CONFIG.DEBUG then
                print("[LivingNarrator] Wrote event: " .. json_line:sub(1, 80))
            end
        end
    end)

    if not success then
        print("[LivingNarrator] Write error: " .. tostring(err))
        g_ErrorCount = g_ErrorCount + 1

        -- Try to recover by reopening the file
        if g_FileHandle then
            pcall(function() g_FileHandle:close() end)
        end
        g_FileHandle = nil
        g_Initialized = false

        return false
    end

    return true
end

-- Close the file handle
function CloseEventFile()
    if g_FileHandle then
        local success, err = pcall(function()
            -- Write shutdown marker
            local shutdown = {
                event_type = "_NARRATOR_SHUTDOWN",
                timestamp = os.time(),
                writes = g_WriteCount,
                errors = g_ErrorCount,
            }
            g_FileHandle:write(SerializeToJSON(shutdown) .. "\n")
            g_FileHandle:flush()
            g_FileHandle:close()
        end)

        if not success then
            print("[LivingNarrator] Error closing file: " .. tostring(err))
        end

        g_FileHandle = nil
        g_Initialized = false
        print("[LivingNarrator] Event file closed. Writes: " .. g_WriteCount .. ", Errors: " .. g_ErrorCount)
    end
end

-- Get file statistics
function GetFileStats()
    return {
        path = g_FilePath,
        state_path = g_StatePath,
        initialized = g_Initialized,
        writes = g_WriteCount,
        errors = g_ErrorCount,
    }
end

-- Write game state to JSON file (overwrites each time)
function WriteGameState(stateObj)
    if not g_Initialized then
        if not InitializeEventFile() then
            return false
        end
    end

    local success, err = pcall(function()
        local stateFile = io.open(g_StatePath, "w")
        if stateFile then
            local json = SerializeToJSON(stateObj)
            stateFile:write(json)
            stateFile:flush()
            stateFile:close()
            if CONFIG.DEBUG then
                print("[LivingNarrator] Game state written")
            end
        else
            print("[LivingNarrator] ERROR: Could not write game state")
        end
    end)

    if not success then
        print("[LivingNarrator] State write error: " .. tostring(err))
        return false
    end

    return true
end

-- Debug: Get current config
function GetFileWriterConfig()
    return CONFIG
end
