"""Exercise result-precheck.sh, dispatch.sh's precheck gate and the .githooks with stubbed host binaries.

Each case runs the scripts as subprocesses from copies in a temporary git repository whose `origin` is a bare
repository. `make`, `shfmt`, `ruff`, `prettier`, `shellcheck`, `gh`, `uv` and `agmsg-dispatch` are stubs on PATH that
record their argv; the `uv` stub runs `python -m unittest` with this interpreter and acts as the masker, changing a
file only while `masker-changes` exists. The secrets-mode and pre-push cases use the real masker through the real uv.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRECHECK = ROOT / "scripts/orchestrator/result-precheck.sh"
TASK = "dotfiles-T0-x-a01"
RECORD = 'printf \'%s\\n\' "$*" >> "$CALLS/$(basename "$0").log"\n'
STUBS = {
    # make <target> fails while make-<target>-fails exists; the other tools fail while <name>-fails exists.
    "make": RECORD + '[[ ! -f "$CALLS/make-$1-fails" ]]\n',
    **{name: RECORD + f'[[ ! -f "$CALLS/{name}-fails" ]]\n' for name in ("shfmt", "ruff", "prettier", "shellcheck")},
    "gh": RECORD + "echo 7\n",
    "agmsg-dispatch": RECORD
    + 'printf "  ○ [2026-10-18T05:00:00Z] %s → %s: %s\\n" "$2" "$3" "$5" >> "$CALLS/history"\n',
    "uv": RECORD
    + 'if [[ " $* " == *" --mask-secrets "* ]]; then\n'
    + '  on=; for f in "$@"; do\n'
    + '    [[ -z $on || ! -f "$CALLS/masker-changes" ]] || echo masked >> "$f"; [[ $f != --mask-secrets ]] || on=1\n'
    + "  done; exit 0\n"
    + f'fi\nshift; exec "{sys.executable}" "${{@:2}}"\n',
}
LOCAL_REVIEW = '#!/usr/bin/env bash\necho "$*" >> "$CALLS/local-review.log"\nexit "$(cat "$CALLS/local-review-status" 2> /dev/null || echo 0)"\n'
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


def token():
    # Built at run time, so this file holds no literal the repository's secret scan flags.
    return "ghp_" + "A1b2" * 8


class ResultPrecheckTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo, self.calls, bin_dir = self.temp / "repo", self.temp / "calls", self.temp / "bin"
        for directory in (self.repo, self.calls, bin_dir, self.temp / "agmsg"):
            directory.mkdir()
        for name, text in STUBS.items():
            (bin_dir / name).write_text("#!/usr/bin/env bash\n" + text)
            (bin_dir / name).chmod(0o755)
        (self.temp / "agmsg/history.sh").write_text('#!/usr/bin/env bash\ncat "$CALLS/history"\n')
        (self.temp / "agmsg/history.sh").chmod(0o755)
        self.env = {
            **os.environ,
            **GIT_ENV,
            "CALLS": str(self.calls),
            "AGMSG_SCRIPTS": str(self.temp / "agmsg"),
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "TMPDIR": str(self.temp),
        }
        self.git("init", "-q", "-b", "main")
        shutil.copytree(ROOT / "scripts/orchestrator", self.repo / "scripts/orchestrator")
        shutil.copy(ROOT / "scripts/validate-agent-assets.py", self.repo / "scripts/")
        (self.repo / "scripts/orchestrator/local-review.sh").write_text(LOCAL_REVIEW)
        self.write("a.py", "x = 1\n")
        self.write("a.md", "# a\n")
        self.write(".gitignore", "__pycache__/\n")  # as the repository's own, so a test run leaves the tree clean
        self.commit("init")
        self.git("init", "-q", "--bare", str(self.temp / "origin.git"))
        self.git("remote", "add", "origin", str(self.temp / "origin.git"))
        self.git("push", "-q", "--no-verify", "origin", "main")
        self.git("fetch", "-q", "origin")

    def git(self, *args):
        return subprocess.run(
            ["git", "-c", "commit.gpgsign=false", *args],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def write(self, rel, text):
        (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (self.repo / rel).write_text(text)

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "--no-verify", "-m", message)
        return self.git("rev-parse", "HEAD")

    def run_script(self, script, *args, env=None, cwd=None):
        return subprocess.run(
            ["bash", str(script), *args],
            cwd=cwd or self.repo,
            env={**self.env, **(env or {})},
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

    def precheck(self, *args, env=None):
        return self.run_script(self.repo / "scripts/orchestrator/result-precheck.sh", TASK, *args, env=env)

    def record(self):
        return json.loads((self.repo / f".orchestration/{TASK}/precheck.json").read_text())

    def test_precheck_exits_1_and_records_ok_false_for_each_failing_check(self):
        self.git("switch", "-q", "-c", "feature")
        self.write("scripts/new.sh", "#!/usr/bin/env bash\necho new\n")
        head = self.commit("feature")
        seat = {"PRECHECK_LOCAL_REVIEW": "seat"}
        names = ["unit-test", "render-check", "format", "shellcheck", "secrets", "local-review"]
        result = self.precheck(env=seat)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        checks = {c["name"]: c["ok"] for c in self.record()["checks"]}
        self.assertEqual(checks, dict.fromkeys(names, True))
        path = self.repo / f".orchestration/{TASK}/precheck.json"
        self.assertEqual(result.stdout.splitlines()[-1], f"precheck={hashlib.sha256(path.read_bytes()).hexdigest()}")
        self.assertEqual(self.record()["head"], head)
        self.assertIn(f"head={head} precheck=", (path.parent / "result.txt").read_text())
        self.assertIn(f"{TASK} {head} 7", (self.calls / "local-review.log").read_text())
        self.assertIn("-x scripts/new.sh", (self.calls / "shellcheck.log").read_text())
        for name, trigger in zip(
            names,
            ["make-unit-test-fails", "make-render-check-fails", "shfmt-fails", "shellcheck-fails", "masker-changes"],
            strict=False,
        ):
            with self.subTest(check=name):
                (self.calls / trigger).touch()
                result = self.precheck(env=seat)
                (self.calls / trigger).unlink()
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                checks = {c["name"]: c["ok"] for c in self.record()["checks"]}
                self.assertEqual(checks, {**dict.fromkeys(names, True), name: False})
        with self.subTest(check="local-review"):
            (self.calls / "local-review-status").write_text("3")
            result = self.precheck(env=seat)
            self.assertEqual(result.returncode, 1)
            local = next(c for c in self.record()["checks"] if c["name"] == "local-review")
            self.assertEqual((local["ok"], local["exit"]), (False, 3))
        self.write("scripts/dirty.sh", "echo dirty\n")
        self.assertEqual(self.precheck().returncode, 2)

    def test_precheck_records_the_local_review_as_deferred_by_default(self):
        result = self.precheck()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn({"name": "local-review", "ok": None, "deferred": "orchestrator"}, self.record()["checks"])
        self.assertFalse((self.calls / "local-review.log").exists())
        self.assertIn(
            "# shortcut: a Claude seat cannot run codex inside its Bash sandbox (local-review.sh's header)",
            PRECHECK.read_text(),
        )

    def test_precheck_selector_proof_requires_red_on_previous_head_and_green_on_head(self):
        case = "import unittest\n\nclass T(unittest.TestCase):\n    def test_a(self):\n        self.assertTrue({})\n\n"
        case += "    def test_b(self):\n        pass\n"
        self.write("tests/unit/test_sel.py", case.format("False"))
        previous = self.commit("red")
        self.write("tests/unit/test_sel.py", case.format("True"))
        self.commit("green")
        green = self.precheck("--previous-head", previous, "--check", "tests/unit/test_sel.py::test_a")
        self.assertEqual(green.returncode, 0, green.stdout + green.stderr)
        selector = self.record()["selectors"][0]
        self.assertEqual((selector["ok"], selector["head_exit"]), (True, 0))
        self.assertNotEqual(selector["previous_head_exit"], 0)
        always = self.precheck("--previous-head", previous, "--check", "tests/unit/test_sel.py::test_b")
        self.assertEqual(always.returncode, 1, always.stdout + always.stderr)
        self.assertFalse(self.record()["selectors"][0]["ok"])
        self.assertEqual(len(self.git("worktree", "list").splitlines()), 1)
        self.assertNotIn("worktree prune", PRECHECK.read_text())

    def test_precheck_secrets_mode_counts_and_never_prints_the_match(self):
        diff = self.temp / "diff"
        diff.write_text(f"diff --git a/x b/x\n+value={token()}\n")
        env = {"PATH": os.environ["PATH"]}  # the real uv and the real masker
        result = self.run_script(PRECHECK, "--secrets", str(diff), env=env, cwd=ROOT)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout, "secrets: 1 match(es)\n")
        self.assertNotIn(token(), result.stdout + result.stderr)
        self.assertIn(token(), diff.read_text())
        diff.write_text("diff --git a/x b/x\n+value=clean\n")
        self.assertEqual(self.run_script(PRECHECK, "--secrets", str(diff), env=env, cwd=ROOT).returncode, 0)

    def dispatch(self, result_line, required):
        record = self.repo / ".orchestration/acceptance/t.md"
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text('---\n{"format": 1, "task": "t"}\n---\n')
        (self.calls / "history").write_text(f"  ● [2026-10-18T04:00:00Z] worker → orch: {result_line}\n")
        (self.calls / "agmsg-dispatch.log").unlink(missing_ok=True)
        line = self.temp / "line.txt"
        line.write_text("AGMSG-ACCEPTANCE v1 task_id=t status=accepted reason=ok next_action=none\n")
        script = self.repo / "scripts/orchestrator/dispatch.sh"
        args = ("team", "orch", "worker", "w5:pA", str(line), str(record))
        result = self.run_script(script, *args, env={"PRECHECK_REQUIRED": required})
        return result, (self.calls / "agmsg-dispatch.log").exists()

    def test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required(self):
        field = self.git("rev-parse", "HEAD")

        def record(*checks):
            document = json.dumps({"head": field, "checks": list(checks), "selectors": []}) + "\n"
            self.write(".orchestration/t/precheck.json", document)
            return hashlib.sha256(document.encode()).hexdigest()

        sum_ = record({"name": "unit-test", "ok": True}, {"name": "local-review", "ok": None})
        head = self.commit("evidence")
        ready = "AGMSG-RESULT v1 task_id=t status=ready_for_review"
        result, sent = self.dispatch(f"{ready} head={head} precheck={sum_}", "1")
        self.assertEqual((result.returncode, sent), (0, True), result.stderr)
        self.assertNotIn("precheck:", result.stderr)
        self.write("a.py", "x = 2\n")
        outside = self.commit("evidence and code")
        failed_sum = record({"name": "unit-test", "ok": False})
        failed = self.commit("a failed record")
        cases = [
            ("precheck the RESULT", f"{ready} head={head}"),
            ("precheck mismatch", f"{ready} head={head} precheck={'0' * 64}"),
            ("precheck.json:head", f"{ready} head={outside} precheck={sum_}"),
            ("precheck.json:checks", f"{ready} head={failed} precheck={failed_sum}"),
            ("head", f"{ready} head={'f' * 40} precheck={sum_}"),
            ("result no", f"AGMSG-RESULT v1 task_id=other status=ready_for_review head={head} precheck={sum_}"),
            ("result the newest", f"AGMSG-RESULT v1 task_id=t status=blocked head={head} precheck={sum_}"),
        ]
        for field_name, result_line in cases:
            with self.subTest(field=field_name):
                refused, sent = self.dispatch(result_line, "1")
                self.assertEqual((refused.returncode, sent), (1, False), refused.stderr)
                self.assertIn(f"precheck: {field_name}", refused.stderr)
                warned, sent = self.dispatch(result_line, "0")
                self.assertEqual((warned.returncode, sent), (0, True), warned.stderr)
                self.assertIn(f"precheck: warning {field_name}", warned.stderr)

    def hooks(self):
        self.git("config", "core.hooksPath", str(ROOT / ".githooks"))

    def test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure(self):
        self.hooks()
        for n, trigger in enumerate(["shfmt-fails", "shellcheck-fails", None]):
            with self.subTest(trigger=trigger):
                if trigger:
                    (self.calls / trigger).touch()
                self.write(f"scripts/s{n}.sh", "#!/usr/bin/env bash\necho s\n")
                self.git("add", "-A")
                result = subprocess.run(
                    ["git", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "s"],
                    cwd=self.repo,
                    env=self.env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 1 if trigger else 0, result.stdout + result.stderr)
                if trigger:
                    self.assertIn("pre-commit: the commit is stopped", result.stderr)
                    (self.calls / trigger).unlink()
                    self.git("reset", "-q")
        self.assertIn("-x scripts/s0.sh scripts/s1.sh scripts/s2.sh", (self.calls / "shellcheck.log").read_text())

    def test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern(self):
        self.hooks()
        env = {**self.env, "PATH": os.environ["PATH"]}  # the real uv and the real masker
        # Thread 4305945403: a token added and removed again before the push is still in the pushed history.
        for branch, values, code in (
            ("secret", [token()], 1),
            ("removed", [token(), "clean"], 1),
            ("clean", ["clean"], 0),
        ):
            with self.subTest(branch=branch):
                self.git("switch", "-q", "-c", branch, "main")
                for value in values:
                    self.write("value.txt", f"value={value}\n")
                    self.commit(branch)
                result = subprocess.run(
                    ["git", "push", "origin", branch],
                    cwd=self.repo,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    check=False,
                )
                self.assertEqual(result.returncode != 0, bool(code), result.stderr)
                self.assertNotIn(token(), result.stdout + result.stderr)
                if code:
                    self.assertRegex(result.stderr, r"pre-push: [1-9][0-9]* match\(es\) in ")
                self.assertEqual(bool(self.git("ls-remote", "origin", branch)), not code)


if __name__ == "__main__":
    unittest.main()
