"""Parse raw JSON lines and normalize into a stable schema."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


EventNormalized = Dict[str, Any]

DEFAULT_SCHEMA = {
    "required_fields": ["event_type", "turn"],
    "optional_fields": ["timestamp", "session_id", "payload", "type", "Turn", "time"],
    "field_aliases": {"type": "event_type", "Turn": "turn", "time": "timestamp"},
    "reject_unknown": False,
}


def parse_json_line(line: str) -> Dict[str, Any]:
    return json.loads(line)


def _parse_simple_yaml(path: Path) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    current_key: Optional[str] = None
    current_type: Optional[str] = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith(":") and not line.startswith("-"):
            current_key = line[:-1].strip()
            data[current_key] = None
            current_type = None
            continue
        if line.startswith("-") and current_key:
            if current_type is None:
                data[current_key] = []
                current_type = "list"
            if isinstance(data[current_key], list):
                data[current_key].append(line[1:].strip())
            continue
        if ":" in line and current_key:
            key, value = [part.strip() for part in line.split(":", 1)]
            if current_type is None:
                data[current_key] = {}
                current_type = "dict"
            if isinstance(data[current_key], dict):
                data[current_key][key] = value
            continue
        if ":" in line and current_key is None:
            key, value = [part.strip() for part in line.split(":", 1)]
            data[key] = value
            continue
    return data


def load_event_schema(path: Optional[str] = None) -> Dict[str, Any]:
    if not path:
        return DEFAULT_SCHEMA.copy()
    schema_path = Path(path)
    if not schema_path.exists():
        return DEFAULT_SCHEMA.copy()
    parsed = _parse_simple_yaml(schema_path)
    schema = DEFAULT_SCHEMA.copy()
    schema.update(parsed)
    if isinstance(schema.get("reject_unknown"), str):
        schema["reject_unknown"] = schema["reject_unknown"].lower() == "true"
    return schema


def normalize_event(raw: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> Optional[EventNormalized]:
    schema = schema or DEFAULT_SCHEMA
    aliases = schema.get("field_aliases", {})
    required = set(schema.get("required_fields", []))
    optional = set(schema.get("optional_fields", []))
    allowed = required | optional | set(aliases.keys())

    normalized: Dict[str, Any] = {}
    for key, value in raw.items():
        canonical = aliases.get(key, key)
        normalized[canonical] = value

    event_type = normalized.get("event_type")
    turn = normalized.get("turn")
    timestamp = normalized.get("timestamp")

    if event_type is None or turn is None:
        return None

    unknown_fields = [key for key in raw.keys() if key not in allowed]
    payload = dict(raw)
    if unknown_fields:
        payload["_unknown_fields"] = unknown_fields
        if schema.get("reject_unknown"):
            return None

    return {
        "event_type": event_type,
        "turn": turn,
        "timestamp": timestamp,
        "payload": payload,
        "session_id": normalized.get("session_id"),
    }
