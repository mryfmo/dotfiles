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

    def test_agmsg_separate_store_prefix_is_ignored(self) -> None:
        self.write_source("agmsg/scripts/executable_send.sh")
        self.write_target("agmsg/scripts/send.sh", executable=True)
        self.write_target("agmsg/db-flue-pi/messages.db", "runtime\n")

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

    def test_json_modifier_accepts_cosmetic_reserialization(self) -> None:
        source = self.write_source(
            "modify.py",
            "#!/usr/bin/env python3\n"
            "import json, sys\n"
            "json.dump(json.load(sys.stdin), sys.stdout, indent=2, sort_keys=True)\n",
        )
        source.chmod(0o755)
        target = self.write_target(
            "settings.json",
            '{"model":"managed","hooks":{"PreToolUse":[]}}\n',
        )

        self.assertTrue(self.module.same_modified(source, target, json_target=True))
        self.assertFalse(self.module.same_modified(source, target))

    def test_json_modifier_rejects_real_value_drift(self) -> None:
        source = self.write_source(
            "modify.py",
            "#!/usr/bin/env python3\n"
            "import json, sys\n"
            'data = json.load(sys.stdin); data["model"] = "managed"\n'
            "json.dump(data, sys.stdout, sort_keys=True)\n",
        )
        source.chmod(0o755)
        target = self.write_target("settings.json", '{"model":"runtime"}\n')

        self.assertFalse(self.module.same_modified(source, target, json_target=True))

    def test_check_uses_same_modified_for_codex_profiles(self) -> None:
        profile = self.write_source(
            "dot_codex/modify_standard.config.toml", "#!/usr/bin/env python3\n"
        )
        profile.chmod(0o755)
        original_source_root = self.module.SOURCE_ROOT
        original_home = self.module.HOME
        original_same_text = self.module.same_text
        original_same_modified = self.module.same_modified
        original_shared = self.module.compare_shared_skills
        original_claude = self.module.compare_claude_skills
        original_hook = self.module.check_executable_hook
        modified_sources: list[Path] = []
        try:
            self.module.SOURCE_ROOT = self.source_root
            self.module.HOME = self.target_root
            self.module.same_text = lambda *args, **kwargs: True
            self.module.same_modified = lambda source, *args, **kwargs: (
                modified_sources.append(source) or True
            )
            self.module.compare_shared_skills = lambda: []
            self.module.compare_claude_skills = lambda: []
            self.module.check_executable_hook = lambda *args, **kwargs: []

            self.module.check()
        finally:
            self.module.SOURCE_ROOT = original_source_root
            self.module.HOME = original_home
            self.module.same_text = original_same_text
            self.module.same_modified = original_same_modified
            self.module.compare_shared_skills = original_shared
            self.module.compare_claude_skills = original_claude
            self.module.check_executable_hook = original_hook

        self.assertIn(profile, modified_sources)


if __name__ == "__main__":
    unittest.main()
