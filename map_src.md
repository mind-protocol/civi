# Repository Map: civi/src

*Generated: 2025-12-22 18:47*

## Statistics

- **Files:** 26
- **Directories:** 11
- **Total Size:** 47.2K
- **Doc Files:** 0
- **Code Files:** 26
- **Areas:** 1 (docs/ subfolders)
- **Modules:** 10 (subfolders in areas)
- **DOCS Links:** 0 (0.0 avg per code file)

### By Language

- python: 26

## File Tree

```
├── audio_runtime_windows/ (2.0K)
│   └── elevenlabs_tts.py (2.0K)
├── decision_engine/ (4.5K)
│   ├── candidate_ranker_and_selector_with_explainability.py (3.0K)
│   ├── narrative_budget_and_cooldown_enforcer.py (1.0K)
│   └── (..1 more files)
├── dm_challenges/ (3.7K)
│   ├── challenge_catalog_loader_and_validator.py (1.9K)
│   ├── challenge_offer_generator.py (910)
│   └── challenge_state_tracker_and_evaluator.py (955)
├── ingest/ (8.0K)
│   ├── civ6_jsonl_tail_reader.py (1.4K)
│   ├── event_deduplicator_and_coalescer.py (3.0K)
│   └── raw_event_parser_and_normalizer.py (3.5K)
├── llm_router/ (5.1K)
│   ├── context_pack_builder_and_truncator.py (597)
│   ├── simple_llm_client.py (2.9K)
│   ├── strict_json_output_validator_and_repair_pass.py (1.5K)
│   └── (..1 more files)
├── moment_graph/ (3.6K)
│   ├── moment_creator_and_merger.py (1.6K)
│   ├── moment_lifecycle_promoter_and_decayer.py (720)
│   └── moment_query_and_callback_selector.py (1.3K)
├── persistence/ (4.7K)
│   ├── sqlite_store_schema_and_migrator.py (1.8K)
│   └── store_adapters_for_counts_moments_challenges.py (2.9K)
├── style_ngrams/ (5.0K)
│   ├── event_tokenizer_and_feature_extractor.py (1.0K)
│   ├── ngram_probability_estimator_and_surprise_scorer.py (814)
│   ├── ngram_scope_backoff_predictor.py (1.9K)
│   └── ngram_transition_counter_store.py (1.3K)
├── telemetry/ (2.1K)
│   ├── health_snapshot_builder.py (959)
│   ├── overlay_payload_emitter.py (861)
│   └── (..1 more files)
├── win_wsl_bridge/ (2.2K)
│   ├── bridge_path_resolver.py (692)
│   ├── session_file_rotator.py (998)
│   └── (..1 more files)
└── main.py (7.8K)
```

## File Details

### `audio_runtime_windows/elevenlabs_tts.py`

**Definitions:**
- `class ElevenLabsTTS`
- `def __init__()`
- `def generate_audio()`

### `decision_engine/candidate_ranker_and_selector_with_explainability.py`

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

### `decision_engine/narrative_budget_and_cooldown_enforcer.py`

**Definitions:**
- `class BudgetState`
- `def is_budget_exceeded()`
- `def is_cooldown_active()`
- `def record_spoken()`

### `dm_challenges/challenge_catalog_loader_and_validator.py`

**Definitions:**
- `def _parse_catalog_yaml()`
- `def load_challenge_catalog()`
- `def validate_challenge_catalog()`

### `dm_challenges/challenge_offer_generator.py`

**Definitions:**
- `class ChallengeOffer`
- `def choose_challenge()`

### `dm_challenges/challenge_state_tracker_and_evaluator.py`

**Definitions:**
- `class ChallengeState`
- `def activate_challenge()`
- `def mark_completed()`
- `def mark_refused()`
- `def can_offer()`

### `ingest/civ6_jsonl_tail_reader.py`

**Definitions:**
- `class TailState`
- `def _split_lines()`
- `def read_new_lines()`

