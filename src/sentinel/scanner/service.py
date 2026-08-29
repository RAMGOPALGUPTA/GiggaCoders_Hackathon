from pathlib import Path

from sentinel.detectors import detect_secrets
from sentinel.models import Finding
from sentinel.scanner.reader import read_text_file
from sentinel.scanner.walker import walk_files


def scan_for_secrets(
    target: Path,
    excluded_paths: set[str] | None = None,
) -> list[Finding]:
    """
    Scan a file or directory for potential secrets.

    Files are discovered recursively, safely read as UTF-8 text,
    and passed to the secret detection engine.
    """
    findings: list[Finding] = []

    files = walk_files(
        target,
        excluded_paths,
    )

    for file_path in files:
        text = read_text_file(file_path)

        if text is None:
            continue

        file_findings = detect_secrets(
            text,
            file_path,
        )

        findings.extend(file_findings)

    return sorted(
        findings,
        key=lambda finding: (
            str(finding.file_path).replace("\\", "/"),
            finding.line_number,
            finding.secret_type,
        ),
    )