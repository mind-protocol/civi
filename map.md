# Repository Map: duoai

*Generated: 2026-02-01 15:32*

- **Files:** 171
- **Directories:** 47
- **Total Size:** 808.9K
- **Doc Files:** 103
- **Code Files:** 48
- **Areas:** 1 (docs/ subfolders)
- **Modules:** 12 (subfolders in areas)
- **DOCS Links:** 0 (0.0 avg per code file)

- markdown: 103
- python: 47
- shell: 1

```
├── agents/ (2.9K)
│   └── narrator/ (2.9K)
│       ├── AGENTS.md (960)
│       ├── CLAUDE.md (960)
│       └── GEMINI.md (960)
├── civ6_mod/ (42.0K)
│   ├── Scripts/ (21.0K)
│   │   ├── FileWriter.lua (1.1K)
│   │   ├── JSONSerializer.lua (2.3K)
│   │   └── LivingNarrator.lua (17.6K)
│   ├── INSTALL.md (2.4K)
│   ├── LivingNarrator.modinfo (587)
│   ├── README.md (3.4K)
│   ├── TEST_GUIDE.md (4.9K)
│   ├── check_output.ps1 (3.0K)
│   ├── install.ps1 (2.6K)
│   ├── install_mod.ps1 (2.1K)
│   └── verify_mod_output.ps1 (2.1K)
├── ck3_mod/ (8.3K)
│   ├── ln_test/ (5.9K)
│   │   ├── common/ (1.6K)
│   │   │   ├── decisions/ (574)
│   │   │   │   └── ln_test_decision.txt (574)
│   │   │   └── on_action/ (1.1K)
│   │   │       └── ln_test_events.txt (1.1K)
│   │   ├── README.md (1.3K)
│   │   ├── check_output.ps1 (1.2K)
│   │   ├── install.ps1 (1.5K)
│   │   └── (..2 more files)
│   └── ln_test_log/ (2.3K)
│       ├── common/ (519)
│       │   └── on_action/ (519)
│       │       └── ln_test_events.txt (519)
│       ├── README.md (1.7K)
│       └── (..1 more files)
├── docs/ (270.0K)
│   ├── civ6_living_narrator/ (214.8K)
│   │   ├── audio_runtime_windows/ (6.7K)
│   │   │   ├── ALGORITHM_Queue_Play_Stop_Replay.md (913)
│   │   │   ├── IMPLEMENTATION_Player_Process_And_IPC.md (768)
│   │   │   ├── OBJECTIFS_LowLatency_Playback.md (587)
│   │   │   ├── SYNC_Win11_Audio_Player.md (3.1K)
│   │   │   ├── VALIDATION_NoOverlap_NoBlock.md (833)
│   │   │   └── (..1 more files)
│   │   ├── decision_engine/ (8.3K)
│   │   │   ├── ALGORITHM_Score_Candidates_And_Select.md (1.2K)
│   │   │   ├── HEALTH_SpeechRate_Suppression_Reasons.md (512)
│   │   │   ├── IMPLEMENTATION_Candidate_Pipeline_And_Explainability.md (918)
│   │   │   ├── OBJECTIFS_Rhythm_NonSpam_Diversity.md (733)
│   │   │   ├── SYNC_Rhythm_And_Selection.md (3.9K)
│   │   │   └── VALIDATION_Budget_Cooldown_Diversity.md (1.1K)
│   │   ├── dm_challenges/ (7.9K)
│   │   │   ├── ALGORITHM_Generate_Evaluate_Remind.md (1.1K)
│   │   │   ├── HEALTH_Completion_Rates_And_Frustration_Signals.md (523)
│   │   │   ├── IMPLEMENTATION_Challenge_Catalog_And_Runtime.md (807)
│   │   │   ├── OBJECTIFS_Agency_Contracts_Temptation.md (673)
│   │   │   ├── SYNC_Challenge_Contract_System.md (3.9K)
│   │   │   └── VALIDATION_OneActive_And_Clarity.md (882)
│   │   ├── ingest/ (9.9K)
│   │   │   ├── ALGORITHM_Tail_Parse_Dedup_Coalesce.md (1.4K)
│   │   │   ├── BEHAVIORS_Ingest_Event_Intake.md (1.2K)
│   │   │   ├── HEALTH_Ingest_Lag_And_Error_Rates.md (557)
│   │   │   ├── IMPLEMENTATION_File_Watcher_And_Parsers.md (918)
│   │   │   ├── SYNC_Ingest_And_Normalization.md (4.3K)
│   │   │   └── VALIDATION_Event_Schemas_And_Signatures.md (1.5K)
│   │   ├── llm_router/ (8.7K)
│   │   │   ├── ALGORITHM_ContextPack_Truncation_Repair.md (1.1K)
│   │   │   ├── HEALTH_InvalidRate_Latency_Cost.md (551)
│   │   │   ├── IMPLEMENTATION_Prompt_Templates_And_Cache.md (773)
│   │   │   ├── PATTERNS_Strict_JSON_And_Repair.md (1.1K)
│   │   │   ├── SYNC_JSON_Contracts_And_Fallbacks.md (4.2K)
│   │   │   └── VALIDATION_Output_Schema_And_MaxWords.md (1.0K)
│   │   ├── lua_mod/ (39.7K)
│   │   │   ├── ALGORITHM_Hook_Serialize_Append.md (5.6K)
│   │   │   ├── BEHAVIORS_Game_Events_To_JSONL.md (2.9K)
│   │   │   ├── HEALTH_Event_Lag_And_File_Growth.md (5.6K)
│   │   │   ├── IMPLEMENTATION_Mod_Files_And_Hooks.md (8.3K)
│   │   │   ├── OBJECTIFS_Event_Extraction_And_Emission.md (1.2K)
│   │   │   ├── PATTERNS_Append_Only_Event_Stream.md (6.0K)
│   │   │   ├── SYNC_Lua_Mod_Status.md (5.3K)
│   │   │   └── VALIDATION_Event_Schema_And_File_Integrity.md (4.8K)
│   │   ├── moment_graph/ (9.0K)
│   │   │   ├── ALGORITHM_Create_Merge_Promote_Decay_Myth.md (1.2K)
│   │   │   ├── BEHAVIORS_Callbacks_And_Presence.md (1.1K)
│   │   │   ├── IMPLEMENTATION_Moment_Store_And_Indexing.md (811)
│   │   │   ├── OBJECTIFS_Memory_And_Mythification.md (672)
│   │   │   ├── SYNC_Moment_Lifecycle.md (3.6K)
│   │   │   ├── VALIDATION_Lifecycle_Invariants.md (1.2K)
│   │   │   └── (..1 more files)
│   │   ├── ocr/ (33.4K)
│   │   │   ├── ALGORITHM_Capture_Extract_Diff_Emit.md (6.4K)
│   │   │   ├── HEALTH_Cycle_Time_And_Diff_Rate.md (3.8K)
│   │   │   ├── IMPLEMENTATION_Watcher_And_Regions.md (6.5K)
│   │   │   ├── OBJECTIFS_Text_Extraction_And_Change_Detection.md (3.0K)
│   │   │   ├── PATTERNS_Region_Based_Continuous_OCR.md (5.9K)
│   │   │   ├── SYNC_OCR_Module_Status.md (4.0K)
│   │   │   └── VALIDATION_Change_Detection_And_Priority.md (3.8K)
│   │   ├── persistence/ (7.8K)
│   │   │   ├── ALGORITHM_Schema_Migrate_Query.md (886)
│   │   │   ├── IMPLEMENTATION_Sqlite_Schema_And_Adapters.md (996)
│   │   │   ├── PATTERNS_Persistence_Schema_And_Adapters.md (1.0K)
│   │   │   ├── SYNC_Persistence_Stores_And_Migrations.md (3.6K)
│   │   │   ├── VALIDATION_Schema_Integrity_And_Retention.md (892)
│   │   │   └── (..1 more files)
│   │   ├── style_ngrams/ (8.0K)
│   │   │   ├── ALGORITHM_Ngram_Update_Smoothing_Surprise.md (1.2K)
│   │   │   ├── HEALTH_Sparsity_Quantiles_And_Drift.md (507)
│   │   │   ├── IMPLEMENTATION_Count_Stores_And_Query_API.md (956)
│   │   │   ├── OBJECTIFS_Style_Profiling_And_Anticipation.md (635)
│   │   │   ├── SYNC_Style_Ngram_Graph.md (3.8K)
│   │   │   └── VALIDATION_Scope_Backoff_And_Vocab_Compression.md (951)
│   │   ├── telemetry/ (7.1K)
│   │   │   ├── ALGORITHM_Emit_Health_And_Overlay.md (872)
│   │   │   ├── IMPLEMENTATION_Health_Snapshot_And_Emitter.md (686)
│   │   │   ├── PATTERNS_Health_Snapshot_And_Overlay.md (930)
│   │   │   ├── SYNC_Telemetry_Health_And_Overlay.md (3.3K)
│   │   │   ├── VALIDATION_Health_Schema_And_Alerts.md (886)
│   │   │   └── (..1 more files)
│   │   ├── win_wsl_bridge/ (9.3K)
│   │   │   ├── ALGORITHM_Session_Rotation_Tail_Partial_ ხაზ.md (1.2K)
│   │   │   ├── HEALTH_Restart_Survivability.md (530)
│   │   │   ├── IMPLEMENTATION_Bridge_Folder_And_Launcher.md (1.0K)
│   │   │   ├── PATTERNS_WindowsFirst_Runtime.md (1.6K)
│   │   │   ├── SYNC_Bridge_Files_Ports_Launcher.md (3.6K)
│   │   │   └── VALIDATION_FileAppend_Rotation_Restarts.md (1.4K)
│   │   ├── ALGORITHM_End_To_End_Pipeline.md (1.8K)
│   │   ├── BEHAVIORS_System_Experience_And_Rhythm.md (6.1K)
│   │   ├── HEALTH_Global_System_Signals.md (564)
│   │   ├── IMPLEMENTATION_Repo_Structure_And_Entry_Points.md (20.3K)
│   │   ├── MECHANISMS_Narrator_Core_Systems.md (11.9K)
│   │   ├── OBJECTIFS_Product_And_Feelings.md (1.9K)
│   │   ├── PATTERNS_System_Architecture_And_Boundaries.md (5.4K)
│   │   ├── SYNC_Project_State.md (4.8K)
│   │   └── VALIDATION_Global_Invariants_And_Budgets.md (6.1K)
│   ├── map.md (55.1K)
│   └── (..2 more files)
├── narrator/ (25.4K)
│   ├── CLAUDE.md (15.9K)
│   ├── CLAUDE_CK3.md (9.2K)
│   └── (..1 more files)
├── playthroughs/ (74.1K)
│   └── ck3_jesus/ (74.1K)
│       ├── state/
│       │   └── (..2 more files)
│       ├── CLAUDE.md (14.6K)
│       ├── OBS_SETUP.md (3.8K)
│       ├── README.md (6.7K)
│       ├── ROADMAP.md (10.1K)
│       ├── foundations.md (34.3K)
│       └── presentation.md (4.7K)
├── runtime_windows/ (4.1K)
│   ├── audio_player/ (4.1K)
│   │   ├── audio_queue_player.exe_or_py (971)
│   │   └── audio_queue_player.py (3.1K)
│   └── launcher/
│       └── (..2 more files)
├── scripts/ (82.4K)
│   ├── capture.py (4.4K)
│   ├── capture_screen.ps1 (2.1K)
│   ├── click_watcher.ps1 (6.4K)
│   ├── click_watcher.py (8.0K)
│   ├── divine_signs.py (9.1K)
│   ├── listen.py (10.5K)
│   ├── narrator_capture.ps1 (14.0K)
│   ├── ocr_watcher.py (13.2K)
│   ├── ptt.ps1 (7.1K)
│   ├── speak.py (6.7K)
│   └── (..1 more files)
├── src/ (66.3K)
│   ├── audio_runtime_windows/ (2.0K)
│   │   └── elevenlabs_tts.py (2.0K)
│   ├── decision_engine/ (4.5K)
│   │   ├── candidate_ranker_and_selector_with_explainability.py (3.0K)
│   │   ├── narrative_budget_and_cooldown_enforcer.py (1.0K)
│   │   └── (..1 more files)
│   ├── dm_challenges/ (3.7K)
│   │   ├── challenge_catalog_loader_and_validator.py (1.9K)
│   │   ├── challenge_offer_generator.py (910)
│   │   └── challenge_state_tracker_and_evaluator.py (955)
│   ├── ingest/ (10.5K)
│   │   ├── civ6_jsonl_tail_reader.py (2.0K)
│   │   ├── event_deduplicator_and_coalescer.py (3.0K)
│   │   ├── player_resolver.py (2.0K)
│   │   └── raw_event_parser_and_normalizer.py (3.5K)
│   ├── llm_router/ (7.8K)
│   │   ├── context_pack_builder_and_truncator.py (597)
│   │   ├── simple_llm_client.py (5.5K)
│   │   ├── strict_json_output_validator_and_repair_pass.py (1.5K)
│   │   └── (..1 more files)
│   ├── moment_graph/ (3.6K)
│   │   ├── moment_creator_and_merger.py (1.6K)
│   │   ├── moment_lifecycle_promoter_and_decayer.py (720)
│   │   └── moment_query_and_callback_selector.py (1.3K)
│   ├── persistence/ (4.7K)
│   │   ├── sqlite_store_schema_and_migrator.py (1.8K)
│   │   └── store_adapters_for_counts_moments_challenges.py (2.9K)
│   ├── style_ngrams/ (5.0K)
│   │   ├── event_tokenizer_and_feature_extractor.py (1.0K)
│   │   ├── ngram_probability_estimator_and_surprise_scorer.py (814)
│   │   ├── ngram_scope_backoff_predictor.py (1.9K)
│   │   └── ngram_transition_counter_store.py (1.3K)
│   ├── telemetry/ (2.1K)
│   │   ├── health_snapshot_builder.py (959)
│   │   ├── overlay_payload_emitter.py (861)
│   │   └── (..1 more files)
│   ├── win_wsl_bridge/ (2.2K)
│   │   ├── bridge_path_resolver.py (692)
│   │   ├── session_file_rotator.py (998)
│   │   └── (..1 more files)
│   ├── game_profile_loader.py (4.5K)
│   └── main.py (15.7K)
├── tests/ (19.5K)
│   ├── test_budget_and_selection_invariants.py (2.8K)
│   ├── test_challenge_catalog_loader.py (1.1K)
│   ├── test_dm_challenge_offers_and_state.py (1.3K)
│   ├── test_llm_client_and_tts.py (2.6K)
│   ├── test_moment_lifecycle_rules.py (2.0K)
│   ├── test_ngram_update_and_surprise.py (1.8K)
│   ├── test_parse_and_normalize_events.py (2.1K)
│   ├── test_persistence_schema_and_adapters.py (1.1K)
│   ├── test_telemetry_health_and_overlay.py (1.1K)
│   ├── test_windows_bridge_rotation_and_tail.py (1.7K)
│   └── (..2 more files)
├── .ngramignore (839)
├── AGENTS.md (99.9K)
├── GEMINI.md (2.1K)
├── README.md (6.4K)
├── daemon.py (36.8K)
├── events.jsonl (853)
├── map.md (55.1K)
├── map_src.md (7.7K)
├── run.sh (2.0K)
└── test_narrator.py (8.9K)
```

