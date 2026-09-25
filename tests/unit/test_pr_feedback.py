#!/usr/bin/env python3
"""Exercise pr-feedback.py against recorded GitHub API shapes (no network)."""

from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from typing import Any
from unittest import mock

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/pr-feedback.py"
REPO = "mryfmo/dotfiles"
SHA = "aa17407b680691a42f421721479d7cd14c4421fa"
BOT = {"login": "coderabbitai[bot]", "type": "Bot"}
HUMAN = {"login": "moriya-fumio-thd", "type": "User"}
ACTIONS = {"slug": "github-actions"}

# Shapes recorded from mryfmo/dotfiles #180 and #181, trimmed to the fields read.
RESPONSES: dict[str, Any] = {
    f"repos/{REPO}/pulls/180": {"head": {"sha": SHA}},
    f"repos/{REPO}/issues/180/comments": [
        [{"user": BOT, "body": "Summary by CodeRabbit", "html_url": "https://x/c1"}],
        [
            {
                "user": HUMAN,
                "body": "@coderabbitai full review",
                "html_url": "https://x/c2",
            }
        ],
    ],
    f"repos/{REPO}/pulls/180/reviews": [
        [
            {
                "user": BOT,
                "state": "COMMENTED",
                "body": "**Actionable comments posted: 1**",
                "html_url": "https://x/r1",
                "commit_id": SHA,
            }
        ]
    ],
    f"repos/{REPO}/pulls/180/comments": [
        [
            {
                "id": 11,
                "user": BOT,
                "body": "Key by render file",
                "html_url": "https://x/rc11",
                "path": "scripts/validate-agent-assets.py",
                "line": None,
                "original_line": 569,
            },
            {
                "id": 12,
                "user": BOT,
                "body": "Match unquoted literals",
                "html_url": "https://x/rc12",
                "path": "scripts/validate-agent-assets.py",
                "line": 551,
            },
            {
                "id": 13,
                "user": HUMAN,
                "body": "Reply beyond the first hundred comments of the thread",
                "html_url": "https://x/rc13",
                "path": "scripts/pr-feedback.py",
                "line": 155,
            },
        ]
    ],
    f"repos/{REPO}/commits/{SHA}/check-runs": [
        {
            "check_runs": [
                {
                    "id": 1,
                    "name": "test (ubuntu-latest, server)",
                    "status": "completed",
                    "conclusion": "success",
                    "html_url": "https://x/j1",
                    "app": ACTIONS,
                    "output": {"title": None, "summary": None, "annotations_count": 1},
                },
                {
                    "id": 2,
                    "name": "validate",
                    "status": "completed",
                    "conclusion": "success",
                    "html_url": "https://x/j2",
                    "app": ACTIONS,
                    "output": {"annotations_count": 0},
                },
            ]
        },
        {
            "check_runs": [
                {
                    "id": 3,
                    "name": "public-bootstrap (macos-14, client)",
                    "status": "completed",
                    "conclusion": "failure",
                    "html_url": "https://x/j3",
                    "app": ACTIONS,
                    "output": {
                        "title": "Bootstrap failed",
                        "summary": "exit 1",
                        "annotations_count": 2,
                    },
                }
            ]
        },
    ],
    f"repos/{REPO}/check-runs/1/annotations": [
        [
            {
                "path": ".github",
                "start_line": 1,
                "annotation_level": "notice",
                "title": "",
                "message": "The ubuntu-latest label will migrate to Ubuntu 26",
            }
        ]
    ],
    f"repos/{REPO}/check-runs/3/annotations": [
        [
            {
                "path": ".github",
                "start_line": 1,
                "annotation_level": "failure",
                "title": "",
                "message": "crit: no bottle available!",
            },
            {
                "path": ".github",
                "start_line": 1,
                "annotation_level": "warning",
                "title": "Untrusted taps",
                "message": "The following taps are not trusted",
            },
        ]
    ],
    f"repos/{REPO}/commits/{SHA}/statuses": [
        [
            {
                "context": "CodeRabbit",
                "state": "success",
                "description": "Review skipped: manual review required for this OSS repository",
                "target_url": None,
                "creator": BOT,
            },
            {
                "context": "CodeRabbit",
                "state": "pending",
                "description": "Review in progress",
                "target_url": None,
                "creator": BOT,
            },
        ]
    ],
}
NO_MORE = {"hasNextPage": False, "endCursor": None}
THREADS = {
    None: {
        "nodes": [
            {
                "id": "T1",
                "isResolved": True,
                "isOutdated": True,
                "comments": {"nodes": [{"databaseId": 11}], "pageInfo": NO_MORE},
            }
        ],
        "pageInfo": {"hasNextPage": True, "endCursor": "c1"},
    },
    "c1": {
        "nodes": [
            {
                "id": "T2",
                "isResolved": False,
                "isOutdated": False,
                "comments": {"nodes": [{"databaseId": 12}], "pageInfo": NO_MORE},
            },
            {
                "id": "T3",
                "isResolved": True,
                "isOutdated": False,
                "comments": {
                    "nodes": [{"databaseId": 14}],
                    "pageInfo": {"hasNextPage": True, "endCursor": "t3c1"},
                },
            },
        ],
        "pageInfo": NO_MORE,
    },
}
# Second page of T2's comments: the 101st comment onward keeps the thread state.
THREAD_COMMENT_PAGES = {
    ("T3", "t3c1"): {"nodes": [{"databaseId": 13}], "pageInfo": NO_MORE},
}


