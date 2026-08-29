import argparse
import sys
from pathlib import Path

from sentinel.integrity import (
    compare_baseline,
    create_baseline,
    load_baseline,
    save_baseline,
)
from sentinel.reporting import (
    build_console_report,
    build_json_report,
)
from sentinel.scanner import scan_for_secrets


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the Sentinel command-line interface.
    """
    parser = argparse.ArgumentParser(
        prog="sentinel",
        description=(
            "Sentinel is a zero-dependency security scanner "
            "and file integrity monitoring tool."
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
    )

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan a file or directory for potential secrets.",
    )

    scan_parser.add_argument(
        "target",
        help="File or directory to scan.",
    )

    scan_parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output the scan report as JSON.",
    )

    scan_parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help=(
            "Exclude a relative file or directory path. "
            "Can be used multiple times."
        ),
    )

    baseline_parser = subparsers.add_parser(
        "baseline",
        help="Create a SHA-256 integrity baseline.",
    )

    baseline_parser.add_argument(
        "target",
        help="File or directory to create a baseline for.",
    )

    baseline_parser.add_argument(
        "--output",
        default="sentinel-baseline.json",
        help="Path where the baseline JSON file will be saved.",
    )

    integrity_parser = subparsers.add_parser(
        "integrity",
        help="Compare a target against an integrity baseline.",
    )

    integrity_parser.add_argument(
        "target",
        help="File or directory to check.",
    )

    integrity_parser.add_argument(
        "baseline",
        help="Path to the previously created baseline JSON file.",
    )

    return parser


def run_scan(
    target: Path,
    json_output: bool,
    excluded_paths: list[str] | None = None,
) -> int:
    """
    Run a secret scan and print the requested report format.
    """
    excluded = set(excluded_paths or [])

    findings = scan_for_secrets(
        target,
        excluded,
    )

    if json_output:
        report = build_json_report(
            findings,
            target,
        )
    else:
        report = build_console_report(
            findings,
            target,
        )

    print(report)
    return 0


def run_baseline(target: Path, output: Path) -> int:
    """
    Create and save a SHA-256 integrity baseline.
    """
    baseline = create_baseline(target)
    save_baseline(baseline, output)

    print("SENTINEL INTEGRITY BASELINE")
    print("=" * 50)
    print(f"Target: {target}")
    print(f"Files hashed: {len(baseline)}")
    print(f"Baseline saved: {output}")

    return 0


def run_integrity(target: Path, baseline_path: Path) -> int:
    """
    Compare the current target against a saved integrity baseline.
    """
    baseline = load_baseline(baseline_path)

    results = compare_baseline(
        target,
        baseline,
    )

    print("SENTINEL FILE INTEGRITY CHECK")
    print("=" * 50)
    print(f"Target: {target}")
    print(f"Baseline: {baseline_path}")
    print("")

    if not results:
        print("No integrity changes detected.")
        return 0

    for result in results:
        print(
            f"{result.status:<10} {result.file_path}"
        )

    print("")
    print(f"Total changes: {len(results)}")

    return 1


def main() -> int:
    """
    Run the Sentinel command-line interface.
    """
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 2

    target = Path(args.target)

    if not target.exists():
        print(
            f"Error: target does not exist: {target}",
            file=sys.stderr,
        )
        return 2

    try:
        if args.command == "scan":
            return run_scan(
                target,
                args.json_output,
                args.exclude,
            )

        if args.command == "baseline":
            return run_baseline(
                target,
                Path(args.output),
            )

        if args.command == "integrity":
            baseline_path = Path(args.baseline)

            if not baseline_path.is_file():
                print(
                    "Error: baseline file does not exist: "
                    f"{baseline_path}",
                    file=sys.stderr,
                )
                return 2

            return run_integrity(
                target,
                baseline_path,
            )

        parser.print_help()
        return 2

    except OSError as error:
        print(
            f"Error while processing target: {error}",
            file=sys.stderr,
        )
        return 1

    except ValueError as error:
        print(
            f"Error: invalid baseline: {error}",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())