import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sentinel.__main__ import main


class CliErrorHandlingTests(unittest.TestCase):

    @patch("sys.argv", ["sentinel", "integrity", "missing-target", "missing.json"])
    def test_integrity_missing_target_returns_two(self):
        result = main()

        self.assertEqual(
            result,
            2,
        )

    def test_integrity_missing_baseline_returns_two(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir)

            with patch(
                "sys.argv",
                [
                    "sentinel",
                    "integrity",
                    str(target),
                    "missing-baseline.json",
                ],
            ):
                result = main()

            self.assertEqual(
                result,
                2,
            )

    def test_integrity_with_invalid_baseline_returns_two(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            target = root / "project"
            target.mkdir()

            baseline = root / "invalid-baseline.json"
            baseline.write_text(
                "{ this is invalid json",
                encoding="utf-8",
            )

            with patch(
                "sys.argv",
                [
                    "sentinel",
                    "integrity",
                    str(target),
                    str(baseline),
                ],
            ):
                result = main()

            self.assertEqual(
                result,
                2,
            )

    def test_scan_empty_directory_returns_zero(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir)

            with patch(
                "sys.argv",
                [
                    "sentinel",
                    "scan",
                    str(target),
                ],
            ):
                result = main()

            self.assertEqual(
                result,
                0,
            )

    def test_baseline_for_single_file_returns_zero(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            target = root / "config.txt"
            target.write_text(
                "safe content",
                encoding="utf-8",
            )

            output = root / "baseline.json"

            with patch(
                "sys.argv",
                [
                    "sentinel",
                    "baseline",
                    str(target),
                    "--output",
                    str(output),
                ],
            ):
                result = main()

            self.assertEqual(
                result,
                0,
            )

            self.assertTrue(
                output.exists(),
            )


if __name__ == "__main__":
    unittest.main()