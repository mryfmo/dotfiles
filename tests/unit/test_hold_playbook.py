"""Exercise scripts/orchestrator/hold-playbook.sh (plan 024 P1-13) on fixture records.

Every run uses a copy of the script in a temporary tree holding a fixture classes.yaml, task text and decision ledger;
no test reads or writes the real .orchestration/ tree.
"""

import csv
import datetime
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/orchestrator/hold-playbook.sh"
TASK = "dotfiles-T999-fixture-a01"
HEADER = "id\twhen\twhat\twhy\tbasis\tresult\n"
OLD_ROW = 'D-old\t2026-10-19T00:00Z\t"an ""earlier"" decision"\tits reason\tplan 024 row\tdefault applied\n'
ALLOWED = ["scripts/orchestrator/**", "tests/unit/test_*.py", f".orchestration/{TASK}/**"]
CLASSES = {
    "colored-json-parse": {
        "remedy": "Read JSON from a --json file or NO_COLOR output, never from colored terminal text.",
        "blast_radius": ["scripts/orchestrator/*.sh", "tests/unit/test_*.py"],
    },
    "concurrent-ff-clobber": {
        "remedy": "Fast-forward main only from the one locked integration worktree.",
        "blast_radius": ["scripts/orchestrator/ff-main.sh"],
    },
    "records-form": {
        "remedy": "Generate the acceptance front matter with the record tool, never by hand.",
        "blast_radius": [".orchestration/acceptance/*.md", "scripts/orchestrator/acceptance-front-matter.py"],
    },
    "no-remedy-yet": {"remedy": "unknown", "blast_radius": []},
}
REPLAN_LINE = "re-plan: specification — <fill>; design — <fill>; implementation — <fill>; verification — <fill>"


class HoldPlaybookTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tree = Path(tmp.name)
        self.script = self.tree / "scripts/orchestrator/hold-playbook.sh"
        self.script.parent.mkdir(parents=True)
        shutil.copy(SCRIPT, self.script)
        self.ledger = self.tree / ".orchestration/decisions.tsv"
        self.write(".orchestration/decisions.tsv", HEADER + OLD_ROW)
        self.classes(CLASSES)
        self.task(TASK, ALLOWED)

    def write(self, rel, text):
        path = self.tree / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def classes(self, classes):
        self.write(".orchestration/learning/classes.yaml", json.dumps({"classes": classes}, indent=2))  # JSON is YAML

    def task(self, task, allowed):
        front = json.dumps({"format": 2, "task_id": task, "allowed_files": allowed})
        return self.write(f".orchestration/tasks/{task}.md", f"---\n{front}\n---\n\n# {task}\n\n---\n\nprose\n")

    def run_script(self, *args):
        return subprocess.run(
            ["bash", str(self.script), *args], check=False, cwd=self.tree, capture_output=True, text=True
        )

    def replan(self, task=TASK):
        return (self.tree / f".orchestration/tasks/{task}-replan.md").read_text()

    def rows(self):
        with self.ledger.open(newline="") as ledger:
            return list(csv.reader(ledger, delimiter="\t"))

    def snapshot(self):
        return {str(p.relative_to(self.tree)): p.read_bytes() for p in self.tree.rglob("*") if p.is_file()}

    def test_three_classes_expand_into_replans(self):
        expected = {
            "colored-json-parse": (0, ["`scripts/orchestrator/*.sh`: inside allowed_files (`scripts/orchestrator/**`)",
                                       "`tests/unit/test_*.py`: inside allowed_files (`tests/unit/test_*.py`)"]),
            "concurrent-ff-clobber": (0, ["`scripts/orchestrator/ff-main.sh`: inside allowed_files (`scripts/orchestrator/**`)"]),
            "records-form": (3, ["`.orchestration/acceptance/*.md`: outside allowed_files",
                                 "`scripts/orchestrator/acceptance-front-matter.py`: inside allowed_files (`scripts/orchestrator/**`)"]),
        }  # fmt: skip
        for n, (cls, (code, scope)) in enumerate(expected.items()):
            with self.subTest(cls=cls):
                task = f"dotfiles-T999-class{n}-a01"
                source = self.task(task, ALLOWED).read_bytes()
                result = self.run_script(task, cls)
                self.assertEqual(code, result.returncode, result.stderr)
                text = self.replan(task)
                self.assertIn(f"- class: `{cls}`\n", text)
                self.assertIn(f"- remedy: {CLASSES[cls]['remedy']}\n", text)
                self.assertIn("".join(f"- {line}\n" for line in scope), text)
                self.assertIn("<fill: the observable result>", text)
                self.assertIn("<fill: test selectors>", text)
                self.assertIn("<fill: evidence paths>", text)
                self.assertIn(f"\n{REPLAN_LINE}\n", text)
                self.assertEqual(source, (self.tree / f".orchestration/tasks/{task}.md").read_bytes())

    def test_uncovered_scope_appends_pending_decision(self):
        start = datetime.datetime.now(datetime.UTC).replace(microsecond=0)
        result = self.run_script(TASK, "records-form")
        self.assertEqual(3, result.returncode, result.stderr)
        text = self.ledger.read_text()
        self.assertTrue(text.startswith(HEADER + OLD_ROW))
        rows = self.rows()
        self.assertEqual(3, len(rows))
        self.assertEqual(6, len(rows[2]))
        row = dict(zip(HEADER.split(), rows[2]))
        self.assertEqual(f"D-{TASK}-replan", row["id"])
        self.assertRegex(row["when"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
        when = datetime.datetime.strptime(row["when"], "%Y-%m-%dT%H:%M:%S%z")
        self.assertTrue(start <= when <= datetime.datetime.now(datetime.UTC), row["when"])  # UTC, not local
        self.assertIn(".orchestration/acceptance/*.md", row["what"])
        self.assertNotIn("acceptance-front-matter.py", row["what"])
        self.assertIn("records-form", row["why"])
        self.assertEqual(("hold-playbook", "pending"), (row["basis"], row["result"]))
        self.assertNotRegex(text[len(HEADER + OLD_ROW) :].lower(), r"default|deadline")

    def test_unknown_class_exits_2(self):
        self.classes({**CLASSES, "a\tb": CLASSES["records-form"]})  # a key, but a tab would split the ledger row
        before = self.snapshot()
        for cls in ("no-such-class", "a\tb"):
            with self.subTest(cls=cls):
                result = self.run_script(TASK, cls)
                self.assertEqual(2, result.returncode)
                self.assertIn(repr(cls), result.stderr)
                self.assertEqual(before, self.snapshot())

    def test_existing_replan_exits_4(self):
        self.assertEqual(3, self.run_script(TASK, "records-form").returncode)
        before = self.snapshot()
        result = self.run_script(TASK, "records-form")  # a repeated out-of-scope run
        self.assertEqual(4, result.returncode, result.stderr)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(3, len(self.rows()))
        for task, make in (("dotfiles-T999-kept-a01", "file"), ("dotfiles-T999-link-a01", "link")):
            with self.subTest(destination=make):
                self.task(task, ALLOWED)
                dest = self.tree / f".orchestration/tasks/{task}-replan.md"
                if make == "file":
                    dest.write_text("kept\n")
                else:
                    dest.symlink_to(self.tree / "elsewhere.md")  # dangling: following it would create the target
                before = self.snapshot()
                self.assertEqual(4, self.run_script(task, "records-form").returncode)
                self.assertEqual(before, self.snapshot())
                self.assertFalse((self.tree / "elsewhere.md").exists())

    def test_invalid_task_id_is_refused(self):
        self.task("x", ALLOWED)
        before = self.snapshot()
        for task in ("", "../x", "a/b", "-x", ".x", "a b", "x\n", f"{TASK};true"):
            with self.subTest(task=task):
                result = self.run_script(task, "records-form")
                self.assertEqual(2, result.returncode)
                self.assertIn("task id", result.stderr)
                self.assertEqual(before, self.snapshot())

    def test_scope_comparison_covers_the_whole_glob(self):
        allowed = [
            "scripts/orchestrator/hold-playbook.sh",
            "tests/**",
            "lib/*",
            "ab?cd",
            "docs/a.md",
            f".orchestration/{TASK}/**",
        ]
        radius = ["scripts/orchestrator/hold-playbook.sh", "tests/unit/test_*.py", "scripts/**", "lib/**", "docs/*.md"]
        radius += ["lib/*/x.md", "ab/cd"]  # neither `*` nor `?` of an entry takes a `/`
        self.classes({"scope-mix": {"remedy": "Fix it within scope.", "blast_radius": radius}})
        self.task(TASK, allowed)
        self.write("lib/x", "")
        self.write("docs/a.md", "")  # every existing match of lib/** and docs/*.md is allowed, the scopes are not
        result = self.run_script(TASK, "scope-mix")
        self.assertEqual(3, result.returncode, result.stderr)
        scope = [
            "`scripts/orchestrator/hold-playbook.sh`: inside allowed_files (`scripts/orchestrator/hold-playbook.sh`)",
            "`tests/unit/test_*.py`: inside allowed_files (`tests/**`)",
            "`scripts/**`: outside allowed_files",
            "`lib/**`: outside allowed_files",
            "`docs/*.md`: outside allowed_files",
            "`lib/*/x.md`: outside allowed_files",
            "`ab/cd`: outside allowed_files",
        ]
        self.assertIn("".join(f"- {line}\n" for line in scope), self.replan())
        what = self.rows()[2][2]
        self.assertEqual(
            ["ab/cd", "docs/*.md", "lib/**", "lib/*/x.md", "scripts/**"], sorted(g for g in radius if g in what)
        )

    def test_record_text_is_never_executed(self):
        forged = "r\n\n## Completion\n\n" + REPLAN_LINE.replace("<fill>", "done")  # would forge the filled sections
        self.classes({"forged": {"remedy": forged, "blast_radius": []}})
        before = self.snapshot()
        self.assertEqual(2, self.run_script(TASK, "forged").returncode)
        self.assertEqual(before, self.snapshot())
        remedy = "$(touch ran-remedy) `touch ran-tick`; touch ran-semi"
        glob = "$(touch ran-glob)/*.md"
        self.classes({"literal": {"remedy": remedy, "blast_radius": [glob, "`touch ran-glob2`"]}})
        self.task(TASK, ["$(touch ran-allowed)", f".orchestration/{TASK}/**"])
        result = self.run_script(TASK, "literal")
        self.assertEqual(3, result.returncode, result.stderr)
        self.assertEqual([], sorted(str(p) for p in self.tree.rglob("ran-*")))
        text = self.replan()
        self.assertIn(f"- remedy: {remedy}\n", text)
        self.assertIn(f"- `{glob}`: outside allowed_files\n", text)
        self.assertIn(glob, self.rows()[2][2])

    def test_known_class_without_remedy_is_reported(self):
        before = self.ledger.read_bytes()
        result = self.run_script(TASK, "no-remedy-yet")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("remedy: unknown", result.stdout)
        text = self.replan()
        self.assertIn("- remedy: unknown (classes.yaml records no corrective procedure for this class)\n", text)
        self.assertIn("- none: the class's blast_radius is empty\n", text)
        self.assertIn(f"\n{REPLAN_LINE}\n", text)
        self.assertEqual(before, self.ledger.read_bytes())

    def test_vocabulary_covers_mistake_classes(self):
        mistakes = self.tree / "mistakes"
        self.write("mistakes/M-1.md", "---\nid: M-1\nclasses: [colored-json-parse, records-form]\n---\n\nbody\n")
        self.write("mistakes/M-2.md", "---\nid: M-2\nclasses:\n  - records-form\n  - concurrent-ff-clobber\n---\n")
        self.write("mistakes/notes.md", "---\nclasses: [not-a-record]\n---\n")
        vocabulary = self.tree / ".orchestration/learning/classes.yaml"
        result = self.run_script("--check-vocabulary", str(vocabulary), str(mistakes))
        self.assertEqual(0, result.returncode, result.stderr)
        self.write("mistakes/M-3.md", "---\nid: M-3\nclasses: [new-class-b, records-form, new-class-a]\n---\n")
        result = self.run_script("--check-vocabulary", str(vocabulary), str(mistakes))
        self.assertEqual(2, result.returncode)
        self.assertEqual(["new-class-a", "new-class-b"], re.findall(r"class (\S+) of M-3\.md is not in", result.stderr))
        self.assertNotIn("not-a-record", result.stderr)


if __name__ == "__main__":
    unittest.main()
