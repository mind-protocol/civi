"""Load and validate DM challenge catalog."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


REQUIRED_FIELDS = {"id", "title", "conditions", "refusal_line"}


def _parse_catalog_yaml(path: Path) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    current_list: List[Dict[str, Any]] = []
    current_item: Dict[str, Any] | None = None
    in_challenges = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line == "challenges:":
            in_challenges = True
            data["challenges"] = current_list
            continue
        if in_challenges and line.startswith("-"):
            if current_item:
                current_list.append(current_item)
            current_item = {}
            remainder = line[1:].strip()
            if remainder:
                key, value = [part.strip() for part in remainder.split(":", 1)]
                current_item[key] = value
            continue
        if in_challenges and ":" in line and current_item is not None:
            key, value = [part.strip() for part in line.split(":", 1)]
            current_item[key] = value
            continue

    if current_item:
        current_list.append(current_item)
    return data


def load_challenge_catalog(path: str) -> List[Dict[str, str]]:
    parsed = _parse_catalog_yaml(Path(path))
    challenges = parsed.get("challenges", [])
    return [dict(item) for item in challenges]


def validate_challenge_catalog(challenges: List[Dict[str, str]]) -> List[str]:
    errors: List[str] = []
    for challenge in challenges:
        missing = REQUIRED_FIELDS - set(challenge.keys())
        if missing:
            errors.append(f"missing_fields:{','.join(sorted(missing))}")
    return errors
