"""Exercise verdict.sh where all nine conditions hold, then break each; gh, dispatch, sweep and counters are fakes."""

import hashlib, json, os, re, shutil, subprocess, sys, tempfile, unittest  # noqa: E401 (one line: the test cap)
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK, V = "t1-a01", ".orchestration/validation"
TASK_MD, RECORD = f".orchestration/tasks/{TASK}.md", f".orchestration/acceptance/{TASK}.md"
FEEDBACK = f"{V}/{TASK}-pr-feedback.json"
OSES = ("ubuntu-24.04, server", "ubuntu-24.04, client", "macos-14, client")
REQUIRED = ["validate"] + [f"{job} ({o})" for job in ("test", "public-bootstrap") for o in OSES]
FAKES = {  # $CALLS becomes the calls directory: verdict.sh runs its tools under env -i
    "scripts/orchestrator/dispatch.sh": '#!/usr/bin/env bash\necho "dispatch $* $(cat "$5")" >> "$CALLS/calls.log"\n',
    "scripts/pr-feedback.py": 'import shutil, sys\nshutil.copy("$CALLS/sweep.json", sys.argv[-1])\n',
    "scripts/regime-counters.sh": '#!/usr/bin/env bash\n[[ " $* " == *" --history-only "* ]] && exec grep -v "^S1:" "$CALLS/counters.txt"\ncat "$CALLS/counters.txt"\n',
    "../bin/gh": '#!/usr/bin/env bash\necho "gh $*" >> "$CALLS/calls.log"\ncase "$1 $2" in "pr view") cat "$CALLS/view.json" ;; "pr checks") cat "$CALLS/checks.json" ;; esac\n',
    "../bin/mise": "#!/bin/sh\nexit 1\n",  # no mise answer: every tool resolves through PATH, these fakes first
}
COPIES = ("orchestrator/verdict.sh", "orchestrator/orch-audit.sh", "require-crit-review.py", "validate-agent-assets.py")
AT, URL = "2026-10-18T05:00:00Z", "https://github.test/pull/9#discussion_r1"
FINDING = {"id": "1", "priority": "P2", "confidence": "high", "file": "x.sh", "line": 1, "class": "records-form"}
INCORRECT, P0 = {"verdict": "incorrect", "scope": "code"}, {"priority": "P0", "scope": "code"}
ITEM = {"source": "check-run", "author": "ci", "level": "failure", "path": "x.sh", "line": 1, "body": "b", "url": URL}
NA = "not-applicable:a reason long enough; evidence=git show"  # 20 characters: a failure-level reason
APPLY = ("--apply", "--team", "dot", "--from", "orch", "--to", "w", "--pane", "herdr:s:wJ:p3")
GIT_ENV = {f"GIT_{role}_{k}": v for role in ("AUTHOR", "COMMITTER") for k, v in (("NAME", "t"), ("EMAIL", "t@t"))}
CAP = "500 changed lines outside `tests/` and `.orchestration/`"
S1 = f"task={TASK} revises=1 x\nS1: class=scope count=3\n"


