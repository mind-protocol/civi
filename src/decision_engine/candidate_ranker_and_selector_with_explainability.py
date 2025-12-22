"""Score candidates, apply gates, and select narration with explainability."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from decision_engine.candidate_builder_for_speakers import Candidate
from decision_engine.narrative_budget_and_cooldown_enforcer import (
    BudgetState,
    is_budget_exceeded,
    is_cooldown_active,
    record_spoken,
)


@dataclass
class SelectionConfig:
    max_speech_budget: int = 2
    budget_window: int = 10
    cooldown_turns: int = 2
    min_delta_value: float = 1.0
    diversity_block: bool = True


@dataclass
class ScoredCandidate:
    candidate: Candidate
    score: float
    penalties: List[str]


@dataclass
class SelectionResult:
    selected: Optional[Candidate]
    suppression_reasons: List[str]
    top_candidates: List[ScoredCandidate]


def _speaker_key(candidate: Candidate) -> str:
    if candidate.speaker_id:
        return f"{candidate.speaker_type}:{candidate.speaker_id}"
    return candidate.speaker_type


def _base_score(candidate: Candidate) -> float:
    return candidate.importance + candidate.surprise + candidate.moment_relevance


def select_candidate(
    candidates: List[Candidate],
    turn: int,
    state: BudgetState,
    config: SelectionConfig,
    last_speaker_type: Optional[str] = None,
) -> SelectionResult:
    suppression: List[str] = []

    if is_budget_exceeded(turn, state, config.max_speech_budget, config.budget_window):
        suppression.append("budget")
        return SelectionResult(selected=None, suppression_reasons=suppression, top_candidates=[])

    scored: List[ScoredCandidate] = []
    filtered_reasons: List[str] = []
    for candidate in candidates:
        penalties: List[str] = []
        speaker_key = _speaker_key(candidate)

        if is_cooldown_active(turn, state, speaker_key, config.cooldown_turns):
            filtered_reasons.append("cooldown")
            continue

        if (
            config.diversity_block
            and candidate.speaker_type == "LEADER"
            and last_speaker_type == "LEADER"
            and not candidate.is_pivot
        ):
            filtered_reasons.append("diversity")
            continue

        score = _base_score(candidate)
        scored.append(ScoredCandidate(candidate=candidate, score=score, penalties=penalties))

    if not scored:
        suppression.extend(sorted(set(filtered_reasons)) or ["no_candidates"])
        return SelectionResult(selected=None, suppression_reasons=suppression, top_candidates=[])

    scored.sort(key=lambda item: item.score, reverse=True)
    top = scored[0]
    if top.score < config.min_delta_value:
        suppression.append("low_value")
        return SelectionResult(selected=None, suppression_reasons=suppression, top_candidates=scored[:5])

    record_spoken(turn, state, _speaker_key(top.candidate))
    return SelectionResult(
        selected=top.candidate,
        suppression_reasons=suppression,
        top_candidates=scored[:5],
    )
