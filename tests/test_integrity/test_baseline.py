import tempfile
import unittest
from pathlib import Path

from sentinel.integrity.baseline import (
    create_baseline,
    load_baseline,
    save_baseline,
)


class BaselineTests(unittest.TestCase):

    def test_creates_baseline_for_single_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "config.txt"

            file_path.write_text(
                "hello",
                encoding="utf-8",
            )

            baseline = create_baseline(file_path)

            self.assertEqual(
                list(baseline.keys()),
                ["config.txt"],
            )

            self.assertEqual(
                len(baseline["config.txt"]),
                64,
            )

    def test_creates_baseline_for_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            first = root / "first.txt"
            nested = root / "nested"
            nested.mkdir()
            second = nested / "second.txt"

            first.write_text(
                "one",
                encoding="utf-8",
            )

            second.write_text(
                "two",
                encoding="utf-8",
            )

            baseline = create_baseline(root)

            self.assertEqual(
                len(baseline),
                2,
            )

            self.assertIn(
                "first.txt",
                baseline,
            )

            self.assertIn(
                "nested/second.txt",
                baseline,
            )

    def test_baseline_is_saved_and_loaded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            baseline = {
                "config.txt": "a" * 64,
            }

            output_path = root / "baseline.json"

            save_baseline(
                baseline,
                output_path,
            )

            loaded = load_baseline(output_path)

            self.assertEqual(
                loaded,
                baseline,
            )

    def test_invalid_baseline_data_raises_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "baseline.json"

            path.write_text(
                '["invalid", "baseline"]',
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_baseline(path)


if __name__ == "__main__":
    unittest.main()