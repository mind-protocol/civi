# SYNC: Project Health

```
LAST_UPDATED: 2025-12-22
UPDATED_BY: ngram doctor
STATUS: CRITICAL
```

---

## CURRENT STATE

**Health Score:** 0/100

The project has critical issues that will significantly impact agent effectiveness. Address these before starting new work.

| Severity | Count |
|----------|-------|
| Critical | 16 |
| Warning | 95 |
| Info | 110 |

---

## ISSUES

### UNDOCUMENTED (14 files)

**What's wrong:** Code without documentation becomes a black box. Agents will reverse-engineer intent from implementation, make changes that violate invisible design decisions, or duplicate existing patterns.

**How to fix:** Add a mapping in modules.yaml (project root), then create at minimum PATTERNS + SYNC docs for the module.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `src/ingest` - No documentation mapping (3 files)
  - Add mapping to modules.yaml
- `src/win_wsl_bridge` - No documentation mapping (3 files)
  - Add mapping to modules.yaml
- `src/decision_engine` - No documentation mapping (3 files)
  - Add mapping to modules.yaml
- `src/style_ngrams` - No documentation mapping (4 files)
  - Add mapping to modules.yaml
- `tests` - No documentation mapping (12 files)
  - Add mapping to modules.yaml
- `src/dm_challenges` - No documentation mapping (3 files)
  - Add mapping to modules.yaml
- `src/telemetry` - No documentation mapping (3 files)
  - Add mapping to modules.yaml
- `src` - No documentation mapping (30 files)
  - Add mapping to modules.yaml
- `scripts` - No documentation mapping (1 files)
  - Add mapping to modules.yaml
- `runtime_windows/audio_player` - No documentation mapping (2 files)
  - Add mapping to modules.yaml
- ... and 4 more

### BROKEN_IMPL_LINK (2 files)

**What's wrong:** IMPLEMENTATION docs reference files that don't exist. Agents following these docs will waste time looking for non-existent code.

**How to fix:** Update file paths in the IMPLEMENTATION doc to match actual locations, or remove references to deleted files.

**Protocol:** Load `VIEW_Document_Create_Module_Documentation.md` before starting.

**Files:**

- `docs/civ6_living_narrator/lua_mod/IMPLEMENTATION_Mod_Files_And_Hooks.md` - References 11 non-existent file(s)
  - Update or remove references: Documents/Civ6LivingNarrator/events/events.jsonl, Events.ResearchCompleted, Events.TurnBegin
- `docs/civ6_living_narrator/IMPLEMENTATION_Repo_Structure_And_Entry_Points.md` - References 17 non-existent file(s)
  - Update or remove references: LivingNarrator.modinfo, config.json, state/config.json

