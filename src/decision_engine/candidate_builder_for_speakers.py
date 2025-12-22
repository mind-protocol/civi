"""Build candidate narration lines for scoring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass
class Candidate:
    candidate_id: str
    speaker_type: str
    speaker_id: Optional[str]
    text: str
    importance: float
    surprise: float
    moment_relevance: float
    is_pivot: bool = False


def build_candidates(raw_candidates: Iterable[Candidate]) -> List[Candidate]:
    return list(raw_candidates)
