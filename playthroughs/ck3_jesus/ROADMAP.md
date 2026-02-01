# Playthrough Jesus — Technical Roadmap

## Final Goal

A system where:
1. God (Claude Code) sees EVERYTHING happening in the game
2. Jesus (Nicolas) can pray and receive responses
3. God sends **signs** (OBS overlay) and **narration** (TTS)
4. The daemon runs in background for the entire session

---

## Target Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CK3 (Ironman)                               │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐            │
│  │ Decision:    │   │ on_actions:  │   │ Screenshots  │            │
│  │ "Pray to God"│   │ Auto events  │   │ (visual)     │            │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘            │
│         │                  │                  │                     │
│         ▼                  ▼                  │                     │
│  ┌──────────────────────────────┐             │                     │
│  │      debug.log               │             │                     │
│  │  [LN_PRAY] {...json...}      │             │                     │
│  │  [LN_EVENT] {...json...}     │             │                     │
│  └──────────────┬───────────────┘             │                     │
└─────────────────┼─────────────────────────────┼─────────────────────┘
                  │                             │
                  ▼                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         DuoAI Daemon                                │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐            │
│  │ Log Parser   │   │ Screenshot   │   │ Audio        │            │
│  │ (debug.log)  │   │ Capture      │   │ Capture      │            │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘            │
│         │                  │                  │                     │
│         └──────────────────┼──────────────────┘                     │
│                            ▼                                        │
│                  ┌──────────────┐                                   │
│                  │ Claude Code  │                                   │
│                  │ (God)        │                                   │
│                  └──────┬───────┘                                   │
│                         │                                           │
│           ┌─────────────┴─────────────┐                             │
│           │                           │                             │
│           ▼                           ▼                             │
│  ┌─────────────────┐        ┌─────────────────┐                    │
│  │ Divine Signs    │        │ TTS Output      │                    │
│  │ (OBS Overlay)   │        │ (English)       │                    │
│  └─────────────────┘        └─────────────────┘                    │
│         │                           │                               │
│         ▼                           ▼                               │
│  divine_sign.txt            last_narration.txt                     │
│  (brief signs)              (spoken responses)                     │
└─────────────────────────────────────────────────────────────────────┘
```

## God's Two Output Channels

| Channel | File | Delivery | Use For |
|---------|------|----------|---------|
| **Divine Signs** | `state/divine_sign.txt` | OBS overlay toast | Brief cues, feelings, Latin phrases |
| **Narration** | `state/last_narration.txt` | TTS spoken audio | Longer responses, interpretation |

---

## Steps

### Phase 1: Research & Validation (1-2h)

| # | Step | Description | Effort |
|---|------|-------------|--------|
| 1.1 | **Test debug_log in Ironman** | Test if `debug_log` writes without `-debug_mode` | 🔍 30min |
| 1.2 | **Locate debug.log** | Confirm Windows path | 🔍 5min |
| 1.3 | **Test basic on_actions** | Create a mini mod that logs an event | 🛠️ 1h |

**Expected debug.log path:**
```
C:\Users\{user}\Documents\Paradox Interactive\Crusader Kings III\logs\debug.log
```

**Mini test mod created:** `ck3_mod/ln_test_log/`

---

### Phase 2: CK3 Mod — Event Logger (2-4h)

| # | Step | Description | Effort |
|---|------|-------------|--------|
| 2.1 | **Mod structure** | Create descriptor.mod and folders | 🛠️ 15min |
| 2.2 | **Main on_actions** | Capture key game events | 🛠️ 2h |
| 2.3 | **"Pray to God" decision** | Custom decision with cooldown and piety | 🛠️ 1h |
| 2.4 | **English localization** | Texts for the decision | 🛠️ 30min |

**Events to capture (on_actions):**

| Event | CK3 on_action | Priority |
|-------|---------------|----------|
| Game start | `on_game_start` | ⭐⭐⭐ |
| Character death | `on_death` | ⭐⭐⭐ |
| Birth | `on_birth_child` | ⭐⭐ |
| Marriage | `on_marriage` | ⭐⭐ |
| War declared | `on_war_started` | ⭐⭐⭐ |
| Siege completed | `on_siege_completion` | ⭐⭐ |
| Title gained | `on_title_gain` | ⭐⭐ |
| Title lost | `on_title_lost` | ⭐⭐ |
| Trait gained | `on_trait_gained` | ⭐⭐ |
| Stress changed | `on_stress_level_changed` | ⭐ |
| Scheme discovered | `on_scheme_discovered` | ⭐⭐ |
| Faction joined | `on_join_faction` | ⭐⭐ |
| **PRAYER** | custom decision | ⭐⭐⭐ |

---

### Phase 3: Log Parser (1-2h)

| # | Step | Description | Effort |
|---|------|-------------|--------|
| 3.1 | **Adapt daemon.py** | Add debug.log parsing | 🛠️ 1h |
| 3.2 | **[LN_EVENT] format** | Same format as Civ6 for code reuse | 🛠️ 30min |
| 3.3 | **Update ck3.yaml** | Enable log parsing | 🛠️ 15min |

**Event format:**
```json
[LN_EVENT]{"type":"WAR_STARTED","attacker":"Jesus Botaniate","defender":"Byzantine Empire","ts":"..."}
[LN_PRAY]{"type":"PRAYER","character":"Jesus Botaniate","piety_gained":10,"ts":"..."}
```

---

### Phase 4: Audio Capture for Prayers (2-3h)

| # | Step | Description | Effort |
|---|------|-------------|--------|
| 4.1 | **Script pray_capture.py** | Capture audio when PRAYER detected | 🛠️ 1.5h |
| 4.2 | **Whisper transcription** | Integrate faster-whisper or API | 🛠️ 1h |
| 4.3 | **Audio signal** | Start/end sound for prayer | 🛠️ 30min |

**Flow:**
```
1. [LN_PRAY]{"type":"PRAYER"} detected in debug.log
2. Daemon plays sound (bell)
3. Daemon records audio (30s max or silence)
4. Daemon transcribes with Whisper
5. Daemon writes to state/prayers.jsonl
6. Daemon triggers response (God responds via TTS and/or Divine Sign)
```

---

### Phase 5: Divine Signs System (DONE ✅)

| # | Step | Description | Status |
|---|------|-------------|--------|
| 5.1 | **divine_signs.py** | Sign manager with types and templates | ✅ Done |
| 5.2 | **OBS_SETUP.md** | Setup instructions for overlay | ✅ Done |
| 5.3 | **CLAUDE.md update** | Document two output channels | ✅ Done |

**Files created:**
- `scripts/divine_signs.py` — Sign manager
- `playthroughs/ck3_jesus/OBS_SETUP.md` — OBS configuration

---

### Phase 6: Integration & Polish (1-2h)

| # | Step | Description | Effort |
|---|------|-------------|--------|
| 6.1 | **Full flow test** | Start game, pray, verify response | 🧪 1h |
| 6.2 | **Auto-launch (optional)** | Detect when CK3 starts | 🛠️ 30min |
| 6.3 | **Documentation** | Update README | 📝 30min |

---

## Risks & Fallbacks

| Risk | Impact | Fallback |
|------|--------|----------|
| `debug_log` doesn't work in Ironman | ❌ Blocking | External hotkey for prayer |
| Mods disable achievements | ⚠️ Medium | Cosmetic-only mod (just logging) |
| Whisper too slow | ⚠️ Low | Cloud API or async transcription |

---

## Next Action

**Step 1.1: Test debug_log in Ironman**

Install `ln_test_log` mod and verify if logs appear without `-debug_mode`.

If it works → continue with full mod
If it fails → fallback to external hotkey

---

## Alternative: External Hotkey (Fallback)

If the mod can't log in Ironman:

```python
# scripts/hotkey_watcher.py
import keyboard

def on_pray_hotkey():
    # 1. Play start sound
    # 2. Capture audio
    # 3. Transcribe
    # 4. Write to prayers.jsonl
    # 5. Trigger response

keyboard.add_hotkey('f9', on_pray_hotkey)
```

**Pros:**
- Works with any game
- No mod required
- Simple to implement

**Cons:**
- No in-game piety gain
- Less immersive
- Need to remember hotkey
