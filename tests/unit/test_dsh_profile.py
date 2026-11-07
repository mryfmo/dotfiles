"""The kit's rendered DeepSeek harness profiles under home/dot_dsh/profiles/thak (regime-cutover U172, U227b) and
home/dot_dsh/profiles/router (U317, the dsh-superagent Router).

The patch carries a `!!js` tag that plain YAML does not load, so the tests read it as text and compare it with the
manifest's `model_profiles.<profile>.dsh` entries and the asset pin, read through the chezmoi template renderer
(no PyYAML under make unit-test). The profile points the agent at the operator's Claude login: the dsh-omp-gateway
plugin row over a child `omp auth-gateway stdio`, the agent-default-model row on its provider, and no API key.
"""

from __future__ import annotations

import contextlib
import copy
import importlib.util
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


ROUTER_DIR = ROOT / "home/dot_dsh/profiles/router"


def sandbox_rows(patch: str) -> list[list[str]]:
    """Every `- id: bash-sandbox` row of the patch, at any depth, with the lines of its block (until the next item at
    the same indentation or a shallower line)."""
    lines = patch.splitlines()
    found: list[list[str]] = []
    for index, line in enumerate(lines):
        if line.strip() != "- id: bash-sandbox":
            continue
        indent = len(line) - len(line.lstrip())
        block = [line]
        for later in lines[index + 1 :]:
            depth = len(later) - len(later.lstrip())
            if depth < indent or (depth == indent and later.lstrip().startswith("- ")):
                break
            block.append(later)
        found.append(block)
    return found


