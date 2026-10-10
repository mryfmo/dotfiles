#!/usr/bin/env python3
"""Validate an agmsg task file's `format: 2` front matter (T124 INV-1, INV-2, INV-8).

Usage: validate-task.py <task file> [--json] [--print-design-hash]
Exit 0 when the file is valid, superseded or legacy (no `format: 2`, grandfathered);
exit 1 with one line per failure. Paths named in the front matter resolve against the
main checkout (`git rev-parse --git-common-dir`), never the caller's cwd.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
sys.dont_write_bytecode = True

from high_risk_paths import (  # noqa: E402
    FrontMatterError,
    canonical_design_hash,
    glob_regex,
    in_design_tier,
    parse_front_matter,
)

KINDS = {"code", "review", "docs", "design"}
NO_FILES_KINDS = {"review", "docs", "design"}
WAVE_FILE_LIMIT = 15
INVARIANT_ID = re.compile(r"INV-[0-9]+")
TASK_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def main_checkout(path: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(path.parent), "rev-parse", "--path-format=absolute", "--git-common-dir"],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise SystemExit(f"validate-task: {path} is not inside a git checkout")
    return Path(result.stdout.strip()).parent


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], check=False, capture_output=True)
    return [name for name in result.stdout.decode().split("\0") if name] if result.returncode == 0 else []


def expand(entry: str, files: list[str]) -> set[str]:
    pattern = glob_regex(entry)
    return {name for name in files if pattern.match(name)}


def is_text_map(value) -> bool:
    return isinstance(value, dict) and all(isinstance(v, str) and v.strip() for v in value.values())


def load(path: Path) -> dict | None:
    return parse_front_matter(path.read_text(encoding="utf-8"))


def validate(path: Path) -> dict:
    report = {"task_file": str(path), "status": "valid", "failures": [], "warnings": []}
    fail, warn = report["failures"].append, report["warnings"].append
    try:
        data = load(path)
    except (OSError, UnicodeDecodeError, FrontMatterError) as error:
        # An unparsable header is a failure only when it claims format 2; older headers stay grandfathered.
        header = path.read_text(encoding="utf-8", errors="replace").split("\n---", 1)[0]
        if not re.search(r"^format:\s*['\"]?2['\"]?\s*$", header, re.M):
            report["status"] = "legacy"
            return report
        fail(f"front matter: {error}")
        report["status"] = "invalid"
        return report
    if data is None or data.get("format") != 2:
        report["status"] = "legacy"
        return report
    root = main_checkout(path.resolve())
    files = tracked_files(root)

    task_id = data.get("task_id")
    report["task_id"] = task_id
    if not isinstance(task_id, str) or not task_id:
        fail("task_id: required")
    elif task_id != path.stem:
        fail(f"task_id: {task_id!r} is not the file stem {path.stem!r}")
    kind = data.get("kind")
    if kind not in KINDS:
        fail(f"kind: must be one of {', '.join(sorted(KINDS))}, got {kind!r}")

    allowed = data.get("allowed_files")
    if allowed is None and kind in NO_FILES_KINDS:
        allowed = []
    if not isinstance(allowed, list) or not all(isinstance(entry, str) and entry for entry in allowed):
        fail("allowed_files: required, a list of paths or globs")
        allowed = []

    # security is derived from the design tier: declaring true ratchets up, declaring false on a match fails.
    matching = [e for e in allowed if in_design_tier(e) or any(in_design_tier(n) for n in expand(e, files))]
    declared = data.get("security")
    if declared not in (None, True, False):
        fail(f"security: must be true or false, got {declared!r}")
    if declared is False and matching:
        fail(f"security: declared false, but these allowed files are in the design tier: {', '.join(matching)}")
    security = bool(matching) or declared is True
    report["security"] = security

    invariants = data.get("invariants")
    if not isinstance(invariants, dict) or not is_text_map(invariants):
        fail("invariants: required, a map of `INV-n: sentence`")
        invariants = {}
    bad_ids = [key for key in invariants if not INVARIANT_ID.fullmatch(key)]
    if bad_ids:
        fail(f"invariants: ids must look like INV-n: {', '.join(bad_ids)}")
    if security and not invariants:
        fail("invariants: a security task needs at least one")

    design_review = data.get("design_review")
    design = None
    if design_review is not None:
        if not isinstance(design_review, dict) or set(design_review) != {"receipt", "design"}:
            fail("design_review: must be a map with exactly `receipt` and `design`")
        else:
            for key in ("receipt", "design"):
                value = design_review[key]
                if not isinstance(value, str) or not (root / value).is_file():
                    fail(f"design_review.{key}: {value!r} does not exist in the main checkout {root}")
            design_path = root / str(design_review["design"])
            if design_path.is_file():
                try:
                    design = load(design_path)
                except (OSError, UnicodeDecodeError, FrontMatterError) as error:
                    fail(f"design_review.design: {error}")
                if design is not None and design.get("format") != 2 and design_path.resolve() != path.resolve():
                    fail("design_review.design: the design task has no `format: 2` front matter")
                    design = None
            if design is not None:
                try:
                    report["design_hash"] = canonical_design_hash(design)
                except KeyError as error:
                    fail(f"design_review.design: the design task lacks {error.args[0]}")
                if design_path.resolve() != path.resolve():
                    design_ids = set(design.get("invariants") or {})
                    extra = sorted(set(invariants) - design_ids)
                    if extra:
                        fail(f"invariants: not in the design {design_review['design']}: {', '.join(extra)}")
    elif security:
        fail("design_review: a security task needs {receipt, design}")

    if security:
        # A code task may take its threat model and trust anchors from the design it names.
        source = design if kind == "code" and design is not None else data
        for key in ("threat_model", "trust_anchors"):
            value = data.get(key, source.get(key))
            if key == "threat_model" and not (isinstance(value, dict) and value and is_text_map(value)):
                fail(
                    "threat_model: a security task needs a map of threats (or, for a code task, a design that has one)"
                )
            if key == "trust_anchors" and not (
                isinstance(value, list) and value and all(isinstance(v, str) for v in value)
            ):
                fail("trust_anchors: a security task needs a list (or, for a code task, a design that has one)")

    expanded = set()
    for entry in allowed:
        expanded |= expand(entry, files)
    waves = data.get("waves")
    if waves is not None:
        if (
            not isinstance(waves, dict)
            or not waves
            or not all(isinstance(v, list) and v and all(isinstance(e, str) for e in v) for v in waves.values())
        ):
            fail("waves: must map each wave name to a list of files")
        else:
            covered = set()
            for entries in waves.values():
                for entry in entries:
                    covered |= expand(entry, files) | {entry}
            missing = sorted((expanded - covered) | {e for e in allowed if not expand(e, files) and e not in covered})
            if missing:
                fail(f"waves: the union does not cover allowed_files: {', '.join(missing)}")
            if len(waves) == 1:
                warn("waves: a single wave covers everything; the gate admits a PR only within one wave")
    if len(expanded) > WAVE_FILE_LIMIT:
        if waves is None:
            fail(f"waves: required, allowed_files expands to {len(expanded)} existing files (limit {WAVE_FILE_LIMIT})")
        else:
            warn(f"allowed_files expands to {len(expanded)} existing files (limit {WAVE_FILE_LIMIT} per PR)")

    superseded_by = data.get("superseded_by")
    if superseded_by is not None:
        if not isinstance(superseded_by, str) or not TASK_ID.fullmatch(superseded_by):
            fail(f"superseded_by: must be a task id, got {superseded_by!r}")
        elif not report["failures"]:
            report["status"] = "superseded"
    if report["failures"]:
        report["status"] = "invalid"
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("task_file", type=Path)
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument(
        "--print-design-hash", action="store_true", help="print the canonical hash of the design named in design_review"
    )
    args = parser.parse_args()
    if not args.task_file.is_file():
        print(f"validate-task: {args.task_file}: no such file", file=sys.stderr)
        return 1
    report = validate(args.task_file)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for failure in report["failures"]:
            print(f"{args.task_file}: {failure}")
        for warning in report["warnings"]:
            print(f"{args.task_file}: warning: {warning}")
        if args.print_design_hash and "design_hash" in report:
            print(report["design_hash"])
        if not report["failures"]:
            print(f"{args.task_file}: {report['status']}")
    if args.print_design_hash and "design_hash" not in report and not report["failures"]:
        print(f"{args.task_file}: no design_review.design to hash", file=sys.stderr)
        return 1
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
