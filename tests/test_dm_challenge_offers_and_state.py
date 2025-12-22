import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from dm_challenges.challenge_offer_generator import choose_challenge
from dm_challenges.challenge_state_tracker_and_evaluator import (
    ChallengeState,
    activate_challenge,
    can_offer,
    mark_completed,
    mark_refused,
)


def test_choose_challenge_skips_used():
    catalog = [
        {"id": "c1", "title": "T", "conditions": "C", "refusal_line": "R"},
        {"id": "c2", "title": "T2", "conditions": "C2", "refusal_line": "R2"},
    ]
    offer = choose_challenge(catalog, used_ids=["c1"])
    assert offer is not None
    assert offer.challenge_id == "c2"


def test_choose_challenge_requires_refusal():
    catalog = [{"id": "c1", "title": "T", "conditions": "C"}]
    assert choose_challenge(catalog) is None


def test_challenge_state_transitions():
    state = ChallengeState()
    assert can_offer(state) is True

    state = activate_challenge(state, "c1", turn=1)
    assert state.active_id == "c1"
    assert can_offer(state) is False

    state = mark_refused(state, turn=2)
    assert can_offer(state) is True

    state = activate_challenge(state, "c2", turn=3)
    state = mark_completed(state, turn=4)
    assert state.status == "completed"
    assert can_offer(state) is True
