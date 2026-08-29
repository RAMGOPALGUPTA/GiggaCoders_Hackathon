import unittest

from sentinel.detectors.entropy import (
    calculate_entropy,
    is_high_entropy,
)


class EntropyTests(unittest.TestCase):

    def test_empty_string_has_zero_entropy(self):
        self.assertEqual(calculate_entropy(""), 0.0)

    def test_repeated_character_has_zero_entropy(self):
        self.assertEqual(calculate_entropy("aaaaaaaaaa"), 0.0)

    def test_entropy_of_mixed_characters_is_higher(self):
        low_entropy = calculate_entropy("aaaaaaaaaaaaaaaaaaaa")
        high_entropy = calculate_entropy("aB9$xP2mQ7!vL4zR8nW3")

        self.assertGreater(high_entropy, low_entropy)

    def test_high_entropy_value_is_detected(self):
        value = "aB9$xP2mQ7!vL4zR8nW3"

        self.assertTrue(is_high_entropy(value))

    def test_short_value_is_not_high_entropy(self):
        value = "aB9$xP2mQ7"

        self.assertFalse(is_high_entropy(value))

    def test_repeated_value_is_not_high_entropy(self):
        value = "aaaaaaaaaaaaaaaaaaaa"

        self.assertFalse(is_high_entropy(value))

    def test_custom_threshold_can_be_used(self):
        value = "abcdefghijabcdefghij"

        self.assertTrue(
            is_high_entropy(
                value,
                threshold=2.0,
                minimum_length=10,
            )
        )

    def test_returns_float(self):
        result = calculate_entropy("hello world")

        self.assertIsInstance(result, float)


if __name__ == "__main__":
    unittest.main()