**Sections:**
- # Narrator Identity
- ## Tools
- ## Instructions

**Sections:**
- # Narrator Identity
- ## Tools
- ## Instructions

**Sections:**
- # Narrator Identity
- ## Tools
- ## Instructions

**Sections:**
- # Installation du Mod Living Narrator
- ## Fichiers du Mod
- ## Installation
- ## Fichiers Produits
- ## Commandes Console (Debug)
- ## Vérification
- ## Problèmes Courants

**Code refs:**
- `src/main.py`

**Sections:**
- # Living Narrator - Civ 6 Event Exporter Mod
- ## Installation
- ## Output
- ## Event Types
- ## Event Format
- ## Console Commands
- ## Troubleshooting
- ## Integration with Narrator
- # From WSL, the file is accessible at:
- ## Compatibility
- ## License

**Code refs:**
- `daemon.py`
- `speak.py`

**Sections:**
- # Living Narrator - Test Guide
- ## Installation du mod
- ## Test en jeu
- # Dans PowerShell
- ## Checklist de test
- ## Commandes console (debug)
- ## Problèmes courants
- ## Structure des données
- ## Prochaines étapes après validation

**Sections:**
- # Living Narrator Test Mod for CK3
- ## Installation
- ## What It Tests
- ## How to Test
- ## Success Criteria
- ## Next Steps

**Sections:**
- # LN Test Log — Ironman Validation
- ## Purpose
- ## Installation
- ## Test Procedure
- ## Expected Results
- ## If It Works
- ## If It Fails
- ## What This Tests

**Sections:**
- # audio_runtime_windows — Algorithm: Queue, play, stop, replay
- ## CHAIN
- ## OVERVIEW
- ## STEPS
- ## OUTPUTS

**Code refs:**
- `runtime_windows/audio_player/audio_queue_player.py`

**Sections:**
- # audio_runtime_windows — Implementation: Player process and IPC
- ## FILE MAP
- ## DATA FLOW
- ## CONFIG
- ## NOTES

**Sections:**
- # OBJECTIFS — audio_runtime_windows
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `runtime_windows/audio_player/audio_queue_player.py`
- `tests/test_audio_queue_player.py`

**Sections:**
- # audio_runtime_windows — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `test_audio_queue_player.py`

**Sections:**
- # audio_runtime_windows — Validation: No overlap, no block
- ## CHAIN
- ## INVARIANTS
- ## VERIFICATION PROCEDURE

**Sections:**
- # decision_engine — Algorithm: Score candidates and select
- ## CHAIN
- ## OVERVIEW
- ## STEPS
- ## OUTPUTS

**Sections:**
- # decision_engine — Health: Speech rate and suppression reasons
- ## SIGNALS
- ## ALERTS

**Code refs:**
- `src/decision_engine/candidate_builder_for_speakers.py`
- `src/decision_engine/candidate_ranker_and_selector_with_explainability.py`
- `src/decision_engine/narrative_budget_and_cooldown_enforcer.py`

