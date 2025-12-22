import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from decision_engine.candidate_builder_for_speakers import Candidate
from decision_engine.candidate_ranker_and_selector_with_explainability import (
    SelectionConfig,
    select_candidate,
)
from decision_engine.narrative_budget_and_cooldown_enforcer import BudgetState


def _candidate(speaker_type="NARRATOR", is_pivot=False):
    return Candidate(
        candidate_id="c1",
        speaker_type=speaker_type,
        speaker_id=None,
        text="line",
        importance=1.0,
        surprise=0.5,
        moment_relevance=0.0,
        is_pivot=is_pivot,
    )


def test_budget_enforced():
    state = BudgetState()
    config = SelectionConfig(max_speech_budget=1, budget_window=3, min_delta_value=0.1)

    result = select_candidate([_candidate()], turn=1, state=state, config=config)
    assert result.selected is not None

    result = select_candidate([_candidate()], turn=2, state=state, config=config)
    assert result.selected is None
    assert "budget" in result.suppression_reasons


def test_cooldown_enforced():
    state = BudgetState()
    config = SelectionConfig(cooldown_turns=2, min_delta_value=0.1)

    result = select_candidate([_candidate()], turn=1, state=state, config=config)
    assert result.selected is not None

    result = select_candidate([_candidate()], turn=2, state=state, config=config)
    assert result.selected is None
    assert "cooldown" in result.suppression_reasons


def test_diversity_blocks_leader_repeat():
    state = BudgetState()
    config = SelectionConfig(min_delta_value=0.1, diversity_block=True, cooldown_turns=0)

    result = select_candidate(
        [_candidate(speaker_type="LEADER")],
        turn=1,
        state=state,
        config=config,
        last_speaker_type=None,
    )
    assert result.selected is not None

    result = select_candidate(
        [_candidate(speaker_type="LEADER")],
        turn=2,
        state=state,
        config=config,
        last_speaker_type="LEADER",
    )
    assert result.selected is None
    assert "diversity" in result.suppression_reasons


def test_diversity_allows_pivot_leader():
    state = BudgetState()
    config = SelectionConfig(min_delta_value=0.1, diversity_block=True)

    result = select_candidate(
        [_candidate(speaker_type="LEADER", is_pivot=True)],
        turn=1,
        state=state,
        config=config,
        last_speaker_type="LEADER",
    )
    assert result.selected is not None


def test_silence_gate_low_value():
    state = BudgetState()
    config = SelectionConfig(min_delta_value=5.0)

    result = select_candidate([_candidate()], turn=1, state=state, config=config)
    assert result.selected is None
    assert "low_value" in result.suppression_reasons
