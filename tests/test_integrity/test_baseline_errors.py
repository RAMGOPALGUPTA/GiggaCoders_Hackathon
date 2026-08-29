import json
import tempfile
import unittest
from pathlib import Path

from sentinel.integrity import load_baseline


class BaselineErrorTests(unittest.TestCase):

    def test_invalid_json_baseline_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            baseline_path = Path(temp_dir) / "baseline.json"

            baseline_path.write_text(
                "{ this is not valid json",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_baseline(baseline_path)

    def test_json_list_baseline_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            baseline_path = Path(temp_dir) / "baseline.json"

            baseline_path.write_text(
                json.dumps(
                    ["file1.txt", "file2.txt"]
                ),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_baseline(baseline_path)

    def test_baseline_with_non_string_hash_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            baseline_path = Path(temp_dir) / "baseline.json"

            baseline_path.write_text(
                json.dumps(
                    {
                        "config.txt": 12345,
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_baseline(baseline_path)

    def test_baseline_with_empty_file_path_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            baseline_path = Path(temp_dir) / "baseline.json"

            baseline_path.write_text(
                json.dumps(
                    {
                        "": (
                            "a" * 64
                        ),
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_baseline(baseline_path)

    def test_baseline_with_invalid_hash_length_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            baseline_path = Path(temp_dir) / "baseline.json"

            baseline_path.write_text(
                json.dumps(
                    {
                        "config.txt": "abc123",
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_baseline(baseline_path)


if __name__ == "__main__":
    unittest.main()