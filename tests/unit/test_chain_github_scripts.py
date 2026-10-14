"""Exercise scripts/orchestrator/resolve-threads.sh and pr-cost.sh with a stub gh (plan 021 step 6.3).

Each test copies both scripts into a temporary git repository, their root, and runs them there with a stub `gh` first
on PATH and stdin closed. The stub appends each call's argv and stdin to a log and answers from a canned map the test
writes. A REST call is keyed on its API path and its --jq expression, and the map holds the post-filter output. A
GraphQL call is keyed on `graphql` and the operation (`query` or `mutation`). A call with no answer fails. jq, awk and
git are the real ones; the tests compute each filtered answer with the real jq from the fixture the case describes.
"""

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
API = "repos/mryfmo/dotfiles/pulls/9"
BOT = {"login": "chatgpt-codex-connector[bot]"}
# pr-cost.sh's --jq expressions, which key the canned answers.
JQ_BOT = '[.[] | select(.user.login=="chatgpt-codex-connector[bot]")] | length'
JQ_P01 = (
    '[.[] | select(.in_reply_to_id==null and .user.login=="chatgpt-codex-connector[bot]")'
    ' | select(.body | test("P[01] Badge"))] | length'
)
JQ_P23 = JQ_P01.replace("P[01]", "P[23]")
JQ_MERGES = '[.[] | select(.commit.message | test("^Merge branch .main. into|^Merge remote-tracking branch"))] | length'
STUB = """#!@PYTHON@
import json, sys
calls = "@CALLS@"
args = sys.argv[1:]
with open(calls + "/gh.log", "a") as log:
    log.write(json.dumps({"argv": args, "stdin": sys.stdin.read()}) + "\\n")
path, jq, query = None, "", ""
rest = iter(args[1:])
for arg in rest:
    if arg in ("-X", "-f", "-F", "-H", "--jq"):
        value = next(rest)
        jq = value if arg == "--jq" else jq
        query = value[6:] if arg == "-f" and value.startswith("query=") else query
    elif not arg.startswith("-") and path is None:
        path = arg
key = "graphql " + query.split()[0] if path == "graphql" else (path + " " + jq).strip()
canned = json.load(open(calls + "/canned.json"))
if key not in canned:
    sys.exit("stub gh: no canned answer for " + key)
sys.stdout.write(canned[key])
"""


def jq(expression, document):
    """What gh prints for one page under --jq."""
    run = subprocess.run(["jq", expression], input=json.dumps(document), capture_output=True, text=True, check=True)
    return run.stdout


def query(call):
    return next((arg[len("query=") :] for arg in call["argv"] if arg.startswith("query=")), "")


class ChainGithubScriptsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.t = Path(temp.name).resolve()
        self.repo = self.t / "repo"
        (self.repo / "scripts/orchestrator").mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        for name in ("resolve-threads.sh", "pr-cost.sh"):
            shutil.copy(ROOT / "scripts/orchestrator" / name, self.repo / "scripts/orchestrator")
        (self.t / "bin").mkdir()
        gh = self.t / "bin/gh"
        gh.write_text(STUB.replace("@PYTHON@", sys.executable).replace("@CALLS@", str(self.t)))
        gh.chmod(0o755)
        self.canned = {}

    def run_script(self, name, *args, code=0):
        """Run a script from the repository with stdin closed; return its stdout and the stub's calls."""
        (self.t / "canned.json").write_text(json.dumps(self.canned))
        log = self.t / "gh.log"
        log.unlink(missing_ok=True)
        result = subprocess.run(
            ["bash", str(self.repo / "scripts/orchestrator" / name), *map(str, args)],
            cwd=self.repo,
            env={**os.environ, "PATH": f"{self.t}/bin{os.pathsep}{os.environ['PATH']}"},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(code, result.returncode, result.stderr)
        calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
        # No call read anything on stdin, so none could swallow the threads the loop reads.
        self.assertEqual([], [call["argv"] for call in calls if call["stdin"]])
        return result.stdout, calls

    def test_resolve_threads_replies_with_the_table_row_and_resolves_only_threads_with_rows(self):
        self.canned = {
            "graphql query": "101 T_one\n202 T_two\n",
            "graphql mutation": "true\n",
            f"{API}/comments/101/replies .id": "9001\n",
            f"{API}/comments/202/replies .id": "9002\n",
        }
        table = self.t / "extra.tsv"
        table.write_text("101\tfixed:abc1234 evidence=git show abc1234\n")
        url = "https://github.com/mryfmo/dotfiles/pull/9#discussion_r"
        items = [{"url": f"{url}999", "disposition": "not-applicable: another thread; evidence=x"}]
        sweep = self.t / "sweep.json"
        sweep.write_text(json.dumps({"pr": 9, "items": items}))
        fixed = (
            "Disposition (orchestrator): fixed:abc1234 evidence=git show abc1234. Fixed at root cause in that commit"
            " on this branch; verified by the task's tests and CI on the final head. Resolving."
        )
        out, calls = self.run_script("resolve-threads.sh", 9, table, "-", sweep, code=3)
        replies = [call["argv"] for call in calls if call["argv"][1:3] == ["-X", "POST"]]
        self.assertEqual(
            [["api", "-X", "POST", f"{API}/comments/101/replies", "-f", f"body={fixed}", "--jq", ".id"]], replies
        )
        mutations = [query(call) for call in calls if query(call).startswith("mutation")]
        self.assertEqual(["T_one"], [re.search(r'threadId: "([^"]+)"', m)[1] for m in mutations])
        self.assertIn("no disposition row for thread 202 (table or sweep); left open\n", out)
        self.assertEqual("resolved 1 thread(s); missing rows: 1", out.splitlines()[-1])

        # The sweep now carries the second thread's disposition: both are resolved.
        items.append({"url": f"{url}202", "disposition": "not-applicable: owned by t-followup-a01; evidence=y"})
        sweep.write_text(json.dumps({"pr": 9, "items": items}))
        out, calls = self.run_script("resolve-threads.sh", 9, table, "-", sweep)
        bodies = [arg[len("body=") :] for call in calls for arg in call["argv"] if arg.startswith("body=")]
        not_applicable = (
            "Disposition (orchestrator): not-applicable: owned by t-followup-a01; evidence=y."
            " Resolving; the owning task on main carries it."
        )
        self.assertEqual([fixed, not_applicable], bodies)
        mutations = [query(call) for call in calls if query(call).startswith("mutation")]
        self.assertEqual(["T_one", "T_two"], [re.search(r'threadId: "([^"]+)"', m)[1] for m in mutations])
        self.assertEqual("resolved 2 thread(s); missing rows: 0", out.splitlines()[-1])

        # --dry-run reads the threads and writes nothing.
        out, calls = self.run_script("resolve-threads.sh", 9, table, "--dry-run", sweep)
        self.assertEqual([["api", "graphql"]], [call["argv"][:2] for call in calls])
        self.assertIn("would reply+resolve 101: fixed:abc1234 evidence=git show abc1234\n", out)
        self.assertIn("would reply+resolve 202: not-applicable: owned by t-followup-a01; evidence=y\n", out)

    def test_pr_cost_appends_one_ledger_line_from_the_api(self):
        pr = {"head": {"ref": "tools/x"}, "created_at": "2026-10-14T00:00:00Z", "commits": 4}
        pr["merged_at"] = "2026-10-14T03:00:00Z"
        # Two pages of reviews, as --paginate gives them: two of the Bot's in all.
        reviews = [[{"user": BOT}, {"user": {"login": "someone"}}], [{"user": BOT}]]
        comments = [
            {"in_reply_to_id": None, "user": BOT, "body": "**![P1 Badge](https://img.shields.io/x)** a finding"},
            {"in_reply_to_id": 1, "user": BOT, "body": "![P2 Badge](https://img.shields.io/x) a reply, not counted"},
            {"in_reply_to_id": None, "user": {"login": "someone"}, "body": "P2 Badge, quoted by someone else"},
        ]
        commits = [{"commit": {"message": "Merge branch 'main' into tools/x"}}, {"commit": {"message": "fix: y"}}]
        self.canned = {
            API: json.dumps(pr),
            f"{API}/reviews {JQ_BOT}": "".join(jq(JQ_BOT, page) for page in reviews),
            f"{API}/comments {JQ_P01}": jq(JQ_P01, comments),
            f"{API}/comments {JQ_P23}": jq(JQ_P23, comments),
            f"{API}/commits {JQ_MERGES}": jq(JQ_MERGES, commits),
        }
        validation = self.repo / ".orchestration/validation"
        validation.mkdir(parents=True)
        (validation / "t-a01-local-review-1.md").write_text("---\npr: 9\n---\n")
        (validation / "t-a01-local-review-2.md").write_text("---\npr: 90\n---\n")
        out, _ = self.run_script("pr-cost.sh", 9)
        ledger = (self.repo / ".orchestration/metrics/pr-cost.tsv").read_text().splitlines()
        header = "pr branch created merged wall_h commits bot_reviews p1 p2 local_reviews boundary_updates recorded_at"
        self.assertEqual(header.split(), ledger[0].split("\t"))
        line = ledger[1].split("\t")
        expected = ["9", "tools/x", "2026-10-14T00:00:00Z", "2026-10-14T03:00:00Z", "3.0", "4", "2", "1", "0", "1", "1"]
        self.assertEqual(expected, line[:11])
        self.assertRegex(line[11], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
        self.assertEqual(ledger[1] + "\n", out)

        # A second run, the PR now open: one more line and no second header.
        pr["merged_at"] = None
        self.canned[API] = json.dumps(pr)
        self.run_script("pr-cost.sh", 9)
        ledger = (self.repo / ".orchestration/metrics/pr-cost.tsv").read_text().splitlines()
        self.assertEqual([header.replace(" ", "\t")], [row for row in ledger if row.startswith("pr\t")])
        self.assertEqual(3, len(ledger))
        line = ledger[2].split("\t")
        self.assertEqual(["9", "tools/x", "2026-10-14T00:00:00Z", "open"], line[:4])
        self.assertRegex(line[4], r"^\d+\.\d$")


if __name__ == "__main__":
    unittest.main()
