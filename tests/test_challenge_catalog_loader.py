import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from dm_challenges.challenge_catalog_loader_and_validator import (
    load_challenge_catalog,
    validate_challenge_catalog,
)


def test_load_and_validate_catalog(tmp_path):
    catalog = tmp_path / "catalog.yaml"
    catalog.write_text(
        """
challenges:
  - id: test
    title: Test challenge
    conditions: Do something
    refusal_line: Maybe later.
""",
        encoding="utf-8",
    )
    challenges = load_challenge_catalog(str(catalog))
    assert len(challenges) == 1
    assert validate_challenge_catalog(challenges) == []


def test_validation_missing_refusal_line(tmp_path):
    catalog = tmp_path / "catalog.yaml"
    catalog.write_text(
        """
challenges:
  - id: test
    title: Test challenge
    conditions: Do something
""",
        encoding="utf-8",
    )
    challenges = load_challenge_catalog(str(catalog))
    errors = validate_challenge_catalog(challenges)
    assert "missing_fields:refusal_line" in errors
