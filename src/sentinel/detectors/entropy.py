import math
from collections import Counter


def calculate_entropy(value: str) -> float:
    """
    Calculate the Shannon entropy of a string.

    Higher entropy generally indicates that a value is more random.
    """
    if not value:
        return 0.0

    length = len(value)
    counts = Counter(value)

    entropy = 0.0

    for count in counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy


def is_high_entropy(
    value: str,
    threshold: float = 3.5,
    minimum_length: int = 20,
) -> bool:
    """
    Return True if a value is long enough and has high Shannon entropy.
    """
    if len(value) < minimum_length:
        return False

    return calculate_entropy(value) >= threshold