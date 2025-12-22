import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from moment_graph.moment_creator_and_merger import Moment, create_or_merge_moment
from moment_graph.moment_lifecycle_promoter_and_decayer import promote_and_decay
from moment_graph.moment_query_and_callback_selector import select_callback


def test_moment_promotion():
    moment = Moment(
        moment_id="m1",
        tags={"war"},
        charge=5.0,
        turn_created=1,
        last_turn=1,
    )
    moments = promote_and_decay([moment], current_turn=1, promote_threshold=4.0, decay_per_turn=0.0, decay_floor=0.0)
    assert moments[0].is_myth is True


def test_moment_decay_removes():
    moment = Moment(
        moment_id="m1",
        tags={"war"},
        charge=0.5,
        turn_created=1,
        last_turn=1,
    )
    moments = promote_and_decay([moment], current_turn=3, promote_threshold=4.0, decay_per_turn=0.3, decay_floor=0.0)
    assert moments == []


def test_create_or_merge_moment_merges_by_overlap():
    moments = []
    create_or_merge_moment(moments, tags=["war", "siege"], importance=1.0, turn=1, merge_window=3, overlap_threshold=0.5)
    create_or_merge_moment(moments, tags=["war"], importance=1.0, turn=2, merge_window=3, overlap_threshold=0.5)
    assert len(moments) == 1


def test_callback_selection_requires_myth():
    moment = Moment(
        moment_id="m1",
        tags={"war"},
        charge=5.0,
        turn_created=1,
        last_turn=1,
        is_myth=False,
    )
    assert select_callback([moment], current_turn=10, tags=["war"]) is None


def test_callback_selection_allows_overlap_or_time_gate():
    moment = Moment(
        moment_id="m1",
        tags={"war"},
        charge=5.0,
        turn_created=1,
        last_turn=1,
        is_myth=True,
        last_callback_turn=None,
    )
    selected = select_callback([moment], current_turn=10, tags=["war"], overlap_threshold=0.5, time_gate=15)
    assert selected is not None
    assert selected.moment_id == "m1"
