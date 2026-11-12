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
import hashlib
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


class DshRouterProfileTest(unittest.TestCase):
    """The router profile: the thak-form rows, the loopback bind, the stateDir under the Router state root, the base
    bundle's bash-sandbox row left on as the shell provider the presets require (srt the one boundary) and no preset
    restated, no API key, the GitHub Source row as data, and the accept-mode allowlist."""

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

    def observe_manifest(self) -> dict:
        """The manifest with its Source row in the observe form (accept_mode observe, no accept_mode_auto_row, allowed
        []): the committed row is auto since U469 (the decisions row 2026-11-12T00:08:25Z), so the observe-form proofs
        and the refusals that presume observe run against this mutated copy."""
        manifest = copy.deepcopy(self.manifest)
        row = manifest["assets"]["dsh-superagent"]["sources"]["github"]
        row.update(accept_mode="observe", allowed=[])
        row.pop("accept_mode_auto_row", None)
        return manifest

    def test_the_patch_names_auto_its_two_rows_the_allowed_login_and_the_source_repository_from_the_manifest(
        self,
    ) -> None:
        # U469: the second rung. The manifest row is auto by the decisions row 2026-11-12T00:08:25Z (phase M-18, the
        # row router-settings-apply admits auto by), and the identity set is the operator's login; the patch comment
        # the generator renders names the mode, both rows and the list, each from the manifest.
        github = self.asset["sources"]["github"]
        self.assertEqual("auto", github["accept_mode"], "the kit holds auto (U469)")
        self.assertRegex(github["repository"], r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
        self.assertEqual("2026-11-12T00:08:25Z", github["accept_mode_auto_row"], "the decisions row the operator wrote")
        self.assertNotEqual(github["accept_mode_row"], github["accept_mode_auto_row"], "two rows, the ladder's rungs")
        self.assertEqual(["mryfmo"], github["allowed"], "the committed identity set is the operator's login (U469)")
        self.assertIn(
            f"repository {github['repository']}, accept_mode\n# auto (M-18 ladder row {github['accept_mode_row']}, "
            f"accept_mode_auto_row {github['accept_mode_auto_row']}); the allowed list: {', '.join(github['allowed'])}.",
            self.patch,
        )
        self.assertNotIn("the allowed list is empty", self.patch)
        self.assertIn(f"pin {self.asset['pin']}", self.patch)

    def test_the_source_comment_names_the_settings_lever_and_the_plugin_row_admits_state_dir_alone(self) -> None:
        # U353: the Source values are no plugin config (upstream src/deployment.ts:33-44 refuses `repository` on the
        # plugin row, naming the Source as where it moved), so the rendered comment says where they live now (the
        # Router's settings store, written through the Management API by `router-settings-apply`), which wrapper the
        # Source's `cli` names (`router-gh`, `GH_CONFIG_DIR` under `$DSH_HOME/router-credentials`) and the one launch
        # (`hcom-seat router -- --no-open`); the plugin row carries `stateDir` and no live key beyond it.
        comments = "\n".join(line for line in self.patch.splitlines() if line.startswith("#"))
        self.assertIn("`router-settings-apply`", comments)
        self.assertIn("`router-gh`", comments)
        self.assertIn("$DSH_HOME/router-credentials", comments)
        self.assertIn("`hcom-seat router -- --no-open`", comments)
        self.assertNotIn("hcom-seat dsh --profile router", comments)
        row = self.rows["id: dsh-superagent"]
        self.assertEqual("  config:\n    stateDir: !!js process.env.DSH_HOME + '/router-state'\n", row)
        for key in ("repository", "cli", "accept_mode", "mode", "observePulls", "eval", "enabled"):
            self.assertNotRegex(row, rf"^\s+{key}:", key)

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

    def test_the_router_keeps_the_base_bundles_bash_sandbox_row_on(self) -> None:
        """The inverse of the thak profile's `test_the_harness_sandbox_row_is_disabled_by_id` (d15): `bash-sandbox` is
        the base bundle's only shell provider whose executor carries a `sandboxMode`, which upstream's permission
        presets require to activate (`permission-presets` lib/index.js:177), so the Router keeps it mounted. Under the
        superagent's presets it runs in `danger-full-access`, the mode without sandbox-exec, and sandbox-exec cannot
        apply inside srt on macOS anyway (measured 2026-11-09), so the seat's one boundary is srt (U406, U406b). The
        thak profile's own row (its turn needs no shell) is unchanged."""
        self.assertNotIn("id: bash-sandbox", self.rows, sorted(self.rows))
        # U466: the one `bash-sandbox` the patch names is the worker preset's nested row, as upstream ships it (the
        # win32 gate, never `disabled: true`); no top-level row and no disabled sandbox row of any kind (U406).
        self.assertNotRegex(self.patch, r"bash-sandbox[^\n]*\n *disabled: true")
        self.assertEqual(
            [
                "          - id: bash-sandbox\n            name: '@deepseek-ai/dsh-bash-sandbox'\n            disabled: !!js"
            ],
            [
                match[0]
                for match in re.finditer(
                    r"^ *- id: bash-sandbox\n *name: [^\n]*\n *disabled: !!js", self.patch, re.MULTILINE
                )
            ],
        )
        self.assertEqual(1, self.patch.count("bash-sandbox\n"), self.patch)
        self.assertIn("- id: bash-sandbox\n  disabled: true\n", self.thak, "d15's thak row stands")

    def test_the_worker_preset_row_is_the_kits_own_row_set_on_the_acp_provider_and_the_router_preset_is_not_restated(
        self,
    ) -> None:
        # Upstream's bundle layer (~/.dsh/plugins/dsh-superagent/cordis.patch.yml) inserts the two agent presets; the kit
        # restated them (U317) only to turn their bash-sandbox rows off, and U406 removed both once the sandbox stayed
        # on. U466 (U437's work, row i8) brings one back as the kit's own row set: the worker preset's nested
        # `tool-subagent` keeps `provider: spawn` in upstream's layer, the patch algorithm reaches no nested row by id
        # and replaces a row's config whole (measured, /tmp/u466/prototype.txt), so the kit addresses the preset row
        # `dsh-superagent-worker-preset` with a config of its own whose delegation row is on the ACP provider with the
        # base row's three keys. The router preset stays upstream's.
        preset = self.rows["id: dsh-superagent-worker-preset"]
        self.assertNotIn("id: dsh-superagent-router-preset", self.rows, sorted(self.rows))
        self.assertTrue(preset.startswith("  config:\n    id: dsh-superagent-worker\n"), preset)
        self.assertNotIn("name: '@deepseek-ai/dsh-agent-preset'", preset, "addressed by id, the bundle's name")
        self.assertIn(
            "          - id: tool-subagent\n"
            "            name: '@deepseek-ai/dsh-tool-subagent'\n"
            "            config:\n"
            "              provider: acp\n"
            "              toolName: subagent\n"
            "              maxDepth: provider-managed\n",
            preset,
        )
        self.assertNotIn("provider: spawn", self.patch)
        self.assertNotIn("disabled: true", preset, "the preset's sandbox rows stay as upstream ships them")
        self.assertIn("disabled: !!js process.platform === 'win32'", preset, "the win32 gates as upstream's")
        self.assertNotIn("preset", self.thak)

    def test_the_rows_are_the_thak_form_rows_the_webserver_the_state_dir_the_subagent_tool_and_the_inserts_in_order(
        self,
    ) -> None:
        self.assertEqual(
            [
                "id: session-log-deepseek",
                "id: llm-deepseek",
                "id: llm-deepseek-account",
                "id: web-search-deepseek",
                "id: web-deepseek-api",
                "id: agent-default-model",
                "id: webserver",
                "id: dsh-superagent",
                "id: tool-subagent",
                "id: dsh-superagent-worker-preset",
                "insert:",
            ],
            list(self.rows),
        )
        # U434: the subagent tool runs on the ACP provider the insert mounts; the gateway insert comes first. U434c: the
        # web-app bundle ships the row disabled, so the kit's row enables it beside its config.
        self.assertEqual(
            "  disabled: false\n  config:\n    provider: acp\n    toolName: subagent\n    maxDepth: provider-managed\n",
            self.rows["id: tool-subagent"],
        )
        self.assertEqual(["omp-gateway", "subagent-acp"], list(self.plugins))
        self.assertNotIn("subagent-acp", self.thak)
        self.assertNotIn("tool-subagent", self.thak)

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
        # hcom-seat seat_write_roots since U321 (main): the dsh and router rows share one case; row 3 is the held
        # physical DSH_HOME, printed before the omp rows, and the Router's state root is a held row of its own.
        lines = [line.strip() for line in (ROOT / "scripts/orchestrator/hcom-seat").read_text().splitlines()]
        start = lines.index("dsh | router)", lines.index("seat_write_roots() {"))
        block = lines[start : lines.index(";;", start)]
        self.assertIn("home=${dsh_home_phys}", block, "the dsh role's write roots beyond its slots: DSH_HOME first")
        self.assertIn(
            "held=${state_root_phys}", block, "the Router's state root <DSH_HOME>/router-state is a write root"
        )

    def test_the_package_links_the_bundle_and_the_gateway_over_the_web_profiles_bundles(self) -> None:
        self.assertEqual("router", self.package["name"])
        self.assertIs(True, self.package["private"])
        # U404: the composed tree holds the superagent entries only when the plugin is a bundle layer, so the bundle
        # list carries the plugin's name after the Web profile's two, and that name is a key of the package's
        # dependencies (the bundle the profile composes is the one the updater installs).
        bundles = ["@deepseek-ai/dsh-base", "@deepseek-ai/dsh-web-app", "dsh-superagent"]
        self.assertEqual({"manifestVersion": 1, "profile": {"bundles": bundles}}, self.package["dsh"])
        # U434b: the subagent-acp insert's package is a dependency too, linked through dsh/current to the pinned
        # tree's built package, so the deployed profile resolves it without a hand-made link.
        self.assertEqual(
            {
                "dsh-superagent": "link:../../plugins/dsh-superagent",
                GATEWAY_PLUGIN: "link:../../plugins/omp-gateway",
                "@deepseek-ai/dsh-subagent-acp": "link:../../dsh/current/packages/subagent/subagent-acp",
            },
            self.package["dependencies"],
        )
        self.assertIn(
            bundles[2], self.package["dependencies"], "the third bundle is the link: dependency the updater installs"
        )
        self.assertEqual("~/.dsh/plugins/dsh-superagent", self.asset["install_path"])
        self.assertEqual("scripts/update-agent-assets.sh#update_dsh_superagent", self.asset["installer"])

    def test_the_accept_mode_allowlist_refuses_auto_without_its_row_and_unknown_keys_by_name(self) -> None:
        generator = load_generator()
        self.assertTrue(generator.render_dsh_router_profile(copy.deepcopy(self.manifest)), "the real manifest renders")
        # The refusals below presume the observe form (U469: the committed row is auto), a mutated copy.
        base = self.observe_manifest()
        self.assertTrue(generator.render_dsh_router_profile(base), "the observe form renders")

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
        label = "assets.dsh-superagent.sources.github.allowed"
        refused(
            lambda row: row.pop("allowed"),
            f"{label} is missing (the Source's identity set; [] when no sender is listed)",
        )
        refused(lambda row: row.update(allowed="someone"), f"{label} must be a list of sender ids, not str: 'someone'")
        refused(lambda row: row.update(allowed=None), f"{label} must be a list of sender ids, not NoneType: None")
        refused(lambda row: row.update(allowed=[1]), f"{label} must be a list of sender ids, not int: 1")
        refused(
            lambda row: row.update(allowed=["some_one"]),
            f"{label} names 'some_one', which is not a sender id of the form [A-Za-z0-9-]+",
        )
        refused(
            lambda row: row.update(allowed=["someone", "Someone"]),
            f"{label} repeats 'Someone' (GitHub logins that differ by case alone are one login)",
        )
        # U465b (verdict U465-4ae6f8c0 P1 `:516`): the list is written in auto alone; a listed login beside observe
        # or off is a dormant grant (a listed login's mention is explicit in every mode) and the manifest is refused.
        refused(
            lambda row: row.update(allowed=["someone"]),
            f"{label} names ['someone'] while accept_mode is 'observe'; the identity set is written in auto alone, so "
            "the list is [] in off and observe",
        )
        refused(
            lambda row: row.update(accept_mode="off", allowed=["someone"]),
            f"{label} names ['someone'] while accept_mode is 'off'; the identity set is written in auto alone, so "
            "the list is [] in off and observe",
        )
        refused(lambda row: row.update(repository="dotfiles"), "repository 'dotfiles' is not owner/name")
        refused(
            lambda row: row.update(accept_mode_row="yesterday"),
            "accept_mode_row 'yesterday' is not a decisions.tsv timestamp",
        )
        # U465c (verdict U465-db9a5e94 P1 `:517`): the auto row is a row of its own, so the two timestamps differ.
        refused(
            lambda row: row.update(accept_mode="auto", accept_mode_auto_row=row["accept_mode_row"]),
            "accept_mode_auto_row '2026-11-06T23:24:00Z' is the accept_mode_row itself; the ladder's second row is "
            "not its first",
        )
        manifest = copy.deepcopy(base)
        manifest["assets"]["dsh-superagent"]["sources"]["github"].update(
            accept_mode="auto", accept_mode_auto_row="2026-11-08T00:00:00Z", allowed=["someone", "other-one"]
        )
        outputs = generator.render_dsh_router_profile(manifest)
        patch = outputs[generator.ROOT / "home/dot_dsh/profiles/router/cordis.patch.yml"]
        self.assertIn(
            "accept_mode\n# auto (M-18 ladder row 2026-11-06T23:24:00Z, accept_mode_auto_row 2026-11-08T00:00:00Z)",
            patch,
        )
        self.assertIn("the allowed list: someone, other-one.", patch)
        self.assertNotIn("the allowed list is empty", patch)

    def test_the_validator_refuses_sources_outside_the_asset_unknown_keys_a_bad_sender_id_and_auto_without_its_row(
        self,
    ) -> None:
        # The validator's own allowlist (scripts/validate-agent-assets.py validate_asset_sources), not the renderer's:
        # the real asset passes (auto with its row and the operator's login, U469), as does its observe form with the
        # empty identity set, a mutated copy the refusals below start from; `sources` under another asset, an unknown
        # Source, an unknown key, a repository that is not owner/name, an `allowed` that is no list of sender ids
        # (U465: ids `[A-Za-z0-9-]+`, src/sources/github.ts:72, no repeat) and `auto` without accept_mode_auto_row
        # are each a refusal naming the key.
        spec = importlib.util.spec_from_file_location(
            "validate_agent_assets", ROOT / "scripts/validate-agent-assets.py"
        )
        assert spec and spec.loader
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        validator.validate_asset_sources("dsh-superagent", copy.deepcopy(self.asset))
        observe = self.observe_manifest()["assets"]["dsh-superagent"]
        validator.validate_asset_sources("dsh-superagent", copy.deepcopy(observe))
        # A listed identity set is admitted beside auto and its row alone (U465b).
        listed = copy.deepcopy(self.asset)
        listed["sources"]["github"].update(
            accept_mode="auto", accept_mode_auto_row="2026-11-08T00:00:00Z", allowed=["someone", "other-one"]
        )
        validator.validate_asset_sources("dsh-superagent", listed)

        def refused(name: str, mutate, expected: str) -> None:
            asset = copy.deepcopy(observe)
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
            lambda asset: asset["sources"]["github"].update(bots=["x"]),
            "has unknown key(s) ['bots']",
        )
        label = "assets.dsh-superagent.sources.github.allowed"
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"]["github"].pop("allowed"),
            f"{label} is missing (the Source's identity set; [] when no sender is listed)",
        )
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"]["github"].update(allowed="x"),
            f"{label} must be a list of sender ids, not str: 'x'",
        )
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"]["github"].update(allowed=[{"id": "someone"}]),
            f"{label} must be a list of sender ids, not dict: {{'id': 'someone'}}",
        )
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"]["github"].update(allowed=["dependabot[bot]"]),
            f"{label} names 'dependabot[bot]', which is not a sender id of the form [A-Za-z0-9-]+",
        )
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"]["github"].update(allowed=["someone", "SOMEONE"]),
            f"{label} repeats 'SOMEONE' (GitHub logins that differ by case alone are one login)",
        )
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"]["github"].update(allowed=["someone"]),
            f"{label} names ['someone'] while accept_mode is 'observe'; the identity set is written in auto alone, so "
            "the list is [] in off and observe",
        )
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"]["github"].update(accept_mode="off", allowed=["someone"]),
            f"{label} names ['someone'] while accept_mode is 'off'; the identity set is written in auto alone, so "
            "the list is [] in off and observe",
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
        refused(
            "dsh-superagent",
            lambda asset: asset["sources"]["github"].update(
                accept_mode="auto", accept_mode_auto_row=asset["sources"]["github"]["accept_mode_row"]
            ),
            "accept_mode_auto_row '2026-11-06T23:24:00Z' is the accept_mode_row itself; the ladder's second row is "
            "not its first",
        )

    def test_the_generator_renders_the_source_row_as_the_json_the_lever_reads_and_the_index_pins_it(self) -> None:
        """U465c (verdict U465-db9a5e94 P1 `:407`): the lever reads no YAML; the generator (PyYAML, the kit's one YAML
        reader) renders the manifest's Source row into `home/dot_agents/router-source.json`, a managed target chezmoi
        deploys beside the manifest as `~/.agents/router-source.json`, which `make render-check` holds to the manifest
        and the output index lists with its sha256 (the doctor's check of the deployed copy, as for a lever copy). The
        object holds `generated_by` and the row's keys in their fixed order, every one present (U465d:
        `accept_mode_auto_row` null when the manifest omits it); the committed rendering is the auto row of U469 (the
        decisions row 2026-11-12T00:08:25Z, the operator's login listed), the observe form proven on a mutated copy."""
        generator = load_generator()
        path = generator.ROOT / "home/dot_agents/router-source.json"
        outputs = generator.render_router_source(copy.deepcopy(self.manifest))
        self.assertEqual([path], list(outputs))
        rendered = outputs[path]
        github = self.asset["sources"]["github"]
        self.assertEqual(
            {
                "generated_by": generator.GENERATED_HEADER,
                "source": {
                    "repository": github["repository"],
                    "accept_mode": "auto",
                    "accept_mode_row": github["accept_mode_row"],
                    "accept_mode_auto_row": github["accept_mode_auto_row"],
                    "observe_admission": "inferred",
                    "allowed": github["allowed"],
                },
            },
            json.loads(rendered),
        )
        self.assertEqual(
            ["generated_by", "source"], list(json.loads(rendered)), "the top level holds the header and the row alone"
        )
        self.assertEqual(
            ["repository", "accept_mode", "accept_mode_row", "accept_mode_auto_row", "observe_admission", "allowed"],
            list(json.loads(rendered)["source"]),
        )
        self.assertEqual(rendered, (ROOT / "home/dot_agents/router-source.json").read_text(), "the committed copy")
        self.assertTrue(rendered.endswith("\n") and not rendered.endswith("\n\n"))
        index = json.loads((ROOT / "scripts/generated-agent-outputs.json").read_text())
        (entry,) = [entry for entry in index["outputs"] if entry["source"] == "home/dot_agents/router-source.json"]
        self.assertEqual(
            {
                "source": "home/dot_agents/router-source.json",
                "target": ".agents/router-source.json",
                "kind": "file",
                "executable": False,
                "sha256": hashlib.sha256(rendered.encode()).hexdigest(),
            },
            entry,
        )
        self.assertIn(
            {"source": "home/dot_agents", "target": ".agents", "glob": "router-source.json"},
            index["scopes"],
            "a stale rendering is an orphan the generator and the doctor report",
        )
        self.assertIn(("home/dot_agents", "router-source.json"), generator.GENERATED_SCOPES)
        # At auto with its row and two ids, the row carries the sixth key in its place and the ids in order.
        manifest = copy.deepcopy(self.manifest)
        manifest["assets"]["dsh-superagent"]["sources"]["github"].update(
            accept_mode="auto", accept_mode_auto_row="2026-11-12T00:00:00Z", allowed=["someone", "other-one"]
        )
        row = json.loads(generator.render_router_source(manifest)[path])["source"]
        self.assertEqual(
            ["repository", "accept_mode", "accept_mode_row", "accept_mode_auto_row", "observe_admission", "allowed"],
            list(row),
        )
        self.assertEqual(("auto", "2026-11-12T00:00:00Z", ["someone", "other-one"]), (row["accept_mode"], row["accept_mode_auto_row"], row["allowed"]))  # fmt: skip
        # The observe form (the committed row before U469): the sixth key null, the list empty.
        row = json.loads(generator.render_router_source(self.observe_manifest())[path])["source"]
        self.assertEqual(("observe", None, []), (row["accept_mode"], row["accept_mode_auto_row"], row["allowed"]))
        # A manifest without the sourced asset renders no file, like the router profile.
        manifest = copy.deepcopy(self.manifest)
        del manifest["assets"]["dsh-superagent"]["sources"]
        self.assertEqual({}, generator.render_router_source(manifest))

    def test_the_one_yaml_reader_refuses_a_manifest_naming_a_key_twice_in_quoted_and_unquoted_forms(self) -> None:
        """U465c (verdict U465-db9a5e94 P1 `:407`): `yaml.safe_load` resolves a repeated key to its last value, so a
        manifest holding `"allowed": [unauthorized]` and `allowed: []` read as the empty list to the validators while a
        text reader saw the first. The kit's one YAML reader, the generator's `parse_yaml` (PyYAML's SafeLoader with a
        mapping constructor that refuses a key named twice, the two forms compared after the scalar is built, so a
        quoted and an unquoted spelling are one key), refuses the manifest naming the key and both lines; the
        validator's `load_yaml` reads through it, so the asset validation refuses the same file. A raw-text check
        would be one more hand-written reader of YAML, the premise this round drops. Without PyYAML both refuse to run
        (`make unit-test` installs none; the asset validation and render-check run with it)."""
        generator = load_generator()
        spec = importlib.util.spec_from_file_location(
            "validate_agent_assets", ROOT / "scripts/validate-agent-assets.py"
        )
        assert spec and spec.loader
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        text = (ROOT / "home/dot_agents/agent-config.yaml").read_text()
        first = '        accept_mode_row: "2026-11-06T23:24:00Z"\n'
        self.assertEqual(1, text.count(first), "the manifest's Source row as this test knows it")
        cases = {
            "quoted-then-plain": text.replace(first, first + '        "allowed": [unauthorized]\n'),
            "plain-then-plain": text.replace(first, first + "        allowed: [unauthorized]\n"),
            "single-quoted": text.replace(first, first + "        'allowed': [unauthorized]\n"),
        }
        duplicate = self.temp_dir / "duplicate.yaml"
        for case, altered in cases.items():
            with self.subTest(case=case):
                self.assertNotEqual(altered, text)
                duplicate.write_text(altered)
                lines = altered.splitlines()
                here = lines.index(first.rstrip("\n")) + 2
                # The committed `allowed:` line, after the inserted duplicate (which the plain case spells the same way).
                later = max(number for number, line in enumerate(lines, 1) if line.startswith("        allowed:"))
                expected = f"names the key 'allowed' twice (lines {here} and {later})"
                if generator.yaml is None:
                    expected = "PyYAML is required"
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    generator.parse_manifest(altered)
                self.assertIn(expected, stderr.getvalue())
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    validator.load_yaml(duplicate)
                self.assertIn(expected, stderr.getvalue())
        if generator.yaml is not None:
            # The same text with the key once parses, and yaml.safe_load alone (the reader dropped) saw the last.
            allowed = self.asset["sources"]["github"]["allowed"]
            self.assertEqual(allowed, generator.parse_manifest(text)["assets"]["dsh-superagent"]["sources"]["github"]["allowed"])  # fmt: skip
            seen = generator.yaml.safe_load(cases["quoted-then-plain"])
            self.assertEqual(allowed, seen["assets"]["dsh-superagent"]["sources"]["github"]["allowed"], "the last wins")

    def test_c_the_generator_renders_every_field_with_its_default_and_refuses_what_the_validator_refuses_by_one_function(
        self,
    ) -> None:
        """U465d test (c) (verdicts/U465-e6a9a84f.md P2 [f2 s5] `generate-agent-configs.py:2524`): a manifest row without
        `observe_admission` passed generation and validation while the lever refused the rendering, and an auto row
        beside observe passed generation while the validator refused it. One function in the generator,
        `dsh_source_row`, applies the defaults and the refusals: the rendering carries every field (`accept_mode_auto_row`
        as null when the manifest omits it, `observe_admission` as upstream's own default `ignore`, src/policy.ts, so an
        omitted cell changes nothing upstream decides; the committed manifest names `inferred`), and the validator's
        `validate_asset_sources` reads the row through that function, so the same bad row is refused with the same
        words by both and the validator's text holds no row rule of its own."""
        generator = load_generator()
        spec = importlib.util.spec_from_file_location(
            "validate_agent_assets", ROOT / "scripts/validate-agent-assets.py"
        )
        assert spec and spec.loader
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        path = generator.ROOT / "home/dot_agents/router-source.json"
        keys = ["repository", "accept_mode", "accept_mode_row", "accept_mode_auto_row", "observe_admission", "allowed"]
        self.assertEqual("ignore", generator.DSH_OBSERVE_ADMISSION_DEFAULT)
        # The observe form (U469: the committed row is auto with its row), the cell omitted.
        manifest = self.observe_manifest()
        del manifest["assets"]["dsh-superagent"]["sources"]["github"]["observe_admission"]
        row = json.loads(generator.render_router_source(manifest)[path])["source"]
        self.assertEqual(keys, list(row), "every field is present, in the fixed order")
        self.assertEqual(("ignore", None), (row["observe_admission"], row["accept_mode_auto_row"]))
        validator.validate_asset_sources("dsh-superagent", copy.deepcopy(manifest["assets"]["dsh-superagent"]))
        committed = json.loads((ROOT / "home/dot_agents/router-source.json").read_text())["source"]
        self.assertEqual(keys, list(committed), "the committed rendering carries every field")
        self.assertEqual(
            ("inferred", self.asset["sources"]["github"]["accept_mode_auto_row"]),
            (committed["observe_admission"], committed["accept_mode_auto_row"]),
        )
        label = "assets.dsh-superagent.sources.github"
        bad = {
            "an auto row beside observe": (
                lambda row: row.update(accept_mode_auto_row="2026-11-08T00:00:00Z"),
                f"{label}.accept_mode_auto_row belongs to accept_mode auto alone, not 'observe'",
            ),
            "a third word for the cell": (
                lambda row: row.update(observe_admission="explicit"),
                f"{label}.observe_admission 'explicit' is not one of ['inferred', 'ignore']",
            ),
            "a cell of the wrong type": (
                lambda row: row.update(observe_admission=1),
                f"{label}.observe_admission must be a string, not int: 1",
            ),
            "auto without its row": (
                lambda row: row.update(accept_mode="auto"),
                f"{label}.accept_mode auto needs accept_mode_auto_row beside accept_mode_row",
            ),
            "a missing first row": (
                lambda row: row.pop("accept_mode_row"),
                f"{label}.accept_mode_row must be a non-empty string",
            ),
            "an unknown key": (lambda row: row.update(bots=["x"]), f"{label} has unknown key(s) ['bots']"),
            "a listed login beside observe": (
                lambda row: row.update(allowed=["someone"]),
                f"{label}.allowed names ['someone'] while accept_mode is 'observe'",
            ),
        }
        for case, (mutate, expected) in bad.items():
            with self.subTest(case=case):
                manifest = self.observe_manifest()
                mutate(manifest["assets"]["dsh-superagent"]["sources"]["github"])
                with contextlib.redirect_stderr(io.StringIO()) as rendered, self.assertRaises(SystemExit):
                    generator.render_router_source(manifest)
                with contextlib.redirect_stderr(io.StringIO()) as validated, self.assertRaises(SystemExit):
                    validator.validate_asset_sources(
                        "dsh-superagent", copy.deepcopy(manifest["assets"]["dsh-superagent"])
                    )
                self.assertIn(expected, rendered.getvalue())
                self.assertEqual(rendered.getvalue(), validated.getvalue(), "one function, one refusal")
        text = (ROOT / "scripts/validate-agent-assets.py").read_text()
        self.assertIn("dsh_source_row", text, "the validator reads the row through the generator's function")
        for own in ("OBSERVE_ADMISSIONS = ", "ACCEPT_MODES = ", "LADDER_ROW_TIMESTAMP = ", "def validate_sender_ids"):
            self.assertNotIn(own, text, f"the validator keeps no row rule of its own ({own.strip()})")

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
        self.assertIn("`hcom-seat router -- --no-open` starts the Router under srt", docs)
        self.assertIn("`srt --settings` invocation whose writes are the new tree and", docs)
        self.assertIn("`$DSH_HOME/.pnpm-store`", docs)
        self.assertIn("`stateDir` at `$DSH_HOME/router-state`", docs)
        self.assertNotIn("tmux", docs)
        self.assertNotIn("scripts/dsh-superagent", docs)
        self.assertNotIn("dsh-router", docs)


if __name__ == "__main__":
    unittest.main()
