import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from ingest.civ6_jsonl_tail_reader import TailState, read_new_lines
from win_wsl_bridge.bridge_path_resolver import resolve_bridge_paths
from win_wsl_bridge.session_file_rotator import rotate_if_needed, SessionState


def test_tail_handles_partial_line(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text('{"a": 1}\n{"b": 2', encoding="utf-8")

    state = TailState()
    lines, state = read_new_lines(str(path), state)
    assert lines == ['{"a": 1}']
    assert state.buffer == '{"b": 2'

    with path.open("a", encoding="utf-8") as handle:
        handle.write('}\n')

    lines, state = read_new_lines(str(path), state)
    assert lines == ['{"b": 2}']
    assert state.buffer == ""


def test_tail_resets_on_rotation(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text('{"a": 1}\n{"c": 3}\n', encoding="utf-8")

    state = TailState()
    lines, state = read_new_lines(str(path), state)
    assert lines == ['{"a": 1}', '{"c": 3}']

    path.write_text('{"b": 2}\n', encoding="utf-8")
    lines, state = read_new_lines(str(path), state)
    assert lines == ['{"b": 2}']


def test_session_rotation_resets_tail_state(monkeypatch):
    paths = resolve_bridge_paths("C:\\Bridge", "/mnt/c/Bridge")
    state = SessionState(session_id="one", tail_state=TailState(offset=10, buffer="x"))

    monkeypatch.setenv("CIV6_LIVING_NARRATOR_SESSION_ID", "two")
    rotated = rotate_if_needed(state, paths)
    assert rotated.session_id == "two"
    assert rotated.tail_state.offset == 0
    assert rotated.tail_state.buffer == ""
