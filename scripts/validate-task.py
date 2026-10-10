#!/usr/bin/env python3
"""Validate an agmsg task file's `format: 2` front matter (T124 INV-1, INV-2, INV-8).

Usage: validate-task.py <task file or design-reset record> [--json] [--print-design-hash]
Exit 0 when the file is valid, superseded or legacy (no `format: 2`, grandfathered);
exit 1 with one line per failure. Paths named in the front matter resolve against the
main checkout (`git rev-parse --git-common-dir`), never the caller's cwd.

A design-reset record (`.orchestration/acceptance/<task id>-design-reset.md`, keyed by
`reset_of`) is checked for its shape, its `kind: design` redesign task and the overlap with
the abandoned task. That a `-redesign-` seat's RESULT precedes the implementing TASK in agmsg
history is the gate's check from T124 wave 2b, not this script's.
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
    LOW_RISK_SUFFIXES,
    glob_regex,
    in_review_tier,
    may_touch_design_tier,
    parse_front_matter,
)

KINDS = {"code", "review", "docs", "design"}
NO_FILES_KINDS = {"review", "docs", "design"}
WAVE_FILE_LIMIT = 15
INVARIANT_ID = re.compile(r"INV-[0-9]+")
# The stop gate's rule: the orchestrator is the unsuffixed identity, every other seat carries -aNNN.
NON_ORCHESTRATOR = re.compile(r".+-a[0-9]{3}")
TASK_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
# The tier table travels with this script: main's validator reads main's manifest.
MANIFEST = Path(__file__).resolve().parents[1] / "home/dot_agents/agent-config.yaml"


def process_tiers(manifest: Path) -> dict | None:
    """The `process_tiers:` map of the manifest, read as one front-matter block (the file itself needs PyYAML)."""
    lines = manifest.read_text(encoding="utf-8").splitlines() if manifest.is_file() else []
    if "process_tiers:" not in lines:
        return None
    start = lines.index("process_tiers:")
    end = next(
        (n for n in range(start + 1, len(lines)) if lines[n][:1] not in ("", " ", "#")),
        len(lines),
    )
    block = parse_front_matter("---\n" + "\n".join(lines[start:end]) + "\n---\n") or {}
    return block.get("process_tiers") if isinstance(block.get("process_tiers"), dict) else None


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


def canonical(path: str) -> bool:
    """A repository-relative path or glob in one spelling: no leading `/`, `./`, `..`, `//` or trailing `/`."""
    return isinstance(path, str) and "\\" not in path and all(part not in ("", ".", "..") for part in path.split("/"))


def is_text_map(value) -> bool:
    return isinstance(value, dict) and all(isinstance(v, str) and v.strip() for v in value.values())


def load(path: Path) -> dict | None:
    return parse_front_matter(path.read_text(encoding="utf-8"))


def receipt_fields(path: Path) -> dict[str, list[str]]:
    """The receipt's top-level `reviewer:` and `design:` lines; its header may hold timestamps the parser refuses."""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    header = lines[1 : lines.index("---", 1)] if lines[:1] == ["---"] and "---" in lines[1:] else []
    fields = {"reviewer": [], "design": [], "verdict": []}
    for line in header:
        match = re.fullmatch(r"(reviewer|design):\s*(\S+)\s*", line)
        if match:
            fields[match.group(1)].append(match.group(2))
    fields["verdict"] = [m.group(1) for m in (re.fullmatch(r"Design verdict:\s*(\S+)\s*", line) for line in lines) if m]
    return fields


def overlaps(left: list, right: list, files: list[str]) -> bool:
    for a in left:
        for b in right:
            if a == b or glob_regex(a).match(b) or glob_regex(b).match(a) or expand(a, files) & expand(b, files):
                return True
    return False