### `ingest/event_deduplicator_and_coalescer.py`

**Definitions:**
- `class EventDeduplicator`
- `def __init__()`
- `def _signature()`
- `def is_duplicate()`
- `def remember()`
- `def _rules_from_types()`
- `def coalesce_events()`

### `ingest/raw_event_parser_and_normalizer.py`

**Definitions:**
- `def parse_json_line()`
- `def _parse_simple_yaml()`
- `def load_event_schema()`
- `def normalize_event()`

### `llm_router/context_pack_builder_and_truncator.py`

**Definitions:**
- `class ContextPack`
- `def truncate_context()`

### `llm_router/simple_llm_client.py`

**Definitions:**
- `class ClaudeCLIClient`
- `def __init__()`
- `def generate_json()`
- `def _call_claude()`

### `llm_router/strict_json_output_validator_and_repair_pass.py`

**Definitions:**
- `class ValidationResult`
- `def _validate_schema()`
- `def validate_json_output()`
- `def repair_json_output()`

### `moment_graph/moment_creator_and_merger.py`

**Definitions:**
- `class Moment`
- `def _tag_overlap()`
- `def create_or_merge_moment()`

### `moment_graph/moment_lifecycle_promoter_and_decayer.py`

**Imports:**
- `moment_graph/moment_creator_and_merger`

**Definitions:**
- `def promote_and_decay()`

### `moment_graph/moment_query_and_callback_selector.py`

**Imports:**
- `moment_graph/moment_creator_and_merger`

**Definitions:**
- `def _tag_overlap()`
- `def select_callback()`

### `persistence/sqlite_store_schema_and_migrator.py`

**Definitions:**
- `class Migration`
- `def apply_migrations()`

### `persistence/store_adapters_for_counts_moments_challenges.py`

**Definitions:**
- `def upsert_count()`
- `def load_counts()`
- `def upsert_moment()`
- `def load_moments()`
- `def upsert_challenge()`
- `def load_challenges()`
- `def prune_session()`

### `style_ngrams/event_tokenizer_and_feature_extractor.py`

**Definitions:**
- `class TokenizationResult`
- `def _compress_token()`
- `def tokenize_event()`

### `style_ngrams/ngram_probability_estimator_and_surprise_scorer.py`

**Definitions:**
- `def estimate_probabilities()`
- `def predict_next()`
- `def surprise_for()`

### `style_ngrams/ngram_scope_backoff_predictor.py`

**Imports:**
- `style_ngrams/ngram_probability_estimator_and_surprise_scorer`
- `style_ngrams/ngram_transition_counter_store`

**Definitions:**
- `class Prediction`
- `def _predict_for_scope()`
- `def predict_with_backoff()`

### `style_ngrams/ngram_transition_counter_store.py`

**Definitions:**
- `class NgramCounterStore`
- `def __init__()`
- `def update()`
- `def counts_for()`
- `def total_for()`
- `def leader_scope()`
- `def phase_scope()`
- `def global_scope()`

### `telemetry/health_snapshot_builder.py`

**Definitions:**
- `class HealthSnapshot`
- `def build_health_snapshot()`

### `telemetry/overlay_payload_emitter.py`

**Definitions:**
- `class OverlayPayload`
- `def build_overlay_payload()`

### `win_wsl_bridge/bridge_path_resolver.py`

**Definitions:**
- `class BridgePaths`
- `def windows_session_file()`
- `def wsl_session_file()`
- `def resolve_bridge_paths()`

### `win_wsl_bridge/session_file_rotator.py`

**Imports:**
- `ingest/civ6_jsonl_tail_reader`
- `win_wsl_bridge/bridge_path_resolver`
- `win_wsl_bridge/launcher_contracts_and_ports`

**Definitions:**
- `class SessionState`
- `def resolve_session_file()`
- `def rotate_if_needed()`

### `main.py`

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
