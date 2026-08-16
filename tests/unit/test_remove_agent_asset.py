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

    def run_remover(
        self, *args: str, env: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
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
                    f"DRY-RUN: rm -rf -- {target.resolve()}\n"
                    "DRY-RUN: remove manifest step demo\n",
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
        self.write_manifest(
            {"demo": self.step("installer", [target]), "other": other}
        )

        result = self.run_remover("demo", "--yes")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(target.exists())
        self.assertEqual("keep", (sibling / "keep.txt").read_text())
        self.assertEqual({"other"}, set(self.manifest()["steps"]))
        self.assertEqual(other, self.manifest()["steps"]["other"])
        self.assertEqual(0o600, stat.S_IMODE(self.manifest_path.stat().st_mode))

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
        self.write_manifest(
            {"mixed": self.step("installer", [safe, outside])}
        )

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
        self.executable(
            "claude", 'printf "claude %s\\n" "$*" >> "$TEST_LOG"\n'
        )
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
            "DRY-RUN: claude plugin uninstall demo@market\n"
            "DRY-RUN: remove manifest step plugin\n",
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
            f"DRY-RUN: rm -rf -- {plugin_root.resolve()}\n"
            "DRY-RUN: remove manifest step crit\n",
            result.stdout,
        )
        self.assertNotIn(str(config), result.stdout)

    def test_plugin_uses_verified_codex_remove(self) -> None:
        self.executable("codex", "exit 0\n")
        cache = self.home / ".codex/plugins/cache/demo/demo"
        cache.mkdir(parents=True)
        self.write_manifest(
            {
                "codex-plugin": self.step(
                    "plugin", [cache], ["codex plugin add demo@market"]
                )
            }
        )

        result = self.run_remover("codex-plugin")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            "DRY-RUN: codex plugin remove demo@market\n"
            "DRY-RUN: remove manifest step codex-plugin\n",
            result.stdout,
        )

    def test_brew_uses_uninstall_for_unambiguous_formula(self) -> None:
        log = self.temp_dir / "brew.log"
        self.executable("brew", 'printf "brew %s\\n" "$*" >> "$TEST_LOG"\n')
        self.write_manifest(
            {
                "brew-step": self.step(
                    "brew", [], ["brew install demo-formula"]
                )
            }
        )

        result = self.run_remover(
            "brew-step", "--yes", env={"TEST_LOG": str(log)}
        )

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
            "herdr integration uninstall claude\n"
            "herdr integration uninstall codex\n",
            log.read_text(),
        )
        self.assertEqual({}, self.manifest()["steps"])

    def executable(self, name: str, body: str) -> None:
        path = self.bin_dir / name
        path.write_text("#!/usr/bin/env bash\n" + textwrap.dedent(body))
        path.chmod(0o755)


if __name__ == "__main__":
    unittest.main()
