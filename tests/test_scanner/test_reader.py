import tempfile
import unittest
from pathlib import Path

from sentinel.scanner.reader import read_text_file


class ReadTextFileTests(unittest.TestCase):
    def test_utf8_text_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sample.txt"
            path.write_text("hello", encoding="utf-8")
            self.assertEqual(read_text_file(path), "hello")

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "empty.txt"
            path.write_text("", encoding="utf-8")
            self.assertEqual(read_text_file(path), "")

    def test_unicode_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "unicode.txt"
            content = "नमस्ते Sentinel 🚀"
            path.write_text(content, encoding="utf-8")
            self.assertEqual(read_text_file(path), content)

    def test_binary_file_returns_none(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "binary.bin"
            path.write_bytes(b"\x00\x01\x02binary")
            self.assertIsNone(read_text_file(path))

    def test_missing_file_returns_none(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertIsNone(read_text_file(Path(temp_dir) / "missing.txt"))
