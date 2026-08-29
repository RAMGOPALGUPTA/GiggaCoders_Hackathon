import re


PLACEHOLDER_VALUES = {
    "",
    "example",
    "example_key",
    "example-key",
    "example_password",
    "your-api-key",
    "your_api_key",
    "your_api_key_here",
    "your-key",
    "your_key",
    "your-token",
    "your_token",
    "your_token_here",
    "your-secret",
    "your_secret",
    "your_secret_here",
    "your-password",
    "your_password",
    "your_password_here",
    "changeme",
    "change-me",
    "change_me",
    "placeholder",
    "dummy",
    "dummy_key",
    "dummy-key",
    "dummy_value",
    "test",
    "test_key",
    "test-key",
    "test_value",
    "fake",
    "fake_key",
    "fake-key",
    "secret",
    "password",
    "none",
    "null",
}


def is_placeholder(value: str) -> bool:
    """
    Return True when a value looks like a common example,
    placeholder, dummy, or test credential.
    """
    normalized = value.strip().lower()

    if normalized in PLACEHOLDER_VALUES:
        return True

    if normalized.startswith("example_"):
        return True

    if normalized.startswith("dummy_"):
        return True

    if normalized.startswith("test_"):
        return True

    if normalized.startswith("fake_"):
        return True

    if re.fullmatch(r"x{4,}", normalized):
        return True

    if re.fullmatch(r"\*{4,}", normalized):
        return True

    return False