def validate_reset(path: Path, data: dict, root: Path, files: list[str], report: dict) -> dict:
    fail, warn = report["failures"].append, report["warnings"].append
    report["record"] = "design-reset"
    fields = {key: data.get(key) for key in ("reset_of", "redesign_task", "redesign_seat", "reason")}
    for key in ("reset_of", "redesign_task"):
        if not isinstance(fields[key], str) or not TASK_ID.fullmatch(fields[key]):
            fail(f"{key}: required, a task id")
    if not isinstance(fields["redesign_seat"], str) or "-redesign-" not in fields["redesign_seat"]:
        fail(f"redesign_seat: must be an identity containing -redesign-, got {fields['redesign_seat']!r}")
    if not isinstance(fields["reason"], str) or not fields["reason"].strip():
        fail("reason: required")
    if isinstance(fields["reset_of"], str) and path.stem != f"{fields['reset_of']}-design-reset":
        fail(f"the file must be named {fields['reset_of']}-design-reset.md")
    tasks = root / ".orchestration/tasks"
    loaded = {}
    for key in ("reset_of", "redesign_task"):
        name = fields[key]
        if not isinstance(name, str) or not TASK_ID.fullmatch(name):
            continue
        try:
            loaded[key] = load(tasks / f"{name}.md") if (tasks / f"{name}.md").is_file() else None
        except (OSError, UnicodeDecodeError, FrontMatterError) as error:
            loaded[key] = None
            fail(f"{key}: {name}: {error}")
        if loaded[key] is None:
            fail(f"{key}: {tasks / name}.md is not a task file with front matter in the main checkout")
    redesign, abandoned = loaded.get("redesign_task"), loaded.get("reset_of")
    if redesign is not None and redesign.get("kind") != "design":
        fail(f"redesign_task: {fields['redesign_task']} must be `kind: design`, got {redesign.get('kind')!r}")
        redesign = None
    if redesign is not None and abandoned is not None:
        # The redesign must replace the abandoned work: its files, or its implementing tasks' files, overlap.
        new_files = list(redesign.get("allowed_files") or [])
        for task in redesign.get("implementing_tasks") or []:
            implementing = (
                load(tasks / f"{task}.md")
                if TASK_ID.fullmatch(str(task)) and (tasks / f"{task}.md").is_file()
                else None
            )
            new_files += list((implementing or {}).get("allowed_files") or [])
        if not overlaps(list(abandoned.get("allowed_files") or []), new_files, files):
            fail(f"redesign_task: {fields['redesign_task']} does not overlap the allowed files of {fields['reset_of']}")
        elif abandoned.get("superseded_by") == fields["redesign_task"]:
            report["abandoned_status"] = "superseded"
        else:
            warn(f"{fields['reset_of']} is not marked superseded_by: {fields['redesign_task']} yet")
    report["status"] = "invalid" if report["failures"] else "valid"
    return report


