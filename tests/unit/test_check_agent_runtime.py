#!/usr/bin/env python3
"""Exercise active agent runtime drift checks."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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
        return self.module.compare_tree_contents(
            "skills",
            expected,
            self.target_root,
            expected_sources,
            warn_unmanaged_top_level,
        )

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

    def test_only_exact_agmsg_root_legacy_database_names_are_ignored(self) -> None:
        self.write_source("agmsg/scripts/executable_send.sh")
        self.write_target("agmsg/scripts/send.sh", executable=True)
        for name in ("messages.db", "messages.db-wal", "messages.db-shm"):
            self.write_target(f"agmsg/{name}", "runtime\n")

        self.assertEqual(self.compare(), [])

        self.write_target("agmsg/messages.db.backup", "unexpected\n")

        self.assertEqual(
            self.compare(),
            ["skills has unexpected files: agmsg/messages.db.backup"],
        )

    def test_unexpected_non_runtime_file_still_fails(self) -> None:
        self.write_source("agmsg/scripts/executable_send.sh")
        self.write_target("agmsg/scripts/send.sh", executable=True)
        self.write_target("agmsg/extra.txt")

        self.assertEqual(self.compare(), ["skills has unexpected files: agmsg/extra.txt"])

    def test_unmanaged_top_level_skill_dir_warns(self) -> None:
        self.write_source("agmsg/scripts/executable_send.sh")
        self.write_target("agmsg/scripts/send.sh", executable=True)
        self.write_target("crit/SKILL.md")

        self.assertEqual(
            self.compare(warn_unmanaged_top_level=True),
            [f"WARN: unmanaged skill dir: {self.target_root / 'crit'}"],
        )

    def test_managed_top_level_extra_still_fails_with_unmanaged_warning_mode(
        self,
    ) -> None:
        self.write_source("agmsg/scripts/executable_send.sh")
        self.write_target("agmsg/scripts/send.sh", executable=True)
        self.write_target("agmsg/extra.txt")

        self.assertEqual(
            self.compare(warn_unmanaged_top_level=True),
            ["skills has unexpected files: agmsg/extra.txt"],
        )

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
            "dot_codex/modify_private_standard.config.toml",
            "#!/usr/bin/env python3\n",
        )
        profile.chmod(0o755)
        original_source_root = self.module.SOURCE_ROOT
        original_home = self.module.HOME
        original_same_text = self.module.same_text
        original_same_modified = self.module.same_modified
        original_shared = self.module.compare_shared_skills
        original_claude = self.module.compare_claude_skills
        original_hook = self.module.check_executable_hook
        original_drift = self.module.chezmoi_drift_warnings
        modified_sources: list[Path] = []
        try:
            self.module.SOURCE_ROOT = self.source_root
            self.module.HOME = self.target_root
            self.module.same_text = lambda *args, **kwargs: True
            self.module.same_modified = lambda source, *args, **kwargs: modified_sources.append(source) or True
            self.module.compare_shared_skills = list
            self.module.compare_claude_skills = list
            self.module.check_executable_hook = lambda *args, **kwargs: []
            self.module.chezmoi_drift_warnings = list

            self.module.check()
        finally:
            self.module.SOURCE_ROOT = original_source_root
            self.module.HOME = original_home
            self.module.same_text = original_same_text
            self.module.same_modified = original_same_modified
            self.module.compare_shared_skills = original_shared
            self.module.compare_claude_skills = original_claude
            self.module.check_executable_hook = original_hook
            self.module.chezmoi_drift_warnings = original_drift

        self.assertIn(profile, modified_sources)

    def test_chezmoi_drift_warnings_classify_status_and_mode_only(self) -> None:
        status = mock.Mock(
            returncode=0,
            stdout=(" M .agents/agent-config.yaml\nMM .zshrc\nMM .codex/deep.config.toml\n"),
            stderr="",
        )
        content_diff = mock.Mock(
            returncode=0,
            stdout="diff --git a/.zshrc b/.zshrc\n@@ -1 +1 @@\n-old\n+new\n",
            stderr="",
        )
        mode_diff = mock.Mock(
            returncode=0,
            stdout=(
                "diff --git a/.codex/deep.config.toml b/.codex/deep.config.toml\nold mode 100600\nnew mode 100644\n"
            ),
            stderr="",
        )

        with mock.patch.object(
            self.module.subprocess,
            "run",
            side_effect=[status, content_diff, content_diff, mode_diff],
        ):
            warnings = self.module.chezmoi_drift_warnings()

        self.assertEqual(
            [
                "WARN: chezmoi drift  M .agents/agent-config.yaml: unapplied source update",
                "WARN: chezmoi drift MM .zshrc: two-sided drift",
                "WARN: chezmoi drift MM .codex/deep.config.toml: permission divergence (mode-only)",
            ],
            warnings,
        )

    def test_chezmoi_drift_status_failure_is_warning(self) -> None:
        result = mock.Mock(returncode=1, stdout="", stderr="status failed\n")

        with mock.patch.object(self.module.subprocess, "run", return_value=result):
            warnings = self.module.chezmoi_drift_warnings()

        self.assertEqual(["WARN: unable to inspect chezmoi drift: status failed"], warnings)

    def test_orphan_detection_classifies_accounted_stale_and_orphan(self) -> None:
        home = self.temp_dir / "home"
        source = self.temp_dir / "repo-source"
        agents = home / ".agents"
        skills = agents / "skills"
        (source / "dot_agents/skills/managed").mkdir(parents=True)
        (source / "dot_agents/plugins/managed").mkdir(parents=True)
        for path in (
            skills / "managed",
            skills / "understand-chat",
            skills / "stale-skill",
            skills / "orphan-skill",
            agents / "plugins",
            agents / "compactiondb",
            agents / "stale-root",
            agents / "orphan-root",
        ):
            path.mkdir(parents=True)
        manifest = {
            "version": 1,
            "steps": {
                "install_stale_skill": {"paths": [str(skills / "stale-skill/payload")]},
                "ensure_mise_npm_agent_cli:claude": {"paths": [str(agents / "stale-root")]},
            },
        }
        (agents / ".installed-manifest.json").write_text(json.dumps(manifest))

        warnings = self.module.orphaned_asset_warnings(home, source)

        self.assertEqual(
            [
                f"WARN: orphaned agent asset: {agents / 'orphan-root'}; manual review required",
                f"WARN: stale agent asset: {agents / 'stale-root'}; suggested: remove-agent-asset ensure_mise_npm_agent_cli:claude",
                f"WARN: orphaned agent asset: {skills / 'orphan-skill'}; manual review required",
                f"WARN: stale agent asset: {skills / 'stale-skill'}; suggested: remove-agent-asset install_stale_skill",
            ],
            warnings,
        )
        joined = "\n".join(warnings)
        for accounted in (
            skills / "managed",
            skills / "understand-chat",
            agents / "plugins",
            agents / "compactiondb",
        ):
            self.assertNotIn(str(accounted), joined)

    def test_installer_owned_agmsg_skill_and_backups_are_not_orphans(self) -> None:
        home = self.temp_dir / "home"
        source = self.temp_dir / "repo-source"
        agents = home / ".agents"
        skills = agents / "skills"
        (source / "dot_agents/skills/managed").mkdir(parents=True)
        for path in (
            skills / "agmsg/scripts",
            agents / "backups/agmsg-state-20260929T000000Z/teams",
            agents / "orphan-root",
        ):
            path.mkdir(parents=True)
        manifest = {
            "version": 1,
            "steps": {"update_agmsg": {"paths": [str(skills / "agmsg/SKILL.md"), str(skills / "agmsg/scripts")]}},
        }
        (agents / ".installed-manifest.json").write_text(json.dumps(manifest))

        warnings = self.module.orphaned_asset_warnings(home, source)

        self.assertEqual(
            [f"WARN: orphaned agent asset: {agents / 'orphan-root'}; manual review required"],
            warnings,
        )

    def test_terminal_browser_receipt_links_are_not_orphans(self) -> None:
        home = self.temp_dir / "home"
        source = self.temp_dir / "repo-source"
        skills = home / ".agents/skills"
        (source / "dot_agents/skills/managed").mkdir(parents=True)
        (skills / "terminal-browser").mkdir(parents=True)
        (skills / "unlisted-skill").mkdir(parents=True)
        receipt = home / ".local/state/terminal-browser/skills.links"
        receipt.parent.mkdir(parents=True)
        receipt.write_text(f"{skills / 'terminal-browser'}\n")

        warnings = self.module.orphaned_asset_warnings(home, source)

        self.assertEqual(
            [
                f"WARN: orphaned agent asset: {skills / 'unlisted-skill'}; manual review required",
            ],
            warnings,
        )

    def test_crit_codex_skills_are_not_orphans(self) -> None:
        home = self.temp_dir / "home"
        source = self.temp_dir / "repo-source"
        skills = home / ".agents/skills"
        (source / "dot_agents/skills/managed").mkdir(parents=True)
        for name in ("crit", "crit-cli", "crit-story", "unlisted-skill"):
            (skills / name).mkdir(parents=True)

        warnings = self.module.orphaned_asset_warnings(home, source)

        self.assertEqual(
            [f"WARN: orphaned agent asset: {skills / 'unlisted-skill'}; manual review required"],
            warnings,
        )

    def test_missing_terminal_browser_receipt_is_harmless(self) -> None:
        self.assertEqual(
            set(),
            self.module.terminal_browser_receipt_paths(self.temp_dir / "no-home"),
        )

    def test_ignored_paths_suppress_receipt_linked_tree_entries(self) -> None:
        self.write_source("agmsg/scripts/executable_send.sh")
        self.write_target("agmsg/scripts/send.sh", executable=True)
        self.write_target("terminal-browser/SKILL.md")

        expected_sources = self.module.source_files(self.source_root)
        expected = {rel: path.read_text() for rel, path in expected_sources.items()}
        ignored = {self.module.normalized_path(self.target_root / "terminal-browser")}

        with_ignore = self.module.compare_tree_contents(
            "skills",
            expected,
            self.target_root,
            expected_sources,
            ignored_paths=ignored,
        )
        without_ignore = self.module.compare_tree_contents("skills", expected, self.target_root, expected_sources)

        self.assertEqual([], with_ignore)
        self.assertEqual(["skills has unexpected files: terminal-browser/SKILL.md"], without_ignore)

    def test_compare_claude_skills_ignores_cowork_synced_subtree(self) -> None:
        (self.source_root / "dot_claude/skills").mkdir(parents=True)
        synced = self.target_root / ".claude/skills/synced/some-cowork-skill"
        synced.mkdir(parents=True)
        (synced / "SKILL.md").write_text("content\n")
        original_source_root = self.module.SOURCE_ROOT
        original_home = self.module.HOME
        try:
            self.module.SOURCE_ROOT = self.source_root
            self.module.HOME = self.target_root

            self.assertEqual([], self.module.compare_claude_skills())
        finally:
            self.module.SOURCE_ROOT = original_source_root
            self.module.HOME = original_home

    def test_repair_actions_map_only_detected_file_drift(self) -> None:
        missing = self.target_root / "missing.json"
        different = self.write_target("different.json", "runtime\n")
        executable = self.write_target("hook.sh", "#!/bin/sh\n")
        failures = [
            f"Claude MCP config differs or is missing: {missing}",
            f"shared skill directory differs: {different}",
            f"Claude enforce-uv hook is not executable: {executable}",
            "Claude shared-skill symlink tree is missing: ~/.claude/skills",
            f"WARN: orphaned agent asset: {self.target_root / 'orphan'}; manual review required",
        ]

        actions = self.module.repair_actions(failures, self.target_root)

        self.assertEqual(
            [
                self.module.RepairAction(
                    "missing file",
                    missing,
                    ("chezmoi", "apply", "--force", str(missing)),
                ),
                self.module.RepairAction(
                    "content differs",
                    different,
                    ("chezmoi", "apply", "--force", str(different)),
                ),
                self.module.RepairAction(
                    "executable bit missing",
                    executable,
                    ("chmod", "+x", str(executable)),
                ),
                self.module.RepairAction(
                    "missing file",
                    self.target_root / ".claude/skills",
                    (
                        "chezmoi",
                        "apply",
                        "--force",
                        str(self.target_root / ".claude/skills"),
                    ),
                ),
            ],
            actions,
        )

    def test_execute_repair_calls_each_mapped_command_once(self) -> None:
        actions = [
            self.module.RepairAction(
                "missing file",
                self.target_root / "missing",
                (
                    "chezmoi",
                    "apply",
                    "--force",
                    str(self.target_root / "missing"),
                ),
            ),
            self.module.RepairAction(
                "executable bit missing",
                self.target_root / "hook.sh",
                ("chmod", "+x", str(self.target_root / "hook.sh")),
            ),
            self.module.RepairAction(
                "asset step missing",
                self.target_root / "asset",
                ("bash", "update-one-step"),
            ),
        ]

        with mock.patch.object(
            self.module.subprocess,
            "run",
            return_value=mock.Mock(returncode=0),
        ) as run:
            results = [self.module.execute_repair(action) for action in actions]

        self.assertEqual([True, True, True], results)
        self.assertEqual(
            [mock.call(action.command, check=False) for action in actions],
            run.call_args_list,
        )

    def test_every_generated_chezmoi_repair_action_is_forced(self) -> None:
        missing = self.target_root / "missing.json"
        different = self.write_target("different.json", "runtime\n")
        failures = [
            f"Claude MCP config differs or is missing: {missing}",
            f"shared skill directory differs: {different}",
            "shared skill directory is missing files: agmsg/scripts/history.sh",
            "Claude shared-skill symlink tree is missing: ~/.claude/skills",
        ]

        commands = [
            action.command
            for action in self.module.repair_actions(failures, self.target_root)
            if action.command[0] == "chezmoi"
        ]

        self.assertEqual(4, len(commands))
        self.assertTrue(all(command[:3] == ("chezmoi", "apply", "--force") for command in commands))

    def test_deleted_shared_skill_file_repair_converges(self) -> None:
        source_root = self.temp_dir / "repo/home"
        source = source_root / "dot_agents/skills/agmsg/scripts/executable_history.sh"
        source.parent.mkdir(parents=True)
        source.write_text("#!/usr/bin/env bash\n")
        source.chmod(0o755)
        home = self.temp_dir / "home"
        (home / ".agents/skills").mkdir(parents=True)
        target = home / ".agents/skills/agmsg/scripts/history.sh"
        actions: list[object] = []

        def execute(action) -> bool:
            actions.append(action)
            self.assertEqual(("chezmoi", "apply", "--force", str(target)), action.command)
            target.parent.mkdir(parents=True)
            shutil.copy2(source, target)
            return True

        with (
            mock.patch.object(self.module, "SOURCE_ROOT", source_root),
            mock.patch.object(self.module, "HOME", home),
            mock.patch.object(
                self.module,
                "check",
                side_effect=lambda: self.module.compare_shared_skills(),
            ),
            mock.patch.object(self.module, "execute_repair", side_effect=execute),
            mock.patch.dict(os.environ, {"REPAIR": "1"}),
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            result = self.module.main([])

        self.assertEqual(0, result)
        self.assertEqual(1, len(actions))
        self.assertEqual(
            [],
            self.module.compare_tree_contents(
                "shared skill directory",
                {Path("agmsg/scripts/history.sh"): source.read_text()},
                home / ".agents/skills",
                {Path("agmsg/scripts/history.sh"): source},
                warn_unmanaged_top_level=True,
            ),
        )

    def test_manifest_drift_requires_recorded_step_with_missing_path(self) -> None:
        home = self.temp_dir / "home"
        agents = home / ".agents"
        present = agents / "present"
        missing = agents / "missing"
        present.mkdir(parents=True)
        manifest = {
            "version": 1,
            "steps": {
                "update_compactiondb": {
                    "kind": "rsync",
                    "paths": [str(missing)],
                    "commands": ["rsync recorded"],
                    "source_version": "same-or-different-is-ignored",
                },
                "update_codex_superpowers": {
                    "kind": "plugin",
                    "paths": [str(present)],
                    "commands": ["codex plugin add superpowers@openai-curated"],
                    "source_version": "old-version-is-not-repair-drift",
                },
            },
        }
        (agents / ".installed-manifest.json").write_text(json.dumps(manifest))

        findings = self.module.manifest_asset_findings(home)

        self.assertEqual(1, len(findings))
        self.assertEqual("update_compactiondb", findings[0].step)
        self.assertEqual((missing,), findings[0].missing_paths)
        self.assertNotIn("update_claude_crit", {item.step for item in findings})

    def test_asset_repair_invokes_only_the_detected_step(self) -> None:
        home = self.temp_dir / "home"
        updater = self.temp_dir / "update-agent-assets.sh"
        updater.write_text("# test updater\n")
        missing = home / ".agents/compactiondb"
        action = self.module.asset_repair_action(
            self.module.AssetFinding(
                "update_compactiondb",
                (missing,),
                {"commands": ["rsync recorded"]},
            ),
            updater,
        )

        self.assertEqual("asset step missing", action.category)
        self.assertEqual(missing, action.target)
        self.assertEqual(
            (
                "bash",
                "-c",
                'source "$1"; export PATH="$HOME/.local/share/mise/shims:$PATH"; shift; "$@"',
                "bash",
                str(updater),
                "update_compactiondb",
            ),
            action.command,
        )

    def test_missing_crit_asset_is_repairable(self) -> None:
        missing = self.target_root / ".local/bin/crit"

        action = self.module.asset_repair_action(
            self.module.AssetFinding(
                "ensure_crit_cli",
                (missing,),
                {"commands": ["install pinned crit"]},
            )
        )

        self.assertEqual("ensure_crit_cli", action.command[-1])

    def test_sourced_asset_repair_runs_no_main_or_sibling_step(self) -> None:
        updater = self.temp_dir / "strict-update-agent-assets.sh"
        log = self.temp_dir / "steps.log"
        updater.write_text(
            "#!/usr/bin/env bash\n"
            "set -Eeuo pipefail\n"
            "function update_compactiondb() { printf 'selected\\n' >> \"$TEST_LOG\"; }\n"
            "function update_codex_crit() { printf 'sibling\\n' >> \"$TEST_LOG\"; }\n"
            "function main() { printf 'main\\n' >> \"$TEST_LOG\"; }\n"
            'if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then main "$@"; fi\n'
        )
        action = self.module.asset_repair_action(
            self.module.AssetFinding(
                "update_compactiondb",
                (self.target_root / "missing",),
                {"commands": ["rsync recorded"]},
            ),
            updater,
        )

        with mock.patch.dict(os.environ, {"TEST_LOG": str(log)}):
            result = self.module.execute_repair(action)

        self.assertTrue(result)
        self.assertEqual("selected\n", log.read_text())

    def test_parameterized_mise_step_uses_key_identity(self) -> None:
        missing = self.target_root / "missing-cli"
        claude = self.module.AssetFinding(
            "ensure_mise_npm_agent_cli:claude",
            (missing,),
            {"commands": []},
        )
        ambiguous = self.module.AssetFinding(
            "ensure_mise_npm_agent_cli:unknown",
            (missing,),
            {
                "commands": [
                    "mise install --force npm:@anthropic-ai/claude-code",
                    "mise install --force npm:@openai/codex",
                ]
            },
        )

        action = self.module.asset_repair_action(claude)

        self.assertEqual(
            ("ensure_mise_npm_agent_cli", "claude", "npm:@anthropic-ai/claude-code"),
            action.command[-3:],
        )
        self.assertIsNone(self.module.asset_repair_action(ambiguous))

    def test_installed_manifest_integrity_reasons(self) -> None:
        missing = self.temp_dir / "missing-manifest.json"
        self.assertIsNone(self.module.installed_manifest_error(missing))

        cases = {
            "root": ([], "root must be an object"),
            "version": ({"version": 2, "steps": {}}, "version must be 1"),
            "steps": ({"version": 1, "steps": []}, "steps must be an object"),
        }
        for name, (manifest, expected) in cases.items():
            with self.subTest(name=name):
                manifest_path = self.temp_dir / f"{name}-manifest.json"
                manifest_path.write_text(json.dumps(manifest))
                self.assertEqual(expected, self.module.installed_manifest_error(manifest_path))

        unreadable = self.temp_dir / "directory-manifest.json"
        unreadable.mkdir()
        self.assertRegex(self.module.installed_manifest_error(unreadable), r"^unreadable: ")

    def test_invalid_manifest_is_one_error_and_skips_dependent_checks(self) -> None:
        agents = self.target_root / ".agents"
        agents.mkdir()
        manifest_path = agents / ".installed-manifest.json"
        manifest_path.write_text("{truncated")
        original_home = self.module.HOME
        original_same_text = self.module.same_text
        original_same_modified = self.module.same_modified
        original_shared = self.module.compare_shared_skills
        original_claude = self.module.compare_claude_skills
        original_hook = self.module.check_executable_hook
        original_findings = self.module.manifest_asset_findings
        original_orphans = self.module.orphaned_asset_warnings
        original_drift = self.module.chezmoi_drift_warnings
        original_gh_login = self.module.gh_login_findings
        try:
            self.module.HOME = self.target_root
            self.module.same_text = lambda *args, **kwargs: True
            self.module.same_modified = lambda *args, **kwargs: True
            self.module.compare_shared_skills = list
            self.module.compare_claude_skills = list
            self.module.check_executable_hook = lambda *args, **kwargs: []
            self.module.manifest_asset_findings = lambda *args, **kwargs: self.fail("manifest findings must be skipped")
            self.module.orphaned_asset_warnings = lambda *args, **kwargs: self.fail(
                "manifest orphan checks must be skipped"
            )
            self.module.chezmoi_drift_warnings = list
            self.module.gh_login_findings = list

            failures = self.module.check()
        finally:
            self.module.HOME = original_home
            self.module.same_text = original_same_text
            self.module.same_modified = original_same_modified
            self.module.compare_shared_skills = original_shared
            self.module.compare_claude_skills = original_claude
            self.module.check_executable_hook = original_hook
            self.module.manifest_asset_findings = original_findings
            self.module.orphaned_asset_warnings = original_orphans
            self.module.chezmoi_drift_warnings = original_drift
            self.module.gh_login_findings = original_gh_login

        self.assertEqual(1, len(failures))
        self.assertRegex(
            failures[0],
            rf"^installed manifest unreadable or invalid: {manifest_path} \(invalid JSON:",
        )

    def test_repair_mode_converges_once_and_reports_each_action(self) -> None:
        target = self.target_root / "missing.json"
        initial = [f"Claude MCP config differs or is missing: {target}"]
        scans = iter((initial, []))
        calls: list[object] = []
        action = self.module.RepairAction("missing file", target, ("chezmoi", "apply", "--force", str(target)))
        original_check = self.module.check
        original_actions = self.module.repair_actions
        original_execute = self.module.execute_repair
        try:
            self.module.check = lambda: next(scans)
            self.module.repair_actions = lambda failures, home=None: [action] if failures else []
            self.module.execute_repair = lambda candidate: calls.append(candidate) or True
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                with mock.patch.dict(os.environ, {"REPAIR": "1"}):
                    result = self.module.main([])
        finally:
            self.module.check = original_check
            self.module.repair_actions = original_actions
            self.module.execute_repair = original_execute

        self.assertEqual(0, result, stderr.getvalue())
        self.assertEqual([action], calls)
        self.assertEqual(
            f"ERROR: {initial[0]}\n"
            f"repaired: missing file {target} (chezmoi apply --force {target})\n"
            "active agent runtime files match this chezmoi source tree\n",
            stderr.getvalue() + stdout.getvalue(),
        )

    def test_repair_mode_fails_after_one_non_convergent_round(self) -> None:
        target = self.target_root / "missing.json"
        failure = f"Claude MCP config differs or is missing: {target}"
        scan_count = 0
        action = self.module.RepairAction("missing file", target, ("chezmoi", "apply", "--force", str(target)))

        def scan() -> list[str]:
            nonlocal scan_count
            scan_count += 1
            return [failure]

        original_check = self.module.check
        original_actions = self.module.repair_actions
        original_execute = self.module.execute_repair
        try:
            self.module.check = scan
            self.module.repair_actions = lambda failures, home=None: [action]
            self.module.execute_repair = lambda candidate: True
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                with mock.patch.dict(os.environ, {"REPAIR": "1"}):
                    result = self.module.main([])
        finally:
            self.module.check = original_check
            self.module.repair_actions = original_actions
            self.module.execute_repair = original_execute

        self.assertEqual(1, result)
        self.assertEqual(2, scan_count)
        self.assertIn("non-convergent after repair", stderr.getvalue())

    def test_repair_unset_is_byte_identical_and_never_mutates(self) -> None:
        warning = "WARN: orphaned agent asset: /tmp/orphan; manual review required"
        failure = "Claude MCP config differs or is missing: /tmp/mcp.json"
        original_check = self.module.check
        original_execute = self.module.execute_repair
        try:
            self.module.check = lambda: [warning, failure]
            self.module.execute_repair = lambda action: self.fail(f"unexpected repair: {action}")
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                with mock.patch.dict(os.environ, {}, clear=False):
                    os.environ.pop("REPAIR", None)
                    result = self.module.main([])
        finally:
            self.module.check = original_check
            self.module.execute_repair = original_execute

        self.assertEqual(1, result)
        self.assertEqual(f"{warning}\n", stdout.getvalue())
        self.assertEqual(f"ERROR: {failure}\n", stderr.getvalue())

    def test_repair_mode_never_acts_on_stale_or_orphan_warnings(self) -> None:
        warnings = [
            "WARN: stale agent asset: /tmp/stale; suggested: remove-agent-asset recorded",
            "WARN: orphaned agent asset: /tmp/orphan; manual review required",
        ]
        original_check = self.module.check
        original_execute = self.module.execute_repair
        try:
            self.module.check = lambda: warnings
            self.module.execute_repair = lambda action: self.fail(f"unexpected repair: {action}")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                with mock.patch.dict(os.environ, {"REPAIR": "1"}):
                    result = self.module.main([])
        finally:
            self.module.check = original_check
            self.module.execute_repair = original_execute

        self.assertEqual(0, result)
        self.assertEqual(
            "\n".join(warnings) + "\nactive agent runtime files match this chezmoi source tree\n",
            stdout.getvalue(),
        )

    def ua_core_tree(self) -> Path:
        core = self.target_root / ".understand-anything/repo/understand-anything-plugin/packages/core"
        (core / "src").mkdir(parents=True)
        (core / "src/index.ts").write_text("export {};\n")
        return core

    def test_ua_core_warns_when_the_codex_clone_has_no_built_dist(self) -> None:
        core = self.ua_core_tree()

        warnings = self.module.understand_anything_core_warnings(self.target_root)

        self.assertEqual(
            [f"WARN: Understand-Anything core not built: {core / 'dist/index.js'} is missing; run make update"],
            warnings,
        )
        self.assertTrue(all(self.module.is_warning(warning) for warning in warnings))

    def test_ua_core_warns_when_dist_is_older_than_src(self) -> None:
        core = self.ua_core_tree()
        (core / "dist").mkdir()
        (core / "dist/index.js").write_text("built\n")
        os.utime(core / "dist/index.js", (1_000_000, 1_000_000))
        os.utime(core / "src/index.ts", (2_000_000, 2_000_000))

        warnings = self.module.understand_anything_core_warnings(self.target_root)

        self.assertEqual(
            [
                f"WARN: Understand-Anything core build is stale: {core / 'dist/index.js'} "
                f"is older than {core / 'src'} or {core.parents[1] / 'pnpm-lock.yaml'}; run make update"
            ],
            warnings,
        )

    def test_ua_core_warns_when_dist_is_older_than_the_root_lockfile(self) -> None:
        core = self.ua_core_tree()
        (core / "dist").mkdir()
        (core / "dist/index.js").write_text("built\n")
        lockfile = core.parents[1] / "pnpm-lock.yaml"
        lockfile.write_text("lockfileVersion: '9.0'\n")
        os.utime(core / "src/index.ts", (1_000_000, 1_000_000))
        os.utime(core / "dist/index.js", (2_000_000, 2_000_000))
        os.utime(lockfile, (3_000_000, 3_000_000))

        warnings = self.module.understand_anything_core_warnings(self.target_root)

        self.assertEqual(
            [
                f"WARN: Understand-Anything core build is stale: {core / 'dist/index.js'} "
                f"is older than {core / 'src'} or {lockfile}; run make update"
            ],
            warnings,
        )

    def test_ua_core_is_quiet_when_dist_is_fresh_or_no_clone_exists(self) -> None:
        self.assertEqual([], self.module.understand_anything_core_warnings(self.target_root))
        core = self.ua_core_tree()
        (core / "dist").mkdir()
        (core / "dist/index.js").write_text("built\n")
        os.utime(core / "src/index.ts", (1_000_000, 1_000_000))
        os.utime(core / "dist/index.js", (2_000_000, 2_000_000))

        self.assertEqual([], self.module.understand_anything_core_warnings(self.target_root))

    def test_check_includes_ua_core_warnings(self) -> None:
        with (
            mock.patch.object(
                self.module, "understand_anything_core_warnings", return_value=["WARN: ua-core sentinel"]
            ),
            mock.patch.object(self.module, "chezmoi_drift_warnings", return_value=[]),
            mock.patch.object(self.module, "orchestrator_seat_lock_warnings", return_value=[]),
        ):
            self.assertIn("WARN: ua-core sentinel", self.module.check())

    def seat_lock_fixture(self, owner: str, *, live: bool = True) -> tuple[Path, Path, Path]:
        project = self.temp_dir / "project"
        project.mkdir()
        skill_dir = self.temp_dir / "agmsg"
        (skill_dir / "scripts").mkdir(parents=True)
        identities = skill_dir / "scripts/identities.sh"
        identities.write_text(
            "#!/bin/sh\nprintf 'dotfiles\\tclaude-remediation-dot\\ndotfiles\\tclaude-standard-dot-a005\\n'\n"
        )
        identities.chmod(0o755)
        (skill_dir / "run").mkdir()
        (skill_dir / "run/actas.dotfiles__claude-remediation-dot.session").write_text(owner + "\n")
        (skill_dir / "run/actas.dotfiles__claude-standard-dot-a005.session").write_text("worker-bare\n")
        proc = self.temp_dir / "proc"
        (proc / "4242").mkdir(parents=True)
        (proc / "4242/comm").write_text("claude\n" if live else "bash\n")
        (proc / "4242/cwd").symlink_to(project)
        return project, skill_dir, proc

    def fake_gh_status(self, accounts: list[dict]) -> str:
        """A fake gh whose `auth status --json hosts` reports ACCOUNTS; it fails if a token variable leaks."""
        status = self.temp_dir / "status.json"
        status.write_text(json.dumps({"hosts": {"github.com": accounts}}))
        gh = self.temp_dir / "gh"
        gh.write_text(
            "#!/bin/sh\n"
            '[ -z "${GH_TOKEN-}${GITHUB_TOKEN-}" ] || { echo "token env leaked" >&2; exit 3; }\n'
            '[ "$*" = "auth status --hostname github.com --json hosts" ] || exit 2\n'
            f"cat {status}\n"
        )
        gh.chmod(0o755)
        return str(gh)

    def gh_hosts_file(self, mode: int = 0o600) -> str:
        hosts = self.temp_dir / "gh-config/hosts.yml"
        hosts.parent.mkdir(exist_ok=True)
        hosts.touch()
        hosts.chmod(mode)
        return str(hosts)

    def test_gh_login_reports_the_one_working_login(self) -> None:
        gh = self.fake_gh_status(
            [{"login": "machine-login", "state": "success", "active": True, "tokenSource": self.gh_hosts_file()}]
        )

        with mock.patch.dict(os.environ, {"GH_TOKEN": "fixture-env-token"}):
            findings = self.module.gh_login_findings(gh=gh, config_dir=self.temp_dir / "gh-config")

        self.assertEqual(findings, ["found: GitHub login machine-login (every seat on this machine acts as it)"])
        # A present login is a report line, not a failure: no repair, no non-zero exit.
        self.assertTrue(self.module.is_info(findings[0]))
        self.assertEqual(self.module.repair_actions(findings, home=self.temp_dir), [])

    def test_gh_login_warns_on_two_logins_none_working_or_no_gh(self) -> None:
        cases = (
            (
                [{"login": "machine-login", "state": "success"}, {"login": "stray-login", "state": "success"}],
                "gh holds 2 working of 2 logins",
            ),
            # A file token that no longer works (revoked).
            (
                [{"login": "machine-login", "state": "error", "tokenSource": self.gh_hosts_file()}],
                "gh holds 0 working of 1 logins",
            ),
            ([], "gh holds 0 working of 0 logins"),
        )
        for accounts, expected in cases:
            with self.subTest(expected=expected):
                findings = self.module.gh_login_findings(
                    gh=self.fake_gh_status(accounts), config_dir=self.temp_dir / "gh-config"
                )
                self.assertEqual(len(findings), 1)
                self.assertTrue(self.module.is_warning(findings[0]))
                self.assertIn(expected, findings[0])
                self.assertTrue(findings[0].endswith("or run make gh-auth)"))
        missing = self.module.gh_login_findings(
            gh=str(self.temp_dir / "absent-gh"), config_dir=self.temp_dir / "gh-config"
        )
        self.assertEqual(missing, ["WARN: GitHub login: gh auth status failed or gh is missing; run make gh-auth"])

    KEYRING_WARNING = (
        "WARN: GitHub login is stored in the OS keyring, which the Claude sandbox cannot reach; "
        "run make gh-auth to store it in gh's file"
    )

    def count_warning(self, working: int, total: int) -> str:
        return (
            f"WARN: GitHub login: gh holds {working} working of {total} logins; keep exactly one "
            "(gh auth logout --user <login> for any other, or run make gh-auth)"
        )

    def test_gh_login_warns_on_a_keyring_login(self) -> None:
        # Outside the sandbox gh names the keyring; inside it, an unreachable keyring token fails as "default",
        # and the storage warning still appears next to the count warning.
        cases = (
            ("keyring", "success", [self.KEYRING_WARNING]),
            ("default", "error", [self.count_warning(0, 1), self.KEYRING_WARNING]),
        )
        for source, state, expected in cases:
            with self.subTest(source=source):
                account = {"login": "machine-login", "state": state, "active": True, "tokenSource": source}
                findings = self.module.gh_login_findings(
                    gh=self.fake_gh_status([account]), config_dir=self.temp_dir / "gh-config"
                )
                self.assertEqual(findings, expected)

    def test_gh_login_warns_on_a_hosts_file_not_0600(self) -> None:
        hosts = self.gh_hosts_file(0o644)
        account = {"login": "machine-login", "state": "success", "active": True, "tokenSource": hosts}

        findings = self.module.gh_login_findings(
            gh=self.fake_gh_status([account]), config_dir=self.temp_dir / "gh-config"
        )

        self.assertEqual(findings, [f"WARN: GitHub login: {hosts} has mode 0644, not 0600; run make gh-auth"])
        self.assertTrue(self.module.is_warning(findings[0]))

    def test_gh_login_storage_and_mode_are_checked_whatever_the_count_and_auth_state(self) -> None:
        hosts = self.gh_hosts_file(0o644)
        mode_warning = f"WARN: GitHub login: {hosts} has mode 0644, not 0600; run make gh-auth"
        cases = (
            (
                "two accounts, active one in the keyring",
                [
                    {"login": "machine-login", "state": "success", "active": True, "tokenSource": "keyring"},
                    {"login": "stray-login", "state": "success", "active": False, "tokenSource": "keyring"},
                ],
                [self.count_warning(2, 2), self.KEYRING_WARNING, mode_warning],
            ),
            (
                "active account in the keyring, inactive one in the 0644 file",
                [
                    {"login": "machine-login", "state": "success", "active": True, "tokenSource": "keyring"},
                    {"login": "stray-login", "state": "success", "active": False, "tokenSource": hosts},
                ],
                [self.count_warning(2, 2), self.KEYRING_WARNING, mode_warning],
            ),
            (
                "two accounts, 0644 file",
                [
                    {"login": "machine-login", "state": "success", "active": True, "tokenSource": hosts},
                    {"login": "stray-login", "state": "error", "active": False, "tokenSource": "default"},
                ],
                [self.count_warning(1, 2), mode_warning],
            ),
            (
                "auth error, 0644 file",
                [{"login": "machine-login", "state": "error", "active": True, "tokenSource": hosts}],
                [self.count_warning(0, 1), mode_warning],
            ),
        )
        for name, accounts, expected in cases:
            with self.subTest(name):
                findings = self.module.gh_login_findings(
                    gh=self.fake_gh_status(accounts), config_dir=self.temp_dir / "gh-config"
                )
                self.assertEqual(findings, expected)
                self.assertTrue(all(self.module.is_warning(finding) for finding in findings))

    def test_gh_login_checks_the_configured_hosts_file_whatever_gh_reports(self) -> None:
        # One working file login whose tokenSource names another path: the configured hosts.yml is still checked.
        elsewhere = self.temp_dir / "elsewhere/hosts.yml"
        elsewhere.parent.mkdir()
        elsewhere.touch(mode=0o600)
        hosts = Path(self.gh_hosts_file(0o644))
        account = {"login": "machine-login", "state": "success", "active": True, "tokenSource": str(elsewhere)}
        gh = self.fake_gh_status([account])

        findings = self.module.gh_login_findings(gh=gh, config_dir=hosts.parent)

        self.assertEqual(findings, [f"WARN: GitHub login: {hosts} has mode 0644, not 0600; run make gh-auth"])
        hosts.unlink()
        hosts.symlink_to(elsewhere)
        findings = self.module.gh_login_findings(gh=gh, config_dir=hosts.parent)
        self.assertEqual(findings, [f"WARN: GitHub login: {hosts} is not a regular file; run make gh-auth"])

    def test_gh_login_checks_the_hosts_file_when_gh_fails(self) -> None:
        # A missing gh, a timeout or unparsable output still leaves the configured hosts.yml checked.
        hosts = Path(self.gh_hosts_file(0o644))
        failed = "WARN: GitHub login: gh auth status failed or gh is missing; run make gh-auth"
        mode_warning = f"WARN: GitHub login: {hosts} has mode 0644, not 0600; run make gh-auth"
        garbage = self.temp_dir / "garbage-gh"
        garbage.write_text("#!/bin/sh\necho not-json\n")
        garbage.chmod(0o755)
        timeout = mock.patch.object(
            self.module.subprocess, "run", side_effect=self.module.subprocess.TimeoutExpired("gh", 60)
        )
        cases = (
            ("gh missing", str(self.temp_dir / "absent-gh"), contextlib.nullcontext()),
            ("gh times out", "gh", timeout),
            ("invalid JSON", str(garbage), contextlib.nullcontext()),
        )
        for name, gh, context in cases:
            with self.subTest(name), context:
                findings = self.module.gh_login_findings(gh=gh, config_dir=hosts.parent)
                self.assertEqual(findings, [failed, mode_warning])

    def test_gh_login_ignores_a_forced_color_setting(self) -> None:
        # gh colours its JSON under CLICOLOR_FORCE, which would break the parse.
        account = {"login": "machine-login", "state": "success", "active": True, "tokenSource": self.gh_hosts_file()}
        gh = Path(self.fake_gh_status([account]))
        gh.write_text(gh.read_text().replace("#!/bin/sh\n", '#!/bin/sh\n[ -z "${CLICOLOR_FORCE-}" ] || exit 4\n', 1))

        with mock.patch.dict(os.environ, {"CLICOLOR_FORCE": "1"}):
            findings = self.module.gh_login_findings(gh=str(gh), config_dir=self.temp_dir / "gh-config")

        self.assertEqual(findings, ["found: GitHub login machine-login (every seat on this machine acts as it)"])

    def test_orchestrator_seat_lock_warns_on_a_bare_session_id(self) -> None:
        project, skill_dir, proc = self.seat_lock_fixture("e7734322-bare")

        warnings = self.module.orchestrator_seat_lock_warnings(project, skill_dir, proc)

        self.assertEqual(1, len(warnings), warnings)
        self.assertTrue(warnings[0].startswith("WARN: orchestrator seat lock "))
        self.assertIn("actas.dotfiles__claude-remediation-dot.session", warnings[0])
        self.assertIn("bare session id e7734322-bare", warnings[0])

    def test_orchestrator_seat_lock_is_quiet_for_a_composite_id_or_no_live_session(self) -> None:
        project, skill_dir, proc = self.seat_lock_fixture("e7734322-sid.15760")
        self.assertEqual([], self.module.orchestrator_seat_lock_warnings(project, skill_dir, proc))

        shutil.rmtree(self.temp_dir / "project")
        shutil.rmtree(self.temp_dir / "agmsg")
        shutil.rmtree(self.temp_dir / "proc")
        project, skill_dir, proc = self.seat_lock_fixture("e7734322-bare", live=False)
        self.assertEqual([], self.module.orchestrator_seat_lock_warnings(project, skill_dir, proc))


if __name__ == "__main__":
    unittest.main()
