import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from llm_router.strict_json_output_validator_and_repair_pass import (
    repair_json_output,
    validate_json_output,
)


def test_validate_json_output():
    raw = '{"text": "Hello", "speaker": "NARRATOR"}'
    result = validate_json_output(raw)
    assert result.valid is True
    assert result.data["text"] == "Hello"


def test_repair_pass_success():
    raw = '{"text": "Hello" "speaker": "NARRATOR"}'

    def repair_fn(_: str) -> str:
        return '{"text": "Hello", "speaker": "NARRATOR"}'

    result, repaired = repair_json_output(raw, repair_fn)
    assert result.valid is True
    assert result.repaired is True
    assert repaired is not None


def test_repair_pass_fails():
    raw = "not json"

    def repair_fn(_: str) -> str:
        return "still bad"

    result, repaired = repair_json_output(raw, repair_fn)
    assert result.valid is False
    assert repaired == "still bad"
