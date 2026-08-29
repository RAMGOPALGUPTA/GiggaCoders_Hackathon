from pathlib import Path

from sentinel.detectors.filtering import is_placeholder
from sentinel.detectors.patterns import SECRET_PATTERNS
from sentinel.detectors.scoring import calculate_confidence
from sentinel.models import Finding


def mask_secret(value: str) -> str:
    """
    Mask a secret so the complete value is not exposed in reports.
    """
    if len(value) <= 4:
        return "*" * len(value)

    visible_start = min(4, len(value))
    visible_end = min(4, len(value) - visible_start)

    return (
        value[:visible_start]
        + "*" * (len(value) - visible_start - visible_end)
        + value[-visible_end:]
    )


def detect_secrets(text: str, file_path: Path) -> list[Finding]:
    """
    Detect known secret patterns in text and return security findings.
    """
    findings: list[Finding] = []

    for secret_type, config in SECRET_PATTERNS.items():
        pattern = config["pattern"]

        for match in pattern.finditer(text):
            line_number = text.count("\n", 0, match.start()) + 1

            matched_value = match.group(0)

            if match.lastindex:
                captured_value = match.group(match.lastindex)
                if captured_value:
                    matched_value = captured_value

            if secret_type in {
                "Password Assignment",
                "API Key Assignment",
            }:
                if is_placeholder(matched_value):
                    continue

            finding = Finding(
                file_path=file_path,
                line_number=line_number,
                secret_type=secret_type,
                severity=config["severity"],
                confidence=calculate_confidence(
                    value=matched_value,
                    secret_type=secret_type,
                    context=match.group(0),
                ),
                reason=config["reason"],
                preview=mask_secret(matched_value),
            )

            findings.append(finding)

    return findings