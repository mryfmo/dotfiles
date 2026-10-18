"""Exercise dispositions.py on a temporary repository: base, the thread's commit, a fix on line 10, a later change on line 1.

The tool runs as `python -I` from this interpreter with the repository as its working directory; a thread's commit comes
from `--commits` except in the hold case, where a stub `gh` that fails is first on PATH.
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "scripts/orchestrator/dispositions.py"
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
STUB_TEST = "import unittest\n\n\nclass T(unittest.TestCase):\n    def test_pass(self):\n        pass\n\n"
STUB_TEST += "    def test_fail(self):\n        self.fail('the stub fails')\n"
REASON = "not-applicable:the finding does not reach this line"


def thread(n, line, disposition=""):
    url = f"https://github.com/o/r/pull/7#discussion_r{n}"
    return {
        "source": "review_comment",
        "path": "a.py",
        "line": line,
        "url": url,
        "body": "b",
        "disposition": disposition,
    }


class DispositionsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo = self.temp / "repo"
        (self.repo / "tests/unit").mkdir(parents=True)
        (self.repo / "tests/unit/test_stub.py").write_text(STUB_TEST)
        lines = [f"line {n}\n" for n in range(1, 31)]
        self.git("init", "-q", "-b", "main")
        self.base = self.commit(lines, "base")
        self.thread_commit = self.commit(lines, "the thread's commit", extra="b.py")
        self.fix = self.commit(lines[:9] + ["line 10 fixed\n"] + lines[10:], "fix line 10")
        self.head = self.commit(["line 1 renamed\n"] + lines[1:9] + ["line 10 fixed\n"] + lines[10:], "touch line 1")

    def git(self, *args):
        run = ["git", "-c", "commit.gpgsign=false", *args]
        env = {**os.environ, **GIT_ENV}
        return subprocess.run(run, cwd=self.repo, env=env, capture_output=True, text=True, check=True).stdout.strip()

    def commit(self, lines, message, extra=None):
        (self.repo / "a.py").write_text("".join(lines))
        if extra:
            (self.repo / extra).write_text("extra\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")

    def run_tool(self, items, *args, commits=None, path=None):
        sweep = {"repo": "o/r", "pr": 7, "head_sha": self.head, "base_sha": self.base, "items": items}
        (self.temp / "sweep.json").write_text(json.dumps(sweep))
        if commits is not None:
            (self.temp / "commits.json").write_text(json.dumps(commits))
            args = (*args, "--commits", str(self.temp / "commits.json"))
        run = [sys.executable, "-I", str(TOOL), "7", self.head, "--feedback", str(self.temp / "sweep.json"), *args]
        env = {**os.environ, "PATH": path or os.environ["PATH"]}
        result = subprocess.run(run, cwd=self.repo, env=env, capture_output=True, text=True, timeout=300, check=False)
        return result.returncode, result.stdout, result.stderr

    def test_dispositions_proposes_fixed_for_a_changed_hunk_and_demands_not_applicable_otherwise(self):
        comment = {"source": "issue_comment", "url": "https://github.com/o/r/pull/7#issuecomment-1", "disposition": ""}
        items = [thread(1, 10), thread(2, 25, REASON + "; evidence=grep -c x a.py"), comment]
        commits = {item["url"]: self.thread_commit for item in items[:2]}
        code, out, err = self.run_tool(items, commits=commits)
        self.assertEqual(code, 0, err)
        result = json.loads(out)["items"]
        self.assertEqual([i.get("proposal") for i in result], [f"fixed:{self.fix}", "not-applicable:", None])
        self.assertEqual([i["disposition"] for i in result], [i["disposition"] for i in items])
        self.assertIn(f"discussion_r1 proposal fixed:{self.fix}", err)

    def test_require_refutation_fails_without_a_form_and_accepts_each_of_the_three(self):
        page = self.temp / "page.html"
        page.write_text("<html><body><p>The quoted   <b>sentence</b> stands.</p></body></html>\n")

        def source(quote):
            return "source:" + json.dumps({"url": page.as_uri(), "fetched_at": "2026-10-18T00:00:00Z", "quote": quote})

        forms = {
            "none": (25, "", False),
            "legacy": (25, "grep -c x a.py", False),
            "test-pass": (25, "test:tests/unit/test_stub.py::test_pass", True),
            "test-fail": (25, "test:tests/unit/test_stub.py::test_fail", False),
            "source-quote": (25, source("The quoted sentence stands."), True),
            "source-missing": (25, source("a sentence the page lacks"), False),
            "diff-untouched": (25, f"diff:{self.thread_commit}..{self.head}", True),
            "diff-touched": (10, f"diff:{self.thread_commit}..{self.head}", False),
        }
        items = [
            thread(n, line, REASON + (f"; evidence={ev}" if ev else ""))
            for n, (line, ev, _) in enumerate(forms.values())
        ]
        commits = {item["url"]: self.thread_commit for item in items}
        code, out, err = self.run_tool(items, "--require-refutation", commits=commits)
        self.assertEqual(code, 1, err)
        result = json.loads(out)["items"]
        self.assertEqual([i["refutation"]["ok"] for i in result], [ok for _, _, ok in forms.values()], err)
        self.assertEqual(
            [i["refutation"]["form"] for i in result],
            ["none", "legacy-evidence", "test", "test", "source", "source", "diff", "diff"],
        )
        self.assertEqual(err.count(" FAIL: "), 5, err)
        self.assertTrue(result[2]["refutation"]["record"].endswith("OK"), result[2])
        self.assertEqual(result[4]["refutation"]["record"], f"sha256={hashlib.sha256(page.read_bytes()).hexdigest()}")
        # Without the flag the same failures are a report: exit 0, nothing marked FAIL.
        code, _, err = self.run_tool(items, commits=commits)
        self.assertEqual((code, err.count(" FAIL: "), err.count(" unverified: ")), (0, 0, 5), err)

    def test_dispositions_holds_on_an_unreadable_sweep_or_a_missing_commit(self):
        (self.temp / "sweep.json").write_text("{not json")
        run = [sys.executable, "-I", str(TOOL), "7", self.head, "--feedback", str(self.temp / "sweep.json")]
        result = subprocess.run(run, cwd=self.repo, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("hold: unreadable input", result.stderr)
        code, _, err = self.run_tool([thread(1, 10)], commits={thread(1, 10)["url"]: "f" * 40})
        self.assertEqual(code, 2, err)
        self.assertIn(f"hold: the thread commit '{'f' * 40}' is not a commit here", err)
        # No commit in the sweep or --commits: gh is asked, and its failure is a hold, not a guess.
        stub = self.temp / "stub"
        stub.mkdir()
        (stub / "gh").write_text("#!/bin/sh\necho 'gh: offline' >&2\nexit 1\n")
        (stub / "gh").chmod(0o755)
        code, out, err = self.run_tool([thread(1, 10)], path=f"{stub}{os.pathsep}{os.environ['PATH']}")
        self.assertEqual(code, 2, err)
        self.assertIn("hold: gh api repos/o/r/pulls/comments/1 failed: gh: offline", err)
        self.assertIsNone(json.loads(out)["items"][0]["proposal"])


if __name__ == "__main__":
    unittest.main()
