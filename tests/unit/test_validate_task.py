#!/usr/bin/env python3
"""Exercise scripts/validate-task.py and scripts/lib/high_risk_paths.py (T124 wave 1: INV-1, INV-2, INV-8)."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validate-task.py"
GATE = ROOT / "scripts/require-crit-review.py"
sys.path.insert(0, str(ROOT / "scripts/lib"))
sys.dont_write_bytecode = True

import high_risk_paths  # noqa: E402

GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"]


def emit(value, indent: int = 0) -> str:
    """Write the YAML subset task files use."""
    pad = " " * indent
    if isinstance(value, dict):
        out = ""
        for key, item in value.items():
            if isinstance(item, (dict, list)) and item:
                out += f"{pad}{key}:\n{emit(item, indent + 2)}"
            else:
                out += f"{pad}{key}: {emit_scalar(item)}\n"
        return out
    return "".join(f"{pad}- {emit_scalar(item)}\n" for item in value)


def emit_scalar(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value == {}:
        return "{}"
    if value == []:
        return "[]"
    text = str(value)
    # Quote what YAML would read as something else, as a task author must.
    return json.dumps(text) if text[:1] in "*&!|>%@`[{'\"" or ": " in text or " #" in text else text


DESIGN = {
    "format": 2,
    "task_id": "design-a01",
    "kind": "design",
    "security": True,
    "design_review": {
        "receipt": ".orchestration/validation/receipt.md",
        "design": ".orchestration/tasks/design-a01.md",
    },
    "threat_model": {"T1": "a wrong principle reaches code"},
    "trust_anchors": ["agmsg history", "GitHub state"],
    "invariants": {"INV-1": "the gate validates the task file", "INV-2": "security derives from the design tier"},
}


def receipt(design: dict = DESIGN, reviewer: str = "claude-review-dot-a002") -> str:
    """A review receipt: its header holds a timestamp, a reviewer and the design path with its canonical hash."""
    digest = high_risk_paths.canonical_design_hash(design)
    return f"---\nreviewed_at: 2026-10-10T09:02:00Z\nreviewer: {reviewer}\ndesign: .orchestration/tasks/design-a01.md@{digest}\n---\n"


class ValidateTaskTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="validate-task-test-"))
        self.main = self.temp_dir / "main"
        self.main.mkdir()
        subprocess.run([*GIT, "init", "-q", str(self.main)], check=True)
        tracked = [
            "install/common/tool.sh",
            "setup.sh",
            "scripts/pr-feedback.py",
            "README.md",
            "home/dot_config/claude/rules/rule.md",
            *(f"many/f{n:02}.txt" for n in range(16)),
            ".orchestration/validation/receipt.md",
        ]
        for name in tracked:
            (self.main / name).parent.mkdir(parents=True, exist_ok=True)
            (self.main / name).write_text("x\n")
        self.tasks = self.main / ".orchestration/tasks"
        self.tasks.mkdir(parents=True)
        self.write("design-a01", DESIGN)
        (self.main / ".orchestration/validation/receipt.md").write_text(receipt())
        subprocess.run([*GIT, "-C", str(self.main), "add", "-A"], check=True)
        subprocess.run([*GIT, "-C", str(self.main), "commit", "-q", "-m", "c"], check=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def write(self, name: str, fields: dict | None, body: str = "# task\n", where: Path | None = None) -> Path:
        path = (where or self.tasks) / f"{name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(("" if fields is None else f"---\n{emit(fields)}---\n") + body)
        return path

    def task(self, name: str = "t-a01", **fields) -> Path:
        base = {
            "format": 2,
            "task_id": name,
            "kind": "code",
            "allowed_files": ["README.md"],
            "invariants": {"INV-1": "the gate validates the task file"},
        }
        base.update(fields)
        return self.write(name, {key: value for key, value in base.items() if value is not None})

    def security_task(self, name: str = "t-a01", **fields) -> Path:
        defaults = {"allowed_files": ["install/common/tool.sh"], "design_review": DESIGN["design_review"]}
        return self.task(name, **{**defaults, **fields})

    def run_validator(self, path: Path, *args: str, cwd: Path | None = None) -> tuple[int, dict]:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(path), "--json", *args],
            cwd=cwd or self.temp_dir,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertIn(result.returncode, (0, 1), result.stderr)
        return result.returncode, json.loads(result.stdout)

    def assertFails(self, path: Path, needle: str, *args: str) -> dict:
        code, report = self.run_validator(path, *args)
        self.assertEqual(1, code, report)
        self.assertEqual("invalid", report["status"])
        self.assertTrue(any(needle in failure for failure in report["failures"]), report["failures"])
        return report

    def assertValid(self, path: Path) -> dict:
        code, report = self.run_validator(path)
        self.assertEqual(0, code, report)
        self.assertEqual("valid", report["status"], report)
        return report

    def test_a_complete_task_and_a_complete_security_task_are_valid(self) -> None:
        self.assertFalse(self.assertValid(self.task())["security"])
        report = self.assertValid(self.security_task())
        self.assertTrue(report["security"])
        self.assertEqual(high_risk_paths.canonical_design_hash(DESIGN), report["design_hash"])

    def test_text_output_is_one_line_per_failure_and_exit_1(self) -> None:
        path = self.task(task_id="other", kind="chore")
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(path)], check=False, text=True, capture_output=True
        )
        self.assertEqual(1, result.returncode)
        self.assertEqual(2, len(result.stdout.splitlines()), result.stdout)

    def test_each_required_key_is_reported(self) -> None:
        cases = {
            "task_id": "task_id: required",
            "kind": "kind: must be one of",
            "allowed_files": "allowed_files: required",
            "invariants": "invariants: required",
        }
        for key, needle in cases.items():
            with self.subTest(key=key):
                self.assertFails(self.task(**{key: None}), needle)
        # A review, docs or design task may omit allowed_files.
        self.assertValid(self.task(kind="docs", allowed_files=None))
        self.assertValid(self.task(kind="design", allowed_files=None))
        security = {
            "design_review": "design_review: a security task needs",
            "threat_model": "threat_model: a security task needs",
            "trust_anchors": "trust_anchors: a security task needs",
        }
        for key, needle in security.items():
            with self.subTest(key=key):
                fields = {
                    "kind": "docs",
                    "allowed_files": None,
                    "security": True,
                    "design_review": DESIGN["design_review"],
                    "threat_model": DESIGN["threat_model"],
                    "trust_anchors": DESIGN["trust_anchors"],
                }
                fields[key] = None
                self.assertFails(self.task(**fields), needle)
        self.assertFails(self.security_task(invariants={}), "invariants: a security task needs at least one")

    def test_task_id_must_equal_the_file_stem(self) -> None:
        self.assertFails(self.task("t-a01", task_id="t-a02"), "is not the file stem")

    def test_security_is_derived_from_the_design_tier_only(self) -> None:
        cases = {
            "install/common/tool.sh": True,
            "setup.sh": True,
            "install/**": True,
            "**/*.sh": True,  # expands to tracked design-tier files
            "scripts/validate-task.py": True,  # a gate script, not created yet
            "scripts/pr-feedback.py": False,  # review tier only
            "README.md": False,  # prose
            "home/dot_config/claude/rules/rule.md": False,  # prose in the review tier
            ".claude/*/new.py": True,  # can create .claude/hooks/new.py although nothing matches yet
            "*.md": False,
            "many/f0*.txt": False,
        }
        for entry, security in cases.items():
            with self.subTest(entry=entry):
                if security:
                    self.assertFails(self.task(allowed_files=[entry]), "design_review: a security task needs")
                else:
                    self.assertFalse(self.assertValid(self.task(allowed_files=[entry]))["security"])

    def test_declared_false_on_a_design_tier_path_fails_and_declared_true_is_kept(self) -> None:
        self.assertFails(self.security_task(security=False), "security: declared false")
        self.assertFails(self.task(security=True), "design_review: a security task needs")
        report = self.assertValid(self.task(security=True, design_review=DESIGN["design_review"]))
        self.assertTrue(report["security"])

    def test_design_review_paths_resolve_in_the_main_checkout_not_the_cwd(self) -> None:
        worktree = self.temp_dir / "wt"
        subprocess.run([*GIT, "-C", str(self.main), "worktree", "add", "-q", "--detach", str(worktree)], check=True)
        receipt = ".orchestration/validation/only-in-the-worktree.md"
        (worktree / receipt).write_text("x\n")
        path = self.task(
            "t-a01",
            allowed_files=["install/common/tool.sh"],
            design_review={"receipt": receipt, "design": ".orchestration/tasks/design-a01.md"},
        ).rename(worktree / ".orchestration/tasks/t-a01.md")
        code, report = self.run_validator(path, cwd=worktree)
        self.assertEqual(1, code)
        self.assertTrue(any("is not a file inside the main checkout" in f for f in report["failures"]), report)
        (self.main / receipt).write_text(globals()["receipt"]())
        self.assertEqual(0, self.run_validator(path, cwd=worktree)[0])

    def test_a_code_task_takes_threat_model_and_trust_anchors_from_its_design_only(self) -> None:
        self.assertValid(self.security_task())
        bare = {**DESIGN, "task_id": "design-b01", "threat_model": None, "trust_anchors": None}
        self.write("design-b01", {key: value for key, value in bare.items() if value is not None})
        self.assertFails(
            self.security_task(
                design_review={**DESIGN["design_review"], "design": ".orchestration/tasks/design-b01.md"}
            ),
            "threat_model: a security task needs",
        )

    def test_waves_are_required_above_fifteen_files_and_must_cover_allowed_files(self) -> None:
        self.assertValid(self.task(allowed_files=[f"many/f{n:02}.txt" for n in range(15)]))
        self.assertFails(self.task(allowed_files=["many/*.txt"]), "waves: required, allowed_files expands to 16")
        partial = {"one": [f"many/f{n:02}.txt" for n in range(8)], "two": ["many/f08.txt"]}
        self.assertFails(self.task(allowed_files=["many/*.txt"], waves=partial), "waves: the union does not cover")
        # A file the task creates expands to nothing, so a wave must name it.
        full = {"one": [f"many/f{n:02}.txt" for n in range(8)], "two": [f"many/f{n:02}.txt" for n in range(8, 16)]}
        self.assertFails(
            self.task(allowed_files=["many/*.txt", "new/file.py"], waves=full),
            "union does not cover allowed_files: new/file.py",
        )
        report = self.assertValid(self.task(allowed_files=["many/*.txt"], waves=full))
        self.assertTrue(any("expands to 16 existing files" in w for w in report["warnings"]), report)

    def test_a_single_all_encompassing_wave_passes_with_a_warning(self) -> None:
        report = self.assertValid(self.task(allowed_files=["many/*.txt"], waves={"all": ["many/*.txt"]}))
        self.assertTrue(any("a single wave covers everything" in w for w in report["warnings"]), report)

    def test_invariant_ids_must_be_a_subset_of_the_design(self) -> None:
        self.assertValid(self.security_task(invariants={"INV-2": "security derives from the design tier"}))
        self.assertFails(
            self.security_task(invariants={"INV-1": "x", "INV-7": "added after the review"}), "not in the design"
        )
        self.assertFails(self.task(invariants={"rule-1": "x"}), "ids must look like INV-n")

    def test_the_canonical_design_hash_ignores_key_order_and_layout_and_tracks_sentences(self) -> None:
        reordered = {key: DESIGN[key] for key in reversed(list(DESIGN))}
        reordered["invariants"] = {k: DESIGN["invariants"][k] for k in reversed(list(DESIGN["invariants"]))}
        self.assertEqual(
            high_risk_paths.canonical_design_hash(DESIGN), high_risk_paths.canonical_design_hash(reordered)
        )
        spaced = "---\n" + emit(reordered).replace(": ", ":   ").replace("\n", "\n\n") + "---\n"
        self.assertEqual(DESIGN, high_risk_paths.parse_front_matter(spaced))
        (self.tasks / "design-a01.md").write_text(spaced)
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(self.tasks / "design-a01.md"), "--print-design-hash"],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn(high_risk_paths.canonical_design_hash(DESIGN), result.stdout.splitlines())
        changed = {**DESIGN, "invariants": {**DESIGN["invariants"], "INV-2": "security derives from any path"}}
        self.assertNotEqual(
            high_risk_paths.canonical_design_hash(DESIGN), high_risk_paths.canonical_design_hash(changed)
        )
        with self.assertRaises(KeyError):
            high_risk_paths.canonical_design_hash({"invariants": {}})

    def test_legacy_files_are_grandfathered(self) -> None:
        for fields, body in (
            (None, "# AGMSG-TASK old\n"),
            ({"task_id": "old", "created": "'2026-09-26'"}, "# old\n"),
        ):
            with self.subTest(fields=fields):
                code, report = self.run_validator(self.write("old", fields, body))
                self.assertEqual((0, "legacy"), (code, report["status"]))
        unparsable = self.tasks / "old.md"
        unparsable.write_text("---\ncreated: 2026-09-26T01:55:00Z\n---\n")
        self.assertEqual((0, "legacy"), (lambda r: (r[0], r[1]["status"]))(self.run_validator(unparsable)))
        unparsable.write_text("---\nformat: 2\ncreated: 2026-09-26T01:55:00Z\n---\n")
        self.assertFails(unparsable, "ambiguous plain scalar")

    def test_the_front_matter_parser_refuses_what_it_cannot_read_exactly(self) -> None:
        for text in (
            "---\nformat: 2\nlist: [a, b]\n---\n",
            "---\nformat: 2\nnote: a: b\n---\n",
            "---\nformat: 2\nnote: see PR #312\n---\n",
            "---\nformat: 2\nflag: yes\n---\n",
            "---\nformat: 2\nformat: 2\n---\n",
            "---\nformat: 2\n",
            "---\nformat: 2\nnote: 'it's risky'\n---\n",
        ):
            with self.subTest(text=text):
                with self.assertRaises(high_risk_paths.FrontMatterError):
                    high_risk_paths.parse_front_matter(text)
        self.assertEqual(
            {"a": "x: y", "b": "it's", "c": [1, True, None]},
            high_risk_paths.parse_front_matter("---\na: \"x: y\"\nb: 'it''s'\nc:\n  - 1\n  - true\n  - null\n---\n"),
        )

    def test_superseded_by_marks_the_task_superseded(self) -> None:
        code, report = self.run_validator(self.task(superseded_by="t-a02"))
        self.assertEqual((0, "superseded"), (code, report["status"]))
        self.assertFails(self.task(superseded_by="not a task id"), "superseded_by: must be a task id")

    def test_task_id_must_be_one_safe_path_segment(self) -> None:
        self.assertFails(self.task("bad id", task_id="bad id"), "must be one path segment")

    def test_allowed_files_must_be_canonical_repository_paths(self) -> None:
        # `./install/...` would neither match the design tier nor expand, so a security task could hide.
        for entry in ("./install/common/tool.sh", "install/", "/etc/passwd", "many/../install/common/tool.sh", "a//b"):
            with self.subTest(entry=entry):
                self.assertFails(self.task(allowed_files=[entry]), "not a canonical repository-relative path")

    def test_design_review_paths_must_stay_inside_the_main_checkout(self) -> None:
        outside = self.temp_dir / "outside.md"
        outside.write_text("x\n")
        (self.main / ".orchestration/validation/link.md").symlink_to(outside)
        for receipt in (str(outside), "../outside.md", ".orchestration/validation/link.md"):
            with self.subTest(receipt=receipt):
                self.assertFails(
                    self.security_task(design_review={**DESIGN["design_review"], "receipt": receipt}),
                    "is not a file inside the main checkout",
                )

    def test_the_design_must_be_a_separate_design_task(self) -> None:
        self.assertValid(self.tasks / "design-a01.md")  # a design task names itself
        own = {
            "design_review": {**DESIGN["design_review"], "design": ".orchestration/tasks/t-a01.md"},
            "threat_model": DESIGN["threat_model"],
            "trust_anchors": DESIGN["trust_anchors"],
        }
        self.assertFails(self.security_task(**own), "names this task itself")
        self.write("code-a01", {**DESIGN, "task_id": "code-a01", "kind": "code", "allowed_files": ["README.md"]})
        (self.tasks / "plain-a01.md").write_text("# no front matter\n")
        for design in ("code-a01", "plain-a01"):
            with self.subTest(design=design):
                self.assertFails(
                    self.security_task(
                        design_review={**DESIGN["design_review"], "design": f".orchestration/tasks/{design}.md"}
                    ),
                    "must be a `format: 2` task file of `kind: design`",
                )

    def test_security_must_be_a_boolean(self) -> None:
        # `security: 1` equals True in Python but must not pass as a declaration.
        self.assertFails(self.task(security=1), "security: must be true or false")

    def test_any_format_other_than_2_fails_closed(self) -> None:
        self.assertFails(self.task(format="'2'"), "format: only 2 is supported")
        self.assertFails(self.task(format=3), "format: only 2 is supported")
        commented = self.tasks / "c-a01.md"
        commented.write_text("---\nformat: 2 # current schema\ntask_id: c-a01\n---\n")
        self.assertFails(commented, "front matter:")
        commented.write_text('---\n"format": 2\ntask_id: c-a01\n---\n')
        self.assertFails(commented, "front matter:")

    def test_a_non_string_kind_is_a_failure_in_the_report(self) -> None:
        self.assertFails(self.task(kind=[]), "kind: must be one of")

    def test_the_receipt_binds_a_non_orchestrator_review_to_the_current_design(self) -> None:
        path = self.tasks.parent / "validation/receipt.md"
        self.assertValid(self.security_task())
        for text, needle in (
            (receipt(reviewer="claude-deep-dot"), "must be one non-orchestrator identity"),  # the orchestrator itself
            ("---\nreviewer: claude-review-dot-a002\n---\n", "does not end in the design's canonical hash"),
            ("x\n", "does not end in the design's canonical hash"),
        ):
            with self.subTest(text=text):
                path.write_text(text)
                self.assertFails(self.security_task(), needle)
        # Gaming path: the design changes after its review, so the receipt's hash no longer matches.
        path.write_text(receipt())
        changed = {**DESIGN, "threat_model": {"T1": "a narrower threat, added after the review"}}
        self.write("design-a01", changed)
        self.assertFails(self.security_task(), "does not end in the design's canonical hash")

    def reset_fixture(self, **fields) -> Path:
        self.task("old-a01", allowed_files=["install/common/tool.sh"], superseded_by="redesign-a01")
        redesign = {**DESIGN, "task_id": "redesign-a01", "allowed_files": ["install/**"]}
        self.write("redesign-a01", redesign)
        record = {
            "format": 2,
            "reset_of": "old-a01",
            "redesign_task": "redesign-a01",
            "redesign_seat": "claude-redesign-dot-a003",
            "reason": "two revise rounds with implementation findings",
        }
        record.update(fields)
        return self.write(
            "old-a01-design-reset",
            {k: v for k, v in record.items() if v is not None},
            where=self.main / ".orchestration/acceptance",
        )

    def test_a_design_reset_record_names_a_redesign_seat_and_an_overlapping_design_task(self) -> None:
        code, report = self.run_validator(self.reset_fixture())
        self.assertEqual((0, "valid", "superseded"), (code, report["status"], report.get("abandoned_status")), report)
        self.assertFails(
            self.reset_fixture(redesign_seat="claude-deep-dot"), "must be an identity containing -redesign-"
        )
        self.assertFails(self.reset_fixture(redesign_task="missing-a01"), "is not a task file with front matter")
        self.write("code-a01", {**DESIGN, "task_id": "code-a01", "kind": "code", "allowed_files": ["install/**"]})
        self.assertFails(self.reset_fixture(redesign_task="code-a01"), "must be `kind: design`")
        self.assertFails(self.reset_fixture(reason=None), "reason: required")

    def test_a_design_reset_must_overlap_the_abandoned_task(self) -> None:
        path = self.reset_fixture()
        self.write("redesign-a01", {**DESIGN, "task_id": "redesign-a01", "allowed_files": ["README.md"]})
        self.assertFails(path, "does not overlap the allowed files of old-a01")
        # The implementing tasks a design names count toward the overlap.
        self.task("impl-a01", allowed_files=["install/common/tool.sh"])
        self.write(
            "redesign-a01",
            {**DESIGN, "task_id": "redesign-a01", "allowed_files": ["README.md"], "implementing_tasks": ["impl-a01"]},
        )
        self.assertEqual(0, self.run_validator(path)[0])
        # Without superseded_by on the abandoned task the record is valid but says so.
        self.task("old-a01", allowed_files=["install/common/tool.sh"])
        code, report = self.run_validator(path)
        self.assertEqual(0, code)
        self.assertTrue(any("is not marked superseded_by" in w for w in report["warnings"]), report)

    def test_the_module_review_tier_equals_the_gate_constants(self) -> None:
        # Until wave 2a switches the gate to the import, the copy must not drift.
        spec = importlib.util.spec_from_file_location("require_crit_review", GATE)
        gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gate)
        for name in ("HIGH_RISK_PREFIXES", "HIGH_RISK_FILES", "HIGH_RISK_TOKENS"):
            with self.subTest(name=name):
                self.assertEqual(getattr(gate, name), getattr(high_risk_paths, name))

    def test_the_design_tier_is_explicit_paths_and_globs(self) -> None:
        self.assertTrue(high_risk_paths.in_design_tier("install/ubuntu/common/aws_cli.sh"))
        self.assertTrue(high_risk_paths.in_design_tier("home/dot_codex/rules/x.toml"))
        self.assertTrue(high_risk_paths.in_design_tier("scripts/gh-auth.sh"))
        for path in (
            "scripts/lib/high_risk_paths.py",
            "scripts/generate-agent-configs.py",
            ".claude/settings.json",
            ".claude/contextdb/contextdb/store.py",
            "home/dot_local/bin/common/executable_provision-machine-key",
            "home/dot_local/bin/common/executable_setup-gpg",
            "home/dot_local/bin/common/executable_agmsg-dispatch",
        ):
            with self.subTest(path=path):
                self.assertTrue(high_risk_paths.in_design_tier(path))
        self.assertFalse(high_risk_paths.in_design_tier("scripts/pr-feedback.py"))
        self.assertFalse(high_risk_paths.in_design_tier("installer/x.sh"))
        self.assertFalse(high_risk_paths.in_design_tier("home/dot_claude/settings.json"))
        self.assertTrue(high_risk_paths.glob_regex("a/**/b.sh").match("a/b.sh"))
        self.assertFalse(high_risk_paths.glob_regex("a/*.sh").match("a/x/b.sh"))


if __name__ == "__main__":
    unittest.main()
