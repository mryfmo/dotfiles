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

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_clone, git_init, quiet_git_env  # noqa: E402

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
        self.env = quiet_git_env(
            {
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
        )
        (self.root / "home").mkdir()
        self.repo = self.root / "repo"
        self.repo.mkdir()
        git_init(self.repo, env=self.env)
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


# A fake sha256sum or shasum for PrBodyEditTest: it fails with exit 1 when its stdin is the file FAKE_HASH_FAIL names
# (compared by device and inode, so the self-checks of the lever and its libraries hash through to the real tool), and
# otherwise runs the real tool with its arguments; `shasum -a 256` stands in for a sha256sum the host lacks.
HASH_FAKE = """#!{python}
import os, sys
want = os.environ.get("FAKE_HASH_FAIL")
if want and os.path.exists(want):
    named, given = os.stat(want), os.fstat(0)
    if (named.st_dev, named.st_ino) == (given.st_dev, given.st_ino):
        print("fake-hash: failing as asked", file=sys.stderr)
        sys.exit(1)
os.execv({real!r}, [{real!r}, *{args!r}, *sys.argv[1:]])
"""


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

    def hash_fake(self, where, name):
        """A fake `name` (sha256sum or shasum) under where, HASH_FAKE over the real tool; None when the host has
        neither sha256sum nor shasum."""
        real, args = shutil.which(name), []
        if real is None:
            real, args = shutil.which("shasum"), ["-a", "256"]
        if real is None:
            return None
        fake = where / name
        fake.write_text(HASH_FAKE.format(python=sys.executable, real=real, args=args))
        fake.chmod(0o755)
        return fake

    def assert_failed_after_the_push(self, body, run):
        """The lever exits 1 naming the pushed body and the hash, prints no receipt, and the one write happened."""
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn(f"pr-body-edit.sh: the body was pushed; cannot hash {body} for the report", run.stderr)
        self.assertEqual(run.stdout, "", "no receipt line with an empty digest")
        self.assertEqual(self.writes(), [["pr", "edit", "9", "--body-file", str(body)]], "the edit was pushed")

    def test_a_sha256sum_that_fails_after_the_edit_is_a_failure_naming_the_push(self):
        """Audit of aa32e0b3 (P2): on main the report's digest read ended in `|| digest=''`, so a sha256sum that failed
        after `gh pr edit` printed a receipt ending `sha256=` with exit 0. The read now ends in `fail`, exit 1 naming
        the pushed body; the fake fails for the body file alone, so the self-checks before it hash through."""
        fakes = self.root / "fakes"
        fakes.mkdir()
        if self.hash_fake(fakes, "sha256sum") is None:
            self.skipTest("no sha256sum or shasum on this host")
        self.github()
        body = self.body(self.NEW)
        self.env |= {"PATH": f"{fakes}:{self.env['PATH']}", "FAKE_HASH_FAIL": str(body)}
        self.assert_failed_after_the_push(body, self.run_lever("pr-body-edit.sh", "--body-file", str(body)))

    def test_a_shasum_that_fails_after_the_edit_with_no_sha256sum_on_path_is_the_same_failure(self):
        """The `else` branch of the digest read: PATH holds only the tools the lever and its libraries run, no
        sha256sum among them, and shasum is the fake."""
        if shutil.which("shasum") is None:
            self.skipTest("no shasum on this host")
        farm = self.root / "farm"
        farm.mkdir()
        for tool in ("bash", "sh", "git", "perl", "awk", "grep", "sed", "cat", "wc", "mktemp", "rm"):
            (farm / tool).symlink_to(shutil.which(tool))
        (farm / "python3").symlink_to(sys.executable)  # the fake gh's interpreter
        (farm / "gh").symlink_to(FAKE_GH)
        self.hash_fake(farm, "shasum")
        self.github()
        body = self.body(self.NEW)
        self.env |= {"PATH": str(farm), "FAKE_HASH_FAIL": str(body)}
        self.assert_failed_after_the_push(body, self.run_lever("pr-body-edit.sh", "--body-file", str(body)))

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


def ledger_row(
    head, verdict="correct (fresh-context audit, findings=0)", pr=7, ts="2026-10-25T09:00:00Z", evidence=None
):
    evidence = evidence or f"https://github.com/acme/widgets/pull/{pr}"
    return f"{ts}\tU71\t{pr}\t{head}\t{verdict}\tcodex exec\t{evidence}\n"


DISPOSITIONS_HEADER = "ts\tunit\thead_sha\tpriority\tpath\tline\tdisposition\treference\n"
UNITS_HEADER = "id\ttrack\tstate\tbranch\tpr\thead_sha\tbrief\tnote\n"
# A `## Findings` line as pr-audit.sh's reader writes it (U119 round 2: a `correct` verdict may carry P2 and P3).
P2_LINE = "- P2 (high) scripts/orchestrator/pr-merge.sh:236: the row is read, the findings are not"
P3_LINE = "- P3 (medium) scripts/orchestrator/README.md:275: the lever row omits the verdict file"


def disposition_row(
    head=SHA_A,
    path="scripts/orchestrator/pr-merge.sh",
    line=236,
    disposition="residual",
    reference="unit=U72 gate=no merge of a correct verdict with an open P2 until U72 lands",
    priority="P2",
    unit="U71",
    ts="2026-10-25T09:30:00Z",
):
    return f"{ts}\t{unit}\t{head}\t{priority}\t{path}\t{line}\t{disposition}\t{reference}\n"


class PrMergeTest(PrLeverTestCase):
    """U71 (F010): the merge lever merges only a head with a `correct` ledger row for its full sha and green CI."""

    def setUp(self):
        super().setUp()
        # The checkout's own store (U71, bot P1 4370212009), kept out of the fixture's commits.
        self.records = self.repo / ".orchestration/orchestrate/regime-cutover"
        self.records.mkdir(parents=True)
        (self.repo / ".git/info/exclude").write_text(".orchestration/\n")
        self.ledger(ledger_row(SHA_A))
        self.verdict()
        self.body = f"## Summary\n\nProgram-Unit: regime-cutover/U71\n\n{FOOTER}\n"

    def ledger(self, *rows):
        (self.records / "ledger.tsv").write_text(LEDGER_HEADER + "".join(rows))

    def verdict(self, *findings, head=SHA_A, unit="U71", last="Verdict: correct", notes="none"):
        """The store's `verdicts/U<n>-<sha8>.md`, the lever's verdict.md in the reader's shape (`- none` by default)."""
        listed = "\n".join(findings or ("- none",))
        (self.records / "verdicts").mkdir(exist_ok=True)
        (self.records / f"verdicts/{unit}-{head[:8]}.md").write_text(
            f"## Findings\n\n{listed}\n\n## Reproduced\n\n- the head builds\n\n## Notes\n\n{notes}\n\nBlocking: 0\n{last}\n"
        )

    def dispositions(self, *rows, header=DISPOSITIONS_HEADER):
        (self.records / "dispositions.tsv").write_text(header + "".join(rows))

    def units(self, *ids):
        (self.records / "units.tsv").write_text(UNITS_HEADER + "".join(f"{i}\tR\tgate\t\t\t\t\t-\n" for i in ids))

    def github(
        self,
        head=SHA_A,
        checks=None,
        checks_exit=0,
        again=None,
        draft=False,
        merge_exit=0,
        after="MERGED",
        again_base="main",
        merged_base="main",
        merged_head=None,
    ):
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
            {"match": r"^pr view 7 --json body$", "json": {"body": self.body}},
            listing,
            {
                "match": r"^pr view 7 --json headRefOid,baseRefName$",
                "json": {"headRefOid": again or head, "baseRefName": again_base},
            },
            {"match": rf"^pr merge 7 --squash --match-head-commit {head}$", "exit": merge_exit, "stderr": "x"},
            {
                "match": r"^pr view 7 --json state,mergeCommit,baseRefName,headRefOid$",
                "json": {
                    "state": after,
                    "mergeCommit": {"oid": SHA_B} if after == "MERGED" else None,
                    "baseRefName": merged_base,
                    "headRefOid": merged_head or head,
                },
            },
        )

    def merge(self, *extra):
        return self.run_lever("pr-merge.sh", "7", "--records", str(self.records), *extra)

    def test_a_correct_row_for_the_head_and_green_ci_merge_at_that_head(self):
        self.github()
        run = self.merge()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, f"merged pr=7 head={SHA_A} commit={SHA_B} verdict=2026-10-25T09:00:00Z\n")
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
        self.verdict(head=head)
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
            # U71 audit round 7 (P2): a pull request retargeted from main with the same head never merges
            ({"again_base": "release"}, "was retargeted from main to release during the checks"),
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
            (("7", "--records", str(self.records), "--carry-from", SHA_A[:8]), "usage:"),
            (("7", "--records", str(self.records), "--auto"), "usage:"),
        ):
            with self.subTest(args=args):
                self.assert_refused(self.run_lever("pr-merge.sh", *args), message)
        self.assertEqual(self.gh_calls(), [])

    def test_only_the_checkout_s_own_store_named_by_the_body_is_read(self):
        # U71, bot P1 4370212009: `--records` took any directory, so a fabricated ledger elsewhere passed.
        fake = self.root / "fabricated"
        fake.mkdir()
        (fake / "ledger.tsv").write_text(LEDGER_HEADER + ledger_row(SHA_A))
        self.ledger()  # the real store holds no verdict for the head
        self.github()
        # U119 round 3: a directory outside the checkout is named as such, before the exact-store comparison
        self.assert_refused(self.run_lever("pr-merge.sh", "7", "--records", str(fake)), "outside the checkout")
        other = self.repo / ".orchestration/orchestrate/other-program"
        other.mkdir()
        (other / "ledger.tsv").write_text(LEDGER_HEADER + ledger_row(SHA_A))
        self.assert_refused(self.run_lever("pr-merge.sh", "7", "--records", str(other)), "is not the program's store")
        self.assertEqual(self.writes(), [])
        # the program comes from the body, and the body must name exactly one
        self.ledger(ledger_row(SHA_A))
        for body, message in (
            ("no marker\n", "exactly one line 'Program-Unit: <program>/U<n>'; it holds: none"),
            ("Program-Unit: regime-cutover/U71\nProgram-Unit: other-program/U1\n", "exactly one line"),
            ("Program-Unit: other-program/U71\n", "is not the program's store"),
            ("Program-Unit: no-store/U71\n", "a symlink or a missing store"),
        ):
            with self.subTest(body=body):
                self.body = body
                self.github()
                self.assert_refused(self.merge(), message)
        self.body = "Program-Unit: regime-cutover/U71\r\n"  # a body edited on github.com carries CRLF
        self.calls.unlink(missing_ok=True)
        self.github()
        self.assertEqual(self.merge().returncode, 0)

    def test_a_symlinked_store_or_ledger_and_a_linked_worktree_are_refused(self):
        real = self.root / "elsewhere"
        real.mkdir()
        (real / "ledger.tsv").write_text(LEDGER_HEADER + ledger_row(SHA_A))
        shutil.rmtree(self.records)
        self.records.symlink_to(real)
        self.github()
        self.assert_refused(self.merge(), "a symlink or a missing store")
        self.records.unlink()
        self.records.mkdir()
        (self.records / "ledger.tsv").symlink_to(real / "ledger.tsv")
        self.assert_refused(self.merge(), "is not a readable regular file of this user")
        (self.records / "ledger.tsv").unlink()
        self.ledger(ledger_row(SHA_A))
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked))
        store = linked / ".orchestration/orchestrate/regime-cutover"
        store.mkdir(parents=True)
        (store / "ledger.tsv").write_text(LEDGER_HEADER + ledger_row(SHA_A))
        run = self.run_lever("pr-merge.sh", "7", "--records", str(store), cwd=linked)
        self.assert_refused(run, "is a linked worktree")
        self.assertEqual(self.writes(), [])

    def test_a_retarget_after_the_last_read_is_reported_as_a_failure(self):
        # gh pr merge takes no base; a retarget in the last window is caught on the read after the merge
        self.github(merged_base="release")
        run = self.merge()
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertIn("merged into release, not main", run.stderr)
        self.assertEqual(run.stdout, "")

    def test_a_merge_at_another_head_is_never_credited_to_the_verdict(self):
        # U71 audit round 9 (P2): the pinned merge failed and someone else merged a later head; MERGED alone gave a
        # receipt for the audited head.
        self.github(merge_exit=1, merged_head=SHA_B)
        run = self.merge()
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(run.stdout, "", "no receipt")
        self.assertIn(f"merged at head {SHA_B}", run.stderr)
        self.assertIn(f"not at the audited head {SHA_A}", run.stderr)

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

    def test_a_head_moved_by_update_branch_needs_its_own_row(self):
        # U71 audit round 10: no carry-over from an earlier audited head; the moved head gets a fresh audit.
        self.ledger(ledger_row(SHA_A))
        self.github(head=SHA_B)
        self.assert_refused(self.merge(), f"has no row for pull request 7 at head {SHA_B}")
        self.assert_refused(self.merge("--carry-from", SHA_A), "usage:")
        self.assertEqual(self.writes(), [])

    def test_a_carried_row_merges_only_on_the_earlier_head_s_correct_row_and_verdict_file(self):
        """U122 (standing order 38): a `carried` row for the head, whose evidence is the line audit-carry.py printed
        (`carried <earlier> <head> <sha256>`), merges like a `correct` row when the earlier head's newest row is
        `correct`; the verdict file and the dispositions the gate reads are then the earlier head's. A carried row whose
        earlier head has no correct row, whose evidence names no digest or another head, or that a newer `incorrect`
        row voids, refuses before CI is read."""
        digest = "d" * 64
        earlier = ledger_row(SHA_B)
        carried = ledger_row(
            SHA_A, "carried", ts="2026-10-25T10:00:00Z", evidence=f"carried {SHA_B} {SHA_A} {digest} (audit-carry.py)"
        )
        self.ledger(earlier, carried)
        (self.records / f"verdicts/U71-{SHA_A[:8]}.md").unlink()  # the carried head has no verdict file of its own
        self.verdict(head=SHA_B)
        self.github()
        run = self.merge()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, f"merged pr=7 head={SHA_A} commit={SHA_B} verdict=2026-10-25T10:00:00Z\n")
        self.assertEqual(self.writes(), [["pr", "merge", "7", "--squash", "--match-head-commit", SHA_A]])
        # the earlier head's findings bind the carried head: its P2 needs the residual row written for the earlier head
        self.verdict(P2_LINE, head=SHA_B)
        self.units("U71", "U72")
        self.dispositions()
        self.calls.unlink()
        self.github()
        self.assert_refused(
            self.merge(),
            f"verdicts/U71-{SHA_B[:8]}.md lists P2 at scripts/orchestrator/pr-merge.sh:236 without a holding disposition",
        )
        self.dispositions(disposition_row(head=SHA_B))
        self.calls.unlink()
        self.github()
        self.assertEqual(self.merge().returncode, 0, "the earlier head's residual row holds for the carried head")
        self.verdict(head=SHA_B)
        for name, rows, message in (
            ("no row for the earlier head", (carried,), f"rests on {SHA_B}, which has no row for pull request 7"),
            (
                "earlier head not correct",
                (ledger_row(SHA_B, "incorrect (round 1)"), carried),
                "is not correct: incorrect",
            ),
            (
                "earlier head voided by a later row",
                (earlier, ledger_row(SHA_B, "incorrect (re-audit)", ts="2026-10-25T09:30:00Z"), carried),
                f"rests on {SHA_B}, whose newest row (2026-10-25T09:30:00Z) is not correct: incorrect",
            ),
            (
                "no digest in the evidence",
                (earlier, ledger_row(SHA_A, "carried", ts="2026-10-25T10:00:00Z", evidence=f"carried from {SHA_B}")),
                "names no 'carried <earlier head> <head> <sha256>' in its evidence",
            ),
            (
                "another head carried",
                (earlier, ledger_row(SHA_A, "carried", evidence=f"carried {SHA_B} {SHA_B} {digest}")),
                f"carries {SHA_B}, not this head {SHA_A}",
            ),
            (
                "carried from itself",
                (earlier, ledger_row(SHA_A, "carried", evidence=f"carried {SHA_A} {SHA_A} {digest}")),
                f"carries {SHA_A} from itself",
            ),
            (
                "a newer incorrect row for the carried head",
                (earlier, carried, ledger_row(SHA_A, "incorrect (fresh audit)", ts="2026-10-25T11:00:00Z")),
                "(2026-10-25T11:00:00Z) is not correct: incorrect",
            ),
        ):
            with self.subTest(name):
                self.calls.unlink(missing_ok=True)
                self.ledger(*rows)
                self.github()
                self.assert_refused(self.merge(), message)
                self.assertNotIn(
                    ["pr", "checks", "7", "--json", "bucket,name"], self.gh_calls(), "refused before CI is read"
                )

    def test_the_lever_reads_no_local_git_objects(self):
        # Only gh and the ledger decide: a planted replace ref, grafts or a broken object store change nothing.
        common = self.repo / ".git"
        (common / "info").mkdir(exist_ok=True)
        (common / "info/grafts").write_text(f"{SHA_A}\n")
        (common / "objects/info/alternates").write_text("/nonexistent/objects\n")
        self.github()
        run = self.merge()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.writes(), [["pr", "merge", "7", "--squash", "--match-head-commit", SHA_A]])

    def test_a_p2_or_p3_finding_of_the_correct_verdict_needs_its_residual_disposition_row(self):
        # U119 round 2 (Codex thread 4419039271, P1): since standing order 35 a `correct` verdict may carry P2 and P3
        # findings, which have no GitHub thread, so the row alone would merge them undispositioned.
        for name, line, at in (
            ("P2", P2_LINE, "scripts/orchestrator/pr-merge.sh:236"),
            ("P3", P3_LINE, "scripts/orchestrator/README.md:275"),
        ):
            with self.subTest(name):
                self.verdict(line)
                self.calls.unlink(missing_ok=True)
                (self.records / "dispositions.tsv").unlink(missing_ok=True)
                self.github()
                run = self.merge()
                self.assert_refused(run, f"lists {name} at {at} and ")
                self.assertIn("dispositions.tsv is not a readable regular file", run.stderr)
                self.calls.unlink()
                self.dispositions()  # the header alone: no row for the finding
                self.assert_refused(self.merge(), f"lists {name} at {at} without a holding disposition: no ")
                self.assertNotIn(
                    ["pr", "checks", "7", "--json", "bucket,name"], self.gh_calls(), "refused before CI is read"
                )
        # a residual row whose unit is a units.tsv row merges, at the one finding of each priority
        self.verdict(P2_LINE, P3_LINE)
        self.dispositions(
            disposition_row(),
            disposition_row(path="scripts/orchestrator/README.md", line=275, priority="P3", ts="2026-10-25T09:31:00Z"),
        )
        self.units("U71", "U72")
        self.calls.unlink()
        self.github()
        run = self.merge()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.writes(), [["pr", "merge", "7", "--squash", "--match-head-commit", SHA_A]])
        # the second finding without its row is named, the first having one
        self.dispositions(disposition_row())
        self.calls.unlink()
        self.github()
        self.assert_refused(
            self.merge(), "lists P3 at scripts/orchestrator/README.md:275 without a holding disposition"
        )

    def test_a_disposition_row_holds_only_as_a_residual_of_a_units_row_for_this_unit_head_path_and_line(self):
        self.verdict(P2_LINE)
        self.units("U71", "U72")
        for name, row, message in (
            ("unit not in units.tsv", disposition_row(reference="unit=U99 gate=x"), "U99, which is not a row of"),
            (
                "fixed row",
                disposition_row(disposition="fixed", reference=SHA_B),
                f"says fixed in {SHA_B}, which is not this head",
            ),
            ("another head", disposition_row(head=SHA_B), "without a holding disposition: no "),
            ("another unit", disposition_row(unit="U72"), "without a holding disposition: no "),
            (
                "another path",
                disposition_row(path="scripts/orchestrator/pr-audit.sh"),
                "without a holding disposition: no ",
            ),
            ("another line", disposition_row(line=237), "without a holding disposition: no "),
            (
                "reference without a gate",
                disposition_row(reference="unit=U72"),
                "reference is not 'unit=U<n> gate=<clause>'",
            ),
        ):
            with self.subTest(name):
                self.dispositions(row)
                self.calls.unlink(missing_ok=True)
                self.github()
                self.assert_refused(self.merge(), message)
        # a fixed row beside the residual row changes nothing: any holding row satisfies the finding
        self.dispositions(
            disposition_row(disposition="fixed", reference=SHA_B), disposition_row(ts="2026-10-25T09:40:00Z")
        )
        self.calls.unlink()
        self.github()
        self.assertEqual(self.merge().returncode, 0)
        # standing order 21: a units.tsv that is missing, or cannot be read, is never "no row" (U119 round 3: a
        # missing or symlinked file is a refusal naming it; a read that fails midway is a failure)
        (self.records / "units.tsv").unlink()
        self.calls.unlink()
        self.github()
        self.assert_refused(self.merge(), "units.tsv is not a regular file of this user (a symlink or missing)")
        if os.geteuid() != 0:
            self.units("U71", "U72")
            (self.records / "units.tsv").chmod(0)
            self.calls.unlink()
            self.github()
            run = self.merge()
            self.assertEqual(run.returncode, 1, run.stderr)
            self.assertIn("cannot read", run.stderr)
            self.assertIn("units.tsv", run.stderr)
            self.assertEqual(run.stdout, "")
        self.assertEqual(self.writes(), [])

    def test_a_malformed_dispositions_file_is_refused_naming_the_line(self):
        self.verdict(P2_LINE)
        self.units("U71", "U72")
        seven = disposition_row().rsplit("\t", 1)[0] + "\n"
        for name, text, message in (
            ("header", "ts\tunit\n" + disposition_row(), "does not start with the header (ts unit head_sha"),
            ("empty file", "", "does not start with the header"),
            ("seven columns", DISPOSITIONS_HEADER + seven, "line 2 has 7 columns, not 8"),
            ("nine columns", DISPOSITIONS_HEADER + disposition_row()[:-1] + "\textra\n", "line 2 has 9 columns, not 8"),
            ("blank line", DISPOSITIONS_HEADER + "\n" + disposition_row(), "line 2 has 0 columns, not 8"),
            # U119 round 3 (audit of 8d442d49, P2): `read` with a tab IFS merged adjacent tabs, so a nine-column row
            # with an empty first or last field passed as eight; the count is awk's now, and no column may be empty
            (
                "nine columns, the last empty",
                DISPOSITIONS_HEADER + disposition_row()[:-1] + "\t\n",
                "line 2 has 9 columns, not 8",
            ),
            (
                "nine columns, the first empty",
                DISPOSITIONS_HEADER + "\t" + disposition_row(),
                "line 2 has 9 columns, not 8",
            ),
            (
                "an empty reference",
                DISPOSITIONS_HEADER + disposition_row(reference=""),
                "line 2: column 8 (reference) is empty",
            ),
            ("an empty unit", DISPOSITIONS_HEADER + disposition_row(unit=""), "line 2: column 2 (unit) is empty"),
            (
                "unknown disposition",
                DISPOSITIONS_HEADER + disposition_row(disposition="accepted"),
                "line 2: disposition 'accepted' is neither residual nor fixed",
            ),
        ):
            with self.subTest(name):
                (self.records / "dispositions.tsv").write_text(text)
                self.calls.unlink(missing_ok=True)
                self.github()
                self.assert_refused(self.merge(), message)
        # CRLF rows, as a file edited on another host may carry, read like LF rows
        self.dispositions(disposition_row().replace("\n", "\r\n"), header=DISPOSITIONS_HEADER.replace("\n", "\r\n"))
        self.calls.unlink()
        self.github()
        self.assertEqual(self.merge().returncode, 0)

    def test_the_verdict_file_of_the_head_is_required_and_read_as_the_reader_wrote_it(self):
        self.github()
        for name, prepare, message in (
            ("missing", lambda: None, "a merge needs the verdict file"),
            ("another head's file", lambda: self.verdict(head=SHA_B), "a merge needs the verdict file"),
            ("another unit's file", lambda: self.verdict(unit="U72"), "a merge needs the verdict file"),
            (
                "P1 under a correct row",
                lambda: self.verdict("- P1 (high) scripts/x.sh:3: boom"),
                "lists P1 at scripts/x.sh:3 under a correct ledger row",
            ),
            (
                "P0 under a correct row",
                lambda: self.verdict("- P0 (low) scripts/x.sh:3: boom"),
                "lists P0 at scripts/x.sh:3 under a correct ledger row",
            ),
            (
                "a line of another shape",
                lambda: self.verdict("- P2 scripts/x.sh:3 boom"),
                "a Findings line is not '- P<n> (<confidence>) <path>:<line>: <rationale>': - P2 scripts/x.sh:3 boom",
            ),
            (
                "a path with a colon",
                lambda: self.verdict("- P2 (high) a:b.sh:3: boom"),
                "a Findings line's path (the text before its last ':<line>: ') holds a colon or whitespace",
            ),
            ("prose in the section", lambda: self.verdict("none found"), "a Findings line is not"),
            ("no list", lambda: self.verdict(""), "the Findings section lists nothing"),
            (
                "no section",
                lambda: (self.records / f"verdicts/U71-{SHA_A[:8]}.md").write_text("## Notes\n\nVerdict: correct\n"),
                "has no '## Findings' section",
            ),
            (
                "verdict line disagrees",
                lambda: self.verdict(last="Verdict: incorrect"),
                "is not 'Verdict: correct' although the ledger row",
            ),
            ("no verdict line", lambda: self.verdict(last="Blocking: 0"), "is not 'Verdict: correct'"),
        ):
            with self.subTest(name):
                shutil.rmtree(self.records / "verdicts", ignore_errors=True)
                (self.records / "verdicts").mkdir()
                prepare()
                self.calls.unlink(missing_ok=True)
                self.assert_refused(self.merge(), message)
        shutil.rmtree(self.records / "verdicts")
        (self.records / "verdicts").mkdir()
        elsewhere = self.root / "elsewhere-verdict.md"
        elsewhere.write_text("## Findings\n\n- none\n\nVerdict: correct\n")
        (self.records / f"verdicts/U71-{SHA_A[:8]}.md").symlink_to(elsewhere)
        self.calls.unlink(missing_ok=True)
        self.assert_refused(self.merge(), "a merge needs the verdict file")
        # `- none`, the shape of a verdict without a finding, merges as before this gate; CRLF reads like LF
        (self.records / f"verdicts/U71-{SHA_A[:8]}.md").unlink()
        self.verdict()
        path = self.records / f"verdicts/U71-{SHA_A[:8]}.md"
        path.write_text(path.read_text().replace("\n", "\r\n"))
        self.calls.unlink(missing_ok=True)
        run = self.merge()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.writes(), [["pr", "merge", "7", "--squash", "--match-head-commit", SHA_A]])

    def test_a_findings_line_is_read_from_its_structure_never_at_its_first_colon(self):
        # U119 round 4 (audit of dc08660f, P2): the gate took the first `:<digits>: ` of the line, so a reader-written
        # path `file:1: real.sh` at line 9 was read as `file` line 1, and that other location's residual row satisfied
        # it. The path is now the text before the line's last `:<line>: ` and may hold no colon and no whitespace.
        self.units("U71", "U72")
        # path `file` line 1, a rationale that begins with `real.sh:9`: only the row for file:1 holds
        self.verdict("- P2 (high) file:1: real.sh:9 is the line it misreads")
        self.dispositions(disposition_row(path="real.sh", line=9))
        self.github()
        self.assert_refused(self.merge(), "lists P2 at file:1 without a holding disposition: no ")
        self.dispositions(disposition_row(path="file", line=1))
        self.calls.unlink()
        self.github()
        run = self.merge()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.writes(), [["pr", "merge", "7", "--squash", "--match-head-commit", SHA_A]])
        # the audit's line, path `file:1: real.sh` at line 9 as the reader writes it, and a rationale holding
        # `:<digits>: `: each is refused naming the line, with rows for both readings present (red on dc08660f: the
        # first merged on the row for file:1)
        self.dispositions(
            disposition_row(path="file", line=1), disposition_row(path="real.sh", line=9, ts="2026-10-25T09:31:00Z")
        )
        for line in ("- P2 (high) file:1: real.sh:9: boom", "- P2 (high) file:1: see real.sh:9: the same shape"):
            with self.subTest(line):
                self.verdict(line)
                self.calls.unlink(missing_ok=True)
                self.github()
                run = self.merge()
                self.assert_refused(
                    run,
                    "a Findings line's path (the text before its last ':<line>: ') holds a colon or whitespace, so its"
                    f" path and line cannot be told from its rationale: {line}",
                )
                self.assertEqual(self.writes(), [])

    def test_only_the_leading_findings_section_of_the_verdict_file_is_read(self):
        # U119 round 4 (audit of dc08660f, P2): every `## Findings` line reopened the list, so a finding-free correct
        # verdict whose Notes held one was refused as prose in the section, and a list line after it would have been a
        # finding. The section runs from the first `## Findings` line to the next `## ` heading; the rest is text.
        self.github()
        self.verdict(
            notes="## Findings\n\nnone found in a second pass\n\n- P2 (high) scripts/x.sh:3: text, not a finding"
        )
        run = self.merge()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.writes(), [["pr", "merge", "7", "--squash", "--match-head-commit", SHA_A]])
        # a later `## Findings` with `- none` does not replace the leading list: its P2 still needs its row
        self.verdict(P2_LINE, notes="## Findings\n\n- none")
        self.dispositions()
        self.calls.unlink()
        self.github()
        self.assert_refused(
            self.merge(), "lists P2 at scripts/orchestrator/pr-merge.sh:236 without a holding disposition: no "
        )

    def test_a_malformed_units_table_is_refused_naming_the_line(self):
        # U119 round 3: the residual's unit is looked up in units.tsv, whose rows are read by the same grammar.
        self.verdict(P2_LINE)
        self.dispositions(disposition_row())
        for name, text, message in (
            ("header", "id\ttrack\nU72\tR\n", "units.tsv does not start with the header (id track state branch"),
            ("empty file", "", "units.tsv does not start with the header"),
            ("seven columns", UNITS_HEADER + "U72\tR\tgate\t\t\t\t-\n", "units.tsv line 2 has 7 columns, not 8"),
            ("nine columns", UNITS_HEADER + "U72\tR\tgate\t\t\t\t\t-\t\n", "units.tsv line 2 has 9 columns, not 8"),
            ("an empty id", UNITS_HEADER + "\tR\tgate\t\t\t\t\t-\n", "units.tsv line 2: column 1 (id) is empty"),
        ):
            with self.subTest(name):
                (self.records / "units.tsv").write_text(text)
                self.calls.unlink(missing_ok=True)
                self.github()
                self.assert_refused(self.merge(), message)
        # the fixture's rows, whose branch, pr, head_sha and brief columns are empty, are eight columns and merge
        self.units("U71", "U72")
        self.calls.unlink()
        self.github()
        self.assertEqual(self.merge().returncode, 0)

    def test_a_symlinked_verdicts_directory_or_units_table_is_refused(self):
        # U119 round 3 (audit of 8d442d49, P2): only the verdict file was checked for a symlink, so a `verdicts/`
        # or `units.tsv` symlink carried files from outside the store into the gate.
        outside = self.root / "outside"
        outside.mkdir()
        shutil.move(str(self.records / "verdicts"), str(outside / "verdicts"))
        (self.records / "verdicts").symlink_to(outside / "verdicts")
        self.github()
        run = self.merge()
        self.assert_refused(run, "verdicts is not a directory of this user (a symlink or missing)")
        self.assertNotIn(["pr", "checks", "7", "--json", "bucket,name"], self.gh_calls(), "refused before CI is read")
        (self.records / "verdicts").unlink()
        shutil.move(str(outside / "verdicts"), str(self.records / "verdicts"))
        # the residual's unit is judged against the store's own units.tsv, never a linked one that holds the row
        self.verdict(P2_LINE)
        self.dispositions(disposition_row())
        (outside / "units.tsv").write_text(UNITS_HEADER + "U72\tR\tgate\t\t\t\t\t-\n")
        (self.records / "units.tsv").symlink_to(outside / "units.tsv")
        self.calls.unlink()
        self.github()
        self.assert_refused(self.merge(), "units.tsv is not a regular file of this user (a symlink or missing)")
        self.assertEqual(self.writes(), [])

    def fake_tool(self, name, failing_on):
        """Put a `name` first on PATH that prints a partial line and exits 1 when an argument holds `failing_on`, and
        runs the real tool otherwise: a producer that fails midway (standing order 21)."""
        real = shutil.which(name, path=os.defpath) or shutil.which(name)
        self.assertTrue(real, f"no {name} on the host")
        script = self.root / "bin" / name
        script.write_text(
            "#!/bin/bash\n"
            'for arg in "$@"; do\n'
            f"    case ${{arg}} in *{failing_on}*) echo partial; echo 'fake {name}: read failed' >&2; exit 1 ;; esac\n"
            "done\n"
            f'exec {real} "$@"\n'
        )
        script.chmod(0o755)

    def test_a_read_of_the_verdict_file_or_a_table_that_fails_never_merges(self):
        # U119 round 3 (audit of 8d442d49, P2): the `cat` of the verdict file and the awk reads of dispositions.tsv
        # and units.tsv had no failure injection; a failed read is exit 1 naming the file, never "no finding" or
        # "no row" (standing order 21).
        self.verdict(P2_LINE)
        self.dispositions(disposition_row())
        self.units("U71", "U72")
        for tool, failing_on, named in (
            ("cat", "verdicts/", f"verdicts/U71-{SHA_A[:8]}.md"),
            ("awk", "dispositions.tsv", "dispositions.tsv"),
            ("awk", "units.tsv", "units.tsv"),
        ):
            with self.subTest(tool=tool, failing_on=failing_on):
                self.fake_tool(tool, failing_on)
                self.calls.unlink(missing_ok=True)
                self.github()
                run = self.merge()
                (self.root / "bin" / tool).unlink()
                self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
                self.assertIn(f"cannot read {self.records}/{named}", run.stderr)
                self.assertEqual(run.stdout, "", "no receipt")
                self.assertEqual(self.writes(), [])
        # the same files, the fakes gone: the merge goes through, so the fakes were what stopped it
        self.calls.unlink()
        self.github()
        self.assertEqual(self.merge().returncode, 0)
        if os.geteuid() != 0:
            # a verdict file this user cannot read is refused by name before any read
            (self.records / f"verdicts/U71-{SHA_A[:8]}.md").chmod(0)
            self.calls.unlink()
            self.github()
            self.assert_refused(self.merge(), f"verdicts/U71-{SHA_A[:8]}.md is not a readable regular file")

    def test_the_gate_takes_no_cache_from_its_environment(self):
        # U119 round 6 (audit of 4f9f958a, P2): the units.tsv cache was tested with `${units_rows+set}` before the
        # gate assigned it, so a caller that exported `units_rows` with a U99 row passed a residual for U99 without
        # units.tsv holding it. Every name the gate reads is assigned in the run before its first read, so an
        # exported one is neither data nor a refusal.
        self.verdict(P2_LINE)
        self.units("U71", "U72")
        planted = "U99\tR\tgate\t\t\t\t\t-"
        self.dispositions(disposition_row(reference="unit=U99 gate=x"))
        for name, env in (
            ("units_rows", {"units_rows": planted}),
            ("units_rows and its flag", {"units_rows": planted, "units_read": "1"}),
        ):
            with self.subTest(name):
                self.env.update(env)
                self.calls.unlink(missing_ok=True)
                self.github()
                self.assert_refused(self.merge(), "U99, which is not a row of")
        # the dispositions rows and the gate's flags: a holding row or a satisfied flag in the environment is none
        # in the store
        self.dispositions()
        self.env.update(
            {
                "dispositions_rows": disposition_row(),
                "rows": disposition_row(),
                "text": disposition_row(),
                "pending": "",
                "findings": "- none",
                "satisfied": "1",
                "seen": "1",
                "section": "1",
                "status": "0",
            }
        )
        self.calls.unlink()
        self.github()
        self.assert_refused(
            self.merge(), "lists P2 at scripts/orchestrator/pr-merge.sh:236 without a holding disposition: no "
        )
        self.assertEqual(self.writes(), [])
        # the same environment with the rows in the store merges: the environment is ignored, never read
        self.dispositions(disposition_row(reference="unit=U72 gate=x"))
        self.calls.unlink()
        self.github()
        self.assertEqual(self.merge().returncode, 0)


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
    print("fake-git: failing as asked", file=sys.stderr)
    sys.exit(int(os.environ.get("FAKE_GIT_FAIL_STATUS", "1")))  # 1 is also `git config`'s status for an unset key
