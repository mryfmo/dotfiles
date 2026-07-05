#!/usr/bin/env python3
"""Exercise focused checks in generate-agent-configs.py."""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "scripts/generate-agent-configs.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_agent_configs", GENERATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GenerateAgentConfigsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_generator()
        self.old_root = self.module.ROOT
        self.temp_dir = Path(tempfile.mkdtemp(prefix="generate-agent-configs-test-"))
        self.module.ROOT = self.temp_dir

    def tearDown(self) -> None:
        self.module.ROOT = self.old_root
        shutil.rmtree(self.temp_dir)

    def test_claude_skill_symlink_outputs_strip_executable_target_prefix(self) -> None:
        source = self.temp_dir / "home/dot_agents/skills/agmsg/scripts/executable_send.sh"
        source.parent.mkdir(parents=True)
        source.write_text("#!/bin/sh\n")

        outputs = self.module.claude_skill_symlink_outputs()

        target = self.temp_dir / "home/dot_claude/skills/agmsg/scripts/symlink_send.sh.tmpl"
        self.assertEqual(
            outputs[target],
            "{{ .chezmoi.sourceDir }}/dot_agents/skills/agmsg/scripts/executable_send.sh\n",
        )
        self.assertNotIn(
            self.temp_dir / "home/dot_claude/skills/agmsg/scripts/symlink_executable_send.sh.tmpl",
            outputs,
        )


if __name__ == "__main__":
    unittest.main()
