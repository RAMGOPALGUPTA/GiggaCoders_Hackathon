# Standard Library Substitutions

This file will document third-party packages we would normally use and
the Python standard-library functionality used instead.

| Normally | Instead |
|---|---|
| pathlib helper package | pathlib |
| pytest | unittest |
| requests | urllib / http.client when needed |
| rich logging | logging |
| external hashing package | hashlib / hmac |
| external randomness package | secrets |
| JSON helper package | json |
| CLI framework | argparse |
| config package | configparser |
| tempfile helper package | tempfile |

The final team will update this table with only substitutions actually
used by Sentinel.