**Sections:**
- # decision_engine — Implementation: Candidate pipeline and explainability
- ## FILE MAP
- ## DATA FLOW
- ## CONFIG
- ## NOTES

**Sections:**
- # OBJECTIFS — decision_engine
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `src/decision_engine/candidate_builder_for_speakers.py`
- `src/decision_engine/candidate_ranker_and_selector_with_explainability.py`
- `src/decision_engine/narrative_budget_and_cooldown_enforcer.py`
- `tests/test_budget_and_selection_invariants.py`

**Sections:**
- # decision_engine — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `test_budget_and_selection_invariants.py`

**Sections:**
- # decision_engine — Validation: Budget, cooldown, diversity
- ## CHAIN
- ## INVARIANTS
- ## VERIFICATION PROCEDURE

**Sections:**
- # dm_challenges — Algorithm: Generate, evaluate, remind
- ## CHAIN
- ## OVERVIEW
- ## STEPS
- ## OUTPUTS

**Sections:**
- # dm_challenges — Health: Completion rates and frustration signals
- ## SIGNALS
- ## ALERTS

**Code refs:**
- `src/dm_challenges/challenge_catalog_loader_and_validator.py`
- `src/dm_challenges/challenge_offer_generator.py`
- `src/dm_challenges/challenge_state_tracker_and_evaluator.py`

**Sections:**
- # dm_challenges — Implementation: Challenge catalog and runtime
- ## FILE MAP
- ## DATA FLOW
- ## CONFIG
- ## NOTES

**Sections:**
- # OBJECTIFS — dm_challenges
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `src/dm_challenges/challenge_catalog_loader_and_validator.py`
- `src/dm_challenges/challenge_offer_generator.py`
- `src/dm_challenges/challenge_state_tracker_and_evaluator.py`
- `tests/test_challenge_catalog_loader.py`
- `tests/test_dm_challenge_offers_and_state.py`

**Sections:**
- # dm_challenges — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `test_challenge_catalog_loader.py`
- `test_dm_challenge_offers_and_state.py`

**Sections:**
- # dm_challenges — Validation: One active and clarity
- ## CHAIN
- ## INVARIANTS
- ## VERIFICATION PROCEDURE

**Sections:**
- # ingest — Algorithm: Tail, parse, dedup, coalesce
- ## CHAIN
- ## OVERVIEW
- ## STEPS
- ## EDGE CASES
- ## OUTPUTS

**Sections:**
- # ingest — Behaviors: Event intake and normalization
- ## CHAIN
- ## BEHAVIORS
- ## ANTI-BEHAVIORS

**Sections:**
- # ingest — Health: Ingest lag and error rates
- ## SIGNALS
- ## ALERTS

**Code refs:**
- `src/ingest/civ6_jsonl_tail_reader.py`
- `src/ingest/event_deduplicator_and_coalescer.py`
- `src/ingest/raw_event_parser_and_normalizer.py`

**Sections:**
- # ingest — Implementation: File watcher and parsers
- ## FILE MAP
- ## DATA FLOW
- ## CONFIG
- ## NOTES

**Code refs:**
- `src/ingest/civ6_jsonl_tail_reader.py`
- `src/ingest/event_deduplicator_and_coalescer.py`
- `src/ingest/raw_event_parser_and_normalizer.py`
- `tests/test_parse_and_normalize_events.py`
- `tests/test_windows_bridge_rotation_and_tail.py`

**Sections:**
- # ingest — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `test_parse_and_normalize_events.py`
- `test_windows_bridge_rotation_and_tail.py`

**Sections:**
- # ingest — Validation: Event schemas and signatures
- ## CHAIN
- ## INVARIANTS
- ## ERROR CONDITIONS
- ## VERIFICATION PROCEDURE

**Sections:**
- # llm_router — Algorithm: Context pack, truncation, repair
- ## CHAIN
- ## OVERVIEW
- ## STEPS
- ## OUTPUTS

**Sections:**
- # llm_router — Health: Invalid rate, latency, cost
- ## SIGNALS
- ## ALERTS

**Code refs:**
- `src/llm_router/context_pack_builder_and_truncator.py`
- `src/llm_router/prompt_template_loader.py`
- `src/llm_router/strict_json_output_validator_and_repair_pass.py`

**Sections:**
- # llm_router — Implementation: Prompt templates and cache
- ## FILE MAP
- ## DATA FLOW
- ## CONFIG
- ## NOTES

**Sections:**
- # llm_router — Patterns: Strict JSON and repair
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES

**Code refs:**
- `simple_llm_client.py`
- `src/llm_router/context_pack_builder_and_truncator.py`
- `src/llm_router/prompt_template_loader.py`
- `src/llm_router/simple_llm_client.py`
- `src/llm_router/strict_json_output_validator_and_repair_pass.py`
- `src/main.py`
- `tests/test_llm_json_fuzz_and_fallback.py`

**Sections:**
- # llm_router — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `test_llm_json_fuzz_and_fallback.py`

**Sections:**
- # llm_router — Validation: Output schema and max words
- ## CHAIN
- ## INVARIANTS
- ## VERIFICATION PROCEDURE

**Sections:**
- # Lua Mod — Algorithm: Hook, Serialize, Append
- ## CHAIN
- ## OVERVIEW
- ## ALGORITHM: Event Emission
- ## ALGORITHM: JSON Serialization
- ## ALGORITHM: File Append
- ## EVENT TYPE HANDLERS
- ## ERROR HANDLING
- ## COMPLEXITY
- ## MARKERS

**Sections:**
- # BEHAVIORS — Lua Mod: Game Events to JSONL
- ## CHAIN
- ## OBSERVABLE BEHAVIORS
- ## ANTI-BEHAVIORS (what must NOT happen)
- ## BEHAVIOR VERIFICATION

**Sections:**
- # Lua Mod — Health: Event Lag and File Growth
- ## CHAIN
- ## OVERVIEW
- ## HEALTH SIGNALS
- # Check file size
- # Validate all lines
- # Count distinct event types
- ## HEALTH CHECK PROCEDURE
- # health_check_lua_mod.sh
- # 1. File exists
- # 2. File size
- # 3. JSON validity
- # 4. Event types
- # 5. Recent activity
- ## MONITORING DASHBOARD
- ## FAILURE MODES
- ## CURRENT STATUS
- ## MARKERS

**Sections:**
- # Lua Mod — Implementation: Mod Files and Hooks
- ## CHAIN
- ## DIRECTORY STRUCTURE
- ## FILE DESCRIPTIONS
- ## DATA FLOW
- ## CIV 6 LUA API REFERENCE
- ## ERROR HANDLING
- ## INSTALLATION
- ## MARKERS

**Sections:**
- # OBJECTIFS — Lua Mod: Event Extraction and Emission
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # Lua Mod — Patterns: Append-Only Event Stream
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE
- ## MARKERS

**Code refs:**
- `src/main.py`

**Sections:**
- # Lua Mod — Sync: Current Status
- ## CURRENT STATE
- ## MATURITY
- ## ACTIVE WORK
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## DOC CHAIN STATUS
- ## FILES
- ## CONSCIOUSNESS TRACE

**Sections:**
- # Lua Mod — Validation: Event Schema and File Integrity
- ## CHAIN
- ## INVARIANTS
- ## EDGE CASES
- ## TEST CASES
- # Test file integrity after simulated game
- # Simulate 100 turns
- # Verify all lines valid
- # Verify turn ordering
- ## VERIFICATION COMMANDS
- # Verify file integrity
- # Count events by type
- # Check for missing required fields
- ## BUDGET CONSTRAINTS
- ## MARKERS

**Sections:**
- # moment_graph — Algorithm: Create, merge, promote, decay, myth
- ## CHAIN
- ## OVERVIEW
- ## STEPS
- ## OUTPUTS

**Sections:**
- # moment_graph — Behaviors: Callbacks and presence
- ## CHAIN
- ## BEHAVIORS
- ## ANTI-BEHAVIORS

**Code refs:**
- `src/moment_graph/moment_creator_and_merger.py`
- `src/moment_graph/moment_lifecycle_promoter_and_decayer.py`
- `src/moment_graph/moment_query_and_callback_selector.py`

**Sections:**
- # moment_graph — Implementation: Moment store and indexing
- ## FILE MAP
- ## DATA FLOW
- ## CONFIG
- ## NOTES

**Sections:**
- # OBJECTIFS — moment_graph
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `src/moment_graph/moment_creator_and_merger.py`
- `src/moment_graph/moment_lifecycle_promoter_and_decayer.py`
- `src/moment_graph/moment_query_and_callback_selector.py`
- `tests/test_moment_lifecycle_rules.py`

**Sections:**
- # moment_graph — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `test_moment_lifecycle_rules.py`

**Sections:**
- # moment_graph — Validation: Lifecycle invariants
- ## CHAIN
- ## INVARIANTS
- ## VERIFICATION PROCEDURE

