#!/usr/bin/env python3
"""Exercise guarded manifest-driven agent asset removal."""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REMOVER = ROOT / "home/dot_local/bin/common/executable_remove-agent-asset"
UV_STUB = """
case "$*" in
"tool dir") printf '%s\\n' "$HOME/.local/share/uv/tools" ;;
"tool uninstall hcom")
    [ -d "$HOME/.local/share/uv/tools/hcom" ] || { echo 'error: `hcom` is not installed' >&2; exit 2; }
    rm -rf "$HOME/.local/share/uv/tools/hcom" ;;
*) exit 2 ;;
esac
"""


class RemoveAgentAssetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="remove-agent-asset-test-"))
        self.home = self.temp_dir / "home"
        self.bin_dir = self.temp_dir / "bin"
        self.home.mkdir()
        self.bin_dir.mkdir()
        jq = shutil.which("jq")
        self.assertIsNotNone(jq, "jq is required for agent asset removal tests")
        (self.bin_dir / "jq").symlink_to(jq)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    @property
    def manifest_path(self) -> Path:
        return self.home / ".agents/.installed-manifest.json"

    def write_manifest(self, steps: dict[str, dict[str, object]]) -> None:
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(json.dumps({"version": 1, "steps": steps}))
        self.manifest_path.chmod(0o600)

    def manifest(self) -> dict[str, object]:
        return json.loads(self.manifest_path.read_text())

    def run_remover(self, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(REMOVER), *args],
            env={
                **os.environ,
                "HOME": str(self.home),
                "PATH": f"{self.bin_dir}:/usr/bin:/bin",
                **(env or {}),
            },
            text=True,
            capture_output=True,
            check=False,
        )

    def step(
        self,
        kind: str,
        paths: list[Path],
        commands: list[str] | None = None,
    ) -> dict[str, object]:
        return {
            "installed_at": "2026-08-16T00:00:00Z",
            "kind": kind,
            "paths": [str(path) for path in paths],
            "commands": commands or [],
            "source_version": "test",
        }

    def test_default_and_explicit_dry_run_print_without_mutating(self) -> None:
        target = self.home / ".agents/cache/demo"
        target.mkdir(parents=True)
        (target / "asset.txt").write_text("asset")
        self.write_manifest({"demo": self.step("rsync", [target])})
        before = self.manifest_path.read_bytes()

        for option in ((), ("--dry-run",)):
            with self.subTest(option=option):
                result = self.run_remover("demo", *option)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(
                    f"DRY-RUN: rm -rf -- {target.resolve()}\nDRY-RUN: remove manifest step demo\n",
                    result.stdout,
                )
                self.assertTrue(target.is_dir())
                self.assertEqual(before, self.manifest_path.read_bytes())

    def test_yes_removes_only_recorded_path_and_preserves_other_steps(self) -> None:
        target = self.home / ".agents/cache/demo"
        sibling = self.home / ".agents/cache/keep"
        target.mkdir(parents=True)
        sibling.mkdir(parents=True)
        (target / "asset.txt").write_text("asset")
        (sibling / "keep.txt").write_text("keep")
        other = self.step("rsync", [sibling])
        self.write_manifest({"demo": self.step("installer", [target]), "other": other})

        result = self.run_remover("demo", "--yes")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(target.exists())
        self.assertEqual("keep", (sibling / "keep.txt").read_text())
        self.assertEqual({"other"}, set(self.manifest()["steps"]))
        self.assertEqual(other, self.manifest()["steps"]["other"])
        self.assertEqual(0o600, stat.S_IMODE(self.manifest_path.stat().st_mode))

    def test_parameterized_step_removal_preserves_sibling_identity(self) -> None:
        claude = self.home / ".local/share/mise/installs/claude"
        codex = self.home / ".local/share/mise/installs/codex"
        claude.mkdir(parents=True)
        codex.mkdir(parents=True)
        codex_entry = self.step("installer", [codex])
        self.write_manifest(
            {
                "ensure_mise_npm_agent_cli:claude": self.step("installer", [claude]),
                "ensure_mise_npm_agent_cli:codex": codex_entry,
            }
        )

        result = self.run_remover("ensure_mise_npm_agent_cli:claude", "--yes")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(claude.exists())
        self.assertTrue(codex.is_dir())
        self.assertEqual({"ensure_mise_npm_agent_cli:codex"}, set(self.manifest()["steps"]))
        self.assertEqual(
            codex_entry,
            self.manifest()["steps"]["ensure_mise_npm_agent_cli:codex"],
        )

    def test_invalid_manifest_is_rejected(self) -> None:
        cases = {
            "truncated": "{",
            "wrong-version": json.dumps({"version": 2, "steps": {}}),
            "wrong-steps": json.dumps({"version": 1, "steps": []}),
        }
        for name, content in cases.items():
            with self.subTest(name=name):
                self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
                self.manifest_path.write_text(content)

                result = self.run_remover("ensure_mise_npm_agent_cli:claude")

                self.assertEqual(1, result.returncode)
                self.assertIn("invalid installed asset manifest", result.stderr)

    def test_tampered_manifest_outside_safe_roots_is_refused(self) -> None:
        outside = self.temp_dir / "outside"
        outside.mkdir()
        (outside / "keep.txt").write_text("keep")
        self.write_manifest({"tampered": self.step("installer", [outside])})
        before = self.manifest_path.read_bytes()

        result = self.run_remover("tampered", "--yes")

        self.assertEqual(1, result.returncode)
        self.assertIn("refusing path outside allowed asset roots", result.stderr)
        self.assertEqual("keep", (outside / "keep.txt").read_text())
        self.assertEqual(before, self.manifest_path.read_bytes())

    def test_all_paths_are_preflighted_before_any_deletion(self) -> None:
        safe = self.home / ".agents/cache/safe-first"
        outside = self.temp_dir / "unsafe-second"
        safe.mkdir(parents=True)
        outside.mkdir()
        (safe / "keep.txt").write_text("safe")
        (outside / "keep.txt").write_text("outside")
        self.write_manifest({"mixed": self.step("installer", [safe, outside])})

        result = self.run_remover("mixed", "--yes")

        self.assertEqual(1, result.returncode)
        self.assertIn("refusing path outside allowed asset roots", result.stderr)
        self.assertEqual("safe", (safe / "keep.txt").read_text())
        self.assertEqual("outside", (outside / "keep.txt").read_text())
        self.assertIn("mixed", self.manifest()["steps"])

    def test_unknown_step_lists_known_steps_without_guessing(self) -> None:
        path = self.home / ".agents/known"
        self.write_manifest(
            {
                "zeta": self.step("rsync", [path]),
                "alpha": self.step("rsync", [path]),
            }
        )

        result = self.run_remover("missing", "--yes")

        self.assertEqual(1, result.returncode)
        self.assertIn("ERROR: unknown manifest step: missing", result.stderr)
        self.assertIn("Known steps: alpha, zeta", result.stderr)

    def test_recorded_symlink_is_removed_without_following_target(self) -> None:
        target = self.temp_dir / "external-target"
        target.mkdir()
        (target / "keep.txt").write_text("keep")
        link = self.home / ".agents/skills/demo-link"
        link.parent.mkdir(parents=True)
        link.symlink_to(target, target_is_directory=True)
        self.write_manifest({"linked": self.step("installer", [link])})

        result = self.run_remover("linked", "--yes")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(link.exists())
        self.assertFalse(link.is_symlink())
        self.assertEqual("keep", (target / "keep.txt").read_text())

    def test_plugin_uses_verified_claude_uninstall(self) -> None:
        cache = self.home / ".claude/plugins/cache/demo/demo"
        settings = self.home / ".claude/settings.json"
        cache.mkdir(parents=True)
        settings.parent.mkdir(parents=True, exist_ok=True)
        settings.write_text("{}")
        log = self.temp_dir / "cli.log"
        self.executable("claude", 'printf "claude %s\\n" "$*" >> "$TEST_LOG"\n')
        self.write_manifest(
            {
                "plugin": self.step(
                    "plugin",
                    [cache, settings],
                    ["claude plugin install demo@market"],
                )
            }
        )

        dry_run = self.run_remover("plugin")
        removed = self.run_remover("plugin", "--yes", env={"TEST_LOG": str(log)})

        self.assertEqual(
            "DRY-RUN: claude plugin uninstall demo@market\nDRY-RUN: remove manifest step plugin\n",
            dry_run.stdout,
        )
        self.assertEqual(0, removed.returncode, removed.stderr)
        self.assertEqual("claude plugin uninstall demo@market\n", log.read_text())
        self.assertEqual({}, self.manifest()["steps"])

    def test_crit_plugin_falls_back_to_data_path_but_not_config(self) -> None:
        plugin_root = self.home / ".codex/plugins/crit"
        config = self.home / ".codex/config.toml"
        plugin_root.mkdir(parents=True)
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text("managed = true\n")
        self.write_manifest(
            {
                "crit": self.step(
                    "plugin",
                    [plugin_root, config],
                    ["crit install codex-plugin --force"],
                )
            }
        )

        result = self.run_remover("crit")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            f"DRY-RUN: rm -rf -- {plugin_root.resolve()}\nDRY-RUN: remove manifest step crit\n",
            result.stdout,
        )
        self.assertNotIn(str(config), result.stdout)

    def test_plugin_uses_verified_codex_remove(self) -> None:
        self.executable("codex", "exit 0\n")
        cache = self.home / ".codex/plugins/cache/demo/demo"
        cache.mkdir(parents=True)
        self.write_manifest({"codex-plugin": self.step("plugin", [cache], ["codex plugin add demo@market"])})

        result = self.run_remover("codex-plugin")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            "DRY-RUN: codex plugin remove demo@market\nDRY-RUN: remove manifest step codex-plugin\n",
            result.stdout,
        )

    def test_brew_uses_uninstall_for_unambiguous_formula(self) -> None:
        log = self.temp_dir / "brew.log"
        self.executable("brew", 'printf "brew %s\\n" "$*" >> "$TEST_LOG"\n')
        self.write_manifest({"brew-step": self.step("brew", [], ["brew install demo-formula"])})

        result = self.run_remover("brew-step", "--yes", env={"TEST_LOG": str(log)})

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("brew uninstall demo-formula\n", log.read_text())
        self.assertEqual({}, self.manifest()["steps"])

    def test_brew_refuses_ambiguous_formula(self) -> None:
        self.write_manifest(
            {
                "brew-step": self.step(
                    "brew",
                    [],
                    ["brew install first", "brew install second"],
                )
            }
        )

        result = self.run_remover("brew-step", "--yes")

        self.assertEqual(1, result.returncode)
        self.assertIn("ambiguous brew formula", result.stderr)
        self.assertIn("brew-step", self.manifest()["steps"])

    def test_integration_uses_verified_herdr_uninstall(self) -> None:
        log = self.temp_dir / "herdr.log"
        self.executable(
            "herdr",
            """
            if [[ "$*" == "integration uninstall --help" ]]; then
                exit 0
            fi
            printf "herdr %s\\n" "$*" >> "$TEST_LOG"
            """,
        )
        self.write_manifest(
            {
                "herdr": self.step(
                    "integration",
                    [
                        self.home / ".claude/hooks/herdr-agent-state.sh",
                        self.home / ".codex/herdr-agent-state.sh",
                    ],
                    [
                        "herdr integration install claude",
                        "herdr integration install codex",
                    ],
                )
            }
        )

        result = self.run_remover("herdr", "--yes", env={"TEST_LOG": str(log)})

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            "herdr integration uninstall claude\nherdr integration uninstall codex\n",
            log.read_text(),
        )
        self.assertEqual({}, self.manifest()["steps"])

    def remove_hcom(
        self, *, uv: bool = True, installed: bool = True, mode: str = "--yes"
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, Path]]:
        # The Bot's P2 4303212235 and the audit of #398 (finding 2): the hcom step leaves its binary, its retained
        # wheel, uv's tool environment and its receipt behind.
        tools = self.home / ".local/share/uv/tools/hcom"
        paths = {
            "binary": self.home / ".local/bin/hcom",
            "wheel": self.home / ".local/share/agent-assets/hcom/hcom-0.7.30-py3-none-any.whl",
            "environment": tools / "bin/hcom",
            "receipt": tools / "uv-receipt.toml",
        }
        for name, path in paths.items():
            if installed or name in ("binary", "wheel"):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("x")
        if uv:  # the stub answers as uv does and uninstalls uv's own state only; the remover deletes the recorded paths
            self.executable("uv", UV_STUB)
        recorded = [paths["binary"], paths["wheel"]]
        self.write_manifest({"update_hcom": self.step("installer", recorded, ["uv tool install --force <wheel>"])})
        return self.run_remover("update_hcom", mode), paths

    def assert_hcom_removal_deletes(self, name: str) -> None:
        removed, paths = self.remove_hcom()
        self.assertEqual(0, removed.returncode, removed.stdout + removed.stderr)
        self.assertFalse(paths[name].exists(), removed.stdout)
        self.assertEqual({}, self.manifest()["steps"])

    def test_hcom_removal_deletes_the_recorded_binary(self) -> None:
        self.assert_hcom_removal_deletes("binary")

    def test_hcom_removal_deletes_the_retained_wheel(self) -> None:
        self.assert_hcom_removal_deletes("wheel")

    def test_hcom_removal_uninstalls_the_uv_tool_environment(self) -> None:
        self.assert_hcom_removal_deletes("environment")

    def test_hcom_removal_uninstalls_the_uv_receipt(self) -> None:
        self.assert_hcom_removal_deletes("receipt")

    def test_hcom_removal_without_uv_reports_and_removes_nothing(self) -> None:
        removed, paths = self.remove_hcom(uv=False)
        self.assertNotEqual(0, removed.returncode)
        self.assertIn("uv command not found", removed.stderr)
        self.assertEqual([], [name for name, path in paths.items() if not path.exists()])
        self.assertIn("update_hcom", self.manifest()["steps"])

    def test_hcom_removal_skips_the_uninstall_when_uv_has_no_hcom_and_removes_the_rest(self) -> None:
        # The worker review: an hcom uv already uninstalled (`hcom` is not installed, exit 2) must not stop the removal.
        removed, paths = self.remove_hcom(installed=False)
        self.assertEqual(0, removed.returncode, removed.stdout + removed.stderr)
        self.assertIn("SKIP: uv has no hcom tool environment", removed.stdout)
        self.assertEqual([], [name for name, path in paths.items() if path.exists()])
        self.assertEqual({}, self.manifest()["steps"])

    def test_hcom_dry_run_without_uv_prints_the_plan(self) -> None:
        removed, paths = self.remove_hcom(uv=False, mode="--dry-run")
        self.assertEqual(0, removed.returncode, removed.stderr)
        self.assertIn("DRY-RUN: uv tool uninstall hcom\n", removed.stdout)
        self.assertEqual([], [name for name, path in paths.items() if not path.exists()])

    def executable(self, name: str, body: str) -> None:
        path = self.bin_dir / name
        path.write_text("#!/usr/bin/env bash\n" + textwrap.dedent(body))
        path.chmod(0o755)


if __name__ == "__main__":
    unittest.main()
