import tempfile
import unittest
from pathlib import Path

from sentinel.scanner.walker import walk_files


class WalkerIgnoreTests(unittest.TestCase):

    def test_ignores_git_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            git_dir = root / ".git"
            git_dir.mkdir()

            ignored_file = git_dir / "config.txt"
            ignored_file.write_text(
                "password = secret",
                encoding="utf-8",
            )

            normal_file = root / "app.py"
            normal_file.write_text(
                "print('hello')",
                encoding="utf-8",
            )

            files = walk_files(root)

            self.assertEqual(
                files,
                [normal_file],
            )

    def test_ignores_pycache_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            cache_dir = root / "__pycache__"
            cache_dir.mkdir()

            cache_file = cache_dir / "app.pyc"
            cache_file.write_bytes(b"binary")

            normal_file = root / "app.py"
            normal_file.write_text(
                "print('hello')",
                encoding="utf-8",
            )

            files = walk_files(root)

            self.assertEqual(
                files,
                [normal_file],
            )

    def test_excludes_explicit_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            tests_dir = root / "tests"
            tests_dir.mkdir()

            test_file = tests_dir / "test.py"
            test_file.write_text(
                "password = secret",
                encoding="utf-8",
            )

            app_file = root / "app.py"
            app_file.write_text(
                "print('hello')",
                encoding="utf-8",
            )

            files = walk_files(
                root,
                {"tests"},
            )

            self.assertEqual(
                files,
                [app_file],
            )

    def test_returns_files_in_deterministic_order(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            third = root / "z.txt"
            first = root / "a.txt"
            second = root / "m.txt"

            third.write_text("z", encoding="utf-8")
            first.write_text("a", encoding="utf-8")
            second.write_text("m", encoding="utf-8")

            files = walk_files(root)

            self.assertEqual(
                files,
                [first, second, third],
            )


if __name__ == "__main__":
    unittest.main()