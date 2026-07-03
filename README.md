# bc-sha256-usb-miner

Safe USB-aware SHA-256 proof-of-work miner scaffold with ledgered audit trails, explicit-run operation, and educational benchmarking.

## Overview

This project is an educational scaffold for a safe, USB-aware SHA-256 proof-of-work miner. It focuses on:
- Clear, auditable mining operations (audit trail recording).
- Explicit-run CLI behavior and safe shutdown handling.
- Educational benchmarking and easily testable mining parameters.

> Note: This repository is educational. It is not intended for production crypto-mining.

## Quickstart

Requirements
- Python 3.9+

Install (recommended in a virtual environment)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run a quick test (low difficulty for local testing):
```bash
python sha256_usb_miner.py "hello" 1
```

This runs the miner over the input data "hello" with difficulty 1 (hex-leading zeros). For CI and unit tests, the project uses a workflow located at `.github/workflows/python-tests.yml`.

## Development notes

- Core miner class: `SHA256Miner` in `sha256_usb_miner.py`. For testing, prefer calling the class programmatically rather than via CLI.
- Difficulty is evaluated as the number of leading hex nibbles equal to `0` in the hex digest (i.e., difficulty=1 requires the hash to start with `"0"`).
- Default `max_nonce` is intentionally large for completeness; for local runs/tests change this to a much smaller value.

Suggested development tasks:
- Add unit tests in `tests/` that run the miner with small `difficulty` and `max_nonce`.
- Add an `examples/basic_usage.md` describing example runs and benchmarking commands.
- Replace CLI `print()` usage with `logging` for CI-friendly output and easily toggled verbosity.

## Contributing

Please follow the contribution guidelines and run tests locally before raising PRs. See `CONTRIBUTING.md` for details (TODO).

## License & Security

Add license info (LICENSE file) and SECURITY.md with vulnerability disclosure instructions.
