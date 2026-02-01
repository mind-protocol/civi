# OCR — Patterns: Region-Based Continuous OCR

## CHAIN

```
OBJECTIFS → PATTERNS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC
```

---

## THE PROBLEM

Games like CK3 and Civ6 display rich text information:
- Event popups with narrative choices
- Character traits and descriptions
- Notifications (deaths, wars, births)
- Resource counters and stats

But:
1. Sending full screenshots to Claude is expensive
2. Screenshots miss transient elements (popups dismissed quickly)
3. Claude has to re-learn the UI layout every time
4. No structured access to specific UI elements

---

## THE PATTERN

**Region-Based Continuous OCR with Change Detection**

```
┌─────────────────────────────────────────────────────────┐
│                    Screenshot                            │
│  ┌──────────────────────────────────────────────────┐   │
│  │ top_bar (priority=3)                              │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌─────────────────┐  ┌────────────────────────────┐    │
│  │                 │  │ notifications (priority=7) │    │
│  │                 │  └────────────────────────────┘    │
│  │  event_popup    │  ┌────────────────────────────┐    │
│  │  (priority=10)  │  │ character_panel            │    │
│  │                 │  │ (priority=5)               │    │
│  │                 │  │                            │    │
│  └─────────────────┘  └────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────┐   │
│  │ player_info (priority=4)    game_info (priority=2)│   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Key insights:**
1. **Regions are game-specific.** CK3 and Civ6 have different UI layouts.
2. **Priority determines importance.** Event popups (10) > notifications (7) > stats (3).
3. **Change detection via hashing.** Only report when text actually changes.
4. **Continuous polling catches transient UI.** 5s intervals vs 60s for screenshots.

---

## BEHAVIORS SUPPORTED

| Behavior | How pattern enables it |
|----------|------------------------|
| Narrator comments on events | Event popup text extracted and sent |
| Narrator notices trait changes | Character panel monitored |
| Narrator alerts on notifications | Notifications region has high priority |
| Cost efficiency | Only text diffs sent, not full images |
| Reactivity | 5s polling catches fast changes |

---

## BEHAVIORS PREVENTED

| Anti-behavior | How pattern prevents it |
|---------------|------------------------|
| Missing popups | Continuous polling at 5s |
| Expensive Claude calls | Text diffs cheaper than images |
| Noise from static UI | Change detection filters unchanged regions |
| Context-less narration | Labeled regions provide structure |

---

## PRINCIPLES

### P1: Game-Specific Region Definitions

Each game has its own `ScreenRegion` definitions. Regions are defined as percentages (0-1) for resolution independence.

```python
CK3_REGIONS = [
    ScreenRegion("event_popup", 0.25, 0.15, 0.50, 0.60, priority=10),
    ScreenRegion("notifications", 0.75, 0.05, 0.25, 0.30, priority=7),
    ...
]
```

### P2: Priority-Based Filtering

Not all changes matter equally. High-priority regions (events, notifications) trigger narration. Low-priority regions (resource counters) provide context but don't trigger.

### P3: Hash-Based Change Detection

Each region's text is hashed. If hash changes between cycles, a diff is recorded. This avoids reporting identical text repeatedly.

### P4: Graceful Degradation

OCR errors are logged but don't crash the watcher. Empty regions are skipped. Corrupted images are ignored.

---

## DATA

### Input
- Screenshots from `SCREENSHOT_DIR` (captured by PowerShell script)

### Output
- `narrator/state/ocr_diffs.jsonl` — Stream of text changes
- `narrator/state/ocr_state.json` — Last known state per region

### Diff Format
```json
{
  "timestamp": "2024-12-30T15:30:00",
  "region": "event_popup",
  "change_type": "new",
  "old_text": "",
  "new_text": "Your spymaster has uncovered a plot...",
  "summary": "[event_popup] New: Your spymaster has uncovered...",
  "priority": 10
}
```

---

## DEPENDENCIES

| Dependency | Purpose |
|------------|---------|
| Tesseract OCR | Text extraction from images |
| Pillow (PIL) | Image cropping and preprocessing |
| Screenshot capture | PowerShell script provides images |

---

## SCOPE

### In Scope
- CK3 region definitions
- Civ6 region definitions
- Text extraction from screenshots
- Change detection between frames
- Diff output for daemon consumption

### Out of Scope
- UI element detection (we use fixed regions)
- Multi-language OCR (English/French only)
- OCR model training
- Real-time (<1s) processing
