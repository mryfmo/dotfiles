"""The kit's rendered DeepSeek harness profile under home/dot_dsh/profiles/thak (regime-cutover U172).

The patch carries a `!!js` tag that plain YAML does not load, so the tests read it as text and compare it with the
manifest's `model_profiles.<profile>.dsh` entries and the asset pin, read through the chezmoi template renderer
(no PyYAML under make unit-test).
"""

from __future__ import annotations

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
from test_generate_agent_configs import load_manifest_fixture

ID_LINE = re.compile(r"^(\s*)- id: (\S+)$")


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


def nested_ids(block: str, parent: str) -> list[str]:
    """The `- id:` values listed under the `parent:` key of a block, until the indentation returns to the key's."""
    found: list[str] = []
    indent = None
    for line in block.splitlines():
        if indent is None:
            if line.strip() == parent:
                indent = len(line) - len(line.lstrip())
            continue
        if line.strip() and len(line) - len(line.lstrip()) <= indent:
            break
        match = ID_LINE.match(line)
        if match:
            found.append(match[2])
    return found


class DshProfileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = Path(tempfile.mkdtemp(prefix="dsh-profile-test-"))
        cls.manifest = load_manifest_fixture(cls.temp_dir)
        cls.patch = (PROFILE_DIR / "cordis.patch.yml").read_text()
        cls.package = json.loads((PROFILE_DIR / "package.json").read_text())
        cls.rows = rows(cls.patch)
        cls.dsh = {name: profile["dsh"] for name, profile in cls.manifest["model_profiles"].items()}

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.temp_dir)

    def test_the_session_log_upload_is_off(self) -> None:
        self.assertIn("- id: session-log-deepseek\n  config:\n    enabled: false\n", self.patch)

    def test_the_provider_models_are_the_six_profiles_dsh_models_and_every_route_is_ollama_cloud(self) -> None:
        self.assertEqual(6, len(self.dsh))
        self.assertEqual({"ollama-cloud"}, {entry["route"] for entry in self.dsh.values()})
        listed = nested_ids(self.rows["id: llm-pi-ai"], "models:")
        self.assertEqual(sorted(listed), listed, "the model ids are sorted")
        self.assertEqual({entry["model"] for entry in self.dsh.values()}, set(listed))

    def test_ollama_cloud_is_the_only_provider_and_the_default_route(self) -> None:
        providers = self.rows["id: llm-pi-ai"]
        keys = re.findall(r"^      ([A-Za-z0-9_-]+):$", providers, re.MULTILINE)
        self.assertEqual(["ollama-cloud"], keys)
        self.assertIn("        baseURL: https://ollama.com/v1\n", providers)
        self.assertIn("        api: openai-responses\n", providers)

    def test_the_official_deepseek_api_rows_are_disabled_and_no_official_route_is_named(self) -> None:
        self.assertNotIn("api.deepseek.com", self.patch)
        self.assertNotIn("deepseek-official", self.patch)
        for row in ("id: llm-deepseek", "id: llm-deepseek-account"):
            self.assertEqual("  disabled: true\n", self.rows[row], row)

    def test_the_claude_hooks_plugin_is_inserted_and_the_package_pins_the_bundles_and_the_plugin(self) -> None:
        inserted = self.rows["insert:"]
        self.assertIn("      name: '@deepseek-ai/dsh-hooks-claude-code'\n", inserted)
        config_path = re.search(r"^\s*configPath: (.*)$", inserted, re.MULTILINE)
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
        self.assertEqual(
            {"@deepseek-ai/dsh-hooks-claude-code": pin.removeprefix("dsh-v")}, self.package["dependencies"]
        )

    def test_the_harness_sandbox_row_is_disabled_by_id(self) -> None:
        self.assertIn("- id: bash-sandbox\n  disabled: true\n", self.patch)
        self.assertNotIn("dsh-bash-sandbox", self.patch)


if __name__ == "__main__":
    unittest.main()
