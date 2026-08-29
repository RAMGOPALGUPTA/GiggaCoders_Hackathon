import json
from pathlib import Path

from sentinel.models import Finding


def build_json_report(
    findings: list[Finding],
    target: Path,
) -> str:
    """
    Build a JSON security scan report.
    """
    report = {
        "target": target.as_posix(),
        "total_findings": len(findings),
        "findings": [
            finding.to_dict()
            for finding in findings
        ],
    }

    return json.dumps(
        report,
        indent=2,
        sort_keys=True,
    )
