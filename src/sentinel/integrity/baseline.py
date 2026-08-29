import json
from pathlib import Path

from sentinel.integrity.hashing import calculate_file_hash
from sentinel.scanner.walker import walk_files


SHA256_HEX_LENGTH = 64


def create_baseline(target: Path) -> dict[str, str]:
    """
    Create a SHA-256 baseline for every regular file
    inside the target.
    """
    target = Path(target)

    if not target.exists():
        raise FileNotFoundError(
            f"Target does not exist: {target}"
        )

    baseline: dict[str, str] = {}

    if target.is_file():
        baseline[target.name] = calculate_file_hash(target)
        return baseline

    for file_path in walk_files(target):
        relative_path = file_path.relative_to(target).as_posix()

        baseline[relative_path] = calculate_file_hash(
            file_path
        )

    return baseline


def save_baseline(
    baseline: dict[str, str],
    path: Path,
) -> None:
    """
    Save a SHA-256 baseline as formatted JSON.
    """
    path = Path(path)

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            baseline,
            file,
            indent=2,
            sort_keys=True,
        )
        file.write("\n")


def load_baseline(path: Path) -> dict[str, str]:
    """
    Load and validate a SHA-256 integrity baseline.
    """
    path = Path(path)

    try:
        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

    except (
        OSError,
        json.JSONDecodeError,
    ) as error:
        raise ValueError(
            f"Invalid baseline file: {path}"
        ) from error

    if not isinstance(data, dict):
        raise ValueError(
            "Invalid baseline: expected a JSON object."
        )

    for file_path, file_hash in data.items():
        if not isinstance(file_path, str):
            raise ValueError(
                "Invalid baseline: file paths must be strings."
            )

        if not file_path.strip():
            raise ValueError(
                "Invalid baseline: file path cannot be empty."
            )

        if not isinstance(file_hash, str):
            raise ValueError(
                "Invalid baseline: hashes must be strings."
            )

        if len(file_hash) != SHA256_HEX_LENGTH:
            raise ValueError(
                "Invalid baseline: SHA-256 hash must contain "
                "64 hexadecimal characters."
            )

        try:
            int(file_hash, 16)
        except ValueError as error:
            raise ValueError(
                "Invalid baseline: hash contains "
                "non-hexadecimal characters."
            ) from error

    return data