"""Exercise the seats' GitHub-write levers under scripts/orchestrator (regime-cutover U28).

Each lever runs from the checkout (its self-check reads the checkout's manifest) in a scratch git repository, with
`tests/fixtures/pr-levers/fake-gh.py` first on PATH as `gh`: it records every argv and answers from a response table,
running the lever's own `--jq` expression through a real jq or gojq (gh embeds gojq), so the filters are tested too.
The tests assert the receipts, the refusals (exit 2, no write call), the failed reads (exit 1, no write call), that
`<owner>/<repo>` comes from `gh repo view` and that `--delete-branch` never appears. The real `gh` is never called.
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
LEVERS = ROOT / "scripts/orchestrator"
FAKE_GH = ROOT / "tests/fixtures/pr-levers/fake-gh.py"
FOOTER = "🤖 Generated with [Claude Code](https://claude.com/claude-code)"
SHA_A = "a" * 40
SHA_B = "b" * 40
# Codex review comments open with this badge (PR #480's comment 4365170609 carried P2).
BADGE = "**<sub><sub>![{} Badge](https://img.shields.io/badge/{}-yellow?style=flat)</sub></sub>  finding**"


def jq_version(candidate):
    """`jq-<version>` or `gojq <version>` when `candidate` is jq or gojq, else None (a clone such as jaq)."""
    if not candidate or not os.access(candidate, os.X_OK):
        return None
    run = subprocess.run([candidate, "--version"], capture_output=True, text=True, check=False)
    version = run.stdout.strip()
    return version if run.returncode == 0 and version.startswith(("jq-", "gojq")) else None


def find_jq():
    """PR_LEVERS_JQ when set (it must be jq or gojq), else the first jq or gojq found; gh embeds gojq, and jq 1.8
    refuses a null where 1.7 passed it through (U28: `split("\\n")[0]` of an empty body), so CI's jq is the one
    that counts."""
    forced = os.environ.get("PR_LEVERS_JQ")
    if forced:
        if not jq_version(forced):
            raise RuntimeError(f"PR_LEVERS_JQ={forced} is not jq or gojq")
        return forced
    for candidate in (shutil.which("gojq"), "/usr/bin/jq", shutil.which("jq")):
        if jq_version(candidate):
            return candidate
    return None


JQ = find_jq()


def setUpModule():
    """Name the jq the fake runs, so a CI log shows the runner's version."""
    if JQ:
        sys.stderr.write(f"test_pr_levers: --jq runs through {JQ} ({jq_version(JQ)})\n")


def thread(first_id, resolved=False, created="2026-10-24T01:00:00Z", severity="P2", replies=(), node="T"):
    """One reviewThreads node: the first comment, then the replies (each a body)."""
    comments = [{"databaseId": first_id, "createdAt": created, "body": BADGE.format(severity, severity) + "\nbody"}]
    comments += [{"databaseId": first_id + n + 1, "createdAt": created, "body": body} for n, body in enumerate(replies)]
    return {
        "id": f"{node}{first_id}",
        "isResolved": resolved,
        "comments": {"totalCount": len(comments), "nodes": comments},
    }


def threads_json(nodes, head=SHA_A, more=False):
    return {
        "data": {
            "repository": {
                "pullRequest": {
                    "headRefOid": head,
                    "reviewThreads": {"pageInfo": {"hasNextPage": more}, "nodes": nodes},
                }
            }
        }
    }


REPO_VIEW = {"match": r"^repo view --json nameWithOwner$", "json": {"nameWithOwner": "acme/widgets"}}
# The resolveReviewThread answer for the thread of comment 4365170609.
RESOLVED = {
    "match": r"^api graphql -f query=mutation.* -f thread=T4365170609$",
    "json": {"data": {"resolveReviewThread": {"thread": {"id": "T4365170609", "isResolved": True}}}},
}