class DshRouterProfileTest(unittest.TestCase):
    """The router profile: the thak rows, the loopback bind, the stateDir under the Router state root, every
    bash-sandbox row disabled, no API key, the GitHub Source row as data, and the accept-mode allowlist."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = Path(tempfile.mkdtemp(prefix="dsh-router-test-"))
        cls.manifest = load_manifest_fixture(cls.temp_dir)
        cls.patch = (ROUTER_DIR / "cordis.patch.yml").read_text()
        cls.package = json.loads((ROUTER_DIR / "package.json").read_text())
        cls.thak = (PROFILE_DIR / "cordis.patch.yml").read_text()
        cls.rows = rows(cls.patch)
        cls.plugins = inserted(cls.rows["insert:"])
        cls.asset = cls.manifest["assets"]["dsh-superagent"]

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.temp_dir)

    def test_the_patch_names_observe_and_the_source_repository_from_the_manifest(self) -> None:
        github = self.asset["sources"]["github"]
        self.assertEqual("observe", github["accept_mode"])
        self.assertRegex(github["repository"], r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
        self.assertIn(f"repository {github['repository']}, accept_mode\n# observe", self.patch)
        self.assertIn(f"ladder row {github['accept_mode_row']}", self.patch)
        self.assertIn("the allowed list is empty", self.patch)
        self.assertIn(f"pin {self.asset['pin']}", self.patch)

    def test_the_session_log_upload_is_off_and_the_thak_rows_are_carried(self) -> None:
        self.assertIn("- id: session-log-deepseek\n  config:\n    enabled: false\n", self.patch)
        for row in ("id: llm-deepseek", "id: llm-deepseek-account", "id: web-search-deepseek", "id: web-deepseek-api"):
            self.assertEqual("  disabled: true\n", self.rows[row], row)
        tier = self.manifest["interactive_profile"]
        self.assertEqual(
            f"  config:\n    provider: {PROVIDER}\n    model: {self.manifest['model_profiles'][tier]['dsh']['model']}\n",
            self.rows["id: agent-default-model"],
        )
        # The gateway insert is the thak profile's, rendered from the same manifest values.
        self.assertEqual(inserted(rows(self.thak)["insert:"])["omp-gateway"], self.plugins["omp-gateway"])
        self.assertNotIn("hooks-claude-code", self.patch, "the Router mounts no Claude Code hooks")

    def test_every_bash_sandbox_row_is_disabled(self) -> None:
        blocks = sandbox_rows(self.patch)
        # The base row and one inside each of the two presets (the shell groups).
        self.assertEqual(3, len(blocks), [block[0] for block in blocks])
        for block in blocks:
            self.assertIn("disabled: true", [line.strip() for line in block], block)
        self.assertEqual(2, self.patch.count("name: '@deepseek-ai/dsh-bash-sandbox'"))
        for preset in ("dsh-superagent-worker-preset", "dsh-superagent-router-preset"):
            self.assertIn(f"- id: {preset}\n  name: '@deepseek-ai/dsh-agent-preset'\n  config:\n", self.patch)

    def test_no_api_key_row_is_enabled_and_no_model_id_outside_model_profiles(self) -> None:
        for name, text in (("cordis.patch.yml", self.patch), ("package.json", json.dumps(self.package))):
            with self.subTest(file=name):
                self.assertNotRegex(text, r"(?i)ollama|apiKeyEnv|api[_-]?key|baseURL|api\.deepseek\.com")
        models = {entry["dsh"]["model"] for entry in self.manifest["model_profiles"].values()}
        for line in self.patch.splitlines():
            if "model:" in line and not line.lstrip().startswith("#"):
                self.assertIn(line.split("model:")[1].strip(), models, line)

    def test_the_webserver_binds_loopback_and_the_state_dir_is_under_the_dsh_write_root(self) -> None:
        self.assertEqual("  config:\n    host: 127.0.0.1\n    port: 3082\n", self.rows["id: webserver"])
        # verdicts/U317 P1 :30: the state was under ~/.local/state, outside every dsh-role write root. The one write
        # root the role grants beyond its slots is DSH_HOME (hcom-seat seat_write_roots), exported into the dsh child
        # as DSH_HOME, so the path is that variable and a child of it, and nothing under HOME, .local or .omp.
        row = self.rows["id: dsh-superagent"]
        self.assertEqual("  config:\n    stateDir: !!js process.env.DSH_HOME + '/router-state'\n", row)
        self.assertEqual(1, self.patch.count("router-state"))
        self.assertNotIn("dsh-router", self.patch)
        for outside in ("process.env.HOME", ".local/state", ".omp", "/tmp"):
            self.assertNotIn(outside, row, f"the state lies under a path outside DSH_HOME: {outside}")
        self.assertEqual(
            'dsh) extra=("${dsh_home}" "${HOME}/.omp/profiles/$1" "${HOME}/.omp/run") ;;',
            next(
                line.strip()
                for line in (ROOT / "scripts/orchestrator/hcom-seat").read_text().splitlines()
                if line.strip().startswith("dsh) extra=(")
            ),
            "the dsh role's write roots beyond its slots: DSH_HOME first",
        )

    def test_the_package_links_the_bundle_and_the_gateway_over_the_web_profiles_bundles(self) -> None:
        self.assertEqual("router", self.package["name"])
        self.assertIs(True, self.package["private"])
        self.assertEqual(
            {"manifestVersion": 1, "profile": {"bundles": ["@deepseek-ai/dsh-base", "@deepseek-ai/dsh-web-app"]}},
            self.package["dsh"],
        )
        self.assertEqual(
            {"dsh-superagent": "link:../../plugins/dsh-superagent", GATEWAY_PLUGIN: "link:../../plugins/omp-gateway"},
            self.package["dependencies"],
        )
        self.assertEqual("~/.dsh/plugins/dsh-superagent", self.asset["install_path"])
        self.assertEqual("scripts/update-agent-assets.sh#update_dsh_superagent", self.asset["installer"])

    def test_the_presets_restate_the_archives_rows_with_the_sandbox_off(self) -> None:
        # The names upstream's tests/bundle-patch.spec.ts asserts for each preset, and the ones it refuses.
        generator = load_generator()
        presets = generator.dsh_superagent_presets()

        def flat(entries: list[dict]) -> list[dict]:
            return [row for entry in entries for row in [entry, *(flat(entry["config"]) if entry.get("group") else [])]]

        worker = flat(presets["dsh-superagent-worker-preset"]["plugins"])
        router = flat(presets["dsh-superagent-router-preset"]["plugins"])
        names = lambda entries: [row["name"] for row in entries]  # noqa: E731
        for name in (
            "@deepseek-ai/dsh-tool-fs",
            "@deepseek-ai/dsh-tool-fs-search",
            "@deepseek-ai/dsh-tool-bash",
            "@deepseek-ai/dsh-tool-skill",
            "@deepseek-ai/dsh-tool-todo",
            "@deepseek-ai/dsh-tool-subagent",
            "@deepseek-ai/dsh-tool-subagent-control",
            "@deepseek-ai/dsh-compaction-basic",
            "@deepseek-ai/dsh-compaction-tool-result-pruner",
            "@deepseek-ai/dsh-agent-instructions",
        ):
            self.assertIn(name, names(worker))
        for name in ("@deepseek-ai/dsh-tool-subagent", "@deepseek-ai/dsh-tool-web", "@deepseek-ai/dsh-tool-fs-search"):
            self.assertNotIn(name, names(router))
        self.assertEqual(
            [{"write": False, "edit": False}], [r["config"] for r in router if r["name"] == "@deepseek-ai/dsh-tool-fs"]
        )
        for entries in (worker, router):
            sandbox = [row for row in entries if row["name"] == "@deepseek-ai/dsh-bash-sandbox"]
            self.assertEqual([True], [row["disabled"] for row in sandbox])
            self.assertEqual([{"timeoutMs": 5000, "maxTimeoutMs": 5000}], [row["config"] for row in sandbox])
            pwsh = [row for row in entries if row["name"] == "@deepseek-ai/dsh-pwsh-sandbox"]
            self.assertEqual(["process.platform !== 'win32'"], [row["disabled"].expression for row in pwsh])
        self.assertEqual(
            (90, 91),
            (presets["dsh-superagent-worker-preset"]["order"], presets["dsh-superagent-router-preset"]["order"]),
        )

    def test_the_accept_mode_allowlist_refuses_auto_without_its_row_and_unknown_keys_by_name(self) -> None:
        generator = load_generator()
        base = copy.deepcopy(self.manifest)
        self.assertTrue(generator.render_dsh_router_profile(base), "the real manifest renders")

        def refused(mutate, expected: str) -> None:
            manifest = copy.deepcopy(base)
            mutate(manifest["assets"]["dsh-superagent"]["sources"]["github"])
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                generator.render_dsh_router_profile(manifest)
            self.assertIn(expected, stderr.getvalue())

        refused(lambda row: row.update(accept_mode="auto"), "accept_mode auto needs accept_mode_auto_row")
        refused(
            lambda row: row.update(accept_mode="always"),
            "accept_mode 'always' is not one of ['off', 'observe', 'auto']",
        )
        refused(lambda row: row.update(allowed="someone"), "unknown key(s) ['allowed']")
        refused(lambda row: row.update(repository="dotfiles"), "repository 'dotfiles' is not owner/name")
        refused(
            lambda row: row.update(accept_mode_row="yesterday"),
            "accept_mode_row 'yesterday' is not a decisions.tsv timestamp",
        )
        manifest = copy.deepcopy(base)
        manifest["assets"]["dsh-superagent"]["sources"]["github"].update(
            accept_mode="auto", accept_mode_auto_row="2026-11-08T00:00:00Z"
        )
        outputs = generator.render_dsh_router_profile(manifest)
        patch = outputs[generator.ROOT / "home/dot_dsh/profiles/router/cordis.patch.yml"]
        self.assertIn(
            "accept_mode\n# auto (M-18 ladder row 2026-11-06T23:24:00Z, accept_mode_auto_row 2026-11-08T00:00:00Z)",
            patch,
        )

    def test_the_validator_refuses_sources_outside_the_asset_unknown_keys_and_auto_without_its_row(self) -> None:
        # The validator's own allowlist (scripts/validate-agent-assets.py validate_asset_sources), not the renderer's:
        # the real asset passes; `sources` under another asset, an unknown Source, an unknown key, a repository that is
        # not owner/name and `auto` without accept_mode_auto_row are each a refusal naming the key.
        spec = importlib.util.spec_from_file_location(
            "validate_agent_assets", ROOT / "scripts/validate-agent-assets.py"
        )
        assert spec and spec.loader
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        validator.validate_asset_sources("dsh-superagent", copy.deepcopy(self.asset))

        def refused(name: str, mutate, expected: str) -> None:
            asset = copy.deepcopy(self.asset)
            mutate(asset)
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                validator.validate_asset_sources(name, asset)
            self.assertIn(expected, stderr.getvalue())

        refused(
            "deepseek-harness",
            lambda asset: None,
            "assets.deepseek-harness.sources: only assets.dsh-superagent carries Source rows",
        )
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"].update(feishu={}),
            "assets.dsh-superagent.sources.feishu is not a Source the kit renders",
        )
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"]["github"].update(allowed="x"),
            "has unknown key(s) ['allowed']",
        )
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"]["github"].update(repository="dotfiles"),
            "repository 'dotfiles' is not owner/name",
        )
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"]["github"].update(accept_mode="always"),
            "accept_mode 'always' is not one of ['off', 'observe', 'auto']",
        )
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"]["github"].update(accept_mode="auto"),
            "accept_mode auto needs accept_mode_auto_row beside accept_mode_row",
        )

    def test_the_installer_pins_are_rendered_from_the_asset(self) -> None:
        # scripts/lib/installer-pins.sh is generated: the two constants the updater reads are the asset's pin and
        # sha256, never a hand-written value (make render-check holds the file to the generator's output).
        pins = (ROOT / "scripts/lib/installer-pins.sh").read_text()
        self.assertIn(f'\nDSH_SUPERAGENT_COMMIT="{self.asset["pin"]}"\n', pins)
        self.assertIn(f'\nDSH_SUPERAGENT_SHA256="{self.asset["sha256"]}"\n', pins)
        self.assertRegex(self.asset["pin"], r"^[0-9a-f]{40}$")
        self.assertRegex(self.asset["sha256"], r"^[0-9a-f]{64}$")

    def test_the_docs_start_the_router_through_hcom_seat_and_build_inside_srt(self) -> None:
        # docs/deepseek-harness.md names the one launch (hcom-seat under srt) and the build's containment, never the
        # archive's tmux launcher or an uncontained pnpm.
        docs = (ROOT / "docs/deepseek-harness.md").read_text()
        self.assertIn("`hcom-seat dsh --profile router -- --no-open` starts the Router under srt", docs)
        self.assertIn("`srt --settings` invocation whose writes are the new tree and", docs)
        self.assertIn("`$DSH_HOME/.pnpm-store`", docs)
        self.assertIn("`stateDir` at `$DSH_HOME/router-state`", docs)
        self.assertNotIn("tmux", docs)
        self.assertNotIn("scripts/dsh-superagent", docs)
        self.assertNotIn("dsh-router", docs)


if __name__ == "__main__":
    unittest.main()