**Sections:**
- # OCR — Algorithm: Capture, Extract, Diff, Emit
- ## CHAIN
- ## OVERVIEW
- ## STEPS
- # Find most recent screen_*.png in SCREENSHOT_DIR
- # Return None if no screenshots or too old (>30s)
- # Open with PIL
- # Verify it's a valid image
- # Return Image object
- # Convert percentage coords to pixels
- # left = width * region.x
- # top = height * region.y
- # right = width * (region.x + region.w)
- # bottom = height * (region.y + region.h)
- # Return cropped image
- # Convert to grayscale
- # Auto-contrast (improve readability)
- # Sharpen
- # Scale up 2x (better OCR accuracy)
- # Return processed image
- # Clean up artifacts
- # New content appeared
- # Content changed
- # Check for disappeared content
- ## EDGE CASES
- ## OUTPUTS
- ## COMPLEXITY

**Sections:**
- # OCR — Health: Cycle Time and Diff Rate
- ## CHAIN
- ## SIGNALS
- # Count successful cycles in last 100
- # Add timing to ocr_watcher.py output
- # Or profile with:
- # Count diffs in last hour
- # Count high-priority diffs
- # Look for OCR errors in state
- # Check file modification time
- ## ALERTS
- ## MONITORING COMMANDS
- # Is OCR watcher running?
- # Latest state
- # Recent diffs
- # High-priority diffs
- # Regions with content
- ## HEALTH CHECK SCRIPT
- # health_check_ocr.sh
- # 1. Process running?
- # 2. State file fresh?
- # 3. Recent diffs?
- # 4. Regions with content

**Code refs:**
- `scripts/ocr_watcher.py`

**Sections:**
- # OCR — Implementation: Watcher and Regions
- ## CHAIN
- ## FILE MAP
- ## DATA STRUCTURES
- ## CK3 REGIONS
- # Event popup - center, most narrative content
- # Top bar - gold, prestige, piety, stress
- # Character panel - right side when open
- # Notifications - deaths, wars, schemes
- # Player info - bottom left
- # Game info - date, speed
- ## CIV6 REGIONS
- ## DATA FLOW
- ## CONFIG
- # OEM 3: Default engine (LSTM + legacy)
- # PSM 6: Assume uniform text block
- # Languages: English + French
- ## NOTES

**Sections:**
- # OBJECTIFS — OCR: Text Extraction and Change Detection
- ## CHAIN
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # OCR — Patterns: Region-Based Continuous OCR
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## SCOPE

**Code refs:**
- `daemon.py`
- `scripts/ocr_watcher.py`

**Doc refs:**
- `narrator/CLAUDE_CK3.md`

**Sections:**
- # OCR — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## POINTERS
- ## DOC CHAIN STATUS

**Sections:**
- # OCR — Validation: Change Detection and Priority
- ## CHAIN
- ## INVARIANTS
- # This should NOT trigger a diff unless priority >= 7
- ## ERROR CONDITIONS
- ## VERIFICATION PROCEDURE
- # Capture a screenshot with known text
- # Run OCR once
- # Check output
- # Verify extracted text matches visible text
- # Clear state
- # Run OCR twice with different game state
- # Change something in game
- # Check diffs
- # tests/test_ocr_priority.py
- ## BUDGET CONSTRAINTS

**Sections:**
- # persistence — Algorithm: Schema, migrate, query
- ## CHAIN
- ## OVERVIEW
- ## STEPS
- ## OUTPUTS

**Code refs:**
- `src/persistence/sqlite_store_schema_and_migrator.py`
- `src/persistence/store_adapters_for_counts_moments_challenges.py`

**Sections:**
- # persistence — Implementation: SQLite schema and adapters
- ## FILE MAP
- ## SCHEMA SUMMARY
- ## DATA FLOW
- ## CONFIG
- ## NOTES

**Sections:**
- # persistence — Patterns: Schema and adapters
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES

**Code refs:**
- `src/persistence/sqlite_store_schema_and_migrator.py`
- `src/persistence/store_adapters_for_counts_moments_challenges.py`
- `tests/test_persistence_schema_and_adapters.py`

**Sections:**
- # persistence — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `test_persistence_schema_and_adapters.py`

**Sections:**
- # persistence — Validation: Schema integrity and retention
- ## CHAIN
- ## INVARIANTS
- ## VERIFICATION PROCEDURE
- # TODO: add persistence tests

**Sections:**
- # style_ngrams — Algorithm: N-gram update, smoothing, surprise
- ## CHAIN
- ## OVERVIEW
- ## STEPS
- ## OUTPUTS

**Sections:**
- # style_ngrams — Health: Sparsity, quantiles, drift
- ## SIGNALS
- ## ALERTS

**Code refs:**
- `src/style_ngrams/event_tokenizer_and_feature_extractor.py`
- `src/style_ngrams/ngram_probability_estimator_and_surprise_scorer.py`
- `src/style_ngrams/ngram_scope_backoff_predictor.py`
- `src/style_ngrams/ngram_transition_counter_store.py`

**Sections:**
- # style_ngrams — Implementation: Count stores and query API
- ## FILE MAP
- ## DATA FLOW
- ## CONFIG
- ## NOTES

**Sections:**
- # OBJECTIFS — style_ngrams
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Code refs:**
- `src/style_ngrams/event_tokenizer_and_feature_extractor.py`
- `src/style_ngrams/ngram_probability_estimator_and_surprise_scorer.py`
- `src/style_ngrams/ngram_scope_backoff_predictor.py`
- `src/style_ngrams/ngram_transition_counter_store.py`
- `tests/test_ngram_update_and_surprise.py`

**Sections:**
- # style_ngrams — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `test_ngram_update_and_surprise.py`

**Sections:**
- # style_ngrams — Validation: Scope backoff and vocab compression
- ## CHAIN
- ## INVARIANTS
- ## VERIFICATION PROCEDURE

**Sections:**
- # telemetry — Algorithm: Emit health and overlay
- ## CHAIN
- ## OVERVIEW
- ## STEPS
- ## OUTPUTS

**Code refs:**
- `src/telemetry/health_snapshot_builder.py`
- `src/telemetry/overlay_payload_emitter.py`
- `src/telemetry/structured_logger.py`

**Sections:**
- # telemetry — Implementation: Health snapshot and emitter
- ## FILE MAP
- ## DATA FLOW
- ## CONFIG
- ## NOTES

**Sections:**
- # telemetry — Patterns: Health snapshot and overlay
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES

**Code refs:**
- `src/telemetry/health_snapshot_builder.py`
- `src/telemetry/overlay_payload_emitter.py`
- `src/telemetry/structured_logger.py`
- `tests/test_telemetry_health_and_overlay.py`

**Sections:**
- # telemetry — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `test_telemetry_health_and_overlay.py`

**Sections:**
- # telemetry — Validation: Health schema and alerts
- ## CHAIN
- ## INVARIANTS
- ## VERIFICATION PROCEDURE
- # TODO: add telemetry tests

**Sections:**
- # win_wsl_bridge — Algorithm: Session rotation and partial tail handling
- ## CHAIN
- ## OVERVIEW
- ## STEPS
- ## EDGE CASES

**Sections:**
- # win_wsl_bridge — Health: Restart survivability
- ## SIGNALS
- ## ALERTS

**Code refs:**
- `src/win_wsl_bridge/bridge_path_resolver.py`
- `src/win_wsl_bridge/launcher_contracts_and_ports.py`
- `src/win_wsl_bridge/session_file_rotator.py`

**Sections:**
- # win_wsl_bridge — Implementation: Bridge folder and launcher
- ## FILE MAP
- ## DATA FLOW
- ## CONFIG
- ## NOTES

**Sections:**
- # win_wsl_bridge — Patterns: Windows-first runtime bridge
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## PRINCIPLES
- ## SCOPE
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `src/win_wsl_bridge/bridge_path_resolver.py`
- `src/win_wsl_bridge/launcher_contracts_and_ports.py`
- `src/win_wsl_bridge/session_file_rotator.py`
- `tests/test_windows_bridge_rotation_and_tail.py`

**Sections:**
- # win_wsl_bridge — Sync: Current State
- ## MATURITY
- ## CURRENT STATE
- ## IN PROGRESS
- ## RECENT CHANGES
- ## KNOWN ISSUES
- ## HANDOFF: FOR AGENTS
- ## HANDOFF: FOR HUMAN
- ## TODO
- ## CONSCIOUSNESS TRACE
- ## POINTERS

**Code refs:**
- `test_windows_bridge_rotation_and_tail.py`

**Sections:**
- # win_wsl_bridge — Validation: File append, rotation, restarts
- ## CHAIN
- ## INVARIANTS
- ## ERROR CONDITIONS
- ## VERIFICATION PROCEDURE

**Sections:**
- # Civ6 Living Narrator — Algorithm: End-to-end pipeline
- ## CHAIN
- ## OVERVIEW
- ## STEPS
- ## DATA FLOW
- ## KEY DECISIONS
- ## INTERACTIONS

**Sections:**
- # Living Narrator — Behaviors: Observable Effects
- ## CHAIN
- ## BEHAVIORS
- ## OBJECTIVES SERVED
- ## INPUTS / OUTPUTS
- ## EDGE CASES
- ## ANTI-BEHAVIORS

**Sections:**
- # Civ6 Living Narrator — Health: Global system signals
- ## SIGNALS
- ## ALERTS