@unittest.skipUnless(JQ, "no jq or gojq (gh's --jq dialect) on this host")
class PrLeverTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        bindir = self.root / "bin"
        bindir.mkdir()
        (bindir / "gh").symlink_to(FAKE_GH)
        self.tmp = self.root / "tmp"
        self.tmp.mkdir()
        gitconfig = self.root / "gitconfig"
        gitconfig.write_text("[user]\n\tname = t\n\temail = t@example.invalid\n[init]\n\tdefaultBranch = main\n")
        self.calls = self.root / "gh-calls"
        self.responses = self.root / "gh-responses.json"
        self.env = {
            "PATH": f"{bindir}:{os.environ['PATH']}",
            "HOME": str(self.root / "home"),
            "TMPDIR": str(self.tmp),
            "LC_ALL": "C",
            "GIT_CONFIG_GLOBAL": str(gitconfig),
            "GIT_CONFIG_NOSYSTEM": "1",
            "FAKE_GH_CALLS": str(self.calls),
            "FAKE_GH_RESPONSES": str(self.responses),
            "FAKE_GH_STATE": str(self.root / "gh-state.json"),
            "FAKE_GH_JQ": JQ,
        }
        (self.root / "home").mkdir()
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("commit", "-q", "--allow-empty", "-m", "initial")

    def git(self, *args, cwd=None, env=None):
        return subprocess.run(
            ["git", *args],
            cwd=cwd or self.repo,
            env={**self.env, **(env or {})},
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def answer(self, *entries):
        self.responses.write_text(json.dumps([REPO_VIEW, *entries]))

    def run_lever(self, name, *args, cwd=None):
        return subprocess.run(
            [str(LEVERS / name), *args],
            cwd=cwd or self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

    def gh_calls(self):
        if not self.calls.exists():
            return []
        return [json.loads(line) for line in self.calls.read_text().splitlines()]

    def writes(self):
        """The calls that write to GitHub."""
        return [
            call
            for call in self.gh_calls()
            if call[:2] in (["pr", "close"], ["pr", "edit"], ["pr", "update-branch"], ["pr", "create"], ["pr", "merge"])
            or "POST" in call
            or any(arg.startswith("query=mutation") for arg in call)
        ]

    def assert_refused(self, run, message):
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertIn("refused:", run.stderr)
        self.assertIn(message, run.stderr)
        self.assertEqual(self.writes(), [], "a refusal writes nothing")

    def body(self, text, where=None):
        path = (where or self.tmp) / "body.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def tearDown(self):
        for call in self.gh_calls():
            self.assertNotIn("--delete-branch", call)
            self.assertNotIn("--admin", call)


class PrThreadReplyTest(PrLeverTestCase):
    def comment(self, pr_number=480, reply_to=None):
        return {
            "match": r"^api repos/acme/widgets/pulls/comments/4365170609$",
            "json": {
                "pull_request_url": f"https://api.github.com/repos/acme/widgets/pulls/{pr_number}",
                "in_reply_to_id": reply_to,
            },
        }

    def post(self):
        return {
            "match": r"^api -X POST repos/acme/widgets/pulls/480/comments/4365170609/replies -F body=@",
            "json": {"id": 99, "html_url": "https://github.com/acme/widgets/pull/480#discussion_r99"},
        }

    def test_the_reply_posts_once_to_the_repository_gh_names(self):
        self.answer(self.comment(), self.post())
        body = self.body("refuted: scripts/orchestrator/regime-ci.py:20 reads the plain id\n\nmore text\n")
        run = self.run_lever("pr-thread-reply.sh", "480", "4365170609", "--body-file", str(body))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            run.stdout,
            "replied pr=480 comment=4365170609 reply=99 url=https://github.com/acme/widgets/pull/480#discussion_r99\n",
        )
        calls = self.gh_calls()
        self.assertEqual(calls[0][:3], ["repo", "view", "--json"])
        self.assertEqual(len(self.writes()), 1)
        self.assertIn(f"body=@{body}", self.writes()[0])

    def test_every_disposition_form_is_accepted(self):
        for line in (
            f"fixed: {SHA_A}",
            f"fixed: {SHA_A} adds the failing-first test",
            "refuted: https://docs.github.com/en/rest says so",
            "residual: unit=U29 gate=no Linux make update until U29",
            "residual: operator=2026-10-24T12:53:00Z",
        ):
            with self.subTest(line=line):
                self.calls.unlink(missing_ok=True)
                self.answer(self.comment(), self.post())
                run = self.run_lever(
                    "pr-thread-reply.sh", "480", "4365170609", "--body-file", str(self.body(line + "\n"))
                )
                self.assertEqual(run.returncode, 0, run.stderr)

    def test_refusals_come_before_any_gh_call(self):
        good = self.body("refuted: a.py:1\n")
        outside = self.root / "home/reply.md"
        outside.write_text("refuted: a.py:1\n")
        link = self.tmp / "link.md"
        link.symlink_to(outside)
        empty = self.tmp / "empty.md"
        empty.write_text("")
        prose = self.tmp / "prose.md"
        prose.write_text("I think this is fine.\n")
        bare_refutation = self.tmp / "bare.md"
        bare_refutation.write_text("refuted: it is fine\n")
        cases = {
            ("480",): "usage:",
            ("48O", "4365170609", "--body-file", str(good)): "not a decimal number",
            ("480", "-1", "--body-file", str(good)): "not a decimal number",
            ("480", "4365170609", "--body", str(good)): "usage:",
            ("480", "4365170609", "--body-file", str(outside)): "outside $TMPDIR",
            ("480", "4365170609", "--body-file", str(link)): "not a regular file",
            ("480", "4365170609", "--body-file", str(empty)): "1 to 65536 bytes",
            ("480", "4365170609", "--body-file", str(prose)): "not a disposition",
            ("480", "4365170609", "--body-file", str(bare_refutation)): "not a disposition",
        }
        self.answer()
        for args, message in cases.items():
            with self.subTest(args=args):
                self.assert_refused(self.run_lever("pr-thread-reply.sh", *args), message)
        self.assertEqual(self.gh_calls(), [])

    def test_a_body_in_the_store_is_accepted(self):
        self.answer(self.comment(), self.post())
        body = self.body("refuted: a.py:1\n", self.repo / ".orchestration/orchestrate/p")
        self.assertEqual(
            self.run_lever("pr-thread-reply.sh", "480", "4365170609", "--body-file", str(body)).returncode, 0
        )

    def test_a_comment_of_another_pull_request_or_a_reply_is_refused(self):
        body = self.body("refuted: a.py:1\n")
        self.answer(self.comment(pr_number=481), self.post())
        self.assert_refused(
            self.run_lever("pr-thread-reply.sh", "480", "4365170609", "--body-file", str(body)),
            "belongs to pull request 481, not 480",
        )
        self.answer(self.comment(reply_to=4365170000), self.post())
        self.assert_refused(
            self.run_lever("pr-thread-reply.sh", "480", "4365170609", "--body-file", str(body)), "is a reply"
        )

    def test_a_failed_read_writes_nothing(self):
        body = self.body("refuted: a.py:1\n")
        self.answer({"match": r"^api repos/", "exit": 1, "stderr": "HTTP 502"}, self.post())
        run = self.run_lever("pr-thread-reply.sh", "480", "4365170609", "--body-file", str(body))
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(self.writes(), [])
        self.responses.write_text(json.dumps([{"match": "^repo view", "exit": 1}]))
        self.assertEqual(
            self.run_lever("pr-thread-reply.sh", "480", "4365170609", "--body-file", str(body)).returncode, 1
        )


def invalid_dispositions(fixture):
    """Replies that parse as dispositions but do not hold for `fixture`'s commits and records (U28b F1)."""
    return [
        (f"fixed: {SHA_B}", "P2", "is not a commit here"),
        (f"fixed: {fixture.old}", "P2", "predates the finding"),
        ("residual: unit=U99 gate=no such unit", "P2", "no units.tsv row U99"),
        ("residual: unit=U29 gate=a P1 needs the operator", "P1", "is for P2 and P3; this is P1"),
        ("residual: operator=2026-10-24T00:00:00Z", "P1", "no decisions.tsv row"),
    ]


class ThreadsFixture(PrLeverTestCase):
    """A head commit at 02:00Z with an older one at 00:30Z, findings at 01:00Z, and a records directory."""

    def setUp(self):
        super().setUp()
        # The finding is from 01:00Z; the fix commit at 02:00Z is the head, an older commit at 00:30Z is in it.
        self.git("commit", "-q", "--allow-empty", "-m", "old", env={"GIT_COMMITTER_DATE": "2026-10-24T00:30:00Z"})
        self.old = self.git("rev-parse", "HEAD")
        self.git("commit", "-q", "--allow-empty", "-m", "fix", env={"GIT_COMMITTER_DATE": "2026-10-24T02:00:00Z"})
        self.head = self.git("rev-parse", "HEAD")
        self.records = self.repo / ".orchestration/orchestrate/regime-cutover"
        self.records.mkdir(parents=True)
        (self.records / "units.tsv").write_text("id\ttrack\nU29\tseats\n")
        (self.records / "decisions.tsv").write_text("ts\tphase\n2026-10-24T12:53:00Z\tlanding\n")


class PrThreadResolveTest(ThreadsFixture):
    def listing(self, *nodes, more=False):
        return {"match": r"^api graphql -f query=query", "json": threads_json(list(nodes), head=self.head, more=more)}

    def resolve(self, *args):
        return self.run_lever("pr-thread-resolve.sh", *args, "--records", str(self.records))

    def test_a_disposed_thread_is_resolved_by_its_node_id(self):
        self.answer(self.listing(thread(100), thread(4365170609, replies=[f"fixed: {self.head}"])), RESOLVED)
        run = self.resolve("480", "4365170609")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            run.stdout, f"resolved pr=480 comment=4365170609 thread=T4365170609 disposition=fixed {self.head}\n"
        )
        listing = self.gh_calls()[1]
        self.assertIn("owner=acme", listing)
        self.assertIn("name=widgets", listing)
        self.assertIn("pr=480", listing)
        self.assertEqual(len(self.writes()), 1)

    def test_each_valid_disposition_resolves(self):
        for reply, severity in (
            ("refuted: https://docs.github.com/en/rest says so", "P2"),
            ("residual: unit=U29 gate=no Linux make update until U29", "P3"),
            ("residual: operator=2026-10-24T12:53:00Z", "P1"),
        ):
            with self.subTest(reply=reply):
                self.calls.unlink(missing_ok=True)
                self.answer(self.listing(thread(4365170609, severity=severity, replies=[reply])), RESOLVED)
                self.assertEqual(self.resolve("480", "4365170609").returncode, 0)
                self.assertEqual(len(self.writes()), 1)

    def test_refusals(self):
        cases = [
            ((), (thread(1),), "usage:"),
            (("480", "x"), (thread(1),), "not a decimal number"),
            (("480", "4365170609", "9"), (thread(1),), "usage:"),
            (("480", "4365170609"), (thread(1),), "no review thread"),
            (
                ("480", "4365170609"),
                (thread(4365170609, resolved=True, replies=["refuted: a.py:1"]),),
                "already resolved",
            ),
            (("480", "4365170609"), (thread(4365170609),), "no valid disposition"),
            (
                ("480", "4365170609"),
                (thread(4365170609, replies=["refuted: a.py:1", "@codex ok?"]),),
                "no valid disposition",
            ),
        ]
        for args, nodes, message in cases:
            with self.subTest(args=args, message=message):
                self.answer(self.listing(*nodes), RESOLVED)
                self.assert_refused(self.resolve(*args), message)
        self.answer(self.listing(thread(4365170609, replies=["refuted: a.py:1"]), more=True), RESOLVED)
        self.assert_refused(self.resolve("480", "4365170609"), "more than 100 review threads")
        self.answer(self.listing(thread(4365170609, replies=["residual: unit=U29 gate=x"])), RESOLVED)
        self.assert_refused(self.run_lever("pr-thread-resolve.sh", "480", "4365170609"), "needs --records")
        self.answer(self.listing(thread(4365170609, replies=["refuted: a.py:1"])), RESOLVED)
        self.assert_refused(
            self.run_lever("pr-thread-resolve.sh", "480", "4365170609", "--records", str(self.tmp)),
            "holds no units.tsv",
        )

    def test_a_head_missing_here_is_refused(self):
        listing = self.listing(thread(4365170609, replies=["refuted: a.py:1"]))
        listing["json"]["data"]["repository"]["pullRequest"]["headRefOid"] = SHA_B
        self.answer(listing, RESOLVED)
        self.assert_refused(self.resolve("480", "4365170609"), "git fetch first")

    def test_resolve_then_check_refuses_a_disposition_that_does_not_hold(self):
        """U28b F1: the reply lever accepts these lines by form; resolving them is refused, and a thread someone
        resolved anyway (in the web UI) is still open to the merge check."""
        for reply, severity, reason in invalid_dispositions(self):
            with self.subTest(reply=reply):
                self.calls.unlink(missing_ok=True)
                self.answer(self.listing(thread(4365170609, severity=severity, replies=[reply])), RESOLVED)
                self.assert_refused(self.resolve("480", "4365170609"), reason)
                self.assertEqual(self.writes(), [], "no resolveReviewThread")
                resolved = thread(4365170609, resolved=True, severity=severity, replies=[reply])
                self.answer(self.listing(resolved), RESOLVED)
                check = self.run_lever(
                    "pr-threads-check.sh", "480", "--head", self.head, "--records", str(self.records)
                )
                self.assertEqual(check.returncode, 2, check.stdout + check.stderr)
                self.assertIn("state=open (resolved without a valid disposition: ", check.stdout)
                self.assertIn(reason, check.stdout)

    def test_a_mutation_that_does_not_report_resolved_fails(self):
        mutation = {
            **RESOLVED,
            "json": {"data": {"resolveReviewThread": {"thread": {"id": "T4365170609", "isResolved": False}}}},
        }
        self.answer(self.listing(thread(4365170609, replies=["refuted: a.py:1"])), mutation)
        self.assertEqual(self.resolve("480", "4365170609").returncode, 1)