### DOC_TEMPLATE_DRIFT (60 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/civ6_living_narrator/moment_graph/IMPLEMENTATION_Moment_Store_And_Indexing.md` - Missing: CHAIN, CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, ENTRY POINTS, DATA FLOW AND DOCKING (FLOW-BY-FLOW), LOGIC CHAINS, MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, CONFIGURATION, BIDIRECTIONAL LINKS, EXTRACTION CANDIDATES, MARKERS
- `docs/civ6_living_narrator/persistence/IMPLEMENTATION_Sqlite_Schema_And_Adapters.md` - Missing: CHAIN, CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, ENTRY POINTS, DATA FLOW AND DOCKING (FLOW-BY-FLOW), LOGIC CHAINS, MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, CONFIGURATION, BIDIRECTIONAL LINKS, EXTRACTION CANDIDATES, MARKERS
- `docs/civ6_living_narrator/dm_challenges/HEALTH_Completion_Rates_And_Frustration_Signals.md` - Missing: PURPOSE OF THIS FILE, WHY THIS PATTERN, HOW TO USE THIS TEMPLATE, CHAIN, FLOWS ANALYSIS (TRIGGERS + FREQUENCY), HEALTH INDICATORS SELECTED, OBJECTIVES COVERAGE, STATUS (RESULT INDICATOR), DOCK TYPES (COMPLETE LIST), CHECKER INDEX, INDICATOR: {Indicator Name}, HOW TO RUN, KNOWN GAPS, MARKERS
- `docs/civ6_living_narrator/telemetry/IMPLEMENTATION_Health_Snapshot_And_Emitter.md` - Missing: CHAIN, CODE STRUCTURE, DESIGN PATTERNS, SCHEMA, ENTRY POINTS, DATA FLOW AND DOCKING (FLOW-BY-FLOW), LOGIC CHAINS, MODULE DEPENDENCIES, STATE MANAGEMENT, RUNTIME BEHAVIOR, CONCURRENCY MODEL, CONFIGURATION, BIDIRECTIONAL LINKS, EXTRACTION CANDIDATES, MARKERS
- `docs/civ6_living_narrator/moment_graph/BEHAVIORS_Callbacks_And_Presence.md` - Missing: OBJECTIVES SERVED, INPUTS / OUTPUTS, EDGE CASES, MARKERS
- `docs/civ6_living_narrator/lua_mod/ALGORITHM_Hook_Serialize_Append.md` - Missing: OBJECTIVES AND BEHAVIORS, DATA STRUCTURES, ALGORITHM: {Primary Function Name}, KEY DECISIONS, DATA FLOW, HELPER FUNCTIONS, INTERACTIONS
- `docs/civ6_living_narrator/llm_router/HEALTH_InvalidRate_Latency_Cost.md` - Missing: PURPOSE OF THIS FILE, WHY THIS PATTERN, HOW TO USE THIS TEMPLATE, CHAIN, FLOWS ANALYSIS (TRIGGERS + FREQUENCY), HEALTH INDICATORS SELECTED, OBJECTIVES COVERAGE, STATUS (RESULT INDICATOR), DOCK TYPES (COMPLETE LIST), CHECKER INDEX, INDICATOR: {Indicator Name}, HOW TO RUN, KNOWN GAPS, MARKERS
- `docs/civ6_living_narrator/persistence/VALIDATION_Schema_Integrity_And_Retention.md` - Missing: BEHAVIORS GUARANTEED, OBJECTIVES COVERED, PROPERTIES, ERROR CONDITIONS, HEALTH COVERAGE, SYNC STATUS, MARKERS; Too short: VERIFICATION PROCEDURE
- `docs/civ6_living_narrator/dm_challenges/VALIDATION_OneActive_And_Clarity.md` - Missing: BEHAVIORS GUARANTEED, OBJECTIVES COVERED, PROPERTIES, ERROR CONDITIONS, HEALTH COVERAGE, SYNC STATUS, MARKERS
- `docs/civ6_living_narrator/lua_mod/VALIDATION_Event_Schema_And_File_Integrity.md` - Missing: BEHAVIORS GUARANTEED, OBJECTIVES COVERED, PROPERTIES, ERROR CONDITIONS, HEALTH COVERAGE, VERIFICATION PROCEDURE, SYNC STATUS
- ... and 50 more

### LEGACY_MARKER (14 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/civ6_living_narrator/win_wsl_bridge/PATTERNS_WindowsFirst_Runtime.md` - Legacy todo format (use @ngram:todo)
- `docs/civ6_living_narrator/persistence/SYNC_Persistence_Stores_And_Migrations.md` - Legacy todo format (use @ngram:todo)
- `docs/civ6_living_narrator/audio_runtime_windows/SYNC_Win11_Audio_Player.md` - Legacy todo format (use @ngram:todo)
- `docs/civ6_living_narrator/lua_mod/SYNC_Lua_Mod_Status.md` - Legacy IDEA format (use @ngram:proposition)
- `docs/civ6_living_narrator/dm_challenges/SYNC_Challenge_Contract_System.md` - Legacy todo format (use @ngram:todo)
- `docs/civ6_living_narrator/decision_engine/SYNC_Rhythm_And_Selection.md` - Legacy todo format (use @ngram:todo)
- `docs/civ6_living_narrator/win_wsl_bridge/PATTERNS_WindowsFirst_Runtime.md` - Legacy GAPS section header
- `docs/civ6_living_narrator/ingest/SYNC_Ingest_And_Normalization.md` - Legacy todo format (use @ngram:todo)
- `docs/civ6_living_narrator/win_wsl_bridge/SYNC_Bridge_Files_Ports_Launcher.md` - Legacy todo format (use @ngram:todo)
- `docs/civ6_living_narrator/lua_mod/SYNC_Lua_Mod_Status.md` - Legacy todo format (use @ngram:todo)
- ... and 4 more

### HARDCODED_CONFIG (2 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `scripts/speak.py` - Contains hardcoded configuration values
- `src/audio_runtime_windows/elevenlabs_tts.py` - Contains hardcoded configuration values

### ESCALATION (13 files)

**What's wrong:** Documentation or code contradicts itself. Agents found conflicts they couldn't resolve - either docs say different things, or docs don't match implementation. This causes confusion and inconsistent behavior.

**How to fix:** Review the CONFLICTS section, make a design decision for each ESCALATION item, update all conflicting sources to be consistent, then convert ESCALATION to DECISION (resolved).

**Protocol:** Load `VIEW_Specify_Design_Vision_And_Architecture.md` before starting.

**Files:**

