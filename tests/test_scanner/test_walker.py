import tempfile
import unittest
from pathlib import Path

from sentinel.scanner.walker import walk_files


class WalkFilesTests(unittest.TestCase):
    def test_single_file_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sample.txt"
            path.write_text("hello", encoding="utf-8")
            self.assertEqual(walk_files(path), [path])

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertEqual(walk_files(Path(temp_dir)), [])

    def test_nested_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "a" / "b").mkdir(parents=True)
            first = root / "a" / "one.txt"
            second = root / "a" / "b" / "two.txt"
            first.write_text("one", encoding="utf-8")
            second.write_text("two", encoding="utf-8")
            self.assertEqual(set(walk_files(root)), {first, second})

    def test_multiple_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            files = [root / "one.txt", root / "two.txt", root / "three.txt"]
            for file in files:
                file.write_text(file.name, encoding="utf-8")
            self.assertEqual(set(walk_files(root)), set(files))

    def test_missing_path_raises(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(FileNotFoundError):
                walk_files(Path(temp_dir) / "missing")
