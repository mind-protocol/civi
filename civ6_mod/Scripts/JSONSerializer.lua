-- JSONSerializer.lua - JSON serialization for Civ 6
print("[LN] JSONSerializer loading...")

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
    for k in pairs(t) do
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
        if value ~= value or value == math.huge or value == -math.huge then
            return "null"
        elseif math.floor(value) == value then
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
                if type(k) == "string" then table.insert(keys, k) end
            end
            table.sort(keys)
            for _, k in ipairs(keys) do
                table.insert(parts, '"' .. EscapeString(k) .. '":' .. SerializeValue(value[k]))
            end
            return "{" .. table.concat(parts, ",") .. "}"
        end
    end
    return "null"
end

function SerializeToJSON(obj)
    local ok, result = pcall(SerializeValue, obj)
    return ok and result or '{"error":"serialize_failed"}'
end

-- Expose via ExposedMembers for cross-context access
ExposedMembers = ExposedMembers or {}
ExposedMembers.LN = ExposedMembers.LN or {}
ExposedMembers.LN.SerializeToJSON = SerializeToJSON

print("[LN] JSONSerializer ready")
