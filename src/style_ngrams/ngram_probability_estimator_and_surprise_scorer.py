"""Estimate transition probabilities and surprise scores."""

from __future__ import annotations

import math
from typing import Dict, Tuple


def estimate_probabilities(
    counts: Dict[str, int], total: int, vocab_size: int, alpha: float = 1.0
) -> Dict[str, float]:
    probabilities: Dict[str, float] = {}
    denom = total + alpha * vocab_size
    for token, count in counts.items():
        probabilities[token] = (count + alpha) / denom
    return probabilities


def predict_next(probabilities: Dict[str, float]) -> Tuple[str, float]:
    if not probabilities:
        return "", 0.0
    token = max(probabilities, key=probabilities.get)
    return token, probabilities[token]


def surprise_for(probability: float) -> float:
    if probability <= 0:
        return 0.0
    return -math.log2(probability)
