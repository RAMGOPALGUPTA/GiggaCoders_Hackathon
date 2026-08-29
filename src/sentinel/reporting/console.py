from collections import Counter
from pathlib import Path

from sentinel.models import Finding


def build_console_report(
    findings: list[Finding],
    target: Path,
) -> str:
    """
    Build a human-readable security scan report.
    """
    lines: list[str] = []

    lines.append("SENTINEL SECURITY SCAN")
    lines.append("=" * 50)
    lines.append(f"Target: {target}")
    lines.append("")

    if not findings:
        lines.append("No potential secrets found.")
        lines.append("")
        lines.append("Total findings: 0")
        return "\n".join(lines)

    severity_counts = Counter(
        finding.severity
        for finding in findings
    )

    severity_order = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }

    sorted_findings = sorted(
        findings,
        key=lambda finding: (
            severity_order.get(finding.severity, 99),
            -finding.confidence,
            str(finding.file_path),
            finding.line_number,
        ),
    )

    for finding in sorted_findings:
        lines.append(
            f"{finding.severity:<9} "
            f"{finding.file_path.as_posix()}:{finding.line_number}"
        )
        lines.append(f"  Type:       {finding.secret_type}")
        lines.append(f"  Confidence: {finding.confidence}%")
        lines.append(f"  Reason:     {finding.reason}")
        lines.append(f"  Preview:    {finding.preview}")
        lines.append("")

    lines.append("-" * 50)
    lines.append(f"Total findings: {len(findings)}")

    for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        count = severity_counts.get(severity, 0)
        lines.append(f"{severity}: {count}")

    return "\n".join(lines)
