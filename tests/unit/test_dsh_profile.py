"""The kit's rendered DeepSeek harness profile under home/dot_dsh/profiles/thak (regime-cutover U172, U227b).

The patch carries a `!!js` tag that plain YAML does not load, so the tests read it as text and compare it with the
manifest's `model_profiles.<profile>.dsh` entries and the asset pin, read through the chezmoi template renderer
(no PyYAML under make unit-test). The profile points the agent at the operator's Claude login: the dsh-omp-gateway
plugin row over a child `omp auth-gateway stdio`, the agent-default-model row on its provider, and no API key.
"""

from __future__ import annotations

import contextlib
import copy
import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILE_DIR = ROOT / "home/dot_dsh/profiles/thak"

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from test_generate_agent_configs import load_generator, load_manifest_fixture

GATEWAY_PLUGIN = "dsh-omp-gateway"
PROVIDER = "claude-bridge"


def rows(patch: str) -> dict[str, str]:
    """Each top-level `- id:` row of the patch with the text of its block (up to the next top-level row)."""
    blocks: dict[str, list[str]] = {}
    current = None
    for line in patch.splitlines():
        if line.startswith("#"):
            continue
        if line.startswith("- "):
            current = line.removeprefix("- ")
            blocks[current] = []
        elif current is not None:
            blocks[current].append(line)
    return {key: "\n".join(lines) + "\n" for key, lines in blocks.items()}


def inserted(block: str) -> dict[str, str]:
    """The plugins of an `insert:` block by id, each with the text of its entry."""
    entries: dict[str, list[str]] = {}
    current = None
    for line in block.splitlines():
        match = re.match(r"^    - id: (\S+)$", line)
        if match:
            current = match[1]
            entries[current] = []
        elif current is not None:
            entries[current].append(line)
    return {key: "\n".join(lines) + "\n" for key, lines in entries.items()}


def items_under(block: str, key: str) -> list[str]:
    """The `- item` values listed under the `key:` line of a block, until the indentation returns to the key's."""
    found: list[str] = []
    indent = None
    for line in block.splitlines():
        if indent is None:
            if line.strip() == key:
                indent = len(line) - len(line.lstrip())
            continue
        if line.strip() and len(line) - len(line.lstrip()) <= indent:
            break
        if line.strip().startswith("- "):
            found.append(line.strip().removeprefix("- "))
    return found


class DshProfileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = Path(tempfile.mkdtemp(prefix="dsh-profile-test-"))
        cls.manifest = load_manifest_fixture(cls.temp_dir)
        cls.patch = (PROFILE_DIR / "cordis.patch.yml").read_text()
        cls.package = json.loads((PROFILE_DIR / "package.json").read_text())
        cls.rows = rows(cls.patch)
        cls.plugins = inserted(cls.rows["insert:"])
        cls.dsh = {name: profile["dsh"] for name, profile in cls.manifest["model_profiles"].items()}

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.temp_dir)

    def test_the_session_log_upload_is_off(self) -> None:
        self.assertIn("- id: session-log-deepseek\n  config:\n    enabled: false\n", self.patch)

    def test_the_gateway_row_runs_the_login_command_and_lists_the_six_profiles_dsh_models_under_the_provider(
        self,
    ) -> None:
        self.assertEqual(6, len(self.dsh))
        self.assertEqual({"omp-gateway"}, {entry["route"] for entry in self.dsh.values()})
        gateway = self.plugins["omp-gateway"]
        self.assertIn(f"      name: {GATEWAY_PLUGIN}\n", gateway)
        self.assertIn("        command: omp\n", gateway)
        self.assertEqual(["auth-gateway", "stdio"], items_under(gateway, "args:"))
        self.assertEqual([PROVIDER], items_under(gateway, "providers:"))
        listed = items_under(gateway, "models:")
        self.assertEqual(sorted(listed), listed, "the model ids are sorted")
        self.assertEqual({f"{PROVIDER}/{entry['model']}" for entry in self.dsh.values()}, set(listed))
        # The plugin's default env list carries USER, which the bridge needs to reach the login; a row that narrows
        # it breaks the login, so the kit sets none.
        self.assertNotRegex(gateway, r"^\s*env:", "the gateway row leaves env to the plugin default")

    def test_the_default_model_is_the_interactive_profiles_dsh_model_on_the_gateway_provider(self) -> None:
        tier = self.manifest["interactive_profile"]
        self.assertEqual(1, self.patch.count("- id: agent-default-model\n"))
        self.assertEqual(
            f"  config:\n    provider: {PROVIDER}\n    model: {self.dsh[tier]['model']}\n",
            self.rows["id: agent-default-model"],
        )
        self.assertIn(f"{PROVIDER}/{self.dsh[tier]['model']}", items_under(self.plugins["omp-gateway"], "models:"))

    def test_no_api_key_and_no_ollama_route_stands_in_the_rendered_files(self) -> None:
        for name, text in (("cordis.patch.yml", self.patch), ("package.json", json.dumps(self.package))):
            with self.subTest(file=name):
                self.assertNotRegex(text, r"(?i)ollama|apiKeyEnv|api[_-]?key|baseURL")
        self.assertNotIn("llm-pi-ai", self.patch)

    def test_the_official_deepseek_api_rows_are_disabled_and_no_official_route_is_named(self) -> None:
        self.assertNotIn("api.deepseek.com", self.patch)
        self.assertNotIn("deepseek-official", self.patch)
        for row in ("id: llm-deepseek", "id: llm-deepseek-account"):
            self.assertEqual("  disabled: true\n", self.rows[row], row)

    def test_the_base_rows_that_read_a_deepseek_api_key_are_disabled_by_id(self) -> None:
        # The base bundle's web search and web API rows carry `apiKeyEnv: DEEPSEEK_API_KEY` (U288 row d20), an API-key
        # route the login-only decision admits nowhere, so the profile turns them off by id like the adapters above.
        for row in ("id: web-search-deepseek", "id: web-deepseek-api"):
            self.assertEqual("  disabled: true\n", self.rows[row], row)

    def test_the_claude_hooks_plugin_is_inserted_and_the_package_pins_the_bundles_and_links_both_plugins(self) -> None:
        hooks = self.plugins["hooks-claude-code"]
        self.assertIn("      name: '@deepseek-ai/dsh-hooks-claude-code'\n", hooks)
        config_path = re.search(r"^\s*configPath: (.*)$", hooks, re.MULTILINE)
        self.assertIsNotNone(config_path)
        # An absolute path: HOME, then a single-quoted literal that starts at `/` (a suffix test alone passed a
        # relative literal).
        home, _, literal = config_path[1].rpartition(" + ")
        self.assertEqual("!!js process.env.HOME", home, config_path[1])
        self.assertTrue(literal.startswith("'/") and literal.endswith("/.claude/settings.json'"), literal)
        pin = self.manifest["assets"]["deepseek-harness"]["pin"]
        self.assertTrue(pin.startswith("dsh-v"), pin)
        self.assertEqual("thak", self.package["name"])
        self.assertIs(True, self.package["private"])
        self.assertEqual(
            {"manifestVersion": 1, "profile": {"bundles": ["@deepseek-ai/dsh-base", "@deepseek-ai/dsh-headless"]}},
            self.package["dsh"],
        )
        # The link is relative to the profile directory: ~/.dsh/profiles/thak to ~/.dsh/plugins/omp-gateway.
        self.assertEqual(
            {
                "@deepseek-ai/dsh-hooks-claude-code": pin.removeprefix("dsh-v"),
                GATEWAY_PLUGIN: "link:../../plugins/omp-gateway",
            },
            self.package["dependencies"],
        )

    def test_the_harness_sandbox_row_is_disabled_by_id(self) -> None:
        self.assertIn("- id: bash-sandbox\n  disabled: true\n", self.patch)
        self.assertNotIn("dsh-bash-sandbox", self.patch)

    def test_the_validator_refuses_an_ollama_form_model_id_and_the_withdrawn_route(self) -> None:
        generator = load_generator()
        refused = (
            ({"model": "deepseek-v4-pro:0813", "route": "omp-gateway"}, "deep.dsh.model"),
            ({"model": "claude-bridge/claude-opus-5-5", "route": "omp-gateway"}, "deep.dsh.model"),
            ({"model": "claude-opus-5-5", "route": "ollama-cloud"}, "deep.dsh.route"),
        )
        for entry, key in refused:
            with self.subTest(entry=entry):
                manifest = copy.deepcopy(self.manifest)
                manifest["model_profiles"]["deep"]["dsh"] = entry
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    generator.model_profiles(manifest)
                self.assertIn(f"model profile {key}", stderr.getvalue())
        generator.model_profiles(self.manifest)

    def test_the_renderer_fails_when_the_interactive_profile_names_no_dsh_model(self) -> None:
        generator = load_generator()
        manifest = copy.deepcopy(self.manifest)
        del manifest["model_profiles"][manifest["interactive_profile"]]["dsh"]
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            generator.render_dsh_profile_patch(manifest)
        self.assertIn(f"interactive_profile {manifest['interactive_profile']!r} names no dsh model", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
