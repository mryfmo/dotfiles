#!/usr/bin/env python3
"""Exercise Codex config modify-script merge behavior."""

from __future__ import annotations

import os
import subprocess
import tempfile
import textwrap
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MERGE_SCRIPT = ROOT / "home/dot_codex/modify_private_config.toml"


class CodexConfigMergeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="codex-config-merge-test-")
        self.source_dir = Path(self.temp_dir.name)
        (self.source_dir / ".chezmoitemplates").mkdir()
        self.baseline_path = self.source_dir / ".chezmoitemplates/codex-config-managed.toml"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def merge(self, managed: str, current: str) -> str:
        self.baseline_path.write_text(textwrap.dedent(managed).lstrip())
        env = os.environ.copy()
        env["CHEZMOI_SOURCE_DIR"] = str(self.source_dir)
        env["CHEZMOI_HOME_DIR"] = str(self.source_dir / "target-home")
        result = subprocess.run(
            [str(MERGE_SCRIPT)],
            input=textwrap.dedent(current).lstrip(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=True,
        )
        tomllib.loads(result.stdout)
        return result.stdout

    def test_managed_templates_are_rendered_before_merge(self) -> None:
        output = self.merge(
            """
            [sandbox_workspace_write]
            writable_roots = ["{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db"]

            [mcp_servers.filesystem_dotfiles]
            args = ["-y", "server", "{{ .chezmoi.sourceDir }}"]
            """,
            "",
        )

        data = tomllib.loads(output)
        self.assertEqual(
            data["sandbox_workspace_write"]["writable_roots"],
            [str(self.source_dir / "target-home/.agents/skills/agmsg/db")],
        )
        self.assertEqual(
            data["mcp_servers"]["filesystem_dotfiles"]["args"],
            ["-y", "server", str(self.source_dir)],
        )

    def test_managed_wins_for_managed_keys(self) -> None:
        output = self.merge(
            """
            model = "managed"
            sandbox_mode = "workspace-write"

            [mcp_servers.github]
            command = "docker"
            enabled = false
            """,
            """
            model = "runtime"
            sandbox_mode = "danger-full-access"

            [mcp_servers.github]
            command = "bad"
            enabled = true
            """,
        )

        data = tomllib.loads(output)
        self.assertEqual(data["model"], "managed")
        self.assertEqual(data["sandbox_mode"], "workspace-write")
        self.assertEqual(data["mcp_servers"]["github"]["command"], "docker")
        self.assertFalse(data["mcp_servers"]["github"]["enabled"])

    def test_runtime_tables_are_preserved(self) -> None:
        output = self.merge(
            """
            model = "managed"

            [hooks.state."managed"]
            trusted_hash = "sha256:managed"

            [tui.model_availability_nux]
            gpt-5 = 1
            """,
            """
            model = "runtime"

            [hooks.state."managed"]
            trusted_hash = "sha256:runtime"

            [tui.model_availability_nux]
            gpt-5 = 9
            "gpt-5.5" = 2
            """,
        )

        data = tomllib.loads(output)
        self.assertEqual(data["model"], "managed")
        self.assertEqual(data["hooks"]["state"]["managed"]["trusted_hash"], "sha256:runtime")
        self.assertEqual(data["tui"]["model_availability_nux"]["gpt-5"], 9)
        self.assertEqual(data["tui"]["model_availability_nux"]["gpt-5.5"], 2)

    def test_runtime_tables_seed_from_managed_when_absent(self) -> None:
        output = self.merge(
            """
            model = "managed"

            [marketplaces.ponytail]
            source = "https://example.invalid/repo.git"
            """,
            """
            model = "runtime"
            """,
        )

        data = tomllib.loads(output)
        self.assertEqual(data["marketplaces"]["ponytail"]["source"], "https://example.invalid/repo.git")

    def test_current_only_runtime_tables_keep_current_group_order(self) -> None:
        output = self.merge(
            """
            model = "managed"

            [hooks.state."managed-hook"]
            trusted_hash = "sha256:managed"

            [projects."/repo"]
            trust_level = "trusted"
            """,
            """
            model = "runtime"

            [hooks.state."managed-hook"]
            trusted_hash = "sha256:runtime"

            [hooks.state."current-only-hook"]
            trusted_hash = "sha256:current"

            [projects."/repo"]
            trust_level = "trusted"
            """,
        )

        self.assertLess(
            output.index('[hooks.state."current-only-hook"]'),
            output.index('[projects."/repo"]'),
        )

    def test_fresh_machine_outputs_managed_baseline(self) -> None:
        managed = """
            model = "managed"

            [projects."/repo"]
            trust_level = "trusted"
            """
        output = self.merge(managed, "")

        self.assertEqual(output, textwrap.dedent(managed).lstrip())

    def test_managed_permgate_replaces_stale_private_ccgate_hook(self) -> None:
        output = self.merge(
            """
            model = "gpt-5.6-sol"

            [[hooks.PermissionRequest]]
            matcher = "*"

            [[hooks.PermissionRequest.hooks]]
            type = "command"
            command = "permgate codex"
            timeout = 10
            """,
            """
            model = "gpt-5.6-sol"

            [[hooks.PermissionRequest]]
            matcher = ""

            [[hooks.PermissionRequest.hooks]]
            type = "command"
            command = "ccgate codex"
            statusMessage = "ccgate evaluating request"

            [mcp_servers.private_server]
            url = "https://example.com/mcp"
            """,
        )

        self.assertIn("hooks.PermissionRequest", output)
        self.assertIn("permgate codex", output)
        self.assertNotIn("ccgate", output)
        self.assertIn("[mcp_servers.private_server]", output)

    def test_unknown_current_tables_are_preserved(self) -> None:
        output = self.merge(
            """
            model = "managed"
            """,
            """
            model = "runtime"

            [experimental.local_state]
            enabled = true
            """,
        )

        data = tomllib.loads(output)
        self.assertEqual(data["model"], "managed")
        self.assertTrue(data["experimental"]["local_state"]["enabled"])


if __name__ == "__main__":
    unittest.main()