def load_script():
    spec = importlib.util.spec_from_file_location("pr_feedback", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fetch(path: str, _paginate: bool) -> Any:
    return RESPONSES[path]


def graphql(_query: str, variables: dict[str, Any]) -> Any:
    if "id" in variables:
        page = THREAD_COMMENT_PAGES[(variables["id"], variables["cursor"])]
        return {"data": {"node": {"comments": page}}}
    return {"data": {"repository": {"pullRequest": {"reviewThreads": THREADS[variables["cursor"]]}}}}


class PrFeedbackTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_script()
        self.document = self.module.collect(REPO, 180, fetch, graphql)
        self.items = self.document["items"]

    def by_source(self, source: str) -> list[dict[str, Any]]:
        return [entry for entry in self.items if entry["source"] == source]

    def test_collects_every_feedback_source_for_the_head(self) -> None:
        self.assertEqual(self.document["head_sha"], SHA)
        self.assertEqual(
            [entry["source"] for entry in self.items],
            [
                "issue_comment",
                "issue_comment",
                "review",
                "review_comment",
                "review_comment",
                "review_comment",
                "annotation",
                "check_run",
                "annotation",
                "annotation",
                "status",
            ],
        )

    def test_every_item_carries_the_disposition_schema(self) -> None:
        keys = {
            "source",
            "author",
            "bot",
            "level",
            "path",
            "line",
            "body",
            "url",
            "disposition",
        }
        for entry in self.items:
            self.assertTrue(keys <= set(entry), entry)
            self.assertEqual(entry["disposition"], "")
        json.dumps(self.document)

    def test_bots_are_detected_from_type_login_or_app(self) -> None:
        authors = {
            (entry["source"], entry["author"], entry["bot"]) for entry in self.items
        }
        self.assertIn(("issue_comment", "coderabbitai[bot]", True), authors)
        self.assertIn(("issue_comment", "moriya-fumio-thd", False), authors)
        self.assertIn(("annotation", "github-actions", True), authors)
        self.assertIn(("status", "coderabbitai[bot]", True), authors)

    def test_review_comments_carry_thread_resolution_across_pages(self) -> None:
        comments = {entry["url"]: entry for entry in self.by_source("review_comment")}
        self.assertEqual(
            (
                comments["https://x/rc11"]["resolved"],
                comments["https://x/rc11"]["line"],
            ),
            (True, 569),
        )
        self.assertEqual(
            (
                comments["https://x/rc12"]["resolved"],
                comments["https://x/rc12"]["line"],
            ),
            (False, 551),
        )

    def test_thread_state_covers_comments_beyond_the_first_page(self) -> None:
        comments = {entry["url"]: entry for entry in self.by_source("review_comment")}
        # Comment 13 is on T3's second GraphQL comment page; without paging it
        # would default to unresolved.
        self.assertEqual(
            (comments["https://x/rc13"]["resolved"], comments["https://x/rc13"]["outdated"]),
            (True, False),
        )

    def test_annotations_keep_every_level_even_on_passing_checks(self) -> None:
        levels = sorted(entry["level"] for entry in self.by_source("annotation"))
        self.assertEqual(levels, ["failure", "notice", "warning"])
        warning = next(
            entry
            for entry in self.by_source("annotation")
            if entry["level"] == "warning"
        )
        self.assertEqual(
            warning["body"], "Untrusted taps The following taps are not trusted"
        )
        self.assertEqual(warning["check"], "public-bootstrap (macos-14, client)")

    def test_only_non_passing_check_runs_become_items(self) -> None:
        self.assertEqual(
            [entry["check"] for entry in self.by_source("check_run")],
            ["public-bootstrap (macos-14, client)"],
        )
        self.assertEqual(
            self.by_source("check_run")[0]["body"],
            "public-bootstrap (macos-14, client): Bootstrap failed exit 1",
        )
        self.assertEqual(len(self.document["checks"]), 3)

    def test_commit_status_keeps_the_latest_state_per_context(self) -> None:
        statuses = self.by_source("status")
        self.assertEqual(len(statuses), 1)
        self.assertEqual(statuses[0]["level"], "success")
        self.assertIn("Review skipped: manual review required", statuses[0]["body"])

    def test_unauthenticated_gh_exits_non_zero(self) -> None:
        def unauthenticated(command, **_kwargs):
            return subprocess.CompletedProcess(command, 1, "", "not logged in")

        # Patch the shared subprocess module only for this call; it is global.
        with (
            mock.patch.object(self.module.subprocess, "run", unauthenticated),
            redirect_stderr(io.StringIO()) as stderr,
            self.assertRaises(SystemExit) as raised,
        ):
            self.module.main(["180", "--repo", REPO])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("gh auth login", stderr.getvalue())

    def test_gh_never_receives_forced_colour(self) -> None:
        with mock.patch.dict(self.module.os.environ, {"CLICOLOR_FORCE": "1"}):
            env = self.module.gh_env()
        self.assertNotIn("CLICOLOR_FORCE", env)
        self.assertEqual(env["NO_COLOR"], "1")

    def test_main_writes_the_document_to_json(self) -> None:
        self.module.require_auth = lambda: None
        self.module.collect = lambda repo, number: self.document
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary) / "feedback.json"
            with redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(
                    self.module.main(["180", "--repo", REPO, "--json", str(out)]), 0
                )
            self.assertEqual(json.loads(out.read_text())["items"], self.items)
        self.assertIn("11 items", stderr.getvalue())



