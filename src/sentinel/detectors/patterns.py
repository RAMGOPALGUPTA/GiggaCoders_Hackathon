import re


SECRET_PATTERNS = {
    "AWS Access Key": {
        "pattern": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "severity": "HIGH",
        "reason": "Matches the AWS Access Key ID format",
    },
    "GitHub Personal Access Token": {
        "pattern": re.compile(r"\bghp_[A-Za-z0-9]{36}\b"),
        "severity": "CRITICAL",
        "reason": "Matches the GitHub personal access token format",
    },
    "Private Key": {
        "pattern": re.compile(
            r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"
        ),
        "severity": "CRITICAL",
        "reason": "Contains a private key header",
    },
    "Password Assignment": {
        "pattern": re.compile(
            r"""(?ix)
            \b
            (?:password|passwd|pwd)
            \b
            \s*
            [:=]
            \s*
            ["']?
            ([^\s"',;]+)
            """,
        ),
        "severity": "HIGH",
        "reason": "Contains a password-like variable assignment",
    },
    "API Key Assignment": {
        "pattern": re.compile(
            r"""(?ix)
            \b
            (?:api[_-]?key|apikey|access[_-]?key)
            \b
            \s*
            [:=]
            \s*
            ["']?
            ([^\s"',;]+)
            """,
        ),
        "severity": "HIGH",
        "reason": "Contains an API-key-like variable assignment",
    },
}