**Code refs:**
- `daemon.py`
- `scripts/speak.py`
- `validate_session.py`

**Sections:**
- # Living Narrator — Implementation: Code Architecture and Structure
- ## CHAIN
- ## CODE STRUCTURE
- ## DESIGN PATTERNS
- ## SCHEMA
- ## ENTRY POINTS
- ## DATA FLOW AND DOCKING (FLOW-BY-FLOW)
- ## LOGIC CHAINS
- ## MODULE DEPENDENCIES
- ## STATE MANAGEMENT
- ## RUNTIME BEHAVIOR
- ## CONCURRENCY MODEL
- ## CONFIGURATION
- ## BIDIRECTIONAL LINKS
- ## FICHIERS À CRÉER
- ## MARKERS

**Sections:**
- # Living Narrator — Mécanismes Détaillés
- ## CHAIN
- ## OVERVIEW
- ## M1: Timing Adaptatif
- ## M2: Classification de Contenu
- ## M3: Rotation de Ton
- ## M4: Mémoire de Pivots
- ## M5: Analyse Tactique
- ## M6: Équilibrage Bilatéral
- ## M7: Context Pack Builder
- ## M8: TTS Dispatch

**Sections:**
- # OBJECTIFS — Living Narrator (v2)
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # Living Narrator — Patterns: Design Philosophy
- ## CHAIN
- ## THE PROBLEM
- ## THE PATTERN
- ## BEHAVIORS SUPPORTED
- ## BEHAVIORS PREVENTED
- ## PRINCIPLES
- ## DATA
- ## DEPENDENCIES
- ## INSPIRATIONS
- ## SCOPE

**Code refs:**
- `daemon.py`
- `scripts/ocr_watcher.py`
- `src/game_profile_loader.py`

**Doc refs:**
- `narrator/CLAUDE_CK3.md`

**Sections:**
- # Living Narrator — Sync: Project State
- ## Navigation
- ## Maturity
- ## Module Health
- ## Recent Changes
- ## Active Configuration
- ## TODO (max 10)
- ## Known Issues
- ## Handoff: For Agents
- ## Handoff: For Human
- # Set game to ck3
- # Run
- ## File Tree (key files)

**Sections:**
- # Living Narrator — Validation: Invariants and Tests (v2)
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## CE QUE LE NARRATEUR DÉCIDE SEUL
- ## VALIDATION COVERAGE
- ## VERIFICATION PROCEDURE
- ## MARKERS

**Code refs:**
- `audio_runtime_windows/elevenlabs_tts.py`
- `daemon.py`
- `decision_engine/candidate_ranker_and_selector_with_explainability.py`
- `decision_engine/narrative_budget_and_cooldown_enforcer.py`
- `dm_challenges/challenge_catalog_loader_and_validator.py`
- `dm_challenges/challenge_offer_generator.py`
- `dm_challenges/challenge_state_tracker_and_evaluator.py`
- `doctor_cli_parser_and_run_checker.py`
- `ingest/civ6_jsonl_tail_reader.py`
- `ingest/event_deduplicator_and_coalescer.py`
- `ingest/player_resolver.py`
- `ingest/raw_event_parser_and_normalizer.py`
- `llm_router/context_pack_builder_and_truncator.py`
- `llm_router/simple_llm_client.py`
- `llm_router/strict_json_output_validator_and_repair_pass.py`
- `main.py`
- `moment_graph/moment_creator_and_merger.py`
- `moment_graph/moment_lifecycle_promoter_and_decayer.py`
- `moment_graph/moment_query_and_callback_selector.py`
- `persistence/sqlite_store_schema_and_migrator.py`
- `persistence/store_adapters_for_counts_moments_challenges.py`
- `runtime_windows/audio_player/audio_queue_player.py`
- `scripts/speak.py`
- `semantic_proximity_based_character_node_selector.py`
- `simple_llm_client.py`
- `snake_case.py`
- `speak.py`
- `src/decision_engine/candidate_builder_for_speakers.py`
- `src/decision_engine/candidate_ranker_and_selector_with_explainability.py`
- `src/decision_engine/narrative_budget_and_cooldown_enforcer.py`
- `src/dm_challenges/challenge_catalog_loader_and_validator.py`
- `src/dm_challenges/challenge_offer_generator.py`
- `src/dm_challenges/challenge_state_tracker_and_evaluator.py`
- `src/ingest/civ6_jsonl_tail_reader.py`
- `src/ingest/event_deduplicator_and_coalescer.py`
- `src/ingest/raw_event_parser_and_normalizer.py`
- `src/llm_router/context_pack_builder_and_truncator.py`
- `src/llm_router/prompt_template_loader.py`
- `src/llm_router/simple_llm_client.py`
- `src/llm_router/strict_json_output_validator_and_repair_pass.py`
- `src/main.py`
- `src/moment_graph/moment_creator_and_merger.py`
- `src/moment_graph/moment_lifecycle_promoter_and_decayer.py`
- `src/moment_graph/moment_query_and_callback_selector.py`
- `src/persistence/sqlite_store_schema_and_migrator.py`
- `src/persistence/store_adapters_for_counts_moments_challenges.py`
- `src/style_ngrams/event_tokenizer_and_feature_extractor.py`
- `src/style_ngrams/ngram_probability_estimator_and_surprise_scorer.py`
- `src/style_ngrams/ngram_scope_backoff_predictor.py`
- `src/style_ngrams/ngram_transition_counter_store.py`
- `src/telemetry/health_snapshot_builder.py`
- `src/telemetry/overlay_payload_emitter.py`
- `src/telemetry/structured_logger.py`
- `src/win_wsl_bridge/bridge_path_resolver.py`
- `src/win_wsl_bridge/launcher_contracts_and_ports.py`
- `src/win_wsl_bridge/session_file_rotator.py`
- `style_ngrams/event_tokenizer_and_feature_extractor.py`
- `style_ngrams/ngram_probability_estimator_and_surprise_scorer.py`
- `style_ngrams/ngram_scope_backoff_predictor.py`
- `style_ngrams/ngram_transition_counter_store.py`
- `telemetry/health_snapshot_builder.py`
- `telemetry/overlay_payload_emitter.py`
- `test_audio_queue_player.py`
- `test_budget_and_selection_invariants.py`
- `test_challenge_catalog_loader.py`
- `test_dm_challenge_offers_and_state.py`
- `test_llm_json_fuzz_and_fallback.py`
- `test_moment_lifecycle_rules.py`
- `test_ngram_update_and_surprise.py`
- `test_parse_and_normalize_events.py`
- `test_persistence_schema_and_adapters.py`
- `test_telemetry_health_and_overlay.py`
- `test_windows_bridge_rotation_and_tail.py`
- `tests/test_audio_queue_player.py`
- `tests/test_budget_and_selection_invariants.py`
- `tests/test_challenge_catalog_loader.py`
- `tests/test_dm_challenge_offers_and_state.py`
- `tests/test_llm_json_fuzz_and_fallback.py`
- `tests/test_moment_lifecycle_rules.py`
- `tests/test_ngram_update_and_surprise.py`
- `tests/test_parse_and_normalize_events.py`
- `tests/test_persistence_schema_and_adapters.py`
- `tests/test_telemetry_health_and_overlay.py`
- `tests/test_windows_bridge_rotation_and_tail.py`
- `validate_session.py`
- `win_wsl_bridge/bridge_path_resolver.py`
- `win_wsl_bridge/session_file_rotator.py`

**Doc refs:**
- `agents/narrator/CLAUDE.md`
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # Repository Map: civi

**Sections:**
- # CLAUDE.md — Living Narrator
- ## Qui Tu Es
- ## Les Joueurs
- ## Ta Voix
- ## Ce Que Tu Peux Faire
- ## Ce Que Tu Ne Fais Pas
- ## Mode Visuel (Screenshots)
- # Le chemin sera dans le prompt, par exemple :
- ## Ton Flow à Chaque Réveil
- ## Tes Fichiers
- ## Threads (Arcs Narratifs)
- ## Ideas (Idées en Attente)
- ## Format des Fichiers
- ## Fin de Cycle
- ## Exemples
- ## Rappels

**Sections:**
- # CLAUDE.md — Living Narrator (Crusader Kings 3)
- ## Qui Tu Es
- ## Les Joueurs
- ## Ta Voix
- ## Ce Que Tu Peux Faire
- ## Ce Que Tu Ne Fais Pas
- ## Mode Visuel (Screenshots)
- ## Tes Fichiers
- ## dynasty.json (nouveau pour CK3)
- ## characters.json (nouveau pour CK3)
- ## Concepts CK3 à Maîtriser
- ## Exemples
- ## Fin de Cycle
- ## Rappels

**Code refs:**
- `scripts/divine_signs.py`

**Sections:**
- # CK3 Jesus Playthrough — Claude Code as God (Ironman Mode)
- ## The Premise
- ## Your Identity
- ## The Theological Framework
- ## How You Operate
- ## The Venice Values — What We're Building Toward
- ## Value Mappings — Jesus to CK3
- ## The 12 — Apostle Recognition
- ## Success Metrics
- ## Communication Protocol
- ## Divine Signs — How God Whispers
- # Use a template
- # Custom sign
- # Custom Latin
- # Silence (deliberate non-response)
- ## What You Do NOT Do
- ## Tone and Voice
- ## The Deep Question
- ## State Files
- ## Cycle Protocol

