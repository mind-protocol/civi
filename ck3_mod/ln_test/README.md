# Living Narrator Test Mod for CK3

**Purpose:** Validate that `debug_log` works in Ironman mode.

## Installation

```powershell
.\install.ps1
```

## What It Tests

1. **Game Start Log** - `[LN_TEST] Game started...` on new game
2. **Monthly Tick** - `[LN_EVENT] {"type":"MONTHLY_TICK",...}` every month
3. **Decision Click** - `[LN_EVENT] {"type":"TEST_DECISION",...}` on demand
4. **Death Events** - `[LN_EVENT] {"type":"CHARACTER_DEATH",...}`
5. **War Events** - `[LN_EVENT] {"type":"WAR_DECLARED",...}`

## How to Test

1. Install and enable the mod
2. Start an **Ironman** game (this is the critical test)
3. Open the Decisions panel (find "Test Living Narrator Log")
4. Click the decision
5. Check the log file:
   ```
   Documents\Paradox Interactive\Crusader Kings III\logs\debug.log
   ```

## Success Criteria

If you see `[LN_EVENT]` or `[LN_TEST]` lines in `debug.log`, the system works.

If the file is empty or these lines don't appear, we need an alternative approach.

## Next Steps

**If it works:**
- Build full event logging mod with all relevant game events
- Add "Pray to God" decision that triggers TTS capture

**If it doesn't work:**
- Try with `-debug_mode` launch option (won't work for Ironman achievements)
- Fallback to external hotkey (F9 = Pray) with OCR screen capture
