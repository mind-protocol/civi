import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from style_ngrams.event_tokenizer_and_feature_extractor import tokenize_event
from style_ngrams.ngram_transition_counter_store import (
    NgramCounterStore,
    global_scope,
    leader_scope,
    phase_scope,
)
from style_ngrams.ngram_scope_backoff_predictor import predict_with_backoff


def test_token_compression_maps_unknown():
    event = {"event_type": "NEW_EVENT"}
    token = tokenize_event(event, token_map={"NEW_EVENT": "NEW_EVENT"}, known_tokens={"KNOWN"}).token
    assert token == "::ANY"


def test_backoff_prediction_source():
    store = NgramCounterStore()
    prev = "A"
    store.update(global_scope(), prev, "B")
    prediction = predict_with_backoff(
        store,
        prev_token=prev,
        vocab_size=3,
        min_count=1,
        leader_id="leader1",
        phase="ANCIENT",
    )
    assert prediction.source == "GLOBAL"
    assert prediction.token == "B"


def test_leader_scope_wins_when_available():
    store = NgramCounterStore()
    prev = "A"
    store.update(leader_scope("leader1"), prev, "L")
    store.update(global_scope(), prev, "G")
    prediction = predict_with_backoff(
        store,
        prev_token=prev,
        vocab_size=3,
        min_count=1,
        leader_id="leader1",
    )
    assert prediction.source == "BY_LEADER"
    assert prediction.token == "L"


def test_phase_scope_fallback():
    store = NgramCounterStore()
    prev = "A"
    store.update(phase_scope("ANCIENT"), prev, "P")
    prediction = predict_with_backoff(
        store,
        prev_token=prev,
        vocab_size=3,
        min_count=1,
        phase="ANCIENT",
    )
    assert prediction.source == "BY_PHASE"
    assert prediction.token == "P"
