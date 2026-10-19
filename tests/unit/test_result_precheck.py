"""Exercise result-precheck.sh, dispatch.sh's precheck gate and the .githooks in temporary repositories with bare origins.

`make`, `shfmt`, `ruff`, `prettier`, `shellcheck`, `gh`, `uv` and `agmsg-dispatch` are argv-recording stubs on PATH; the
`uv` stub runs Python with this interpreter and masks a `ghp_` token (or prints its input and fails while `masker-fails`
exists). Secret scans use the real detector through the real uv. HOME is the fixture's own (security review of ddf262d).
"""

import hashlib
import json
import os
import re
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
    "make": RECORD + '[[ ! -f "$CALLS/make-prints" ]] || cat "$CALLS/make-prints"\n[[ ! -f "$CALLS/make-$1-fails" ]]\n',
    **{name: RECORD + f'[[ ! -f "$CALLS/{name}-fails" ]]\n' for name in ("shfmt", "ruff", "prettier", "shellcheck")},
    "gh": RECORD + '[[ ! -f "$CALLS/gh-fails" ]] || exit 1\necho 7\n',
    "agmsg-dispatch": RECORD
    + 'printf "  ○ [2026-10-18T05:00:00Z] %s → %s: %s\\n" "$2" "$3" "$5" >> "$CALLS/history"\n',
    "uv": RECORD
    + 'if [[ " $* " == *" --mask-secrets "* ]]; then\n  on=; for f in "$@"; do\n'
    + '    [[ -z $on ]] || if [[ -f "$CALLS/masker-fails" ]]; then cat -- "$f" >&2; rc=1\n'
    + '    else sed -i.bak -E \'s/ghp_[A-Za-z0-9]+/<masked>/g\' "$f" && rm -f "$f.bak"; fi\n'
    + '    [[ $f != --mask-secrets ]] || on=1\n  done; exit "${rc:-0}"\nfi\n'
    # dispatch.sh's offline form: its yaml probe passes, a review-brief parse answers "not a brief", a script runs.
    + '[[ " $* " != *" --offline "* ]] || { while [[ $1 != python ]]; do shift; done; shift\n'
    + '  [[ $2 != -c ]] || exit "$([[ $3 == "import yaml" ]]; echo $?)"\n'
    + f'  exec "{sys.executable}" "$@"; }}\n'
    + f'shift; while [[ $1 == --* ]]; do [[ $1 != --with ]] || shift; shift; done; shift; exec "{sys.executable}" "$@"\n',
}
LOCAL_REVIEW = '#!/usr/bin/env bash\necho "$*" >> "$CALLS/local-review.log"\nexit "$(cat "$CALLS/local-review-status" 2> /dev/null || echo 0)"\n'
CHECKS_OK = [
    {"name": n, "ok": True, "exit": 0} for n in ("unit-test", "render-check", "format", "shellcheck", "secrets")
]
DEFERRED = {"name": "local-review", "ok": None, "deferred": "orchestrator"}
SEL_A, SEL_B, BASE = "tests/unit/test_x.py::test_a", "tests/unit/test_x.py::test_b", "a" * 40
PROOFS = [{"selector": s, "ok": True, "previous_head": BASE} for s in (SEL_A, SEL_B)]
UNITS = (("missing", {}), ("string", {"ok": "true"}), ("numeric", {"ok": 1}), ("null", {"ok": None}))  # bad ok values
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
TOKEN = "ghp_" + "A1b2" * 8  # built at run time, so this file holds no literal the secret scan flags
MATCH, DECODING = r"pre-push: [1-9][0-9]* match\(es\) in ", r"pre-push: decoding: .* cannot be decoded"


class ResultPrecheckTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo, self.calls, bin_dir = self.temp / "repo", self.temp / "calls", self.temp / "bin"
        self.sh = self.repo / "scripts/orchestrator"  # the scripts under test, copied into the repository
        for directory in (self.repo, self.calls, bin_dir, self.temp / "agmsg", self.temp / "home"):
            directory.mkdir()
        stubs = {bin_dir / n: t for n, t in STUBS.items()} | {self.temp / "agmsg/history.sh": 'cat "$CALLS/history"\n'}
        for path, text in stubs.items():
            path.write_text("#!/usr/bin/env bash\n" + text)
            path.chmod(0o755)
        # No inherited Git configuration override, and a HOME of the fixture's own (the security review of ddf262d).
        self.env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_CONFIG", "XDG_CONFIG"))} | GIT_ENV
        self.env |= {"HOME": str(self.temp / "home"), "GIT_CONFIG_NOSYSTEM": "1", "CALLS": str(self.calls)}
        self.env |= {"AGMSG_SCRIPTS": str(self.temp / "agmsg"), "TMPDIR": str(self.temp)}
        self.env |= {"PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"}
        self.git("init", "-q", "-b", "main")
        shutil.copytree(ROOT / "scripts/orchestrator", self.repo / "scripts/orchestrator")
        shutil.copy(ROOT / "scripts/validate-agent-assets.py", self.repo / "scripts/")
        (self.repo / "scripts/orchestrator/local-review.sh").write_text(LOCAL_REVIEW)
        for rel, text in (("a.py", "x = 1\n"), ("a.md", "# a\n"), (".gitignore", "__pycache__/\n")):
            self.write(rel, text)  # the .gitignore is the repository's own, so a run leaves the tree clean
        self.commit("init")
        origin = str(self.temp / "origin.git")
        steps = [("init", "-q", "--bare", origin), ("remote", "add", "origin", origin), ("fetch", "-q", "origin")]
        for args in steps[:2] + [("push", "-q", "--no-verify", "origin", "main")] + steps[2:]:
            self.git(*args)

    def git(self, *args):
        run = {"cwd": self.repo, "env": self.env, "capture_output": True, "text": True}
        return subprocess.run(["git", "-c", "commit.gpgsign=false", *args], **run, check=True).stdout.strip()

    def write(self, rel, text):
        (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (self.repo / rel).write_bytes(text if isinstance(text, bytes) else text.encode())

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "--no-verify", "--allow-empty", "-m", message)
        return self.git("rev-parse", "HEAD")

    def run_script(self, script, *args, env=None, cwd=None):
        run = {"cwd": cwd or self.repo, "env": self.env | (env or {}), "capture_output": True, "text": True}
        return subprocess.run(["bash", str(script), *args], **run, timeout=120, check=False)

    def precheck(self, *args, env=None):
        return self.run_script(self.sh / "result-precheck.sh", TASK, *args, env=env)

    def record(self):
        return json.loads((self.repo / f".orchestration/{TASK}/precheck.json").read_text())

    def test_precheck_exits_1_and_records_ok_false_for_each_failing_check(self):
        self.git("switch", "-q", "-c", "feature")
        self.write("scripts/new.sh", "#!/usr/bin/env bash\necho new\n")
        head = self.commit("feature")
        seat = {"PRECHECK_LOCAL_REVIEW": "seat"}
        names = ["unit-test", "render-check", "format", "shellcheck", "secrets", "local-review"]
        oks = lambda: {c["name"]: c["ok"] for c in self.record()["checks"]}
        result = self.precheck(env=seat)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(oks(), dict.fromkeys(names, True))
        path = self.repo / f".orchestration/{TASK}/precheck.json"
        self.assertEqual(result.stdout.splitlines()[-1], f"precheck={hashlib.sha256(path.read_bytes()).hexdigest()}")
        self.assertEqual(self.record()["head"], head)
        self.assertIn(f"head={head} precheck=", (path.parent / "result.txt").read_text())
        self.assertIn(f"{TASK} {head} 7", (self.calls / "local-review.log").read_text())
        self.assertIn("-x scripts/new.sh", (self.calls / "shellcheck.log").read_text())
        tools = [(n, f"make-{n}-fails") for n in ("unit-test", "render-check")] + [("shellcheck", "shellcheck-fails")]
        for name, trigger in tools + [("format", f"{tool}-fails") for tool in ("shfmt", "ruff", "prettier")]:
            with self.subTest(check=name, trigger=trigger):
                (self.calls / trigger).touch()
                result = self.precheck(env=seat)
                (self.calls / trigger).unlink()
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual(oks(), dict.fromkeys(names, True) | {name: False})
        with self.subTest(check="secrets"):  # a committed token, found by the real detector (a03 item 1)
            self.write("leak.txt", f"value={TOKEN}\n")
            self.commit("leak")
            self.assertEqual(self.precheck(env=seat).returncode, 1)
            self.assertEqual(oks()["secrets"], False)
            self.git("reset", "-q", "--hard", "HEAD~1")
        with self.subTest(check="local-review"):
            (self.calls / "local-review-status").write_text("3")
            result = self.precheck(env=seat)
            local = next(c for c in self.record()["checks"] if c["name"] == "local-review")
            self.assertEqual((result.returncode, local["ok"], local["exit"]), (1, False, 3))
        self.write("scripts/dirty.sh", "echo dirty\n")
        self.assertEqual(self.precheck().returncode, 2)

    def test_precheck_records_failed_commands_as_not_ok(self):
        # Local review of a5cb73b4 (P2, result-precheck.sh:173-174): a failed prerequisite never passes a check.
        self.git("switch", "-q", "-c", "feature")
        self.write("scripts/new.sh", "#!/usr/bin/env bash\necho new\n")
        self.commit("feature")
        healthy = self.precheck()  # by default the local review is recorded as deferred and never run (end of test)
        self.assertEqual(healthy.returncode, 0, healthy.stdout + healthy.stderr)
        self.assertIn(DEFERRED, self.record()["checks"])
        self.assertIn("# shortcut: a Claude seat cannot run codex inside its Bash sandbox", PRECHECK.read_text())

        def failed(*names, env=None):  # the run exits 1 and each named check is ok false with a nonzero exit
            result, checks = self.precheck(env=env), {c["name"]: c for c in self.record()["checks"]}
            got = [(checks[n]["ok"], checks[n]["exit"] != 0) for n in names]
            self.assertEqual((result.returncode, got), (1, [(False, True)] * len(names)), result.stdout + result.stderr)

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

    def scan(self, path):  # `result-precheck.sh --secrets <path>` of this repository, the real uv and detector
        return self.run_script(PRECHECK, "--secrets", str(path), env={"PATH": os.environ["PATH"]}, cwd=ROOT)

    def dispatch(self, result_line, required, revise=None, later=None, rows=None):
        """Send the accepted ACCEPTANCE from orch to worker over a history of (sender, recipient, text) rows."""
        self.write(".orchestration/acceptance/t.md", '---\n{"format": 1, "task": "t"}\n---\n')
        record = self.repo / ".orchestration/acceptance/t.md"
        rows = rows or [("orch", "worker", revise), ("worker", "orch", result_line), ("orch", "worker", later)]
        text = "".join(f"  ● [2026-10-18T0{n}:00:00Z] {s} → {r}: {t}\n" for n, (s, r, t) in enumerate(rows) if t)
        (self.calls / "history").write_text(text)
        (self.calls / "agmsg-dispatch.log").unlink(missing_ok=True)
        line = self.temp / "line.txt"
        line.write_text("AGMSG-ACCEPTANCE v1 task_id=t status=accepted reason=ok next_action=none\n")
        args = ("team", "orch", "worker", "w5:pA", str(line), str(record))
        result = self.run_script(self.sh / "dispatch.sh", *args, env={"PRECHECK_REQUIRED": required})
        return result, (self.calls / "agmsg-dispatch.log").exists()

    def gated(self, line, field, revise=None, later=None, rows=None):  # refused under 1, only warned under 0
        for required, outcome, prefix in (("1", (1, False), "precheck: "), ("0", (0, True), "precheck: warning ")):
            result, sent = self.dispatch(line, required, revise, later, rows)
            self.assertEqual((result.returncode, sent), outcome, result.stderr)
            self.assertIn(prefix + field, result.stderr)

    def test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required(self):
        line = self.evidence([*CHECKS_OK, DEFERRED])
        ready, rest = line.split(" head=")
        head, sum_ = rest.split(" precheck=")  # head keeps its precheck_head= field
        result, sent = self.dispatch(line, "1")
        self.assertEqual((result.returncode, sent, "precheck:" in result.stderr), (0, True, False), result.stderr)
        self.write("a.py", "x = 2\n")
        outside = self.commit("evidence and code")
        failed = self.evidence([{"name": "unit-test", "ok": False, "exit": 2}, *CHECKS_OK[1:], DEFERRED])
        cases = [
            ("precheck the RESULT", f"{ready} head={head}"),
            ("precheck mismatch", f"{ready} head={head} precheck={'0' * 64}"),
            ("precheck_head", f"{ready} head={outside} precheck_head={self.code} precheck={sum_}"),
            ("precheck.json:checks", failed),
            ("head", f"{ready} head={'f' * 40} precheck_head={self.code} precheck={sum_}"),
            ("result no", f"AGMSG-RESULT v1 task_id=other status=ready_for_review head={head} precheck={sum_}"),
            ("result the newest", f"AGMSG-RESULT v1 task_id=t status=blocked head={head} precheck={sum_}"),
        ]
        for field_name, result_line in cases:
            with self.subTest(field=field_name):
                self.gated(result_line, field_name)

    def evidence(self, checks, selectors=(), **fields):
        """Commit a precheck.json of task t whose head is the current code, and return its ready RESULT line."""
        self.code = getattr(self, "code", None) or self.git("rev-parse", "HEAD")  # the code head, before any record
        doc = {"head": self.code, "code_head": self.code, "tree": self.git("rev-parse", f"{self.code}^{{tree}}")}
        document = json.dumps({**doc, "checks": checks, "selectors": list(selectors), **fields}) + "\n"
        self.write(".orchestration/t/precheck.json", document)
        self.git("add", ".orchestration/t/precheck.json")  # only the record, so the evidence-only ancestry holds
        self.git("commit", "-q", "--no-verify", "--allow-empty", "-m", "record")
        head, sha = self.git("rev-parse", "HEAD"), hashlib.sha256(document.encode()).hexdigest()
        return f"AGMSG-RESULT v1 task_id=t status=ready_for_review head={head} precheck_head={self.code} precheck={sha}"

    def test_dispatch_rejects_malformed_checks_and_missing_requested_selectors(self):
        # Local review of a5cb73b4 (P2, dispatch.sh:188-190): the record proves all six checks and every requested proof.
        revise = f"AGMSG-ACCEPTANCE v1 task_id=t status=revise previous_head={BASE} check={SEL_A} check={SEL_B}"
        proofs, result = PROOFS, self.evidence
        unit = lambda ok: [{"name": "unit-test", **ok}, *CHECKS_OK[1:], DEFERRED]
        valid = result([*CHECKS_OK, DEFERRED], proofs)
        for required in ("1", "0"):
            passed, sent = self.dispatch(valid, required, revise)
            self.assertEqual((passed.returncode, sent, "precheck:" in passed.stderr), (0, True, False), passed.stderr)
        malformed = {
            "an empty entry": ("checks", result([{}], proofs)),
            "a missing check": ("checks", result([*CHECKS_OK[:4], DEFERRED], proofs)),
            "only an unrelated check": ("checks", result([{"name": "other", "ok": True}], proofs)),
            "a duplicate name": ("checks", result([*CHECKS_OK, DEFERRED, CHECKS_OK[0]], proofs)),
            **{f"a {k} ok": ("checks", result(unit(v), proofs)) for k, v in UNITS},
            "a null without the marker": ("checks", result([*CHECKS_OK, {"name": "local-review", "ok": None}], proofs)),
            "missing selectors": ("selectors", result([*CHECKS_OK, DEFERRED])),
            "one requested selector omitted": ("selectors", result([*CHECKS_OK, DEFERRED], proofs[:1])),
        }
        for name, (field_name, line) in malformed.items():
            with self.subTest(case=name):
                self.gated(line, f"precheck.json:{field_name} ", revise)

    def test_dispatch_acceptance_check_requires_a_result_newer_than_the_latest_revise(self):
        # Local review of 4ed1b27 (P2, dispatch.sh:174-176): a revise after the newest RESULT outdates that RESULT.
        revise = lambda task, s: f"AGMSG-ACCEPTANCE v1 task_id={task} status=revise previous_head={BASE} check={s}"
        ready = self.evidence([*CHECKS_OK, DEFERRED], PROOFS)
        self.gated(ready, "result ", revise("t", SEL_A), later=revise("t", SEL_B))
        # The same RESULT after the latest revise passes, as does one followed only by another task's revise.
        for before, after in ((revise("t", SEL_B), None), (revise("t", SEL_A), revise("other", SEL_B))):
            passed, sent = self.dispatch(ready, "1", before, later=after)
            self.assertEqual((passed.returncode, sent), (0, True), passed.stderr)

    def test_dispatch_acceptance_check_compares_the_proof_baseline_with_the_latest_revise(self):
        # The audit of bccb2de (P2, dispatch.sh:177): a proof counts only against the latest revise's previous_head.
        revise = f"AGMSG-ACCEPTANCE v1 task_id=t status=revise previous_head={BASE} check={SEL_A} check={SEL_B}"
        stale = self.evidence([*CHECKS_OK, DEFERRED], [{**p, "previous_head": "f" * 40} for p in PROOFS])
        self.gated(stale, "precheck.json:selectors ", revise)
        listed = revise.replace(f" check={SEL_B}", f",{SEL_B}")
        passed, sent = self.dispatch(self.evidence([*CHECKS_OK, DEFERRED], PROOFS), "1", listed)
        self.assertEqual((passed.returncode, sent), (0, True), passed.stderr)

    def test_result_precheck_stops_when_the_clean_tree_query_fails(self):
        # The audit of bccb2de (P2, result-precheck.sh:187): a failed git status stops the run before any check.
        (self.repo / ".git/index").write_bytes(b"not an index")
        result, made = self.precheck(), (self.repo / f".orchestration/{TASK}").exists()
        self.assertEqual((result.returncode, made, "index" in result.stderr), (2, False, True), result.stderr)

    def leaks(self, result):  # the token in the run's output, its evidence, or a private capture left behind
        files = [*(self.repo / ".orchestration").rglob("*"), *self.temp.glob("result-precheck.*/**/*")]
        texts = [result.stdout, result.stderr, *(f.read_text(errors="replace") for f in files if f.is_file())]
        return TOKEN in "".join(texts) or bool(list(self.temp.glob("result-precheck.*")))

    def test_precheck_fails_closed_when_masking_fails(self):
        # The security review of ddf262d (P1, result-precheck.sh:251): a failed masker leaks nothing it was given.
        (self.calls / "make-prints").write_text(f"key={TOKEN}\n")
        (self.calls / "masker-fails").touch()
        result, evidence = self.precheck(), self.repo / f".orchestration/{TASK}"
        self.assertEqual((result.returncode, self.leaks(result)), (1, False), result.stdout + result.stderr)
        self.assertEqual((evidence / "precheck-unit-test.log").read_text(), "masking failed: exit 1\n")
        self.assertNotIn(True, [c["ok"] for c in self.record()["checks"]])
        self.assertIn("status=blocked", (evidence / "result.txt").read_text())

    def test_precheck_masks_logs_when_proof_worktree_creation_fails(self):
        # The audit of ddf262d (P2, result-precheck.sh:235): an early exit still masks, publishes and cleans up.
        (self.calls / "make-prints").write_text(f"key={TOKEN}\n")
        git, head, record = self.temp / "bin/git", self.git("rev-parse", "HEAD"), self.repo / f".orchestration/{TASK}"
        git.write_text(f'#!/usr/bin/env bash\n[[ $1 != worktree ]] || exit 3\nexec "{shutil.which("git")}" "$@"\n')
        git.chmod(0o755)
        for fails in (False, True):
            with self.subTest(masker_fails=fails):
                (self.calls / "masker-fails").touch() if fails else None
                result = self.precheck("--previous-head", head, "--check", SEL_A)
                done = (result.returncode != 0, self.leaks(result), (record / "precheck.json").exists())
                self.assertEqual(done, (True, False, False), result.stdout + result.stderr)

    def test_precheck_refuses_symlinked_evidence(self):
        # The security review of ddf262d (P1, result-precheck.sh:278): no evidence write follows a committed symlink.
        sentinel, outside, base = self.temp / "sentinel", self.temp / "outside", self.git("rev-parse", "HEAD")
        outside.mkdir()
        fresh = lambda: [self.git(*a) for a in (("reset", "-q", "--hard", base), ("clean", "-qfd"))]
        for name in ("precheck.json", "result.txt", "precheck-unit-test.log", ""):
            fresh()
            with self.subTest(link=name or "the task directory"):
                sentinel.write_text("kept\n")
                link = self.repo / f".orchestration/{TASK}" / name
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(sentinel if name else outside)
                self.commit("a symlinked evidence path")
                result = self.precheck()
                done = (result.returncode, sentinel.read_text(), list(outside.iterdir()))
                self.assertEqual(done, (1, "kept\n", []), result.stdout + result.stderr)
        fresh()  # a regular directory: a complete record
        self.assertEqual(self.precheck().returncode, 0)
        names = {p.name for p in (self.repo / f".orchestration/{TASK}").iterdir()}
        self.assertTrue({"precheck.json", "result.txt", "precheck-unit-test.log"} <= names, names)

    def test_blob_scan_rejects_paths_outside_scan_directory(self):
        # The audit of ddf262d (P2, result-precheck.sh:103): a blob path is confined before any destination exists.
        victim = self.temp / "victim"
        for path in ("../../victim", str(victim), "a/../../../victim"):
            with self.subTest(path=path):
                victim.write_text("kept\n")
                result = self.run_script(PRECHECK, "--blob", f"HEAD:{path}")
                self.assertEqual((result.returncode != 0, victim.read_text()), (True, "kept\n"), result.stdout)
        self.assertEqual(self.run_script(PRECHECK, "--blob", "HEAD:a.py").stdout, "secrets: 0 match(es)\n")

    def test_precheck_fixtures_isolate_home(self):
        # The security review of ddf262d (P2, setUp): HOME is the fixture's own; the probe runs the committed fixture.
        source, sentinel = self.temp / "fixture.py", self.temp / "sentinel-home"
        sentinel.mkdir()
        show = ["git", "show", "HEAD:tests/unit/test_result_precheck.py"]
        source.write_text(subprocess.run(show, cwd=ROOT, capture_output=True, text=True, check=True).stdout)
        probe = "import importlib.util as u, pathlib, sys\ns = u.spec_from_file_location('f', sys.argv[1])\n"
        probe += "m = u.module_from_spec(s)\ns.loader.exec_module(m)\nm.ROOT = pathlib.Path(sys.argv[2])\n"
        probe += "t = m.ResultPrecheckTest('setUp')\nt.setUp()\nprint(t.env['HOME'], t.temp)\nt.doCleanups()\n"
        run, env = [sys.executable, "-c", probe, str(source), str(ROOT)], os.environ | {"HOME": str(sentinel)}
        home, temp = subprocess.run(run, env=env, capture_output=True, text=True, check=True).stdout.split()
        self.assertTrue(home.startswith(temp + os.sep) and str(sentinel) not in home, home)

    def test_dispatch_ignores_messages_from_unregistered_identities(self):
        # The security review of ddf262d (P2, dispatch.sh:171): rows of other identities are ignored.
        revise = f"AGMSG-ACCEPTANCE v1 task_id=t status=revise previous_head={BASE} check={SEL_A},{SEL_B}"
        ready, bare = self.evidence([*CHECKS_OK, DEFERRED], PROOFS), self.evidence([*CHECKS_OK, DEFERRED])
        forged = f"AGMSG-RESULT v1 task_id=t status=ready_for_review head={'f' * 40} precheck={'0' * 64}"
        task = "AGMSG-TASK v1 task_id=t task_file=x.md"
        rows = [("orch", "worker", task), ("orch", "worker", revise), ("worker", "orch", ready)]
        rows += [("intruder", "orch", forged), ("worker", "other", forged)]
        passed, sent = self.dispatch(None, "1", rows=rows)
        self.assertEqual((passed.returncode, sent, "ignored 2 row" in passed.stderr), (0, True, True), passed.stderr)
        cut = revise.split(" check=")[0]  # a revise without the requested checks, from or to another identity
        erased = [rows[1], ("intruder", "worker", cut), ("orch", "other", cut), ("worker", "orch", bare)]
        self.gated(None, "precheck.json:selectors ", rows=erased)
        self.gated(None, "result ", rows=[("orch", "someone", task), *rows[1:3]])  # the task went to another seat

    def test_dispatch_binds_precheck_to_code_head_across_update_branch(self):
        # The audit and security review of ddf262d (P2): after the tested code only evidence or a base merge may follow.
        self.git("switch", "-q", "-c", "feature")
        self.write(".orchestration/t/task.md", "---\nallowed_files:\n  - a.py\n  - .orchestration/t/**\n---\n")
        code, ev = self.commit("the task copy"), lambda **f: self.evidence([*CHECKS_OK, DEFERRED], **f)
        ready = ev()
        at = lambda head: re.sub(r" head=\S+", f" head={head}", ready)

        def merge(rel):  # main gains a commit changing rel, origin/main follows, and the branch merges it
            self.git("switch", "-q", "main")
            self.write(rel, f"{rel} on main\n")
            self.commit(f"main changes {rel}")
            for args in (("update-ref", "refs/remotes/origin/main", "main"), ("switch", "-q", "feature")):
                self.git(*args)
            self.git("merge", "-q", "--no-edit", "--no-verify", "main")
            return self.git("rev-parse", "HEAD")

        merged = merge("base.txt")
        passed, sent = self.dispatch(at(merged), "1")
        self.assertEqual((passed.returncode, sent), (0, True), passed.stderr)
        self.write("other.txt", "not evidence\n")
        cases = [("precheck_head", at(self.commit("an unexplained commit")))]
        self.git("reset", "-q", "--hard", merged)
        cases += [("precheck_head", at(merge("a.py")))]  # a post-proof change of the task's code
        self.git("reset", "-q", "--hard", merged)
        orphan = self.git("commit-tree", f"{code}^{{tree}}", "-m", "unrelated")
        cases += [("precheck_head", ready.replace(f" precheck_head={code}", ""))]
        cases += [("precheck_head", ready.replace(f"precheck_head={code}", f"precheck_head={merged}"))]
        cases += [("precheck_head", ev(code_head="f" * 40)), ("precheck.json:tree", ev(tree="0" * 40))]
        cases += [("precheck_head", ev(head=orphan, code_head=orphan).replace(code, orphan))]
        for field_name, line in cases:
            with self.subTest(line=line):
                self.gated(line, field_name)

    def test_dispatch_passes_the_task_sha_to_c14_and_forwards_warnings(self):
        # The P1-12 a02 RESULT (dispatch.sh:238): C14 gets the TASK's own sha, and its warnings reach the caller.
        runs, argv = self.temp / "premise-runs", self.temp / "checker-argv"
        checker = f"import hashlib, pathlib, sys\na = sys.argv[1:]\npathlib.Path({str(argv)!r}).write_text(str(a))\n"
        checker += "f, sha = pathlib.Path(a[-1]), a[a.index('--premises-sha') + 1] if '--premises-sha' in a else None\n"
        checker += f"if sha == hashlib.sha256(f.read_bytes()).hexdigest(): open({str(runs)!r}, 'a').write('x')\n"
        checker += "else: print(f'{f.name}: warning: C14: not run (no trusted sha)', file=sys.stderr)\n"
        checker += "print(f'{f.name}: OK'); print(f'{f.name}: warning: C14: tool absent fake', file=sys.stderr)\n"
        (self.sh / "task-consistency-check.py").write_text(checker)
        self.write(".orchestration/tasks/t.md", "---\nkind: code\n---\n")
        sha, line = hashlib.sha256(b"---\nkind: code\n---\n").hexdigest(), self.temp / "task.txt"
        for want, code, warning in ((sha, 0, "C14: tool absent fake"), ("0" * 64, 1, "C14: not run (no trusted sha)")):
            with self.subTest(task_sha256=want):
                line.write_text(f"AGMSG-TASK v1 task_id=t task_file=.orchestration/tasks/t.md task_sha256={want}\n")
                result = self.run_script(self.sh / "dispatch.sh", "t", "orch", "w", "p", str(line))
                done = (result.returncode, warning in result.stderr, runs.read_text() if runs.exists() else "")
                self.assertEqual(done, (code, True, "x"), result.stdout + result.stderr)
        self.assertIn(f"'--premises-sha', '{sha}'", argv.read_text())
        self.assertEqual(len((self.calls / "agmsg-dispatch.log").read_text().splitlines()), 1)

    def hooked_commit(self):  # `git commit` through the repository's hooks, as a seat runs it
        self.git("config", "core.hooksPath", str(ROOT / ".githooks"))
        run = ["git", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "s"]
        return subprocess.run(run, cwd=self.repo, env=self.env, capture_output=True, text=True, check=False)

    def test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure(self):
        for n, trigger in enumerate(["shfmt-fails", "shellcheck-fails", None]):
            with self.subTest(trigger=trigger):
                (self.calls / trigger).touch() if trigger else None
                self.write(f"scripts/s{n}.sh", "#!/usr/bin/env bash\necho s\n")
                self.git("add", "-A")
                result, want = self.hooked_commit(), (1, True) if trigger else (0, False)
                done = (result.returncode, "pre-commit: the commit is stopped" in result.stderr)
                self.assertEqual(done, want, result.stdout + result.stderr)
                if trigger:
                    (self.calls / trigger).unlink()
                    self.git("reset", "-q")
        self.assertIn("-x scripts/s0.sh scripts/s1.sh scripts/s2.sh", (self.calls / "shellcheck.log").read_text())

    def test_pre_commit_hook_checks_the_staged_blobs_not_the_working_tree(self):
        # Thread 4305945406: a malformed staged blob stops the commit even when the working-tree copy is fixed.
        stub = '#!/usr/bin/env bash\nfor f in "$@"; do [[ ! -f $f ]] || ! grep -q BAD -- "$f" || exit 1; done\n'
        (self.temp / "bin/shfmt").write_text(stub)
        self.write("scripts/s.sh", "#!/usr/bin/env bash\necho BAD\n")
        self.git("add", "scripts/s.sh")
        self.write("scripts/s.sh", "#!/usr/bin/env bash\necho fixed\n")
        refused = self.hooked_commit()
        out = refused.stdout + refused.stderr
        self.assertEqual((refused.returncode, "failed: shfmt" in out), (1, True), out)
        self.git("add", "scripts/s.sh")
        self.assertEqual(self.hooked_commit().returncode, 0)

    def push(self, branch, *commits):
        """Commit each {path: bytes} on a new branch from main, push it through the hooks and return (exit, stderr)."""
        self.git("config", "core.hooksPath", str(ROOT / ".githooks"))
        self.git("switch", "-q", "-c", branch, "main")
        for files in commits:
            for rel, data in files.items():
                self.write(rel, data)
            self.git("add", "--", *files)  # only these, never the precheck's untracked evidence
            self.git("commit", "-q", "--no-verify", "-m", branch)
        env = {**self.env, "PATH": os.environ["PATH"]}  # the real uv and the real detector
        run = ["git", "push", "origin", branch]
        result = subprocess.run(run, cwd=self.repo, env=env, capture_output=True, text=True, timeout=300, check=False)
        self.assertNotIn(TOKEN, result.stdout + result.stderr)
        self.assertEqual(bool(self.git("ls-remote", "origin", branch)), result.returncode == 0, result.stderr)
        return result.returncode, result.stderr

    def secrets_ok(self):
        """The precheck's `secrets` check on the current branch: the shared per-blob scan with the real detector."""
        result = self.precheck()
        logs = "".join(p.read_text() for p in (self.repo / f".orchestration/{TASK}").glob("precheck-*.log"))
        self.assertNotIn(TOKEN, result.stdout + result.stderr + logs)
        return next(c for c in self.record()["checks"] if c["name"] == "secrets")["ok"]

    def test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern(self):
        # Thread 4305945403: a token added and removed again before the push is still in the pushed history.
        secret, clean = {"value.txt": f"value={TOKEN}\n".encode()}, {"value.txt": b"value=clean\n"}
        for branch, commits in (("secret", [secret]), ("removed", [secret, clean]), ("clean", [clean])):
            with self.subTest(branch=branch):
                code, err = self.push(branch, *commits)
                self.assertEqual(code != 0, branch != "clean", err)
                self.assertEqual(bool(re.search(MATCH, err)), branch != "clean", err)

    def test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit(self):
        # Local review of a5cb73b4 (P1, pre-push:19-20): binary classification never hides pushed content (a03 item 4).
        secret, clean, cred = f"key={TOKEN}\n".encode(), b"key=clean\n", {".gitattributes": b"*.cred -diff\n"}
        for branch, commits, refusal in (
            ("diff-attr", [{**cred, "a.cred": secret}], MATCH),
            ("binary-attr", [{".gitattributes": b"*.dat binary\n", "a.dat": secret}], MATCH),
            ("nul", [{"a.bin": b"\x00\x01" + secret + b"\x00"}], DECODING),
            ("added-then-removed", [{**cred, "a.cred": secret}, {"a.cred": clean}], MATCH),
            ("diff-attr-clean", [{**cred, "a.cred": clean}], None),
            ("nul-clean", [{"a.bin": b"\x00\x01" + clean + b"\x00"}], DECODING),
        ):
            with self.subTest(branch=branch):
                code, err = self.push(branch, *commits)
                self.assertEqual(code != 0, bool(refusal), err)
                self.assertRegex(err, refusal or r"^(?![\s\S]*pre-push:)")  # a clean push prints no hook line
        self.git("switch", "-q", "diff-attr")  # the precheck's per-blob scan: a -diff attribute hides nothing there
        self.assertIs(self.secrets_ok(), False)

    def test_pre_push_scans_each_blob_on_its_own_boundary(self):
        # Local review of 9cd5514 (P1, pre-push:27): a blob's last word never joins the token opening the next blob.
        code, err = self.push("joined", {"a.txt": b"word", "b.txt": TOKEN.encode() + b"\n"})
        self.assertEqual(code, 1, err)
        self.assertRegex(err, MATCH)

    def test_pre_push_scans_each_blob_on_its_own_and_keeps_json_decoding(self):
        # Local review of 4ed1b27 (P1, pre-push:27-31): a JSON-escaped credential is found in its own document.
        cred, clean = b'{"key": "\\u0067' + TOKEN[1:].encode() + b'"}\n', b'{"key": "clean"}\n'
        for data, code in ((cred, 1), (cred + clean, 0)):
            (self.temp / "joined.json").write_bytes(data)
            self.assertEqual(self.scan(self.temp / "joined.json").returncode, code)
        code, err = self.push("json", {"a.json": cred, "b.json": clean})
        self.assertEqual(code, 1, err)
        self.assertRegex(err, MATCH)
        self.assertIs(self.secrets_ok(), False)
        self.assertEqual(self.push("json-clean", {"a.json": clean, "b.json": clean})[0], 0)

    def test_pre_push_fails_closed_on_an_undecodable_blob(self):
        # a03 item 5: a blob the detector cannot decode stops the push as a decoding failure, never as a match.
        code, err = self.push("undecodable", {"a.dat": b"key=\xc3\x28 clean\n"})
        self.assertEqual(code, 1, err)
        self.assertRegex(err, DECODING)
        self.assertNotRegex(err, MATCH)
        self.assertIs(self.secrets_ok(), False)
        self.assertEqual(self.push("decodable", {"a.dat": b"key=clean\n"})[0], 0)

    def test_pre_push_reports_home_path_rewrites_only_under_orchestration(self):
        # Local review of 4ed1b27 (P2, result-precheck.sh:98-103): a home path is refused only under .orchestration/.
        doc = b"Example: /Users/example/.config/tool.toml\n"
        self.assertEqual(self.push("public", {"docs/guide.md": doc})[0], 0)
        self.assertIs(self.secrets_ok(), True)
        code, err = self.push("evidence", {".orchestration/x/report.md": doc})
        self.assertEqual(code, 1, err)
        self.assertRegex(err, r"pre-push: home-path: \.orchestration/x/report\.md ")
        self.assertNotRegex(err, MATCH)
        self.assertIs(self.secrets_ok(), False)

    def test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan(self):
        # Local review of 9cd5514 (P1, result-precheck.sh:85): UTF-16 decodes with a BOM and is refused without;
        # plain UTF-8 counts the same, and `--secrets` neither prints nor changes its input.
        blob, found, refused = self.temp / "blob", r"^secrets: 1 match\(es\)\n$", "^decoding: "
        for encoding, stdout in (("utf-8", found), ("utf-16", found), ("utf-16-le", refused), ("utf-16-be", refused)):
            with self.subTest(encoding=encoding):
                blob.write_bytes(f"key={TOKEN}\r\n".encode(encoding))
                result = self.scan(blob)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertRegex(result.stdout, stdout)
                self.assertNotIn(TOKEN, result.stdout + result.stderr)
                self.assertEqual(blob.read_bytes(), f"key={TOKEN}\r\n".encode(encoding))
        blob.write_bytes("key=clean\r\n".encode("utf-16"))
        self.assertEqual(self.scan(blob).returncode, 0)

    def proofs(self, lib, case, cases):  # previous and current lib.py, a new test module; each selector's proof
        self.write("lib.py", "VALUE = 1\n")
        previous = self.commit("previous code")
        self.write("lib.py", lib)
        self.write("tests/unit/test_new.py", "import unittest\n\nimport lib\n\n\nclass T(unittest.TestCase):\n" + case)
        self.commit("this head")  # the previous head lacks the module, so it runs this head's copy
        for name, ok in cases:
            with self.subTest(name=name):
                result = self.precheck("--previous-head", previous, "--check", f"tests/unit/test_new.py::{name}")
                self.assertEqual(result.returncode, 0 if ok else 1, result.stdout + result.stderr)
                self.assertIs(self.record()["selectors"][0]["ok"], ok)
        return previous

    def test_previous_head_proof_requires_an_executed_failing_test(self):
        # Local review of 9cd5514 (P2, result-precheck.sh:250): only an executed test failing by assertion is red proof.
        case = "    def test_value(self):\n        self.assertEqual(lib.VALUE, 2)\n\n"  # fails on the previous code
        case += "    def test_always(self):\n        self.assertTrue(lib.VALUE)\n\n"  # passes on both
        case += "    def test_helper(self):\n        from lib import helper\n\n        self.assertEqual(helper(), 2)\n"
        cases = (("test_value", True), ("test_always", False), ("test_helper", False), ("test_none", False))
        self.proofs("VALUE = 2\n\n\ndef helper():\n    return 2\n", case, cases)
        self.assertEqual(len(self.git("worktree", "list").splitlines()), 1)
        self.assertNotIn("worktree prune", PRECHECK.read_text())

    def test_previous_head_proof_selects_tests_by_exact_id(self):
        # The audit of bccb2de (P2) and amendment 1: a proof runs one exact test; a name two classes define runs none.
        case = "    def test_requested(self):\n        pass\n\n    def test_requested_extra(self):\n"
        case += "        self.assertEqual(lib.VALUE, 2)\n\n    def test_twice(self):\n        pass\n\n\n"
        case += "class U(unittest.TestCase):\n    def test_twice(self):\n        pass\n"
        cases = (("test_requested", False), ("test_twice", False), ("test_requested_extra", True))
        previous, proof = self.proofs("VALUE = 2\n", case, cases), self.record()["selectors"][0]  # requested_extra's
        keys = ("id", "previous_head", "previous_head_tests", "previous_head_exit", "head_tests", "head_exit")
        want = ("tests.unit.test_new.T.test_requested_extra", previous, 1, 1, 1, 0)
        self.assertEqual(tuple(proof.get(k) for k in keys), want)


if __name__ == "__main__":
    unittest.main()
