"""Tail an append-only JSONL file with partial-line tolerance."""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Iterable, List, Tuple


@dataclass(frozen=True)
class TailState:
    offset: int = 0
    buffer: str = ""
    mtime_ns: int = 0


def _split_lines(data: str) -> Tuple[List[str], str]:
    lines = data.split("\n")
    if data.endswith("\n"):
        complete = lines[:-1]
        buffer = ""
    else:
        complete = lines[:-1]
        buffer = lines[-1]
    complete = [line[:-1] if line.endswith("\r") else line for line in complete]
    complete = [line for line in complete if line]
    return complete, buffer


def read_new_lines(path: str, state: TailState) -> Tuple[List[str], TailState]:
    if not os.path.exists(path):
        return [], state

    stat = os.stat(path)
    size = stat.st_size
    if size < state.offset:
        state = TailState()
    elif state.mtime_ns and stat.st_mtime_ns != state.mtime_ns and size <= state.offset:
        state = TailState()

    if size == state.offset:
        return [], state

    with open(path, "r", encoding="utf-8") as handle:
        handle.seek(state.offset)
        chunk = handle.read()

    if not chunk:
        return [], state

    data = state.buffer + chunk
    lines, buffer = _split_lines(data)
    new_state = TailState(offset=size, buffer=buffer, mtime_ns=stat.st_mtime_ns)
    return lines, new_state