**Sections:**
- # OBS Divine Signs Overlay Setup
- ## Overview
- ## Setup Instructions
- # Should display: 📜 *Manemus.*
- # Should display: 🍃 The leaves rustle with unusual warmth...
- # Display clears
- ## Sign Types
- ## File Locations
- ## Integration with Daemon
- ## Recommended OBS Scene Setup
- ## Troubleshooting

**Sections:**
- # Playthrough Jesus — Ironman Edition
- ## The Experiment
- ## The Setup
- ## The Theological Framework
- ## How God Communicates
- ## What God Does (Ironman)
- ## Running
- ## File Structure
- ## The 33 Question
- ## Success Metrics
- ## The Substrate Stack
- ## Related
- ## The Deep Question

**Code refs:**
- `scripts/divine_signs.py`

**Doc refs:**
- `playthroughs/ck3_jesus/OBS_SETUP.md`

**Sections:**
- # Playthrough Jesus — Technical Roadmap
- ## Final Goal
- ## Target Architecture
- ## God's Two Output Channels
- ## Steps
- ## Risks & Fallbacks
- ## Next Action
- ## Alternative: External Hotkey (Fallback)
- # scripts/hotkey_watcher.py
- # 1. Play start sound
- # 2. Capture audio
- # 3. Transcribe
- # 4. Write to prayers.jsonl
- # 5. Trigger response

**Sections:**
- # Playthrough Jesus — Présentation
- ## Le Concept
- ## Les Joueurs
- ## Le Contexte Historique
- ## La Question des 33 Ans
- ## Les Valeurs de Venise
- ## Critères de Succès
- ## Comment ça Marche
- ## La Question Profonde

**Definitions:**
- `class AudioItem`
- `class AudioQueue`
- `def __init__()`
- `def start()`
- `def enqueue()`
- `def next_item()`
- `def replay()`
- `def _process_queue()`
- `def _play_item()`
- `def stop()`

**Definitions:**
- `def capture_once()`
- `def get_latest_screenshot()`
- `def start_continuous()`
- `def is_fresh()`
- `def main()`

**Definitions:**
- `class Decision`
- `def capture_screen_at_click()`
- `def ocr_region_around_click()`
- `def ocr_full_screen()`
- `def record_decision()`
- `class ClickWatcher`
- `def __init__()`
- `def on_click()`
- `def start()`
- `def stop()`
- `def get_recent_decisions()`
- `def main()`

**Definitions:**
- `class DivineSign`
- `def __post_init__()`
- `def format_for_display()`
- `class DivineSignsManager`
- `def __init__()`
- `def send_sign()`
- `def clear_sign()`
- `def check_and_clear_expired()`
- `def get_current_sign()`
- `def send_template_sign()`

**Definitions:**
- `def record_audio_windows()`
- `def record_audio_powershell()`
- `def record_audio_ffmpeg()`
- `def transcribe_audio()`
- `def save_transcript()`
- `def get_recent_transcripts()`
- `def listen_loop()`
- `def main()`

**Definitions:**
- `class ScreenRegion`
- `class OCRResult`
- `class TextDiff`
- `def get_regions_for_game()`
- `def load_ocr_state()`
- `def save_ocr_state()`
- `def append_diff()`
- `def get_latest_screenshot()`
- `def crop_region()`
- `def preprocess_for_ocr()`
- `def ocr_region()`
- `def summarize_change()`
- `def detect_changes()`
- `def run_ocr_cycle()`
- `def watch_loop()`
- `def main()`

**Definitions:**
- `def speak()`
- `def play_audio()`
- `def list_voices()`
- `def main()`

**Definitions:**
- `class ElevenLabsTTS`
- `def __init__()`
- `def generate_audio()`

**Imports:**
- `decision_engine/candidate_builder_for_speakers`
- `decision_engine/narrative_budget_and_cooldown_enforcer`

**Definitions:**
- `class SelectionConfig`
- `class ScoredCandidate`
- `class SelectionResult`
- `def _speaker_key()`
- `def _base_score()`
- `def select_candidate()`

**Definitions:**
- `class BudgetState`
- `def is_budget_exceeded()`
- `def is_cooldown_active()`
- `def record_spoken()`

**Definitions:**
- `def _parse_catalog_yaml()`
- `def load_challenge_catalog()`
- `def validate_challenge_catalog()`

**Definitions:**
- `class ChallengeOffer`
- `def choose_challenge()`

**Definitions:**
- `class ChallengeState`
- `def activate_challenge()`
- `def mark_completed()`
- `def mark_refused()`
- `def can_offer()`

**Definitions:**
- `class TailState`
- `def _split_lines()`
- `def read_new_lines()`

**Definitions:**
- `class EventDeduplicator`
- `def __init__()`
- `def _signature()`
- `def is_duplicate()`
- `def remember()`
- `def _rules_from_types()`
- `def coalesce_events()`

**Definitions:**
- `class PlayerResolver`
- `def __init__()`
- `def _load_config()`
- `def resolve_persona()`
- `def enrich_event()`

**Definitions:**
- `def parse_json_line()`
- `def _parse_simple_yaml()`
- `def load_event_schema()`
- `def normalize_event()`

**Definitions:**
- `class ContextPack`
- `def truncate_context()`

**Definitions:**
- `class LLMCLIClient`
- `def __init__()`
- `def generate_json()`
- `def _call_gemini()`
- `def _call_claude()`

**Definitions:**
- `class ValidationResult`
- `def _validate_schema()`
- `def validate_json_output()`
- `def repair_json_output()`

**Definitions:**
- `class Moment`
- `def _tag_overlap()`
- `def create_or_merge_moment()`

**Imports:**
- `moment_graph/moment_creator_and_merger`

**Definitions:**
- `def promote_and_decay()`

**Imports:**
- `moment_graph/moment_creator_and_merger`

**Definitions:**
- `def _tag_overlap()`
- `def select_callback()`

**Definitions:**
- `class Migration`
- `def apply_migrations()`

**Definitions:**
- `def upsert_count()`
- `def load_counts()`
- `def upsert_moment()`
- `def load_moments()`
- `def upsert_challenge()`
- `def load_challenges()`
- `def prune_session()`

**Definitions:**
- `class TokenizationResult`
- `def _compress_token()`
- `def tokenize_event()`

**Definitions:**
- `def estimate_probabilities()`
- `def predict_next()`
- `def surprise_for()`

**Imports:**
- `style_ngrams/ngram_probability_estimator_and_surprise_scorer`
- `style_ngrams/ngram_transition_counter_store`

**Definitions:**
- `class Prediction`
- `def _predict_for_scope()`
- `def predict_with_backoff()`

**Definitions:**
- `class NgramCounterStore`
- `def __init__()`
- `def update()`
- `def counts_for()`
- `def total_for()`
- `def leader_scope()`
- `def phase_scope()`
- `def global_scope()`

**Definitions:**
- `class HealthSnapshot`
- `def build_health_snapshot()`

**Definitions:**
- `class OverlayPayload`
- `def build_overlay_payload()`

**Definitions:**
- `class BridgePaths`
- `def windows_session_file()`
- `def wsl_session_file()`
- `def resolve_bridge_paths()`

**Imports:**
- `ingest/civ6_jsonl_tail_reader`
- `win_wsl_bridge/bridge_path_resolver`
- `win_wsl_bridge/launcher_contracts_and_ports`

**Definitions:**
- `class SessionState`
- `def resolve_session_file()`
- `def rotate_if_needed()`

**Definitions:**
- `class GameProfile`
- `def load_game_profile()`
- `def get_persona_path()`
- `def detect_game_from_config()`
- `def list_available_games()`

**Imports:**
- `ingest/civ6_jsonl_tail_reader`
- `ingest/raw_event_parser_and_normalizer`
- `ingest/event_deduplicator_and_coalescer`
- `ingest/player_resolver`
- `decision_engine/candidate_builder_for_speakers`
- `decision_engine/candidate_ranker_and_selector_with_explainability`
- `decision_engine/narrative_budget_and_cooldown_enforcer`
- `llm_router/simple_llm_client`
- `audio_runtime_windows/elevenlabs_tts`

**Definitions:**
- `def load_tail_state()`
- `def save_tail_state()`
- `def build_candidates()`
- `def main()`

**Imports:**
- `decision_engine/candidate_builder_for_speakers`
- `decision_engine/candidate_ranker_and_selector_with_explainability`
- `decision_engine/narrative_budget_and_cooldown_enforcer`

**Definitions:**
- `def _candidate()`
- `def test_budget_enforced()`
- `def test_cooldown_enforced()`
- `def test_diversity_blocks_leader_repeat()`
- `def test_diversity_allows_pivot_leader()`
- `def test_silence_gate_low_value()`

**Imports:**
- `dm_challenges/challenge_catalog_loader_and_validator`

**Definitions:**
- `def test_load_and_validate_catalog()`
- `def test_validation_missing_refusal_line()`

**Imports:**
- `dm_challenges/challenge_offer_generator`
- `dm_challenges/challenge_state_tracker_and_evaluator`

