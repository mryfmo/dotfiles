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
MERGE_SCRIPT = ROOT / "home/dot_omp/agent/modify_config.yml"
MANAGED = "# Generated fixture.\nmodelRoles:\n  default: anthropic/claude-managed\n"


class OmpConfigMergeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="omp-config-merge-test-")
        self.source_dir = Path(self.temp_dir.name)
        (self.source_dir / ".chezmoitemplates").mkdir()
        (self.source_dir / ".chezmoitemplates/omp-config-managed.yml").write_text(MANAGED)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def merge(self, current: str, pythonpath: Path | None = None) -> subprocess.CompletedProcess[str]:
        env = {**os.environ, "CHEZMOI_SOURCE_DIR": str(self.source_dir)}
        if pythonpath is not None:
            env["PYTHONPATH"] = str(pythonpath)
        return subprocess.run(
            [shutil.which("uv"), "run", "--no-project", "--with", "pyyaml", "python", str(MERGE_SCRIPT)],
            input=current,
            text=True,
            capture_output=True,
            env=env,
            check=True,
        )

    def test_sets_the_default_role_and_keeps_every_other_key_and_role(self) -> None:
        current = (
            "symbolPreset: nerd\n"
            "modelRoles:\n"
            "  default: anthropic/claude-old\n"
            "  smol: openai-codex/gpt-5.6-luna\n"
            "theme:\n"
            "  dark: night\n"
            "setupVersion: 3\n"
        )

        result = self.merge(current)

        self.assertEqual(result.stdout, current.replace("anthropic/claude-old", "anthropic/claude-managed"))
        self.assertEqual(result.stderr, "")

    def test_empty_input_yields_the_managed_mapping_only(self) -> None:
        self.assertEqual(self.merge("").stdout, "modelRoles:\n  default: anthropic/claude-managed\n")

    def test_input_that_is_not_a_yaml_mapping_passes_through_byte_for_byte(self) -> None:
        for current in ("modelRoles: [unclosed\n", "- a\n- b\n", "modelRoles: plain\n"):
            with self.subTest(current=current):
                result = self.merge(current)
                self.assertEqual(result.stdout, current)
                self.assertEqual(len(result.stderr.splitlines()), 1)

    def test_missing_pyyaml_passes_through_byte_for_byte(self) -> None:
        stub = self.source_dir / "stub"
        (stub / "yaml").mkdir(parents=True)
        (stub / "yaml/__init__.py").write_text('raise ImportError("stub without PyYAML")\n')
        current = "modelRoles:\n  default: anthropic/claude-old\n# a comment omp may not keep\n"

        result = self.merge(current, pythonpath=stub)

        self.assertEqual(result.stdout, current)
        self.assertIn("PyYAML", result.stderr)


if __name__ == "__main__":
    unittest.main()
