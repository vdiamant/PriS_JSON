#!/usr/bin/env python3
"""Self-tests for the PriS JSON schemas and validator (no pytest needed).

Run from the repository root:  python tests/run_tests.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from validate import SCHEMAS, validate_paths  # noqa: E402

EXAMPLE_PATTERN = ROOT / "examples" / "career-office" / "anonymity.pattern.json"
INVALID = ROOT / "tests" / "invalid"

# fixture -> text expected in at least one error message
EXPECTED_FAILURES = {
    "bad-decomposition.requirement.json": "'XOR' is not one of",
    "bad-option-key.requirement.json": "'Option A' does not match",
    "unknown-privacy-goal.requirement.json": "'Anonymisation' is not one of",
    "pet-not-in-pattern.requirement.json": "'Homomorphic encryption' is not an implementation technique",
    "self-related.pattern.json": "lists itself",
    "option-gap.pattern.json": "not numbered 1..3",
    "missing-forces.pattern.json": "'Forces' is a required property",
}


def check(condition: bool, message: str, failures: list[str]) -> None:
    print(("PASS " if condition else "FAIL ") + message)
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []

    errors, warnings = validate_paths([ROOT / "examples"])
    check(not errors and not warnings, f"examples validate cleanly {errors + warnings}", failures)

    enums = [json.loads(p.read_text(encoding="utf-8"))["$defs"]["privacyProperty"]["enum"] for p in SCHEMAS.values()]
    check(enums[0] == enums[1], "privacy-property lists identical in both schemas", failures)

    listed = {p.name for p in INVALID.glob("*.json")}
    check(listed == set(EXPECTED_FAILURES), "every invalid fixture has an expected failure", failures)

    for name, expected in EXPECTED_FAILURES.items():
        paths = [INVALID / name]
        if name.endswith(".requirement.json"):
            paths.append(EXAMPLE_PATTERN)  # enables the PET cross-check
        errors, _ = validate_paths(paths)
        check(any(expected in e for e in errors), f"{name} rejected ({expected})", failures)

    print(f"\n{'FAILED' if failures else 'OK'}: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
