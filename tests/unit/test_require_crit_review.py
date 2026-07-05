#!/usr/bin/env python3
"""Exercise the review guard in isolated git repositories."""

from __future__ import annotations

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
        run(["git", "add", "README.md"], self.temp_dir)
        run(["git", "commit", "-m", "init"], self.temp_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def guard(self, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return run([sys.executable, str(GUARD)], self.temp_dir, env)

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
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        result = self.guard()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Native agent review required", result.stdout)
        self.assertIn("not a browser by default", result.stdout)
        self.assertIn("agent lifecycle", result.stdout)

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
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        evidence = self.temp_dir / ".agents/worklog/review/crit.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("review_surface: crit-web\nreviewer: user\nreview_outcome: approved\n")
        result = self.guard({"CRIT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CRIT_REVIEWED=1", result.stdout)

    def test_native_reviewed_environment_satisfies_required_review(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        evidence = self.temp_dir / ".agents/worklog/review/native.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("review_surface: codex-/review\nreviewer: user\nreview_outcome: addressed\n")
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("AGENT_REVIEWED=1", result.stdout)

    def test_native_reviewed_without_evidence_still_requires_review(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        result = self.guard({"AGENT_REVIEWED": "1"})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("REVIEW_EVIDENCE", result.stdout)

    def test_reviewed_with_incomplete_evidence_still_requires_review(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        evidence = self.temp_dir / ".agents/worklog/review/incomplete.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("review_surface: codex-/review\n")
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("reviewer", result.stdout)

    def test_reviewed_with_blank_evidence_values_still_requires_review(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        evidence = self.temp_dir / ".agents/worklog/review/blank.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("review_surface:\nreviewer: user\nreview_outcome: approved\n")
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("non-empty", result.stdout)

    def test_agent_self_reviewer_evidence_still_requires_review(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        evidence = self.temp_dir / ".agents/worklog/review/self.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("review_surface: codex-/review\nreviewer: codex\nreview_outcome: approved\n")
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("review_surface: crit-data", result.stdout)

    def test_agent_reviewer_with_crit_data_satisfies_required_review(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        crit_data = self.temp_dir / ".agents/worklog/review/crit-comments.json"
        crit_data.parent.mkdir(parents=True)
        crit_data.write_text("null\n")
        evidence = self.temp_dir / ".agents/worklog/review/agent-crit-data.md"
        evidence.write_text(
            "review_surface: crit-data\n"
            "reviewer: codex\n"
            "review_source: .agents/worklog/review/crit-comments.json\n"
            "review_outcome: approved\n"
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("AGENT_REVIEWED=1", result.stdout)

    def test_agent_reviewer_with_command_string_source_still_requires_review(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        evidence = self.temp_dir / ".agents/worklog/review/agent-command-source.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text(
            "review_surface: crit-data\n"
            "reviewer: codex\n"
            "review_source: crit comments --json\n"
            "review_outcome: approved\n"
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("JSON evidence file", result.stdout)

    def test_agent_reviewer_with_unresolved_crit_json_still_requires_review(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        crit_data = self.temp_dir / ".agents/worklog/review/crit-comments.json"
        crit_data.parent.mkdir(parents=True)
        crit_data.write_text('[{"id":"c_1","body":"fix this","resolved":false}]\n')
        evidence = self.temp_dir / ".agents/worklog/review/agent-unresolved.md"
        evidence.write_text(
            "review_surface: crit-data\n"
            "reviewer: claude-code\n"
            "review_source: .agents/worklog/review/crit-comments.json\n"
            "review_outcome: approved\n"
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("unresolved Crit comments", result.stdout)

    def test_agent_reviewer_with_external_crit_json_still_requires_review(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        external = Path(tempfile.mkdtemp(prefix="crit-external-")) / "comments.json"
        self.addCleanup(lambda: shutil.rmtree(external.parent, ignore_errors=True))
        external.write_text("null\n")
        evidence = self.temp_dir / ".agents/worklog/review/agent-external.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text(
            "review_surface: crit-data\n"
            "reviewer: codex\n"
            f"review_source: {external}\n"
            "review_outcome: approved\n"
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("repo-local", result.stdout)

    def test_agent_reviewer_with_crit_reviewed_marker_still_requires_review(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        crit_data = self.temp_dir / ".agents/worklog/review/crit-comments.json"
        crit_data.parent.mkdir(parents=True)
        crit_data.write_text("null\n")
        evidence = self.temp_dir / ".agents/worklog/review/agent-wrong-marker.md"
        evidence.write_text(
            "review_surface: crit-data\n"
            "reviewer: claude-code\n"
            "review_source: .agents/worklog/review/crit-comments.json\n"
            "review_outcome: approved\n"
        )
        result = self.guard({"CRIT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("AGENT_REVIEWED=1", result.stdout)

    def test_agent_self_review_flag_evidence_still_requires_review(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        evidence = self.temp_dir / ".agents/worklog/review/self-flag.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text(
            "review_surface: codex-/review\nreviewer: user\nreview_outcome: approved\nagent_self_review: true\n"
        )
        result = self.guard({"AGENT_REVIEWED": "1", "REVIEW_EVIDENCE": str(evidence)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("bare agent self-attestation", result.stdout)

    def test_explicit_disable_skips_guard(self) -> None:
        scripts_dir = self.temp_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "update-agent-assets.sh").write_text("#!/usr/bin/env bash\n")
        result = self.guard({"CRIT_REVIEW": "off"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CRIT_REVIEW=off", result.stdout)


if __name__ == "__main__":
    unittest.main()
