from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Finding:
    """
    Represents one potential security finding discovered by Sentinel.
    """

    file_path: Path
    line_number: int
    secret_type: str
    severity: str
    confidence: int
    reason: str
    preview: str

    def __post_init__(self) -> None:
        if self.line_number < 1:
            raise ValueError("line_number must be at least 1")

        if not 0 <= self.confidence <= 100:
            raise ValueError("confidence must be between 0 and 100")

    def to_dict(self) -> dict:
        """
        Return a JSON-serializable representation of the finding.
        """
        data = asdict(self)
        data["file_path"] = self.file_path.as_posix()
        return data