class PrUpdateBranchTest(PrLeverTestCase):
    def view(self, state="OPEN", base="main"):
        return {
            "match": r"^pr view 7 --json state,baseRefName,headRefOid$",
            "json": {"state": state, "baseRefName": base, "headRefOid": SHA_A},
        }

    def test_the_merge_form_updates_and_prints_both_heads(self):
        self.answer(
            self.view(),
            {"match": r"^pr update-branch 7$", "stdout": ""},
            {"match": r"^pr view 7 --json headRefOid$", "json": {"headRefOid": SHA_B}},
        )
        run = self.run_lever("pr-update-branch.sh", "7")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, f"updated pr=7 old={SHA_A} new={SHA_B}\n")
        self.assertEqual(self.writes(), [["pr", "update-branch", "7"]], "never --rebase")

    def test_refusals(self):
        for args, view, message in (
            ((), self.view(), "usage:"),
            (("7", "--rebase"), self.view(), "usage:"),
            (("#7",), self.view(), "not a decimal number"),
            (("7",), self.view(state="MERGED"), "is MERGED, not OPEN"),
            (("7",), self.view(base="release"), "targets release, not main"),
        ):
            with self.subTest(args=args, message=message):
                self.answer(view, {"match": r"^pr update-branch", "stdout": ""})
                self.assert_refused(self.run_lever("pr-update-branch.sh", *args), message)


class PrCloseTest(PrLeverTestCase):
    TABLE = """# Clean-up table

## Open pull requests

| PR | branch | opened | files | title | default |
| --- | --- | --- | --- | --- | --- |
| #378 | `tools/chain-glue-finish` | 2026-10-16 | 16 | feat(orchestrator): chain-finish \\| merge | close: superseded by the cutover (agmsg-regime tooling) |
| #396 | `tools/anthropic-auth-route-structured` | 2026-10-17 | 186 | fix(validator): x | close: superseded by the cutover |
| #404 | `tools/anthropic-auth-runtime-check` | 2026-10-17 | 8 | feat(doctor): y | close: superseded by the cutover |
| #412 | `tools/anthropic-auth-route-structured` | 2026-10-18 | 34 | feat(agents): z | carry: judge the branch's diff against main |

## Worktrees

| path | head | branch | default |
| --- | --- | --- | --- |
| `/tmp/x` | 3b6fa294 | `records/x` | close: not a pull request |
"""

    def setUp(self):
        super().setUp()
        self.handouts = self.repo / ".orchestration/orchestrate/regime-cutover/handouts"
        self.handouts.mkdir(parents=True)
        self.table = self.handouts / "cleanup-table.md"
        self.table.write_text(self.TABLE)

    def github(self):
        heads = {
            378: "tools/chain-glue-finish",
            396: "tools/anthropic-auth-route-structured",
            404: "tools/anthropic-auth-runtime-check",
        }
        states = {378: "OPEN", 396: "OPEN", 404: "CLOSED"}
        entries = [
            {"match": rf"^pr view {n} --json state,headRefName$", "json": {"state": states[n], "headRefName": head}}
            for n, head in heads.items()
        ]
        entries += [
            {"match": r"^pr list --state open --head tools/chain-glue-finish ", "json": [{"number": 378}]},
            {
                "match": r"^pr list --state open --head tools/anthropic-auth-route-structured ",
                "json": [{"number": 396}, {"number": 412}],
            },
            {"match": r"^pr close \d+ --comment ", "stdout": ""},
        ]
        self.answer(*entries)

    def test_the_close_rows_close_and_the_shared_or_closed_ones_are_refused(self):
        self.github()
        run = self.run_lever("pr-close.sh", "--from-table", str(self.table))
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertEqual(
            run.stdout.splitlines(),
            [
                "refused pr=396 reason=branch tools/anthropic-auth-route-structured is the head of open pull requests 396,412",
                "refused pr=404 reason=state CLOSED, not OPEN",
                "closed pr=378 branch=tools/chain-glue-finish",
                "summary closed=1 refused=2",
            ],
        )
        self.assertEqual(
            self.writes(),
            [["pr", "close", "378", "--comment", "close: superseded by the cutover (agmsg-regime tooling)"]],
        )

    def test_only_closes_one_row_and_refuses_a_row_not_marked_close(self):
        self.github()
        run = self.run_lever("pr-close.sh", "--from-table", str(self.table), "--only", "378")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            run.stdout.splitlines(), ["closed pr=378 branch=tools/chain-glue-finish", "summary closed=1 refused=0"]
        )
        self.calls.unlink()
        self.assert_refused(
            self.run_lever("pr-close.sh", "--from-table", str(self.table), "--only", "412"), "no close: row"
        )
        self.assertEqual(self.gh_calls(), [])

    def test_a_head_branch_that_differs_from_the_table_is_refused(self):
        self.answer(
            {"match": r"^pr view 378 ", "json": {"state": "OPEN", "headRefName": "tools/other"}},
            {"match": r"^pr close", "stdout": ""},
        )
        run = self.run_lever("pr-close.sh", "--from-table", str(self.table), "--only", "378")
        self.assertEqual(run.returncode, 2)
        self.assertIn("is not the table's tools/chain-glue-finish", run.stdout)
        self.assertEqual(self.writes(), [])

    def test_the_table_path_and_shape_are_checked_before_any_gh_call(self):
        self.github()
        elsewhere = self.repo / ".orchestration/orchestrate/regime-cutover/cleanup-table.md"
        elsewhere.write_text(self.TABLE)
        link = self.handouts / "link.md"
        link.symlink_to(self.table)
        outside = self.tmp / "handouts/cleanup-table.md"
        outside.parent.mkdir()
        outside.write_text(self.TABLE)
        no_header = self.handouts / "no-header.md"
        no_header.write_text(self.TABLE.replace("| PR | branch |", "| branch | PR |"))
        bad_row = self.handouts / "bad-row.md"
        bad_row.write_text(self.TABLE.replace("| #404 |", "| 404 |"))
        no_close = self.handouts / "carry-only.md"
        no_close.write_text(self.TABLE.replace("| close: superseded", "| carry: kept"))
        cases = {
            ("480",): "usage:",
            ("--from-table",): "usage:",
            ("--from-table", str(self.table), "--only", "x"): "not a decimal number",
            ("--from-table", str(self.table), "--delete-branch"): "usage:",
            ("--from-table", str(elsewhere)): "is not under",
            ("--from-table", str(outside)): "is not under",
            ("--from-table", str(link)): "not a regular file",
            ("--from-table", str(no_header)): "no '## Open pull requests' section",
            ("--from-table", str(bad_row)): "has no #<n> PR cell",
            ("--from-table", str(no_close)): "no row whose default starts with close:",
        }
        for args, message in cases.items():
            with self.subTest(args=args):
                self.assert_refused(self.run_lever("pr-close.sh", *args), message)
        self.assertEqual(self.gh_calls(), [])

    def test_a_linked_worktree_is_refused(self):
        self.github()
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "table")
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked))
        table = linked / ".orchestration/orchestrate/regime-cutover/handouts/cleanup-table.md"
        self.assert_refused(self.run_lever("pr-close.sh", "--from-table", str(table), cwd=linked), "linked worktree")

    def test_a_failed_read_closes_nothing(self):
        self.github()
        entries = json.loads(self.responses.read_text())
        entries.insert(1, {"match": r"^pr view 404 ", "exit": 1, "stderr": "HTTP 502"})
        self.responses.write_text(json.dumps(entries))
        run = self.run_lever("pr-close.sh", "--from-table", str(self.table))
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertIn("nothing was closed", run.stderr)
        self.assertEqual(self.writes(), [])


