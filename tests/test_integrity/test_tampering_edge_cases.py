import tempfile
import unittest
from pathlib import Path

from sentinel.integrity import (
    compare_baseline,
    create_baseline,
)


class IntegrityTamperingEdgeCaseTests(unittest.TestCase):

    def test_detects_new_file_added_after_baseline(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            original_file = root / "config.txt"
            original_file.write_text(
                "original",
                encoding="utf-8",
            )

            baseline = create_baseline(root)

            new_file = root / "new_secret.txt"
            new_file.write_text(
                "new content",
                encoding="utf-8",
            )

            results = compare_baseline(
                root,
                baseline,
            )

            self.assertEqual(
                len(results),
                1,
            )

            self.assertEqual(
                results[0].status,
                "NEW",
            )

            self.assertEqual(
                results[0].file_path,
                "new_secret.txt",
            )

    def test_detects_file_deleted_after_baseline(self):
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

            self.assertEqual(
                len(results),
                1,
            )

            self.assertEqual(
                results[0].status,
                "DELETED",
            )

            self.assertEqual(
                results[0].file_path,
                "config.txt",
            )

    def test_detects_multiple_integrity_changes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            modified_file = root / "modified.txt"
            deleted_file = root / "deleted.txt"

            modified_file.write_text(
                "original",
                encoding="utf-8",
            )

            deleted_file.write_text(
                "original",
                encoding="utf-8",
            )

            baseline = create_baseline(root)

            modified_file.write_text(
                "changed",
                encoding="utf-8",
            )

            deleted_file.unlink()

            added_file = root / "added.txt"
            added_file.write_text(
                "new file",
                encoding="utf-8",
            )

            results = compare_baseline(
                root,
                baseline,
            )

            statuses = {
                result.file_path: result.status
                for result in results
            }

            self.assertEqual(
                statuses["modified.txt"],
                "MODIFIED",
            )

            self.assertEqual(
                statuses["deleted.txt"],
                "DELETED",
            )

            self.assertEqual(
                statuses["added.txt"],
                "NEW",
            )

            self.assertEqual(
                len(results),
                3,
            )

    def test_detects_nested_file_modification(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            nested_dir = root / "config" / "production"
            nested_dir.mkdir(
                parents=True,
            )

            file_path = nested_dir / "settings.txt"

            file_path.write_text(
                "safe=true",
                encoding="utf-8",
            )

            baseline = create_baseline(root)

            file_path.write_text(
                "safe=false",
                encoding="utf-8",
            )

            results = compare_baseline(
                root,
                baseline,
            )

            self.assertEqual(
                len(results),
                1,
            )

            self.assertEqual(
                results[0].status,
                "MODIFIED",
            )

            self.assertEqual(
                results[0].file_path,
                "config/production/settings.txt",
            )


if __name__ == "__main__":
    unittest.main()