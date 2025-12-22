-- DOCS: docs/civ6_living_narrator/lua_mod/ALGORITHM_Hook_Serialize_Append.md
-- JSONSerializer.lua - Minimal JSON serialization for Civ 6 Lua
--
-- Civ 6 uses Lua 5.1 without native JSON support.
-- This module provides basic serialization for event export.

-- Escape special characters in strings for JSON
local function EscapeString(s)
    if s == nil then return "" end
    s = tostring(s)
    s = s:gsub('\\', '\\\\')
    s = s:gsub('"', '\\"')
    s = s:gsub('\n', '\\n')
    s = s:gsub('\r', '\\r')
    s = s:gsub('\t', '\\t')
    -- Handle control characters
    s = s:gsub('[\x00-\x1f]', function(c)
        return string.format('\\u%04x', string.byte(c))
    end)
    return s
end

-- Check if table is an array (sequential integer keys starting at 1)
local function IsArray(t)
    if type(t) ~= "table" then return false end
    local count = 0
    for k, v in pairs(t) do
        if type(k) ~= "number" or k <= 0 or math.floor(k) ~= k then
            return false
        end
        count = count + 1
    end
    -- Check for gaps
    for i = 1, count do
        if t[i] == nil then return false end
    end
    return true
end

-- Forward declaration for recursion
local SerializeValue

-- Serialize array to JSON
local function SerializeArray(arr)
    local parts = {}
    for i, v in ipairs(arr) do
        parts[i] = SerializeValue(v)
    end
    return "[" .. table.concat(parts, ",") .. "]"
end

-- Serialize object to JSON
local function SerializeObject(obj)
    local parts = {}
    -- Sort keys for deterministic output
    local keys = {}
    for k in pairs(obj) do
        if type(k) == "string" then
            table.insert(keys, k)
        end
    end
    table.sort(keys)

    for _, k in ipairs(keys) do
        local v = obj[k]
        local key_json = '"' .. EscapeString(k) .. '"'
        local val_json = SerializeValue(v)
        table.insert(parts, key_json .. ":" .. val_json)
    end
    return "{" .. table.concat(parts, ",") .. "}"
end

-- Main serialization function
SerializeValue = function(value)
    local t = type(value)

    if t == "nil" then
        return "null"
    elseif t == "boolean" then
        return value and "true" or "false"
    elseif t == "number" then
        -- Handle special float values
        if value ~= value then -- NaN
            return "null"
        elseif value == math.huge then
            return "null"
        elseif value == -math.huge then
            return "null"
        elseif math.floor(value) == value then
            return string.format("%d", value)
        else
            return string.format("%.6g", value)
        end
    elseif t == "string" then
        return '"' .. EscapeString(value) .. '"'
    elseif t == "table" then
        if IsArray(value) then
            return SerializeArray(value)
        else
            return SerializeObject(value)
        end
    else
        -- Functions, userdata, threads -> null
        return "null"
    end
end

-- Public API
function SerializeToJSON(obj)
    local success, result = pcall(function()
        return SerializeValue(obj)
    end)

    if success then
        return result
    else
        print("[LivingNarrator] JSON serialization error: " .. tostring(result))
        return '{"error":"serialization_failed"}'
    end
end

-- Test helper (can be called from console)
function TestJSONSerializer()
    local tests = {
        {input = nil, expected = "null"},
        {input = true, expected = "true"},
        {input = false, expected = "false"},
        {input = 42, expected = "42"},
        {input = 3.14, expected = "3.14"},
        {input = "hello", expected = '"hello"'},
        {input = 'with "quotes"', expected = '"with \\"quotes\\""'},
        {input = {a = 1, b = 2}, expected = '{"a":1,"b":2}'},
        {input = {1, 2, 3}, expected = "[1,2,3]"},
    }

    print("[LivingNarrator] Running JSON serializer tests...")
    local passed = 0
    for i, test in ipairs(tests) do
        local result = SerializeToJSON(test.input)
        if result == test.expected then
            passed = passed + 1
        else
            print("  FAIL test " .. i .. ": got " .. result .. ", expected " .. test.expected)
        end
    end
    print("[LivingNarrator] Tests: " .. passed .. "/" .. #tests .. " passed")
end
