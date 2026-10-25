#!/usr/bin/env python3
"""Exercise the omp config modify script's merge and fail-closed paths."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.unit.test_omp_seat_policy import decide, load_policy

ROOT = Path(__file__).resolve().parents[2]
MERGE_SCRIPT = ROOT / "home/dot_omp/private_agent/modify_private_config.yml"
MANAGED = (
    "# Generated fixture.\n"
    "modelRoles:\n"
    "  default: anthropic/claude-managed\n"
    "skills:\n"
    "  customDirectories:\n"
    "    - ~/.agents/skills\n"
    "extensions:\n"
    "  - ~/.local/lib/omp-extensions/pi-claude-bridge\n"
    "  - /srv/omp-ext\n"
    "disabledProviders:\n"
    "  - agent-plugins\n"
    "  - openai-codex\n"
)
# The real home: uv (the script's runtime) needs it, so the test cannot fake $HOME.
HOME = os.path.expanduser("~")
MANAGED_SKILLS = f"skills:\n  customDirectories:\n  - {HOME}/.agents/skills\n"
MANAGED_EXTENSIONS = (
    f"extensions:\n- {HOME}/.local/lib/omp-extensions/pi-claude-bridge\n- /srv/omp-ext\n"
    "disabledProviders:\n- agent-plugins\n- openai-codex\n"
)


class OmpConfigMergeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="omp-config-merge-test-")
        self.source_dir = Path(self.temp_dir.name)
        (self.source_dir / ".chezmoitemplates").mkdir()
        (self.source_dir / ".chezmoitemplates/omp-config-managed.yml").write_text(MANAGED)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def merge(self, current: str, path: Path | None = None) -> subprocess.CompletedProcess[str]:
        env = {**os.environ, "CHEZMOI_SOURCE_DIR": str(self.source_dir)}
        if path is not None:
            env["PATH"] = str(path)
        return subprocess.run(
            ["/bin/sh", str(MERGE_SCRIPT)],
            input=current,
            text=True,
            capture_output=True,
            env=env,
            check=True,
        )

    def test_sets_the_managed_keys_and_keeps_every_other_key_and_role(self) -> None:
        current = (
            "symbolPreset: nerd\n"
            "modelRoles:\n"
            "  default: anthropic/claude-old\n"
            "  smol: openai-siwc/gpt-5.6-luna\n"
            "skills:\n"
            "  ignoredSkills:\n"
            "  - noisy\n"
            "  customDirectories:\n"
            "  - /old/skills\n"
            "theme:\n"
            "  dark: night\n"
            "extensions:\n"
            "- /old/ext\n"
            "- /other/ext\n"
            "disabledProviders:\n"
            "- mine\n"
            "setupVersion: 3\n"
        )

        result = self.merge(current)

        expected = current.replace("anthropic/claude-old", "anthropic/claude-managed")
        expected = expected.replace("/old/skills", f"{HOME}/.agents/skills")
        expected = expected.replace(
            "extensions:\n- /old/ext\n- /other/ext\ndisabledProviders:\n- mine\n", MANAGED_EXTENSIONS
        )
        self.assertEqual(result.stdout, expected)
        self.assertEqual(result.stderr, "")

    def test_extensions_are_added_after_the_keys_omp_wrote(self) -> None:
        result = self.merge("theme:\n  dark: night\nmodelRoles:\n  default: anthropic/claude-old\n")

        self.assertEqual(
            result.stdout,
            "theme:\n  dark: night\nmodelRoles:\n  default: anthropic/claude-managed\n"
            + MANAGED_SKILLS
            + MANAGED_EXTENSIONS,
        )

    def test_empty_input_yields_the_managed_mapping_only(self) -> None:
        self.assertEqual(
            self.merge("").stdout,
            "modelRoles:\n  default: anthropic/claude-managed\n" + MANAGED_SKILLS + MANAGED_EXTENSIONS,
        )

    def test_input_that_is_not_a_yaml_mapping_passes_through_byte_for_byte(self) -> None:
        for current in ("modelRoles: [unclosed\n", "- a\n- b\n", "modelRoles: plain\n", "skills: plain\n"):
            with self.subTest(current=current):
                result = self.merge(current)
                self.assertEqual(result.stdout, current)
                self.assertEqual(len(result.stderr.splitlines()), 1)

    def test_second_apply_is_a_no_op(self) -> None:
        first = self.merge("theme:\n  dark: night\nmodelRoles:\n  default: anthropic/claude-old\n").stdout

        self.assertEqual(self.merge(first).stdout, first)

    def test_missing_uv_passes_through_byte_for_byte(self) -> None:
        bin_dir = self.source_dir / "bin"
        bin_dir.mkdir()
        (bin_dir / "cat").symlink_to(shutil.which("cat"))
        current = "modelRoles:\n  default: anthropic/claude-old\n# a comment omp may not keep\n"

        result = self.merge(current, path=bin_dir)

        self.assertEqual(result.stdout, current)
        self.assertIn("uv", result.stderr)

    def test_the_managed_denies_join_omps_policy_and_the_approval_mode_is_kept(self) -> None:
        """U66 F043: a plain launch keeps its approval mode and every rule the operator wrote, and gains the managed
        tool and bash denies ahead of them, so a managed deny wins over a user allow for the same command."""
        policy = (
            "tools:\n  approval:\n    debug: deny\n    AskClaude: deny\n"
            'bash:\n  patterns:\n    - match: "*sudo *"\n      approval: deny\n'
            '    - match: "*rm -rf *"\n      approval: deny\n'
        )
        (self.source_dir / ".chezmoitemplates/omp-config-managed.yml").write_text(MANAGED + policy)
        current = (
            "tools:\n  approvalMode: yolo\n  approval:\n    read: allow\n    debug: allow\n    ast_edit: deny\n"
            "bash:\n  allowCompoundCommands: false\n  patterns:\n"
            "  - match: 'ssh *'\n    approval: deny\n"
            "  - match: 'sudo *'\n    approval: allow\n"
            "  - match: '*sudo *'\n    approval: deny\n"
            "  - match: '*'\n    approval: allow\n"
        )
        result = self.merge(current)
        merged = self.source_dir / "merged.yml"
        merged.write_text(result.stdout)
        data = load_policy(merged)
        self.assertEqual(
            data["tools"],
            {
                "approvalMode": "yolo",
                "approval": {"read": "allow", "debug": "deny", "ast_edit": "deny", "AskClaude": "deny"},
            },
        )
        self.assertFalse(data["bash"]["allowCompoundCommands"])
        self.assertEqual(
            data["bash"]["patterns"],
            [
                {"match": "*sudo *", "approval": "deny"},
                {"match": "*rm -rf *", "approval": "deny"},
                {"match": "ssh *", "approval": "deny"},
                {"match": "sudo *", "approval": "allow"},
                {"match": "*", "approval": "allow"},
            ],
        )
        for tool, command, expected in (
            ("bash", "sudo ls", "deny"),  # the managed deny wins over the user's `sudo *` allow
            ("bash", "ssh example.invalid", "deny"),  # the user's own deny stays
            ("bash", "cd /tmp && rm -rf build", "deny"),
            ("bash", "git status", "allow"),
            ("debug", None, "deny"),
            ("ast_edit", None, "deny"),  # the user's own tool deny stays
        ):
            with self.subTest(command=command or tool):
                self.assertEqual(decide(data, tool, command), expected)
        self.assertEqual(self.merge(result.stdout).stdout, result.stdout)
        self.assertNotIn("approvalMode", self.merge("theme:\n  dark: night\n").stdout)
        for current in ("tools: plain\n", "tools:\n  approval: [a]\n", "bash: [a]\n", "bash:\n  patterns: plain\n"):
            with self.subTest(current=current):
                passed = self.merge(current)
                self.assertEqual(passed.stdout, current)
                self.assertEqual(len(passed.stderr.splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
