import tempfile
import unittest
from pathlib import Path

from sentinel.scanner import scan_for_secrets


class NestedExclusionTests(unittest.TestCase):

    def test_excludes_nested_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            ignored_dir = root / "project" / "generated"
            ignored_dir.mkdir(parents=True)

            secret_file = ignored_dir / "config.py"
            secret_file.write_text(
                'password = "MyActualPassword123!"',
                encoding="utf-8",
            )

            findings = scan_for_secrets(
                root,
                {"project/generated"},
            )

            self.assertEqual(findings, [])

    def test_excludes_nested_directory_with_backslashes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            ignored_dir = root / "project" / "generated"
            ignored_dir.mkdir(parents=True)

            secret_file = ignored_dir / "config.py"
            secret_file.write_text(
                'password = "MyActualPassword123!"',
                encoding="utf-8",
            )

            findings = scan_for_secrets(
                root,
                {"project\\generated"},
            )

            self.assertEqual(findings, [])

    def test_excluding_nested_directory_does_not_exclude_parent_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            source_dir = root / "project"
            source_dir.mkdir()

            normal_secret = source_dir / "config.py"
            normal_secret.write_text(
                'password = "ParentSecret123!"',
                encoding="utf-8",
            )

            ignored_dir = source_dir / "generated"
            ignored_dir.mkdir()

            ignored_secret = ignored_dir / "config.py"
            ignored_secret.write_text(
                'password = "IgnoredSecret123!"',
                encoding="utf-8",
            )

            findings = scan_for_secrets(
                root,
                {"project/generated"},
            )

            self.assertEqual(len(findings), 1)
            self.assertEqual(
                findings[0].file_path,
                normal_secret,
            )


if __name__ == "__main__":
    unittest.main()