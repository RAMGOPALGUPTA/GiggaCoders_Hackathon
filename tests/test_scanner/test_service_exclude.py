import tempfile
import unittest
from pathlib import Path

from sentinel.scanner import scan_for_secrets


class ScannerExclusionTests(unittest.TestCase):

    def test_excluded_directory_is_not_scanned(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            tests_dir = root / "tests"
            tests_dir.mkdir()

            secret_file = tests_dir / "secret.py"
            secret_file.write_text(
                'password = "MyActualPassword123!"',
                encoding="utf-8",
            )

            findings = scan_for_secrets(
                root,
                {"tests"},
            )

            self.assertEqual(
                findings,
                [],
            )

    def test_non_excluded_directory_is_scanned(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            source_dir = root / "src"
            source_dir.mkdir()

            secret_file = source_dir / "config.py"
            secret_file.write_text(
                'password = "MyActualPassword123!"',
                encoding="utf-8",
            )

            findings = scan_for_secrets(root)

            self.assertEqual(
                len(findings),
                1,
            )


if __name__ == "__main__":
    unittest.main()