class PrIntegrationRuleParityTest(unittest.TestCase):
    """Keep the PR integration rule, its mirrors, and the skills in step."""

    TOKENS = (
        "scripts/pr-feedback.py",
        "@coderabbitai full review",
        "fixed:<commit>",
        "not-applicable:",
        "BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review",
    )

    def test_rule_symlink_points_at_the_rule(self) -> None:
        self.assertEqual(
            (ROOT / "home/dot_claude/rules/symlink_pr-integration.md.tmpl").read_text(),
            "{{ .chezmoi.sourceDir }}/dot_config/claude/rules/pr-integration.md\n",
        )

    def test_rule_mirrors_and_skills_carry_the_same_requirements(self) -> None:
        codex = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
        codex_section = codex.split("## PR 統合", 1)[1].split("\n## ", 1)[0]
        sources = {
            "claude rule": (ROOT / "home/dot_config/claude/rules/pr-integration.md").read_text(),
            "codex mirror": codex_section,
            "gh-first-workflow": (ROOT / "home/dot_agents/skills/gh-first-workflow/SKILL.md").read_text(),
            "agmsg-orchestration": (ROOT / "home/dot_agents/skills/agmsg-orchestration/SKILL.md").read_text(),
        }
        for name, text in sources.items():
            for token in self.TOKENS:
                with self.subTest(source=name, token=token):
                    self.assertIn(token, text)

if __name__ == "__main__":
    unittest.main()