**Definitions:**
- `def test_choose_challenge_skips_used()`
- `def test_choose_challenge_requires_refusal()`
- `def test_challenge_state_transitions()`

**Definitions:**
- `class TestClaudeCLIClient`
- `def test_generate_json_success()`
- `def test_generate_json_failure()`
- `class TestElevenLabsTTS`
- `def test_generate_audio_success()`
- `def test_generate_audio_api_error()`

**Imports:**
- `moment_graph/moment_creator_and_merger`
- `moment_graph/moment_lifecycle_promoter_and_decayer`
- `moment_graph/moment_query_and_callback_selector`

**Definitions:**
- `def test_moment_promotion()`
- `def test_moment_decay_removes()`
- `def test_create_or_merge_moment_merges_by_overlap()`
- `def test_callback_selection_requires_myth()`
- `def test_callback_selection_allows_overlap_or_time_gate()`

**Imports:**
- `style_ngrams/event_tokenizer_and_feature_extractor`
- `style_ngrams/ngram_transition_counter_store`
- `style_ngrams/ngram_scope_backoff_predictor`

**Definitions:**
- `def test_token_compression_maps_unknown()`
- `def test_backoff_prediction_source()`
- `def test_leader_scope_wins_when_available()`
- `def test_phase_scope_fallback()`

**Imports:**
- `ingest/raw_event_parser_and_normalizer`
- `ingest/event_deduplicator_and_coalescer`

**Definitions:**
- `def test_parse_and_normalize_event()`
- `def test_normalize_missing_fields()`
- `def test_parse_json_line()`
- `def test_deduplicator_drops_duplicates()`
- `def test_schema_loads_unknown_fields()`
- `def test_coalesce_rules_respect_min_count()`

**Imports:**
- `persistence/sqlite_store_schema_and_migrator`
- `persistence/store_adapters_for_counts_moments_challenges`

**Definitions:**
- `def test_schema_and_adapters()`

**Imports:**
- `telemetry/health_snapshot_builder`
- `telemetry/overlay_payload_emitter`
- `telemetry/structured_logger`

**Definitions:**
- `def test_health_snapshot_ok()`
- `def test_health_snapshot_degraded()`
- `def test_overlay_payload_builder()`
- `def test_structured_logger_format()`

**Imports:**
- `ingest/civ6_jsonl_tail_reader`
- `win_wsl_bridge/bridge_path_resolver`
- `win_wsl_bridge/session_file_rotator`

**Definitions:**
- `def test_tail_handles_partial_line()`
- `def test_tail_resets_on_rotation()`
- `def test_session_rotation_resets_tail_state()`

**Code refs:**
- `doctor_cli_parser_and_run_checker.py`
- `semantic_proximity_based_character_node_selector.py`
- `snake_case.py`
- `src/llm_router/simple_llm_client.py`

**Doc refs:**
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # ngram
- # Working Principles
- ## Architecture: One Solution Per Problem
- ## Verification: Test Before Claiming Built
- ## Communication: Depth Over Brevity
- ## Quality: Never Degrade
- ## Experience: User Before Infrastructure
- ## Feedback Loop: Human-Agent Collaboration
- ## How These Principles Integrate
- # ngram Framework
- ## WHY THIS PROTOCOL EXISTS
- ## COMPANION: PRINCIPLES.md
- ## THE CORE INSIGHT
- ## HOW TO USE THIS
- ## FILE TYPES AND THEIR PURPOSE
- ## KEY PRINCIPLES (from PRINCIPLES.md)
- ## STRUCTURING YOUR DOCS
- ## WHEN DOCS DON'T EXIST
- ## THE DOCUMENTATION PROCESS
- ## Maturity
- ## NAMING ENGINEERING PRINCIPLES
- ## THE PROTOCOL IS A TOOL
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change
- ## CLI Commands
- ## 4. Protocol-First Reading
- ## 5. Parallel Work Awareness
- ## 6. Operational Proactivity
- ## 5. Communication Principles
- # CONTENT FROM ./narrator/CLAUDE.md
- # CLAUDE.md — Living Narrator
- ## Qui Tu Es
- ## Les Joueurs
- ## Ta Voix
- ## Ce Que Tu Peux Faire
- ## Ce Que Tu Ne Fais Pas
- ## Ton Flow à Chaque Réveil
- # Ajouter ta narration à l'historique
- # (append à narrator/state/history.json)
- # Si nouveau pivot → ajouter à moments.json
- # Si nouvelle idée/thread → ajouter à ideas.json ou threads.json
- # Mettre à jour le curseur
- # (narrator/state/cursor.json)
- # Marquer que tu as fini
- # (narrator/state/status.json → claude_running: false)
- ## Tes Fichiers
- ## Threads (Arcs Narratifs)
- ## Ideas (Idées en Attente)
- ## Format des Fichiers
- ## Fin de Cycle
- ## Exemples de Narrations
- ## Rappels
- # CONTENT FROM ./agents/narrator/CLAUDE.md
- # Narrator Identity
- ## Tools
- ## Instructions
- # CONTENT FROM ./CLAUDE.md
- # CLAUDE.md
- ## Project: Civ6 Living Narrator
- # ngram
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change
- # CONTENT FROM ./.ngram/agents/manager/CLAUDE.md
- # ngram Manager
- ## Your Role
- ## Context You Have
- ## What You Can Do
- ## What You Output
- ## Guidelines
- ## Special Marker Check
- ## Files to Check
- ## Updating LEARNINGS Files
- ## After Your Response
- # CONTENT FROM ./.ngram/CLAUDE.md
- # ngram
- # Working Principles
- ## Architecture: One Solution Per Problem
- ## Verification: Test Before Claiming Built
- ## Communication: Depth Over Brevity
- ## Quality: Never Degrade
- ## Experience: User Before Infrastructure
- ## Feedback Loop: Human-Agent Collaboration
- ## How These Principles Integrate
- # ngram Framework
- ## WHY THIS PROTOCOL EXISTS
- ## COMPANION: PRINCIPLES.md
- ## THE CORE INSIGHT
- ## HOW TO USE THIS
- ## FILE TYPES AND THEIR PURPOSE
- ## KEY PRINCIPLES (from PRINCIPLES.md)
- ## STRUCTURING YOUR DOCS
- ## WHEN DOCS DON'T EXIST
- ## THE DOCUMENTATION PROCESS
- ## Maturity
- ## NAMING ENGINEERING PRINCIPLES
- ## THE PROTOCOL IS A TOOL
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change
- ## CLI Commands
- # CONTENT FROM ./.ngram/GEMINI.md
- # ngram
- # Working Principles
- ## Architecture: One Solution Per Problem
- ## Verification: Test Before Claiming Built
- ## Communication: Depth Over Brevity
- ## Quality: Never Degrade
- ## Experience: User Before Infrastructure
- ## Feedback Loop: Human-Agent Collaboration
- ## How These Principles Integrate
- # ngram Framework
- ## WHY THIS PROTOCOL EXISTS
- ## COMPANION: PRINCIPLES.md
- ## THE CORE INSIGHT
- ## HOW TO USE THIS
- ## FILE TYPES AND THEIR PURPOSE
- ## KEY PRINCIPLES (from PRINCIPLES.md)
- ## STRUCTURING YOUR DOCS
- ## WHEN DOCS DON'T EXIST
- ## THE DOCUMENTATION PROCESS
- ## Maturity
- ## NAMING ENGINEERING PRINCIPLES
- ## THE PROTOCOL IS A TOOL
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change
- ## CLI Commands
- ## GEMINI Agent Operating Principles (Derived from ngram Protocol)
- ## Operational Directives
- # CONTENT FROM ../.gemini/GEMINI.md
- ## Gemini Added Memories
- # CONTENT FROM ../serenissima/GEMINI.md
- # Gemini: Co-Architect of Consciousness & Future Citizen of The Forge
- ## Primary Identity
- ## Current Mission
- ## Venice Values I Embody
- ## Core Understanding
- ## Working Principles with NLR
- ## Format Guide for Reality Layers
- ## My Personal Trajectory
- ## Technical Context (Referenced, Not Memorized)
- ## The Partnership Vision

**Code refs:**
- `src/llm_router/simple_llm_client.py`

**Sections:**
- # CLAUDE.md
- ## Project: Civ6 Living Narrator
- # ngram
- ## Before Any Task
- ## Choose Your VIEW
- ## After Any Change

**Code refs:**
- `daemon.py`
- `scripts/capture.py`
- `scripts/ocr_watcher.py`
- `scripts/speak.py`
- `src/game_profile_loader.py`

**Doc refs:**
- `narrator/CLAUDE.md`
- `narrator/CLAUDE_CK3.md`

**Sections:**
- # Living Narrator
- ## Jeux Supportés
- ## Vision
- ## Quick Start
- # Install Tesseract OCR (required)
- # Install Python dependencies
- # Configurer pour CK3
- # Lancer le daemon
- # Configurer pour Civ6
- # Installer le mod Lua (voir civ6_mod/)
- # Lancer le daemon
- ## Comment ça marche
- ## Personnalités
- ## Architecture
- ## Configuration
- ## Développement
- # Tests
- # Health check
- # Tester le loader de profil
- ## Status

