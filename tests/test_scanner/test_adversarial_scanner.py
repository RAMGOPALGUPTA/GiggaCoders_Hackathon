import tempfile
import unittest
from pathlib import Path

from sentinel.scanner import scan_for_secrets


class AdversarialScannerTests(unittest.TestCase):

    def test_empty_file_produces_no_findings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "empty.py"
            file_path.write_text(
                "",
                encoding="utf-8",
            )

            findings = scan_for_secrets(root)

            self.assertEqual(
                findings,
                [],
            )

    def test_placeholder_password_is_not_detected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "config.py"
            file_path.write_text(
                'password = "YOUR_PASSWORD_HERE"\n',
                encoding="utf-8",
            )

            findings = scan_for_secrets(root)

            self.assertEqual(
                findings,
                [],
            )

    def test_multiple_secrets_in_same_file_are_detected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "config.py"
            file_path.write_text(
                'password = "MyActualPassword123!"\n'
                'api_key = "abcdefghijklmnopqrstuvwxyz123456"\n',
                encoding="utf-8",
            )

            findings = scan_for_secrets(root)

            self.assertGreaterEqual(
                len(findings),
                2,
            )

            secret_types = {
                finding.secret_type
                for finding in findings
            }

            self.assertIn(
                "Password Assignment",
                secret_types,
            )

            self.assertIn(
                "API Key Assignment",
                secret_types,
            )

    def test_secret_on_first_line_reports_line_one(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "config.py"
            file_path.write_text(
                'password = "MyActualPassword123!"\n'
                "safe = True\n",
                encoding="utf-8",
            )

            findings = scan_for_secrets(root)

            password_findings = [
                finding
                for finding in findings
                if finding.secret_type
                == "Password Assignment"
            ]

            self.assertEqual(
                len(password_findings),
                1,
            )

            self.assertEqual(
                password_findings[0].line_number,
                1,
            )

    def test_secret_on_last_line_reports_correct_line(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "config.py"
            file_path.write_text(
                "safe = True\n"
                "debug = False\n"
                'password = "MyActualPassword123!"',
                encoding="utf-8",
            )

            findings = scan_for_secrets(root)

            password_findings = [
                finding
                for finding in findings
                if finding.secret_type
                == "Password Assignment"
            ]

            self.assertEqual(
                len(password_findings),
                1,
            )

            self.assertEqual(
                password_findings[0].line_number,
                3,
            )

    def test_placeholder_api_key_is_not_detected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "config.py"
            file_path.write_text(
                'api_key = "YOUR_API_KEY_HERE"\n',
                encoding="utf-8",
            )

            findings = scan_for_secrets(root)

            api_key_findings = [
                finding
                for finding in findings
                if finding.secret_type
                == "API Key Assignment"
            ]

            self.assertEqual(
                api_key_findings,
                [],
            )

    def test_normal_text_does_not_produce_findings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_path = root / "notes.txt"
            file_path.write_text(
                "This file contains ordinary text.\n"
                "There are no credentials here.\n"
                "Everything is safe.\n",
                encoding="utf-8",
            )

            findings = scan_for_secrets(root)

            self.assertEqual(
                findings,
                [],
            )


if __name__ == "__main__":
    unittest.main()
    