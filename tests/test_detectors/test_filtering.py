import unittest

from sentinel.detectors.filtering import is_placeholder


class PlaceholderFilteringTests(unittest.TestCase):

    def test_detects_changeme(self):
        self.assertTrue(is_placeholder("changeme"))

    def test_detects_example(self):
        self.assertTrue(is_placeholder("example"))

    def test_detects_dummy_key(self):
        self.assertTrue(is_placeholder("dummy_key"))

    def test_detects_your_api_key(self):
        self.assertTrue(is_placeholder("your-api-key"))

    def test_detects_repeated_x(self):
        self.assertTrue(is_placeholder("xxxxxxxx"))

    def test_detects_repeated_asterisks(self):
        self.assertTrue(is_placeholder("********"))

    def test_realistic_value_is_not_placeholder(self):
        self.assertFalse(is_placeholder("MyRealSecret123!"))

    def test_value_is_case_insensitive(self):
        self.assertTrue(is_placeholder("CHANGEme"))

    def test_whitespace_is_ignored(self):
        self.assertTrue(is_placeholder("  example  "))


if __name__ == "__main__":
    unittest.main()