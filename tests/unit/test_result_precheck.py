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
    "gh": RECORD + '[[ ! -f "$CALLS/gh-fails" ]] || exit 1\necho 7\n',
    "agmsg-dispatch": RECORD
    + 'printf "  ○ [2026-10-18T05:00:00Z] %s → %s: %s\\n" "$2" "$3" "$5" >> "$CALLS/history"\n',
    "uv": RECORD
    + 'if [[ " $* " == *" --mask-secrets "* ]]; then\n'
    + f'  [[ ! -f "$CALLS/real-masker" ]] || exec "{shutil.which("uv")}" "$@"\n'
    + '  on=; for f in "$@"; do\n'
    + '    [[ -z $on || ! -f "$CALLS/masker-changes" ]] || echo masked >> "$f"; [[ $f != --mask-secrets ]] || on=1\n'
    + "  done; exit 0\n"
    + f'fi\nshift; exec "{sys.executable}" "${{@:2}}"\n',
}
LOCAL_REVIEW = '#!/usr/bin/env bash\necho "$*" >> "$CALLS/local-review.log"\nexit "$(cat "$CALLS/local-review-status" 2> /dev/null || echo 0)"\n'
CHECKS_OK = [
    {"name": n, "ok": True, "exit": 0} for n in ("unit-test", "render-check", "format", "shellcheck", "secrets")
]
DEFERRED = {"name": "local-review", "ok": None, "deferred": "orchestrator"}
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
        self.git("commit", "-q", "--no-verify", "--allow-empty", "-m", message)
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
        for name, trigger in (
            ("unit-test", "make-unit-test-fails"),
            ("render-check", "make-render-check-fails"),
            ("format", "shfmt-fails"),
            ("format", "ruff-fails"),
            ("format", "prettier-fails"),
            ("shellcheck", "shellcheck-fails"),
            ("secrets", "masker-changes"),
        ):
            with self.subTest(check=name, trigger=trigger):
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
        # The previous head runs this head's test source (revise 1 of a02), so the code under test is what changes.
        case = "import unittest\n\nimport flag\n\n\nclass T(unittest.TestCase):\n    def test_a(self):\n"
        case += "        self.assertTrue(flag.ON)\n\n    def test_b(self):\n        pass\n"
        self.write("tests/unit/test_sel.py", case)
        self.write("flag.py", "ON = False\n")
        previous = self.commit("red")
        self.write("flag.py", "ON = True\n")
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

    def test_precheck_records_failed_commands_as_not_ok(self):
        # Local review of a5cb73b4 (P2, result-precheck.sh:173-174): a failed prerequisite never passes a check.
        self.git("switch", "-q", "-c", "feature")
        self.write("scripts/new.sh", "#!/usr/bin/env bash\necho new\n")
        self.commit("feature")
        healthy = self.precheck()
        self.assertEqual(healthy.returncode, 0, healthy.stdout + healthy.stderr)

        def failed(*names, env=None):
            result = self.precheck(env=env)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            checks = {c["name"]: c for c in self.record()["checks"]}
            for name in names:
                self.assertIs(checks[name]["ok"], False, name)
                self.assertNotEqual(checks[name]["exit"], 0, name)
            return checks

        main = self.git("rev-parse", "origin/main")
        self.git("update-ref", "-d", "refs/remotes/origin/main")
        failed("shellcheck", "secrets")
        self.assertIn("fatal", (self.repo / f".orchestration/{TASK}/precheck-secrets.log").read_text())
        orphan = self.git("commit-tree", "4b825dc642cb6eb9a060e54bf8d69288fbee4904", "-m", "unrelated")
        self.git("update-ref", "refs/remotes/origin/main", orphan)
        failed("shellcheck", "secrets")
        self.git("update-ref", "refs/remotes/origin/main", main)
        wrapper = self.temp / "bin/git"
        wrapper.write_text(f'#!/usr/bin/env bash\n[[ $1 != ls-files ]] || exit 3\nexec "{shutil.which("git")}" "$@"\n')
        wrapper.chmod(0o755)
        failed("format")
        wrapper.unlink()
        real = self.temp / "realbin"
        real.mkdir()
        for name, target in (("git", shutil.which("git")), ("bash", shutil.which("bash")), ("python3", sys.executable)):
            (real / name).symlink_to(target)
        (self.temp / "bin/prettier").unlink()
        failed("format", env={"PATH": f"{self.temp / 'bin'}{os.pathsep}{real}{os.pathsep}/usr/bin{os.pathsep}/bin"})
        (self.calls / "gh-fails").touch()
        failed("local-review", env={"PRECHECK_LOCAL_REVIEW": "seat"})
        self.assertFalse((self.calls / "local-review.log").exists())

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

    def dispatch(self, result_line, required, revise=None):
        record = self.repo / ".orchestration/acceptance/t.md"
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text('---\n{"format": 1, "task": "t"}\n---\n')
        rows = f"  ● [2026-10-18T03:00:00Z] orch → worker: {revise}\n" if revise else ""
        (self.calls / "history").write_text(rows + f"  ● [2026-10-18T04:00:00Z] worker → orch: {result_line}\n")
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

        sum_ = record(*CHECKS_OK, DEFERRED)
        head = self.commit("evidence")
        ready = "AGMSG-RESULT v1 task_id=t status=ready_for_review"
        result, sent = self.dispatch(f"{ready} head={head} precheck={sum_}", "1")
        self.assertEqual((result.returncode, sent), (0, True), result.stderr)
        self.assertNotIn("precheck:", result.stderr)
        self.write("a.py", "x = 2\n")
        outside = self.commit("evidence and code")
        failed_sum = record({"name": "unit-test", "ok": False, "exit": 2}, *CHECKS_OK[1:], DEFERRED)
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

    def test_dispatch_rejects_malformed_checks_and_missing_requested_selectors(self):
        # Local review of a5cb73b4 (P2, dispatch.sh:188-190): the record proves all six checks and every requested proof.
        field = self.git("rev-parse", "HEAD")
        sel_a, sel_b = "tests/unit/test_x.py::test_a", "tests/unit/test_x.py::test_b"
        revise = f"AGMSG-ACCEPTANCE v1 task_id=t status=revise previous_head={'a' * 40} check={sel_a} check={sel_b}"
        proofs = [{"selector": sel_a, "ok": True}, {"selector": sel_b, "ok": True}]

        def result(checks, selectors=()):
            document = json.dumps({"head": field, "checks": checks, "selectors": list(selectors)}) + "\n"
            self.write(".orchestration/t/precheck.json", document)
            self.git("add", ".orchestration/t/precheck.json")  # only the record, so the evidence-only ancestry holds
            self.git("commit", "-q", "--no-verify", "--allow-empty", "-m", "record")
            head = self.git("rev-parse", "HEAD")
            return f"AGMSG-RESULT v1 task_id=t status=ready_for_review head={head} precheck={hashlib.sha256(document.encode()).hexdigest()}"

        unit = lambda ok: [{"name": "unit-test", **ok}, *CHECKS_OK[1:], DEFERRED]  # noqa: E731
        valid = result([*CHECKS_OK, DEFERRED], proofs)
        for required in ("1", "0"):
            passed, sent = self.dispatch(valid, required, revise)
            self.assertEqual((passed.returncode, sent), (0, True), passed.stderr)
            self.assertNotIn("precheck:", passed.stderr)
        malformed = {
            "an empty entry": ("checks", result([{}], proofs)),
            "a missing check": ("checks", result([*CHECKS_OK[:4], DEFERRED], proofs)),
            "only an unrelated check": ("checks", result([{"name": "other", "ok": True}], proofs)),
            "a duplicate name": ("checks", result([*CHECKS_OK, DEFERRED, CHECKS_OK[0]], proofs)),
            "a missing ok": ("checks", result(unit({}), proofs)),
            "a string ok": ("checks", result(unit({"ok": "true"}), proofs)),
            "a numeric ok": ("checks", result(unit({"ok": 1}), proofs)),
            "a null ok": ("checks", result(unit({"ok": None}), proofs)),
            "a null without the marker": ("checks", result([*CHECKS_OK, {"name": "local-review", "ok": None}], proofs)),
            "missing selectors": ("selectors", result([*CHECKS_OK, DEFERRED])),
            "one requested selector omitted": ("selectors", result([*CHECKS_OK, DEFERRED], proofs[:1])),
        }
        for name, (field_name, line) in malformed.items():
            with self.subTest(case=name):
                refused, sent = self.dispatch(line, "1", revise)
                self.assertEqual((refused.returncode, sent), (1, False), refused.stderr)
                self.assertIn(f"precheck: precheck.json:{field_name} ", refused.stderr)
                warned, sent = self.dispatch(line, "0", revise)
                self.assertEqual((warned.returncode, sent), (0, True), warned.stderr)
                self.assertIn(f"precheck: warning precheck.json:{field_name} ", warned.stderr)

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

    def test_pre_commit_hook_checks_the_staged_blobs_not_the_working_tree(self):
        # Thread 4305945406: a malformed staged blob stops the commit even when the working-tree copy is fixed.
        self.hooks()
        stub = '#!/usr/bin/env bash\nfor f in "$@"; do [[ ! -f $f ]] || ! grep -q BAD -- "$f" || exit 1; done\n'
        (self.temp / "bin/shfmt").write_text(stub)

        def commit():
            run = ["git", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "s"]
            return subprocess.run(run, cwd=self.repo, env=self.env, capture_output=True, text=True, check=False)

        self.write("scripts/s.sh", "#!/usr/bin/env bash\necho BAD\n")
        self.git("add", "scripts/s.sh")
        self.write("scripts/s.sh", "#!/usr/bin/env bash\necho fixed\n")
        refused = commit()
        self.assertEqual(refused.returncode, 1, refused.stdout + refused.stderr)
        self.assertIn("failed: shfmt", refused.stdout + refused.stderr)
        self.git("add", "scripts/s.sh")
        self.assertEqual(commit().returncode, 0)

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

    def test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit(self):
        # Local review of a5cb73b4 (P1, pre-push:19-20): Git's binary classification never hides pushed content.
        self.hooks()
        env = {**self.env, "PATH": os.environ["PATH"]}  # the real uv and the real masker
        secret, clean = f"key={token()}\n".encode(), b"key=clean\n"
        for branch, commits, code in (
            ("diff-attr", [{".gitattributes": b"*.cred -diff\n", "a.cred": secret}], 1),
            ("binary-attr", [{".gitattributes": b"*.dat binary\n", "a.dat": secret}], 1),
            ("nul", [{"a.bin": b"\x00\x01" + secret + b"\x00"}], 1),
            ("added-then-removed", [{".gitattributes": b"*.cred -diff\n", "a.cred": secret}, {"a.cred": clean}], 1),
            ("diff-attr-clean", [{".gitattributes": b"*.cred -diff\n", "a.cred": clean}], 0),
            ("nul-clean", [{"a.bin": b"\x00\x01" + clean + b"\x00"}], 0),
        ):
            with self.subTest(branch=branch):
                self.git("switch", "-q", "-c", branch, "main")
                for files in commits:
                    for rel, data in files.items():
                        (self.repo / rel).write_bytes(data)
                    self.commit(branch)
                run = ["git", "push", "origin", branch]
                result = subprocess.run(run, cwd=self.repo, env=env, capture_output=True, text=True, timeout=120)
                self.assertEqual(result.returncode != 0, bool(code), result.stderr)
                self.assertNotIn(token(), result.stdout + result.stderr)
                if code:
                    self.assertRegex(result.stderr, r"pre-push: [1-9][0-9]* match\(es\) in ")
                self.assertEqual(bool(self.git("ls-remote", "origin", branch)), not code)
        # The precheck's own secrets input is the forced-text diff: a -diff attribute hides nothing there either.
        self.git("switch", "-q", "diff-attr")
        (self.calls / "real-masker").touch()
        result = self.precheck()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIs(next(c for c in self.record()["checks"] if c["name"] == "secrets")["ok"], False)
        logs = "".join(p.read_text() for p in (self.repo / f".orchestration/{TASK}").glob("precheck-*.log"))
        self.assertNotIn(token(), result.stdout + result.stderr + logs)

    def test_pre_push_scans_each_blob_on_its_own_boundary(self):
        # Local review of 9cd5514 (P1, pre-push:27): a blob ending in a word character never joins a token that opens
        # the next blob, where the masker's word boundary would no longer see it.
        self.hooks()
        env = {**self.env, "PATH": os.environ["PATH"]}  # the real uv and the real masker
        self.git("switch", "-q", "-c", "joined", "main")
        (self.repo / "a.txt").write_bytes(b"word")
        (self.repo / "b.txt").write_bytes(token().encode() + b"\n")
        self.commit("joined")
        run = ["git", "push", "origin", "joined"]
        result = subprocess.run(run, cwd=self.repo, env=env, capture_output=True, text=True, timeout=120)
        self.assertNotEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stderr, r"pre-push: [1-9][0-9]* match\(es\) in ")
        self.assertNotIn(token(), result.stdout + result.stderr)
        self.assertEqual(self.git("ls-remote", "origin", "joined"), "")

    def test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan(self):
        # Local review of 9cd5514 (P1, result-precheck.sh:85): a UTF-16 credential file is caught, with a BOM or without.
        env = {"PATH": os.environ["PATH"]}  # the real uv and the real masker
        blob = self.temp / "blob"
        for encoding in ("utf-16", "utf-16-le", "utf-16-be"):
            with self.subTest(encoding=encoding):
                blob.write_bytes(f"key={token()}\r\n".encode(encoding))
                result = self.run_script(PRECHECK, "--secrets", str(blob), env=env, cwd=ROOT)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertRegex(result.stdout, r"^secrets: [1-9][0-9]* match\(es\)\n$")
                self.assertNotIn(token(), result.stdout + result.stderr)
        blob.write_bytes("key=clean\r\n".encode("utf-16"))
        self.assertEqual(self.run_script(PRECHECK, "--secrets", str(blob), env=env, cwd=ROOT).returncode, 0)

    def test_previous_head_proof_requires_an_executed_failing_test(self):
        # Local review of 9cd5514 (P2, result-precheck.sh:250): the previous head runs this head's test source, and only
        # an executed test that fails by assertion there is a red proof; an import error or no test run proves nothing.
        self.write("lib.py", "VALUE = 1\n")
        previous = self.commit("previous code")
        self.write("lib.py", "VALUE = 2\n\n\ndef helper():\n    return 2\n")
        case = "import unittest\n\nimport lib\n\n\nclass T(unittest.TestCase):\n"
        case += "    def test_value(self):\n        self.assertEqual(lib.VALUE, 2)\n\n"  # fails on the previous code
        case += "    def test_always(self):\n        self.assertTrue(lib.VALUE)\n\n"  # passes on both
        case += "    def test_helper(self):\n        from lib import helper\n\n        self.assertEqual(helper(), 2)\n"
        self.write("tests/unit/test_new.py", case)  # a new module: the previous head lacks it
        self.commit("this head")
        for name, ok in (("test_value", True), ("test_always", False), ("test_helper", False), ("test_none", False)):
            with self.subTest(name=name):
                result = self.precheck("--previous-head", previous, "--check", f"tests/unit/test_new.py::{name}")
                self.assertEqual(result.returncode, 0 if ok else 1, result.stdout + result.stderr)
                self.assertIs(self.record()["selectors"][0]["ok"], ok)
        self.assertEqual(len(self.git("worktree", "list").splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