class VerdictTest(unittest.TestCase):
    failed = staticmethod(lambda doc: [c["id"] for c in doc["conditions"] if not c["ok"]])
    calls_log = lambda self: (self.calls / "calls.log").read_text() if (self.calls / "calls.log").exists() else ""  # noqa: E731

    def setUp(self):
        self.temp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.repo, self.calls = self.temp / "repo", self.temp / "calls"
        for d in (self.repo / "scripts/orchestrator", self.calls):
            d.mkdir(parents=True)
        for name in COPIES:
            shutil.copy(ROOT / "scripts" / name, self.repo / "scripts" / name)
        shutil.copytree(ROOT / ".schemas", self.repo / ".schemas")
        for path, text in FAKES.items():
            self.write(path, text.replace("$CALLS", str(self.calls))).chmod(0o755)
        environ = {k: v for k, v in os.environ.items() if k != "PRECHECK_REQUIRED"}
        self.env = {**environ, **GIT_ENV, "PATH": f"{self.temp / 'bin'}{os.pathsep}{os.environ['PATH']}"}
        origin = str(self.temp / "origin.git")
        steps = (("init", "-q", "-b", "main"), ("add", "."), ("commit", "-q", "-m", "init"))
        for args in (*steps, ("init", "-q", "--bare", origin)):
            self.git(*args)
        for args in (("remote", "add", "origin", origin), ("push", "-q", "origin", "main"), ("fetch", "-q", "origin")):
            self.git(*args)
        self.git("switch", "-q", "-c", "pr")
        self.write("scripts/orchestrator/x.sh", "echo x\n")
        self.write("tests/unit/t.py", "x = 1\n")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "code")
        self.precheck = json.dumps({"head": self.git("rev-parse", "HEAD")})
        self.write(f".orchestration/{TASK}/precheck.json", self.precheck)
        self.git("add", ".")
        self.git("commit", "-q", "-m", "evidence")
        self.head = self.git("rev-parse", "HEAD")
        self.git("switch", "-q", "main")
        self.green()

    def write(self, rel, text):
        (path := self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def replace(self, rel, old, new):
        self.write(rel, (self.repo / rel).read_text().replace(old, new))

    def run_in_repo(self, *cmd, env=None):
        env = {**self.env, **(env or {})}
        return subprocess.run(cmd, cwd=self.repo, env=env, capture_output=True, text=True, timeout=60)

    def git(self, *args):
        return self.run_in_repo("git", "-c", "commit.gpgsign=false", *args).stdout.strip()

    def audit(self, verdict="correct", **finding):
        doc = {"head": self.head, "task_id": TASK, "auditor": "codex", "generated_at": AT, "verdict": verdict}
        rest = {"scope": "records", "rationale": "r", "status": "new"}
        doc["findings"] = [FINDING | rest | finding] if finding or verdict != "correct" else []
        return self.write(f"{V}/{TASK}-audit-{self.head[:7]}.json", json.dumps(doc))

    def green(self, security=False, verdict="correct", items=(), fresh=None, **finding):
        view = {"headRefOid": self.head, "isDraft": False, "baseRefName": "main", "state": "OPEN", "number": 9}
        (self.calls / "view.json").write_text(json.dumps(view))
        self.checks("SUCCESS")
        (self.calls / "counters.txt").write_text(f"task={TASK} tasks=1 revises=1 results=2 source=live\ndetail: pr=9\n")
        self.feedback(*(items or [ITEM | {"disposition": NA}]), fresh=fresh)
        allowed = f'["scripts/orchestrator/x.sh", "tests/**", ".orchestration/{TASK}/**"]'
        front = f"allowed_files: {allowed}\nsecurity: {str(security).lower()}"
        self.write(TASK_MD, f"---\n{front}\n---\n\nat most {CAP}, 500 under `tests/`.\n")
        audit = self.audit(verdict, **finding)  # written before the record, which carries its hash
        block = json.dumps({"task": TASK, "pr": 9, "head": self.head, "format": 1, "ledger": []})
        prose = f"precheck: {hashlib.sha256(self.precheck.encode()).hexdigest()}\n"
        prose += f"sha256:{hashlib.sha256(audit.read_bytes()).hexdigest()} {V}/{TASK}-audit-{self.head[:7]}.json\n"
        self.write(RECORD, f"---\n{block}\n---\n\n{prose}")
        self.write(f"{V}/{TASK}-security-{self.head[:7]}.md.last.md", "x\nVerdict: correct\n")

    def checks(self, state, *failed):
        rows = [{"name": n, "state": state} for n in REQUIRED] + [{"name": n, "state": "FAILURE"} for n in failed]
        (self.calls / "checks.json").write_text(json.dumps(rows))

    def feedback(self, *saved, fresh=None):  # the fresh sweep is the saved items undispositioned unless given
        fresh = [item | {"disposition": ""} for item in saved] if fresh is None else fresh
        for path, items in ((self.calls / "sweep.json", fresh), (self.repo / FEEDBACK, saved)):
            self.write(path, json.dumps({"head_sha": self.head, "items": list(items)}))

    def verdict(self, *args, code, env=None):
        result = self.run_in_repo("bash", str(self.repo / "scripts/orchestrator/verdict.sh"), "9", *args, env=env)
        self.assertEqual(code, result.returncode, result.stdout + result.stderr)
        out = self.repo / f"{V}/{TASK}-verdict-{self.head[:7]}.json"
        return json.loads(out.read_text()) if out.exists() else None

    def record_lines(self, precheck=None, extra=""):
        text = (self.repo / RECORD).read_text()
        self.write(RECORD, re.sub(r"(?m)^precheck: .*$", f"precheck: {precheck}", text) if precheck else text + extra)

    def test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds(self):
        doc = self.verdict(code=0)
        self.assertEqual(("accept", [*range(1, 10)]), (doc["verdict"], [c["id"] for c in doc["conditions"] if c["ok"]]))
        security = f"{V}/{TASK}-security-{self.head[:7]}.md.last.md"
        breaks = [
            (1, lambda: self.record_lines(precheck="0" * 64)),
            (2, lambda: self.checks("FAILURE")),
            (2, lambda: self.checks("SUCCESS", "validate")),
            (3, lambda: self.audit("incorrect", scope="code")),
            (4, lambda: self.write(FEEDBACK, '{"items": [{"url": "u", "disposition": "fixed:abc1234"}]}')),
            (4, lambda: self.feedback(ITEM | {"disposition": "later"})),
            (5, lambda: self.write(TASK_MD, '---\nallowed_files: ["other"]\nsecurity: false\n---\n')),
            (5, lambda: self.replace(TASK_MD, CAP, "0 changed lines outside `tests/` and `.orchestration/`")),
            (5, lambda: self.replace(TASK_MD, "500 under", "0 under")),
            (6, lambda: (self.calls / "counters.txt").write_text(S1)),
            (7, lambda: self.audit("correct", priority="P1", scope="code", status="still-open")),
            (8, lambda: (self.green(security=True), self.write(security, "Verdict: incorrect\n"))),
            (9, lambda: self.record_lines(extra="sha256:" + "0" * 64 + f" .orchestration/tasks/{TASK}.md\n")),
            (9, lambda: self.replace(RECORD, "sha256:", "sha:")),
        ]
        revise = f"AGMSG-ACCEPTANCE v1 task_id={TASK} status=revise previous_head={self.head} reason=conditions-"
        for n, (condition, breaker) in enumerate(breaks):
            with self.subTest(case=n, condition=condition):
                self.green()
                breaker()
                code = 20 if condition in (6, 7) else 10
                doc = self.verdict(code=code, env={"PRECHECK_REQUIRED": "1"})
                self.assertIn(condition, self.failed(doc))
                self.assertEqual("hold" if code == 20 else "revise", doc["verdict"])
                self.assertEqual(code == 10, doc.get("revise_line", "").startswith(revise))
        # Every path the Check sentence lists after "outside" leaves the count (Amendment 1's .schemas/).
        self.green()
        self.replace(TASK_MD, CAP, "0 changed lines outside `tests/`, `.orchestration/` and `scripts/` (data)")
        self.assertEqual("accept", self.verdict(code=0)["verdict"])

    def test_verdict_holds_on_a_missing_or_schema_failing_input(self):
        (audit := self.repo / f"{V}/{TASK}-audit-{self.head[:7]}.json").unlink()
        self.assertEqual("hold", self.verdict(code=20)["verdict"])
        self.green()
        audit.write_text(audit.read_text().replace('"findings": []', '"findings": [{"class": "no-such-class"}]'))
        self.assertIn(3, self.failed(self.verdict(code=20)))
        breaks = ((lambda: (self.calls / "checks.json").write_text(""), 2), (lambda: self.audit("blocked"), 3))
        for breaker, condition in breaks:
            with self.subTest(condition=condition):
                self.green()
                breaker()
                self.assertIn(condition, self.failed(self.verdict(code=20)))
        (self.repo / f"{V}/{TASK}-verdict-{self.head[:7]}.json").unlink()
        self.write(RECORD, "---\nnot json\n---\n")
        self.assertIsNone(self.verdict(code=20))
        self.green()
        self.replace(RECORD, ', "ledger": []', "")  # no ledger: no S1 source for condition 6
        self.assertEqual("hold", self.verdict(code=20)["verdict"])
        (self.repo / RECORD).unlink()
        self.assertEqual("hold", self.verdict("--task", TASK, code=20)["verdict"])
        view = json.loads((self.calls / "view.json").read_text()) | {"headRefOid": "f" * 40}
        (self.calls / "view.json").write_text(json.dumps(view))
        self.assertIn("not in this checkout", self.run_in_repo("bash", "scripts/orchestrator/verdict.sh", "9").stderr)

    def test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto(self):
        shadow = self.write(f"{V}/verdict-shadow.tsv", "9\th\taccept\taccept\tyes\tt\n" * 4)  # one PR is not four
        self.assertIn("four agreeing", self.run_in_repo("bash", "scripts/orchestrator/verdict.sh", "9", *APPLY).stderr)
        shadow.write_text("".join(f"{n}\th\taccept\taccept\tyes\tt\n" for n in range(1, 5)))
        for code, finding in ((10, INCORRECT), (20, P0)):
            with self.subTest(code=code):
                self.green()
                self.audit(**finding)
                (self.calls / "calls.log").unlink(missing_ok=True)
                self.verdict(*APPLY, code=code)
                self.assertNotRegex(self.calls_log(), "dispatch|pr merge")
        self.green()
        (self.calls / "calls.log").unlink()
        self.verdict(*APPLY, code=0)
        calls, line = self.calls_log().splitlines(), f"status=accepted reason=verdict-{self.head[:7]} next_action=merge"
        self.assertTrue(calls[-2].startswith("dispatch dot orch w herdr:s:wJ:p3 ") and calls[-2].endswith(line), calls)
        self.assertEqual(f"gh pr merge 9 --squash --match-head-commit {self.head}", calls[-1])
        for args in (("--admin",), (*APPLY, "--auto"), ("--task=--admin-x",)):
            with self.subTest(args=args):
                (self.calls / "calls.log").unlink(missing_ok=True)
                self.verdict(*args, code=2)
                self.assertEqual("", self.calls_log())
        self.git("switch", "-q", "--detach", "pr~1")  # a checkout of the PR's code never merges it
        result = self.run_in_repo("bash", "scripts/orchestrator/verdict.sh", "9", *APPLY)
        self.assertIn("equal origin/main", result.stderr)
        self.assertNotIn("pr merge", self.calls_log())

    def test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold(self):
        out = self.repo / f"{V}/{TASK}-verdict-{self.head[:7]}.json"
        for code, finding in ((0, {}), (10, INCORRECT), (20, P0)):
            with self.subTest(code=code):
                self.green()
                self.audit(**finding) if finding else None
                self.verdict(code=code)
                check = self.run_in_repo(
                    "bash", "scripts/orchestrator/orch-audit.sh", "--validate", ".schemas/verdict.json", out
                )
                self.assertEqual(0, check.returncode, check.stderr)

    def test_verdict_reads_the_record_front_matter_offline_and_holds_when_pyyaml_is_unavailable(self):
        online = '[[ "$*" != *pyyaml* || "$*" == *--offline* ]] || { echo "$*" >> "$CALLS/online.log"; exit 1; }'
        cold = f'[[ "$*" == *pyyaml* && -f $CALLS/no-pyyaml ]] && exit 1; exec "{shutil.which("uv")}" "$@"'
        uv = f"#!/usr/bin/env bash\n{online}\n{cold}\n".replace("$CALLS", str(self.calls))
        self.write("../bin/uv", uv).chmod(0o755)
        self.assertEqual("accept", self.verdict(code=0)["verdict"])
        (self.calls / "no-pyyaml").write_text("")
        self.assertIn(5, self.failed(self.verdict(code=20)))
        self.assertFalse((self.calls / "online.log").exists())  # no online resolution, ever

    def test_verdict_condition_1_is_a_warning_under_precheck_required_0(self):
        self.record_lines(precheck="1" * 64)
        for env, code in (({}, 0), ({"PRECHECK_REQUIRED": "0"}, 0), ({"PRECHECK_REQUIRED": "1"}, 10)):
            with self.subTest(env=env):
                first = self.verdict(code=code, env=env)["conditions"][0]
                self.assertEqual((code == 0, code == 0), (first["ok"], first["evidence"].startswith("warning:")))

    def test_verdict_shadow_appends_the_machine_column_only(self):
        doc = self.verdict("--shadow", code=0)
        row = f"9\t{self.head}\taccept\t\t\t{doc['generated_at']}"
        self.assertEqual([row], (self.repo / f"{V}/verdict-shadow.tsv").read_text().splitlines())
        self.assertNotRegex(self.calls_log(), "dispatch|pr merge")

    def test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout(self):
        planted, marker = self.temp / "planted", self.temp / "planted.log"  # a working python that leaves a marker
        python = f'#!/bin/sh\necho "$0" >> "{marker}"\nexec "{sys.executable}" "$@"\n'
        self.write(planted / "bin/python", python).chmod(0o755)
        self.write(planted / "pyvenv.cfg", f"home = {Path(sys.executable).parent}\n")
        self.write(f"{V}/verdict-shadow.tsv", "".join(f"{n}\th\taccept\taccept\tyes\tt\n" for n in range(1, 5)))
        selectors = {".python-version": {}, ".venv": {}, "UV_PYTHON": {"UV_PYTHON": f"{planted}/bin/python"}}
        for name, env in (selectors | {"VIRTUAL_ENV": {"VIRTUAL_ENV": str(planted)}}).items():
            with self.subTest(selector=name):  # outside the --apply guard's directories, so the old guard passed
                for path in (self.calls / "calls.log", marker, self.repo / ".python-version", self.repo / ".venv"):
                    path.unlink(missing_ok=True)
                self.write(".python-version", f"{planted}/bin/python\n") if name == ".python-version" else None
                (self.repo / ".venv").symlink_to(planted) if name == ".venv" else None
                self.verdict(*APPLY, code=0, env=env)
                self.assertIn(f"gh pr merge 9 --squash --match-head-commit {self.head}", self.calls_log())
                self.assertFalse(marker.exists(), "a checkout or inherited selector ran the planted interpreter")

    def test_verdict_counts_open_p0_p1_findings_even_when_the_id_is_empty(self):
        cases = (("P1", "new", [3, 7]), ("P0", "new", [3, 7]), ("P1", "still-open", [3, 7]), ("P1", "fixed", [3]))
        for priority, status, failed in cases:  # a fixed one is not open: the incorrect audit then fails 3 alone
            with self.subTest(priority=priority, status=status):
                self.green(verdict="incorrect", id="", priority=priority, status=status)  # scope records
                self.assertEqual(failed, self.failed(self.verdict(code=20 if 7 in failed else 10)))

    def test_verdict_condition_4_requires_saved_and_fresh_heads_to_equal_the_accepted_head(self):
        self.assertEqual("accept", self.verdict(code=0)["verdict"])  # both documents name the head
        for path, head in [(p, h) for p in (self.calls / "sweep.json", self.repo / FEEDBACK) for h in ("0" * 40, None)]:
            with self.subTest(document=path.name, head=head):
                self.green()
                items = json.loads(path.read_text())["items"]
                path.write_text(json.dumps({"items": items} | ({"head_sha": head} if head else {})))
                self.assertEqual([4], self.failed(self.verdict(code=10)))

    def test_verdict_condition_4_rejects_an_undispositioned_status_with_a_null_url(self):
        status = ITEM | {"source": "status", "level": "pending", "path": None, "line": None, "url": None}
        for saved, code in ((status, 10), (status | {"disposition": NA}, 0)):  # no disposition, then a valid one
            with self.subTest(disposition=saved.get("disposition")):
                self.green(items=[saved])
                self.assertEqual([4] if code else [], self.failed(self.verdict(code=code)))

    def test_verdict_condition_4_preserves_complete_item_identity_and_multiplicity(self):
        first, last = ITEM | {"body": "first"}, ITEM | {"line": 2, "body": "last"}  # one check-run url
        for case, saved, fresh, code in (
            ("disposition on the last annotation only", [first, last | {"disposition": NA}], None, 10),
            ("two fresh occurrences, one saved", [ITEM | {"disposition": NA}], [ITEM, ITEM], 10),
            ("one saved occurrence for each fresh one", [ITEM | {"disposition": NA}] * 2, [ITEM, ITEM], 0),
        ):
            with self.subTest(case=case):
                self.green(items=saved, fresh=fresh)
                self.assertEqual([4] if code else [], self.failed(self.verdict(code=code)))

    def test_verdict_condition_4_uses_the_existing_disposition_and_commit_validators(self):
        base, fix = self.git("merge-base", "origin/main", self.head), self.git("rev-parse", f"{self.head}~1")
        side = self.git("commit-tree", "-m", "side", f"{base}^{{tree}}")  # exists, outside the head's ancestry
        bad = ["not-applicable:; evidence=", "not-applicable:   ; evidence=git show", NA.replace("git show", "")]
        bad += [f"{NA}; evidence=x", "fixed:abcdef1", f"fixed:{base}", f"fixed:{side}"]
        bad += ["not-applicable:short; evidence=git show"]  # under 20 characters at the failure level
        for disposition, code in [*((d, 10) for d in bad), (f"fixed:{fix}", 0), (NA, 0)]:
            with self.subTest(disposition=disposition):
                self.green(items=[ITEM | {"disposition": disposition}])
                self.assertEqual([4] if code else [], self.failed(self.verdict(code=code)))
