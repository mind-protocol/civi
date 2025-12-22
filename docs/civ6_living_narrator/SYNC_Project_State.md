# Civ6 Living Narrator — Sync: Project State

## Navigation
- Protocol: `.ngram/PROTOCOL.md`
- View: `.ngram/views/VIEW_Document_Create_Module_Documentation.md`
- View: `.ngram/views/VIEW_Onboard_Understand_Existing_Codebase.md`

## Maturity
STATUS: DESIGNING

## Module Health
- ingest: OK (docs/civ6_living_narrator/ingest/HEALTH_Ingest_Lag_And_Error_Rates.md)
- style_ngrams: OK (docs/civ6_living_narrator/style_ngrams/HEALTH_Sparsity_Quantiles_And_Drift.md)
- moment_graph: OK (docs/civ6_living_narrator/moment_graph/HEALTH_Moment_Count_Charge_Distribution.md)
- decision_engine: OK (docs/civ6_living_narrator/decision_engine/HEALTH_SpeechRate_Suppression_Reasons.md)
- dm_challenges: OK (docs/civ6_living_narrator/dm_challenges/HEALTH_Completion_Rates_And_Frustration_Signals.md)
- llm_router: OK (docs/civ6_living_narrator/llm_router/HEALTH_InvalidRate_Latency_Cost.md)
- audio_runtime_windows: OK (docs/civ6_living_narrator/audio_runtime_windows/HEALTH_QueueDepth_Stutter_Rate.md)
- win_wsl_bridge: OK (docs/civ6_living_narrator/win_wsl_bridge/HEALTH_Restart_Survivability.md)

## Recent Decisions
- Seeded doc chain files from ngram templates to standardize module stubs.
- Drafted top-level OBJECTIFS, PATTERNS, and VALIDATION for the v1.2 scaffold.
- Drafted ingest and win_wsl_bridge module docs to define boundaries and invariants.
- Drafted decision_engine and moment_graph module docs for rhythm and memory.
- Drafted style_ngrams and llm_router module docs for profiling and JSON routing.
- Drafted dm_challenges and audio_runtime_windows module docs for contracts and playback.
- Drafted persistence and telemetry module docs for storage and observability.
- Completed the project-level doc chain and added the missing pair-programming VIEW.
- Implemented baseline ingest tailing, normalization, and dedup helpers with tests.
- Added ingest schema validation and configurable coalescing rules.
- Implemented win_wsl_bridge session id and path resolution helpers with tests.
- Implemented decision_engine selection baseline with tests and config defaults.
- Implemented moment_graph lifecycle helpers with tests and config defaults.
- Implemented llm_router strict JSON validation baseline with tests.
- Implemented style_ngrams tokenization, backoff prediction, and tests with token_map config.
- Implemented dm_challenges catalog loading and validation with tests.
- Implemented persistence SQLite schema and adapters with tests.
- Implemented telemetry health snapshot, overlay payload, and structured logging helpers with tests.
- Implemented dm_challenges offer selection and state tracking with tests.
- Implemented audio_runtime_windows queue stub with tests.
- Added persistence session pruning helper with tests.
- Implemented V1 orchestrator (`src/main.py`) with mock LLM client (`src/llm_router/simple_llm_client.py`) and demo event loop.
- Added persistent tail state (`.tail_state.json`) and CLI `--once` flag to support single-step execution.
- Created `step.sh` for easy one-shot execution of the pipeline.
- Integrated Claude CLI as the LLM agent using `cd agents/name/ && claude` command pattern.
- Integrated ElevenLabs TTS for high-quality audio generation using `.env` API key.
- Established `audio_output/` as the local bridge for generated narration files.
- Created `CLAUDE.md` to define project commands and coding style.
- Defined `speak` tool schema and persona in `agents/narrator/CLAUDE.md` (moved from `identity.md`).
- Implemented and verified `ClaudeCLIClient` and `ElevenLabsTTS` with unit tests.
- Implemented system audio playback using `ffplay`/`mpg123` in `AudioQueue`.
- Configured comprehensive logging to `.ngram/error.log`.

## TODO (max 10)
- Fill module docs with initial decisions and boundaries.
- Populate validation invariants and health checks.
- Add first-pass implementation notes for each module.
- Docs updated, implementation needs: confirm module APIs, budget gates, and runtime bridge wiring.

## Handoff
- Next VIEW: `.ngram/views/VIEW_Document_Create_Module_Documentation.md`
- Focus: Define module boundaries and initial invariants.