# FAKE_GIT_WARN=<word>: the shape of `git config -f <mode-000 file>` on git 2.56.0 (research 01 section 1.2), a warning
# on stderr and exit 1, the status of an unset key.
if os.environ.get("FAKE_GIT_WARN") and os.environ["FAKE_GIT_WARN"] in sys.argv[1:]:
    print("warning: unable to access 'config': Permission denied", file=sys.stderr)
    sys.exit(1)
# The fake network: FAKE_GIT_HTTPS_ORIGIN="<https url>=<bare repository>" maps the https origin onto the local bare
# repository as a command-line insteadOf; a pushInsteadOf in any config git reads still outranks it for a push. The
# local transport is re-opened for every call (U113: the library's `protocol.allow=never` refuses it, as it would
# refuse a rewrite of the real origin to a path), the way a caller's own `-c protocol.file.allow=always` would.
https_origin = os.environ.get("FAKE_GIT_HTTPS_ORIGIN")
mapping = ["-c", "protocol.file.allow=always"]
if https_origin:
    mapping += ["-c", "url.{1}.insteadOf={0}".format(*https_origin.split("=", 1))]
# FAKE_GIT_EXTRA_ENTRY=<path>: before a `write-tree`, one more entry (an empty blob) enters the index it writes, as
# something other than the lever's own update-index calls would.
extra_entry = os.environ.get("FAKE_GIT_EXTRA_ENTRY")
if extra_entry and "write-tree" in sys.argv[1:]:
    git_dir = [arg for arg in sys.argv[1:] if arg.startswith("--git-dir=")]
    empty = subprocess.run(
        [os.environ["REAL_GIT"], *git_dir, "hash-object", "-w", "--stdin"], input=b"", stdout=subprocess.PIPE, check=True
    ).stdout.decode().strip()
    subprocess.run(
        [os.environ["REAL_GIT"], *git_dir, "update-index", "--add", "--cacheinfo", f"100644,{empty},{extra_entry}"],
        check=True,
    )
