"""Exercise audit-pool.sh, orch-audit.sh's json mode, .schemas/audit.json and .schemas/classes.yaml in a temporary repository.

Fakes on PATH: codex (answers `$CALLS/message-<task>`; a 429 while `$CALLS/fail-<task>` counts down), sleep, and uv
(runs this interpreter). No model, sleep or network is reached."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UV = f'#!/usr/bin/env bash\nshift\nwhile [[ $1 == --* ]]; do [[ $1 == --with ]] && shift; shift; done\n[[ $1 == python ]] && shift\nexec "{sys.executable}" "$@"\n'
CODEX = """#!/usr/bin/env bash
task=$(grep -o 'Audit task [^ ]*' <<< "$*" | cut -d' ' -f3)
printf '%s\\n' "$*" >> "$CALLS/codex.log"
while (($#)); do [[ $1 == -o ]] && out=$2; shift; done
n=$(cat "$CALLS/fail-$task" 2> /dev/null || echo 0)
if ((n > 0)); then echo $((n - 1)) > "$CALLS/fail-$task"; echo "error: 429 Too Many Requests"; exit 1; fi
cp "$CALLS/message-$task" "$out"
"""
SLEEP = '#!/usr/bin/env bash\necho "$1" >> "$CALLS/sleep.log"\n'
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


def record(head, task, verdict="correct", cls="string-form-comparison"):
    finding = {
        "id": "1",
        "priority": "P2",
        "confidence": "high",
        "file": "a.sh",
        "line": 3,
        "class": cls,
        "scope": "code",
    }
    meta = {"head": head, "task_id": task, "auditor": "codex --profile audit", "generated_at": "2026-10-18T05:00:00Z"}
    return meta | {
        "verdict": verdict,
        "findings": [finding | {"rationale": "a path by its string form", "status": "new"}],
    }


def message(doc, verdict=None):
    return f"[P2] high implementation a.sh:3 x\n```json\n{json.dumps(doc)}\n```\nVerdict: {verdict or doc['verdict']}\n"


class AuditPoolTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo, self.calls, bin_dir = self.temp / "repo", self.temp / "calls", self.temp / "bin"
        for d in (self.repo / "scripts/orchestrator", self.calls, bin_dir):
            d.mkdir(parents=True)
        for name in ("orch-audit.sh", "audit-pool.sh"):
            shutil.copy(ROOT / "scripts/orchestrator" / name, self.repo / "scripts/orchestrator")
        shutil.copytree(ROOT / ".schemas", self.repo / ".schemas")
        (self.repo / "scripts/orchestrator/ledger-check.py").write_text("print('ledger ok')\n")
        (self.repo / "scripts/validate-agent-assets.py").write_text("")
        for name, text in (("uv", UV), ("codex", CODEX), ("sleep", SLEEP)):
            (bin_dir / name).write_text(text)
            (bin_dir / name).chmod(0o755)
        path, origin = f"{bin_dir}{os.pathsep}{os.environ['PATH']}", str(self.temp / "origin.git")
        self.env = {**os.environ, **GIT_ENV, "CALLS": str(self.calls), "PATH": path}
        for args in (
            ("init", "-q", "-b", "main"),
            ("add", "."),
            ("commit", "-q", "-m", "init"),
            ("init", "-q", "--bare", origin),
        ):
            self.git(*args)
        for args in (("remote", "add", "origin", origin), ("push", "-q", "origin", "main"), ("fetch", "-q", "origin")):
            self.git(*args)
        self.git("worktree", "add", "-q", "--detach", ".claude/worktrees/orchestrator-review", "origin/main")
        self.git("worktree", "add", "-q", "-b", "pr", str(self.temp / "pr"), "main")
        self.validation = self.repo / ".orchestration/validation"
        self.validation.mkdir(parents=True)

    def git(self, *args, cwd=None):
        cmd = ["git", "-c", "commit.gpgsign=false", *args]
        out = subprocess.run(cmd, cwd=cwd or self.repo, env=self.env, check=True, capture_output=True, text=True)
        return out.stdout.strip()

    def head(self, task):
        """A new commit on the PR branch, the task's sweep with no gap, and the fake codex's answer for it."""
        self.git("commit", "-q", "--allow-empty", "-m", task, cwd=self.temp / "pr")
        head = self.git("rev-parse", "HEAD", cwd=self.temp / "pr")
        (self.validation / f"{task}-pr-feedback.json").write_text('{"items": []}')
        (self.calls / f"message-{task}").write_text(message(record(head, task)))
        return head

    def run_script(self, name, *args, code=0):
        cmd = ["bash", str(self.repo / "scripts/orchestrator" / name), *map(str, args)]
        result = subprocess.run(
            cmd, cwd=self.repo, env=self.env, capture_output=True, text=True, timeout=60, check=False
        )
        self.assertEqual(code, result.returncode, result.stdout + result.stderr)
        return result

    def request(self, task, head, **extra):
        queue = self.validation / "audit-queue"
        queue.mkdir(exist_ok=True)
        fields = {"pr": 9, "head": head, "base": head, "task": task, **extra}
        (queue / f"{task}-{head[:7]}.request").write_text("".join(f"{k}={v}\n" for k, v in fields.items()))
        return queue / f"{task}-{head[:7]}"

    def test_pool_saves_only_schema_valid_audit_json_and_blocks_a_rejected_request(self):
        good, bad = self.head("t1-a01"), self.head("t2-a01")
        (self.calls / "message-t2-a01").write_text(message(record(bad, "t2-a01", cls="no-such-class")))
        done, blocked = self.request("t1-a01", good), self.request("t2-a01", bad)
        self.run_script("audit-pool.sh", "--once")
        self.assertTrue(done.with_suffix(".done").exists())
        self.assertEqual(
            record(good, "t1-a01"), json.loads((self.validation / f"t1-a01-audit-{good[:7]}.json").read_text())
        )
        self.assertTrue(blocked.with_suffix(".blocked").exists())
        self.assertIn(
            "orch-audit exited 3", (self.validation / f"audit-queue/t2-a01-{bad[:7]}.request.rejected").read_text()
        )
        self.assertFalse((self.validation / f"t2-a01-audit-{bad[:7]}.json").exists())

    def test_pool_runs_at_most_max_audits_and_the_third_request_waits(self):
        paths = [self.request(t, self.head(t)) for t in ("t1-a01", "t2-a01", "t3-a01")]
        self.run_script("audit-pool.sh", "--once", "--max", "2")
        self.assertEqual([True, True, False], [p.with_suffix(".done").exists() for p in paths])
        self.assertTrue(paths[2].with_suffix(".request").exists())
        self.assertTrue((self.repo / ".claude/worktrees/orchestrator-review-2").is_dir())
        self.run_script("audit-pool.sh", "--once", "--max", "2")
        self.assertTrue(paths[2].with_suffix(".done").exists())

    def test_pool_retries_a_429_three_times_then_blocks(self):
        for count, outcome in (("2", ".done"), ("4", ".blocked")):
            with self.subTest(failures=count):
                (self.calls / "sleep.log").unlink(missing_ok=True)
                head = self.head(f"t{count}-a01")
                (self.calls / f"fail-t{count}-a01").write_text(count)
                path = self.request(f"t{count}-a01", head)
                self.run_script("audit-pool.sh", "--once")
                self.assertTrue(path.with_suffix(outcome).exists())
                delays = ["60", "120", "240"][: min(int(count), 3)]
                self.assertEqual(delays, (self.calls / "sleep.log").read_text().split())

    def test_pool_writes_the_differential_prompt_but_audits_in_full_until_two_shadow_rows_agree(self):
        prev = self.head("t1-a01")
        (self.validation / f"t1-a01-audit-{prev[:7]}.json").write_text(json.dumps(record(prev, "t1-a01")))
        head = self.head("t1-a01")
        shadow = self.validation / "audit-shadow.tsv"
        for rows, differential in (("t\th\tp\t1\t1\t0\n", False), ("t\th\tp\t1\t1\t0\nt\th\tp\t2\t2\t0\n", True)):
            with self.subTest(rows=rows.count("\n")):
                shadow.write_text(rows)
                (self.calls / "codex.log").unlink(missing_ok=True)
                self.request("t1-a01", head, previous_head=prev)
                self.run_script("audit-pool.sh", "--once")
                prompt = (self.calls / "codex.log").read_text()
                self.assertEqual(differential, "This audit is differential" in prompt)
                text = (self.validation / f"t1-a01-audit-{head[:7]}.json.differential-prompt.txt").read_text()
                self.assertIn(f"git diff {prev} {head}", text)

    def test_orch_audit_json_mode_extracts_the_final_json_block_and_keeps_every_refusal(self):
        head, out = self.head("t1-a01"), self.validation / "out.json"
        self.run_script("orch-audit.sh", "t1-a01", "--head", head, 9, "--json", out)
        self.assertEqual(record(head, "t1-a01"), json.loads(out.read_text()))
        self.assertIn(".schemas/audit.json", (self.calls / "codex.log").read_text())
        broken = (
            ("no block", "Verdict: correct\n"),
            ("unknown class", message(record(head, "t1-a01", cls="no-such-class"))),
            ("another head", message(record("0" * 40, "t1-a01"))),
            ("verdict differs", message(record(head, "t1-a01"), verdict="incorrect")),
        )
        for case, text in broken:
            with self.subTest(case=case):
                (self.calls / "message-t1-a01").write_text(text)
                result = self.run_script("orch-audit.sh", "t1-a01", "--head", head, 9, "--json", out, code=3)
                self.assertIn("json block is missing or invalid", result.stderr)
                self.assertFalse(out.exists())
        main = self.git("rev-parse", "HEAD")
        self.assertIn(
            "at the audited head", self.run_script("orch-audit.sh", "t1-a01", "--head", main, 9, code=2).stderr
        )
        self.assertIn("not a commit", self.run_script("orch-audit.sh", "t1-a01", "--head", "1" * 40, 9, code=2).stderr)
        (self.validation / "t1-a01-pr-feedback.json").write_text('{"items": [{"url": "u"}]}')
        self.assertIn(
            "the sweep has gaps", self.run_script("orch-audit.sh", "t1-a01", "--head", head, 9, code=3).stderr
        )

    def test_audit_schema_class_enum_equals_the_classes_file_and_rejects_an_unknown_class(self):
        schema = json.loads((ROOT / ".schemas/audit.json").read_text())
        enum = schema["properties"]["findings"]["items"]["properties"]["class"]["enum"]
        self.assertEqual(sorted(self.classes()), enum)
        doc = self.validation / "doc.json"
        for cls, code in (("records-form", 0), ("no-such-class", 1)):
            with self.subTest(cls=cls):
                doc.write_text(json.dumps(record("a" * 40, "t1-a01", cls=cls)))
                self.run_script("orch-audit.sh", "--validate", ".schemas/audit.json", doc, code=code)

    def test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius(self):
        classes, ledger = self.classes(), set()
        for path in sorted((ROOT / ".orchestration/acceptance").glob("*.md")):
            front = path.read_text().split("\n---\n")[0].lstrip("-\n")
            if front.startswith("{"):
                ledger |= {row["class"] for row in json.loads(front).get("ledger", [])}
        self.assertEqual(set(), ledger - set(classes))
        for name, entry in classes.items():
            with self.subTest(name=name):
                self.assertEqual({"remedy", "blast_radius"}, set(entry))
                self.assertTrue(entry["remedy"] and all(isinstance(g, str) and g for g in entry["blast_radius"]))
                self.assertTrue(entry["blast_radius"])

    def classes(self):
        read = "import json, sys, yaml; print(json.dumps(yaml.safe_load(open(sys.argv[1]))))"
        command = [shutil.which("uv"), "run", "--no-project", "--with", "pyyaml", "python", "-I", "-c", read]
        return json.loads(
            subprocess.run(
                [*command, ROOT / ".schemas/classes.yaml"], check=True, capture_output=True, text=True
            ).stdout
        )


if __name__ == "__main__":
    unittest.main()
