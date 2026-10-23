#!/usr/bin/env python3
"""Exercise the omp config modify script's merge and fail-closed paths."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MERGE_SCRIPT = ROOT / "home/dot_omp/private_agent/modify_private_config.yml"
MANAGED = (
    "# Generated fixture.\n"
    "modelRoles:\n"
    "  default: anthropic/claude-managed\n"
    "skills:\n"
    "  customDirectories:\n"
    "    - ~/.agents/skills\n"
)
# The real home: uv (the script's runtime) needs it, so the test cannot fake $HOME.
HOME = os.path.expanduser("~")
MANAGED_SKILLS = f"skills:\n  customDirectories:\n  - {HOME}/.agents/skills\n"


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
            "  smol: openai-codex/gpt-5.6-luna\n"
            "skills:\n"
            "  ignoredSkills:\n"
            "  - noisy\n"
            "  customDirectories:\n"
            "  - /old/skills\n"
            "theme:\n"
            "  dark: night\n"
            "setupVersion: 3\n"
        )

        result = self.merge(current)

        expected = current.replace("anthropic/claude-old", "anthropic/claude-managed")
        self.assertEqual(result.stdout, expected.replace("/old/skills", f"{HOME}/.agents/skills"))
        self.assertEqual(result.stderr, "")

    def test_empty_input_yields_the_managed_mapping_only(self) -> None:
        self.assertEqual(self.merge("").stdout, "modelRoles:\n  default: anthropic/claude-managed\n" + MANAGED_SKILLS)

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


if __name__ == "__main__":
    unittest.main()
