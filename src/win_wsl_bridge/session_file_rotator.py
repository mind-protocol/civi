"""Track session id changes and rotate tail state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ingest.civ6_jsonl_tail_reader import TailState
from win_wsl_bridge.bridge_path_resolver import BridgePaths
from win_wsl_bridge.launcher_contracts_and_ports import read_session_id


@dataclass(frozen=True)
class SessionState:
    session_id: Optional[str] = None
    tail_state: TailState = TailState()


def resolve_session_file(paths: BridgePaths, session_id: str, prefer_wsl: bool) -> str:
    if prefer_wsl:
        return paths.wsl_session_file(session_id)
    return paths.windows_session_file(session_id)


def rotate_if_needed(
    state: SessionState,
    paths: BridgePaths,
    prefer_wsl: bool = False,
) -> SessionState:
    current_session_id = read_session_id(state.session_id)
    if current_session_id != state.session_id:
        return SessionState(session_id=current_session_id, tail_state=TailState())
    return state