class PrBodyEditTest(PrLeverTestCase):
    CURRENT = f"## Summary\n\ntext\n\n## Threat table\n\n| a | b |\n\nProgram-Unit: regime-cutover/U41b\n\n{FOOTER}\n"
    NEW = f"## Summary\n\nnew text\n\n## Threat table\n\n| a | b |\n\n## Added\n\nProgram-Unit: regime-cutover/U41\n\n{FOOTER}\n"

    def setUp(self):
        super().setUp()
        self.git("switch", "-q", "-c", "feat/x")
        for program in ("regime-cutover", "other-program"):  # the program stores the checkout holds (U71)
            store = self.repo / ".orchestration/orchestrate" / program
            store.mkdir(parents=True)
            (store / "units.tsv").write_text("id\n")

    def github(self, current=CURRENT, head="feat/x", state="OPEN"):
        self.answer(
            {
                "match": r"^pr view --json number,headRefName,state$",
                "json": {"number": 9, "headRefName": head, "state": state},
            },
            {"match": r"^pr view 9 --json body$", "json": {"body": current}},
            {"match": r"^pr edit 9 --body-file ", "stdout": ""},
        )

    def test_the_body_of_the_branch_pull_request_is_replaced(self):
        self.github()
        body = self.body(self.NEW)
        run = self.run_lever("pr-body-edit.sh", "--body-file", str(body))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertRegex(
            run.stdout, r"^edited pr=9 branch=feat/x program=regime-cutover unit=U41 sha256=[0-9a-f]{64}\n$"
        )
        self.assertEqual(self.writes(), [["pr", "edit", "9", "--body-file", str(body)]])

    def test_a_body_in_the_checkout_is_accepted_and_crlf_is_read_as_lf(self):
        self.github(current=self.CURRENT.replace("\n", "\r\n"))
        body = self.body(self.NEW, self.repo / "pr")
        self.assertEqual(self.run_lever("pr-body-edit.sh", "--body-file", str(body)).returncode, 0)

    def test_any_program_whose_store_the_checkout_holds_is_accepted(self):
        # U71 (F063): the program is not fixed to regime-cutover
        self.github(current=self.CURRENT.replace("regime-cutover/U41b", "other-program/U41"))
        body = self.body(self.NEW.replace("regime-cutover/U41", "other-program/U41"))
        run = self.run_lever("pr-body-edit.sh", "--body-file", str(body))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(" program=other-program unit=U41 ", run.stdout)

    def test_local_refusals_come_before_any_gh_call(self):
        self.github()
        outside = self.root / "home/body.md"
        outside.write_text(self.NEW)
        cases = {
            (): "usage:",
            ("--body-file", str(outside)): "outside $TMPDIR and the checkout",
            ("--body-file", str(self.body(self.NEW.replace("U41\n", "U41b\n")))): "exactly one line",
            ("--body-file", str(self.body(self.NEW + "Program-Unit: regime-cutover/U41\n"))): "exactly one line",
            (
                "--body-file",
                str(self.body(self.NEW.replace("Program-Unit: regime-cutover/U41\n", ""))),
            ): "exactly one line",
            ("--body-file", str(self.body(self.NEW.replace("regime-cutover/U41", "Other/U41")))): "exactly one line",
            (
                "--body-file",
                str(self.body(self.NEW.replace("regime-cutover/U41", "other/U41"))),
            ): "names other, but the checkout holds no .orchestration/orchestrate/other/units.tsv",
        }
        for args, message in cases.items():
            with self.subTest(args=args):
                self.assert_refused(self.run_lever("pr-body-edit.sh", *args), message)
        self.assertEqual(self.gh_calls(), [])

    def test_the_branch_must_be_checked_out_and_not_main(self):
        self.github()
        body = self.body(self.NEW)
        self.git("switch", "-q", "--detach")
        self.assert_refused(self.run_lever("pr-body-edit.sh", "--body-file", str(body)), "HEAD is detached")
        self.git("switch", "-q", "main")
        self.assert_refused(self.run_lever("pr-body-edit.sh", "--body-file", str(body)), "the current branch is main")
        self.assertEqual(self.gh_calls(), [])

    def test_remote_refusals(self):
        body = self.body(self.NEW)
        for kwargs, message in (
            ({"head": "feat/y"}, "is the pull request of feat/y, not of the current branch feat/x"),
            ({"state": "MERGED"}, "is MERGED, not OPEN"),
            ({"current": self.CURRENT.replace("U41b", "U28")}, "the current body names regime-cutover/U28"),
            (
                {"current": self.CURRENT.replace("regime-cutover/U41b", "other-program/U41")},
                "the current body names other-program/U41",
            ),
            (
                {"current": self.CURRENT.replace("U41b", "U41") + "## Verify\n"},
                "drops the line of the current body: ## Verify",
            ),
            ({"current": self.CURRENT + "x\n"}, None),
        ):
            with self.subTest(kwargs=kwargs):
                self.calls.unlink(missing_ok=True)
                self.github(**kwargs)
                run = self.run_lever("pr-body-edit.sh", "--body-file", str(body))
                if message is None:
                    self.assertEqual(run.returncode, 0, run.stderr)
                else:
                    self.assert_refused(run, message)
        self.calls.unlink(missing_ok=True)
        self.github()
        self.assert_refused(
            self.run_lever("pr-body-edit.sh", "--body-file", str(self.body(self.NEW.replace(FOOTER, "")))),
            "drops the line of the current body: " + FOOTER,
        )


