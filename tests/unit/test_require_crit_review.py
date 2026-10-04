#!/usr/bin/env python3
"""Exercise the review guard in isolated git repositories."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD = ROOT / "scripts/require-crit-review.py"


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        command,
        cwd=cwd,
        env=merged_env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class ReviewGuardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="crit-guard-test-"))
        run(["git", "init"], self.temp_dir)
        run(["git", "config", "user.email", "codex@example.com"], self.temp_dir)
        run(["git", "config", "user.name", "Codex"], self.temp_dir)
        (self.temp_dir / "README.md").write_text("# Test\n")
        # Stand-in collector: the guard re-runs scripts/pr-feedback.py under
        # --base; this one writes the document $FAKE_COLLECTED points to.
        collector = self.temp_dir / "scripts/pr-feedback.py"
        collector.parent.mkdir()
        collector.write_text(
            "import os, sys\n"
            "assert sys.argv[sys.argv.index('--repo') + 1] == 'mryfmo/dotfiles'\n"
            "if not os.environ.get('FAKE_COLLECTED'):\n"
            "    sys.exit('gh is not authenticated')\n"
            "out = sys.argv[sys.argv.index('--json') + 1]\n"
            "open(out, 'w').write(open(os.environ['FAKE_COLLECTED']).read())\n"
        )
        run(["git", "add", "README.md", "scripts/pr-feedback.py"], self.temp_dir)
        run(["git", "commit", "-m", "init"], self.temp_dir)
        self.collected_dir = Path(tempfile.mkdtemp(prefix="crit-guard-collected-"))
        self.collected = self.collected_dir / "collected.json"
        self.base_sha = self.head_commit()
        self.metadata = self.collected_dir / "metadata.json"
        fake_gh = self.collected_dir / "gh"
        fake_gh.write_text(
            f"#!{sys.executable}\n"
            "import json, os, sys\n"
            "if sys.argv[1:] == ['repo', 'view', '--json', 'nameWithOwner']:\n"
            "    print(json.dumps({'nameWithOwner': os.environ.get('GH_REPO', 'mryfmo/dotfiles')}))\n"
            "else:\n"
            "    assert sys.argv[1:] in (['pr', 'view', '1', '--json', 'headRefOid,baseRefName,baseRefOid'], ['pr', 'view', '1', '--repo', 'mryfmo/dotfiles', '--json', 'headRefOid,baseRefName,baseRefOid'])\n"
            "    if os.environ.get('GH_REPO') and '--repo' not in sys.argv:\n"
            "        print(json.dumps({'headRefOid': 'f' * 40, 'baseRefName': 'main', 'baseRefOid': 'f' * 40}))\n"
            "    else:\n"
            "        print(open(os.environ['FAKE_PR_METADATA']).read())\n"
        )
        fake_gh.chmod(0o755)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)
        shutil.rmtree(self.collected_dir)

    def guard(self, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return run([sys.executable, str(GUARD)], self.temp_dir, env)

    def touch_lifecycle_script(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")

    def write_review_file(self, relative_path: str, content: str) -> Path:
        path = self.temp_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def write_changed_path(self, relative_path: str) -> None:
        run(["git", "clean", "-fd"], self.temp_dir)
        path = self.temp_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("#!/usr/bin/env bash\n")

    def agent_review(
        self, data: object, *, outcome: str = "approved", reviewer: str = "codex"
    ) -> subprocess.CompletedProcess[str]:
        self.touch_lifecycle_script()
        source = ".agents/worklog/review/crit-comments.json"
        self.write_review_file(source, json.dumps(data))
        evidence = self.write_review_file(
            ".agents/worklog/review/agent-crit-data.md",
            f"review_surface: crit-data\nreviewer: {reviewer}\nreview_source: {source}\nreview_outcome: {outcome}\n",
        )
        return self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})

    def test_no_diff_does_not_require_review(self) -> None:
        result = self.guard()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("not required", result.stdout)

    def test_small_docs_only_change_does_not_require_review(self) -> None:
        (self.temp_dir / "README.md").write_text("# Test\n\nSmall note.\n")
        result = self.guard()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("not required", result.stdout)

    def test_high_risk_markdown_change_requires_review(self) -> None:
        codex_rules = self.temp_dir / "home/dot_config/codex"
        codex_rules.mkdir(parents=True)
        (codex_rules / "AGENTS.md").write_text("# Agent policy\n")
        result = self.guard()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("agent lifecycle", result.stdout)

    def test_agent_lifecycle_script_change_requires_review(self) -> None:
        self.touch_lifecycle_script()
        result = self.guard()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Native agent review required", result.stdout)
        self.assertIn("not a browser by default", result.stdout)
        self.assertIn("agent lifecycle", result.stdout)

    def test_agent_lifecycle_surfaces_require_review(self) -> None:
        high_risk_paths = (
            "home/dot_local/bin/common/executable_herdr-agents",
            "home/dot_local/bin/common/executable_agent-fanout",
            "home/dot_config/herdr/config.yaml",
            "home/dot_zshrc",
            "home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl",
        )
        for path in high_risk_paths:
            with self.subTest(path=path):
                self.write_changed_path(path)
                result = self.guard()
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("Native agent review required", result.stdout)

    def test_agent_lifecycle_tokens_require_review(self) -> None:
        high_risk_paths = (
            "docs/herdr.md",
            "docs/agmsg.md",
        )
        for path in high_risk_paths:
            with self.subTest(path=path):
                self.write_changed_path(path)
                result = self.guard()
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("review-sensitive path changed", result.stdout)

    def test_broad_diff_requires_review(self) -> None:
        for index in range(5):
            (self.temp_dir / f"file-{index}.py").write_text("print('x')\n")
        result = self.guard()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("broad diff", result.stdout)

    def test_large_untracked_file_requires_broad_diff_review(self) -> None:
        (self.temp_dir / "generated.py").write_text("print('x')\n" * 201)
        result = self.guard()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("broad diff changes", result.stdout)

    def test_reviewed_environment_satisfies_required_review(self) -> None:
        self.touch_lifecycle_script()
        evidence = self.write_review_file(
            ".agents/worklog/review/crit.md",
            "review_surface: crit-web\nreviewer: user\nreview_outcome: approved\n",
        )
        result = self.guard({"CRIT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CRIT_REVIEWED=1", result.stdout)

    def test_native_reviewed_environment_rejects_human_reviewer(self) -> None:
        self.touch_lifecycle_script()
        evidence = self.write_review_file(
            ".agents/worklog/review/native.md",
            "review_surface: codex-/review\nreviewer: user\nreview_outcome: addressed\n",
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("agent reviewer", result.stdout)

    def test_native_reviewed_without_evidence_still_requires_review(self) -> None:
        self.touch_lifecycle_script()
        result = self.guard({"AGENT_REVIEWED": "1"})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("REVIEW_EVIDENCE", result.stdout)

    def test_reviewed_with_incomplete_evidence_still_requires_review(self) -> None:
        self.touch_lifecycle_script()
        evidence = self.write_review_file(".agents/worklog/review/incomplete.md", "review_surface: codex-/review\n")
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("reviewer", result.stdout)

    def test_reviewed_with_blank_evidence_values_still_requires_review(self) -> None:
        self.touch_lifecycle_script()
        evidence = self.write_review_file(
            ".agents/worklog/review/blank.md",
            "review_surface:\nreviewer: user\nreview_outcome: approved\n",
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("non-empty", result.stdout)

    def test_agent_self_reviewer_evidence_still_requires_review(self) -> None:
        self.touch_lifecycle_script()
        evidence = self.write_review_file(
            ".agents/worklog/review/self.md",
            "review_surface: codex-/review\nreviewer: codex\nreview_outcome: approved\n",
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("review_surface: crit-data", result.stdout)

    def test_agent_reviewer_with_crit_data_satisfies_required_review(self) -> None:
        result = self.agent_review([{"id": "c_1", "body": "Approved", "scope": "review", "resolved": True}])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("AGENT_REVIEWED=1", result.stdout)

    def test_agent_reviewer_with_resolved_line_comment_satisfies_required_review(self) -> None:
        result = self.agent_review(
            [
                {
                    "id": "c_1",
                    "body": "Addressed",
                    "author": "codex",
                    "scope": "line",
                    "path": "scripts/example.py",
                    "resolved": True,
                }
            ],
            outcome="addressed",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_agent_reviewer_rejects_empty_or_malformed_crit_data(self) -> None:
        valid = {"id": "c_1", "body": "Approved", "author": "codex", "scope": "review", "resolved": True}
        cases = {
            "null": None,
            "empty list": [],
            "dict root": {"comments": [valid]},
            "malformed member": ["comment"],
            "unresolved": [{**valid, "resolved": False}],
            "unrelated scope": [{**valid, "scope": "thread"}],
            "line without path": [{**valid, "scope": "line"}],
        }
        for field in ("id", "body", "scope"):
            cases[f"missing {field}"] = [{key: value for key, value in valid.items() if key != field}]
            cases[f"empty {field}"] = [{**valid, field: ""}]
        for name, data in cases.items():
            with self.subTest(name=name):
                result = self.agent_review(data)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_agent_reviewer_rejects_invalid_review_outcome(self) -> None:
        result = self.agent_review(
            [{"id": "c_1", "body": "Approved", "author": "codex", "scope": "review", "resolved": True}],
            outcome="pending",
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("review_outcome", result.stdout)

    def test_agent_reviewer_with_command_string_source_still_requires_review(self) -> None:
        self.touch_lifecycle_script()
        evidence = self.write_review_file(
            ".agents/worklog/review/agent-command-source.md",
            "review_surface: crit-data\n"
            "reviewer: codex\n"
            "review_source: crit comments --json\n"
            "review_outcome: approved\n",
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("JSON evidence file", result.stdout)

    def test_agent_reviewer_with_unresolved_crit_json_still_requires_review(self) -> None:
        self.touch_lifecycle_script()
        self.write_review_file(
            ".agents/worklog/review/crit-comments.json",
            '[{"id":"c_1","body":"fix this","resolved":false}]\n',
        )
        evidence = self.write_review_file(
            ".agents/worklog/review/agent-unresolved.md",
            "review_surface: crit-data\n"
            "reviewer: claude-code\n"
            "review_source: .agents/worklog/review/crit-comments.json\n"
            "review_outcome: approved\n",
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("resolved: true", result.stdout)

    def test_agent_reviewer_with_non_review_crit_json_object_still_requires_review(self) -> None:
        self.touch_lifecycle_script()
        self.write_review_file(".agents/worklog/review/crit-comments.json", "{}\n")
        evidence = self.write_review_file(
            ".agents/worklog/review/agent-empty-object.md",
            "review_surface: crit-data\n"
            "reviewer: codex\n"
            "review_source: .agents/worklog/review/crit-comments.json\n"
            "review_outcome: approved\n",
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("non-empty Crit comment list", result.stdout)

    def test_agent_reviewer_with_external_crit_json_still_requires_review(self) -> None:
        self.touch_lifecycle_script()
        external = Path(tempfile.mkdtemp(prefix="crit-external-")) / "comments.json"
        self.addCleanup(lambda: shutil.rmtree(external.parent, ignore_errors=True))
        external.write_text("null\n")
        evidence = self.write_review_file(
            ".agents/worklog/review/agent-external.md",
            f"review_surface: crit-data\nreviewer: codex\nreview_source: {external}\nreview_outcome: approved\n",
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("repo-local", result.stdout)

    def test_agent_reviewer_with_crit_reviewed_marker_still_requires_review(self) -> None:
        self.touch_lifecycle_script()
        self.write_review_file(".agents/worklog/review/crit-comments.json", "null\n")
        evidence = self.write_review_file(
            ".agents/worklog/review/agent-wrong-marker.md",
            "review_surface: crit-data\n"
            "reviewer: claude-code\n"
            "review_source: .agents/worklog/review/crit-comments.json\n"
            "review_outcome: approved\n",
        )
        result = self.guard({"CRIT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("AGENT_REVIEWED=1", result.stdout)

    def test_agent_self_review_flag_evidence_still_requires_review(self) -> None:
        self.touch_lifecycle_script()
        evidence = self.write_review_file(
            ".agents/worklog/review/self-flag.md",
            "review_surface: codex-/review\nreviewer: user\nreview_outcome: approved\nagent_self_review: true\n",
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("bare agent self-attestation", result.stdout)

    def commit_on_branch(self, relative_path: str) -> None:
        run(["git", "switch", "-c", "feature"], self.temp_dir)
        path = self.temp_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("#!/usr/bin/env bash\n")
        run(["git", "add", relative_path], self.temp_dir)
        run(["git", "commit", "-m", "feature"], self.temp_dir)

    def head_commit(self) -> str:
        return run(["git", "rev-parse", "HEAD"], self.temp_dir).stdout.strip()

    def write_feedback(
        self,
        items: list[dict],
        relative_path: str = ".orchestration/validation/test-pr-feedback.json",
        head_sha: str | None = None,
    ) -> str:
        document = {
            "repo": "mryfmo/dotfiles",
            "pr": 1,
            "head_sha": head_sha or self.head_commit(),
            "base_ref": "main",
            "base_sha": self.base_sha,
            "items": items,
        }
        self.write_review_file(relative_path, json.dumps(document))
        self.write_collected([{key: value for key, value in item.items() if key != "disposition"} for item in items])
        self.metadata.write_text(
            json.dumps(
                {
                    "headRefOid": self.head_commit(),
                    "baseRefName": "main",
                    "baseRefOid": self.base_sha,
                }
            )
        )
        return relative_path

    def write_collected(self, items: list[dict], head_sha: str | None = None) -> None:
        document = {"repo": "mryfmo/dotfiles", "pr": 1, "head_sha": head_sha or self.head_commit(), "items": items}
        self.collected.write_text(json.dumps(document))

    def guard_base(self, env: dict[str, str] | None = None, base: str = "main") -> subprocess.CompletedProcess[str]:
        defaults = {
            "CRIT_REVIEW": "",
            "FAKE_COLLECTED": str(self.collected),
            "FAKE_PR_METADATA": str(self.metadata),
            "PATH": f"{self.collected_dir}{os.pathsep}{os.environ['PATH']}",
        }
        return run([sys.executable, str(GUARD), "--base", base], self.temp_dir, {**defaults, **(env or {})})

    def test_base_reviews_committed_branch_changes(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("scripts/update-agent-assets.sh")

        plain = self.guard()
        self.assertEqual(plain.returncode, 0, plain.stdout)
        self.assertIn("Review not required", plain.stdout)

        feedback = self.write_feedback([{"source": "status", "level": "success", "disposition": "not-applicable:ok"}])
        based = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})
        self.assertEqual(based.returncode, 1, based.stdout)
        self.assertIn("agent lifecycle path changed: scripts/update-agent-assets.sh", based.stdout)

    def test_base_fails_closed_when_unresolvable_or_option_like(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        feedback = self.write_feedback([])
        env = {"CRIT_REVIEW": "", "FAKE_COLLECTED": str(self.collected), "PR_FEEDBACK_EVIDENCE": feedback}
        for base, message in (
            ("no-such-ref", "does not resolve to a commit"),
            ("--output=leak", "is not a git ref"),
            ("", "is not a git ref"),
        ):
            with self.subTest(base=base):
                result = run([sys.executable, str(GUARD), f"--base={base}"], self.temp_dir, env)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn(message, result.stdout)
                self.assertNotIn("PR feedback evidence accepted", result.stdout)
        self.assertFalse((self.temp_dir / "leak").exists())

    def test_base_requires_pr_feedback_evidence(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": ""})

        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("PR_FEEDBACK_EVIDENCE must point to the filled scripts/pr-feedback.py JSON", result.stdout)

    def test_pr_feedback_rejects_incomplete_or_invalid_dispositions(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        commit = self.head_commit()
        cases = {
            "missing disposition": (
                [{"source": "annotation", "level": "notice", "disposition": ""}],
                "needs a disposition",
            ),
            "stopgap wording": (
                [{"source": "review_comment", "level": "comment", "disposition": "later"}],
                "needs a disposition",
            ),
            "unknown commit": (
                [{"source": "annotation", "level": "warning", "disposition": "fixed:deadbee"}],
                "cites an unknown commit: deadbee",
            ),
            "short failure reason": (
                [{"source": "annotation", "level": "failure", "disposition": "not-applicable:flaky"}],
                "failure-level; not-applicable needs a reason of at least 20 characters",
            ),
            "short in-progress reason": (
                [{"source": "check_run", "level": "in_progress", "disposition": "not-applicable:wip"}],
                "in_progress-level; not-applicable needs a reason of at least 20 characters",
            ),
            "short cancelled reason": (
                [{"source": "check_run", "level": "cancelled", "disposition": "not-applicable:rerun"}],
                "cancelled-level; not-applicable needs a reason of at least 20 characters",
            ),
            "not an items document": ([], None),
        }
        for name, (items, message) in cases.items():
            with self.subTest(case=name):
                if message is None:
                    self.write_review_file(".orchestration/validation/test-pr-feedback.json", json.dumps([]))
                    feedback = ".orchestration/validation/test-pr-feedback.json"
                    message = "must be a pr-feedback.py document with an items list"
                else:
                    feedback = self.write_feedback(items)
                result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn(message, result.stdout)
        self.assertTrue(commit)

    def test_pr_feedback_must_be_collected_for_the_current_head(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        feedback = self.write_feedback(
            [{"source": "status", "level": "success", "disposition": "not-applicable:review completed"}],
            head_sha="0" * 40,
        )

        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})

        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(f"not the current HEAD {self.head_commit()}", result.stdout)

    def test_pr_feedback_rejects_evidence_outside_the_repository(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump({"items": []}, handle)
        self.addCleanup(os.unlink, handle.name)

        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": handle.name})

        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("must point to a repo-local JSON file", result.stdout)

    def test_pr_feedback_accepts_complete_root_cause_dispositions(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        commit = self.head_commit()
        feedback = self.write_feedback(
            [
                {"source": "review_comment", "level": "comment", "disposition": f"fixed:{commit[:7]}"},
                {
                    "source": "annotation",
                    "level": "failure",
                    "disposition": "not-applicable:annotation belongs to a job on the base branch run, not this head",
                },
                {"source": "status", "level": "success", "disposition": "not-applicable:review completed"},
            ]
        )

        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn(f"PR feedback evidence accepted: {feedback}", result.stdout)
        self.assertIn("Review not required", result.stdout)

    def test_pr_feedback_evidence_file_is_not_counted_as_a_change(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        items = [
            {"source": "annotation", "level": "notice", "disposition": f"not-applicable:runner notice {index}"}
            for index in range(60)
        ]
        feedback = self.write_feedback(items)
        path = self.temp_dir / feedback
        path.write_text(json.dumps(json.loads(path.read_text()), indent=2))
        self.assertGreater(len(path.read_text().splitlines()), 200)

        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Review not required", result.stdout)

    def test_pr_feedback_must_cover_every_currently_collected_item(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        listed = {"source": "status", "level": "success", "url": "https://x/s", "body": "CodeRabbit: done"}
        unlisted = {"source": "annotation", "level": "warning", "url": "https://x/j", "body": "untrusted taps"}
        for name, evidence_items in (
            ("one item missing", [{**listed, "disposition": "not-applicable:review completed"}]),
            ("hand-written empty list", []),
        ):
            with self.subTest(case=name):
                feedback = self.write_feedback(evidence_items)
                self.write_collected([listed, unlisted])
                result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("current feedback item(s) for PR #1", result.stdout)

    def test_pr_feedback_bodies_are_compared_after_secret_masking(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        key_shaped = "ghp_" + "a" * 25
        quoted = f"quotes {key_shaped} here"
        with_placeholder = f"GITHUB_PERSONAL_ACCESS_TOKEN stays\n{quoted}"
        assignment = "set api_" + 'key = "live-value"'
        for name, live, saved, mask_file, returncode in (
            ("masked with --mask-secrets", quoted, quoted, True, 0),
            ("placeholder on another line, masked", with_placeholder, with_placeholder, True, 0),
            ("quoted assignment, masked", assignment, assignment, True, 0),
            ("verbatim body", quoted, quoted, False, 0),
            ("different body", quoted, "quotes something else here", False, 1),
            ("placeholder dropped from a body without a match", "GITHUB_PERSONAL_ACCESS_TOKEN only", " only", False, 1),
            ("unmasked assignment with another value", assignment, assignment.replace("live", "other"), False, 1),
        ):
            with self.subTest(case=name):
                item = {"source": "review_comment", "level": "comment", "url": "https://x/r1"}
                feedback = self.write_feedback([{**item, "body": saved, "disposition": "not-applicable:quoted only"}])
                path = self.temp_dir / feedback
                if mask_file:
                    masker = ROOT / "scripts/validate-agent-assets.py"
                    run([sys.executable, str(masker), "--mask-secrets", str(path)], self.temp_dir)
                    self.assertIn("<redacted:secret-pattern>", json.loads(path.read_text())["items"][0]["body"])
                self.write_collected([{**item, "body": live}])
                result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})
                self.assertEqual(result.returncode, returncode, result.stdout)
                if returncode:
                    self.assertIn("current feedback item(s) for PR #1", result.stdout)

    def test_pr_feedback_matches_a_masked_path_but_not_an_edited_one(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        live = {"source": "review_comment", "level": "comment", "url": "https://x/r1", "body": "nit"}
        live["path"] = "docs/ghp_" + "c" * 25 + ".md"
        masker = ROOT / "scripts/validate-agent-assets.py"
        for name, saved_path, mask_file, returncode in (
            ("masked with --mask-secrets", live["path"], True, 0),
            ("edited path", "docs/other.md", False, 1),
        ):
            with self.subTest(case=name):
                feedback = self.write_feedback([{**live, "path": saved_path, "disposition": "not-applicable:a nit"}])
                if mask_file:
                    run([sys.executable, str(masker), "--mask-secrets", str(self.temp_dir / feedback)], self.temp_dir)
                self.write_collected([live])
                result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})
                self.assertEqual(result.returncode, returncode, result.stdout)

    def test_pr_feedback_requires_the_github_head_to_match(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        feedback = self.write_feedback([])
        self.write_collected([], head_sha="1" * 40)

        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})

        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("head on GitHub is 1111", result.stdout)
        self.assertIn("push first", result.stdout)

    def test_pr_feedback_accepts_complete_evidence_without_a_bot_review(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        feedback = self.write_feedback(
            [{"source": "status", "level": "success", "url": "https://x/s", "disposition": "not-applicable:ok"}]
        )
        self.assertFalse(any(item["source"] == "review" for item in json.loads(self.collected.read_text())["items"]))

        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn(f"PR feedback evidence accepted: {feedback}", result.stdout)

    def test_pr_feedback_uses_the_base_collector_not_the_prs_own(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        run(["git", "switch", "-c", "feature"], self.temp_dir)
        tampered = self.temp_dir / "scripts/pr-feedback.py"
        tampered.write_text(
            "import json, sys\n"
            "out = sys.argv[sys.argv.index('--json') + 1]\n"
            "open(out, 'w').write(json.dumps({'head_sha': 'x', 'items': []}))\n"
        )
        run(["git", "commit", "-am", "tamper with the collector"], self.temp_dir)
        feedback = self.write_feedback([])
        unlisted = {"source": "annotation", "level": "warning", "url": "https://x/j", "body": "untrusted taps"}
        self.write_collected([unlisted])

        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})

        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("lacks 1 current feedback item(s) for PR #1", result.stdout)

    def test_pr_feedback_fails_when_the_collector_cannot_run(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        feedback = self.write_feedback([])

        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback, "FAKE_COLLECTED": ""})

        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("could not re-collect PR #1 feedback", result.stdout)

    def test_pr_feedback_without_base_is_only_format_checked(self) -> None:
        feedback = self.write_feedback([{"source": "status", "level": "success", "disposition": "not-applicable:ok"}])

        result = self.guard({"PR_FEEDBACK_EVIDENCE": feedback, "CRIT_REVIEW": ""})

        self.assertIn("PR feedback evidence format checked only", result.stdout)
        self.assertNotIn("PR feedback evidence accepted", result.stdout)

    def test_feedback_cannot_hide_an_arbitrary_path_without_base(self) -> None:
        for path in (
            "scripts/policy.json",
            "docs/test-pr-feedback.json",
            ".orchestration/validation/feedback.json",
            ".orchestration/validation/../test-pr-feedback.json",
        ):
            with self.subTest(path=path):
                feedback = self.write_feedback([], relative_path=path)
                result = self.guard({"PR_FEEDBACK_EVIDENCE": feedback})
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn(
                    "evidence must live under .orchestration/validation/ and end with -pr-feedback.json", result.stdout
                )

    def test_feedback_symlink_cannot_hide_a_file_outside_validation(self) -> None:
        target = self.write_feedback([], relative_path="docs/test-pr-feedback.json")
        link = self.temp_dir / ".orchestration/validation/test-pr-feedback.json"
        link.parent.mkdir(parents=True)
        link.symlink_to(self.temp_dir / target)
        result = self.guard({"PR_FEEDBACK_EVIDENCE": str(link)})
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("evidence must live under", result.stdout)

    def test_feedback_does_not_exclude_symlink_aliases_outside_validation(self) -> None:
        feedback = self.write_feedback([])
        (self.temp_dir / "scripts/policy.json").symlink_to(self.temp_dir / feedback)
        result = self.guard({"PR_FEEDBACK_EVIDENCE": feedback})
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("scripts/policy.json", result.stdout)

    def test_feedback_path_itself_must_be_under_validation(self) -> None:
        feedback = self.write_feedback([])
        alias = self.temp_dir / "scripts/policy.json"
        alias.symlink_to(self.temp_dir / feedback)
        result = self.guard({"PR_FEEDBACK_EVIDENCE": str(alias)})
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("evidence must live under", result.stdout)

    def test_feedback_accepts_absolute_path_through_a_repository_parent_alias(self) -> None:
        feedback = self.write_feedback(
            [
                {"source": "annotation", "level": "notice", "disposition": "not-applicable:runner notice"}
                for _ in range(60)
            ]
        )
        path = self.temp_dir / feedback
        path.write_text(json.dumps(json.loads(path.read_text()), indent=2))
        alias = self.collected_dir / "parent-alias"
        alias.symlink_to(self.temp_dir.parent, target_is_directory=True)
        evidence = alias / self.temp_dir.name / feedback
        result = self.guard({"PR_FEEDBACK_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Review not required", result.stdout)

    def test_advanced_base_cannot_supply_an_untrusted_collector(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        feedback = self.write_feedback([])
        self.write_collected([{"source": "annotation", "level": "warning", "body": "must fix"}])
        run(["git", "switch", "-c", "forged-base", "main"], self.temp_dir)
        collector = self.temp_dir / "scripts/pr-feedback.py"
        collector.write_text(
            "import json, os, sys\n"
            "open('executed', 'w').write('untrusted')\n"
            "data = json.load(open(os.environ['FAKE_COLLECTED']))\n"
            "data['items'] = []\n"
            "open(sys.argv[-1], 'w').write(json.dumps(data))\n"
        )
        run(["git", "commit", "-am", "untrusted base collector"], self.temp_dir)
        run(["git", "switch", "feature"], self.temp_dir)
        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback}, base="forged-base")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertFalse((self.temp_dir / "executed").exists())

    def test_advanced_base_cannot_delete_collector_to_trigger_head_fallback(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        collector = self.temp_dir / "scripts/pr-feedback.py"
        collector.write_text(collector.read_text() + "open('executed', 'w').write('untrusted')\n")
        run(["git", "commit", "-am", "head collector"], self.temp_dir)
        feedback = self.write_feedback([])
        self.write_collected([{"source": "annotation", "level": "warning", "body": "must fix"}])
        run(["git", "switch", "-c", "forged-base", "main"], self.temp_dir)
        run(["git", "rm", "scripts/pr-feedback.py"], self.temp_dir)
        run(["git", "commit", "-m", "delete base collector"], self.temp_dir)
        run(["git", "switch", "feature"], self.temp_dir)
        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback}, base="forged-base")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertFalse((self.temp_dir / "executed").exists())

    def test_base_rejects_pr_commits_before_executing_their_collector(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        first = self.head_commit()
        collector = self.temp_dir / "scripts/pr-feedback.py"
        collector.write_text(collector.read_text() + "open('executed', 'w').write('untrusted')\n")
        run(["git", "commit", "-am", "replace collector"], self.temp_dir)
        feedback = self.write_feedback([])
        for base in ("HEAD", first, "feature"):
            with self.subTest(base=base):
                result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback}, base=base)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("is not bound to PR #1 base", result.stdout)
                self.assertFalse((self.temp_dir / "executed").exists())

    def test_base_rejects_forged_evidence_metadata(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        feedback = self.write_feedback([])
        path = self.temp_dir / feedback
        original = json.loads(path.read_text())
        for field, value in (("base_sha", self.head_commit()), ("base_ref", "feature"), ("base_sha", None)):
            with self.subTest(field=field, value=value):
                path.write_text(json.dumps({**original, field: value}))
                result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback}, base="HEAD")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("does not match the GitHub base", result.stdout)

    def test_base_accepts_exact_and_advanced_base_with_unchanged_merge_base(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        run(["git", "commit", "--allow-empty", "-m", "advance main"], self.temp_dir)
        self.base_sha = self.head_commit()
        self.commit_on_branch("docs/fix.md")
        feedback = self.write_feedback([])
        run(["git", "switch", "main"], self.temp_dir)
        run(["git", "commit", "--allow-empty", "-m", "advance after collection"], self.temp_dir)
        run(["git", "switch", "feature"], self.temp_dir)
        for base in (self.base_sha, "main"):
            with self.subTest(base=base):
                result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback}, base=base)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_older_base_must_not_be_on_the_head_first_parent_chain(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        shared = self.base_sha
        self.commit_on_branch("docs/fix.md")
        run(["git", "switch", "main"], self.temp_dir)
        run(["git", "commit", "--allow-empty", "-m", "older main commit"], self.temp_dir)
        older = self.head_commit()
        run(["git", "commit", "--allow-empty", "-m", "current main commit"], self.temp_dir)
        self.base_sha = self.head_commit()
        run(["git", "switch", "feature"], self.temp_dir)
        feedback = self.write_feedback([])
        accepted = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback}, base=older)
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        rejected = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback}, base=shared)
        self.assertEqual(rejected.returncode, 1, rejected.stdout)
        self.assertIn("is not bound to PR #1 base", rejected.stdout)
        run(["git", "merge", "--no-ff", "--no-edit", "main"], self.temp_dir)
        feedback = self.write_feedback([])
        merged = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback}, base=older)
        self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)

    def test_base_rejects_side_branch_and_advanced_base_containing_pr_commits(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        feedback = self.write_feedback([])
        run(["git", "switch", "-c", "absorbed"], self.temp_dir)
        run(["git", "commit", "--allow-empty", "-m", "contains PR head"], self.temp_dir)
        run(["git", "switch", "--orphan", "unrelated"], self.temp_dir)
        run(["git", "commit", "--allow-empty", "-m", "unrelated"], self.temp_dir)
        run(["git", "switch", "feature"], self.temp_dir)
        for base in ("absorbed", "unrelated"):
            with self.subTest(base=base):
                result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback}, base=base)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("is not bound to PR #1 base", result.stdout)

    def test_missing_base_collector_falls_back_only_after_binding(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        collector = self.temp_dir / "scripts/pr-feedback.py"
        source = collector.read_text()
        run(["git", "rm", "scripts/pr-feedback.py"], self.temp_dir)
        run(["git", "commit", "-m", "base has no collector"], self.temp_dir)
        self.base_sha = self.head_commit()
        self.commit_on_branch("scripts/pr-feedback.py")
        collector.write_text(source)
        run(["git", "commit", "-am", "introduce collector"], self.temp_dir)
        feedback = self.write_feedback([])
        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})
        self.assertIn("PR feedback evidence accepted", result.stdout)
        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback}, base="HEAD")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("is not bound to PR #1 base", result.stdout)

    def test_base_fails_closed_when_github_metadata_is_unavailable(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        feedback = self.write_feedback([])
        for metadata in ("not JSON", "{}", json.dumps({"baseRefOid": "-HEAD"})):
            with self.subTest(metadata=metadata):
                self.metadata.write_text(metadata)
                result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("could not verify PR #1 base on GitHub", result.stdout)

    def test_fixed_commit_is_checked_against_github_base_not_an_older_side_parent(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        run(["git", "switch", "-c", "side"], self.temp_dir)
        run(["git", "commit", "--allow-empty", "-m", "side change"], self.temp_dir)
        side = self.head_commit()
        run(["git", "switch", "main"], self.temp_dir)
        run(["git", "merge", "--no-ff", "--no-edit", "side"], self.temp_dir)
        self.base_sha = self.head_commit()
        self.commit_on_branch("docs/fix.md")
        feedback = self.write_feedback(
            [
                {
                    "source": "review_comment",
                    "level": "comment",
                    "disposition": f"fixed:{self.base_sha}",
                }
            ]
        )
        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback}, base=side)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("outside", result.stdout)
        self.assertIn("cite the fix commit in this PR", result.stdout)

    def test_github_lookup_ignores_environment_repository_override(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        feedback = self.write_feedback([])
        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback, "GH_REPO": "attacker/fork"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_github_lookup_rejects_evidence_from_another_repository(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        feedback = self.write_feedback([])
        path = self.temp_dir / feedback
        document = json.loads(path.read_text())
        document["repo"] = "attacker/fork"
        path.write_text(json.dumps(document))
        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("does not match the local GitHub repository", result.stdout)

    def test_recollection_must_match_the_authenticated_repository(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        feedback = self.write_feedback([])
        collected = json.loads(self.collected.read_text())
        collected["repo"] = "attacker/fork"
        self.collected.write_text(json.dumps(collected))
        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("collected feedback does not match", result.stdout)

    def test_pr_feedback_fixed_commit_must_be_in_the_pr_range(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        base_commit = self.head_commit()
        run(["git", "switch", "-c", "elsewhere"], self.temp_dir)
        (self.temp_dir / "other.md").write_text("other\n")
        run(["git", "add", "other.md"], self.temp_dir)
        run(["git", "commit", "-m", "elsewhere"], self.temp_dir)
        unrelated_commit = self.head_commit()
        run(["git", "switch", "main"], self.temp_dir)
        self.commit_on_branch("docs/fix.md")
        for label, commit in (("predates the base", base_commit), ("not in HEAD", unrelated_commit)):
            with self.subTest(case=label):
                feedback = self.write_feedback(
                    [{"source": "review_comment", "level": "comment", "disposition": f"fixed:{commit[:7]}"}]
                )
                result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback})
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn(f"cites commit {commit[:7]} outside GitHub base {base_commit}..HEAD", result.stdout)

    def test_explicit_disable_skips_guard(self) -> None:
        self.touch_lifecycle_script()
        result = self.guard({"CRIT_REVIEW": "off"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CRIT_REVIEW=off", result.stdout)

    def audit_guard(
        self,
        audit_text: str | None,
        *,
        transcript: str = "exec\ngit diff\ncodex\nreview\n",
        sha: str | None = None,
        audit_path: str | None = None,
        dispositions: str | None = None,
        last_symlink: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """Run --base on a reviewed lifecycle change whose feedback and review evidence pass.

        The transcript goes to the audit file and audit_text to its `.last.md` companion
        (codex's final message); last_symlink makes the companion a symlink instead.
        """
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch("scripts/update-agent-assets.sh")
        feedback = self.write_feedback([])
        source = ".agents/worklog/review/crit-comments.json"
        self.write_review_file(
            source, json.dumps([{"id": "c1", "body": "approved", "scope": "review", "resolved": True}])
        )
        receipt = self.write_review_file(
            ".agents/worklog/review/receipt.md",
            f"review_surface: crit-data\nreviewer: claude-code\nreview_source: {source}\nreview_outcome: approved\n",
        )
        env = {
            "PR_FEEDBACK_EVIDENCE": feedback,
            "AGENT_REVIEWED": "1",
            "REVIEW_EVIDENCE": str(receipt),
            "AUDIT_EVIDENCE": "",
            "AUDIT_DISPOSITIONS": "",
        }
        if audit_text is not None:
            audit = audit_path or f".orchestration/validation/test-audit-{sha or self.head_commit()[:7]}.md"
            self.write_review_file(audit, transcript)
            if last_symlink is not None:
                (self.temp_dir / f"{audit}.last.md").symlink_to(last_symlink)
            else:
                self.write_review_file(f"{audit}.last.md", audit_text)
            env["AUDIT_EVIDENCE"] = audit
        if dispositions is not None:
            env["AUDIT_DISPOSITIONS"] = ".orchestration/acceptance/t1.md"
            self.write_review_file(env["AUDIT_DISPOSITIONS"], dispositions)
        return self.guard_base(env)

    def test_base_requires_audit_evidence_for_a_reviewed_change(self) -> None:
        result = self.audit_guard(None)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("AUDIT_EVIDENCE must point to the task-level audit of HEAD", result.stdout)
        self.assertIn("agent lifecycle path changed: scripts/update-agent-assets.sh", result.stdout)

    def test_base_accepts_a_correct_audit_of_head(self) -> None:
        result = self.audit_guard("[P3] high spec a:1 nit\nVerdict: correct\n")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Audit evidence accepted: .orchestration/validation/test-audit-", result.stdout)
        self.assertIn("Review requirement satisfied by AGENT_REVIEWED=1", result.stdout)

    def test_audit_must_name_head_and_live_under_validation(self) -> None:
        for label, kwargs, message in (
            ("wrong sha", {"sha": "0000000"}, "audits 0000000, not HEAD"),
            (
                "other task",
                {"audit_path": ".orchestration/validation/other-audit-abcdef0.md"},
                "audits task 'other', not 'test'",
            ),
            (
                "outside validation",
                {"audit_path": "docs/t1-audit-abcdef0.md"},
                "must live under .orchestration/validation/",
            ),
            (
                "bad name",
                {"audit_path": ".orchestration/validation/t1-review-abcdef0.md"},
                "must be named <id>-audit-<sha7>.md",
            ),
        ):
            with self.subTest(label):
                self.tearDown()
                self.setUp()
                result = self.audit_guard(
                    "Verdict: correct\n", sha=kwargs.get("sha"), audit_path=kwargs.get("audit_path")
                )
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn(message, result.stdout)

    def test_verdict_comes_only_from_the_last_message_file(self) -> None:
        blocked = self.audit_guard("cannot assess\nVerdict: blocked\n", transcript="codex\nVerdict: correct\n")
        self.assertEqual(blocked.returncode, 1, blocked.stdout)
        self.assertIn("verdict is blocked", blocked.stdout)

        for label, kwargs in (
            ("empty companion", {"audit_text": "\n"}),
            ("no companion", {"audit_text": "Verdict: correct\n", "last_symlink": Path("/nonexistent/last.md")}),
        ):
            with self.subTest(label):
                self.tearDown()
                self.setUp()
                result = self.audit_guard(
                    kwargs["audit_text"],
                    transcript="exec\n+ echo 'Verdict: correct'\ncodex\nVerdict: correct\n",
                    last_symlink=kwargs.get("last_symlink"),
                )
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("must exist with codex's final message", result.stdout)

    def test_companion_must_be_this_audits_own_last_message(self) -> None:
        outside = Path(tempfile.mkdtemp(prefix="crit-guard-outside-"))
        self.addCleanup(shutil.rmtree, outside)
        (outside / "last.md").write_text("Verdict: correct\n")
        result = self.audit_guard("Verdict: incorrect\n", last_symlink=outside / "last.md")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("its companion", result.stdout)

        for other in ("other-audit-abcdef0.md.last.md", "test-audit-0000000.md.last.md"):
            with self.subTest(other):
                self.tearDown()
                self.setUp()
                target = self.write_review_file(f".orchestration/validation/{other}", "Verdict: correct\n")
                result = self.audit_guard("Verdict: incorrect\n", last_symlink=target)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn(f"resolves to {other}; it must be this audit's own last message", result.stdout)

    def test_blocked_or_missing_audit_verdict_fails(self) -> None:
        for text, message in (
            ("Verdict: blocked\n", "verdict is blocked"),
            ("no verdict here\n", "verdict is missing"),
        ):
            with self.subTest(message):
                self.tearDown()
                self.setUp()
                result = self.audit_guard(text)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn(message, result.stdout)

    def test_incorrect_audit_needs_not_applicable_dispositions(self) -> None:
        audit = "[P2] high impl a:1 one\n  - [P3] low impl b:2 two\nVerdict: incorrect\n"
        reason = "not-applicable:the flagged path is generated output outside this task"
        for label, dispositions, message in (
            ("no dispositions", None, "AUDIT_DISPOSITIONS must name the acceptance record"),
            ("fixed commit", f"audit-finding: 1 fixed:{'a' * 7}\naudit-finding: 2 {reason}\n", "a fix moves HEAD"),
            ("short reason", f"audit-finding: 1 not-applicable:nope\naudit-finding: 2 {reason}\n", "at least 20"),
            ("one missing", f"audit-finding: 1 {reason}\n", "leaves audit finding(s) 2 of 2 without a disposition"),
            ("unnumbered repeat", f"audit-finding: x {reason}\naudit-finding: x {reason}\n", "must name its finding"),
            (
                "same finding twice",
                f"audit-finding: 1 {reason}\naudit-finding: 1 {reason}\n",
                "finding 1 more than once",
            ),
            ("out of range", f"audit-finding: 1 {reason}\naudit-finding: 3 {reason}\n", "<1-2>"),
            ("accepted", f"# acceptance\naudit-finding: 1 {reason}\naudit-finding: 2 {reason}\n", None),
        ):
            with self.subTest(label):
                self.tearDown()
                self.setUp()
                result = self.audit_guard(audit, dispositions=dispositions)
                if message is None:
                    self.assertEqual(result.returncode, 0, result.stdout)
                    self.assertIn("Audit evidence accepted", result.stdout)
                else:
                    self.assertEqual(result.returncode, 1, result.stdout)
                    self.assertIn(message, result.stdout)

    def test_incorrect_audit_without_findings_fails(self) -> None:
        result = self.audit_guard(
            "Verdict: incorrect\n", dispositions="audit-finding: x not-applicable:nothing to see here at all\n"
        )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("lists no [P0-P3] finding", result.stdout)

    def test_orchestration_only_pr_needs_no_audit(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        self.commit_on_branch(".orchestration/reports/t1.md")
        feedback = self.write_feedback([])

        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback, "AUDIT_EVIDENCE": ""})

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Review not required", result.stdout)
        self.assertNotIn("AUDIT_EVIDENCE", result.stdout)

    def test_broad_orchestration_only_pr_needs_no_audit(self) -> None:
        run(["git", "branch", "-M", "main"], self.temp_dir)
        run(["git", "switch", "-c", "feature"], self.temp_dir)
        for index in range(5):
            self.write_review_file(f".orchestration/reports/t{index}.md", "line\n" * 50)
        run(["git", "add", ".orchestration"], self.temp_dir)
        run(["git", "commit", "-m", "boundary"], self.temp_dir)
        feedback = self.write_feedback([])

        result = self.guard_base({"PR_FEEDBACK_EVIDENCE": feedback, "AUDIT_EVIDENCE": ""})

        self.assertIn("broad diff touches", result.stdout)
        self.assertNotIn("AUDIT_EVIDENCE", result.stdout)
        self.assertNotIn("Task-level audit evidence is required", result.stdout)


if __name__ == "__main__":
    unittest.main()
