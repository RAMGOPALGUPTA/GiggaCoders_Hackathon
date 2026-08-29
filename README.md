# Sentinel

A zero-dependency security scanner and file integrity monitoring tool written in Python.

Sentinel helps developers identify potential hardcoded secrets in source code and detect file changes using SHA-256 integrity baselines.

## Features

1. **Secret Detection** — Detects potential hardcoded credentials and secrets using configurable patterns.
2. **Password Detection** — Detects password-like variable assignments while reducing false positives from common placeholder values.
3. **API Key Detection** — Detects API-key-like assignments and masks detected values in reports.
4. **Secret Masking** — Potential secrets are displayed in masked form so complete credentials are not unnecessarily exposed.
5. **Confidence Scoring** — Findings include confidence scores to help distinguish stronger matches from weaker ones.
6. **Severity Levels** — Findings are categorized with severity information to make security results easier to prioritize.
7. **File and Directory Scanning** — Sentinel can scan either a single file or an entire directory recursively.
8. **Smart File Filtering** — Binary and unreadable files are skipped safely, and configured directories can be excluded from scans.
9. **JSON Reporting** — Scan results can be exported in JSON format for automation and integration.
10. **File Integrity Monitoring** — Sentinel creates SHA-256 baselines and later detects modified, added, and deleted files.

## Requirements

- Python 3.10 or newer
- No third-party dependencies

## Project Structure

```text
sentinel/
├── src/
│   └── sentinel/
│       ├── detectors/
│       ├── integrity/
│       ├── models/
│       ├── reporting/
│       ├── scanner/
│       └── __main__.py
└── tests/
    ├── test_cli/
    ├── test_detectors/
    ├── test_integration/
    ├── test_integrity/
    ├── test_models/
    ├── test_reporting/
    └── test_scanner/
```

## Installation

```bash
git clone <YOUR-REPOSITORY-URL>
cd sentinel
```

No external packages are required.

## Running Sentinel

### PowerShell

```powershell
$env:PYTHONPATH="src"
```

### Security Scan

```powershell
python -m sentinel scan <target>
```

Example:

```powershell
python -m sentinel scan .
```

### JSON Output

```powershell
python -m sentinel scan . --json
```

### Create an Integrity Baseline

```powershell
python -m sentinel baseline <target> --output baseline.json
```

Example:

```powershell
python -m sentinel baseline . --output sentinel-baseline.json
```

### Check File Integrity

```powershell
python -m sentinel integrity <target> <baseline-file>
```

Example:

```powershell
python -m sentinel integrity . sentinel-baseline.json
```

The integrity checker detects:

- `MODIFIED`
- `ADDED`
- `DELETED`

## Running Tests

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -p "test_*.py"
```

The project includes comprehensive unit, integration, edge-case, and adversarial tests.

## Example Workflow

### Step 1: Scan the project

```powershell
python -m sentinel scan .
```

### Step 2: Create an integrity baseline

```powershell
python -m sentinel baseline . --output sentinel-baseline.json
```

### Step 3: Check for changes

```powershell
python -m sentinel integrity . sentinel-baseline.json
```

## Security Design

- Detected secret values are masked in reports.
- Common placeholder credentials are filtered to reduce false positives.
- Binary and unreadable files are handled safely.
- SHA-256 hashes are used for integrity comparison.
- Invalid baseline data is validated before use.
- File additions, modifications, and deletions are detected.

## Limitations

Sentinel is a lightweight educational and developer-focused security tool. Pattern-based secret detection cannot guarantee detection of every possible credential and may still produce false positives or false negatives.

Integrity monitoring detects changes relative to a saved baseline. The baseline itself should be protected separately.

## Future Improvements

- Additional secret patterns
- Configurable ignore rules
- Custom scanning policies
- SARIF reporting
- CI/CD integration
- Cryptographic signing of baselines
- Web dashboard
- Automated scheduled scans

## Demo

1. Run a security scan.
2. Show detected findings and masked secret previews.
3. Generate JSON output.
4. Create a SHA-256 integrity baseline.
5. Modify, add, or delete a file.
6. Run the integrity check.
7. Show the detected changes.
8. Run the automated test suite.

## Why Sentinel?

Sentinel combines two useful security capabilities in a single lightweight tool:

- **Secret scanning** for identifying potential hardcoded credentials.
- **File integrity monitoring** for detecting unexpected changes.

The project uses only the Python standard library and includes automated testing for core functionality, edge cases, adversarial inputs, command-line behavior, and end-to-end workflows.

## License

This project is intended for educational and demonstration purposes.
