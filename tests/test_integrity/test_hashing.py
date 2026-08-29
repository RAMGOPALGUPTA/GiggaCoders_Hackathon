import tempfile
import unittest
from pathlib import Path

from sentinel.integrity.hashing import calculate_file_hash


class HashingTests(unittest.TestCase):

    def test_same_content_has_same_hash(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            first = root / "first.txt"
            second = root / "second.txt"

            first.write_text("hello", encoding="utf-8")
            second.write_text("hello", encoding="utf-8")

            self.assertEqual(
                calculate_file_hash(first),
                calculate_file_hash(second),
            )

    def test_different_content_has_different_hash(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            first = root / "first.txt"
            second = root / "second.txt"

            first.write_text("hello", encoding="utf-8")
            second.write_text("world", encoding="utf-8")

            self.assertNotEqual(
                calculate_file_hash(first),
                calculate_file_hash(second),
            )

    def test_hash_is_sha256_length(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "file.txt"

            file_path.write_text(
                "Sentinel",
                encoding="utf-8",
            )

            result = calculate_file_hash(file_path)

            self.assertEqual(len(result), 64)

    def test_hash_is_deterministic(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "file.txt"

            file_path.write_text(
                "same content",
                encoding="utf-8",
            )

            first_hash = calculate_file_hash(file_path)
            second_hash = calculate_file_hash(file_path)

            self.assertEqual(
                first_hash,
                second_hash,
            )


if __name__ == "__main__":
    unittest.main()