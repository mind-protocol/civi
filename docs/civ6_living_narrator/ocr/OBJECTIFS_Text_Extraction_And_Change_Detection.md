# OBJECTIFS — OCR: Text Extraction and Change Detection

## CHAIN

```
OBJECTIFS → PATTERNS → ALGORITHM → VALIDATION → IMPLEMENTATION → HEALTH → SYNC
    ↑                                                                        ↓
    └────────────────────────────────────────────────────────────────────────┘
```

---

## PRIMARY OBJECTIVES (ranked)

### O1: Reduce LLM Token Cost

**The core problem:** Sending raw screenshots to Claude is expensive (~$0.01-0.05 per image). A 2-hour session with 60s intervals = 120 images = $1.20-6.00 just for images.

**The solution:** Extract text locally via OCR, detect changes, only invoke Claude when meaningful changes occur. Text diffs are cheaper than image tokens.

**Success metric:** 10x reduction in Claude invocations while maintaining awareness.

### O2: Increase Reactivity

**The problem:** 60s screenshot intervals mean the narrator misses fast events (popup appears → player clicks → popup gone in 10s).

**The solution:** OCR every 5s captures transient UI elements. Claude still invoked at 30-120s intervals, but with accumulated context.

**Success metric:** Event popups captured before player dismisses them.

### O3: Provide Structured Context

**The problem:** Raw screenshots require Claude to "understand" the game UI every time.

**The solution:** OCR with region awareness extracts text from known UI elements (event_popup, notifications, character_panel). Claude receives labeled text, not raw pixels.

**Success metric:** Narrator references specific UI text ("I see you got the 'Ambitious' trait").

---

## NON-OBJECTIVES

- **Perfect OCR accuracy.** 80% accuracy is fine. The narrator can work with imperfect text.
- **Real-time processing.** 5s intervals are fast enough. Sub-second is not needed.
- **Cross-platform.** WSL/Windows only for now. No macOS/Linux native.
- **UI element detection.** We use fixed regions, not computer vision to find buttons.

---

## TRADEOFFS (canonical decisions)

| Decision | Chosen | Rejected | Rationale |
|----------|--------|----------|-----------|
| OCR engine | Tesseract (local) | Cloud OCR (Google/AWS) | Free, no API keys, privacy |
| Region detection | Fixed percentages | Dynamic CV detection | Simpler, predictable, game-specific |
| Change detection | Text hash diff | Pixel diff | Text changes are what matters |
| Processing model | Continuous watcher | On-demand | Catches transient popups |

---

## SUCCESS SIGNALS (observable)

| Signal | How to verify |
|--------|---------------|
| OCR running | `ps aux | grep ocr_watcher` |
| Diffs being generated | `tail -f narrator/state/ocr_diffs.jsonl` |
| Event popups captured | Diff file contains "event_popup" entries with event text |
| Cost reduction | Compare Claude invocations with/without OCR |
| Reactivity | Narrator comments on events seen in OCR before screenshot sent |
