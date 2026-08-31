# Sentinel

A zero-dependency security scanner and file integrity monitoring tool written in Python.

Sentinel helps developers identify potential hardcoded secrets in source code and detect unexpected file changes using SHA-256 integrity baselines.

Built for the **Zero Dependency 2026 Hackathon — Track E: Security & Crypto Utilities**.

## Features

1. **Secret Detection** — Detects potential hardcoded credentials and secrets using pattern-based analysis.
2. **Password Detection** — Detects password-like variable assignments while reducing false positives from common placeholder values.
3. **API Key Detection** — Detects API-key-like assignments and masks detected values in reports.
4. **Secret Masking** — Potential secrets are displayed in masked form so complete credentials are not unnecessarily exposed.
5. **Confidence Scoring** — Findings include confidence scores to help distinguish stronger matches from weaker ones.
6. **Severity Levels** — Findings are categorized by severity to make security results easier to prioritize.
7. **File and Directory Scanning** — Sentinel can scan either a single file or an entire directory recursively.
8. **Smart File Filtering** — Binary and unreadable files are skipped safely, and configured directories can be excluded from scans.
9. **JSON Reporting** — Scan results can be exported in JSON format for automation and integration.
10. **File Integrity Monitoring** — Sentinel creates SHA-256 baselines and detects modified, new, and deleted files.

## Requirements

- Python 3.12.x (team-tested runtime)
- No third-party runtime dependencies

Sentinel uses Python's standard library and its own source code. No external packages are required to run the application or test suite.

## Installation

Clone the repository:

```powershell
git clone https://github.com/RAMGOPALGUPTA/GiggaCoders_Hackathon.git
cd GiggaCoders_Hackathon
```

No package installation is required.

## Build and Run

Sentinel is a Python command-line application and does not require a compilation step or package installation.

From the project root, start the CLI with one command:

```powershell
$env:PYTHONPATH="src"; python -m sentinel --help
```

For a security scan:

```powershell
$env:PYTHONPATH="src"; python -m sentinel scan demo_project
```

## Running Sentinel

### PowerShell

Set the source path for the current terminal session:

```powershell
$env:PYTHONPATH="src"
```

### Security Scan

Scan a file or directory:

```powershell
python -m sentinel scan <target>
```

Example:

```powershell
python -m sentinel scan demo_project
```

### JSON Output

Export scan results as JSON:

```powershell
python -m sentinel scan demo_project --json
```

### Create an Integrity Baseline

Create a SHA-256 integrity baseline:

```powershell
python -m sentinel baseline <target> --output baseline.json
```

Example:

```powershell
python -m sentinel baseline demo_project --output sentinel-baseline.json
```

### Check File Integrity

Compare the current project state against a saved baseline:

```powershell
python -m sentinel integrity <target> <baseline-file>
```

Example:

```powershell
python -m sentinel integrity demo_project sentinel-baseline.json
```

The integrity checker can report:

- `MODIFIED` — an existing file has changed
- `NEW` — a file appeared after the baseline was created
- `DELETED` — a baseline file is no longer present

## Demo Project

The repository includes a small `demo_project` containing intentionally fake credentials for demonstrating Sentinel's secret detection capabilities.

The demonstration credentials are not real credentials and must not be used for authentication or access to external services.

Run the demonstration scan:

```powershell
$env:PYTHONPATH="src"
python -m sentinel scan demo_project
```

The demo project can also be used to demonstrate:

- Secret detection
- Secret masking
- Confidence and severity scoring
- Placeholder filtering
- JSON reporting
- SHA-256 integrity monitoring

## Running Tests

