# Living Narrator — Sync: Project State

```
LAST_UPDATED: 2026-02-01
UPDATED_BY: Claude (agent)
```

---

## CURRENT STATE

**Living Narrator** — Un troisième joueur qui ne joue pas. Il regarde, se souvient, commente, taquine, conseille.

An AI companion for strategy games that provides real-time French-language narrative commentary. Watches your game, remembers pivotal moments, and speaks with personality.

**Supported Games:**

| Game | Input Mode | Persona |
|------|------------|---------|
| Civilization VI | Lua mod events + OCR | Pote de table coop |
| Crusader Kings III | Pure visual (OCR) | Chroniqueur de cour |

**Maturity:** CANONICAL (v1 functional, in active use)

---

## MODULE HEALTH

| Module | Status | Doc Chain | Code |
|--------|--------|-----------|------|
| ingest | OK | `docs/civ6_living_narrator/ingest/` | `src/ingest/` |
| ocr | OK | `docs/civ6_living_narrator/ocr/` | `scripts/ocr_watcher.py` |
| style_ngrams | OK | `docs/civ6_living_narrator/style_ngrams/` | `src/style_ngrams/` |
| moment_graph | OK | `docs/civ6_living_narrator/moment_graph/` | `src/moment_graph/` |
| decision_engine | OK | `docs/civ6_living_narrator/decision_engine/` | `src/decision_engine/` |
| dm_challenges | OK | `docs/civ6_living_narrator/dm_challenges/` | `src/dm_challenges/` |
| llm_router | OK | `docs/civ6_living_narrator/llm_router/` | `src/llm_router/` |
| audio_runtime_windows | OK | `docs/civ6_living_narrator/audio_runtime_windows/` | `src/audio_runtime_windows/` |
| win_wsl_bridge | OK | `docs/civ6_living_narrator/win_wsl_bridge/` | `src/win_wsl_bridge/` |
| lua_mod | OK | `docs/civ6_living_narrator/lua_mod/` | `civ6_mod/` |
| persistence | OK | `docs/civ6_living_narrator/persistence/` | `src/persistence/` |
| telemetry | OK | `docs/civ6_living_narrator/telemetry/` | `src/telemetry/` |

All 12 modules have complete doc chains and implementations.

---

## ARCHITECTURE

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Game Input    │────▶│   Claude LLM    │────▶│  Windows Audio  │
│ (events + OCR)  │     │  (narrator AI)  │     │   (TTS out)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

**Pipeline:**
1. **Ingest** — Lua mod writes events to `events.jsonl` (Civ6) or OCR extracts screen text (both)
2. **Moment Graph** — Events become moments with charge, decay, callbacks
3. **Decision Engine** — Scores candidates, enforces rhythm/budget/diversity
4. **LLM Router** — Packs context, calls Claude, validates JSON output
5. **Audio Runtime** — TTS via ElevenLabs, plays on Windows speakers

**Key Files:**
- `daemon.py` — Main orchestrator
- `run.sh` — Launcher (starts OCR by default)
- `config/games/{game}.yaml` — Game profiles
- `narrator/CLAUDE.md` — Civ6 persona
- `narrator/CLAUDE_CK3.md` — CK3 persona

---

## ACTIVE WORK

None currently. System is stable and functional.

---

## RECENT CHANGES

### 2026-02-01: Mind Protocol Init

- **What:** Initialized Mind Protocol framework
- **Why:** Structured documentation and agent coordination
- **Impact:** `.mind/` directory with agents, skills, procedures

### 2024-12-30: Multi-Game Support + OCR

- **What:** Added CK3 support, implemented OCR watcher
- **Why:** CK3 has no modding API, visual analysis required
- **Impact:** New game profile system, OCR reduces token cost 10x

---

## KNOWN ISSUES

| Issue | Severity | Notes |
|-------|----------|-------|
| OCR regions tuned for 1920x1080 | Low | May need adjustment for other resolutions |
| Stylized game fonts reduce OCR accuracy | Low | ~80% accuracy acceptable |

---

## HANDOFF: FOR AGENTS

**Likely agent:** groundwork (implementation), witness (investigation)

**Key context:**
- French-language project (README, comments, narration all in French)
- Windows/WSL hybrid: game runs on Windows, daemon runs in WSL
- OCR runs as separate process, daemon consumes diffs via cursor
- Game profile loaded from `narrator/state/config.json`

**Doc chain entry point:** `docs/civ6_living_narrator/SYNC_Project_State.md`

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Living Narrator is functional. Supports Civ6 (events + visual) and CK3 (pure visual). OCR-based text extraction reduces costs and increases reactivity.

**To run:**
```bash
# Configure session
echo '{"game": "civ6", "visual_mode": true}' > narrator/state/config.json

# Launch
./run.sh
```

---

## Init: 2026-02-01 15:32

| Setting | Value |
|---------|-------|
| Version | v0.0.0 |
| Database | falkordb |
| Graph | duoai |

**Steps completed:** ecosystem, capabilities, runtime, ai_configs, skills, database_config, database_setup, file_ingest, capabilities_graph, agents, env_example, mcp_config, gitignore, overview, embeddings, health_checks

---
