# Living Narrator — Sync: Project State

```
LAST_UPDATED: 2026-02-01
UPDATED_BY: Claude (agent)
```

## Navigation
- Protocol: `.ngram/PROTOCOL.md`
- Mind Framework: `.mind/FRAMEWORK.md`

## Maturity
STATUS: CANONICAL (v1)

Multi-game narrator with OCR-based text extraction. Supports Civ6 and CK3.

## Module Health

| Module | Status | Doc Chain |
|--------|--------|-----------|
| ingest | OK | `docs/civ6_living_narrator/ingest/` |
| ocr | OK | `docs/civ6_living_narrator/ocr/` |
| **prayer** | **NEW** | `docs/civ6_living_narrator/prayer/` |
| style_ngrams | OK | `docs/civ6_living_narrator/style_ngrams/` |
| moment_graph | OK | `docs/civ6_living_narrator/moment_graph/` |
| decision_engine | OK | `docs/civ6_living_narrator/decision_engine/` |
| dm_challenges | OK | `docs/civ6_living_narrator/dm_challenges/` |
| llm_router | OK | `docs/civ6_living_narrator/llm_router/` |
| audio_runtime_windows | OK | `docs/civ6_living_narrator/audio_runtime_windows/` |
| win_wsl_bridge | OK | `docs/civ6_living_narrator/win_wsl_bridge/` |
| lua_mod | OK | `docs/civ6_living_narrator/lua_mod/` |
| persistence | OK | `docs/civ6_living_narrator/persistence/` |
| telemetry | OK | `docs/civ6_living_narrator/telemetry/` |

## Recent Changes

### 2026-02-01: Prayer System (F9 Hotkey)

**What:**
- Implemented "Pray" hotkey (F9) for CK3 Ironman mode
- Created `scripts/pray_hotkey.ps1` for Windows hotkey detection
- Modified `daemon.py` to detect `prayer_request.json` signal
- Documented theological design philosophy

**Why:**
- CK3 `debug_log` doesn't work without `-debug_mode`
- `-debug_mode` disables achievements (bad for stream)
- Intentional prayer > automatic narration (theologically richer)

**Architectural Decision:**
- Dieu omniscient non-interventionniste
- OCR = conscience passive (Dieu voit tout)
- F9 = prière active (Dieu ne parle que quand invoqué)
- "La prière qui coûte quelque chose est plus vraie"

**Impact:**
- New module: `docs/civ6_living_narrator/prayer/`
- New file: `scripts/pray_hotkey.ps1`
- Modified: `daemon.py` (prayer request detection)

### 2024-12-30: Multi-Game Support + OCR

**What:**
- Added CK3 support via pure visual mode (screenshots only)
- Implemented OCR watcher with Tesseract
- Created game profiles system (`config/games/`)
- OCR is now required and runs by default

**Why:**
- User requested CK3 playthrough support
- CK3 has no modding API like Civ6, so visual analysis is required
- OCR reduces Claude token cost by 10x while increasing reactivity

**Impact:**
- New files: `scripts/ocr_watcher.py`, `src/game_profile_loader.py`
- New config: `config/games/ck3.yaml`, `config/games/civ6.yaml`
- New persona: `narrator/CLAUDE_CK3.md`
- New doc chain: `docs/civ6_living_narrator/ocr/`
- Updated: `daemon.py`, `run.sh`, `README.md`

### Key Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| OCR engine | Tesseract (local) | Free, no API keys, privacy |
| Region detection | Fixed percentages | Simpler, predictable, game-specific |
| Game selection | Config-based profiles | Clean separation, easy to add games |
| CK3 input mode | Pure visual (no events) | No modding API available |

## Active Configuration

| Setting | Value |
|---------|-------|
| Game | Configurable (civ6/ck3) |
| OCR interval | 5s |
| Screenshot interval | 30s (CK3) / 60s (Civ6) |
| Narration interval | 30-120s |

## TODO (max 10)

- [ ] Test OCR regions on different screen resolutions
- [ ] Add region visualization tool
- [ ] Tune CK3 regions for better accuracy
- [ ] Add more CK3 regions (tech tree, dynasty view)
- [ ] Test end-to-end with real CK3 gameplay
- [ ] Consider OCR caching (skip if screenshot unchanged)
- [ ] Add support for more games (EU4, Stellaris)

## Known Issues

| Issue | Severity | Notes |
|-------|----------|-------|
| OCR region coords may need tuning | Low | Based on 1920x1080 |
| Stylized game fonts reduce OCR accuracy | Low | ~80% accuracy acceptable |
| No dynamic UI detection | Low | Using fixed percentages |

## Handoff: For Agents

**Likely agent:** groundwork (implementation)

**Current focus:** CK3 playtesting and region tuning

**Key context:**
- OCR runs as separate process, started by `run.sh`
- Game profile loaded from `narrator/state/config.json` → `game` field
- CK3 uses `visual_primary=true` (no Lua events)
- Daemon consumes OCR diffs via cursor system

## Handoff: For Human

**Executive summary:**
Multi-game narrator is ready. CK3 support via screenshots + OCR. OCR now required.

**To start a CK3 session:**
```bash
# Set game to ck3
echo '{"game": "ck3", "visual_mode": true, "players": [{"name": "Nico", "dynasty": "Valois"}]}' > narrator/state/config.json

# Run
./run.sh
```

**Needs input:**
- Test on your screen resolution
- Report if OCR regions miss important text
- Feedback on CK3 narrator persona

## File Tree (key files)

```
├── daemon.py                    # Main orchestrator
├── run.sh                       # Launcher (starts OCR by default)
├── config/
│   └── games/
│       ├── civ6.yaml           # Civ6 profile
│       └── ck3.yaml            # CK3 profile
├── narrator/
│   ├── CLAUDE.md               # Civ6 persona
│   ├── CLAUDE_CK3.md           # CK3 persona
│   └── state/
│       ├── config.json         # Session config
│       ├── ocr_state.json      # Current OCR state
│       └── ocr_diffs.jsonl     # OCR change stream
├── scripts/
│   ├── capture.py              # Screenshot capture
│   ├── ocr_watcher.py          # OCR engine
│   └── speak.py                # TTS
└── src/
    └── game_profile_loader.py  # Profile loader
```
