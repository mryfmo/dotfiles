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
                "install_stale_skill": {
                    "paths": [str(skills / "stale-skill/payload")]
                },
                "install_stale_root": {"paths": [str(agents / "stale-root")]},
            },
        }
        (agents / ".installed-manifest.json").write_text(json.dumps(manifest))

        warnings = self.module.orphaned_asset_warnings(home, source)

        self.assertEqual(
            [
                f"WARN: orphaned agent asset: {agents / 'orphan-root'}; manual review required",
                f"WARN: stale agent asset: {agents / 'stale-root'}; suggested: remove-agent-asset install_stale_root",
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
        self.assertTrue(
            all(command[:3] == ("chezmoi", "apply", "--force") for command in commands)
        )

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
            self.assertEqual(
                ("chezmoi", "apply", "--force", str(target)), action.command
            )
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
        self.assertEqual([], self.module.compare_tree_contents(
            "shared skill directory",
            {Path("agmsg/scripts/history.sh"): source.read_text()},
            home / ".agents/skills",
            {Path("agmsg/scripts/history.sh"): source},
            warn_unmanaged_top_level=True,
        ))

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

    def test_mise_step_identity_comes_only_from_recorded_command(self) -> None:
        missing = self.target_root / "missing-cli"
        claude = self.module.AssetFinding(
            "ensure_mise_npm_agent_cli",
            (missing,),
            {
                "commands": [
                    "MISE_NPM_PACKAGE_MANAGER=npm npm_config_min_release_age=0 "
                    "mise install --force --locked npm:@anthropic-ai/claude-code"
                ]
            },
        )
        ambiguous = self.module.AssetFinding(
            "ensure_mise_npm_agent_cli",
            (missing,),
            {
                "commands": [
                    "mise install --force --locked npm:@anthropic-ai/claude-code",
                    "mise install --force --locked npm:@openai/codex",
                ]
            },
        )

        action = self.module.asset_repair_action(claude)

        self.assertEqual(
            ("ensure_mise_npm_agent_cli", "claude", "npm:@anthropic-ai/claude-code"),
            action.command[-3:],
        )
        self.assertIsNone(self.module.asset_repair_action(ambiguous))

    def test_repair_mode_converges_once_and_reports_each_action(self) -> None:
        target = self.target_root / "missing.json"
        initial = [f"Claude MCP config differs or is missing: {target}"]
        scans = iter((initial, []))
        calls: list[object] = []
        action = self.module.RepairAction(
            "missing file", target, ("chezmoi", "apply", "--force", str(target))
        )
        original_check = self.module.check
        original_actions = self.module.repair_actions
        original_execute = self.module.execute_repair
        try:
            self.module.check = lambda: next(scans)
            self.module.repair_actions = lambda failures, home=None: (
                [action] if failures else []
            )
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
        action = self.module.RepairAction(
            "missing file", target, ("chezmoi", "apply", "--force", str(target))
        )

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
            self.module.execute_repair = lambda action: self.fail(
                f"unexpected repair: {action}"
            )
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
            self.module.execute_repair = lambda action: self.fail(
                f"unexpected repair: {action}"
            )
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                with mock.patch.dict(os.environ, {"REPAIR": "1"}):
                    result = self.module.main([])
        finally:
            self.module.check = original_check
            self.module.execute_repair = original_execute

        self.assertEqual(0, result)
        self.assertEqual(
            "\n".join(warnings)
            + "\nactive agent runtime files match this chezmoi source tree\n",
            stdout.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()
