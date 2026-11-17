#!/usr/bin/env python3
"""Validate PriS JSON files against the schemas in ../schema.

File naming convention:
  *.requirement.json  -> schema/pris-privacy-requirement.schema.json
  *.pattern.json      -> schema/pris-privacy-process-pattern.schema.json

Besides JSON Schema validation, the script runs consistency checks that
JSON Schema cannot express:
  - "Option N" keys start at 1 and are consecutive;
  - a pattern does not list itself among its related patterns;
  - every PET chosen for a privacy requirement is one of the implementation
    techniques of the Privacy Process Pattern applied to its process
    (only when that pattern's file is among the files validated).

Usage:
  python tools/validate.py                 # validates examples/ and patterns/
  python tools/validate.py PATH [PATH ...] # files or directories
  python tools/validate.py --strict ...    # warnings also fail the run

Requires: jsonschema >= 4.18  (pip install jsonschema)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"
SCHEMAS = {
    "requirement": SCHEMA_DIR / "pris-privacy-requirement.schema.json",
    "pattern": SCHEMA_DIR / "pris-privacy-process-pattern.schema.json",
}
OPTION_KEY = re.compile(r"^Option ([1-9][0-9]*)$")


def load_json(path: Path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_validators() -> dict[str, Draft202012Validator]:
    validators = {}
    for kind, path in SCHEMAS.items():
        schema = load_json(path)
        Draft202012Validator.check_schema(schema)
        validators[kind] = Draft202012Validator(schema)
    return validators


def kind_of(path: Path) -> str | None:
    if path.name.endswith(".requirement.json"):
        return "requirement"
    if path.name.endswith(".pattern.json"):
        return "pattern"
    return None


def collect(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        if p.is_dir():
            files.extend(sorted(f for f in p.rglob("*.json") if kind_of(f)))
        elif p.is_file():
            files.append(p)
        else:
            raise FileNotFoundError(p)
    return files


def option_numbering(obj: dict, where: str) -> list[str]:
    numbers = sorted(int(m.group(1)) for k in obj if (m := OPTION_KEY.match(k)))
    if numbers and numbers != list(range(1, len(numbers) + 1)):
        return [f"{where}: options are not numbered 1..{len(numbers)} (found {numbers})"]
    return []


def options(obj: dict) -> list[str]:
    return [v for k, v in obj.items() if OPTION_KEY.match(k)]


def validate_paths(paths: list[Path]) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for the given files or directories."""
    validators = load_validators()
    errors: list[str] = []
    warnings: list[str] = []
    documents: list[tuple[Path, str, object]] = []

    for path in collect(paths):
        kind = kind_of(path)
        if kind is None:
            errors.append(f"{path}: name must end in .requirement.json or .pattern.json")
            continue
        try:
            doc = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON ({exc})")
            continue
        schema_errors = sorted(validators[kind].iter_errors(doc), key=lambda e: list(e.absolute_path))
        for err in schema_errors:
            location = "/".join(str(p) for p in err.absolute_path) or "(root)"
            errors.append(f"{path}: {location}: {err.message}")
        if not schema_errors:
            documents.append((path, kind, doc))

    # Index valid patterns by name.
    patterns: dict[str, tuple[Path, dict]] = {}
    for path, kind, doc in documents:
        if kind != "pattern":
            continue
        name = doc["Name"]
        if name in patterns:
            warnings.append(f"{path}: pattern '{name}' also defined in {patterns[name][0]}")
        patterns[name] = (path, doc)
        if name in doc["Related patterns"]:
            errors.append(f"{path}: pattern '{name}' lists itself in 'Related patterns'")
        for i, category in enumerate(doc["Implementation techniques"]):
            errors += option_numbering(category, f"{path}: Implementation techniques/{i}")

    # Cross-check requirements against their patterns.
    for path, kind, doc in documents:
        if kind != "requirement":
            continue
        for i, record in enumerate(doc["privacy requirement"]):
            where = f"{path}: privacy requirement/{i}"
            pets = record["Privacy Enhancing Technologies"]
            errors += option_numbering(pets, f"{where}/Privacy Enhancing Technologies")
            pattern_name = record["Process"]["Process Pattern"]
            if pattern_name not in patterns:
                warnings.append(f"{where}: pattern '{pattern_name}' not among the validated files; PETs not cross-checked")
                continue
            available = {t for c in patterns[pattern_name][1]["Implementation techniques"] for t in options(c)}
            for pet in options(pets):
                if pet not in available:
                    errors.append(
                        f"{where}: PET '{pet}' is not an implementation technique of pattern "
                        f"'{pattern_name}' ({patterns[pattern_name][0].name})"
                    )
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", type=Path, help="files or directories (default: examples/ patterns/)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()
    paths = args.paths or [p for p in (ROOT / "examples", ROOT / "patterns") if p.exists()]

    errors, warnings = validate_paths(paths)
    for w in warnings:
        print(f"WARNING {w}")
    for e in errors:
        print(f"ERROR   {e}")
    n_files = len(collect(paths))
    if errors or (args.strict and warnings):
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s) in {n_files} file(s)")
        return 1
    print(f"OK: {n_files} file(s) valid, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