def validate(path: Path) -> dict:
    report = {"task_file": str(path), "status": "valid", "failures": [], "warnings": []}
    fail, warn = report["failures"].append, report["warnings"].append
    try:
        data = load(path)
    except (OSError, UnicodeDecodeError, FrontMatterError) as error:
        # An unparsable header that names any format fails; only a header without one is grandfathered.
        header = path.read_text(encoding="utf-8", errors="replace").split("\n---", 1)[0]
        if not re.search(r"""(?:^|[\s{,])["']?format["']?\s*:""", header):
            report["status"] = "legacy"
            return report
        fail(f"front matter: {error}")
        report["status"] = "invalid"
        return report
    if data is None or "format" not in data:
        report["status"] = "legacy"
        return report
    if data["format"] != 2 or isinstance(data["format"], bool):
        fail(f"format: only 2 is supported, got {data['format']!r}")
        report["status"] = "invalid"
        return report
    root = main_checkout(path.resolve())
    files = tracked_files(root)
    if path.resolve().parent == (root / ".orchestration/acceptance").resolve():
        return validate_reset(path, data, root, files, report)
    if "reset_of" in data:
        fail("reset_of: a design-reset record belongs in .orchestration/acceptance/<task id>-design-reset.md")

    task_id = data.get("task_id")
    report["task_id"] = task_id
    if not isinstance(task_id, str) or not task_id:
        fail("task_id: required")
    elif not TASK_ID.fullmatch(task_id):
        fail(f"task_id: {task_id!r} must be one path segment of letters, digits, `.`, `_` and `-`")
    elif task_id != path.stem:
        fail(f"task_id: {task_id!r} is not the file stem {path.stem!r}")
    kind = data.get("kind")
    if not isinstance(kind, str) or kind not in KINDS:
        fail(f"kind: must be one of {', '.join(sorted(KINDS))}, got {kind!r}")

    allowed = data.get("allowed_files")
    if allowed is None and isinstance(kind, str) and kind in NO_FILES_KINDS:
        allowed = []
    if not isinstance(allowed, list) or not all(isinstance(entry, str) and entry for entry in allowed):
        fail("allowed_files: required, a list of paths or globs")
        allowed = []
    unspelled = [entry for entry in allowed if not canonical(entry)]
    if unspelled:
        fail(f"allowed_files: not a canonical repository-relative path: {', '.join(unspelled)}")

    # security is derived from the design tier: declaring true ratchets up, declaring false on a match fails.
    # A glob counts when any path it can name, existing or created later, is in the design tier.
    matching = [entry for entry in allowed if may_touch_design_tier(entry)]
    declared = data.get("security")
    if declared is not None and not isinstance(declared, bool):
        fail(f"security: must be true or false, got {declared!r}")
    if declared is False and matching:
        fail(f"security: declared false, but these allowed files are in the design tier: {', '.join(matching)}")
    security = bool(matching) or declared is True
    report["security"] = security
    # The process tier (T126): design over review over docs; a path that is neither prose nor in a tier is review.
    if security:
        tier = "design"
    elif any(
        in_review_tier(e) or not e.endswith(LOW_RISK_SUFFIXES) or any(in_review_tier(n) for n in expand(e, files))
        for e in allowed
    ):
        tier = "review"
    else:
        tier = "docs"
    report["tier"] = tier
    tiers = process_tiers(MANIFEST)
    if tiers is None or not isinstance(tiers.get(tier), dict):
        fail(f"tier: {MANIFEST.name} has no process_tiers entry for {tier!r}")

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
            inside = {}
            for key in ("receipt", "design"):
                value = design_review[key]
                # Both must be files of the main checkout itself: no absolute path, `..` or symlink out of it.
                target = (root / value).resolve() if canonical(value) else None
                inside[key] = target is not None and target.is_relative_to(root.resolve()) and target.is_file()
                if not inside[key]:
                    fail(f"design_review.{key}: {value!r} is not a file inside the main checkout {root}")
            design_path = root / str(design_review["design"])
            same_file = inside["design"] and design_path.resolve() == path.resolve()
            if inside["design"]:
                try:
                    design = load(design_path)
                except (OSError, UnicodeDecodeError, FrontMatterError) as error:
                    fail(f"design_review.design: {error}")
                if same_file and kind != "design":
                    # Only a design task may name itself; anything else would review its own threat model.
                    fail("design_review.design: names this task itself; a non-design task needs a separate design task")
                    design = None
                elif design is None or design.get("format") != 2 or design.get("kind") != "design":
                    fail("design_review.design: must be a `format: 2` task file of `kind: design`")
                    design = None
            if design is not None:
                try:
                    report["design_hash"] = canonical_design_hash(design)
                except KeyError as error:
                    fail(f"design_review.design: the design task lacks {error.args[0]}")
                if not same_file:
                    # One reviewed design authorizes only the tasks it names.
                    if task_id not in (design.get("implementing_tasks") or []):
                        fail(
                            f"design_review.design: {design_review['design']} does not list {task_id} in implementing_tasks"
                        )
                    design_ids = set(design.get("invariants") or {})
                    extra = sorted(set(invariants) - design_ids)
                    if extra:
                        fail(f"invariants: not in the design {design_review['design']}: {', '.join(extra)}")
            if inside["receipt"] and "design_hash" in report:
                # The receipt binds a non-orchestrator review to the design as it is now (T124 Amendment 3).
                fields = receipt_fields(root / design_review["receipt"])
                if len(fields["design"]) != 1 or not fields["design"][0].endswith(report["design_hash"]):
                    fail(
                        f"design_review.receipt: its `design:` does not end in the design's canonical hash "
                        f"{report['design_hash']} (re-review the design after any change to its keys)"
                    )
                if len(fields["reviewer"]) != 1 or not NON_ORCHESTRATOR.fullmatch(fields["reviewer"][0]):
                    fail("design_review.receipt: its `reviewer:` must be one non-orchestrator identity (-aNNN)")
                if fields["verdict"] != ["accept"]:
                    fail(
                        f"design_review.receipt: it must carry one `Design verdict: accept` line, found {fields['verdict']}"
                    )
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
                isinstance(value, list) and value and all(isinstance(v, str) and v.strip() for v in value)
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
            listed = {}
            for name, entries in waves.items():
                for entry in entries:
                    listed.setdefault(entry, []).append(name)
            # A glob can name files created later, so only the glob itself, in exactly one wave, covers it.
            missing = [
                entry
                for entry in allowed
                if (
                    len(listed.get(entry, [])) != 1
                    if re.search(r"[*?]", entry)
                    else entry not in listed and not any(glob_regex(w).match(entry) for w in listed)
                )
            ]
            if missing:
                fail(
                    "waves: each allowed glob must appear verbatim in exactly one wave and each path in some wave: "
                    + ", ".join(missing)
                )
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
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("task_file", type=Path)
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument(
        "--print-design-hash", action="store_true", help="print the canonical hash of the design named in design_review"
    )
    parser.add_argument(
        "--print-tier", action="store_true", help="print the derived process tier (docs, review or design)"
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
        if args.print_tier and "tier" in report:
            print(report["tier"])
        if not report["failures"]:
            print(f"{args.task_file}: {report['status']}")
    if args.print_design_hash and "design_hash" not in report and not report["failures"]:
        print(f"{args.task_file}: no design_review.design to hash", file=sys.stderr)
        return 1
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
