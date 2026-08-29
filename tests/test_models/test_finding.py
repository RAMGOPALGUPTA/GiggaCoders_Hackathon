import unittest
from pathlib import Path

from sentinel.models import Finding


class FindingTests(unittest.TestCase):

    def test_create_valid_finding(self):
        finding = Finding(
            file_path=Path("config.py"),
            line_number=12,
            secret_type="API Key",
            severity="HIGH",
            confidence=95,
            reason="Matches a known API key pattern",
            preview="sk_live_********1234",
        )

        self.assertEqual(finding.file_path, Path("config.py"))
        self.assertEqual(finding.line_number, 12)
        self.assertEqual(finding.secret_type, "API Key")
        self.assertEqual(finding.severity, "HIGH")
        self.assertEqual(finding.confidence, 95)

    def test_confidence_below_zero_raises_error(self):
        with self.assertRaises(ValueError):
            Finding(
                file_path=Path("config.py"),
                line_number=1,
                secret_type="Token",
                severity="HIGH",
                confidence=-1,
                reason="Test",
                preview="masked",
            )

    def test_confidence_above_hundred_raises_error(self):
        with self.assertRaises(ValueError):
            Finding(
                file_path=Path("config.py"),
                line_number=1,
                secret_type="Token",
                severity="HIGH",
                confidence=101,
                reason="Test",
                preview="masked",
            )

    def test_line_number_zero_raises_error(self):
        with self.assertRaises(ValueError):
            Finding(
                file_path=Path("config.py"),
                line_number=0,
                secret_type="Token",
                severity="HIGH",
                confidence=90,
                reason="Test",
                preview="masked",
            )

    def test_to_dict_converts_path_to_string(self):
        finding = Finding(
            file_path=Path("nested/config.py"),
            line_number=5,
            secret_type="GitHub Token",
            severity="CRITICAL",
            confidence=99,
            reason="Matches a known token pattern",
            preview="ghp_********abcd",
        )

        result = finding.to_dict()

        self.assertEqual(result["file_path"], "nested/config.py")
        self.assertEqual(result["line_number"], 5)
        self.assertEqual(result["confidence"], 99)


if __name__ == "__main__":
    unittest.main()