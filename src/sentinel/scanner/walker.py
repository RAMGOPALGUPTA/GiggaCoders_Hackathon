from pathlib import Path


DEFAULT_IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
}


def should_ignore(
    path: Path,
    target: Path,
    excluded_paths: set[str],
) -> bool:
    """
    Return True if a path should be excluded from scanning.
    """
    try:
        relative_path = path.relative_to(target)
    except ValueError:
        return False

    relative_path_string = relative_path.as_posix()

    if path.suffix == ".pyc":
        return True

    for part in relative_path.parts:
        if part in DEFAULT_IGNORED_DIRECTORIES:
            return True

    for excluded_path in excluded_paths:
        normalized_excluded = excluded_path.replace("\\", "/").strip("/")

        if not normalized_excluded:
            continue

        if (
            relative_path_string == normalized_excluded
            or relative_path_string.startswith(
                normalized_excluded + "/"
            )
        ):
            return True

    return False


def walk_files(
    target: Path,
    excluded_paths: set[str] | None = None,
) -> list[Path]:
    """
    Return all regular files under a target file or directory.

    Automatically ignores common generated directories and supports
    explicitly excluded relative paths.
    """
    target = Path(target)

    if not target.exists():
        raise FileNotFoundError(
            f"Target does not exist: {target}"
        )

    if excluded_paths is None:
        excluded_paths = set()

    if target.is_file():
        return [target]

    files: list[Path] = []

    for path in target.rglob("*"):
        try:
            if should_ignore(
                path,
                target,
                excluded_paths,
            ):
                continue

            if path.is_file():
                files.append(path)

        except OSError:
            continue

    return sorted(
        files,
        key=lambda path: path.as_posix(),
    )