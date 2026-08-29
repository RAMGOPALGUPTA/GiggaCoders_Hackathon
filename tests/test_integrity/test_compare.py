import tempfile
import unittest
from pathlib import Path

from sentinel.integrity import (
    compare_baseline,
    create_baseline,
)


class CompareBaselineTests(unittest.TestCase):

    def test_unchanged_files_produce_no_results(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "config.txt"
            file_path.write_text(
                "original content",
                encoding="utf-8",
            )

            baseline = create_baseline(root)

            results = compare_baseline(
                root,
                baseline,
            )

            self.assertEqual(results, [])

    def test_detects_new_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            original = root / "original.txt"
            original.write_text(
                "original",
                encoding="utf-8",
            )

            baseline = create_baseline(root)

            new_file = root / "new.txt"
            new_file.write_text(
                "new content",
                encoding="utf-8",
            )

            results = compare_baseline(
                root,
                baseline,
            )

            self.assertEqual(len(results), 1)
            self.assertEqual(
                results[0].file_path,
                "new.txt",
            )
            self.assertEqual(
                results[0].status,
                "NEW",
            )

    def test_detects_modified_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "config.txt"
            file_path.write_text(
                "original",
                encoding="utf-8",
            )

            baseline = create_baseline(root)

            file_path.write_text(
                "modified",
                encoding="utf-8",
            )

            results = compare_baseline(
                root,
                baseline,
            )

            self.assertEqual(len(results), 1)
            self.assertEqual(
                results[0].file_path,
                "config.txt",
            )
            self.assertEqual(
                results[0].status,
                "MODIFIED",
            )

    def test_detects_deleted_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "config.txt"
            file_path.write_text(
                "original",
                encoding="utf-8",
            )

            baseline = create_baseline(root)

            file_path.unlink()

            results = compare_baseline(
                root,
                baseline,
            )

            self.assertEqual(len(results), 1)
            self.assertEqual(
                results[0].file_path,
                "config.txt",
            )
            self.assertEqual(
                results[0].status,
                "DELETED",
            )

    def test_detects_multiple_integrity_changes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            modified = root / "modified.txt"
            deleted = root / "deleted.txt"
            unchanged = root / "unchanged.txt"

            modified.write_text(
                "before",
                encoding="utf-8",
            )
            deleted.write_text(
                "before",
                encoding="utf-8",
            )
            unchanged.write_text(
                "same",
                encoding="utf-8",
            )

            baseline = create_baseline(root)

            modified.write_text(
                "after",
                encoding="utf-8",
            )

            deleted.unlink()

            new_file = root / "new.txt"
            new_file.write_text(
                "new",
                encoding="utf-8",
            )

            results = compare_baseline(
                root,
                baseline,
            )

            changes = {
                (result.file_path, result.status)
                for result in results
            }

            expected = {
                ("modified.txt", "MODIFIED"),
                ("deleted.txt", "DELETED"),
                ("new.txt", "NEW"),
            }

            self.assertEqual(
                changes,
                expected,
            )


if __name__ == "__main__":
    unittest.main()