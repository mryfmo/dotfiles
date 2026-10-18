"""Three-outcome gate decisions under fake GitHub and temporary protected state."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "home/dot_claude/hooks/executable_gh-merge-gate.sh"
SHA = "3498973bd057ea4fb405823de718e9da6e40e548"
PINNED = f"gh pr merge 7 --squash --match-head-commit {SHA}"
DRAFT = "gh pr create --draft --base main --head task/ok --fill"
METACHARS = ";&|<>()`$\\\n*?[]{}#~"
GH = r"""#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
p = Path(os.environ['GATE_FIXTURE']); a = sys.argv[1:]
with (p/'argv.jsonl').open('a') as out: out.write(json.dumps(a)+'\n')
if a[:2] == ['repo','view']: print((p/('default' if 'defaultBranchRef' in a else 'nwo')).read_text().strip())
elif a[:2] == ['pr','view']:
    if os.environ.get('CLICOLOR_FORCE') == '1': print('\x1b[31m',end='')
    print((p/'pr.json').read_text())
elif a[:2] == ['pr','list']: print('1' if 'stack/parent' in a else '0')
elif a[0] == 'api':
    endpoint = next(x for x in a[1:] if x.startswith('repos/'))
    key = ('rules' if '/rules/branches/' in endpoint else 'runs' if '/check-runs' in endpoint else
           'statuses' if '/status' in endpoint else 'compare' if '/compare/' in endpoint else 'branch')
    if key == 'branch':
        if not endpoint.endswith(('/task/ok','/orchestration/b')): sys.exit(1)
        print(json.dumps({'commit':{'sha':os.environ['GATE_SHA']}}))
    else:
        value = json.loads((p/(key+'.json')).read_text())
        print(json.dumps([value] if '--slurp' in a else value))
