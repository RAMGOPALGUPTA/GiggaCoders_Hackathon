import unittest
from pathlib import Path

from sentinel.models import Finding
from sentinel.reporting.console import build_console_report


class ConsoleReportTests(unittest.TestCase):

    def test_empty_report(self):
        report = build_console_report(
            [],
            Path("project"),
        )

        self.assertIn("SENTINEL SECURITY SCAN", report)
        self.assertIn("No potential secrets found.", report)
        self.assertIn("Total findings: 0", report)

    def test_report_contains_finding_details(self):
        finding = Finding(
            file_path=Path("config.py"),
            line_number=10,
            secret_type="Password Assignment",
            severity="HIGH",
            confidence=75,
            reason="Contains a password-like variable assignment",
            preview="MyAc********23",
        )

        report = build_console_report(
            [finding],
            Path("project"),
        )

        self.assertIn("HIGH", report)
        self.assertIn("config.py:10", report)
        self.assertIn("Password Assignment", report)
        self.assertIn("75%", report)
        self.assertIn("Total findings: 1", report)
        self.assertIn("HIGH: 1", report)

    def test_findings_are_sorted_by_severity(self):
        low_finding = Finding(
            file_path=Path("low.txt"),
            line_number=1,
            secret_type="Low Finding",
            severity="LOW",
            confidence=50,
            reason="Low severity",
            preview="low",
        )

        critical_finding = Finding(
            file_path=Path("critical.txt"),
            line_number=1,
            secret_type="Critical Finding",
            severity="CRITICAL",
            confidence=100,
            reason="Critical severity",
            preview="critical",
        )

        report = build_console_report(
            [low_finding, critical_finding],
            Path("project"),
        )

        critical_position = report.find("Critical Finding")
        low_position = report.find("Low Finding")

        self.assertLess(
            critical_position,
            low_position,
        )

    def test_multiple_severity_counts(self):
        findings = [
            Finding(
                file_path=Path("a.txt"),
                line_number=1,
                secret_type="One",
                severity="CRITICAL",
                confidence=100,
                reason="Test",
                preview="a",
            ),
            Finding(
                file_path=Path("b.txt"),
                line_number=2,
                secret_type="Two",
                severity="HIGH",
                confidence=80,
                reason="Test",
                preview="b",
            ),
            Finding(
                file_path=Path("c.txt"),
                line_number=3,
                secret_type="Three",
                severity="HIGH",
                confidence=70,
                reason="Test",
                preview="c",
            ),
        ]

        report = build_console_report(
            findings,
            Path("project"),
        )

        self.assertIn("CRITICAL: 1", report)
        self.assertIn("HIGH: 2", report)
        self.assertIn("MEDIUM: 0", report)
        self.assertIn("LOW: 0", report)


if __name__ == "__main__":
    unittest.main()
    