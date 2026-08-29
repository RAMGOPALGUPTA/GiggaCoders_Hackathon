import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sentinel.__main__ import create_parser, main


class ParserTests(unittest.TestCase):

    def test_scan_command_parses_target(self):
        parser = create_parser()

        args = parser.parse_args(
            ["scan", "project"]
        )

        self.assertEqual(args.command, "scan")
        self.assertEqual(args.target, "project")
        self.assertFalse(args.json_output)
        self.assertEqual(args.exclude, [])

    def test_scan_command_parses_json_flag(self):
        parser = create_parser()

        args = parser.parse_args(
            ["scan", "project", "--json"]
        )

        self.assertTrue(args.json_output)

    def test_scan_command_parses_multiple_excludes(self):
        parser = create_parser()

        args = parser.parse_args(
            [
                "scan",
                "project",
                "--exclude",
                "tests",
                "--exclude",
                "demo",
            ]
        )

        self.assertEqual(
            args.exclude,
            ["tests", "demo"],
        )

    def test_baseline_command_parses_arguments(self):
        parser = create_parser()

        args = parser.parse_args(
            [
                "baseline",
                "project",
                "--output",
                "baseline.json",
            ]
        )

        self.assertEqual(args.command, "baseline")
        self.assertEqual(args.target, "project")
        self.assertEqual(
            args.output,
            "baseline.json",
        )

    def test_integrity_command_parses_arguments(self):
        parser = create_parser()

        args = parser.parse_args(
            [
                "integrity",
                "project",
                "baseline.json",
            ]
        )

        self.assertEqual(args.command, "integrity")
        self.assertEqual(args.target, "project")
        self.assertEqual(
            args.baseline,
            "baseline.json",
        )


class MainTests(unittest.TestCase):

    @patch("sys.argv", ["sentinel"])
    def test_main_without_command_returns_two(self):
        self.assertEqual(main(), 2)

    @patch("sys.argv", ["sentinel", "scan", "missing-path"])
    def test_main_with_missing_target_returns_two(self):
        self.assertEqual(main(), 2)

    def test_main_creates_baseline(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            target = root / "project"
            target.mkdir()

            file_path = target / "config.txt"
            file_path.write_text(
                "original content",
                encoding="utf-8",
            )

            output = root / "baseline.json"

            with patch(
                "sys.argv",
                [
                    "sentinel",
                    "baseline",
                    str(target),
                    "--output",
                    str(output),
                ],
            ):
                result = main()

            self.assertEqual(result, 0)
            self.assertTrue(output.exists())

    def test_main_integrity_returns_zero_when_unchanged(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            target = root / "project"
            target.mkdir()

            file_path = target / "config.txt"
            file_path.write_text(
                "original content",
                encoding="utf-8",
            )

            baseline = root / "baseline.json"

            with patch(
                "sys.argv",
                [
                    "sentinel",
                    "baseline",
                    str(target),
                    "--output",
                    str(baseline),
                ],
            ):
                main()

            with patch(
                "sys.argv",
                [
                    "sentinel",
                    "integrity",
                    str(target),
                    str(baseline),
                ],
            ):
                result = main()

            self.assertEqual(result, 0)

    def test_main_integrity_returns_one_when_changed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            target = root / "project"
            target.mkdir()

            file_path = target / "config.txt"
            file_path.write_text(
                "original content",
                encoding="utf-8",
            )

            baseline = root / "baseline.json"

            with patch(
                "sys.argv",
                [
                    "sentinel",
                    "baseline",
                    str(target),
                    "--output",
                    str(baseline),
                ],
            ):
                main()

            file_path.write_text(
                "modified content",
                encoding="utf-8",
            )

            with patch(
                "sys.argv",
                [
                    "sentinel",
                    "integrity",
                    str(target),
                    str(baseline),
                ],
            ):
                result = main()

            self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()