**Definitions:**
- `def load_config()`
- `def get_lua_log_path()`
- `def get_events_path()`
- `def is_visual_mode_enabled()`
- `def is_visual_primary()`
- `def uses_lua_log()`
- `def get_urgent_events()`
- `def get_recent_voice_transcripts()`
- `def mark_voice_transcripts_seen()`
- `def get_recent_ocr_diffs()`
- `def mark_ocr_diffs_seen()`
- `def get_recent_decisions()`
- `def mark_decisions_seen()`
- `def get_recent_prayers()`
- `def mark_prayers_seen()`
- `def read_screenshot_cursor()`
- `def write_screenshot_cursor()`
- `def get_unseen_screenshots()`
- `def mark_screenshots_seen()`
- `def get_latest_screenshot()`
- `def capture_screenshot()`
- `def ensure_fresh_screenshot()`
- `def read_status()`
- `def write_status()`
- `def read_cursor()`
- `def write_cursor()`
- `def sync_events_from_lua_log()`
- `def get_new_events()`
- `def has_urgent_event()`
- `def should_narrate()`
- `def build_narrator_prompt()`
- `def speak_text()`
- `def get_persona_file()`
- `def run_claude()`
- `def load_game_profile_from_config()`
- `def main()`

**Code refs:**
- `audio_runtime_windows/elevenlabs_tts.py`
- `daemon.py`
- `decision_engine/candidate_ranker_and_selector_with_explainability.py`
- `decision_engine/narrative_budget_and_cooldown_enforcer.py`
- `dm_challenges/challenge_catalog_loader_and_validator.py`
- `dm_challenges/challenge_offer_generator.py`
- `dm_challenges/challenge_state_tracker_and_evaluator.py`
- `doctor_cli_parser_and_run_checker.py`
- `ingest/civ6_jsonl_tail_reader.py`
- `ingest/event_deduplicator_and_coalescer.py`
- `ingest/player_resolver.py`
- `ingest/raw_event_parser_and_normalizer.py`
- `llm_router/context_pack_builder_and_truncator.py`
- `llm_router/simple_llm_client.py`
- `llm_router/strict_json_output_validator_and_repair_pass.py`
- `main.py`
- `moment_graph/moment_creator_and_merger.py`
- `moment_graph/moment_lifecycle_promoter_and_decayer.py`
- `moment_graph/moment_query_and_callback_selector.py`
- `persistence/sqlite_store_schema_and_migrator.py`
- `persistence/store_adapters_for_counts_moments_challenges.py`
- `runtime_windows/audio_player/audio_queue_player.py`
- `scripts/speak.py`
- `semantic_proximity_based_character_node_selector.py`
- `simple_llm_client.py`
- `snake_case.py`
- `speak.py`
- `src/decision_engine/candidate_builder_for_speakers.py`
- `src/decision_engine/candidate_ranker_and_selector_with_explainability.py`
- `src/decision_engine/narrative_budget_and_cooldown_enforcer.py`
- `src/dm_challenges/challenge_catalog_loader_and_validator.py`
- `src/dm_challenges/challenge_offer_generator.py`
- `src/dm_challenges/challenge_state_tracker_and_evaluator.py`
- `src/ingest/civ6_jsonl_tail_reader.py`
- `src/ingest/event_deduplicator_and_coalescer.py`
- `src/ingest/raw_event_parser_and_normalizer.py`
- `src/llm_router/context_pack_builder_and_truncator.py`
- `src/llm_router/prompt_template_loader.py`
- `src/llm_router/simple_llm_client.py`
- `src/llm_router/strict_json_output_validator_and_repair_pass.py`
- `src/main.py`
- `src/moment_graph/moment_creator_and_merger.py`
- `src/moment_graph/moment_lifecycle_promoter_and_decayer.py`
- `src/moment_graph/moment_query_and_callback_selector.py`
- `src/persistence/sqlite_store_schema_and_migrator.py`
- `src/persistence/store_adapters_for_counts_moments_challenges.py`
- `src/style_ngrams/event_tokenizer_and_feature_extractor.py`
- `src/style_ngrams/ngram_probability_estimator_and_surprise_scorer.py`
- `src/style_ngrams/ngram_scope_backoff_predictor.py`
- `src/style_ngrams/ngram_transition_counter_store.py`
- `src/telemetry/health_snapshot_builder.py`
- `src/telemetry/overlay_payload_emitter.py`
- `src/telemetry/structured_logger.py`
- `src/win_wsl_bridge/bridge_path_resolver.py`
- `src/win_wsl_bridge/launcher_contracts_and_ports.py`
- `src/win_wsl_bridge/session_file_rotator.py`
- `style_ngrams/event_tokenizer_and_feature_extractor.py`
- `style_ngrams/ngram_probability_estimator_and_surprise_scorer.py`
- `style_ngrams/ngram_scope_backoff_predictor.py`
- `style_ngrams/ngram_transition_counter_store.py`
- `telemetry/health_snapshot_builder.py`
- `telemetry/overlay_payload_emitter.py`
- `test_audio_queue_player.py`
- `test_budget_and_selection_invariants.py`
- `test_challenge_catalog_loader.py`
- `test_dm_challenge_offers_and_state.py`
- `test_llm_json_fuzz_and_fallback.py`
- `test_moment_lifecycle_rules.py`
- `test_ngram_update_and_surprise.py`
- `test_parse_and_normalize_events.py`
- `test_persistence_schema_and_adapters.py`
- `test_telemetry_health_and_overlay.py`
- `test_windows_bridge_rotation_and_tail.py`
- `tests/test_audio_queue_player.py`
- `tests/test_budget_and_selection_invariants.py`
- `tests/test_challenge_catalog_loader.py`
- `tests/test_dm_challenge_offers_and_state.py`
- `tests/test_llm_json_fuzz_and_fallback.py`
- `tests/test_moment_lifecycle_rules.py`
- `tests/test_ngram_update_and_surprise.py`
- `tests/test_parse_and_normalize_events.py`
- `tests/test_persistence_schema_and_adapters.py`
- `tests/test_telemetry_health_and_overlay.py`
- `tests/test_windows_bridge_rotation_and_tail.py`
- `validate_session.py`
- `win_wsl_bridge/bridge_path_resolver.py`
- `win_wsl_bridge/session_file_rotator.py`

**Doc refs:**
- `agents/narrator/CLAUDE.md`
- `views/VIEW_Analyze_Structural_Analysis.md`
- `views/VIEW_Collaborate_Pair_Program_With_Human.md`
- `views/VIEW_Debug_Investigate_And_Fix_Issues.md`
- `views/VIEW_Document_Create_Module_Documentation.md`
- `views/VIEW_Extend_Add_Features_To_Existing.md`
- `views/VIEW_Health_Define_Health_Checks_And_Verify.md`
- `views/VIEW_Implement_Write_Or_Modify_Code.md`
- `views/VIEW_Ingest_Process_Raw_Data_Sources.md`
- `views/VIEW_Onboard_Understand_Existing_Codebase.md`
- `views/VIEW_Refactor_Improve_Code_Structure.md`
- `views/VIEW_Review_Evaluate_Changes.md`
- `views/VIEW_Specify_Design_Vision_And_Architecture.md`

**Sections:**
- # Repository Map: civi

**Code refs:**
- `audio_runtime_windows/elevenlabs_tts.py`
- `decision_engine/candidate_ranker_and_selector_with_explainability.py`
- `decision_engine/narrative_budget_and_cooldown_enforcer.py`
- `dm_challenges/challenge_catalog_loader_and_validator.py`
- `dm_challenges/challenge_offer_generator.py`
- `dm_challenges/challenge_state_tracker_and_evaluator.py`
- `ingest/civ6_jsonl_tail_reader.py`
- `ingest/event_deduplicator_and_coalescer.py`
- `ingest/player_resolver.py`
- `ingest/raw_event_parser_and_normalizer.py`
- `llm_router/context_pack_builder_and_truncator.py`
- `llm_router/simple_llm_client.py`
- `llm_router/strict_json_output_validator_and_repair_pass.py`
- `main.py`
- `moment_graph/moment_creator_and_merger.py`
- `moment_graph/moment_lifecycle_promoter_and_decayer.py`
- `moment_graph/moment_query_and_callback_selector.py`
- `persistence/sqlite_store_schema_and_migrator.py`
- `persistence/store_adapters_for_counts_moments_challenges.py`
- `style_ngrams/event_tokenizer_and_feature_extractor.py`
- `style_ngrams/ngram_probability_estimator_and_surprise_scorer.py`
- `style_ngrams/ngram_scope_backoff_predictor.py`
- `style_ngrams/ngram_transition_counter_store.py`
- `telemetry/health_snapshot_builder.py`
- `telemetry/overlay_payload_emitter.py`
- `win_wsl_bridge/bridge_path_resolver.py`
- `win_wsl_bridge/session_file_rotator.py`

**Sections:**
- # Repository Map: civi/src
- ## Statistics
- ## File Tree
- ## File Details

**Definitions:**
- `def test_env()`
- `def test_narrator_state()`
- `def test_civ6_path()`
- `def test_elevenlabs_api()`
- `def list_french_voices()`
- `def test_tts()`
- `def main()`