Run the complete automated test suite:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -p "test_*.py"
```

The project includes unit, integration, edge-case, adversarial, CLI, and end-to-end tests.

Current verification:

```text
Ran 117 tests
OK
```

## Zero-Dependency Verification

Sentinel is designed to run without third-party runtime packages.

Dependency verification was performed inside a clean Python virtual environment.

The environment was checked with:

```powershell
python -m pip freeze
```

The command returned no third-party packages.

Sentinel was then executed successfully with:

```powershell
$env:PYTHONPATH="src"
python -m sentinel --help
```

The complete test suite also passed in the same clean environment:

```text
Ran 117 tests
OK
```

A concise verification record is included in:

```text
deps-proof.txt
```

The standard-library substitutions and implementation details are documented in:

```text
STDLIB.md
```

## Standard Library Usage

Sentinel intentionally replaces common third-party functionality with Python standard-library modules.

| Capability | Standard Library |
|---|---|
| Command-line interface | `argparse` |
| File traversal | `pathlib` |
| Regular expressions | `re` |
| SHA-256 hashing | `hashlib` |
| JSON processing | `json` |
| Data models | `dataclasses` |
| Entropy analysis | `math`, `collections` |
| Testing | `unittest` |
| Temporary test environments | `tempfile` |

See `STDLIB.md` for the detailed substitution log.

## Example Workflow

### Step 1: Scan the project

```powershell
$env:PYTHONPATH="src"
python -m sentinel scan demo_project
```

### Step 2: Generate JSON results

```powershell
python -m sentinel scan demo_project --json
```

### Step 3: Create an integrity baseline

```powershell
python -m sentinel baseline demo_project --output sentinel-baseline.json
```

### Step 4: Make a file change

Modify an existing file, add a new file, or delete a file after the baseline has been created.

### Step 5: Check for integrity changes

```powershell
python -m sentinel integrity demo_project sentinel-baseline.json
```

The result can contain:

```text
MODIFIED
NEW
DELETED
```

## Security Design

- Detected secret values are masked in reports.
- Common placeholder credentials are filtered to reduce false positives.
- Binary and unreadable files are handled safely.
- Pattern matching is combined with contextual analysis and confidence scoring.
- SHA-256 hashes are used for integrity comparison.
- Invalid baseline data is validated before use.
- File additions, modifications, and deletions are detected.
- The baseline format is validated before integrity comparison.

## Testing and Adversarial Coverage

Sentinel has been tested against normal and adversarial inputs, including:

- Password-like assignments
- API-key-like assignments
- Placeholder credentials
- Dummy and test values
- High-entropy values
- Binary files
- Unreadable files
- Nested directories
- Explicitly excluded directories
- Git directories
- Invalid baseline data
- Missing targets
- Missing baseline files
- Modified files
- New files
- Deleted files
- CLI error cases
- Complete end-to-end workflows

The final test suite currently passes **117 tests**.

## Limitations

Sentinel is a lightweight developer-focused security tool.

Pattern-based secret detection cannot guarantee detection of every possible credential and may still produce false positives or false negatives.

Integrity monitoring detects changes relative to a saved baseline. The baseline itself should be protected separately and should not be treated as an independently trusted security boundary.

## Future Improvements

Potential future improvements include:

- Additional secret patterns
- More configurable ignore rules
- Custom scanning policies
- SARIF reporting
- CI/CD integration
- Cryptographic signing of baselines
- Web dashboard
- Automated scheduled scans

## Demo

The demonstration video showcases the following workflow:

1. Introduce the Sentinel project.
2. Demonstrate the security problem.
3. Scan a project containing fake credentials.
4. Show detected findings and masked secret previews.
5. Demonstrate placeholder filtering and confidence scoring.
6. Generate JSON scan output.
7. Create a SHA-256 integrity baseline.
8. Modify and add files after the baseline.
9. Run the integrity checker and show detected changes.
10. Run the complete automated test suite.
11. Demonstrate the zero-dependency implementation and verification.

## Why Sentinel?

Sentinel combines two useful security capabilities in a single lightweight command-line tool:

- **Secret scanning** for identifying potential hardcoded credentials.
- **File integrity monitoring** for detecting unexpected file changes.

The project uses Python's standard library and its own implementation without requiring third-party runtime dependencies.

Sentinel also includes automated testing covering core functionality, edge cases, adversarial inputs, command-line behavior, integrity tampering, and end-to-end workflows.

## Hackathon Context

Sentinel was built for the **Zero Dependency 2026 Hackathon — Track E: Security & Crypto Utilities**.

The project is designed around the hackathon's zero-dependency requirement: useful security functionality implemented with the standard library rather than third-party runtime packages.

## Team

- **Amay** — Scanner and secret-detection subsystem
- **Ram Gopal** — Integrity and security subsystem
- **Sarab** — CLI, reporting, integration, and presentation

## License

This project is intended for educational and demonstration purposes.