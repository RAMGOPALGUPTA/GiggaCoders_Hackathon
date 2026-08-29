import unittest

from sentinel.detectors.scoring import (
    calculate_confidence,
    has_secret_context,
)


class ContextTests(unittest.TestCase):

    def test_detects_password_context(self):
        self.assertTrue(
            has_secret_context('password = "secret123"')
        )

    def test_detects_token_context(self):
        self.assertTrue(
            has_secret_context("GITHUB_TOKEN=value")
        )

    def test_normal_text_has_no_secret_context(self):
        self.assertFalse(
            has_secret_context("The weather is nice today.")
        )


class ConfidenceScoringTests(unittest.TestCase):

    def test_aws_key_has_high_base_confidence(self):
        score = calculate_confidence(
            value="AKIA1234567890ABCDEF",
            secret_type="AWS Access Key",
            context="AWS_KEY = AKIA1234567890ABCDEF",
        )

        self.assertGreaterEqual(score, 90)

    def test_github_token_has_high_confidence(self):
        value = "ghp_" + "A" * 36

        score = calculate_confidence(
            value=value,
            secret_type="GitHub Personal Access Token",
            context=f"GITHUB_TOKEN={value}",
        )

        self.assertGreaterEqual(score, 95)

    def test_private_key_is_maximum_confidence(self):
        score = calculate_confidence(
            value="-----BEGIN RSA PRIVATE KEY-----",
            secret_type="Private Key",
            context="-----BEGIN RSA PRIVATE KEY-----",
        )

        self.assertEqual(score, 100)

    def test_generic_secret_has_lower_base_confidence(self):
        score = calculate_confidence(
            value="secret123",
            secret_type="Password Assignment",
            context='password = "secret123"',
        )

        self.assertLess(score, 90)

    def test_score_never_exceeds_hundred(self):
        value = "aB9$xP2mQ7!vL4zR8nW3zK5#fT"

        score = calculate_confidence(
            value=value,
            secret_type="GitHub Personal Access Token",
            context=f"token={value}",
        )

        self.assertLessEqual(score, 100)

    def test_high_entropy_increases_confidence(self):
        low_value = "aaaaaaaaaaaaaaaaaaaa"
        high_value = "aB9$xP2mQ7!vL4zR8nW3"

        low_score = calculate_confidence(
            value=low_value,
            secret_type="Password Assignment",
            context="value",
        )

        high_score = calculate_confidence(
            value=high_value,
            secret_type="Password Assignment",
            context="value",
        )

        self.assertGreater(high_score, low_score)


if __name__ == "__main__":
    unittest.main()