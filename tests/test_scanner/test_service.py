import tempfile
import unittest
from pathlib import Path

from sentinel.scanner import scan_for_secrets


class ScannerServiceTests(unittest.TestCase):

    def test_scans_single_file_for_secret(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "config.py"

            file_path.write_text(
                'password = "MyActualPassword123!"',
                encoding="utf-8",
            )

            findings = scan_for_secrets(file_path)

            self.assertEqual(len(findings), 1)
            self.assertEqual(
                findings[0].secret_type,
                "Password Assignment",
            )
            self.assertEqual(findings[0].file_path, file_path)

    def test_scans_directory_recursively(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            nested = root / "nested"
            nested.mkdir()

            clean_file = root / "clean.txt"
            secret_file = nested / "config.py"

            clean_file.write_text(
                "This is normal text.",
                encoding="utf-8",
            )

            secret_file.write_text(
                'api_key = "MyRealApiKey123456!"',
                encoding="utf-8",
            )

            findings = scan_for_secrets(root)

            self.assertEqual(len(findings), 1)
            self.assertEqual(
                findings[0].secret_type,
                "API Key Assignment",
            )
            self.assertEqual(findings[0].file_path, secret_file)

    def test_skips_binary_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            binary_file = root / "data.bin"
            binary_file.write_bytes(
                b"\x00\x01password=secret123"
            )

            findings = scan_for_secrets(root)

            self.assertEqual(findings, [])

    def test_ignores_clean_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "notes.txt"
            file_path.write_text(
                "Nothing sensitive is stored here.",
                encoding="utf-8",
            )

            findings = scan_for_secrets(root)

            self.assertEqual(findings, [])

    def test_detects_multiple_secrets_across_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            first_file = root / "config.py"
            second_file = root / ".env"

            first_file.write_text(
                'password = "MyActualPassword123!"',
                encoding="utf-8",
            )

            token = "ghp_" + "A" * 36
            second_file.write_text(
                f"GITHUB_TOKEN={token}",
                encoding="utf-8",
            )

            findings = scan_for_secrets(root)

            self.assertEqual(len(findings), 2)

            secret_types = {
                finding.secret_type
                for finding in findings
            }

            self.assertIn(
                "Password Assignment",
                secret_types,
            )

            self.assertIn(
                "GitHub Personal Access Token",
                secret_types,
            )


if __name__ == "__main__":
    unittest.main()