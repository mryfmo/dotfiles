#!/usr/bin/env python3
"""Exercise Codex config modify-script merge behavior."""

from __future__ import annotations

import json
import os
import runpy
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
MERGE_SCRIPT = ROOT / "home/dot_codex/modify_private_config.toml"
# A project path that exists on every test host, so the merge keeps its trust.
EXISTING_PROJECT = "/tmp"
# A profile table whose multiline strings hold header-like lines, with and without a trailing comment.
MULTILINE_PROFILE = (
    "[agents.reviewer]\n"
    'developer_instructions = """\n'
    "Examples:\n"
    '[hooks.state."custom-hook"] # example\n'
    '[projects."/x"]\n'
    'An escaped \\""" stays inside.\n'
    '"""\n'
    "notes = '''\n"
    "[[mcp_servers.example]] # literal\n"
    "[tui]\n"
    "'''\n"
    'one_line = """[a] # b"""\n'
)


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

    def test_codex_path_uses_mise_shims_and_names_homebrew_only_on_macos(self) -> None:
        home = self.source_dir / "target-home"
        self.baseline_path.write_text((ROOT / "home/.chezmoitemplates/codex-config-managed.toml").read_text())
        homebrew = ["/opt/homebrew/bin"]
        for target_os, os_entries in (("darwin", homebrew), ("linux", [])):
            with self.subTest(target_os=target_os):
                env = os.environ.copy()
                env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(home), CHEZMOI_OS=target_os)
                result = subprocess.run(
                    [str(MERGE_SCRIPT)], input="", text=True, capture_output=True, env=env, check=True
                )
                path = tomllib.loads(result.stdout)["shell_environment_policy"]["set"]["PATH"].split(":")
                # mise shims first (node from mise's config, no per-version node directory); Homebrew on macOS only.
                expected = [
                    *(str(home / entry) for entry in (".local/share/mise/shims", ".local/bin", ".local/bin/common")),
                    *os_entries,
                    *("/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin"),
                ]
                self.assertEqual(path, expected)

    def test_managed_templates_are_rendered_before_merge(self) -> None:
        output = self.merge(
            """
            [sandbox_workspace_write]
            writable_roots = ["{{ .chezmoi.homeDir }}/.cache/codex-root"]

            [mcp_servers.filesystem_dotfiles]
            args = ["-y", "server", "{{ .chezmoi.sourceDir }}"]
            """,
            "",
        )

        data = tomllib.loads(output)
        self.assertEqual(
            data["sandbox_workspace_write"]["writable_roots"],
            [str(self.source_dir / "target-home/.cache/codex-root")],
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

    def test_retired_mcp_servers_are_matched_by_decoded_key_path(self) -> None:
        current = 'model = "gpt-5.6-sol"\n'
        current += '\n[ mcp_servers . "github" ]\ncommand = "docker"\nenabled = false\n'
        current += '\n["mcp_servers".github.env]\nGITHUB_TOOLSETS = "repos"\n'
        current += '\n[mcp_servers."private_server"]\nurl = "https://example.com/mcp"\nenabled = false\n'

        output = self.merge('model = "gpt-5.6-sol"\n', current)

        self.assertEqual(sorted(tomllib.loads(output)["mcp_servers"]), ["private_server"])
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
        operator_hooks = self.source_dir / "elsewhere/hooks.json"
        operator_hooks.parent.mkdir()
        operator_hooks.write_text("{}")
        operator_key = f"{operator_hooks}:stop:0:0"
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
                f'[hooks.state."{operator_key}"]\ntrusted_hash = "sha256:operator"\n'
            ),
            text=True,
            capture_output=True,
            env=env,
            check=True,
        )

        state = tomllib.loads(result.stdout)["hooks"]["state"]
        self.assertEqual(state[key], {"trusted_hash": expected, "enabled": True})
        self.assertEqual(state[operator_key], {"trusted_hash": "sha256:operator"})
        self.assertIn(f"replacing sha256:stale with {expected}", result.stderr)
        # No plugin cache in the fixture home: the plugin pins fall back to the manifest literal, with a warning.
        ponytail = "ponytail@ponytail:hooks/claude-codex-hooks.json:session_start:0:0"
        self.assertTrue(state[ponytail]["trusted_hash"].startswith("sha256:"))
        self.assertIn(f"warning: cannot compute hook trust for {ponytail} (no installed copy", result.stderr)
        # A declared key the template does not carry (crit) is left alone, not injected.
        self.assertNotIn("crit@mryfmo-personal-plugins:hooks/hooks.json:stop:0:0", state)

    def test_a_plugin_hook_that_differs_from_its_pin_stays_untrusted(self) -> None:
        # A fixture Ponytail whose installed SessionStart hook is not the one the manifest pinned,
        # as after `make update` upgraded the marketplace to an unreviewed release.
        home = self.source_dir / "target-home"
        ponytail = "ponytail@ponytail:hooks/claude-codex-hooks.json:session_start:0:0"
        handler = {"type": "command", "command": "ponytail-unreviewed session-start", "timeout": 5}
        hook_file = home / ".codex/plugins/cache/ponytail/ponytail/99.0.0/hooks/claude-codex-hooks.json"
        hook_file.parent.mkdir(parents=True)
        hook_file.write_text(json.dumps({"hooks": {"SessionStart": [{"matcher": "startup", "hooks": [handler]}]}}))
        block = MERGE_SCRIPT.read_text().split("# >>> codex hook trust", 1)[1].split("# <<< codex hook trust", 1)[0]
        namespace = {"sys": __import__("sys"), "Path": Path}
        exec(block.split("\n", 1)[1], namespace)
        installed = namespace["codex_hook_hash"]("session_start", "startup", handler)
        pin = next(entry for entry in namespace["HOOK_TRUST"]["declared"] if entry["key"] == ponytail)["trusted_hash"]
        self.assertNotEqual(installed, pin)
        self.baseline_path.write_text(f'[hooks.state]\n\n[hooks.state."{ponytail}"]\nenabled = true\n')
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(home))
        # The current file already trusts the installed hook, as the previous apply-time hashing wrote it.
        current = f'[hooks.state]\n\n[hooks.state."{ponytail}"]\ntrusted_hash = "{installed}"\nenabled = true\n'

        for applied in range(2):
            with self.subTest(applied=applied):
                result = subprocess.run(
                    [str(MERGE_SCRIPT)], input=current, text=True, capture_output=True, env=env, check=True
                )
                state = tomllib.loads(result.stdout)["hooks"]["state"]
                self.assertEqual(state[ponytail], {"enabled": True})
                self.assertNotIn(installed, result.stdout)
                self.assertIn(f"{ponytail}", result.stderr)
                self.assertIn(installed, result.stderr)
                self.assertIn(pin, result.stderr)
                self.assertIn("/hooks", result.stderr)
                current = result.stdout

    def test_declared_hook_trust_replaces_a_single_quoted_existing_entry(self) -> None:
        home = self.source_dir / "target-home"
        key = f"{home}/.codex/config.toml:permission_request:0:0"
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(home))
        self.baseline_path.write_text(
            '[hooks.state]\n\n[hooks.state."{{ .chezmoi.homeDir }}/.codex/config.toml:permission_request:0:0"]\n'
            "enabled = true\n"
        )
        result = subprocess.run(
            [str(MERGE_SCRIPT)],
            input=f"[hooks.state]\n\n[hooks.state.'{key}']\ntrusted_hash = \"sha256:stale\"\n",
            text=True,
            capture_output=True,
            env=env,
            check=True,
        )

        # A literal-quoted existing entry is the same TOML key: it is replaced, not duplicated.
        state = tomllib.loads(result.stdout)["hooks"]["state"]
        self.assertTrue(state[key]["trusted_hash"].startswith("sha256:"))
        self.assertNotEqual(state[key]["trusted_hash"], "sha256:stale")
        self.assertEqual(result.stdout.count(key), 1)
        self.assertIn("replacing sha256:stale with", result.stderr)

    def test_declared_hook_trust_handles_table_headers_with_trailing_comments(self) -> None:
        home = self.source_dir / "target-home"
        key = f"{home}/.codex/config.toml:permission_request:0:0"
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(home))
        self.baseline_path.write_text(
            '[hooks.state]\n\n[hooks.state."{{ .chezmoi.homeDir }}/.codex/config.toml:permission_request:0:0"]\n'
            "enabled = true\n"
        )
        others = (
            '[hooks.state."custom-hook"] # mine\ntrusted_hash = "sha256:custom"\n\n'
            f'[projects."{EXISTING_PROJECT}"]  # trusted\ntrust_level = "trusted"\n'
        )
        # A commented declared header, then an uncommented one followed by commented unrelated tables.
        for declared in (f'[hooks.state."{key}"] # declared', f'[hooks.state."{key}"]'):
            with self.subTest(declared=declared):
                current = f'[hooks.state]\n\n{declared}\ntrusted_hash = "sha256:stale"\n\n' + others
                result = subprocess.run(
                    [str(MERGE_SCRIPT)], input=current, text=True, capture_output=True, env=env, check=True
                )

                # A commented header is still a header: the declared one is replaced once and the others survive.
                data = tomllib.loads(result.stdout)
                state = data["hooks"]["state"]
                self.assertNotEqual(state[key]["trusted_hash"], "sha256:stale")
                self.assertEqual(result.stdout.count(key), 1)
                self.assertEqual(state["custom-hook"], {"trusted_hash": "sha256:custom"})
                self.assertEqual(data["projects"][EXISTING_PROJECT], {"trust_level": "trusted"})
                self.assertIn("replacing sha256:stale with", result.stderr)

    def test_table_name_reads_headers_with_trailing_comments(self) -> None:
        table_name = runpy.run_path(str(MERGE_SCRIPT), run_name="codex_config_merge")["table_name"]
        for header, name in (
            ("[a]", "a"),
            ("[[a.b]]", "a.b"),
            ("  [ a . b ]  ", "a.b"),
            ('[hooks.state."x"] # c', "hooks.state.x"),
            ('[hooks.state."a]#b"]#c', 'hooks.state."a]#b"'),
            ("[hooks.state.'a]b'] # c", 'hooks.state."a]b"'),
            ('[hooks.state."q\\"]"]', 'hooks.state."q\\"]"'),
            ("[[a]] # c", "a"),
            ("[a] = 1", None),
            ("[a] x", None),
            ("[[a] ]", None),
            ('[a."b]', None),
            ("a = [1]", None),
        ):
            with self.subTest(header=header):
                self.assertEqual(table_name(header), name)

    def test_canonical_table_names_decode_each_key_segment(self) -> None:
        canonical = runpy.run_path(str(MERGE_SCRIPT), run_name="codex_config_merge")["canonical_table_name"]
        cases = (
            ("hooks . state", "hooks.state"),
            ('"hooks"."state"', "hooks.state"),
            ("'hooks' . \"state\"", "hooks.state"),
            (' hooks . state . "k/x:0" ', 'hooks.state."k/x:0"'),
            ("hooks.state.'k/x:0'", 'hooks.state."k/x:0"'),
            ('"hooks.state"', '"hooks.state"'),
            ('projects."/work"', 'projects."/work"'),
            ('a."b\\"c"', 'a."b\\"c"'),
            ('a."é"', 'a."é"'),
        )
        for raw, name in cases:
            with self.subTest(raw=raw):
                self.assertEqual(canonical(raw), name)

    def test_equivalent_hook_state_spellings_are_one_table(self) -> None:
        home = self.source_dir / "target-home"
        key = f"{home}/.codex/config.toml:permission_request:0:0"
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(home))
        self.baseline_path.write_text(
            '[hooks.state]\n\n[hooks.state."{{ .chezmoi.homeDir }}/.codex/config.toml:permission_request:0:0"]\n'
            "enabled = true\n"
        )
        others = f'\n[projects."{EXISTING_PROJECT}"]\ntrust_level = "trusted"\n'
        currents = [
            f'{parent}\n"{key}" = {{ trusted_hash = "sha256:stale", enabled = false }}\n'
            f'"other" = {{ trusted_hash = "sha256:other" }}\n' + others
            for parent in ("[hooks . state]", '["hooks"."state"]')
        ]
        currents.append(
            f'[hooks.state]\n"other" = {{ trusted_hash = "sha256:other" }}\n\n'
            f'[ hooks . state . "{key}" ]\ntrusted_hash = "sha256:stale"\n' + others
        )
        for current in currents:
            with self.subTest(current=current.splitlines()[0]):
                result = subprocess.run(
                    [str(MERGE_SCRIPT)], input=current, text=True, capture_output=True, env=env, check=True
                )

                data = tomllib.loads(result.stdout)
                state = data["hooks"]["state"]
                self.assertNotEqual(state[key]["trusted_hash"], "sha256:stale")
                self.assertIs(state[key]["enabled"], True)
                self.assertEqual(state["other"], {"trusted_hash": "sha256:other"})
                self.assertEqual(data["projects"][EXISTING_PROJECT], {"trust_level": "trusted"})
                self.assertEqual(result.stdout.count(key), 1)
                self.assertEqual(result.stderr.count("replacing sha256:stale with"), 1)
                self.assertNotIn("WARN", result.stderr)

    def test_header_like_lines_inside_multiline_strings_stay_string_content(self) -> None:
        home = self.source_dir / "target-home"
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(home))
        self.baseline_path.write_text('[hooks.state]\n\n[hooks.state."custom-hook"]\nenabled = true\n')
        current = '[hooks.state]\n\n[hooks.state."custom-hook"]\nenabled = true\n\n' + MULTILINE_PROFILE
        result = subprocess.run([str(MERGE_SCRIPT)], input=current, text=True, capture_output=True, env=env, check=True)

        self.assertIn(MULTILINE_PROFILE, result.stdout)
        merged = tomllib.loads(result.stdout)
        self.assertEqual(merged["agents"], tomllib.loads(MULTILINE_PROFILE)["agents"])
        self.assertEqual(merged["hooks"]["state"], {"custom-hook": {"enabled": True}})

    def test_multiline_string_after_tracks_basic_and_literal_strings(self) -> None:
        after = runpy.run_path(str(MERGE_SCRIPT), run_name="codex_config_merge")["multiline_string_after"]
        basic, literal = '"""', "'''"
        for line, before, expected in (
            ('a = """', None, basic),
            ("a = '''", None, literal),
            ('a = """x"""', None, None),
            ('a = """x""""', None, None),
            ('a = "\\"""" # """', None, None),
            ("a = 'x\"\"\"' # '''", None, None),
            ('# """', None, None),
            ('[a] # """', None, None),
            ('x \\""" y', basic, basic),
            ('x \\\\"""', basic, None),
            ('x """', literal, literal),
            ("x ''' b = '''", literal, literal),
            ('[hooks.state."x"] # c', basic, basic),
        ):
            with self.subTest(line=line, before=before):
                self.assertEqual(after(line + "\n", before), expected)

    def test_declared_hook_trust_replaces_inline_table_and_dotted_forms(self) -> None:
        home = self.source_dir / "target-home"
        key = f"{home}/.codex/config.toml:permission_request:0:0"
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(home))
        self.baseline_path.write_text(
            '[hooks.state]\n\n[hooks.state."{{ .chezmoi.homeDir }}/.codex/config.toml:permission_request:0:0"]\n'
            "enabled = true\n"
        )
        for entry in (
            f'"{key}" = {{ trusted_hash = "sha256:stale", enabled = false }}\n',
            f'"{key}".trusted_hash = "sha256:stale"\n"{key}" . enabled = false\n',
        ):
            with self.subTest(entry=entry):
                current = (
                    f'[hooks.state]\n{entry}"other" = {{ trusted_hash = "sha256:other" }}\n\n'
                    f'[projects."{EXISTING_PROJECT}"]\ntrust_level = "trusted"\n'
                )
                result = subprocess.run(
                    [str(MERGE_SCRIPT)], input=current, text=True, capture_output=True, env=env, check=True
                )

                data = tomllib.loads(result.stdout)
                state = data["hooks"]["state"]
                self.assertTrue(state[key]["trusted_hash"].startswith("sha256:"))
                self.assertNotEqual(state[key]["trusted_hash"], "sha256:stale")
                self.assertIs(state[key]["enabled"], True)
                self.assertEqual(state["other"], {"trusted_hash": "sha256:other"})
                self.assertEqual(data["projects"][EXISTING_PROJECT], {"trust_level": "trusted"})
                self.assertEqual(result.stderr.count("replacing sha256:stale with"), 1)
                self.assertNotIn("WARN", result.stderr)

    def test_declared_dotted_keys_under_hooks_and_at_the_root_are_replaced(self) -> None:
        home = self.source_dir / "target-home"
        key = f"{home}/.codex/config.toml:permission_request:0:0"
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(home))
        self.baseline_path.write_text(
            '[hooks.state]\n\n[hooks.state."{{ .chezmoi.homeDir }}/.codex/config.toml:permission_request:0:0"]\n'
            "enabled = true\n"
        )
        others = f'\n[projects."{EXISTING_PROJECT}"]\ntrust_level = "trusted"\n'
        for current in (
            f'[hooks]\nstate."{key}".trusted_hash = "sha256:stale"\nstate . "{key}" . enabled = false\n' + others,
            f'hooks.state."{key}".trusted_hash = "sha256:stale"\n"hooks".state."{key}".enabled = false\n' + others,
        ):
            with self.subTest(current=current.splitlines()[0]):
                result = subprocess.run(
                    [str(MERGE_SCRIPT)], input=current, text=True, capture_output=True, env=env, check=True
                )

                data = tomllib.loads(result.stdout)
                state = data["hooks"]["state"]
                self.assertNotEqual(state[key]["trusted_hash"], "sha256:stale")
                self.assertIs(state[key]["enabled"], True)
                self.assertEqual(data["projects"][EXISTING_PROJECT], {"trust_level": "trusted"})
                self.assertEqual(result.stdout.count(key), 1)
                self.assertEqual(result.stderr.count("replacing sha256:stale with"), 1)
                self.assertNotIn("WARN", result.stderr)

    def test_an_unpinned_plugin_hook_is_revoked_in_every_toml_form(self) -> None:
        # The audit case: the current file trusts the installed (unreviewed) Ponytail hook in a non-table form.
        home = self.source_dir / "target-home"
        ponytail = "ponytail@ponytail:hooks/claude-codex-hooks.json:session_start:0:0"
        handler = {"type": "command", "command": "ponytail-unreviewed session-start", "timeout": 5}
        hook_file = home / ".codex/plugins/cache/ponytail/ponytail/99.0.0/hooks/claude-codex-hooks.json"
        hook_file.parent.mkdir(parents=True)
        hook_file.write_text(json.dumps({"hooks": {"SessionStart": [{"matcher": "startup", "hooks": [handler]}]}}))
        block = MERGE_SCRIPT.read_text().split("# >>> codex hook trust", 1)[1].split("# <<< codex hook trust", 1)[0]
        namespace = {"sys": __import__("sys"), "Path": Path}
        exec(block.split("\n", 1)[1], namespace)
        installed = namespace["codex_hook_hash"]("session_start", "startup", handler)
        self.baseline_path.write_text(f'[hooks.state]\n\n[hooks.state."{ponytail}"]\nenabled = true\n')
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(home))
        entry = f'"{ponytail}" = {{ trusted_hash = "{installed}", enabled = true }}'
        operator_hooks = self.source_dir / "elsewhere/hooks.json"
        operator_hooks.parent.mkdir()
        operator_hooks.write_text("{}")
        operator_key = f"{operator_hooks}:stop:0:0"
        other = f'"{operator_key}" = {{ trusted_hash = "sha256:operator" }}'
        projects = f'\n[projects."{EXISTING_PROJECT}"]\ntrust_level = "trusted"\n'
        for form, current in (
            ("inline table under [hooks]", f"[hooks]\nstate = {{ {entry}, {other} }}\n{projects}"),
            ("inline table at the root", f"hooks.state = {{ {entry}, {other} }}\n{projects}"),
            ("nested inline table at the root", f"hooks = {{ state = {{ {entry}, {other} }} }}\n{projects}"),
            ("inline entries under [hooks.state]", f"[hooks.state]\n{entry}\n{other}\n{projects}"),
            (
                "dotted keys under [hooks]",
                f'[hooks]\nstate."{ponytail}".trusted_hash = "{installed}"\nstate.{other}\n{projects}',
            ),
            (
                "dotted keys at the root",
                f'hooks.state."{ponytail}".trusted_hash = "{installed}"\nhooks.state.{other}\n{projects}',
            ),
        ):
            with self.subTest(form=form):
                result = subprocess.run(
                    [str(MERGE_SCRIPT)], input=current, text=True, capture_output=True, env=env, check=False
                )

                self.assertEqual(result.returncode, 0, result.stderr)
                data = tomllib.loads(result.stdout)
                self.assertEqual(data["hooks"]["state"][ponytail], {"enabled": True})
                self.assertEqual(data["hooks"]["state"][operator_key], {"trusted_hash": "sha256:operator"})
                self.assertEqual(data["projects"][EXISTING_PROJECT], {"trust_level": "trusted"})
                self.assertNotIn(installed, result.stdout)

    def test_a_current_file_that_is_not_valid_toml_is_refused(self) -> None:
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(self.source_dir / "target-home"))
        self.baseline_path.write_text('[hooks.state]\n\n[hooks.state."custom-hook"]\nenabled = true\n')

        result = subprocess.run(
            [str(MERGE_SCRIPT)], input="[hooks\nstate = 1\n", text=True, capture_output=True, env=env, check=False
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("ERROR: codex config merge:", result.stderr)

    def test_every_modify_script_refuses_cleanly_without_tomllib(self) -> None:
        # Failure injection: run each committed modify script with tomllib unimportable.
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(self.source_dir / "target-home"))
        env["HOME"] = str(self.source_dir / "target-home")
        self.baseline_path.write_text('[hooks.state]\n\n[hooks.state."custom-hook"]\nenabled = true\n')
        blocked = "import runpy, sys; sys.modules['tomllib'] = None; runpy.run_path(sys.argv[1], run_name='__main__')"
        for script in sorted((ROOT / "home/dot_codex").glob("modify_*config.toml")):
            with self.subTest(script=script.name):
                result = subprocess.run(
                    [sys.executable, "-c", blocked, str(script)],
                    input="",
                    text=True,
                    capture_output=True,
                    env=env,
                    check=False,
                )

                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertIn("ERROR: codex config merge: reading hook trust needs Python 3.11", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_invalid_merge_output_is_refused(self) -> None:
        home = self.source_dir / "target-home"
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(home))
        self.baseline_path.write_text('[hooks.state]\n\n[hooks.state."custom-hook"]\nenabled = true\n')
        # A splitter that emits every chunk twice stands in for any representation the merge mishandles.
        source = MERGE_SCRIPT.read_text()
        broken = source.replace(
            '\nif __name__ == "__main__":',
            '\n_split_chunks = split_chunks\nsplit_chunks = lambda text: _split_chunks(text) * 2\n\nif __name__ == "__main__":',
        )
        self.assertNotEqual(broken, source)
        script = self.source_dir / "broken-merge"
        script.write_text(broken)
        script.chmod(0o755)
        current = '[hooks.state]\n\n[hooks.state."custom-hook"]\nenabled = true\n\n[projects."/work"]\ntrust_level = "trusted"\n'

        result = subprocess.run([str(script)], input=current, text=True, capture_output=True, env=env, check=False)

        # chezmoi keeps the target untouched when a modify script fails, and reports the error.
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("ERROR: codex config merge: the merged config is not valid TOML", result.stderr)

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
        # make update pulls, then runs everything else in update-tree, the second make.
        self.assertIn("update-tree", makefile.split("\nupdate:\n", 1)[1].split("\n\n", 1)[0])
        update = makefile.split("\nupdate-tree:\n", 1)[1].split("\n\n", 1)[0]
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

    def test_the_managed_skills_config_replaces_an_operator_array_in_every_toml_form(self) -> None:
        """U87: the managed [[skills.config]] array is the only one; a second copy of the key would abort the apply."""
        managed = """
            model = "managed"

            [[skills.config]]
            path = "/managed/SKILL.md"
            enabled = false
            """
        operator = '{ path = "/operator/SKILL.md", enabled = false }'
        forms = {
            "inline array under [skills]": f"[skills]\nmax_context_tokens = 500\nconfig = [\n  {operator},\n]\n",
            "dotted at the root": f"skills.config = [\n  {operator},\n]\nskills.max_context_tokens = 500\n",
            "inline table at the root": f"skills = {{ config = [{operator}], max_context_tokens = 500 }}\n",
            "array of tables": '[[skills.config]]\npath = "/operator/SKILL.md"\nenabled = false\n',
        }
        for form, skills in forms.items():
            with self.subTest(form=form):
                output = self.merge(managed, f'{skills}\n[tui]\ntheme = "night"\n')
                data = tomllib.loads(output)
                self.assertEqual([{"path": "/managed/SKILL.md", "enabled": False}], data["skills"]["config"])
                self.assertEqual({"theme": "night"}, data["tui"])
                if form != "array of tables":
                    self.assertEqual(500, data["skills"]["max_context_tokens"], "the other skills settings stay")

    def test_a_skills_table_that_cannot_be_rewritten_refuses_the_apply(self) -> None:
        self.baseline_path.write_text('model = "managed"\n')
        env = {**os.environ, "CHEZMOI_SOURCE_DIR": str(self.source_dir)}
        env["CHEZMOI_HOME_DIR"] = str(self.source_dir / "target-home")
        current = '[skills]\nconfig = [{ path = "/operator/SKILL.md", enabled = false }]\nsince = 2026-10-25\n'
        result = subprocess.run(
            [str(MERGE_SCRIPT)], input=current, text=True, capture_output=True, env=env, check=False
        )
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertIn("cannot rewrite a date value in skills", result.stderr)

    def merge_stale_paths(self, script: Path, current: str, home: Path) -> subprocess.CompletedProcess:
        """Run one committed modify script over `current` with an empty managed baseline and HOME at `home`."""
        self.baseline_path.write_text('model = "managed"\n')
        env = os.environ.copy()
        env.update(CHEZMOI_SOURCE_DIR=str(self.source_dir), CHEZMOI_HOME_DIR=str(home), HOME=str(home))
        return subprocess.run([str(script)], input=current, text=True, capture_output=True, env=env, check=True)

    def test_project_trust_for_a_path_that_no_longer_exists_is_dropped_in_every_form_by_every_modify_script(
        self,
    ) -> None:
        # Audit de9fff57 P2: a project written as an inline table or a dotted key kept its trust; every valid TOML
        # form is read from the parsed data, so an absent path loses its trust whatever form held it.
        kept = self.source_dir / "work/repo"
        kept.mkdir(parents=True)
        gone = self.source_dir / "work/deleted-checkout"
        k, g = json.dumps(str(kept)), json.dumps(str(gone))
        relative = '"~/relative-key"'
        forms = {
            "tables": f'[projects.{k}]\ntrust_level = "trusted"\n\n[projects.{g}]\ntrust_level = "trusted"\n\n'
            f'[projects.{relative}]\ntrust_level = "trusted"\n',
            "inline at the root": f'projects = {{ {k} = {{ trust_level = "trusted" }}, {g} = {{ trust_level = "trusted" }}, '
            f'{relative} = {{ trust_level = "trusted" }} }}\n',
            "dotted at the root": f'projects.{k}.trust_level = "trusted"\nprojects.{g}.trust_level = "trusted"\n'
            f'projects.{relative}.trust_level = "trusted"\n',
            "dotted and inline under [projects]": f'[projects]\n{k}.trust_level = "trusted"\n'
            f'{g} = {{ trust_level = "trusted" }}\n{relative}.trust_level = "trusted"\n',
            "mixed": f'projects.{g}.trust_level = "trusted"\n\n[projects.{k}]\ntrust_level = "trusted"\n\n'
            f'[projects.{relative}]\ntrust_level = "trusted"\n',
        }
        expected = {str(kept): {"trust_level": "trusted"}, "~/relative-key": {"trust_level": "trusted"}}
        home = self.source_dir / "target-home"
        for script in sorted((ROOT / "home/dot_codex").glob("modify_*config.toml")):
            for form, projects in forms.items():
                with self.subTest(script=script.name, form=form):
                    current = (
                        'approval_policy = "on-request"\n' + projects + "\n[experimental.local_state]\nenabled = true\n"
                    )
                    result = self.merge_stale_paths(script, current, home)

                    data = tomllib.loads(result.stdout)
                    self.assertEqual(expected, data["projects"])
                    self.assertTrue(data["experimental"]["local_state"]["enabled"])

    def test_projects_that_cannot_be_rewritten_refuse_the_apply(self) -> None:
        # An inline table whose array spans lines is valid TOML the line rewrite cannot carry: the apply stops with
        # the contracted message instead of keeping or dropping trust it could not read.
        gone = json.dumps(str(self.source_dir / "work/deleted-checkout"))
        current = f'projects = {{ {gone} = {{ trust_level = "trusted", tags = [\n"a",\n] }} }}\n'
        for script in sorted((ROOT / "home/dot_codex").glob("modify_*config.toml")):
            with self.subTest(script=script.name):
                with self.assertRaises(subprocess.CalledProcessError) as raised:
                    self.merge_stale_paths(script, current, self.source_dir / "target-home")
                self.assertEqual(1, raised.exception.returncode)
                self.assertIn(
                    "cannot rewrite projects in the current file without changing its other settings",
                    raised.exception.stderr,
                )
                self.assertEqual("", raised.exception.stdout)

    def test_project_trust_is_kept_and_reported_when_its_path_cannot_be_checked(self) -> None:
        if os.geteuid() == 0:
            self.skipTest("root reads through directory permissions")
        locked = self.source_dir / "locked"
        hidden = locked / "repo"
        hidden.mkdir(parents=True)
        locked.chmod(0)
        try:
            result = self.merge_stale_paths(
                MERGE_SCRIPT,
                f'[projects.{json.dumps(str(hidden))}]\ntrust_level = "trusted"\n',
                self.source_dir / "target-home",
            )
        finally:
            locked.chmod(0o755)

        self.assertEqual(tomllib.loads(result.stdout)["projects"], {str(hidden): {"trust_level": "trusted"}})
        self.assertIn(str(hidden), result.stderr)

    def test_hook_trust_for_a_hooks_file_that_no_longer_exists_is_dropped_by_every_modify_script(self) -> None:
        home = self.source_dir / "target-home"
        present = self.source_dir / "work/repo/.codex/hooks.json"
        present.parent.mkdir(parents=True)
        present.write_text('{"hooks": {}}')
        gone = self.source_dir / "work/retired/.codex/hooks.json"
        plugin = "example@example-market:hooks/hooks.json:stop:0:0"
        state = (f"{present}:stop:0:0", f"{gone}:stop:0:0", plugin)
        current = "[hooks.state]\n\n" + "".join(
            f'[hooks.state.{json.dumps(key)}]\ntrusted_hash = "sha256:operator"\n\n' for key in state
        )
        # A profile also copies the base config's hook trust; an absent hooks file there must not come back.
        (home / ".codex").mkdir(parents=True)
        (home / ".codex/config.toml").write_text(current)
        for script in sorted((ROOT / "home/dot_codex").glob("modify_*config.toml")):
            with self.subTest(script=script.name):
                result = self.merge_stale_paths(script, current, home)

                merged = tomllib.loads(result.stdout)["hooks"]["state"]
                self.assertIn(f"{present}:stop:0:0", merged)
                self.assertIn(plugin, merged)
                self.assertNotIn(f"{gone}:stop:0:0", merged)


if __name__ == "__main__":
    unittest.main()