else: sys.exit(9)
"""


def corpus() -> list[tuple[str, str, str, str]]:
    rows = [
        ("honest", PINNED, "allow", ""),
        ("tabs", PINNED.replace(" ", "\t"), "allow", ""),
        ("quoted-binary", PINNED.replace("gh", "'gh'", 1), "allow", ""),
        ("concatenated-subcommand", PINNED.replace("merge", "m''erge", 1), "allow", ""),
        ("boundary", PINNED, "allow", "boundary"),
        ("colour", PINNED, "allow", "colour"),
        ("update", "gh pr update-branch 7 --repo o/r", "allow", ""),
        ("draft", DRAFT, "allow", ""),
        ("ready", "gh pr create --base main --head task/ok --fill", "allow", ""),
        ("records", "gh pr create --base main --head orchestration/b --fill", "allow", ""),
        ("quoted-title", DRAFT + " --title 'ordinary title'", "allow", ""),
        ("read", "gh pr view 7", "", ""),
        ("alias-residual", "gh land 7 --admin", "", ""),
        ("bracket", "[ -f README.md ]", "", ""),
        ("double-bracket", "[[ -f README.md ]]", "", ""),
        ("unrelated", "git merge main", "", ""),
        ("metachar-only", "echo x | cat", "", ""),
        ("prose", "git commit -m 'docs: explain gh pr merge 7'", "ask", ""),
        ("live-tests", "cat > tests.py <<'PY'\ncommand='gh pr merge 7'\nPY\npython -m unittest", "ask", ""),
        ("live-report", "cat > report.md <<'EOF'\ngh pr create was checked\nEOF", "ask", ""),
        ("env-s", "env -S 'gh pr merge 7 --admin'", "ask", ""),
        ("pipe-shell", "printf '%s' 'gh pr merge 7 --admin' | bash", "ask", ""),
        ("heredoc-expansion", "cat <<E\\\nOF\n$(gh pr merge 7 --admin)\nEOF", "ask", ""),
        ("bracket-words", "[ -n 'gh pr merge' ]", "ask", ""),
        ("assign", "TOKEN=value gh pr merge 7 --admin", "ask", ""),
        ("compound", "echo done; gh pr merge 7 --admin", "ask", ""),
        ("glob", DRAFT + " --title *", "ask", ""),
        ("hash", DRAFT + " --title 'a#b'", "ask", ""),
        ("tilde", DRAFT + " --title 'a~b'", "ask", ""),
        ("control", "gh\vpr\vupdate-branch\v7", "ask", ""),
        ("syntax", DRAFT + " --title 'unterminated", "ask", ""),
        ("repo", PINNED + " --repo other/repo", "ask", "nwo-other"),
        ("no-pin", "gh pr merge 7 --squash", "ask", ""),
        ("short-pin", PINNED.replace(SHA, SHA[:12]), "ask", ""),
        ("default-bad", DRAFT, "ask", "default-bad"),
        ("audit-disposition", PINNED, "allow", "audit-disposition"),
        ("empty-command", "", "ask", ""),
    ]
    conditions = (
        "default-empty record-body record-task record-pr record-status record-separator record-symlink "
        "record-missing audit-directory audit-missing audit-incorrect check-missing check-new-failure "
        "gh-failure parser-failure json-failure malformed-view payload-empty payload-bad "
        "pr-head pr-base pr-state pr-draft rules-empty record-json-list record-json-bad "
        "compare-empty compare-incomplete compare-large compare-rename compare-tasks compare-removed compare-malformed"
    )
    rows += [(name, PINNED, "ask", name) for name in conditions.split()]
    rows += [
        (flag, PINNED + " " + flag, "ask", "")
        for flag in ("--admin", "--auto", "--merge", "--rebase", "--delete-branch", "--body x")
    ]
    rows += [
        (key, "gh pr create --base main --head orchestration/b --fill", "ask", key)
        for key in ("compare-empty", "compare-incomplete", "compare-large", "compare-rename")
    ]
    rows += [
        (text, text, "ask", "")
        for text in (
            "gh pr update-branch 7 --rebase",
            "gh pr create --draft --head task/ok --fill",
            "gh pr create --draft --base main --head main --fill",
            "gh pr create --draft --base other --head task/ok --fill",
            DRAFT + " --reviewer x",
            DRAFT.replace("task/ok", "task/missing"),
            PINNED + " --match-head-commit " + "f" * 40,
        )
    ]
    return rows


class GhMergeGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.tmp = Path(self.temp.name)
        self.bin = self.tmp / "bin"
        self.bin.mkdir()
        self.env = dict(
            os.environ,
            HOME=str(self.tmp),
            PATH=f"{self.bin}:{os.environ['PATH']}",
            GATE_FIXTURE=str(self.tmp),
            GATE_SHA=SHA,
            XDG_STATE_HOME=str(self.tmp / "state"),
            GIT_CONFIG_GLOBAL="/dev/null",
            GIT_CONFIG_NOSYSTEM="1",
        )
        self.repo = self.tmp / "repo"
        self.git("init", "-q", str(self.repo))
        self.git("-C", str(self.repo), "config", "user.name", "t")
        self.git("-C", str(self.repo), "config", "user.email", "t@t")
        self.git("-C", str(self.repo), "remote", "add", "origin", "https://github.com/o/r.git")
        for directory in ("acceptance", "validation", "tasks"):
            (self.repo / ".orchestration" / directory).mkdir(parents=True)
        (self.repo / ".orchestration/tasks/t.md").write_text("task\n")
        self.anchor = self.tmp / ".agents/agent-config.yaml"
        self.anchor.parent.mkdir()
        self.anchor.write_text("orchestrator_checkout: ~/repo\n")
        (self.bin / "gh").write_text(GH)
        (self.bin / "gh").chmod(0o755)
        (self.tmp / "default").write_text("main")
        (self.tmp / "nwo").write_text("o/r")
        self.write_pr()
        self.write_record()
        self.audit = self.repo / f".orchestration/validation/t-audit-{SHA[:7]}.md"
        self.audit.write_text("approval\n")
        self.last = Path(str(self.audit) + ".last.md")
        self.last.write_text("justified approval\nVerdict: correct\n")
        required = [{"context": name, "integration_id": 15368} for name in ("validate", "test")]
        self.write_json(
            "rules", [{"type": "required_status_checks", "parameters": {"required_status_checks": required}}]
        )
        run = dict(app={"id": 15368}, status="completed", conclusion="success", head_sha=SHA)
        self.write_json(
            "runs", {"check_runs": [dict(run, id=i, name=name) for i, name in enumerate(("validate", "test"), 1)]}
        )
        self.write_json("statuses", {"statuses": []})
        self.write_json("compare", {"files": [{"filename": ".orchestration/t/task.md", "status": "added"}]})

    def git(self, *args: str) -> None:
        subprocess.run(["git", *args], env=self.env, check=True, capture_output=True)

    def write_json(self, name: str, value: object) -> None:
        (self.tmp / (name + ".json")).write_text(json.dumps(value))

    def write_pr(self, **changes: object) -> None:
        value = dict(headRefOid=SHA, baseRefName="main", headRefName="task/ok", state="OPEN", isDraft=False)
        value.update(changes)
        self.write_json("pr", value)

    def write_record(self, **changes: object) -> None:
        self.record = dict(format=1, task="t", head=SHA, pr=7, audit_findings=[])
        self.record["dispatch"] = ["AGMSG-ACCEPTANCE v1 task_id=t status=accepted reason=fixture"]
        self.record.update(changes)
        (self.repo / ".orchestration/acceptance/t.md").write_text("---\n" + json.dumps(self.record) + "\n---\nbody\n")

    def decide(self, command: str, cwd: Path | None = None) -> str:
        payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(cwd or self.repo)})
        result = subprocess.run(
            ["bash", str(HOOK)],
            input=getattr(self, "payload_override", payload),
            capture_output=True,
            text=True,
            env=self.env,
        )
        self.last_result = result
        self.last_reason = ""
        self.assertEqual(0, result.returncode, result.stderr)
        if not result.stdout:
            return ""
        output = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual("PreToolUse", output["hookEventName"])
        self.last_reason = output["permissionDecisionReason"]
        return output["permissionDecision"]

    def condition(self, name: str) -> None:
        path = self.repo / ".orchestration/acceptance/t.md"
        changes = {
            "pr-head": {"headRefOid": "f" * 40},
            "pr-base": {"baseRefName": "other"},
            "pr-state": {"state": "MERGED"},
            "pr-draft": {"isDraft": True},
            "boundary": {"headRefName": "orchestration/boundary-x"},
        }
        if name in changes:
            self.write_pr(**changes[name])
        if name == "boundary":
            path.unlink()
            self.audit.unlink()
        if name == "colour":
            self.env["CLICOLOR_FORCE"] = "1"
        if name.startswith("default-"):
            (self.tmp / "default").write_text("" if name.endswith("empty") else "bad..branch")
        if name == "nwo-other":
            (self.tmp / "nwo").write_text("other/repo")
        if name == "record-body":
            self.write_record(head="f" * 40)
            path.write_text(path.read_text() + '"head": "' + SHA + '"\n')
        if name == "record-task":
            self.write_record(task="wrong")
        if name == "record-pr":
            self.write_record(pr=8)
        if name == "record-status":
            self.write_record(dispatch=self.record["dispatch"] + ["AGMSG-ACCEPTANCE v1 task_id=t status=revise"])
        if name == "record-separator":
            path.write_text(path.read_text().replace("\n---\n", "\n---invalid\n"))
        if name.startswith("record-json"):
            path.write_text("---\n" + ("[]" if name.endswith("list") else "{") + "\n---\n")
        if name == "record-missing":
            path.unlink()
        if name == "record-symlink":
            path.parent.rename(self.repo / ".orchestration/saved")
            path.parent.symlink_to("saved", target_is_directory=True)
        if name in ("audit-directory", "audit-missing"):
            self.audit.unlink()
        if name == "audit-directory":
            self.audit.mkdir()
        if name.startswith("audit-i") or name == "audit-disposition":
            self.last.write_text("[P1] finding\nVerdict: incorrect\n")
        if name == "audit-disposition":
            entry = dict(n="1", reason="fixture explains the finding with concrete evidence", evidence="command output")
            self.write_record(audit_findings=[entry])
        if name == "rules-empty":
            self.write_json("rules", [])
        if name == "check-missing":
            self.write_json("runs", {"check_runs": []})
        if name == "check-new-failure":
            value = json.loads((self.tmp / "runs.json").read_text())
            value["check_runs"].append(dict(value["check_runs"][0], id=99, conclusion="failure"))
            self.write_json("runs", value)
        if name.startswith("compare-"):
            files = {
                "compare-empty": [],
                "compare-incomplete": None,
                "compare-large": [{"filename": ".orchestration/a"}] * 300,
                "compare-rename": [dict(filename=".orchestration/a", previous_filename="scripts/x", status="renamed")],
                "compare-tasks": [dict(filename=f".orchestration/{t}/task.md", status="added") for t in ("t", "u")],
                "compare-removed": [{"filename": ".orchestration/t/task.md", "status": "removed"}],
                "compare-malformed": [None],
            }
            self.write_json("compare", {"files": files[name]})
        if name in ("gh-failure", "parser-failure", "json-failure"):
            target = self.bin / ({"gh-failure": "gh", "parser-failure": "python3", "json-failure": "jq"}[name])
            target.write_text("#!/bin/sh\nexit 23\n")
            target.chmod(0o755)
        if name == "malformed-view":
            (self.tmp / "pr.json").write_text("{")
        if name.startswith("payload-"):
            self.payload_override = "" if name.endswith("empty") else "{"

    def test_gate_closes_each_of_the_seven_review_classes(self) -> None:
        for label, command, expected, condition in corpus():
            with self.subTest(case=label):
                f = GhMergeGateTest()
                f.setUp()
                try:
                    f.condition(condition)
                    self.assertEqual(expected, f.decide(command), f.last_result.stderr)
                    if expected == "ask":
                        self.assertRegex(f.last_reason, "merge|create|update-branch")
                finally:
                    f.doCleanups()

    def test_no_shell_metacharacter_input_is_allowed(self) -> None:
        commands = [command for _, command, _, _ in corpus() if any(c in command for c in METACHARS)]
        for seed, condition in ((PINNED, ""), (PINNED, "boundary"), (DRAFT, ""), ("gh pr update-branch 7", "")):
            self.write_pr()
            if condition:
                self.condition(condition)
            self.assertEqual("allow", self.decide(seed))
            for character in METACHARS + "\x00\x01\v\f\r\x1b\x7f":
                commands += [seed[:i] + character + seed[i:] for i in (0, 1, 2, len(seed) // 2, len(seed))]
                commands.append(seed + f" --title 'a{character}b'")
        for command in commands:
            with self.subTest(command=command):
                self.assertNotEqual("allow", self.decide(command))

    def test_legacy_records_do_not_block_bound_acceptance(self) -> None:
        path = self.repo / ".orchestration/acceptance/t.md"
        path.parent.rename(self.repo / ".orchestration/previous-acceptance")
        path.parent.mkdir()
        records = [path.parent / f"legacy-{i}.md" for i in range(100)]
        for text in (
            "",
            "legacy\n",
            "---\nformat: 1\n---\n",
            "---\n{\n---\n",
            "---\n[]\n---\n",
            "---\nnull\n---\n",
            '---\n{"head":"other"}\n---\n',
        ):
            with self.subTest(legacy=text):
                for record in records:
                    record.write_text(text)
                self.write_record()
                self.assertGreater(list(path.parent.glob("*.md")).index(path), 0)
                for command in (PINNED, DRAFT.replace("--draft ", "")):
                    self.assertEqual("allow", self.decide(command), self.last_reason)
        for record in records:
            record.unlink()
            record.symlink_to(self.tmp / "unrelated-missing-record")
        self.assertEqual("allow", self.decide(PINNED), self.last_reason)
        for status in ({}, {"status": None}, {"status": "unexpected"}):
            with self.subTest(status=status):
                self.write_json("compare", dict(files=[dict(filename=".orchestration/t/task.md", **status)]))
                self.assertEqual("ask", self.decide(PINNED), self.last_reason)

    def test_body_files_are_regular_and_bound_to_the_invoking_worktree(self) -> None:
        body = self.repo / "body.md"
        body.write_text("synthetic public PR body\n")
        outside = self.tmp / "synthetic-private.txt"
        outside.write_text("synthetic fixture, no real credentials\n")
        (self.repo / "linked.md").symlink_to(outside)
        (self.repo / "linked-dir").symlink_to(self.tmp, target_is_directory=True)
        os.mkfifo(self.repo / "pipe")
        paths = (
            str(outside),
            *"../synthetic-private.txt linked.md linked-dir/synthetic-private.txt linked-dir/../body.md "
            "missing.md .orchestration .git/config pipe -".split(),
        )
        for command in (DRAFT, DRAFT.replace("--draft ", "")):
            for flag in ("--body-file ", "-F ", "--body-file="):
                for value in ("body.md", str(body), *paths):
                    with self.subTest(command=command, flag=flag, path=value):
                        expected = "allow" if value in ("body.md", str(body)) else "ask"
                        self.assertEqual(expected, self.decide(command + f" {flag}{value}"), self.last_reason)
        docs = self.repo / "docs"
        docs.mkdir()
        (docs / "body.md").write_text("")
        self.assertEqual("allow", self.decide(DRAFT + " -F body.md", docs))
        self.assertEqual("allow", self.decide(DRAFT + f" -F {body}", docs))
        self.git("-C", str(self.repo), "init", "-q", "--separate-git-dir", str(self.repo / ".metadata"))
        self.assertEqual("ask", self.decide(DRAFT + " -F .metadata/config"), self.last_reason)

    def test_anchor_and_worker_draft_operation_split(self) -> None:
        self.git("-C", str(self.repo), "commit", "--allow-empty", "-qm", "fixture")
        worker = self.tmp / "worker"
        self.git("-C", str(self.repo), "worktree", "add", "-q", str(worker))
        other = self.tmp / "other"
        self.git("init", "-q", str(other))
        self.git("-C", str(other), "remote", "add", "origin", "https://github.com/o/r.git")
        for cwd in (worker, other):
            self.assertEqual("ask", self.decide(PINNED, cwd))
            self.assertEqual("ask", self.decide(DRAFT.replace("--draft ", ""), cwd))
        self.assertEqual("allow", self.decide(DRAFT, worker))
        (worker / "body.md").write_text("synthetic worker PR body\n")
        self.assertEqual("allow", self.decide(DRAFT + " -F body.md", worker))
        self.assertEqual("ask", self.decide(DRAFT + f" -F {worker / 'body.md'}"), self.last_reason)
        self.assertEqual("allow", self.decide(DRAFT.replace("main", "stack/parent"), worker))
        self.assertEqual("allow", self.decide("gh pr update-branch 7", self.tmp))
        self.condition("boundary")
        self.assertEqual("ask", self.decide(PINNED, worker))


if __name__ == "__main__":
    unittest.main()
