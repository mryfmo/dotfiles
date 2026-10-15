"""Run scripts/orchestrator/task-consistency-check.py and ledger-check.py as subprocesses (plan 007 T704).

Each checker runs under `uv run --no-project --with pyyaml python -I` with a stub `git` first on PATH (set inside
`uv run`, which prepends its own directories) that answers only the checks' two probes: `cat-file -e` succeeds when STUB_CAT_FILE is `present`, `grep -q` when STUB_GREP is
`found`; the subprocess pattern of tests/unit/test_orchestrator_tools.py. tests/fixtures/lessons/ holds copies from
origin/main: the front matter of the ten historical task files and the pre-fix record triple of process-rules-a05.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LESSONS = ROOT / "tests/fixtures/lessons"
GIT = "#!/usr/bin/env bash\ncase $1 in\ncat-file) [[ $STUB_CAT_FILE == present ]] ;;\ngrep) [[ $STUB_GREP == found ]] ;;\n"
GIT += "*) exit 99 ;;\nesac\n"
ROW_UNIT = "task metadata|metadata separators|in-process effects|workflow and interpreter or environment inputs"
ROW_UNIT += "|new or renamed scripts|orchestrator effect merge|orchestrator effect update-branch"
ROW_UNIT += "|orchestrator effect forced worker removal"
A05 = LESSONS / "dotfiles-T128-process-rules-a05"


class TaskCheckersTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        (self.temp / "bin").mkdir()
        (self.temp / "bin/git").write_text(GIT)
        (self.temp / "bin/git").chmod(0o755)

    def run_check(self, script, *args, code, cat_file="present", grep="found"):
        # uv run puts its environment's and its base interpreter's bin directories before PATH (on the macOS runner
        # Homebrew's, which holds a git), so the stub goes first inside uv run, right before python starts.
        stub_first = ["sh", "-c", 'PATH="$STUB_BIN:$PATH" exec python -I "$@"', "sh"]
        result = subprocess.run(
            [shutil.which("uv"), "run", "--no-project", "--with", "pyyaml", *stub_first]
            + [str(ROOT / "scripts/orchestrator" / script), *map(str, args)],
            capture_output=True,
            text=True,
            env={**os.environ, "STUB_BIN": str(self.temp / "bin"), "STUB_CAT_FILE": cat_file, "STUB_GREP": grep},
            timeout=120,
            check=False,
        )
        self.assertEqual(code, result.returncode, result.stdout + result.stderr)
        return result.stdout

    def failing_checks(self, *files, root, code=1, **stub):
        """Map each file name the check prints to the set of check ids of its finding lines."""
        found, name = {}, None
        for line in self.run_check("task-consistency-check.py", "--root", root, *files, code=code, **stub).splitlines():
            if line.startswith("  "):
                found[name].add(re.match(r"  (C\d+b?) ", line).group(1))
            else:
                name = line.split(": ")[0]
                found[name] = set()
        return found

    def task(self, tid="t-a01", kind="code", body="", allowed=("scripts/x.py",), rows=(), name=None, uncovered=()):
        """A complete task file under self.temp: one row per allowed_files entry (but `uncovered`) and ROW_UNIT name."""
        allowed = [*allowed, f".orchestration/{tid}/**"]
        controls = [f"the PR adds {a}" for a in allowed] + ROW_UNIT.split("|")
        allowed += uncovered
        table = [{"control": c, "disposition": "residual: a compensating control"} for c in controls] + list(rows)
        front = {"format": 2, "task_id": tid, "kind": kind, "allowed_files": allowed, "threat_table": table}
        front["design_review"] = {"design": "design.md", "receipt": "receipt.md"}
        (path := self.temp / f"{name or tid}.md").write_text(f"---\n{json.dumps(front)}\n---\n\n{body}\n")
        return path

    def test_task_consistency_check_detects_the_ten_historical_files(self):
        text = (LESSONS / "historical-front-matter.txt").read_text()
        blocks = re.split(r"^# (dotfiles-T128-\S+)\n", text, flags=re.MULTILINE)
        files = [self.temp / f"{tid}.md" for tid in blocks[1::2]]
        for path, block in zip(files, blocks[2::2], strict=True):
            path.write_text(block)
        c2467, c467, c23467 = {"C2", "C4", "C6", "C7"}, {"C4", "C6", "C7"}, {"C2", "C3", "C4", "C6", "C7"}
        expected = {"process-rules-a01": {"C2", "C6"}, "process-rules-a05": c467, "process-rules-a06": c467}
        expected |= dict.fromkeys(["process-rules-a02", "process-rules-a03", "process-rules-a04"], c2467)
        expected |= dict.fromkeys(["regime-counters-a01", "ci-skip-orchestration-a01"], c2467)
        expected |= dict.fromkeys(["regime-counters-a02", "ci-skip-orchestration-a02"], c23467)
        expected = {f"dotfiles-T128-{t}.md": ids for t, ids in expected.items()}
        self.assertEqual(expected, self.failing_checks(*files, root=ROOT))

    def test_task_consistency_check_passes_a_complete_task_file(self):
        design = "---\ndesign_review:\n  receipt: {}\n---\n\n# Design\n"
        (self.temp / "design.md").write_text(design.format("receipt.md"))
        path = self.task(body="The gate reads REVIEW_EVIDENCE, an input on origin/main.")
        self.assertEqual({"t-a01.md": set()}, self.failing_checks(path, root=self.temp, code=0))
        # The design resolves under --root, not the current directory: a newer receipt there is C6.
        (self.temp / "design.md").write_text(design.format("receipt-2.md"))
        self.assertEqual({"t-a01.md": {"C6"}}, self.failing_checks(path, root=self.temp))

    def test_task_consistency_check_reaches_every_other_check(self):
        two = {"allowed": ("scripts/x.py", "scripts/y.py"), "rows": [{"control": "scripts/x.py, scripts/y.py"}]}
        absent = '"the gate runs scripts/absent-tool.sh before every merge"'
        literal = '"run scripts/present.sh with `MODE=strict` before a dispatch"'
        for check, args, stub in (
            ("C1", {"name": "t-a02"}, {}),
            # C2's other branch (another task's directory); the ten reach only the missing own directory.
            ("C2", {"allowed": ("scripts/x.py", ".orchestration/t-a00/task.md")}, {}),
            ("C5", {"tid": "t-a02", "rows": [{"control": "task.md", "disposition": "names the a01 file's hash"}]}, {}),
            ("C7b", two, {}),
            ("C8", {"body": "The gate reads NEW_EVIDENCE."}, {"grep": "missing"}),
            ("C9", {"kind": "docs", "body": absent}, {"cat_file": "absent"}),
            ("C10", {"kind": "docs", "body": literal}, {"grep": "missing"}),
        ):
            with self.subTest(check=check):
                path = self.task(**args)
                self.assertIn(check, self.failing_checks(path, root=self.temp, **stub)[path.name])

    def test_task_consistency_check_c9_probes_the_landed_checker_path(self):
        # Owned row local:c1f60f7:3: `task-consistency-check C<n>` names scripts/orchestrator/task-consistency-check.py,
        # where the checker landed; a stub git that knows only that path answers present.
        (self.temp / "bin/git").write_text(
            '#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "$STUB_BIN/git.log"\n'
            "case $1 in\ncat-file) [[ $3 == origin/main:scripts/orchestrator/task-consistency-check.py ]] ;;\n"
            "grep) true ;;\n*) exit 99 ;;\nesac\n"
        )
        design = "---\ndesign_review:\n  receipt: receipt.md\n---\n\n# Design\n"
        (self.temp / "design.md").write_text(design)
        path = self.task(kind="docs", body='"every task file passes task-consistency-check C4 before its dispatch"')
        self.assertEqual({"t-a01.md": set()}, self.failing_checks(path, root=self.temp, code=0))
        probes = (self.temp / "bin/git.log").read_text().splitlines()
        self.assertIn("cat-file -e origin/main:scripts/orchestrator/task-consistency-check.py", probes)

    def ledger(self, *args, code):
        return self.run_check("ledger-check.py", *args, code=code).splitlines()

    def test_ledger_check_reports_the_gaps_of_the_pre_fix_record(self):
        out = self.ledger(f"{A05}.record.txt", f"{A05}-pr-feedback.json", f"{A05}-audit-4af8939.md.last.txt", code=1)
        self.assertEqual("ledger rows 0; findings 36; gaps 36", out[0])
        self.assertEqual(36, sum(line.startswith("GAP ") for line in out))

    def test_ledger_check_passes_a_complete_record(self):
        url = "https://github.test/pull/9#discussion_r"
        codex = {"source": "review_comment", "bot": True, "author": "chatgpt-codex-connector[bot]"}
        items = [{**codex, "url": f"{url}{n}"} for n in (4250000001, 4250000002)]
        items += [{"source": "review_comment", "bot": False, "url": f"{url}4250000003"}, {"source": "issue_comment"}]
        (sweep := self.temp / "sweep.json").write_text(json.dumps({"items": items}))
        audit = self.temp / "t-a01-audit-abcdef0.md.last.md"
        audit.write_text("[P0] high implementation x.py:1 one\n[P3] low evidence x.py:2 two\nVerdict: incorrect\n")
        rows = ["4250000001\tstale-path", "4250000002\tother", "audit:abcdef0:1\tother", "audit:abcdef0:2\tother"]
        (record := self.temp / "record.md").write_text("\n".join(["---", "{}", "---", "", *rows, ""]))
        self.assertEqual(["ledger rows 4; findings 4; gaps 0"], self.ledger(record, sweep, audit, code=0))
        record.write_text("\n".join(rows[:3]) + "\n")
        gap = ["ledger rows 3; findings 4; gaps 1", "GAP audit:abcdef0:2"]
        self.assertEqual(gap, self.ledger(record, sweep, audit, code=1))

    def test_ledger_check_counts_what_the_gate_counts(self):
        # Amendment 2: a badged Codex Bot review body and a bulleted audit line are findings, as the gate counts them;
        # an unbadged Bot review and another author's badged review are not. Owned row audit:c1f60f7:1: a Codex Bot
        # inline comment is a finding, another bot's (CodeRabbit's) is not, as the gate's swept_finding_ids() counts.
        review = {"source": "review", "author": "chatgpt-codex-connector[bot]", "body": "![P1 Badge](x) y"}
        items = [{**review, "url": "https://github.test/pull/9#pullrequestreview-5510000001"}]
        items += [{**review, "author": "o", "url": "#pullrequestreview-5510000002"}]
        items += [{**review, "body": "no badge", "url": "#pullrequestreview-5510000003"}]
        inline = {"source": "review_comment", "bot": True, "author": "chatgpt-codex-connector[bot]"}
        items += [{**inline, "url": "https://github.test/pull/9#discussion_r4250000001"}]
        items += [{**inline, "author": "coderabbitai[bot]", "url": "https://github.test/pull/9#discussion_r4250000002"}]
        (sweep := self.temp / "sweep.json").write_text(json.dumps({"items": items}))
        (audit := self.temp / "t-a01-audit-abcdef0.md.last.md").write_text("- [P1] high evidence x.py:1 one\n")
        (record := self.temp / "record.md").write_text("---\n{}\n---\n")
        gaps = ["ledger rows 0; findings 3; gaps 3", "GAP 5510000001", "GAP 4250000001", "GAP audit:abcdef0:1"]
        self.assertEqual(gaps, self.ledger(record, sweep, audit, code=1))

    def test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary(self):
        # Amendment 2: the prefix counts when the control text goes on with its end, a space, a slash, a parenthesis,
        # a quote, a comma or a glob character, and not when it goes on with more of a path.
        for after in (".bak", "", " and its test", "/task.md", ") and more", '" and more', ", and more", "* and more"):
            with self.subTest(after=after):
                path = self.task(
                    uncovered=("scripts/foo.py",), rows=[{"control": f"the PR adds scripts/foo.py{after}"}]
                )
                found = self.failing_checks(path, root=self.temp, code=1 if after == ".bak" else 0)[path.name]
                self.assertEqual({"C4"} if after == ".bak" else set(), found)


if __name__ == "__main__":
    unittest.main()
