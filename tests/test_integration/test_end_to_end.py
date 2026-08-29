import tempfile
import unittest
from pathlib import Path

from sentinel.integrity import (
    compare_baseline,
    create_baseline,
)
from sentinel.scanner import scan_for_secrets


class EndToEndTests(unittest.TestCase):

    def test_complete_security_and_integrity_workflow(self):
        """
        Test the complete Sentinel workflow:

        1. Scan project for secrets.
        2. Create integrity baseline.
        3. Verify unchanged project.
        4. Modify a file.
        5. Add a file.
        6. Delete a file.
        7. Verify all integrity changes are detected.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()

            config = root / "config.py"
            config.write_text(
                'API_KEY = "YOUR_API_KEY_HERE"\n',
                encoding="utf-8",
            )

            app = root / "app.py"
            app.write_text(
                'print("hello")\n',
                encoding="utf-8",
            )

            readme = root / "README.md"
            readme.write_text(
                "# Demo Project\n",
                encoding="utf-8",
            )

            # Step 1: Scan the project.
            findings = scan_for_secrets(root)

            # The API key is a placeholder, so it should not
            # be reported as a real secret.
            self.assertEqual(findings, [])

            # Step 2: Create the integrity baseline.
            baseline = create_baseline(root)

            self.assertEqual(
                len(baseline),
                3,
            )

            # Step 3: Verify no changes exist initially.
            unchanged_results = compare_baseline(
                root,
                baseline,
            )

            self.assertEqual(
                unchanged_results,
                [],
            )

            # Step 4: Modify an existing file.
            app.write_text(
                'print("modified")\n',
                encoding="utf-8",
            )

            # Step 5: Add a new file.
            new_file = root / "new_config.py"
            new_file.write_text(
                'DEBUG = True\n',
                encoding="utf-8",
            )

            # Step 6: Delete an existing file.
            readme.unlink()

            # Step 7: Compare against original baseline.
            results = compare_baseline(
                root,
                baseline,
            )

            statuses = {
                result.file_path: result.status
                for result in results
            }

            self.assertEqual(
                statuses["app.py"],
                "MODIFIED",
            )

            self.assertEqual(
                statuses["new_config.py"],
                "NEW",
            )

            self.assertEqual(
                statuses["README.md"],
                "DELETED",
            )

            self.assertEqual(
                len(results),
                3,
            )


if __name__ == "__main__":
    unittest.main()