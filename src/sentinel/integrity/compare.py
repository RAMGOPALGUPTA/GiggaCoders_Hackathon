from dataclasses import dataclass
from pathlib import Path

from sentinel.integrity.baseline import create_baseline


@dataclass(frozen=True)
class IntegrityResult:
    """
    Represents the result of comparing one file
    against a previously created integrity baseline.
    """

    file_path: str
    status: str


def compare_baseline(
    target: Path,
    baseline: dict[str, str],
) -> list[IntegrityResult]:
    """
    Compare the current state of a target against
    a previously created SHA-256 baseline.

    Possible statuses are:
    - NEW
    - MODIFIED
    - DELETED
    """
    current = create_baseline(target)

    results: list[IntegrityResult] = []

    baseline_paths = set(baseline)
    current_paths = set(current)

    new_paths = current_paths - baseline_paths
    deleted_paths = baseline_paths - current_paths

    common_paths = baseline_paths & current_paths

    for file_path in sorted(new_paths):
        results.append(
            IntegrityResult(
                file_path=file_path,
                status="NEW",
            )
        )

    for file_path in sorted(common_paths):
        if baseline[file_path] != current[file_path]:
            results.append(
                IntegrityResult(
                    file_path=file_path,
                    status="MODIFIED",
                )
            )

    for file_path in sorted(deleted_paths):
        results.append(
            IntegrityResult(
                file_path=file_path,
                status="DELETED",
            )
        )

    return results