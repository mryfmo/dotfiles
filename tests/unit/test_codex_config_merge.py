#!/usr/bin/env python3
"""Exercise Codex config modify-script merge behavior."""

from __future__ import annotations

import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

import tomllib

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

    def test_working_tree_placeholder_falls_back_to_source_dir_parent(self) -> None:
        output = self.merge(
            """
            [projects."{{ .chezmoi.workingTree }}"]
            trust_level = "trusted"
            """,
            "",
        )

        data = tomllib.loads(output)
        self.assertEqual(list(data["projects"].keys()), [str(self.source_dir.parent)])

    def test_working_tree_placeholder_prefers_env_override(self) -> None:
        self.baseline_path.write_text('[projects."{{ .chezmoi.workingTree }}"]\ntrust_level = "trusted"\n')
        env_override = self.source_dir / "explicit-working-tree"
        env = os.environ.copy()
        env["CHEZMOI_SOURCE_DIR"] = str(self.source_dir)
        env["CHEZMOI_WORKING_TREE"] = str(env_override)
        result = subprocess.run(
            [str(MERGE_SCRIPT)],
            input="",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=True,
        )

        data = tomllib.loads(result.stdout)
        self.assertEqual(list(data["projects"].keys()), [str(env_override)])

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
        self.assertEqual(
            data["marketplaces"]["ponytail"]["source"],
            "https://example.invalid/repo.git",
        )

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

    def test_repeated_runtime_tables_are_preserved_in_order(self) -> None:
        output = self.merge(
            """
            model = "managed"
            """,
            """
            model = "managed"

            [[hooks.state.sub]]
            name = "first"

            [[hooks.state.sub]]
            name = "second"
            """,
        )

        self.assertEqual(output.count("[[hooks.state.sub]]"), 2)
        self.assertLess(output.index('name = "first"'), output.index('name = "second"'))

    def test_fresh_machine_outputs_managed_baseline(self) -> None:
        managed = """
            model = "managed"

            [projects."/repo"]
            trust_level = "trusted"
            """
        output = self.merge(managed, "")

        self.assertEqual(output, textwrap.dedent(managed).lstrip())

    def test_retired_disabled_mcp_servers_are_purged_and_enabled_ones_kept(self) -> None:
        retired = ("filesystem_dotfiles", "time", "sequential_thinking", "playwright")
        current = 'model = "gpt-5.6-sol"\n' + "".join(
            f'\n[mcp_servers.{name}]\ncommand = "npx"\nenabled = false\nrequired = false\n' for name in retired
        )
        # A disabled retired parent takes its child table with it.
        current += '\n[mcp_servers.github]\ncommand = "docker"\nenabled = false\n'
        current += '\n[mcp_servers.github.env]\nGITHUB_TOOLSETS = "repos"\n'
        # Enablement is read from the parsed field, not from text inside a string value.
        current += (
            '\n[mcp_servers.context7]\nurl = "https://mcp.context7.com/mcp"\nenabled = true\n'
            'description = """\nenabled = false\n"""\n'
        )
        current += '\n[mcp_servers.context7.env]\nNOTE = "kept with its parent"\n'
        current += '\n[mcp_servers.private_server]\nurl = "https://example.com/mcp"\nenabled = false\n'

        output = self.merge('model = "gpt-5.6-sol"\n', current)

        data = tomllib.loads(output)
        self.assertEqual(sorted(data["mcp_servers"]), ["context7", "private_server"])
        self.assertTrue(data["mcp_servers"]["context7"]["enabled"])
        self.assertEqual(data["mcp_servers"]["context7"]["env"], {"NOTE": "kept with its parent"})
        self.assertNotIn("GITHUB_TOOLSETS", output)

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

    def test_declared_hook_trust_replaces_stale_entries_and_keeps_undeclared(self) -> None:
        home = self.source_dir / "target-home"
        key = f"{home}/.codex/config.toml:permission_request:0:0"
        block = MERGE_SCRIPT.read_text().split("# >>> codex hook trust", 1)[1].split("# <<< codex hook trust", 1)[0]
        namespace = {"sys": __import__("sys"), "Path": Path}
        exec(block.split("\n", 1)[1], namespace)
        handler = namespace["HOOK_TRUST"]["config_hooks"]["permission_request"][0]["hooks"][0]
        expected = namespace["codex_hook_hash"]("permission_request", "*", namespace["with_home"](handler, str(home)))
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(home))
        # Like the rendered template: the declared keys appear under [hooks.state] with their managed fields.
        self.baseline_path.write_text(
            "[hooks.state]\n\n"
            '[hooks.state."{{ .chezmoi.homeDir }}/.codex/config.toml:permission_request:0:0"]\nenabled = true\n\n'
            '[hooks.state."ponytail@ponytail:hooks/claude-codex-hooks.json:session_start:0:0"]\nenabled = true\n'
        )
        result = subprocess.run(
            [str(MERGE_SCRIPT)],
            input=(
                f'[hooks.state]\n\n[hooks.state."{key}"]\ntrusted_hash = "sha256:stale"\n\n'
                '[hooks.state."/elsewhere/hooks.json:stop:0:0"]\ntrusted_hash = "sha256:operator"\n'
            ),
            text=True,
            capture_output=True,
            env=env,
            check=True,
        )

        state = tomllib.loads(result.stdout)["hooks"]["state"]
        self.assertEqual(state[key], {"trusted_hash": expected, "enabled": True})
        self.assertEqual(state["/elsewhere/hooks.json:stop:0:0"], {"trusted_hash": "sha256:operator"})
        self.assertIn(f"replacing sha256:stale with {expected}", result.stderr)
        # No plugin cache in the fixture home: the plugin pins fall back to the manifest literal, with a warning.
        ponytail = "ponytail@ponytail:hooks/claude-codex-hooks.json:session_start:0:0"
        self.assertTrue(state[ponytail]["trusted_hash"].startswith("sha256:"))
        self.assertIn(f"warning: cannot compute hook trust for {ponytail} (no installed copy", result.stderr)
        # A declared key the template does not carry (crit) is left alone, not injected.
        self.assertNotIn("crit@mryfmo-personal-plugins:hooks/hooks.json:stop:0:0", state)

    def test_make_update_refreshes_codex_hook_trust_after_the_plugin_update(self) -> None:
        script = (ROOT / "scripts/update-agent-assets.sh").read_text()
        main = script.split("\nfunction main() {\n", 1)[1].split("\n}\n", 1)[0]
        steps = [line.strip() for line in main.splitlines()]
        # The refresh is the last step of the asset update, after every Codex plugin update.
        self.assertEqual(steps[-1], "refresh_codex_hook_trust")
        for plugin_step in ("update_codex_superpowers", "update_codex_crit", "update_codex_ponytail"):
            with self.subTest(step=plugin_step):
                self.assertLess(steps.index(plugin_step), steps.index("refresh_codex_hook_trust"))
        refresh = script.split("\nfunction refresh_codex_hook_trust() {\n", 1)[1].split("\n}\n", 1)[0]
        # Unattended: --force never prompts, and only the managed Codex config files are re-applied.
        self.assertIn('chezmoi apply --force "${targets[@]}"', refresh)
        self.assertIn("pattern='/\\.codex/([a-z0-9_]+\\.)?config\\.toml$'", refresh)
        makefile = (ROOT / "Makefile").read_text()
        update = makefile.split("\nupdate:\n", 1)[1].split("\n\n", 1)[0]
        self.assertIn("./scripts/update-agent-assets.sh", update)
        self.assertIn("refresh_codex_hook_trust", makefile.split("\ncodex-hook-trust:\n", 1)[1].split("\n\n", 1)[0])

    def run_hook_trust_refresh(self, managed: str, apply_status: int = 0) -> tuple[subprocess.CompletedProcess, str]:
        bin_dir = self.source_dir / "bin"
        bin_dir.mkdir(exist_ok=True)
        calls = self.source_dir / "chezmoi-calls"
        fake = bin_dir / "chezmoi"
        listing = self.source_dir / "managed-listing"
        listing.write_text(managed)
        fake.write_text(
            "#!/bin/sh\n"
            f'printf "%s\\n" "$*" >> {str(calls)!r}\n'
            f'if [ "$1" = managed ]; then cat {str(listing)!r}; exit 0; fi\n'
            f"exit {apply_status}\n"
        )
        fake.chmod(0o755)
        result = subprocess.run(
            [
                "bash",
                "-c",
                'source "$1" && refresh_codex_hook_trust',
                "bash",
                str(ROOT / "scripts/update-agent-assets.sh"),
            ],
            text=True,
            capture_output=True,
            env={**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"},
            check=False,
        )
        return result, calls.read_text() if calls.exists() else ""

    def test_hook_trust_refresh_reapplies_only_the_codex_config_files(self) -> None:
        managed = "/h/.codex/config.toml\n/h/.codex/standard.config.toml\n/h/.codex/AGENTS.md\n/h/.zshrc\n"
        result, calls = self.run_hook_trust_refresh(managed)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            calls.splitlines(),
            [
                "managed --path-style=absolute --include=files",
                "apply --force /h/.codex/config.toml /h/.codex/standard.config.toml",
            ],
        )
        result, calls = self.run_hook_trust_refresh("/h/.zshrc\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls.splitlines()[-1], "managed --path-style=absolute --include=files")
        # A failed refresh warns and lets the rest of `make update` continue.
        result, _ = self.run_hook_trust_refresh(managed, apply_status=1)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("WARN: Codex hook trust not refreshed: chezmoi apply failed", result.stderr)

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
