"""Exercise scripts/orchestrator/ci-rerun.sh with a stub gh only (plan 024 P1-3, T133 item 4).

The test copies the script into a temporary git repository, its root, beside a fixture .github/flakes.yaml, and runs
it with a stub `gh` first on PATH and stdin closed. The stub answers `gh run view` from a JSON map the test writes,
records every argv, and accepts `gh run rerun`; any other call fails. No call reaches GitHub.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUB = """#!@PYTHON@
import json, os, sys
args = sys.argv[1:]
with open(os.environ["GH_LOG"], "a") as log:
    log.write(json.dumps(args) + "\\n")
runs = json.load(open(os.environ["GH_RUNS"]))
if args[:2] == ["run", "view"] and "--json" in args:
    print(json.dumps(runs[args[2]]))
elif args[:2] == ["run", "view"] and "--log-failed" in args:
    print(runs["logs"][args[args.index("--job") + 1]])
elif args[:2] != ["run", "rerun"]:
    sys.exit("stub gh: unexpected call " + " ".join(args))
"""
FLAKES = r"""# Fixture signatures.
- id: snap-timeout
  job: '^public-bootstrap \(ubuntu-'
  log_regex: 'got unexpected HTTP status code 408 via GET to "https://api\.snapcraft\.io/'
  note: fixture
- id: brew-tap
  job: '\(macos-14, '
  log_regex: 'Error: Failed to fetch tap'
  note: fixture
"""
SNAP = 'error: cannot perform: got unexpected HTTP status code 408 via GET to "https://api.snapcraft.io/v2/assertions"'
HEAD = "a" * 40


def job(number, name, conclusion="failure"):
    return {"databaseId": number, "name": name, "conclusion": conclusion, "status": "completed"}


RUNS = {
    "101": {
        "status": "completed",
        "conclusion": "failure",
        "headSha": HEAD,
        "event": "pull_request",
        "jobs": [
            job(1, "public-bootstrap (ubuntu-24.04, client)"),
            job(2, "test (macos-14, client)"),
            job(3, "validate", "success"),
        ],
    },
    "202": {
        "status": "completed",
        "conclusion": "failure",
        "headSha": "b" * 40,
        "event": "pull_request",
        "jobs": [job(4, "public-bootstrap (ubuntu-24.04, server)"), job(5, "test (ubuntu-24.04, client)")],
    },
    "logs": {
        "1": SNAP,
        "2": "Error: Failed to fetch tap homebrew/fixture",
        "4": SNAP,
        "5": "FAIL: test_something\nAssertionError: 1 != 2",
    },
}


class CiRerunTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.t = Path(temp.name).resolve()
        self.repo = self.t / "repo"
        (self.repo / "scripts/orchestrator").mkdir(parents=True)
        (self.repo / ".github").mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        shutil.copy(ROOT / "scripts/orchestrator/ci-rerun.sh", self.repo / "scripts/orchestrator")
        (self.repo / ".github/flakes.yaml").write_text(FLAKES)
        (self.t / "bin").mkdir()
        gh = self.t / "bin/gh"
        gh.write_text(STUB.replace("@PYTHON@", sys.executable))
        gh.chmod(0o755)
        (self.t / "runs.json").write_text(json.dumps(RUNS))
        self.ledger = self.repo / ".orchestration/validation/ci-reruns.tsv"

    def run_script(self, run_id):
        log = self.t / "gh.log"
        log.write_text("")
        result = subprocess.run(
            ["bash", str(self.repo / "scripts/orchestrator/ci-rerun.sh"), run_id],
            env=os.environ
            | {
                "PATH": str(self.t / "bin") + os.pathsep + os.environ["PATH"],
                "GH_LOG": str(log),
                "GH_RUNS": str(self.t / "runs.json"),
            },
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        return result, [json.loads(line) for line in log.read_text().splitlines()]

    def test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature(self):
        result, calls = self.run_script("101")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(1, calls.count(["run", "rerun", "101", "--failed"]))
        rows = [line.split("\t") for line in self.ledger.read_text().splitlines()]
        self.assertEqual(
            [
                ["101", HEAD, "public-bootstrap (ubuntu-24.04, client)", "snap-timeout"],
                ["101", HEAD, "test (macos-14, client)", "brew-tap"],
            ],
            [row[1:] for row in rows],
        )
        self.assertRegex(rows[0][0], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")

        result, calls = self.run_script("101")
        self.assertEqual(4, result.returncode, result.stdout + result.stderr)
        self.assertEqual([], calls)

        before = self.ledger.read_text()
        result, calls = self.run_script("202")
        self.assertEqual(3, result.returncode, result.stdout + result.stderr)
        self.assertIn("real failure: test (ubuntu-24.04, client)", result.stdout)
        self.assertNotIn("real failure: public-bootstrap", result.stdout)
        self.assertNotIn(["run", "rerun", "202", "--failed"], calls)
        self.assertEqual(before, self.ledger.read_text())


if __name__ == "__main__":
    unittest.main()