- `.claude/skills/SKILL_Update_Module_Sync_State_And_Record_Markers.md` - Escalation marker needs decision (priority: 5)
- `.claude/skills/SKILL_Debug_Investigate_And_Fix_Issues_With_Evidence_First.md` - Escalation marker needs decision (priority: 5)
- `.claude/skills/SKILL_Extend_Add_Features_To_Existing_Systems_With_Canon_Constraints.md` - Escalation marker needs decision (priority: 5)
- `.claude/skills/SKILL_Orchestrate_Feature_Integration_Pipeline_Orchestrator_And_Progress_Router.md` - Escalation marker needs decision (priority: 5)
- `docs/civ6_living_narrator/lua_mod/IMPLEMENTATION_Mod_Files_And_Hooks.md` - Escalation marker needs decision (priority: 5)
- `.claude/skills/SKILL_Implement_Write_Or_Modify_Code_With_Doc_Chain_Coupling.md` - Escalation marker needs decision (priority: 5)
- `AGENTS.md` - Escalation marker needs decision (priority: 5)
- `.claude/skills/SKILL_Create_Module_Documentation_Chain_From_Templates_And_Seed_Todos.md` - Escalation marker needs decision (priority: 5)
- `.claude/skills/SKILL_Review_Evaluate_Changes_And_Produce_Auditable_Report.md` - Escalation marker needs decision (priority: 5)
- `.claude/skills/SKILL_Ingest_Raw_Data_Sources_And_Route_To_Modules.md` - Escalation marker needs decision (priority: 5)
- ... and 3 more

### NON_STANDARD_DOC_TYPE (2 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/civ6_living_narrator/MECHANISMS_Narrator_Core_Systems.md` - Doc filename does not use a standard prefix
- `docs/SPEC.md` - Doc filename does not use a standard prefix

### NAMING_CONVENTION (3 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `src/llm_router/context_pack_builder_and_truncator.py` - Code file 'context_pack_builder_and_truncator.py' contains 'and', suggesting it should be split
- `tests/test_dm_challenge_offers_and_state.py` - Code file 'test_dm_challenge_offers_and_state.py' contains 'and', suggesting it should be split
- `docs/SPEC.md` - Naming convention violations task (1): 10 items

### STALE_IMPL (1 files)

**What's wrong:** This issue may cause problems.

**How to fix:** Review and fix.

**Protocol:** Load `VIEW_Implement_Write_Or_Modify_Code.md` before starting.

**Files:**

- `docs/civ6_living_narrator/IMPLEMENTATION_Repo_Structure_And_Entry_Points.md` - 1 referenced files not found

---

## LATER

These are minor issues that don't block work but would improve project health:

- [ ] `tests/test_parse_and_normalize_events.py` - No DOCS: reference in file header
- [ ] `tests/test_llm_client_and_tts.py` - No DOCS: reference in file header
- [ ] `docs/civ6_living_narrator/dm_challenges/SYNC_Challenge_Contract_System.md` - 42% similar to `docs/civ6_living_narrator/win_wsl_bridge/SYNC_Bridge_Files_Ports_Launcher.md`
- [ ] `.claude/skills/SKILL_Create_Module_Documentation_Chain_From_Templates_And_Seed_Todos.md` - Agent proposition needs review (priority: 5)
- [ ] `docs/civ6_living_narrator/SYNC_Project_State.md` - Doc not linked from code or modules.yaml
- [ ] `docs/civ6_living_narrator/decision_engine/SYNC_Rhythm_And_Selection.md` - 47% similar to `docs/civ6_living_narrator/moment_graph/SYNC_Moment_Lifecycle.md`
- [ ] `docs/civ6_living_narrator/dm_challenges/SYNC_Challenge_Contract_System.md` - 44% similar to `docs/civ6_living_narrator/llm_router/SYNC_JSON_Contracts_And_Fallbacks.md`
- [ ] `docs/civ6_living_narrator/dm_challenges/SYNC_Challenge_Contract_System.md` - 43% similar to `docs/civ6_living_narrator/style_ngrams/SYNC_Style_Ngram_Graph.md`
- [ ] `.claude/skills/SKILL_Extend_Add_Features_To_Existing_Systems_With_Canon_Constraints.md` - Agent proposition needs review (priority: 5)
- [ ] `docs/SPEC.md` - Doc not linked from code or modules.yaml
- ... and 100 more

---

## HANDOFF

**For the next agent:**

Before starting your task, consider addressing critical issues - especially if your work touches affected files. Monoliths and undocumented code will slow you down.

**Recommended first action:** Pick one MONOLITH file you'll be working in and split its largest function into a separate module.

---

*Generated by `ngram doctor`*