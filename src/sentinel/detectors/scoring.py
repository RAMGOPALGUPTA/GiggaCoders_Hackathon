from sentinel.detectors.entropy import is_high_entropy


SECRET_CONTEXT_WORDS = (
    "password",
    "passwd",
    "pwd",
    "token",
    "secret",
    "api_key",
    "apikey",
    "access_key",
    "auth",
    "credential",
)


def has_secret_context(text: str) -> bool:
    """
    Check whether text contains words commonly associated
    with credentials or secrets.
    """
    normalized = text.lower()

    return any(word in normalized for word in SECRET_CONTEXT_WORDS)


def calculate_confidence(
    value: str,
    secret_type: str,
    context: str,
) -> int:
    """
    Calculate a confidence score from 0 to 100 using
    multiple detection signals.
    """

    # Strong known-format patterns start with higher confidence.
    known_pattern_scores = {
        "AWS Access Key": 90,
        "GitHub Personal Access Token": 95,
        "Private Key": 100,
    }

    confidence = known_pattern_scores.get(secret_type, 60)

    # Random-looking values are more suspicious.
    if is_high_entropy(value):
        confidence += 15

    # Secret-related context increases confidence.
    if has_secret_context(context):
        confidence += 15

    # Long credential-like values receive a small boost.
    if len(value) >= 32:
        confidence += 5

    # Never allow confidence above 100.
    return min(confidence, 100)