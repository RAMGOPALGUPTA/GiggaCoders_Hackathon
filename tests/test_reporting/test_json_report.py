import json
import unittest
from pathlib import Path

from sentinel.models import Finding
from sentinel.reporting.json_report import build_json_report


class JsonReportTests(unittest.TestCase):

    def test_empty_json_report(self):
        report = build_json_report(
            [],
            Path("project"),
        )

        data = json.loads(report)

        self.assertEqual(
            data["target"],
            "project",
        )

        self.assertEqual(
            data["total_findings"],
            0,
        )

        self.assertEqual(
            data["findings"],
            [],
        )

    def test_json_report_contains_finding(self):
        finding = Finding(
            file_path=Path("config.py"),
            line_number=5,
            secret_type="API Key Assignment",
            severity="HIGH",
            confidence=80,
            reason="Contains an API-key-like variable assignment",
            preview="abcd******wxyz",
        )

        report = build_json_report(
            [finding],
            Path("project"),
        )

        data = json.loads(report)

        self.assertEqual(
            data["total_findings"],
            1,
        )

        self.assertEqual(
            data["findings"][0]["secret_type"],
            "API Key Assignment",
        )

        self.assertEqual(
            data["findings"][0]["file_path"],
            "config.py",
        )

    def test_json_report_is_valid_json(self):
        report = build_json_report(
            [],
            Path("project"),
        )

        data = json.loads(report)

        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
    