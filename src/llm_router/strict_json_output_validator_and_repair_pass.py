"""Validate LLM JSON output and optionally run a repair pass."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple


@dataclass
class ValidationResult:
    valid: bool
    data: Optional[Dict[str, Any]]
    error: Optional[str]
    repaired: bool = False


def _validate_schema(data: Dict[str, Any]) -> bool:
    return isinstance(data.get("text"), str) and isinstance(data.get("speaker"), str)


def validate_json_output(raw: str) -> ValidationResult:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        return ValidationResult(valid=False, data=None, error=str(exc))
    if not isinstance(parsed, dict):
        return ValidationResult(valid=False, data=None, error="not an object")
    if not _validate_schema(parsed):
        return ValidationResult(valid=False, data=None, error="schema_mismatch")
    return ValidationResult(valid=True, data=parsed, error=None)


def repair_json_output(
    raw: str,
    repair_fn: Callable[[str], str],
) -> Tuple[ValidationResult, Optional[str]]:
    result = validate_json_output(raw)
    if result.valid:
        return result, None
    repaired_raw = repair_fn(raw)
    repaired_result = validate_json_output(repaired_raw)
    if repaired_result.valid:
        repaired_result.repaired = True
        return repaired_result, repaired_raw
    return repaired_result, repaired_raw
