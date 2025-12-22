# Repository Map: civi

*Generated: 2025-12-22 18:47*

- **Files:** 111
- **Directories:** 30
- **Total Size:** 276.8K
- **Doc Files:** 71
- **Code Files:** 37
- **Areas:** 1 (docs/ subfolders)
- **Modules:** 10 (subfolders in areas)
- **DOCS Links:** 0 (0.0 avg per code file)

- markdown: 71
- python: 37

```
├── agents/ (960)
│   └── narrator/ (960)
│       └── CLAUDE.md (960)
├── docs/ (137.4K)
│   ├── civ6_living_narrator/ (100.1K)
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
│   │   ├── llm_router/ (8.0K)
│   │   │   ├── ALGORITHM_ContextPack_Truncation_Repair.md (1.1K)
│   │   │   ├── HEALTH_InvalidRate_Latency_Cost.md (551)
│   │   │   ├── IMPLEMENTATION_Prompt_Templates_And_Cache.md (773)
│   │   │   ├── PATTERNS_Strict_JSON_And_Repair.md (1.1K)
│   │   │   ├── SYNC_JSON_Contracts_And_Fallbacks.md (3.5K)
│   │   │   └── VALIDATION_Output_Schema_And_MaxWords.md (1.0K)
│   │   ├── moment_graph/ (9.0K)
│   │   │   ├── ALGORITHM_Create_Merge_Promote_Decay_Myth.md (1.2K)
│   │   │   ├── BEHAVIORS_Callbacks_And_Presence.md (1.1K)
│   │   │   ├── IMPLEMENTATION_Moment_Store_And_Indexing.md (811)
│   │   │   ├── OBJECTIFS_Memory_And_Mythification.md (672)
│   │   │   ├── SYNC_Moment_Lifecycle.md (3.6K)
│   │   │   ├── VALIDATION_Lifecycle_Invariants.md (1.2K)
│   │   │   └── (..1 more files)
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
│   │   ├── BEHAVIORS_System_Experience_And_Rhythm.md (1.7K)
│   │   ├── HEALTH_Global_System_Signals.md (564)
│   │   ├── IMPLEMENTATION_Repo_Structure_And_Entry_Points.md (1.3K)
│   │   ├── OBJECTIFS_Product_And_Feelings.md (761)
│   │   ├── PATTERNS_System_Architecture_And_Boundaries.md (3.9K)
│   │   ├── SYNC_Project_State.md (4.1K)
│   │   └── VALIDATION_Global_Invariants_And_Budgets.md (3.8K)
│   ├── map.md (37.3K)
│   └── (..2 more files)
├── runtime_windows/ (3.5K)
│   ├── audio_player/ (3.5K)
│   │   ├── audio_queue_player.exe_or_py (971)
│   │   └── audio_queue_player.py (2.5K)
│   └── launcher/
│       └── (..2 more files)
├── src/ (48.7K)
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
│   ├── ingest/ (8.0K)
│   │   ├── civ6_jsonl_tail_reader.py (1.4K)
│   │   ├── event_deduplicator_and_coalescer.py (3.0K)
│   │   └── raw_event_parser_and_normalizer.py (3.5K)
│   ├── llm_router/ (5.1K)
│   │   ├── context_pack_builder_and_truncator.py (597)
│   │   ├── simple_llm_client.py (2.9K)
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
│   └── main.py (7.8K)
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
├── AGENTS.md (26.2K)
├── CLAUDE.md (2.1K)
├── events.jsonl (743)
├── map.md (34.7K)
└── map_src.md (7.4K)
```

**Sections:**
- # Narrator Identity
- ## Tools
- ## Instructions

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
- `src/llm_router/context_pack_builder_and_truncator.py`
- `src/llm_router/prompt_template_loader.py`
- `src/llm_router/strict_json_output_validator_and_repair_pass.py`
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
- # Civ6 Living Narrator — Behaviors: System experience and rhythm
- ## CHAIN
- ## BEHAVIORS
- ## OBJECTIVES SERVED
- ## EDGE CASES
- ## ANTI-BEHAVIORS

**Sections:**
- # Civ6 Living Narrator — Health: Global system signals
- ## SIGNALS
- ## ALERTS

**Sections:**
- # Civ6 Living Narrator — Implementation: Repo structure and entry points
- ## CHAIN
- ## CODE STRUCTURE
- ## ENTRY POINTS
- ## NOTES

**Sections:**
- # OBJECTIFS — Civ6 Living Narrator
- ## PRIMARY OBJECTIVES (ranked)
- ## NON-OBJECTIVES
- ## TRADEOFFS (canonical decisions)
- ## SUCCESS SIGNALS (observable)

**Sections:**
- # Civ6 Living Narrator — Patterns: Modular, silence-first narration pipeline
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
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `src/llm_router/simple_llm_client.py`
- `src/main.py`

**Doc refs:**
- `agents/narrator/CLAUDE.md`

**Sections:**
- # Civ6 Living Narrator — Sync: Project State
- ## Navigation
- ## Maturity
- ## Module Health
- ## Recent Decisions
- ## TODO (max 10)
- ## Handoff

**Code refs:**
- `test_budget_and_selection_invariants.py`
- `test_llm_json_fuzz_and_fallback.py`
- `test_moment_lifecycle_rules.py`
- `test_windows_bridge_rotation_and_tail.py`

**Sections:**
- # Civ6 Living Narrator — Validation: Global invariants and budgets
- ## CHAIN
- ## BEHAVIORS GUARANTEED
- ## OBJECTIVES COVERED
- ## INVARIANTS
- ## PROPERTIES
- ## ERROR CONDITIONS
- ## HEALTH COVERAGE
- ## VERIFICATION PROCEDURE
- ## SYNC STATUS
- ## GAPS / IDEAS / QUESTIONS

**Code refs:**
- `doctor_cli_parser_and_run_checker.py`
- `runtime_windows/audio_player/audio_queue_player.py`
- `semantic_proximity_based_character_node_selector.py`
- `snake_case.py`
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

**Definitions:**
- `class AudioItem`
- `class AudioItem`
- `class AudioQueue`
- `def __init__()`
- `def enqueue()`
- `def _process_queue()`
- `def _play_item()`
- `def stop()`

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
- `def parse_json_line()`
- `def _parse_simple_yaml()`
- `def load_event_schema()`
- `def normalize_event()`

**Definitions:**
- `class ContextPack`
- `def truncate_context()`

**Definitions:**
- `class ClaudeCLIClient`
- `def __init__()`
- `def generate_json()`
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

**Imports:**
- `ingest/civ6_jsonl_tail_reader`
- `ingest/raw_event_parser_and_normalizer`
- `ingest/event_deduplicator_and_coalescer`
- `decision_engine/candidate_builder_for_speakers`
- `decision_engine/candidate_ranker_and_selector_with_explainability`
- `decision_engine/narrative_budget_and_cooldown_enforcer`
- `llm_router/simple_llm_client`
- `audio_runtime_windows/elevenlabs_tts`

**Definitions:**
- `def load_tail_state()`
- `def save_tail_state()`
- `def build_mock_candidates()`
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
- `doctor_cli_parser_and_run_checker.py`
- `runtime_windows/audio_player/audio_queue_player.py`
- `semantic_proximity_based_character_node_selector.py`
- `snake_case.py`
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