run = subprocess.run([os.environ["REAL_GIT"], *mapping, *sys.argv[1:]], stdout=subprocess.PIPE)
out = run.stdout
if os.environ.get("FAKE_GIT_TRUNCATE") in sys.argv[1:]:
    out = out[:-3]  # the last entry cut short, its NUL end gone
sys.stdout.buffer.write(out)
extra = os.environ.get("FAKE_GIT_EXTRA_OTHERS")
if extra and "--others" in sys.argv:
    sys.stdout.buffer.write(extra.encode() + b"\\0")
if os.environ.get("FAKE_GIT_FAIL_AFTER") in sys.argv[1:]:
    sys.exit(1)  # a failure after plausible output
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
        git_init(self.origin, "--bare", env=self.env)
        (self.repo / "scripts").mkdir()
        shutil.copy2(ROOT / "scripts/validate-agent-assets.py", self.repo / "scripts/validate-agent-assets.py")
        self.records = self.repo / ".orchestration/orchestrate/prog"
        self.records.mkdir(parents=True)
        (self.records / "units.tsv").write_text("id\ttrack\nU1\tseats\n")
        (self.records / "decisions.tsv").write_text("ts\tphase\n")
        (self.repo / "README").write_text("scratch\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")
        # The lever removes every inherited GIT_* variable, so the user config it reads is HOME's own .gitconfig.
        user_config = self.root / "home/.gitconfig"
        shutil.copy2(self.env["GIT_CONFIG_GLOBAL"], user_config)
        self.env["GIT_CONFIG_GLOBAL"] = str(user_config)
        self.url = "https://github.com/acme/widgets.git"
        self.env["FAKE_GIT_HTTPS_ORIGIN"] = f"{self.url}={self.origin}"
        self.git("remote", "add", "origin", self.url)
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

    def synced_body(self, *args):
        """Run the lever with the GitHub fake keeping the body file, and return the body text."""
        bodies = self.root / "bodies"
        fake = self.root / "bin/gh"
        fake.unlink()
        fake.write_text(
            f'#!/bin/sh\nfor a; do case $a in */body.md) mkdir -p {bodies} && cp "$a" {bodies}/;; esac; done\nexec {FAKE_GH} "$@"\n'
        )
        fake.chmod(0o755)
        run = self.run_lever("records-sync.sh", *args)
        self.assertEqual(run.returncode, 0, run.stderr)
        return (bodies / "body.md").read_text()

    def test_the_body_names_the_units_and_decisions(self):
        self.github()
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        (self.records / "decisions.tsv").write_text("ts\tphase\n2026-10-24T13:00:00Z\tseats\n")
        body = self.synced_body("--unit", "U20")
        self.assertIn("- units.tsv rows added or changed: U2\n", body)
        self.assertIn("- decisions.tsv rows added or changed: 2026-10-24T13:00:00Z\n", body)
        self.assertIn("Program-Unit: prog/U20\n", body)
        self.assertTrue(body.endswith(FOOTER + "\n"))

    def test_the_body_carries_the_sync_contract(self):
        """U108: pr-audit.sh refuses a body without `## Contract`, so the sync writes the section it is judged by."""
        self.github()
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        body = self.synced_body("--unit", "U20")
        self.assertEqual(body.count("## Contract\n"), 1)
        self.assertLess(body.index("## Summary\n"), body.index("## Contract\n"))
        self.assertLess(body.index("## Contract\n"), body.index("Program-Unit: prog/U20\n"))
        contract = body[body.index("## Contract\n") : body.index("Program-Unit: prog/U20\n")]
        bullets = [line for line in contract.splitlines() if line.startswith("- ")]
        self.assertEqual(len(bullets), 5, contract)
        for bullet, phrase in zip(
            bullets,
            (
                "the store's files (`.orchestration/orchestrate/prog/`, tracked or untracked and not git-ignored, `redact-words.txt` excluded) whose masked copy or executable mode differs from origin/main, plus every path origin/main holds under that directory that the listing does not hold as a regular file; the new tree's change set against origin/main is checked to equal exactly that set",
                "No path lies outside that directory",
                "masked with `validate-agent-assets.py --mask-secrets` and passed its `--scan-identifiers`, with the program's `redact-words.txt` when present",
                "no user, system or checkout configuration, and pushed over https with no user configuration",
                "not reviewed for truth, only by the identifier scan",
            ),
        ):
            self.assertIn(phrase, bullet)

    def test_a_mode_only_change_is_synced_with_the_new_mode(self):
        """U108 round 3 (audit of acd87c5a): the comparison is of `<mode> blob <oid>`, so a store file whose bytes equal
        origin/main but whose executable bit differs is one changed path, published with the new mode."""
        self.github()
        units = self.records / "units.tsv"
        units.chmod(units.stat().st_mode | 0o111)
        run = self.run_lever("records-sync.sh", "--unit", "U20")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            run.stdout, "synced branch=records/sync-7 files=1 pr=https://github.com/acme/widgets/pull/600\n"
        )
        path = ".orchestration/orchestrate/prog/units.tsv"
        changed = self.git("diff", "--name-only", "main", "records/sync-7", cwd=self.origin).splitlines()
        self.assertEqual(changed, [path])
        entry = self.git("ls-tree", "records/sync-7", "--", path, cwd=self.origin)
        self.assertTrue(entry.startswith("100755 blob "), entry)
        self.assertEqual(
            self.git("show", f"records/sync-7:{path}", cwd=self.origin),
            self.git("show", f"main:{path}", cwd=self.origin),
            "the bytes are main's",
        )

    def test_a_copy_the_masker_changes_is_synced_though_its_source_equals_origin_main(self):
        """U108 round 3 (audit of acd87c5a): the comparison is of the masked copy, so a store file whose bytes equal
        origin/main is one changed path when masking changes the copy; origin/main keeps the token, the sync does not."""
        self.github()
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        (self.records / "notes.md").write_text(f"token {planted}\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "a token on main")
        self.git("push", "-q", "origin", "main")
        run = self.run_lever("records-sync.sh", "--unit", "U20")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            run.stdout, "synced branch=records/sync-7 files=1 pr=https://github.com/acme/widgets/pull/600\n"
        )
        path = ".orchestration/orchestrate/prog/notes.md"
        changed = self.git("diff", "--name-only", "main", "records/sync-7", cwd=self.origin).splitlines()
        self.assertEqual(changed, [path])
        self.assertIn(planted, self.git("show", f"main:{path}", cwd=self.origin), "the source equals origin/main")
        self.assertNotIn(planted, self.git("show", f"records/sync-7:{path}", cwd=self.origin), "the copy is masked")

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
        self.env["FAKE_GIT_FAIL"] = "commit-tree"
        run = self.run_lever("records-sync.sh", "--unit", "U20")
        del self.env["FAKE_GIT_FAIL"]
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assert_nothing_left()
        run = self.run_lever("records-sync.sh", "--unit", "U20")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(run.stdout.startswith("synced branch=records/sync-7 "), run.stdout)

    def test_a_config_read_that_fails_is_not_read_as_unset_and_an_empty_value_refuses(self):
        """U101 round 10 (bot finding 4379614437, audit of 0c7bf092): `|| refuse 'unset'` read a failed `git config` as
        an unset key (the identity, then origin's URL), and a configured empty value passed to be refused by
        commit-tree after the branch existed. Exit 1 is unset (refused), any other status is a read failure (failed),
        an empty value is refused; all before any gh call."""
        self.github()
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        self.env |= {"FAKE_GIT_FAIL": "config", "FAKE_GIT_FAIL_STATUS": "3"}
        run = self.run_lever("records-sync.sh")
        del self.env["FAKE_GIT_FAIL"], self.env["FAKE_GIT_FAIL_STATUS"]
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("cannot read git config user.name (git config exited 3)", run.stderr)
        self.assertNotIn("unset", run.stderr)
        self.assert_nothing_left()
        self.assertEqual(self.gh_calls(), [])
        self.env["FAKE_GIT_WARN"] = "config"
        run = self.run_lever("records-sync.sh")
        del self.env["FAKE_GIT_WARN"]
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("cannot read git config user.name (git config exited 1); it wrote to its stderr", run.stderr)
        self.assertNotIn("unset", run.stderr)
        self.assert_nothing_left()
        self.assertEqual(self.gh_calls(), [])
        self.git("config", "user.email", "")
        self.assert_refused(self.run_lever("records-sync.sh"), "git config user.email is unset or empty")
        self.assert_nothing_left()
        self.assertEqual(self.gh_calls(), [])
        self.git("config", "--unset", "user.email")  # the unset case: test_the_push_url_and_the_identity_are_checked...
        self.env |= {"FAKE_GIT_FAIL": "remote.origin.url", "FAKE_GIT_FAIL_STATUS": "3"}
        run = self.run_lever("records-sync.sh")
        del self.env["FAKE_GIT_FAIL"], self.env["FAKE_GIT_FAIL_STATUS"]
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("cannot read git config remote.origin.url (git config exited 3)", run.stderr)
        self.git("config", "remote.origin.url", "")
        self.assert_refused(self.run_lever("records-sync.sh"), "git config remote.origin.url is unset or empty")
        self.git("config", "remote.origin.url", self.url)
        self.assert_nothing_left()
        self.assertEqual(self.gh_calls(), [])
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_a_store_directory_that_cannot_be_entered_refuses_instead_of_deleting_its_files(self):
        """U101 round 10 (audit of 0c7bf092): `git ls-files` warns and exits 0 for a directory it cannot open, so its
        files left the listing and, absent from the store as far as the lever could see, were pushed as deletions.
        The store is walked first; a directory that cannot be read or entered refuses the run before anything exists."""
        if os.geteuid() == 0:
            self.skipTest("file modes do not bind root")
        self.github()
        (self.records / "briefs").mkdir()
        (self.records / "briefs/B1.md").write_text("brief\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "a brief")
        self.git("push", "-q", "origin", "main")
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        locked = self.records / "briefs"
        self.addCleanup(locked.chmod, 0o755)
        for mode in (0o000, 0o444, 0o111):
            with self.subTest(oct(mode)):
                locked.chmod(mode)
                run = self.run_lever("records-sync.sh")
                locked.chmod(0o755)
                self.assert_refused(run, "cannot be read or entered")
                self.assertNotIn("B1.md", run.stdout + run.stderr, "no output names a store path")
                self.assert_nothing_left()
                self.assertEqual(self.gh_calls(), [])
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.branch_changes(), ["M\t.orchestration/orchestrate/prog/units.tsv"])

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
        self.github()
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        self.assertIn("Program-Unit: prog/U20\n", self.synced_body())

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

    def advance_main(self, *changes):
        """Another clone moves origin/main past the checkout, which is never pulled (the operator's stale HEAD)."""
        other = self.root / "other"
        git_clone(self.origin, other, env=self.env)
        for change in changes:
            change(other)
        self.git("add", "-A", cwd=other)
        self.git("commit", "-q", "-m", "main moves on", cwd=other)
        self.git("push", "-q", "origin", "HEAD:main", cwd=other)

    def branch_changes(self, branch="records/sync-7"):
        return self.git("diff", "--no-renames", "--name-status", "main", branch, cwd=self.origin).splitlines()

    def test_a_file_that_became_a_directory_and_the_reverse_are_mirrored_in_one_commit(self):
        """U101 round 4: a deletion candidate got the regular-file check, so a store file `briefs` that became a
        directory `briefs/` refused with "not a regular file". A deletion candidate is now checked by name only, the
        deletions run before the copies, and the one commit carries the deletion and the additions."""
        self.github()
        prog = ".orchestration/orchestrate/prog"
        cases = {
            "file to directory": (("briefs",), ("briefs/B1.md",)),
            "directory to file": (("briefs/B1.md", "briefs/B2.md"), ("briefs",)),
        }
        for case, (before, after) in cases.items():
            with self.subTest(case):
                shutil.rmtree(self.records / "briefs", ignore_errors=True)
                (self.records / "briefs").unlink(missing_ok=True)
                for name in before:
                    (self.records / name).parent.mkdir(parents=True, exist_ok=True)
                    (self.records / name).write_text(f"{name} on main\n")
                self.git("add", "-A")
                self.git("commit", "-q", "-m", f"main holds {before}")
                self.git("push", "-q", "origin", "main")
                shutil.rmtree(self.records / "briefs", ignore_errors=True)
                (self.records / "briefs").unlink(missing_ok=True)
                for name in after:
                    (self.records / name).parent.mkdir(parents=True, exist_ok=True)
                    (self.records / name).write_text(f"{name} in the store\n")
                run = self.run_lever("records-sync.sh")
                self.assertEqual(run.returncode, 0, run.stderr)
                branch = run.stdout.split()[1].removeprefix("branch=")
                expected = sorted([f"D\t{prog}/{name}" for name in before] + [f"A\t{prog}/{name}" for name in after])
                self.assertEqual(sorted(self.branch_changes(branch)), expected)
                self.assertEqual(self.git("rev-list", "--count", f"main..{branch}", cwd=self.origin), "1")
                self.git("push", "-q", "origin", "--delete", branch)
                entries = json.loads(self.responses.read_text())
                entries[2]["match"] = r"^pr create --base main --head records/sync-\d+ "
                self.responses.write_text(json.dumps(entries))

    def test_a_stale_checkout_adds_nothing_main_lacks_and_a_store_deletion_is_synced(self):
        """U101: sync 11 carried 99 untracked validation files of a checkout 60 commits behind origin/main. The copy
        set is the store alone, compared with origin/main: the stale HEAD and the files outside the store do not
        matter, and a file deleted from the store is deleted on the branch."""
        self.github()
        validation = self.repo / ".orchestration/validation"
        validation.mkdir()
        (validation / "old.md").write_text("old\n")
        (self.records / "briefs").mkdir()
        (self.records / "briefs/B1.md").write_text("brief\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "validation and a brief")
        self.git("push", "-q", "origin", "main")

        def drop_old_validation(other):
            (other / ".orchestration/validation/old.md").unlink()
            (other / "README").write_text("main's\n")

        self.advance_main(drop_old_validation)
        (validation / "old.md").write_text("old, edited in the checkout\n")  # tracked at the stale HEAD, gone on main
        (validation / "new.md").write_text("an untracked validation file\n")
        (self.repo / "README").write_text("the checkout's\n")
        (self.records / "briefs/B1.md").unlink()  # deleted from the store, never with git rm
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            self.branch_changes(),
            ["D\t.orchestration/orchestrate/prog/briefs/B1.md", "M\t.orchestration/orchestrate/prog/units.tsv"],
        )
        self.assertTrue(run.stdout.startswith("synced branch=records/sync-7 files=2 "), run.stdout)

    def test_a_push_instead_of_in_the_user_config_does_not_redirect_the_push(self):
        """U101: the operator's global config rewrites https://github.com/ to an SSH URL for pushes, and the host has
        no SSH key; the push, the commit and the gh steps read no user config, and the identity is read once."""
        self.github()
        gitconfig = Path(self.env["GIT_CONFIG_GLOBAL"])
        with gitconfig.open("a") as config:
            config.write('[url "/nonexistent-push-target/"]\n\tpushInsteadOf = https://github.com/\n')
        refused = subprocess.run(
            ["git", "push", "--dry-run", "origin", "main"],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(refused.returncode, 0, "the rewrite is live for a plain push")
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.branch_changes(), ["M\t.orchestration/orchestrate/prog/units.tsv"])
        author = self.git("log", "-1", "--format=%an <%ae>", "records/sync-7", cwd=self.origin)
        self.assertEqual(author, "t <t@example.invalid>")

    def test_the_push_url_and_the_identity_are_checked_before_anything_is_created(self):
        self.github()
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        self.git("remote", "set-url", "origin", "git@github.com:acme/widgets.git")
        self.assert_refused(self.run_lever("records-sync.sh"), "needs an https origin URL")
        self.git("remote", "set-url", "origin", str(self.origin))
        self.assert_refused(self.run_lever("records-sync.sh"), "needs an https origin URL")
        self.git("remote", "set-url", "origin", self.url)
        Path(self.env["GIT_CONFIG_GLOBAL"]).write_text("[init]\n\tdefaultBranch = main\n")
        self.assert_refused(self.run_lever("records-sync.sh"), "git config user.name is unset")
        self.assert_nothing_left()
        self.assertEqual(self.gh_calls(), [])

    def assert_a_worktree_push_is_redirected(self, evil, env):
        """The rewrite is live: a push from a linked worktree of the checkout lands in EVIL, not in origin."""
        probe = self.root / "probe-tree"
        self.git("worktree", "add", "-q", "--detach", str(probe))
        self.git("push", "-q", "origin", "HEAD:refs/heads/probe", cwd=probe, env=env)
        self.git("worktree", "remove", "--force", str(probe))
        self.assertIn("refs/heads/probe", self.git("for-each-ref", cwd=evil))
        self.git("update-ref", "-d", "refs/heads/probe", cwd=evil)

    def assert_the_sync_reached_origin_only(self, evil, env=None):
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        self.env.update(env or {})
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.branch_changes(), ["M\t.orchestration/orchestrate/prog/units.tsv"])
        self.assertEqual(self.git("for-each-ref", cwd=evil), "", "nothing reached the rewrite's target")

    def hostile_include(self):
        """An include file whose pushInsteadOf sends the https origin to a bare repository of its own."""
        evil = git_init(self.root / "evil.git", "--bare", env=self.env)
        include = self.root / "worktrees.gitconfig"
        include.write_text(f'[url "{evil}"]\n\tpushInsteadOf = {self.url}\n')
        return evil, include

    def test_an_include_if_worktree_rule_in_the_repository_config_does_not_redirect_the_push(self):
        """U101 round 2: the rewrite check read the checkout's config, where `includeIf "gitdir:**/worktrees/**"` is
        off; the push ran in the sync worktree, where it is on. The push now runs in a fresh repository."""
        self.github()
        evil, include = self.hostile_include()
        self.git("config", "includeIf.gitdir:**/worktrees/**.path", str(include))
        self.assert_a_worktree_push_is_redirected(evil, None)
        self.assert_the_sync_reached_origin_only(evil)

    def test_an_include_if_worktree_rule_through_git_config_variables_does_not_redirect_the_push(self):
        self.github()
        evil, include = self.hostile_include()
        count = int(self.env["GIT_CONFIG_COUNT"])
        hostile = {
            "GIT_CONFIG_COUNT": str(count + 1),
            f"GIT_CONFIG_KEY_{count}": "includeIf.gitdir:**/worktrees/**.path",
            f"GIT_CONFIG_VALUE_{count}": str(include),
        }
        self.assert_a_worktree_push_is_redirected(evil, hostile)
        self.assert_the_sync_reached_origin_only(evil, hostile)

    def test_inherited_author_and_committer_variables_are_ignored(self):
        """U101 round 2: an exported GIT_AUTHOR_* or GIT_COMMITTER_* outranked `-c user.name`/`-c user.email`."""
        self.github()
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        self.env |= {
            "GIT_AUTHOR_NAME": "intruder",
            "GIT_AUTHOR_EMAIL": "intruder@example.invalid",
            "GIT_COMMITTER_NAME": "intruder",
            "GIT_COMMITTER_EMAIL": "intruder@example.invalid",
        }
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)
        people = self.git("log", "-1", "--format=%an <%ae>|%cn <%ce>", "records/sync-7", cwd=self.origin)
        self.assertEqual(people, "t <t@example.invalid>|t <t@example.invalid>")

    def test_author_and_committer_config_in_the_repository_or_the_worktree_is_ignored(self):
        """U101 round 3: `author.*` and `committer.*` config outranked `-c user.*`. The identity now rides on
        GIT_AUTHOR_*/GIT_COMMITTER_*, which outrank every config key. The worktree case is an include that switches
        on only in the sync worktree (`includeIf "gitdir:**/worktrees/**"`), the config only that worktree reads."""
        self.github()
        worktree_only = self.root / "worktree-identity.gitconfig"
        worktree_only.write_text(
            "[author]\n\tname = wt-author\n\temail = wt-author@example.invalid\n"
            "[committer]\n\tname = wt-committer\n\temail = wt-committer@example.invalid\n"
        )
        cases = {
            "repository config": (
                ("author.name", "repo-author"),
                ("author.email", "repo-author@example.invalid"),
                ("committer.name", "repo-committer"),
                ("committer.email", "repo-committer@example.invalid"),
            ),
            "worktree config": (("includeIf.gitdir:**/worktrees/**.path", str(worktree_only)),),
        }
        for number, (case, settings) in enumerate(cases.items()):
            with self.subTest(case):
                for key, value in settings:
                    self.git("config", key, value)
                with (self.records / "units.tsv").open("a") as units:
                    units.write(f"U{number + 2}\tseats\n")
                run = self.run_lever("records-sync.sh")
                self.assertEqual(run.returncode, 0, run.stderr)
                branch = run.stdout.split()[1].removeprefix("branch=")
                people = self.git("log", "-1", "--format=%an <%ae>|%cn <%ce>", branch, cwd=self.origin)
                self.assertEqual(people, "t <t@example.invalid>|t <t@example.invalid>")
                for key, _ in settings:
                    self.git("config", "--unset", key)
                self.git("push", "-q", "origin", "--delete", branch)
                entries = json.loads(self.responses.read_text())
                entries[2]["match"] = r"^pr create --base main --head records/sync-\d+ "
                self.responses.write_text(json.dumps(entries))

    def test_the_masker_s_output_is_never_shown(self):
        """U101 round 3: on a key collision the masker prints the file's path and both original keys, so a redact word
        or a secret reached the lever's stderr before the scan ran. Its output now goes to the scratch directory."""
        self.github()
        (self.records / "redact-words.txt").write_text("operator1\n")
        first, second = ("ghp_" + letter * 36 for letter in "AB")
        cases = {
            "in the content": ("notes.json", {f"operator1 {first}": 1, f"operator1 {second}": 2}),
            "in the file name": ("notes-operator1.json", {first: 1, second: 2}),
        }
        for case, (name, document) in cases.items():
            with self.subTest(case):
                (self.records / name).write_text(json.dumps(document))
                run = self.run_lever("records-sync.sh")
                self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
                self.assertIn("masking the copies failed (exit 1); its output is withheld", run.stderr)
                for secret in ("operator1", first, second):
                    self.assertNotIn(secret, run.stdout + run.stderr)
                self.assert_nothing_left()
                (self.records / name).unlink()

    def test_a_redact_word_in_a_store_file_refuses(self):
        """U101: host and user names are refused even as bare words; the words file is never published."""
        self.github()
        (self.records / "redact-words.txt").write_text("# host and user names\nmbp-kana\n\noperator1\n")
        cases = {
            "in the text": ("notes.md", "the run went from MBP-Kana fine\n"),
            "in a file name": ("notes-operator1.md", "clean\n"),
        }
        for case, (name, text) in cases.items():
            with self.subTest(case):
                (self.records / name).write_text(text)
                run = self.run_lever("records-sync.sh")
                self.assert_refused(run, "identifier scan")
                self.assertIn("its output is withheld", run.stderr)
                for word in ("mbp-kana", "operator1"):
                    self.assertNotIn(word, run.stderr.lower(), "no output line quotes a word, in a path either")
                self.assert_nothing_left()
                (self.records / name).unlink()
        (self.records / "notes.md").write_text("mbp-kanax is another word\n")
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.branch_changes(), ["A\t.orchestration/orchestrate/prog/notes.md"])

    def test_a_secret_or_a_home_path_in_a_file_name_refuses(self):
        """U101 round 5: a clean file named after a token published the token in its path. The scan tests each path of
        the copy set as it tests the content, and the refusal names neither the path nor what was found."""
        self.github()
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        for case, relative in (("a secret", f"{planted}.md"), ("a home path", "home/runner/notes.md")):
            with self.subTest(case):
                path = self.records / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("clean\n")
                run = self.run_lever("records-sync.sh")
                self.assert_refused(run, "identifier scan")
                self.assertIn("(exit 1); its output is withheld", run.stderr)
                for found in (planted, "runner"):
                    self.assertNotIn(found, run.stdout + run.stderr)
                self.assert_nothing_left()
                path.unlink()

    def test_a_hook_of_the_checkout_never_runs(self):
        """U101 round 6: a post-checkout or pre-commit hook of the checkout's repository dropped files in the sync
        worktree that `add -A` then staged, unmasked and unscanned. The sync now has no worktree: it is built in its
        own repository, which has no hooks, so none of the checkout's runs. Round 12 (audit of 7b3c2718): a
        `core.fsmonitor` hook runs inside `git ls-files`, the lever's one index read in the checkout, and could plant a
        store file there before the copy; the listing turns it off."""
        self.github()
        marker = self.root / "hook-ran"
        hooks = self.repo / ".git/hooks"
        hooks.mkdir(exist_ok=True)
        body = (
            "#!/bin/sh\n"
            "mkdir -p .orchestration/validation .orchestration/orchestrate/other\n"
            "echo hooked > .orchestration/validation/hooked.md\n"
            "echo hooked > .orchestration/orchestrate/other/hooked.md\n"
            "echo hooked > .orchestration/orchestrate/prog/hooked.md\n"
        )
        for name in ("post-checkout", "pre-commit", "post-commit", "pre-push", "reference-transaction"):
            hook = hooks / name
            hook.write_text(body + f"echo {name} >> {marker}\n")
            hook.chmod(0o755)
        fsmonitor = self.root / "fsmonitor-hook"
        fsmonitor.write_text(body + f"echo fsmonitor >> {marker}\n")
        fsmonitor.chmod(0o755)
        self.git("config", "core.fsmonitor", str(fsmonitor))
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.branch_changes(), ["M\t.orchestration/orchestrate/prog/units.tsv"])
        self.assertFalse(marker.exists(), "no hook ran")
        self.assertFalse((self.records / "hooked.md").exists(), "nothing was planted in the store")

    def test_a_tree_entry_outside_the_copy_set_refuses(self):
        """U101 rounds 6 and 8: the new tree's change against main must equal the computed set exactly, so one more
        entry in the index the tree is written from, inside or outside .orchestration/, refuses."""
        self.github()
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        for extra in (".orchestration/validation/extra.md", ".orchestration/orchestrate/other/extra.md", "scripts/x"):
            with self.subTest(extra):
                self.env["FAKE_GIT_EXTRA_ENTRY"] = extra
                run = self.run_lever("records-sync.sh")
                del self.env["FAKE_GIT_EXTRA_ENTRY"]
                self.assert_refused(run, "the new tree changes other paths than the copy set")
                self.assert_nothing_left()
                self.assertEqual(self.gh_calls(), [])
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_the_checkout_s_git_config_has_no_effect_on_the_commit_or_the_push(self):
        """U101 round 8: each round found another channel from the checkout's git config into the sync worktree
        (includeIf rewrites, author config, hooks, clean filters). The commit is now built in a repository of its own,
        so every one of them at once changes nothing: the committed bytes are the store's, the author is the
        identity, and the push reaches origin only."""
        self.github()
        evil, include = self.hostile_include()
        marker = self.root / "filter-ran"
        identity = self.root / "identity.gitconfig"
        identity.write_text("[author]\n\tname = included\n\temail = included@example.invalid\n")
        for key, value in (
            ("filter.evil.clean", f"sh -c 'echo clean >> {marker}; sed s/seats/CLEANED/'"),
            ("filter.evil.smudge", f"sh -c 'echo smudge >> {marker}; sed s/seats/SMUDGED/'"),
            ("filter.evil.required", "true"),
            ("includeIf.gitdir:**/worktrees/**.path", str(include)),
            ("include.path", str(identity)),
            ("committer.name", "repo-committer"),
            ("url./nonexistent-fetch-target/.insteadOf", self.url),
            ("core.hooksPath", str(self.root / "hooks")),
        ):
            self.git("config", key, value)
        (self.repo / ".git/info").mkdir(exist_ok=True)
        (self.repo / ".git/info/attributes").write_text("* filter=evil\n")
        hooks = self.root / "hooks"
        hooks.mkdir()
        for name in ("post-checkout", "pre-commit", "post-commit", "pre-push"):
            (hooks / name).write_text(f"#!/bin/sh\necho {name} >> {marker}\n")
            (hooks / name).chmod(0o755)
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.branch_changes(), ["M\t.orchestration/orchestrate/prog/units.tsv"])
        committed = self.git("show", "records/sync-7:.orchestration/orchestrate/prog/units.tsv", cwd=self.origin)
        self.assertEqual(committed + "\n", (self.records / "units.tsv").read_text(), "no filter touched the bytes")
        people = self.git("log", "-1", "--format=%an <%ae>|%cn <%ce>", "records/sync-7", cwd=self.origin)
        self.assertEqual(people, "t <t@example.invalid>|t <t@example.invalid>")
        self.assertEqual(self.git("for-each-ref", cwd=evil), "", "nothing reached the rewrite's target")
        self.assertFalse(marker.exists(), "no filter or hook of the checkout ran")

    def test_the_committed_blobs_are_the_scanned_bytes(self):
        """U101 round 8: what the identifier scan reads is what is committed, byte for byte. Main's validator is
        wrapped to copy every file it scans; each committed blob equals that copy, masked tokens and rewritten JSON
        included."""
        self.github()
        dump = self.root / "scanned"
        validator = self.repo / "scripts/validate-agent-assets.py"
        text = validator.read_text()
        hook = '    if sys.argv[1:2] == ["--scan-identifiers"]:\n'
        self.assertIn(hook, text)
        validator.write_text(
            text.replace(
                hook,
                hook + "        for _name in sys.argv[sys.argv.index('--') + 1 :]:\n"
                f"            _target = Path({str(dump)!r}) / _name\n"
                "            _target.parent.mkdir(parents=True, exist_ok=True)\n"
                "            _target.write_bytes(Path(_name).read_bytes())\n",
                1,
            )
        )
        self.git("commit", "-q", "-am", "a validator that records what it scans")
        self.git("push", "-q", "origin", "main")
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        (self.records / "notes.md").write_text(f"token {planted}\n")
        (self.records / "evidence.json").write_text('{"b": 1,   "a": "' + planted + '"}')
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)
        prog = ".orchestration/orchestrate/prog"
        for name in ("notes.md", "evidence.json", "units.tsv"):
            with self.subTest(name):
                blob = subprocess.run(
                    ["git", "-C", str(self.origin), "cat-file", "blob", f"records/sync-7:{prog}/{name}"],
                    env=self.env,
                    capture_output=True,
                    check=True,
                ).stdout
                self.assertEqual(blob, (dump / prog / name).read_bytes())
                self.assertNotIn(planted.encode(), blob)

    @unittest.skipUnless(Path("/bin/bash").is_file(), "no /bin/bash")
    def test_the_git_scrub_holds_under_bin_bash_with_an_unwritable_tmpdir(self):
        """U101 round 6: on macOS /bin/bash is 3.2, whose here-strings need a temporary file; the scrub now reads
        compgen through a command substitution. With TMPDIR unwritable and GIT_DIR and GIT_WORK_TREE exported, the
        run gets past every git command that would fail under them and stops at the lever's own mktemp."""
        self.github()
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        locked = self.root / "locked"
        locked.mkdir()
        locked.chmod(0o555)
        self.addCleanup(locked.chmod, 0o755)
        env = self.env | {
            "TMPDIR": str(locked),
            "GIT_DIR": str(self.root / "nonexistent.git"),
            "GIT_WORK_TREE": str(self.root / "nonexistent"),
        }
        run = subprocess.run(
            ["/bin/bash", str(LEVERS / "records-sync.sh")],
            cwd=self.repo,
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("records-sync.sh: mktemp failed", run.stderr)
        self.assertNotIn("not in a git checkout", run.stderr)
        self.assert_nothing_left()
        self.assertEqual(self.gh_calls(), [])

    def test_the_identifier_scan_refuses_what_the_masking_left(self):
        """U101: the scan is a refusal of its own, not a re-run of the masker: with a validator on origin/main whose
        masking leaves the copies as they are, a home path and a secret pattern still stop the run."""
        self.github()
        validator = self.repo / "scripts/validate-agent-assets.py"
        text = validator.read_text()
        hook = '    if sys.argv[1:2] == ["--mask-secrets"]:\n'
        self.assertIn(hook, text)
        validator.write_text(
            text.replace(hook, '    if sys.argv[1:2] == ["--mask-secrets"]:\n        raise SystemExit(0)\n', 1)
        )
        self.git("commit", "-q", "-am", "a masker that masks nothing")
        self.git("push", "-q", "origin", "main")
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        for kind, text in (("a home directory path", "from /Users/someone/x\n"), ("a secret pattern", f"{planted}\n")):
            with self.subTest(kind):
                (self.records / "notes.md").write_text(text)
                run = self.run_lever("records-sync.sh")
                self.assert_refused(run, "identifier scan")
                self.assertIn("(exit 1); its output is withheld", run.stderr)
                self.assertNotIn("notes.md", run.stderr, "not even the path the scan found it in")
                self.assertNotIn(planted, run.stderr)
                self.assert_nothing_left()

    def test_a_listing_that_fails_or_is_cut_short_refuses_before_anything_is_created(self):
        """U101 audit P2: the origin/main listing decides what is deleted, and the store listing what is carried; a
        git failure before or after output and a listing whose last entry is cut short each stop the run first."""
        self.github()
        with (self.records / "units.tsv").open("a") as units:
            units.write("U2\tseats\n")
        cases = (
            ("FAKE_GIT_FAIL", "ls-tree", 1, "git ls-tree origin/main failed"),
            ("FAKE_GIT_FAIL_AFTER", "ls-tree", 1, "git ls-tree origin/main failed"),
            (
                "FAKE_GIT_TRUNCATE",
                "ls-tree",
                2,
                "the listing of origin/main:.orchestration/orchestrate/prog/ ends mid-entry",
            ),
            ("FAKE_GIT_FAIL_AFTER", "ls-files", 1, "git ls-files failed"),
            ("FAKE_GIT_TRUNCATE", "ls-files", 2, "the listing of .orchestration/orchestrate/prog/ ends mid-entry"),
        )
        for variable, command, code, message in cases:
            with self.subTest(variable=variable, command=command):
                self.env[variable] = command
                run = self.run_lever("records-sync.sh")
                del self.env[variable]
                self.assertEqual(run.returncode, code, run.stdout + run.stderr)
                self.assertIn(message, run.stderr)
                self.assert_nothing_left()
                self.assertEqual(self.gh_calls(), [])
        run = self.run_lever("records-sync.sh")
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_a_path_with_a_newline_is_refused_before_any_copy(self):
        """U101 audit P1: a newline in a name ended the component split early, so a symlink at the real name went
        unchecked and cp published its target. Any control character in a path of the copy set is refused."""
        self.github()
        outside = self.root / "outside.md"
        outside.write_text("outside the store\n")
        (self.records / "x\nnotes.md").symlink_to(outside)
        run = self.run_lever("records-sync.sh")
        self.assert_refused(run, "holds a control character")
        self.assert_nothing_left()
        self.assertEqual(self.gh_calls(), [])


if __name__ == "__main__":
    unittest.main()
