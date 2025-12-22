"""Backoff prediction across leader, phase, and global scopes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from style_ngrams.ngram_probability_estimator_and_surprise_scorer import (
    estimate_probabilities,
    predict_next,
    surprise_for,
)
from style_ngrams.ngram_transition_counter_store import (
    NgramCounterStore,
    global_scope,
    leader_scope,
    phase_scope,
)


@dataclass(frozen=True)
class Prediction:
    token: Optional[str]
    probability: float
    surprise: float
    source: str


def _predict_for_scope(
    store: NgramCounterStore,
    scope_key: str,
    prev_token: str,
    vocab_size: int,
    alpha: float,
) -> Tuple[Optional[str], float, float]:
    total = store.total_for(scope_key, prev_token)
    counts = store.counts_for(scope_key, prev_token)
    probabilities = estimate_probabilities(counts, total, vocab_size, alpha=alpha)
    token, prob = predict_next(probabilities)
    return (token if token else None, prob, surprise_for(prob))


def predict_with_backoff(
    store: NgramCounterStore,
    prev_token: str,
    vocab_size: int,
    min_count: int,
    leader_id: Optional[str] = None,
    phase: Optional[str] = None,
    alpha: float = 1.0,
) -> Prediction:
    scopes = []
    if leader_id:
        scopes.append((leader_scope(leader_id), "BY_LEADER"))
    if phase:
        scopes.append((phase_scope(phase), "BY_PHASE"))
    scopes.append((global_scope(), "GLOBAL"))

    for scope_key, label in scopes:
        if store.total_for(scope_key, prev_token) < min_count:
            continue
        token, prob, surprise = _predict_for_scope(
            store, scope_key, prev_token, vocab_size, alpha
        )
        if token:
            return Prediction(token=token, probability=prob, surprise=surprise, source=label)

    return Prediction(token=None, probability=0.0, surprise=0.0, source="NONE")
