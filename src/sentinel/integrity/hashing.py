import hashlib
from pathlib import Path


def calculate_file_hash(path: Path) -> str:
    """
    Calculate the SHA-256 hash of a file.

    The file is read in chunks so large files do not need to be
    loaded completely into memory.
    """
    path = Path(path)

    hasher = hashlib.sha256()

    with path.open("rb") as file:
        while chunk := file.read(65536):
            hasher.update(chunk)

    return hasher.hexdigest()