# LN Test Log — Ironman Validation

## Purpose

Tests whether `debug_log` effect works in Ironman mode (without `-debug_mode` launch flag).

**This is Step 1.1 of the Prayer System Roadmap.**

## Installation

1. Copy `ln_test_log/` folder to:
   - **Windows:** `Documents\Paradox Interactive\Crusader Kings III\mod\`
   - **Linux:** `~/.local/share/Paradox Interactive/Crusader Kings III/mod/`

2. Create `ln_test_log.mod` file in the `mod/` folder (sibling to the folder):
```
version="1.0.0"
tags={
	"Utilities"
}
name="LN Test Log"
supported_version="1.14.*"
path="mod/ln_test_log"
```

3. Enable the mod in CK3 launcher

## Test Procedure

1. Start CK3 **normally** (no `-debug_mode`)
2. Enable the mod
3. Start a **new Ironman game** (any character)
4. Wait for game to load
5. Check debug.log:
   - **Windows:** `Documents\Paradox Interactive\Crusader Kings III\logs\debug.log`
   - **Linux:** `~/.local/share/Paradox Interactive/Crusader Kings III/logs/debug.log`

## Expected Results

### SUCCESS (debug_log works in Ironman)
```
[LN_TEST]{"type":"GAME_START","date":"..."}
LN_TEST: Game started - If you see this in Ironman, debug_log works!
```

### FAILURE (debug_log doesn't work)
No `[LN_TEST]` lines in debug.log

## If It Works

✅ Proceed with full mod development (prayer decision, event logging)

## If It Fails

❌ Fallback to external hotkey system:
- F9 = Pray (triggers audio capture)
- No in-game integration
- Still functional, just less elegant

## What This Tests

| Feature | Tested By |
|---------|-----------|
| debug_log in Ironman | on_game_start trigger |
| JSON format in log | Structured output |
| Character data access | on_death with [ROOT.GetName] |
| Date string access | [GetDateString] |
