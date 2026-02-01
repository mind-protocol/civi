# OCR — Implementation: Watcher and Regions

## CHAIN

```
OBJECTIFS → PATTERNS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC
```

---

## FILE MAP

| File | Purpose |
|------|---------|
| `scripts/ocr_watcher.py` | Main OCR watcher script |
| `config/games/ck3.yaml` | CK3 game profile (visual_primary=true) |
| `config/games/civ6.yaml` | Civ6 game profile |
| `narrator/state/ocr_state.json` | Current OCR state per region |
| `narrator/state/ocr_diffs.jsonl` | Stream of detected changes |
| `narrator/state/ocr_cursor.json` | Daemon's read position |

---

## DATA STRUCTURES

### ScreenRegion

```python
@dataclass
class ScreenRegion:
    name: str       # e.g., "event_popup"
    x: float        # 0-1, left edge
    y: float        # 0-1, top edge
    w: float        # 0-1, width
    h: float        # 0-1, height
    priority: int   # 1-10, higher = more important
```

### OCRResult

```python
@dataclass
class OCRResult:
    region: str     # Region name
    text: str       # Extracted text
    hash: str       # MD5 hash (12 chars)
    timestamp: str  # ISO8601
```

### TextDiff

```python
@dataclass
class TextDiff:
    timestamp: str
    region: str
    change_type: str  # "new", "changed", "removed"
    old_text: str
    new_text: str
    summary: str      # Human-readable
    priority: int
```

---

## CK3 REGIONS

```python
CK3_REGIONS = [
    # Event popup - center, most narrative content
    ScreenRegion("event_popup", 0.25, 0.15, 0.50, 0.60, priority=10),

    # Top bar - gold, prestige, piety, stress
    ScreenRegion("top_bar", 0.0, 0.0, 1.0, 0.05, priority=3),

    # Character panel - right side when open
    ScreenRegion("character_panel", 0.65, 0.10, 0.35, 0.80, priority=5),

    # Notifications - deaths, wars, schemes
    ScreenRegion("notifications", 0.75, 0.05, 0.25, 0.30, priority=7),

    # Player info - bottom left
    ScreenRegion("player_info", 0.0, 0.85, 0.25, 0.15, priority=4),

    # Game info - date, speed
    ScreenRegion("game_info", 0.40, 0.92, 0.20, 0.08, priority=2),
]
```

### Visual Layout (1920x1080)

```
┌────────────────────────────────────────────────────────────────────┐
│ top_bar (0,0 → 1920x54)                                    [P=3]   │
├────────────────────────────────────────────────────────────────────┤
│                           │ notifications (1440,54 → 480x324) [P=7]│
│                           ├────────────────────────────────────────┤
│    event_popup            │                                        │
│    (480,162 → 960x648)    │    character_panel                     │
│    [P=10]                 │    (1248,108 → 672x864)                │
│                           │    [P=5]                               │
│                           │                                        │
│                           │                                        │
├───────────────────────────┼────────────────────────────────────────┤
│ player_info               │ game_info (768,994 → 384x86) [P=2]     │
│ (0,918 → 480x162) [P=4]   │                                        │
└────────────────────────────────────────────────────────────────────┘
```

---

## CIV6 REGIONS

```python
CIV6_REGIONS = [
    ScreenRegion("top_bar", 0.0, 0.0, 1.0, 0.08, priority=3),
    ScreenRegion("unit_panel", 0.0, 0.70, 0.25, 0.30, priority=4),
    ScreenRegion("city_panel", 0.0, 0.0, 0.30, 0.50, priority=5),
    ScreenRegion("notifications", 0.85, 0.10, 0.15, 0.60, priority=6),
    ScreenRegion("popup_center", 0.25, 0.20, 0.50, 0.50, priority=8),
    ScreenRegion("turn_info", 0.45, 0.0, 0.10, 0.05, priority=2),
]
```

---

## DATA FLOW

```
Screenshot (PNG)
      │
      ▼
┌─────────────────┐
│ ocr_watcher.py  │
│                 │
│ 1. Load image   │
│ 2. Crop regions │
│ 3. Preprocess   │
│ 4. Tesseract    │
│ 5. Hash & diff  │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
ocr_state   ocr_diffs.jsonl
  .json           │
                  ▼
           ┌─────────────┐
           │ daemon.py   │
           │             │
           │ Reads diffs │
           │ via cursor  │
           └─────────────┘
```

---

## CONFIG

### Tesseract

```python
TESSERACT_CONFIG = '--oem 3 --psm 6 -l eng+fra'
# OEM 3: Default engine (LSTM + legacy)
# PSM 6: Assume uniform text block
# Languages: English + French
```

### Timing

```python
OCR_INTERVAL = 5              # seconds between cycles
MIN_CHANGE_THRESHOLD = 50     # chars required to report change
SCREENSHOT_MAX_AGE = 30       # ignore screenshots older than this
```

### Preprocessing

```python
def preprocess_for_ocr(img):
    img = img.convert('L')                    # Grayscale
    img = ImageOps.autocontrast(img, cutoff=2)  # Contrast
    img = img.filter(ImageFilter.SHARPEN)     # Sharpen
    img = img.resize((w*2, h*2), LANCZOS)     # 2x scale
    return img
```

---

## NOTES

### Region Tuning

Regions are defined as percentages for resolution independence, but may need adjustment for:
- Different aspect ratios (16:9 vs 21:9)
- UI scaling settings in game
- Different game versions

### OCR Accuracy

Tesseract accuracy varies by:
- Font (game fonts are often stylized)
- Background (busy backgrounds hurt OCR)
- Size (small text is harder)

Current preprocessing (contrast, sharpen, 2x scale) improves accuracy but isn't perfect. 80% accuracy is acceptable.

### Performance

On a typical system:
- Screenshot load: ~50ms
- Crop regions: ~5ms
- Preprocess: ~20ms per region
- Tesseract: ~200-400ms per region
- Total cycle: ~500ms-1s for 6 regions

Well within the 5s interval budget.