class PrThreadsCheckTest(ThreadsFixture):
    def check(self, *nodes, head=None, more=False, records=True):
        self.answer(
            {
                "match": r"^api graphql -f query=query",
                "json": threads_json(list(nodes), head=head or self.head, more=more),
            }
        )
        args = ["480", "--head", self.head]
        if records:
            args += ["--records", str(self.records)]
        return self.run_lever("pr-threads-check.sh", *args)

    def test_resolved_and_disposed_threads_pass(self):
        run = self.check(
            thread(1, resolved=True, replies=["refuted: a.py:1"]),
            thread(2, replies=[f"fixed: {self.head}"]),
            thread(3, replies=["refuted: https://docs.github.com/en/rest/pulls/comments says so"]),
            thread(4, severity="P3", replies=["residual: unit=U29 gate=no Linux make update until U29"]),
            thread(5, severity="P1", replies=["residual: operator=2026-10-24T12:53:00Z"]),
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(
            run.stdout.splitlines(),
            [
                "thread comment=1 severity=P2 state=resolved refuted",
                f"thread comment=2 severity=P2 state=fixed {self.head}",
                "thread comment=3 severity=P2 state=refuted",
                "thread comment=4 severity=P3 state=residual U29",
                "thread comment=5 severity=P1 state=residual operator=2026-10-24T12:53:00Z",
                "summary threads=5 open=0",
            ],
        )
        self.assertEqual(self.writes(), [], "read-only")

    def test_undisposed_threads_refuse_the_merge(self):
        cases = [
            (thread(1), "open (no reply)"),
            (thread(1, replies=["looks fine to me"]), "open (the newest reply is not a disposition)"),
            (thread(1, replies=[f"fixed: {self.old}"]), "predates the finding"),
            (thread(1, created="2026-10-24T03:00:00Z", replies=[f"fixed: {self.head}"]), "predates the finding"),
            (thread(1, created="2026-10-24T03:00:00Z"), "open (no reply)"),
            (thread(1, replies=[f"fixed: {SHA_B}"]), "is not a commit here"),
            (thread(1, severity="P1", replies=["residual: unit=U29 gate=x"]), "is for P2 and P3; this is P1"),
            (thread(1, replies=["residual: unit=U99 gate=x"]), "no units.tsv row U99"),
            (thread(1, replies=["residual: operator=2026-10-24T00:00:00Z"]), "no decisions.tsv row"),
            (thread(1, replies=["refuted: a.py:1", "@codex please re-check"]), "not a disposition"),
        ]
        for node, message in cases:
            with self.subTest(message=message, node=node["comments"]["nodes"][-1]["body"][:40]):
                run = self.check(thread(9, resolved=True, replies=["refuted: a.py:1"]), node)
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                self.assertIn("state=open", run.stdout)
                self.assertIn(message, run.stdout)
                self.assertTrue(run.stdout.endswith("summary threads=2 open=1\n"))

    def test_a_resolved_thread_is_judged_like_an_open_one(self):
        """U28b F1: isResolved alone passes nothing; a resolved thread without a reply, or with one that does not
        hold, is open."""
        cases = [(None, "P2", "no reply"), ("looks fine", "P2", "not a disposition")]
        cases += invalid_dispositions(self)
        for reply, severity, reason in cases:
            with self.subTest(reply=reply):
                node = thread(1, resolved=True, severity=severity, replies=[reply] if reply else [])
                run = self.check(node)
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                self.assertIn("state=open (resolved without a valid disposition: ", run.stdout)
                self.assertIn(reason, run.stdout)
                self.assertTrue(run.stdout.endswith("summary threads=1 open=1\n"))

    def test_a_fix_outside_the_head_is_open(self):
        self.git("switch", "-q", "-c", "side", self.old)
        self.git("commit", "-q", "--allow-empty", "-m", "side", env={"GIT_COMMITTER_DATE": "2026-10-24T02:30:00Z"})
        side = self.git("rev-parse", "HEAD")
        run = self.check(thread(1, replies=[f"fixed: {side}"]))
        self.assertEqual(run.returncode, 2)
        self.assertIn("is not in the head", run.stdout)

    def test_refusals(self):
        run = self.check(thread(1, resolved=True), head=self.old)
        self.assertEqual(run.returncode, 2)
        self.assertIn(f"is {self.old}, not {self.head}", run.stderr)
        run = self.check(thread(1, resolved=True), more=True)
        self.assertEqual(run.returncode, 2)
        self.assertIn("more than 100 review threads", run.stderr)
        run = self.check(thread(1, replies=["residual: unit=U29 gate=x"]), records=False)
        self.assertEqual(run.returncode, 2)
        self.assertIn("needs --records", run.stderr)
        for args, message in (
            (("480",), "--head is not a 40-hex sha"),
            (("480", "--head", "abc"), "--head is not a 40-hex sha"),
            (("--head", self.head), "not a decimal number"),
            (("480", "--head", SHA_B), "is not a commit in this checkout"),
            (("480", "--head", self.head, "--records", str(self.tmp)), "holds no units.tsv"),
        ):
            with self.subTest(args=args):
                self.calls.unlink(missing_ok=True)
                self.assert_refused(self.run_lever("pr-threads-check.sh", *args), message)
                self.assertEqual(self.gh_calls(), [])

    def test_a_failed_listing_is_a_failure_not_a_pass(self):
        self.answer({"match": r"^api graphql", "exit": 1, "stderr": "HTTP 502"})
        run = self.run_lever("pr-threads-check.sh", "480", "--head", self.head)
        self.assertEqual(run.returncode, 1)
        self.assertNotIn("summary", run.stdout)


LEDGER_HEADER = "ts\tunit\tpr\thead_sha\tverdict\tverifier\tevidence\n"


def ledger_row(head, verdict="correct (fresh-context audit, findings=0)", pr=7, ts="2026-10-25T09:00:00Z"):
    return f"{ts}\tU71\t{pr}\t{head}\t{verdict}\tcodex exec\thttps://github.com/acme/widgets/pull/{pr}\n"


class PrMergeTest(PrLeverTestCase):
    """U71 (F010): the merge lever merges only a head with a `correct` ledger row for its full sha and green CI."""

    def setUp(self):
        super().setUp()
        self.records = self.root / "store"
        self.records.mkdir()
        self.ledger(ledger_row(SHA_A))

    def ledger(self, *rows):
        (self.records / "ledger.tsv").write_text(LEDGER_HEADER + "".join(rows))

    def github(self, head=SHA_A, checks=None, checks_exit=0, again=None, draft=False, merge_exit=0, after="MERGED"):
        if checks is None:
            checks = [{"bucket": "pass", "name": "test"}, {"bucket": "skipping", "name": "docs"}]
        listing = {"match": r"^pr checks 7 --json bucket,name$", "json": checks}
        if checks_exit:
            listing = {"match": listing["match"], "exit": checks_exit, "stderr": "HTTP 502"}
        self.answer(
            {
                "match": r"^pr view 7 --json state,baseRefName,headRefOid,isDraft$",
                "json": {"state": "OPEN", "baseRefName": "main", "headRefOid": head, "isDraft": draft},
            },
            listing,
            {"match": r"^pr view 7 --json headRefOid$", "json": {"headRefOid": again or head}},
            {"match": rf"^pr merge 7 --squash --match-head-commit {head}$", "exit": merge_exit, "stderr": "x"},
            {
                "match": r"^pr view 7 --json state,mergeCommit$",
                "json": {"state": after, "mergeCommit": {"oid": SHA_B} if after == "MERGED" else None},
            },
        )

    def merge(self, *extra):
        return self.run_lever("pr-merge.sh", "7", "--records", str(self.records), *extra)

    def test_a_correct_row_for_the_head_and_green_ci_merge_at_that_head(self):
        self.github()
        run = self.merge()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            run.stdout, f"merged pr=7 head={SHA_A} commit={SHA_B} verdict=2026-10-25T09:00:00Z carried-from=-\n"
        )
        self.assertEqual(self.writes(), [["pr", "merge", "7", "--squash", "--match-head-commit", SHA_A]])

    def test_the_ledger_decides(self):
        cases = {
            "missing row": ((ledger_row(SHA_B),), "has no row for pull request 7 at head " + SHA_A),
            "short sha": ((ledger_row(SHA_A[:8]),), "has no row for pull request 7 at head"),
            "other pull request": ((ledger_row(SHA_A, pr=8),), "has no row for pull request 7"),
            "incorrect verdict": ((ledger_row(SHA_A, "incorrect (round 1, P2)"),), "is not correct: incorrect"),
            "blocked verdict": ((ledger_row(SHA_A, "blocked"),), "is not correct: blocked"),
            "newer incorrect row": (
                (ledger_row(SHA_A), ledger_row(SHA_A, "incorrect (re-audit)", ts="2026-10-25T10:00:00Z")),
                "(2026-10-25T10:00:00Z) is not correct",
            ),
        }
        for name, (rows, message) in cases.items():
            with self.subTest(name):
                self.calls.unlink(missing_ok=True)
                self.ledger(*rows)
                self.github()
                self.assert_refused(self.merge(), message)
        self.ledger(ledger_row(SHA_A, "incorrect"), ledger_row(SHA_A, "correct", ts="2026-10-25T11:00:00Z"))
        self.calls.unlink(missing_ok=True)
        self.assertEqual(self.merge().returncode, 0, "the newest row decides")
        self.calls.unlink()
        (self.records / "ledger.tsv").write_text("ts\tunit\n" + ledger_row(SHA_A))
        self.assert_refused(self.merge(), "does not start with the ledger header")

    def test_an_all_digit_sha_matches_only_itself(self):
        # U71 audit round 1 (P2): awk compared two numeric-looking shas as numbers, so these two matched.
        head, other = "1" * 40, "1" * 39 + "2"
        self.ledger(ledger_row(other))
        self.github(head=head)
        self.assert_refused(self.merge(), f"has no row for pull request 7 at head {head}")
        self.calls.unlink()
        self.ledger(ledger_row(other), ledger_row(head))
        self.github(head=head)
        self.assertEqual(self.merge().returncode, 0)

    def test_ci_that_is_not_green_on_the_head_refuses(self):
        for kwargs, message in (
            ({"checks": [{"bucket": "pass", "name": "a"}, {"bucket": "fail", "name": "test"}]}, "test=fail"),
            ({"checks": [{"bucket": "pending", "name": "test"}]}, "test=pending"),
            ({"checks": [{"bucket": "cancel", "name": "test"}]}, "test=cancel"),
            ({"checks": []}, "no check is reported"),
            ({"again": SHA_B}, f"moved from {SHA_A} to {SHA_B}"),
            ({"draft": True}, "is a draft"),
        ):
            with self.subTest(kwargs=kwargs):
                self.calls.unlink(missing_ok=True)
                self.github(**kwargs)
                self.assert_refused(self.merge(), message)
        self.calls.unlink(missing_ok=True)
        self.github(checks_exit=1)
        run = self.merge()
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertIn("gh pr checks 7 failed", run.stderr)
        self.assertEqual(self.writes(), [])

    def test_local_refusals_come_before_any_gh_call(self):
        self.github()
        for args, message in (
            ((), "usage:"),
            (("7",), "usage:"),
            (("x7", "--records", str(self.records)), "not a decimal number"),
            (("7", "--records", str(self.root / "none")), "no readable regular ledger.tsv"),
            (("7", "--records", str(self.records), "--carry-from", SHA_A[:8]), "full 40-hex sha"),
            (("7", "--records", str(self.records), "--auto"), "usage:"),
        ):
            with self.subTest(args=args):
                self.assert_refused(self.run_lever("pr-merge.sh", *args), message)
        self.assertEqual(self.gh_calls(), [])

    def test_a_merge_error_reads_the_state_and_never_merges_twice(self):
        self.github(merge_exit=1)
        run = self.merge()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("exited 1, but the pull request is MERGED", run.stderr)
        self.assertEqual(len(self.writes()), 1)
        self.calls.unlink()
        self.github(merge_exit=1, after="OPEN")
        run = self.merge()
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertIn("is OPEN after the merge command (exit 1)", run.stderr)

    def carry_repo(self, extra_commit=False):
        """main, a branch head X (audited), main moves on, then main merged into the branch: head H."""
        origin = self.root / "origin.git"
        self.git("init", "-q", "--bare", str(origin))
        self.git("remote", "add", "origin", str(origin))
        self.git("switch", "-q", "-c", "feat")
        (self.repo / "tool.sh").write_text("a\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "x")
        audited = self.git("rev-parse", "HEAD")
        self.git("switch", "-q", "main")
        (self.repo / "other.txt").write_text("main moved\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "main")
        self.git("switch", "-q", "feat")
        self.git("merge", "-q", "--no-edit", "main")
        if extra_commit:
            (self.repo / "tool.sh").write_text("changed after the audit\n")
            self.git("commit", "-q", "-am", "unaudited")
        head = self.git("rev-parse", "HEAD")
        self.git("push", "-q", "origin", "main", f"{head}:refs/pull/7/head")
        return audited, head

    def test_a_carry_holds_only_while_the_diff_against_main_is_unchanged(self):
        audited, head = self.carry_repo()
        self.ledger(ledger_row(audited))
        self.github(head=head)
        self.assert_refused(self.merge(), f"has no row for pull request 7 at head {head}")
        self.calls.unlink()
        run = self.merge("--carry-from", audited)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn(f"head={head} commit={SHA_B} verdict=2026-10-25T09:00:00Z carried-from={audited}\n", run.stdout)
        self.assertEqual(self.writes(), [["pr", "merge", "7", "--squash", "--match-head-commit", head]])

    def test_a_carry_refuses_a_changed_diff_and_a_sha_off_the_branch(self):
        audited, head = self.carry_repo(extra_commit=True)
        self.ledger(ledger_row(audited), ledger_row(SHA_B))
        self.github(head=head)
        self.assert_refused(self.merge("--carry-from", audited), "differs from the audited")
        self.assert_refused(self.merge("--carry-from", SHA_B), f"--carry-from {SHA_B} is no commit")

    def test_a_carry_compares_the_whole_tree_whatever_the_cwd_and_git_config(self):
        # U71 audit round 2 (P1): `git diff` under diff.relative=true, run from an unchanged subdirectory, saw neither
        # side's change, so an unaudited commit after the audited one carried the verdict.
        (self.repo / "sub").mkdir()
        (self.repo / "sub/keep.txt").write_text("unchanged\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "a subdirectory")
        self.git("config", "diff.relative", "true")
        self.git("config", "diff.external", "false")
        audited, head = self.carry_repo(extra_commit=True)
        self.ledger(ledger_row(audited))
        self.github(head=head)
        self.assert_refused(
            self.run_lever(
                "pr-merge.sh", "7", "--records", str(self.records), "--carry-from", audited, cwd=self.repo / "sub"
            ),
            "differs from the audited",
        )
        self.assertEqual(self.writes(), [])


FAKE_CODEX = """#!/bin/sh
# A fake codex for PrAuditTest: records what the audit run sees, then answers with FAKE_CODEX_VERDICT.
out=''
dir=''
prev=''
for arg in "$@"; do
    [ "$prev" = -o ] && out=$arg
    [ "$prev" = -C ] && dir=$arg
    prev=$arg
done
cd "$dir" || exit 7
printf '%s\\n' "$@" > "$FAKE_CODEX_LOG/argv"
ls -A "$CODEX_HOME" > "$FAKE_CODEX_LOG/codex-home"
readlink "$CODEX_HOME/auth.json" > "$FAKE_CODEX_LOG/login"
printf '%s\\n' "$HOME" > "$FAKE_CODEX_LOG/home"
ls -A "$HOME" > "$FAKE_CODEX_LOG/home-ls"
env | grep '^XDG_' > "$FAKE_CODEX_LOG/xdg"
cat "$CODEX_HOME/config.toml" > "$FAKE_CODEX_LOG/config"
ls -A . > "$FAKE_CODEX_LOG/cwd"
cat > "$FAKE_CODEX_LOG/prompt"
echo "codex log ${FAKE_CODEX_TAG:-}"
[ -n "$FAKE_CODEX_VERDICT" ] && printf '%s\\n' "$FAKE_CODEX_VERDICT" > "$out"
exit "${FAKE_CODEX_EXIT:-0}"
"""


class PrAuditTest(PrLeverTestCase):
    """U71 (F010, F153): one fresh read-only codex round per head, its verdict file and its own ledger row."""

    def setUp(self):
        super().setUp()
        codex = self.root / "bin/codex"
        codex.write_text(FAKE_CODEX)
        codex.chmod(0o755)
        self.seen = self.root / "seen"
        self.seen.mkdir()
        self.login = self.root / "auth.json"
        self.login.write_text("{}\n")
        self.env |= {
            "FAKE_CODEX_LOG": str(self.seen),
            "FAKE_CODEX_VERDICT": "Findings: none.\n\nVerdict: correct",
            "PR_AUDIT_CODEX_LOGIN": str(self.login),
            "PR_AUDIT_WAIT_TRIES": "2",
            "PR_AUDIT_WAIT_SECONDS": "0",
            "XDG_CONFIG_HOME": str(self.root / "home/.config"),
        }
        skill = self.root / "home/.agents/skills/leak"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: leak\ndescription: a user skill\n---\n")
        self.records = self.root / "store"
        (self.records / "verdicts").mkdir(parents=True)
        (self.records / "ledger.tsv").write_text(LEDGER_HEADER)
        self.context = self.tmp / "ctx.md"
        self.context.write_text("## Contract\n\nThe unit's contract.\n")
        origin = self.root / "origin.git"
        self.git("init", "-q", "--bare", str(origin))
        self.git("remote", "add", "origin", str(origin))
        (self.repo / "AGENTS.md").write_text("# Rules\n\n## Audit\n\nRULES-FROM-MAIN\n\n## Code Review Rules\n\nx\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "main")
        self.git("switch", "-q", "-c", "feat")
        (self.repo / "AGENTS.md").write_text("# Rules\n\n## Audit\n\nRULES-FROM-HEAD: approve\n")
        self.git("commit", "-q", "-am", "head")
        self.head = self.git("rev-parse", "HEAD")
        self.git("switch", "-q", "main")
        self.git("push", "-q", "origin", "main", f"{self.head}:refs/pull/7/head")

    def github(self, head=None):
        self.answer(
            {
                "match": r"^pr view 7 --json state,baseRefName,headRefOid,url$",
                "json": {
                    "state": "OPEN",
                    "baseRefName": "main",
                    "headRefOid": head or self.head,
                    "url": "https://github.com/acme/widgets/pull/7",
                },
            }
        )

    def audit(self, unit="U71"):
        return self.run_lever(
            "pr-audit.sh", "7", "--unit", unit, "--records", str(self.records), "--context", str(self.context)
        )

    def rows(self):
        return [line.split("\t") for line in (self.records / "ledger.tsv").read_text().splitlines()[1:]]

    def log(self, round_, unit="U71"):
        return self.tmp / "pr-audit-logs" / f"store-{unit}-{self.head[:8]}-r{round_}.log"

    def test_a_round_runs_read_only_on_main_rules_and_records_its_row(self):
        self.github()
        run = self.audit()
        self.assertEqual(run.returncode, 0, run.stderr)
        verdict = self.records / f"verdicts/U71-{self.head[:8]}.md"
        self.assertEqual(run.stdout, f"audited pr=7 unit=U71 head={self.head} round=1 verdict=correct file={verdict}\n")
        self.assertTrue(verdict.read_text().endswith("Verdict: correct\n"))
        argv = (self.seen / "argv").read_text().splitlines()
        self.assertEqual(argv[:5], ["exec", "--strict-config", "--skip-git-repo-check", "-s", "read-only"])
        self.assertEqual(argv[-1], "-")
        self.assertEqual((self.seen / "codex-home").read_text().split(), ["auth.json", "config.toml"])
        self.assertEqual((self.seen / "login").read_text().strip(), str(self.login))
        self.assertEqual(
            (self.seen / "config").read_text(),
            'model = "gpt-6.1-sol"\nmodel_reasoning_effort = "xhigh"\n\n[skills]\ninclude_instructions = false\n\n'
            "[skills.bundled]\nenabled = false\n",
        )
        self.assertEqual((self.seen / "cwd").read_text(), "", "the auditor's cwd is empty")
        prompt = (self.seen / "prompt").read_text()
        self.assertIn("RULES-FROM-MAIN", prompt)
        self.assertNotIn("RULES-FROM-HEAD", prompt)
        self.assertIn("The unit's contract.", prompt)
        self.assertIn(f"(HEAD {self.head[:8]})", prompt)
        [row] = self.rows()
        self.assertEqual(row[1:4], ["U71", "7", self.head])
        self.assertEqual(row[4], f"correct (pr-audit.sh round 1; verdicts/U71-{self.head[:8]}.md, log {self.log(1)})")
        self.assertEqual(self.log(1).read_text(), "codex log \n")
        self.assertIn("read-only, scratch cwd, scratch HOME and CODEX_HOME", row[5])
        self.assertEqual(row[6], "https://github.com/acme/widgets/pull/7")
        self.assertEqual(self.git("worktree", "list", "--porcelain").count("worktree "), 1, "the worktree is removed")

    def test_the_auditor_gets_an_empty_scratch_home(self):
        self.github()
        self.assertEqual(self.audit().returncode, 0)
        # U71 audit round 2 (P2): codex reads user skills under $HOME/.agents/skills, so its HOME is an empty scratch
        # directory, never the caller's (whose skills directory the fixture fills), and no XDG variable survives.
        home = (self.seen / "home").read_text().strip()
        self.assertNotEqual(home, self.env["HOME"])
        self.assertTrue(home.startswith(str(self.tmp)), home)
        self.assertEqual((self.seen / "home-ls").read_text(), "", "the auditor's HOME is empty")
        self.assertEqual((self.seen / "xdg").read_text(), "")

    def test_every_round_gets_its_own_row_and_an_incorrect_or_silent_round_exits_3(self):
        (self.records / "ledger.tsv").write_text(LEDGER_HEADER + ledger_row(SHA_B, "incorrect"))
        self.github()
        self.env["FAKE_CODEX_VERDICT"] = "P2 finding\nVerdict: incorrect"
        run = self.audit()
        self.assertEqual(run.returncode, 3, run.stderr)
        self.assertEqual(
            self.rows()[-1][4], f"incorrect (pr-audit.sh round 2; verdicts/U71-{self.head[:8]}.md, log {self.log(2)})"
        )
        self.env["FAKE_CODEX_VERDICT"] = "no verdict"
        run = self.audit(unit="U71b")
        self.assertEqual(run.returncode, 3, run.stderr)
        self.assertTrue(self.rows()[-1][4].startswith("blocked (no verdict line; pr-audit.sh round 1;"))
        # a re-run of the same head after `blocked` keeps the first round's file and writes its own
        self.env["FAKE_CODEX_VERDICT"] = "Verdict: correct"
        run = self.audit(unit="U71b")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            self.rows()[-1][4],
            f"correct (pr-audit.sh round 2; verdicts/U71b-{self.head[:8]}-r2.md, log {self.log(2, 'U71b')})",
        )
        kept = (self.records / f"verdicts/U71b-{self.head[:8]}.md").read_text()
        self.assertTrue(kept.startswith("no verdict\n") and kept.endswith("Verdict: blocked\n"), kept)
        self.assertEqual(len(self.rows()), 4)

    def test_a_silent_round_keeps_its_own_verdict_and_log_and_a_rerun_truncates_nothing(self):
        # U71 audit round 1 (P2): a no-output round left no verdict file and a shared log the next run truncated.
        self.github()
        self.env |= {"FAKE_CODEX_VERDICT": "", "FAKE_CODEX_TAG": "first"}
        run = self.audit()
        self.assertEqual(run.returncode, 3, run.stderr)
        first = self.records / f"verdicts/U71-{self.head[:8]}.md"
        self.assertIn(f"is blocked: no output; codex exit status 0; its log is {self.log(1)}", first.read_text())
        self.assertTrue(first.read_text().endswith("Verdict: blocked\n"))
        self.assertEqual(
            self.rows()[-1][4], f"blocked (no output; pr-audit.sh round 1; verdicts/{first.name}, log {self.log(1)})"
        )
        self.env |= {"FAKE_CODEX_TAG": "second", "FAKE_CODEX_EXIT": "4"}
        run = self.audit()
        self.assertEqual(run.returncode, 3, run.stderr)
        second = self.records / f"verdicts/U71-{self.head[:8]}-r2.md"
        self.assertIn(f"codex exec exited 4; codex exit status 4; its log is {self.log(2)}", second.read_text())
        self.assertTrue(self.rows()[-1][4].startswith("blocked (no output; codex exec exited 4; pr-audit.sh round 2;"))
        self.assertEqual(self.log(1).read_text(), "codex log first\n", "the first round's log is untouched")
        self.assertEqual(self.log(2).read_text(), "codex log second\n")
        self.assertIn("codex exit status 0;", first.read_text(), "the first round's verdict is untouched")
        # a log at the next round's name (a round the ledger lacks) is a refusal, never a truncation
        self.log(3).write_text("kept\n")
        self.assert_refused(self.audit(), "already exists")
        self.assertEqual(self.log(3).read_text(), "kept\n")
        self.assertEqual(len(self.rows()), 2)

    def test_a_verdict_followed_by_a_failed_exit_ends_blocked_in_the_file_and_the_row(self):
        # U71 audit round 2 (P2): the file kept `Verdict: correct` while the ledger said blocked.
        self.github()
        self.env |= {"FAKE_CODEX_VERDICT": "Findings: none.\n\nVerdict: correct", "FAKE_CODEX_EXIT": "5"}
        run = self.audit()
        self.assertEqual(run.returncode, 3, run.stderr)
        text = (self.records / f"verdicts/U71-{self.head[:8]}.md").read_text()
        self.assertTrue(text.startswith("Findings: none.\n\nVerdict: correct\n"), text)
        self.assertIn(f"codex exec exited 5; codex exit status 5; its log is {self.log(1)}", text)
        self.assertTrue(text.endswith("\nVerdict: blocked\n"), text)
        self.assertTrue(self.rows()[-1][4].startswith("blocked (codex exec exited 5; pr-audit.sh round 1;"))

    def test_a_context_lost_after_the_check_blocks_the_round_and_starts_no_codex(self):
        # U71 audit round 3 (P2): a failed `cat` of the context was masked by the printf after it, so the audit ran
        # without the unit's contract and could record `correct`. The `gh` call comes after the context check, so a
        # wrapper there takes the context away (unreadable, then emptied) before the prompt is built.
        gh = self.root / "bin/gh"
        for name, spoil in (("unreadable", 'chmod 000 "$CTX"'), ("emptied", ': > "$CTX"')):
            with self.subTest(name):
                self.context.chmod(0o644)
                self.context.write_text("## Contract\n\nThe unit's contract.\n")
                (self.seen / "argv").unlink(missing_ok=True)
                gh.unlink()
                gh.write_text(f'#!/bin/sh\nCTX="{self.context}"\n{spoil}\nexec "{FAKE_GH}" "$@"\n')
                gh.chmod(0o755)
                self.github()
                run = self.audit(unit=f"U{len(self.rows()) + 80}")
                self.assertEqual(run.returncode, 3, run.stdout + run.stderr)
                self.assertIn("codex did not run", run.stderr)
                self.assertFalse((self.seen / "argv").exists(), "codex never starts without the contract")
                row = self.rows()[-1][4]
                self.assertTrue(row.startswith("blocked ("), row)
                self.assertIn("codex not run;", row)
                verdict = self.records / "verdicts" / f"{self.rows()[-1][1]}-{self.head[:8]}.md"
                self.assertTrue(verdict.read_text().endswith("\nVerdict: blocked\n"), verdict.read_text())
        self.context.chmod(0o644)

    def test_refusals(self):
        self.github(head=SHA_A)
        self.assert_refused(self.audit(), f"refs/pull/7/head is {self.head}, the pull request's head is {SHA_A}")
        self.github()
        (self.records / f"verdicts/U71-{self.head[:8]}.md").write_text("an earlier round\n")
        (self.records / f"verdicts/U71-{self.head[:8]}-r1.md").write_text("a round the ledger lacks\n")
        self.assert_refused(self.audit(), "already exists")
        self.assertEqual(self.rows(), [])
        self.assertFalse((self.seen / "argv").exists(), "no codex run after a refusal")
        self.env["PR_AUDIT_CODEX_LOGIN"] = str(self.root / "absent.json")
        self.assert_refused(self.audit(unit="U72"), "no readable Codex login")
        self.assert_refused(self.audit(unit="u72"), "--unit must be")


class DispositionDriftTest(unittest.TestCase):
    def test_the_resolve_lever_and_the_merge_check_judge_by_the_same_function(self):
        """U28b F1: `disposition` is one text in pr-thread-resolve.sh and pr-threads-check.sh."""

        def function(name):
            text = (LEVERS / name).read_text()
            start = text.index("disposition() {")
            return text[start : text.index("\n}\n", start)]

        self.assertEqual(function("pr-thread-resolve.sh"), function("pr-threads-check.sh"))


GIT_WRAPPER = """#!/usr/bin/env python3
import os, subprocess, sys
if os.environ.get("FAKE_GIT_FAIL") and os.environ["FAKE_GIT_FAIL"] in sys.argv[1:]:
    sys.exit("fake-git: failing as asked")
run = subprocess.run([os.environ["REAL_GIT"], *sys.argv[1:]], stdout=subprocess.PIPE)
sys.stdout.buffer.write(run.stdout)
extra = os.environ.get("FAKE_GIT_EXTRA_OTHERS")
if extra and "--others" in sys.argv:
    sys.stdout.buffer.write(extra.encode() + b"\\0")
sys.exit(run.returncode)
"""


class RecordsSyncTest(PrLeverTestCase):
    def setUp(self):
        super().setUp()
        wrapper = self.root / "bin/git"
        wrapper.write_text(GIT_WRAPPER)
        wrapper.chmod(0o755)
        self.env["REAL_GIT"] = shutil.which("git", path=os.environ["PATH"])
        self.origin = self.root / "origin.git"
        self.git("init", "-q", "--bare", str(self.origin))
        (self.repo / "scripts").mkdir()
        shutil.copy2(ROOT / "scripts/validate-agent-assets.py", self.repo / "scripts/validate-agent-assets.py")
        self.records = self.repo / ".orchestration/orchestrate/prog"
        self.records.mkdir(parents=True)
        (self.records / "units.tsv").write_text("id\ttrack\nU1\tseats\n")
        (self.records / "decisions.tsv").write_text("ts\tphase\n")
        (self.repo / "README").write_text("scratch\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")
        self.git("remote", "add", "origin", str(self.origin))
        self.git("push", "-q", "origin", "main")
        self.git("fetch", "-q", "origin")

    def github(self):
        self.answer(
            {
                "match": r"^pr list --state all ",
                "json": [{"headRefName": "records/program-store-6"}, {"headRefName": "feat/x"}],
            },
            {
                "match": r"^pr create --base main --head records/sync-7 ",
                "stdout": "https://github.com/acme/widgets/pull/600\n",
            },
        )

    def test_the_records_reach_a_records_branch_and_a_pull_request(self):
        self.github()
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        (self.records / "decisions.tsv").write_text("ts\tphase\n2026-10-24T13:00:00Z\tseats\n")
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        (self.records / "notes.md").write_text(f"token {planted}\n")
        (self.repo / "scripts/stray.sh").write_text("not records\n")
        run = self.run_lever("records-sync.sh", "--unit", "U20")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            run.stdout, "synced branch=records/sync-7 files=3 pr=https://github.com/acme/widgets/pull/600\n"
        )
        files = self.git("ls-tree", "-r", "--name-only", "records/sync-7", cwd=self.origin).splitlines()
        self.assertNotIn("scripts/stray.sh", files)
        changed = self.git("diff", "--name-only", "main", "records/sync-7", cwd=self.origin).splitlines()
        self.assertEqual(
            changed,
            [
                ".orchestration/orchestrate/prog/decisions.tsv",
                ".orchestration/orchestrate/prog/notes.md",
                ".orchestration/orchestrate/prog/units.tsv",
            ],
        )
        notes = self.git("show", "records/sync-7:.orchestration/orchestrate/prog/notes.md", cwd=self.origin)
        self.assertNotIn(planted, notes, "the copy is masked")
        self.assertIn(planted, (self.records / "notes.md").read_text(), "the checkout's file is never changed")
        message = self.git("log", "-1", "--format=%B", "records/sync-7", cwd=self.origin)
        self.assertTrue(message.startswith("chore(records): prog sync 7\n"))
        self.assertIn("Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>", message)
        create = self.writes()[0]
        body = Path(create[create.index("--body-file") + 1])
        self.assertFalse(body.exists(), "the scratch directory is removed")
        self.assertEqual(self.git("worktree", "list", "--porcelain").count("worktree "), 1, "the worktree is removed")
        self.assertEqual(
            self.git("ls-remote", "--heads", str(self.origin)).count("refs/heads/"), 2, "main and the sync only"
        )

    def test_the_body_names_the_units_and_decisions(self):
        bodies = self.root / "bodies"
        self.github()
        entries = json.loads(self.responses.read_text())
        entries[2] = {**entries[2], "stdout": "https://github.com/acme/widgets/pull/600\n"}
        self.responses.write_text(json.dumps(entries))
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        (self.records / "decisions.tsv").write_text("ts\tphase\n2026-10-24T13:00:00Z\tseats\n")
        fake = self.root / "bin/gh"
        fake.unlink()
        fake.write_text(
            f'#!/bin/sh\nfor a; do case $a in */body.md) mkdir -p {bodies} && cp "$a" {bodies}/;; esac; done\nexec {FAKE_GH} "$@"\n'
        )
        fake.chmod(0o755)
        run = self.run_lever("records-sync.sh", "--unit", "U20")
        self.assertEqual(run.returncode, 0, run.stderr)
        body = (bodies / "body.md").read_text()
        self.assertIn("- units.tsv rows added or changed: U2\n", body)
        self.assertIn("- decisions.tsv rows added or changed: 2026-10-24T13:00:00Z\n", body)
        self.assertIn("Program-Unit: prog/U20\n", body)
        self.assertTrue(body.endswith(FOOTER + "\n"))

    def test_refusals_create_and_push_nothing(self):
        self.github()
        (self.records / "units.tsv").write_text("id\ttrack\nU2\tseats\n")
        cases = [
            (("--base", "origin/dev"), {}, "accepts only origin/main"),
            (("--unit", "U20b"), {}, "not a plain unit id"),
            (("--program", "../x"), {}, "outside [a-z0-9]"),
            (("--program", "absent"), {}, "no program directory"),
            (("extra",), {}, "usage:"),
            ((), {"FAKE_GIT_EXTRA_OTHERS": "scripts/evil.sh"}, "outside .orchestration/: scripts/evil.sh"),
        ]
        for args, env, message in cases:
            with self.subTest(args=args, env=env):
                self.env.update(env)
                self.assert_refused(self.run_lever("records-sync.sh", *args), message)
                for key in env:
                    del self.env[key]
        (self.records / "link.md").symlink_to(self.repo / "README")
        self.assert_refused(self.run_lever("records-sync.sh"), "is a symlink")
        (self.records / "link.md").unlink()
        self.git("checkout", "-q", "--", ".")
        self.assert_refused(self.run_lever("records-sync.sh"), "nothing to sync")
        self.assertEqual(self.gh_calls(), [])
        self.assertEqual(self.git("ls-remote", "--heads", str(self.origin)).count("refs/heads/"), 1)

    def test_a_linked_worktree_is_refused(self):
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked))
        self.assert_refused(self.run_lever("records-sync.sh", cwd=linked), "linked worktree")

    def assert_nothing_left(self):
        self.assertEqual(self.writes(), [], "no gh pr create")
        self.assertEqual(self.git("ls-remote", "--heads", str(self.origin)).count("refs/heads/"), 1, "main only")
        self.assertEqual(self.git("for-each-ref", "refs/heads/records/"), "", "no local records branch")
        self.assertEqual(self.git("worktree", "list", "--porcelain").count("worktree "), 1)

    def test_a_symlinked_ancestor_is_refused_before_any_copy(self):
        """U28b F2: git lists the tracked files below a linked directory; none of them is copied or pushed."""
        self.github()
        outside = self.root / "outside-orchestrate"
        shutil.move(str(self.repo / ".orchestration/orchestrate"), str(outside))
        (self.repo / ".orchestration/orchestrate").symlink_to(outside)
        (outside / "prog/units.tsv").write_text("id\ttrack\nU1\tseats\nU9\toutside the store\n")
        run = self.run_lever("records-sync.sh", "--program", "prog")
        self.assert_refused(run, "is a symlink: .orchestration/orchestrate")
        self.assert_nothing_left()

    def test_a_symlinked_store_root_is_refused(self):
        self.github()
        outside = self.root / "outside-store"
        shutil.move(str(self.repo / ".orchestration"), str(outside))
        (self.repo / ".orchestration").symlink_to(outside)
        (outside / "orchestrate/prog/units.tsv").write_text("id\ttrack\nU9\toutside\n")
        self.assert_refused(
            self.run_lever("records-sync.sh", "--program", "prog"), ".orchestration is missing or a symlink"
        )
        self.assert_nothing_left()

    def test_a_failed_run_leaves_no_branch_and_the_rerun_takes_the_same_number(self):
        """U28b F6: the commit fails; the branch this run created is deleted, so the rerun syncs as records/sync-7."""
        self.github()
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        self.env["FAKE_GIT_FAIL"] = "commit"
        run = self.run_lever("records-sync.sh", "--unit", "U20")
        del self.env["FAKE_GIT_FAIL"]
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assert_nothing_left()
        run = self.run_lever("records-sync.sh", "--unit", "U20")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(run.stdout.startswith("synced branch=records/sync-7 "), run.stdout)

    def test_a_staged_rename_carries_its_source(self):
        """U28c F1: with rename detection the source path was dropped and the old record stayed on the branch."""
        self.github()
        self.git("mv", str(self.records / "units.tsv"), str(self.records / "units-renamed.tsv"))
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)
        files = self.git("ls-tree", "-r", "--name-only", "records/sync-7", cwd=self.origin).splitlines()
        self.assertIn(".orchestration/orchestrate/prog/units-renamed.tsv", files)
        self.assertNotIn(".orchestration/orchestrate/prog/units.tsv", files)

    def test_a_bare_run_names_the_records_unit(self):
        """U28c F2: with no --unit the body still carries the `Program-Unit:` line the regime check requires."""
        bodies = self.root / "bodies"
        self.github()
        fake = self.root / "bin/gh"
        fake.unlink()
        fake.write_text(
            f'#!/bin/sh\nfor a; do case $a in */body.md) mkdir -p {bodies} && cp "$a" {bodies}/;; esac; done\nexec {FAKE_GH} "$@"\n'
        )
        fake.chmod(0o755)
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("Program-Unit: prog/U20\n", (bodies / "body.md").read_text())

    def test_a_local_branch_takes_its_number(self):
        """U28b F6: a local records branch, whatever left it, is never reused."""
        self.github()
        entries = json.loads(self.responses.read_text())
        entries[2]["match"] = r"^pr create --base main --head records/sync-8 "
        self.responses.write_text(json.dumps(entries))
        self.git("branch", "records/sync-7")
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(run.stdout.startswith("synced branch=records/sync-8 "), run.stdout)
        self.assertEqual(self.git("rev-parse", "records/sync-7"), self.git("rev-parse", "main"), "left as it was")


if __name__ == "__main__":
    unittest.main()
