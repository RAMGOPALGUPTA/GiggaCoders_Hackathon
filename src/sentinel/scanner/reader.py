from pathlib import Path


def read_text_file(path: Path) -> str | None:
    """Return UTF-8 text, or None for binary/unreadable files."""
    path = Path(path)

    try:
        data = path.read_bytes()
    except OSError:
        return None

    if b"\x00" in data:
        return None

    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None
