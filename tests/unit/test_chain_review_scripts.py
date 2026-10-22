"""Exercise the review-side chain scripts (plan 021 step 6.3) in a temporary git repository.

Each script runs as a subprocess from this checkout with the temporary repository as its working directory, so the
repository root it resolves is the temporary one. git is the real one. A stub review binary appends its argv, its
working directory, the HEAD there, PATH and its stdin to `<calls>/<name>.log`, prints `<calls>/transcript` and exits with
`<calls>/status` (0 when absent).
"""

import hashlib
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.unit.test_pr_feedback import GhFixture

TOOLS = Path(__file__).resolve().parents[2] / "scripts/orchestrator"
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
STUB = (
    "#!/usr/bin/env bash\n"
    '{{ printf "argv:"; printf " %s" "$@"; printf "\\ncwd: %s\\nhead: %s\\npath: %s\\nstdin: %s\\n" '
    '"$(pwd -P)" "$(/usr/bin/git rev-parse HEAD)" "$PATH" "$(/bin/cat)"; }} >> "{calls}/{name}.log"\n'
    '{record}/bin/cat "{calls}/transcript"\nexit "$(/bin/cat "{calls}/status" 2> /dev/null || echo 0)"\n'
)
ARGV = "argv: --profile review -s read-only review --base main"
SCAN_HIT = "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"


class ChainReviewScriptsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.binding = GhFixture(self.temp / "gh-binding")
        self.repo = self.temp / "repo"
        self.repo.mkdir()
        self.calls = self.temp / "calls"
        self.calls.mkdir()
        self.git("init", "-q", "-b", "main")
        source = self.write("scripts/pr-feedback.py", (TOOLS.parent / "pr-feedback.py").read_text())
        self.git("add", str(source))
        self.write("a.txt", "a\n")
        self.git("add", "a.txt")
        self.git("commit", "-q", "-m", "main")
        self.env = {**self.binding.env, **GIT_ENV, "CALLS": str(self.calls), "TMPDIR": str(self.temp)}
        for name in ("CODEX_BIN", "ORCH_REVIEW_WORKTREE"):
            self.env.pop(name, None)

    def git(self, *args, cwd=None):
        return self.binding.git(cwd or self.repo, *args)

    def write(self, rel, text, root=None):
        path = (root or self.repo) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def stub(self, path, name):
        path.parent.mkdir(parents=True, exist_ok=True)
        record = f'for p in "$PATH"/*; do printf "%s %s\\n" "$p" "$(/usr/bin/readlink "$p")"; done >> "{self.calls}/{name}.path"\n'
        path.write_text(STUB.format(name=name, calls=self.calls, record=record))
        path.chmod(0o755)

    def mise(self, body):
        """A mise stub first on PATH; it runs under env -i, so it carries the calls directory itself."""
        path = self.temp / "bin/mise"
        path.parent.mkdir(parents=True, exist_ok=True)
        log = f'echo "argv: $* MISE_CONFIG_FILE=${{MISE_CONFIG_FILE:-unset}}" >> "{self.calls}/mise.log"\n'
        self.binding.executable(self.temp / "bin/uv", f'#!/bin/bash\nprintf "%s\\n" "{self.binding.python}"\n')
        fixed = f'[[ $2 != uv ]] || {{ printf "%s\\n" "{self.temp}/bin/uv"; exit; }}\n'
        fixed += '[[ $2 != git ]] || { printf "%s\\n" /usr/bin/git; exit; }\n'
        path.write_text("#!/bin/bash\n" + fixed + log + body)
        path.chmod(0o755)

    def review_head(self, name="review"):
        """A clean review worktree at main, a head commit made in it, codex stubbed and mise failing on PATH."""
        review = self.temp / name
        self.git("worktree", "add", "-q", "--detach", str(review), "main")
        self.write("b.txt", "b\n", root=review)
        self.git("add", "b.txt", cwd=review)
        self.git("commit", "-q", "-m", "head", cwd=review)
        head = self.git("rev-parse", "HEAD", cwd=review)
        self.git("checkout", "-q", "--detach", "main", cwd=review)
        self.stub(self.temp / "bin/codex", "codex")
        self.mise("exit 1\n")
        (self.repo / ".orchestration/validation").mkdir(parents=True, exist_ok=True)
        path = f"{self.temp / 'bin'}{os.pathsep}{self.binding.env['PATH']}"
        return review, head, {"ORCH_REVIEW_WORKTREE": str(review), "PATH": path}

    def log(self, name):
        path = self.calls / f"{name}.log"
        text = path.read_text() if path.exists() else ""
        paths = re.findall(r"^path: (.+)$", text, re.MULTILINE)
        if paths:
            expected = {}
            for private in paths:
                self.assertEqual(1, len(private.split(os.pathsep)))
                self.assertEqual(self.temp, Path(private).parent)
                expected |= {f"{private}/gh": str(self.binding.target), f"{private}/git": "/usr/bin/git"}
                text = text.replace(f"path: {private}\n", "path: checked gh/git\n")
            links = dict(line.split(" ", 1) for line in (self.calls / f"{name}.path").read_text().splitlines())
            self.assertEqual(expected, links)
        return text

    def run_tool(self, name, *args, code=0, env=None, cwd=None):
        # The review binary must not read what the caller's stdin holds.
        result = subprocess.run(
            ["bash", str(TOOLS / name), *map(str, args)],
            capture_output=True,
            text=True,
            input="caller stdin\n",
            cwd=cwd or self.repo,
            env={**self.env, **(env or {})},
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result.stdout

    def test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file(self):
        review = self.temp / "review"
        self.git("worktree", "add", "-q", "--detach", str(review), "main")
        # The head commit, made in the review worktree, carries a decoy bin/codex; the main working tree never does.
        self.stub(review / "bin/codex", "decoy")
        self.write("b.txt", "b\n", root=review)
        self.git("add", "bin/codex", "b.txt", cwd=review)
        self.git("commit", "-q", "-m", "head", cwd=review)
        head, base = self.git("rev-parse", "HEAD", cwd=review), self.git("rev-parse", "main")
        self.git("checkout", "-q", "--detach", "main", cwd=review)
        self.stub(self.temp / "bin/codex", "codex")
        self.mise("exit 1\n")
        (self.repo / ".orchestration/validation").mkdir(parents=True)
        path = f"./bin{os.pathsep}{self.temp / 'bin'}{os.pathsep}{self.binding.env['PATH']}"
        env = {"ORCH_REVIEW_WORKTREE": str(review), "PATH": path}
        # An earlier marker's message is not the final one; the worktree prefix is stripped; a repeated line counts once.
        final = f"One finding.\n- [P2] {review}/b.txt:1 b is new\n- [P2] {review}/b.txt:1 b is new\n"
        (self.calls / "transcript").write_text(f"codex\n- [P1] {review}/a.txt:1 superseded\ncodex\n{final}")
        finding = "- [P2] b.txt:1 b is new"
        call = f"{ARGV}\ncwd: {review}\nhead: {head}\npath: checked gh/git\nstdin: \n"

        def out(task):
            return self.repo / f".orchestration/validation/{task}-local-review-{head[:7]}.md"

        with self.subTest("a review worktree path without its own .git entry exits 2"):
            # First, while the main working tree is clean: the dirty check alone would pass it.
            (self.repo / "plain").mkdir()
            plain = {**env, "ORCH_REVIEW_WORKTREE": str(self.repo / "plain")}
            self.assertIn("is not a worktree root", self.run_tool("local-review.sh", "t-p", head, 9, code=2, env=plain))
            self.assertEqual("", self.log("codex"))
            self.assertEqual(base, self.git("rev-parse", "HEAD"))
        with self.subTest("CODEX_BIN unset: codex resolved in the root before the checkout"):
            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
            self.assertEqual(f"{finding}\nlocal-review: 1 findings ({out('t-a')})\n", stdout)
            self.assertEqual(call, self.log("codex"))
            self.assertEqual("", self.log("decoy"))
            self.assertEqual(head, self.git("rev-parse", "HEAD", cwd=review))
            status = self.git("status", "--porcelain", "--untracked-files=all")
            self.assertEqual(f"?? .orchestration/validation/t-a-local-review-{head[:7]}.md", status)
            text = out("t-a").read_text()
            front = f"---\ntask: t-a\nhead: {head}\npr: 9\nbase: {base}\nstarted: .+\nfinished: .+\nfindings: 1\n"
            self.assertRegex(text, "^" + re.escape(front).replace(r"\.\+", ".+"))
            self.assertIn("engine: codex review --base main (profile review, read-only)\n---\n", text)
            self.assertIn(f"\n{finding}\n\n```text\nOne finding.\n{finding}\n{finding}\n```\n", text)
            self.assertNotIn("superseded", text)
            self.assertEqual([], list(self.temp.glob("local-review.*")))
        self.git("checkout", "-q", "--detach", "main", cwd=review)
        with self.subTest("CODEX_BIN set: that binary runs, a relative path resolved in the root"):
            self.stub(self.repo / "seam/review-binary", "seam")
            seam = {**env, "CODEX_BIN": "seam/review-binary"}
            self.run_tool("local-review.sh", "t-b", head, 9, code=3, env=seam, cwd=self.repo / ".orchestration")
            self.assertEqual(call, self.log("seam"))
            self.assertEqual(call, self.log("codex"))
        with self.subTest("one review per head: the file is reused"):
            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
            self.assertEqual(f"{finding}\nlocal-review: 1 findings (existing {out('t-a')})\n", stdout)
            self.assertEqual(call, self.log("codex"))
        (self.calls / "transcript").write_text("codex\nNo findings.\n")
        with self.subTest("no finding exits 0"):
            stdout = self.run_tool("local-review.sh", "t-c", head, 9, env=env)
            self.assertEqual(f"\nlocal-review: 0 findings ({out('t-c')})\n", stdout)
            self.assertIn("findings: 0\n", out("t-c").read_text())
        missing = {**env, "CODEX_BIN": "seam/missing"}
        self.assertIn("no review binary", self.run_tool("local-review.sh", "t-d", head, 9, code=2, env=missing))
        self.write("dirty.txt", "x\n", root=review)
        with self.subTest("a dirty review worktree or an unknown head exits 2 and runs nothing"):
            self.assertIn("is not clean", self.run_tool("local-review.sh", "t-d", head, 9, code=2, env=env))
            unknown = "0" * 40
            self.assertIn("is not a local commit", self.run_tool("local-review.sh", "t-d", unknown, 9, code=2, env=env))
            self.assertEqual(2, self.log("codex").count(ARGV))
            self.assertFalse(out("t-d").exists())

    def test_local_review_writes_no_file_when_the_review_binary_fails(self):
        # PR #357 thread 4270918132 and local:b6ce4ff:1: a failed review is no sample, so nothing is left to reuse.
        _, head, env = self.review_head()
        out = self.repo / f".orchestration/validation/t-a-local-review-{head[:7]}.md"
        (self.calls / "transcript").write_text("codex\nNo findings.\n")
        (self.calls / "status").write_text("5")
        stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=4, env=env)
        self.assertIn("local-review: codex exited 5; no review file written (transcript ", stdout)
        self.assertFalse(out.exists())
        (self.calls / "status").unlink()
        self.assertEqual(
            f"\nlocal-review: 0 findings ({out})\n", self.run_tool("local-review.sh", "t-a", head, 9, env=env)
        )
        self.assertEqual(2, self.log("codex").count(ARGV))

    def test_local_review_reuses_only_a_file_that_records_this_head(self):
        # PR #357 thread 4270918140 and local:b6ce4ff:2: the file name keeps seven characters of the head.
        review, head, env = self.review_head()
        other = head[:7] + ("0" if head[7] != "0" else "1") * 33
        out = self.write(
            f".orchestration/validation/t-a-local-review-{head[:7]}.md", f"---\nhead: {other}\nfindings: 0\n---\n"
        )
        self.assertIn(
            "records another head; not reused", self.run_tool("local-review.sh", "t-a", head, 9, code=2, env=env)
        )
        self.assertEqual("", self.log("codex"))
        self.assertEqual(self.git("rev-parse", "main"), self.git("rev-parse", "HEAD", cwd=review))
        out.write_text(f"---\nhead: {head}\nfindings: 0\n---\n")
        stdout = self.run_tool("local-review.sh", "t-a", head, 9, env=env)
        self.assertEqual(f"\nlocal-review: 0 findings (existing {out})\n", stdout)
        self.assertEqual("", self.log("codex"))

    def test_local_review_resolves_codex_through_mise_and_refuses_a_shim(self):
        # audit:b6ce4ff:1 (operator decision A's P1): codex is what mise which answers under env -i, never a shim.
        review, head, env = self.review_head()
        (self.calls / "transcript").write_text("codex\nNo findings.\n")
        self.stub(self.temp / "installs/codex", "installed")
        env["MISE_CONFIG_FILE"] = str(self.temp / "payload.toml")
        self.mise(f'printf "%s\\n" "{self.temp}/mise/shims/$2"\n')
        self.assertIn(
            "is under a shims directory; refused", self.run_tool("local-review.sh", "t-a", head, 9, code=2, env=env)
        )
        self.assertEqual(self.git("rev-parse", "main"), self.git("rev-parse", "HEAD", cwd=review))
        # mise knows codex only, so the stub's own env-shebang interpreter (bash) falls back to command -v.
        self.mise(f'[[ $2 == codex ]] && printf "%s\\n" "{self.temp}/installs/$2"\n')
        self.run_tool("local-review.sh", "t-a", head, 9, env=env)
        self.assertEqual(1, self.log("installed").count(ARGV))
        self.assertEqual("", self.log("codex"))
        asked = [f"argv: which {name} MISE_CONFIG_FILE=unset" for name in ("codex", "codex", "bash")]
        self.assertEqual(asked, self.log("mise").splitlines())

    def test_local_review_resolves_the_review_binary_before_the_checkout(self):
        # audit:b6ce4ff:4: mise answers while the review worktree is still where the run found it, not at the head.
        review, head, env = self.review_head()
        (self.calls / "transcript").write_text("codex\nNo findings.\n")
        self.stub(self.temp / "installs/codex", "installed")
        self.mise(
            f'[[ $2 == codex ]] || exit 1\ngit -C "{review}" rev-parse HEAD > "{self.calls}/mise-head"\n'
            f'printf "%s\\n" "{self.temp}/installs/$2"\n'
        )
        self.run_tool("local-review.sh", "t-a", head, 9, env=env)
        self.assertEqual(self.git("rev-parse", "main"), (self.calls / "mise-head").read_text().strip())
        self.assertIn(f"head: {head}\n", self.log("installed"))

    def test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory(self):
        # audit:b6ce4ff:2: a / in the task id or the head would place the file outside its directory.
        _, head, env = self.review_head()
        for task, commit in (("../escape", head), ("a/b", head), ("t-a", "../../x" + head[7:]), ("t-a", head[:7])):
            with self.subTest(task=task, commit=commit):
                self.assertIn("usage:", self.run_tool("local-review.sh", task, commit, 9, code=2, env=env))
        self.assertEqual("", self.log("codex"))
        self.assertEqual([], list(self.repo.glob(".orchestration/*.md")))
        # A review file one level up, which ../x would read and whose rows it would append to .orchestration/x.md.
        a40 = "a" * 40
        self.write(".orchestration/x-local-review-aaaaaaa.md", "---\nfindings: 1\n---\n\n- [P2] x.sh:1 x\n")
        for task, commit in (("../x", a40), ("t-a", "../" + a40[3:])):
            with self.subTest(task=task, commit=commit):
                self.assertIn("usage:", self.run_tool("local-advisory.sh", task, commit, "t-followup-a01", code=2))
        self.assertFalse((self.repo / ".orchestration/x.md").exists())
        self.assertFalse((self.repo / ".orchestration/acceptance").exists())

    def test_local_review_strips_a_worktree_path_holding_sed_syntax_literally(self):
        # audit:b6ce4ff:3: the worktree path is no part of a sed program.
        review, head, env = self.review_head("re[1]#view")
        (self.calls / "transcript").write_text(f"codex\n- [P2] {review}/b.txt:1 b is new\n")
        out = self.repo / f".orchestration/validation/t-a-local-review-{head[:7]}.md"
        stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
        self.assertEqual(f"- [P2] b.txt:1 b is new\nlocal-review: 1 findings ({out})\n", stdout)
        self.assertIn("```text\n- [P2] b.txt:1 b is new\n```\n", out.read_text())

    def test_local_review_pins_the_review_binary_interpreter(self):
        # The audit of c45f9b5: a binary whose first line is an env shebang runs under the interpreter mise which
        # answers in the root, never one PATH finds in the PR worktree.
        review, head, env = self.review_head()
        (self.calls / "transcript").write_text("codex\nNo findings.\n")
        binary = self.temp / "installs/codex"
        self.stub(binary, "codex")
        binary.write_text(binary.read_text().replace("#!/usr/bin/env bash\n", "#!/usr/bin/env -S interp --flag\n"))
        interp = self.temp / "installs/interp"
        interp.write_text(
            f'#!/bin/bash\nprintf "%s\\n" "$*" > "{self.calls}/interp.argv"\nshift\nexec /bin/bash "$@"\n'
        )
        interp.chmod(0o755)
        out = self.repo / f".orchestration/validation/t-a-local-review-{head[:7]}.md"
        with self.subTest("the interpreter mise answers runs the binary"):
            self.mise(f'printf "%s\\n" "{self.temp}/installs/$2"\n')
            self.run_tool("local-review.sh", "t-a", head, 9, env=env)
            self.assertEqual(
                f"--flag {binary} {ARGV.removeprefix('argv: ')}\n", (self.calls / "interp.argv").read_text()
            )
            self.assertEqual(1, self.log("codex").count(ARGV))
        out.unlink()
        (self.calls / "interp.argv").unlink()
        self.git("checkout", "-q", "--detach", "main", cwd=review)
        with self.subTest("an interpreter under a shims directory is refused before the checkout"):
            self.mise(f'[[ $2 == codex ]] && printf "%s\\n" "{binary}" || printf "%s\\n" "{self.temp}/mise/shims/$2"\n')
            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=2, env=env)
            self.assertIn("review binary's interpreter", stdout)
            self.assertIn("is under a shims directory; refused", stdout)
            self.assertEqual(self.git("rev-parse", "main"), self.git("rev-parse", "HEAD", cwd=review))
            self.assertFalse(out.exists())
            self.assertFalse((self.calls / "interp.argv").exists())

    def test_local_review_keeps_env_S_shebang_arguments(self):
        # The local review of 850fc54e: env -S passes the rest of its line to the interpreter, so those words
        # come between the interpreter and the binary.
        _, head, env = self.review_head()
        (self.calls / "transcript").write_text("codex\nNo findings.\n")
        binary = self.temp / "installs/codex"
        self.stub(binary, "codex")
        binary.write_text(
            binary.read_text().replace("#!/usr/bin/env bash\n", "#!/usr/bin/env -S fakeinterp --flag x\n")
        )
        interp = self.temp / "installs/fakeinterp"
        interp.write_text(
            f'#!/bin/bash\nprintf "%s %s\\n" "$0" "$*" > "{self.calls}/fakeinterp.argv"\nshift 2\nexec /bin/bash "$@"\n'
        )
        interp.chmod(0o755)
        self.mise(f'printf "%s\\n" "{self.temp}/installs/$2"\n')
        self.run_tool("local-review.sh", "t-a", head, 9, env=env)
        expected = f"{interp} --flag x {binary} {ARGV.removeprefix('argv: ')}\n"
        self.assertEqual(expected, (self.calls / "fakeinterp.argv").read_text())
        self.assertEqual(1, self.log("codex").count(ARGV))

    def test_local_review_refuses_a_quoted_env_S_shebang(self):
        # audit:2e3ff49:1: env -S quotes, escapes, expands and comments where read -a does not; refused before the checkout.
        review, head, env = self.review_head()
        binary = self.temp / "installs/codex"
        interp = self.temp / "installs/fakeinterp"
        interp.parent.mkdir(parents=True, exist_ok=True)
        interp.write_text(f'#!/bin/bash\ntouch "{self.calls}/fakeinterp.ran"\n')
        interp.chmod(0o755)
        self.mise(f'printf "%s\\n" "{self.temp}/installs/$2"\n')
        refused = "local-review: the review binary's env -S shebang holds a quote, an escape, an expansion or a comment"
        for rest in ('--require "/opt/a b/x.js"', "'x'", "a\\ b", "${HOMEX}/lib", "one # two"):
            with self.subTest(rest=rest):
                # Each case starts clean, so a run a mutant lets through cannot decide the next case.
                for path in (self.calls / "fakeinterp.ran", self.calls / "codex.log"):
                    path.unlink(missing_ok=True)
                for path in (self.repo / ".orchestration/validation").iterdir():
                    path.unlink()
                self.git("checkout", "-q", "--detach", "main", cwd=review)
                self.stub(binary, "codex")
                binary.write_text(
                    binary.read_text().replace("#!/usr/bin/env bash\n", f"#!/usr/bin/env -S fakeinterp {rest}\n")
                )
                self.assertIn(refused, self.run_tool("local-review.sh", "t-a", head, 9, code=2, env=env))
                self.assertEqual(self.git("rev-parse", "main"), self.git("rev-parse", "HEAD", cwd=review))
                self.assertEqual([], list((self.repo / ".orchestration/validation").iterdir()))
                self.assertFalse((self.calls / "fakeinterp.ran").exists())
                self.assertEqual("", self.log("codex"))

    def test_local_advisory_records_p2_rows_and_stops_on_p0_p1(self):
        head, owner = "abcdef0" + "1" * 33, "t-followup-a01"
        record = self.write(".orchestration/acceptance/t-a01.md", "# record\n")
        sha = hashlib.sha256(self.write(f".orchestration/tasks/{owner}.md", "owner\n").read_bytes()).hexdigest()
        heading = f"## Owned by {owner} (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n"
        # Numbered in sort order; the second is cut to 120 characters, then loses its backticks.
        first, long = "- [P2] `a.sh:1` first", "- [P2] `b.sh:3` " + "y" * 130

        def review(*findings):
            front = f"---\ntask: t-a01\nfindings: {len(findings)}\n---\n\n"
            # Each finding appears twice, in the list and in the transcript, as the local review writes it.
            text = "\n".join(findings)
            self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", f"{front}{text}\n\n{text}\n")

        def line(n, finding):
            text = finding[:120].replace("`", "")
            return (
                f"local-finding: abcdef0:{n} not-applicable:advisory P2 owned by {owner} ({text}); "
                f"evidence=shasum -a 256 .orchestration/tasks/{owner}.md ({sha})\n"
            )

        review(long, first)
        for _ in range(2):
            stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner)
        self.assertEqual(
            f"local review of abcdef0: 2 finding(s) recorded as advisory under 'Owned by {owner}' in .orchestration/acceptance/t-a01.md\n",
            stdout,
        )
        rows = "local:abcdef0:1\tadvisory-p2\n" + line(1, first)
        rows += "local:abcdef0:2\tadvisory-p2\n" + line(2, long)
        self.assertEqual(f"# record\n\n{heading}\n{rows}", record.read_text())
        record.write_text("# record\n")
        review("- [P1] a.sh:1 blocks", "- [P2] b.sh:2 second")
        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
        self.assertIn("STOP: local finding 1 of abcdef0 is P0/P1: - [P1] a.sh:1 blocks\n", stdout)
        rows = "local:abcdef0:2\tadvisory-p2\n" + line(2, "- [P2] b.sh:2 second")
        self.assertEqual(f"# record\n\n{heading}\n{rows}", record.read_text())
        record.write_text("# record\n")
        review("- [P0] c.sh:1 breaks")
        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
        self.assertIn("STOP: local finding 1 of abcdef0 is P0/P1: - [P0] c.sh:1 breaks\n", stdout)
        self.assertEqual(f"# record\n\n{heading}\n", record.read_text())
        record.write_text("# record\n")
        review()
        self.assertEqual(
            "local review of abcdef0: no findings\n", self.run_tool("local-advisory.sh", "t-a01", head, owner)
        )
        self.assertEqual("# record\n", record.read_text())
        self.assertIn("no local review file", self.run_tool("local-advisory.sh", "t-b01", head, owner, code=2))

    def test_local_advisory_refuses_a_malformed_owner_id(self):
        # The owner is a grep pattern and verbatim record text; a malformed one changes nothing.
        head = "abcdef0" + "1" * 33
        self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", "---\nfindings: 1\n---\n\n- [P2] x\n")
        for owner in ("", "../x", "a b", "a\nb", ".*", "-a"):
            with self.subTest(owner=owner):
                self.assertIn("usage:", self.run_tool("local-advisory.sh", "t-a01", head, owner, code=2))
        self.assertFalse((self.repo / ".orchestration/acceptance").exists())

    def test_local_advisory_matches_the_owner_heading_literally(self):
        # A dotted owner is no wildcard, and a longer id that starts with the owner is another owner.
        head = "abcdef0" + "1" * 33
        self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", "---\nfindings: 1\n---\n\n- [P2] x\n")
        # tXfollowup-a01 matches t.followup-a01 as a regex, anchored or not (the audit of 40f3be4, finding 2).
        near = "# record\n## Owned by t-followupXa01 (x)\n## Owned by t.followup-a01b (x)\n## Owned by tXfollowup-a01 (x)\n"
        record = self.write(".orchestration/acceptance/t-a01.md", near)
        self.write(".orchestration/tasks/t.followup-a01.md", "owner\n")
        self.run_tool("local-advisory.sh", "t-a01", head, "t.followup-a01")
        self.assertEqual(1, record.read_text().count("\n## Owned by t.followup-a01 (advisory P2"))
        self.run_tool("local-advisory.sh", "t-a01", head, "t.followup-a01")
        self.assertEqual(1, record.read_text().count("\n## Owned by t.followup-a01 (advisory P2"))
        self.assertTrue(record.read_text().startswith(near))

    def test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file(self):
        # C-51: no row names an owner task that does not exist, and the evidence replays before the boundary.
        head, owner = "abcdef0" + "1" * 33, "t-followup-a01"
        self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", "---\nfindings: 1\n---\n\n- [P2] x\n")
        record = self.write(".orchestration/acceptance/t-a01.md", "# record\n")
        self.assertIn(
            f"write the owner task {owner} first", self.run_tool("local-advisory.sh", "t-a01", head, owner, code=2)
        )
        self.assertEqual("# record\n", record.read_text())
        owner_file = self.write(f".orchestration/tasks/{owner}.md", "# the owner task\n")
        self.run_tool("local-advisory.sh", "t-a01", head, owner)
        sha = hashlib.sha256(owner_file.read_bytes()).hexdigest()
        [line] = [line for line in record.read_text().splitlines() if line.startswith("local-finding:")]
        self.assertTrue(line.endswith(f"; evidence=shasum -a 256 .orchestration/tasks/{owner}.md ({sha})"), line)

    def test_local_advisory_classes_a_repeat_by_the_earlier_row(self):
        # C-50: a finding found again on a later head takes the class the record gave the earlier finding, so the
        # three-rows rule can count it; the later head's row wins, and a line range is a token.
        owner, v = "t-followup-a01", ".orchestration/validation"
        self.write(f".orchestration/tasks/{owner}.md", "owner\n")
        self.write(
            f"{v}/t-a01-local-review-aaaaaa1.md",
            "---\nfindings: 2\n---\n\n- [P2] scripts/x.sh:12 quoting\n- [P2] scripts/y.sh:3-5 range\n",
        )
        self.write(f"{v}/t-a01-local-review-bbbbbb2.md", "---\nfindings: 1\n---\n\n- [P3] scripts/x.sh:12 again\n")
        rows = "local:aaaaaa1:1\tquoting\nlocal:aaaaaa1:2\trange-case\nlocal:bbbbbb2:1\tenv-s-quoting\n"
        record = self.write(".orchestration/acceptance/t-a01.md", f"# record\n{rows}")
        head = "cccccc3" + "1" * 33
        current = "- [P2] `scripts/x.sh:12` once more\n- [P2] scripts/y.sh:3-5 again\n- [P2] scripts/y.sh:3-9 wider\n- [P2] scripts/z.sh:7 new\n"
        self.write(f"{v}/t-a01-local-review-cccccc3.md", f"---\nfindings: 4\n---\n\n{current}")
        self.run_tool("local-advisory.sh", "t-a01", head, owner)
        text = record.read_text()
        self.assertEqual(
            [
                "local:cccccc3:1\tenv-s-quoting",
                "local:cccccc3:2\trange-case",
                "local:cccccc3:3\tadvisory-p2",  # y.sh:3-9 is another token than y.sh:3-5
                "local:cccccc3:4\tadvisory-p2",
            ],
            re.findall(r"^local:cccccc3:\d\t.*$", text, re.MULTILINE),
        )
        findings = re.findall(r"^local-finding: cccccc3:(\d) .*$", text, re.MULTILINE)
        self.assertEqual(["1", "2", "3", "4"], findings)
        lines = [line for line in text.splitlines() if line.startswith("local-finding: cccccc3:")]
        self.assertIn("(- [P2] scripts/x.sh:12 once more; repeat of local:bbbbbb2:1)", lines[0])
        self.assertIn("(- [P2] scripts/y.sh:3-5 again; repeat of local:aaaaaa1:2)", lines[1])
        self.assertNotIn("repeat of", lines[2] + lines[3])
        # A review without findings needs no owner file and writes no heading.
        empty = "dddddd4" + "1" * 33
        self.write(f"{v}/t-b01-local-review-dddddd4.md", "---\nfindings: 0\n---\n")
        b = self.write(".orchestration/acceptance/t-b01.md", "# record\n")
        self.run_tool("local-advisory.sh", "t-b01", empty, "t-nobody-a01")
        self.assertEqual("# record\n", b.read_text())

    def test_local_advisory_matches_an_earlier_review_id_literally(self):
        # A historical suffix is no regex: a review file named t-a01-local-review-.*.md made `local:.*:1` match an
        # unrelated row, whose class and provenance the repeat then took (the audit of d3e8acf, finding 1). Only a
        # seven-hex suffix names a reviewed head, so t-a01-local-review-notes.md is no earlier review either.
        owner, v = "t-followup-a01", ".orchestration/validation"
        self.write(f".orchestration/tasks/{owner}.md", "owner\n")
        for suffix in (".*", "notes"):
            self.write(
                f"{v}/t-a01-local-review-{suffix}.md", "---\nfindings: 1\n---\n\n- [P2] scripts/x.sh:12 quoting\n"
            )
        rows = "local:notes:1\tnotes-class\nlocal:aaaaaa1:1\tunrelated-class\n"
        record = self.write(".orchestration/acceptance/t-a01.md", f"# record\n{rows}")
        head = "cccccc3" + "1" * 33
        self.write(f"{v}/t-a01-local-review-cccccc3.md", "---\nfindings: 1\n---\n\n- [P2] scripts/x.sh:12 again\n")
        self.run_tool("local-advisory.sh", "t-a01", head, owner)
        text = record.read_text()
        self.assertEqual(["local:cccccc3:1\tadvisory-p2"], re.findall(r"^local:cccccc3:\d\t.*$", text, re.MULTILINE))
        [line] = [line for line in text.splitlines() if line.startswith("local-finding: cccccc3:")]
        self.assertNotIn("repeat of", line)

    def test_local_advisory_reads_the_whole_suffix_after_the_task_prefix(self):
        # The audit of 000c5c6, finding 1: the guard read the text after the last `-local-review-`, so a file named
        # t-a01-local-review-notes-local-review-aaaaaa1.md passed as aaaaaa1 and a repeat took that unrelated row's class.
        owner, v = "t-followup-a01", ".orchestration/validation"
        self.write(f".orchestration/tasks/{owner}.md", "owner\n")
        self.write(
            f"{v}/t-a01-local-review-notes-local-review-aaaaaa1.md",
            "---\nfindings: 1\n---\n\n- [P2] scripts/x.sh:12 quoting\n",
        )
        record = self.write(".orchestration/acceptance/t-a01.md", "# record\nlocal:aaaaaa1:1\tunrelated-class\n")
        head = "cccccc3" + "1" * 33
        self.write(f"{v}/t-a01-local-review-cccccc3.md", "---\nfindings: 1\n---\n\n- [P2] scripts/x.sh:12 again\n")
        self.run_tool("local-advisory.sh", "t-a01", head, owner)
        text = record.read_text()
        self.assertEqual(["local:cccccc3:1\tadvisory-p2"], re.findall(r"^local:cccccc3:\d\t.*$", text, re.MULTILINE))
        [line] = [line for line in text.splitlines() if line.startswith("local-finding: cccccc3:")]
        self.assertNotIn("repeat of", line)
        # A real earlier review of the same task still classes the repeat.
        self.write(f"{v}/t-a01-local-review-aaaaaa1.md", "---\nfindings: 1\n---\n\n- [P2] scripts/x.sh:12 quoting\n")
        record.write_text("# record\nlocal:aaaaaa1:1\tquoting\n")
        self.run_tool("local-advisory.sh", "t-a01", head, owner)
        self.assertIn("local:cccccc3:1\tquoting\n", record.read_text())

    def test_sandbox_scan_prints_the_unsandboxed_mutation_calls(self):
        sandboxes = ".orchestration/sandboxes"
        hit = "| 2 | dangerouslyDisableSandbox: git commit -m wip |"
        self.write(
            f"{sandboxes}/t-a01.md", f"# sandbox\n{hit}\n- The unsandboxed table Counts every git commit > log.\n"
        )
        self.assertEqual(f"2:{hit}\n{SCAN_HIT}\n", self.run_tool("sandbox-scan.sh", "t-a01"))
        # A trailing -fixtures is stripped, and the match ignores case.
        self.write(f"{sandboxes}/t-b01.md", "Outside The Sandbox: GIT ADD x\n")
        self.assertEqual(
            f"1:Outside The Sandbox: GIT ADD x\n{SCAN_HIT}\n", self.run_tool("sandbox-scan.sh", "t-b01-fixtures")
        )
        reads = (
            "| 1 | gh pr view 9 > pr.json (outside the sandbox; reads) |\n| 2 | unsandboxed tee log, lists the PRs |\n"
        )
        self.write(f"{sandboxes}/t-c01.md", reads)
        none = f"sandbox scan: no unsandboxed mutation call in {sandboxes}/t-c01.md\n"
        self.assertEqual(none, self.run_tool("sandbox-scan.sh", "t-c01"))
        self.assertEqual("", self.run_tool("sandbox-scan.sh", "t-d01"))


if __name__ == "__main__":
    unittest.main()
