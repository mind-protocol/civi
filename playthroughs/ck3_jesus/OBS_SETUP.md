# OBS Divine Signs Overlay Setup

## Overview

God communicates through **signs** — environmental cues, feelings, Latin phrases that appear as subtle toasts in the game UI via OBS overlay.

```
┌─────────────────────────────────────────────┐
│                                    CK3 Game │
│                                             │
│                                             │
│   ┌───────────────────────────────┐         │
│   │ 🍃 The wind shifts...         │         │
│   │    carrying warmth.           │         │
│   └───────────────────────────────┘         │
│         ↑ OBS Text Overlay                  │
│                                             │
└─────────────────────────────────────────────┘
```

## Setup Instructions

### 1. Create Text Source in OBS

1. In OBS, add a new **Text (GDI+)** source
2. Name it: `Divine Sign`
3. Configure:
   - **Read from file**: ✅ Checked
   - **Text file**: `[path to duoai]/state/divine_sign.txt`
   - **Font**: Georgia or similar serif, 24-28pt
   - **Color**: Soft white (#F5F5DC) or parchment (#FFF8DC)

### 2. Style Settings

```
Font: Georgia (or Palatino, Times New Roman)
Size: 26px
Color: #FFF8DC (Cornsilk) or #F5DEB3 (Wheat)
Outline: 2px black (for readability)
Alignment: Center
```

### 3. Position

- **Bottom-center** or **top-right** of game window
- Avoid covering important UI elements
- Should feel like a subtle notification, not intrusive

### 4. Optional: Fade Effect

For smoother appearance, add a **Color Correction** filter:
- Add filter → Color Correction
- Animate opacity when text changes (requires Advanced Scene Switcher or scripting)

Or use **Move Transition** plugin for fade in/out effects.

### 5. Test

```bash
cd duoai
python scripts/divine_signs.py template manemus
# Should display: 📜 *Manemus.*

python scripts/divine_signs.py send nature "The leaves rustle with unusual warmth..."
# Should display: 🍃 The leaves rustle with unusual warmth...

python scripts/divine_signs.py clear
# Display clears
```

## Sign Types

| Type | Prefix | Example |
|------|--------|---------|
| nature | 🍃 | The wind shifts... carrying warmth. |
| feeling | ✨ | A warmth spreads through your chest. |
| latin | 📜 | *Manemus.* |
| presence | 👁 | You are being watched. Not judged. Watched. |
| silence | (empty) | (nothing displays) |

## File Locations

| File | Purpose |
|------|---------|
| `state/divine_sign.txt` | Current sign text (OBS reads this) |
| `state/divine_sign_meta.json` | Metadata (timing, auto-clear) |
| `state/divine_signs.jsonl` | History of all signs sent |

## Integration with Daemon

The daemon automatically:
1. Checks for expired signs and clears them
2. Writes new signs when God responds to prayers or events
3. Manages the timing/duration of each sign

## Recommended OBS Scene Setup

```
Scene: CK3 Jesus Playthrough
├── Game Capture (CK3)
├── Divine Sign (Text GDI+)      ← reads divine_sign.txt
├── Webcam (optional)
└── Audio sources
```

## Troubleshooting

**Sign not appearing:**
- Check file path is correct (use absolute path)
- Verify `divine_sign.txt` exists and has content
- Check "Read from file" is enabled

**Sign not updating:**
- OBS reads file periodically, should update within 1s
- Try toggling source visibility

**Encoding issues:**
- Ensure file is UTF-8
- Special characters (emojis) require UTF-8 support
