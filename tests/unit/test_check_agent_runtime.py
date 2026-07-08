#!/usr/bin/env python3
"""Exercise active agent runtime drift checks."""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts/check-agent-runtime.py"


class CheckAgentRuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="check-agent-runtime-test-"))
        self.source_root = self.temp_dir / "source"
        self.target_root = self.temp_dir / "target"
        self.source_root.mkdir()
        self.target_root.mkdir()
        spec = importlib.util.spec_from_file_location("check_agent_runtime", CHECKER)
        if spec is None or spec.loader is None:
            raise RuntimeError("unable to load check-agent-runtime.py")
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_source(self, rel: str, text: str = "content\n") -> Path:
        path = self.source_root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def write_target(self, rel: str, text: str = "content\n", *, executable: bool = False) -> Path:
        path = self.target_root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        if executable:
            path.chmod(0o755)
        return path

    def compare(self, *, warn_unmanaged_top_level: bool = False) -> list[str]:
        expected_sources = self.module.source_files(self.source_root)
        expected = {rel: path.read_text() for rel, path in expected_sources.items()}
        return self.module.compare_tree_contents("skills", expected, self.target_root, expected_sources, warn_unmanaged_top_level)

    def test_executable_prefix_is_compared_against_deployed_name(self) -> None:
        self.write_source("agmsg/scripts/executable_send.sh")
        self.write_target("agmsg/scripts/send.sh", executable=True)

        self.assertEqual(self.compare(), [])

    def test_executable_prefix_requires_deployed_execute_bit(self) -> None:
        self.write_source("agmsg/scripts/executable_send.sh")
        target = self.write_target("agmsg/scripts/send.sh")

        self.assertEqual(self.compare(), [f"skills is not executable: {target}"])

    def test_private_prefix_is_compared_against_deployed_name(self) -> None:
        self.write_source("workflow/private_config.json", '{"ok": true}\n')
        self.write_target("workflow/config.json", '{"ok": true}\n')

        self.assertEqual(self.compare(), [])

    def test_agmsg_runtime_paths_are_ignored_on_both_sides(self) -> None:
        self.write_source("agmsg/db/.keep")
        self.write_source("agmsg/run/.keep")
        self.write_source("agmsg/teams/.keep")
        self.write_source("agmsg/scripts/executable_send.sh")
        self.write_target("agmsg/.agmsg", "marker\n")
        self.write_target("agmsg/db/config.yaml", "runtime\n")
        self.write_target("agmsg/db/messages.db", "runtime\n")
        self.write_target("agmsg/run/.lastcheck-worker", "runtime\n")
        self.write_target("agmsg/teams/example/config.json", "runtime\n")
        self.write_target("agmsg/scripts/send.sh", executable=True)

        self.assertEqual(self.compare(), [])

    def test_unexpected_non_runtime_file_still_fails(self) -> None:
        self.write_source("agmsg/scripts/executable_send.sh")
        self.write_target("agmsg/scripts/send.sh", executable=True)
        self.write_target("agmsg/extra.txt")

        self.assertEqual(self.compare(), ["skills has unexpected files: agmsg/extra.txt"])

    def test_unmanaged_top_level_skill_dir_warns(self) -> None:
        self.write_source("agmsg/scripts/executable_send.sh")
        self.write_target("agmsg/scripts/send.sh", executable=True)
        self.write_target("crit/SKILL.md")

        self.assertEqual(self.compare(warn_unmanaged_top_level=True), [f"WARN: unmanaged skill dir: {self.target_root / 'crit'}"])

    def test_managed_top_level_extra_still_fails_with_unmanaged_warning_mode(self) -> None:
        self.write_source("agmsg/scripts/executable_send.sh")
        self.write_target("agmsg/scripts/send.sh", executable=True)
        self.write_target("agmsg/extra.txt")

        self.assertEqual(self.compare(warn_unmanaged_top_level=True), ["skills has unexpected files: agmsg/extra.txt"])

    def test_content_drift_still_fails(self) -> None:
        self.write_source("agmsg/scripts/executable_send.sh", "source\n")
        target = self.write_target("agmsg/scripts/send.sh", "target\n", executable=True)

        self.assertEqual(self.compare(), [f"skills differs: {target}"])


if __name__ == "__main__":
    unittest.main()
