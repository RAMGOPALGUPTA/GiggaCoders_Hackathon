import unittest
from pathlib import Path

from sentinel.detectors import detect_secrets
from sentinel.detectors.secrets import mask_secret


class SecretDetectionTests(unittest.TestCase):

    def test_detects_aws_access_key(self):
        text = "AWS_KEY = AKIA1234567890ABCDEF"

        findings = detect_secrets(text, Path("config.py"))

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].secret_type, "AWS Access Key")
        self.assertEqual(findings[0].severity, "HIGH")
        self.assertEqual(findings[0].line_number, 1)

    def test_detects_github_token(self):
        token = "ghp_" + "A" * 36
        text = f"GITHUB_TOKEN={token}"

        findings = detect_secrets(text, Path(".env"))

        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0].secret_type,
            "GitHub Personal Access Token",
        )
        self.assertEqual(findings[0].severity, "CRITICAL")

    def test_detects_private_key_header(self):
        text = (
            "-----BEGIN RSA PRIVATE KEY-----\n"
            "fake-key-data\n"
            "-----END RSA PRIVATE KEY-----"
        )

        findings = detect_secrets(text, Path("private.pem"))

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].secret_type, "Private Key")
        self.assertEqual(findings[0].line_number, 1)

    def test_detects_password_assignment(self):
        text = 'password = "supersecret123"'

        findings = detect_secrets(text, Path("config.py"))

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].secret_type, "Password Assignment")

    def test_detects_api_key_assignment(self):
        text = 'api_key = "my-api-key-123456"'

        findings = detect_secrets(text, Path("settings.py"))

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].secret_type, "API Key Assignment")

    def test_correct_line_number(self):
        text = (
            "normal line\n"
            "another normal line\n"
            'password = "secret123"\n'
        )

        findings = detect_secrets(text, Path("config.py"))

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line_number, 3)

    def test_no_detection_for_normal_text(self):
        text = "This is an ordinary text file with no credentials."

        findings = detect_secrets(text, Path("notes.txt"))

        self.assertEqual(findings, [])

    def test_masks_long_secret(self):
        result = mask_secret("abcdefghijklmnop")

        self.assertTrue(result.startswith("abcd"))
        self.assertTrue(result.endswith("mnop"))
        self.assertNotIn("efghijkl", result)

    def test_masks_short_secret(self):
        self.assertEqual(mask_secret("abc"), "***")

    def test_multiple_secrets(self):
        token = "ghp_" + "A" * 36

        text = (
            'password = "secret123"\n'
            f"GITHUB_TOKEN={token}\n"
        )

        findings = detect_secrets(text, Path(".env"))

        self.assertEqual(len(findings), 2)




def test_ignores_placeholder_password(self):
    text = 'password = "changeme"'

    findings = detect_secrets(text, Path("config.py"))

    self.assertEqual(findings, [])


def test_ignores_placeholder_api_key(self):
    text = 'api_key = "your-api-key"'

    findings = detect_secrets(text, Path("config.py"))

    self.assertEqual(findings, [])


def test_ignores_repeated_x_placeholder(self):
    text = 'api_key = "xxxxxxxx"'

    findings = detect_secrets(text, Path("config.py"))

    self.assertEqual(findings, [])


def test_still_detects_real_password(self):
    text = 'password = "MyActualPassword123!"'

    findings = detect_secrets(text, Path("config.py"))

    self.assertEqual(len(findings), 1)
    self.assertEqual(findings[0].secret_type, "Password Assignment")

    def test_known_secret_has_dynamic_confidence(self):
        text = "AWS_KEY = AKIA1234567890ABCDEF"

        findings = detect_secrets(text, Path("config.py"))

        self.assertEqual(len(findings), 1)
        self.assertGreaterEqual(findings[0].confidence, 90)

    def test_generic_password_has_lower_confidence_than_known_token(self):
        password_text = 'password = "MyPassword123!"'
        token = "ghp_" + "A" * 36
        token_text = f"GITHUB_TOKEN={token}"

        password_findings = detect_secrets(
            password_text,
            Path("config.py"),
        )

        token_findings = detect_secrets(
            token_text,
            Path(".env"),
        )

        self.assertLess(
            password_findings[0].confidence,
            token_findings[0].confidence,
        )

if __name__ == "__main__":
    unittest.main()