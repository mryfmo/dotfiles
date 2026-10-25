"""Every record the pin checks read has one strict parser: valid shapes parse, the rest raise naming the field."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("pin_records", ROOT / "scripts/pin_records.py")
records = importlib.util.module_from_spec(spec)
sys.modules["pin_records"] = records
spec.loader.exec_module(records)
MODIFY = ROOT / "home/dot_codex/modify_private_config.toml"
COMMIT = "a" * 40


class PinRecordsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = Path(tempfile.mkdtemp(prefix="pin-records-"))
        self.addCleanup(lambda: subprocess.run(["rm", "-rf", str(self.dir)], check=False))

    def write(self, name: str, content: object) -> Path:
        path = self.dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content if isinstance(content, str) else json.dumps(content))
        return path

    def refused(self, call, field: str) -> None:
        with self.assertRaises(records.RecordError) as raised:
            call()
        self.assertIn(field, str(raised.exception))

    def test_plugin_pins(self) -> None:
        good = {
            "claude": {"crit@crit": {"marketplace": "tomasz-tomczyk/crit", "pin": "1.8.14"}},
            "codex": {"tail@tail": {"marketplace": "https://example.invalid/tail.git", "pin": "5.0", "ref": COMMIT}},
            "gh_extensions": {"seachicken/gh-poi": "v0.18.5"},
        }
        pins = records.load_plugin_pins(self.write("pins.json", good))
        self.assertEqual("1.8.14", pins.claude["crit@crit"].pin)
        self.assertEqual(COMMIT, pins.codex["tail@tail"].ref)
        for name, change, field in (
            ("missing top key", lambda d: d.pop("gh_extensions"), "(top)"),
            ("bad id", lambda d: d["claude"].update({"crit": d["claude"]["crit@crit"]}), "claude.crit"),
            ("numeric pin", lambda d: d["claude"]["crit@crit"].update(pin=1.8), "claude.crit@crit.pin"),
            ("extra key", lambda d: d["claude"]["crit@crit"].update(sha="x"), "claude.crit@crit"),
            ("short ref", lambda d: d["codex"]["tail@tail"].update(ref="abc"), "codex.tail@tail.ref"),
            ("bad repository", lambda d: d["gh_extensions"].update({"gh-poi": "v1"}), "gh_extensions.gh-poi"),
        ):
            with self.subTest(case=name):
                data = json.loads(json.dumps(good))
                change(data)
                self.refused(lambda: records.load_plugin_pins(self.write("pins.json", data)), field)
        self.refused(lambda: records.load_plugin_pins(self.dir / "absent.json"), "is missing")

    def test_claude_installs(self) -> None:
        cache = "/h/.claude/plugins/cache/crit/crit/1.8.14"
        good = {"version": 2, "plugins": {"crit@crit": [{"scope": "user", "version": "1.8.14", "installPath": cache}]}}
        self.assertEqual("1.8.14", records.load_claude_installs(self.write("i.json", good))["crit@crit"][0].version)
        self.assertIsNone(records.load_claude_installs(self.dir / "absent.json"))
        entry = good["plugins"]["crit@crit"][0]
        for name, bad, field in (
            ("no installPath (audit case)", {"scope": "user", "version": "9.9.9"}, "installPath: is missing"),
            ("numeric version", {**entry, "version": 1.8}, "version: must be str"),
            ("unknown scope", {**entry, "scope": "global"}, "scope"),
            ("foreign cache", {**entry, "installPath": "/h/.claude/plugins/cache/other/crit/1"}, "installPath"),
            ("project without path", {**entry, "scope": "project"}, "projectPath: is missing"),
            ("not an object", "crit", "must be an object"),
        ):
            with self.subTest(case=name):
                data = {"plugins": {"crit@crit": [bad]}}
                self.refused(lambda: records.load_claude_installs(self.write("i.json", data)), field)
        self.refused(lambda: records.load_claude_installs(self.write("i.json", {"plugins": []})), "plugins")
        self.refused(lambda: records.load_claude_installs(self.write("i.json", "{truncated")), "not JSON")

    def test_claude_enabled(self) -> None:
        self.assertEqual(
            {"crit@crit": False},
            records.load_claude_enabled(self.write("s.json", {"enabledPlugins": {"crit@crit": False}})),
        )
        self.assertEqual({}, records.load_claude_enabled(self.write("s.json", {"model": "x"})))
        self.assertIsNone(records.load_claude_enabled(self.dir / "absent.json"))
        for name, data, field in (
            ("string false", {"enabledPlugins": {"crit@crit": "false"}}, "enabledPlugins.crit@crit"),
            ("zero", {"enabledPlugins": {"crit@crit": 0}}, "enabledPlugins.crit@crit"),
            ("list", {"enabledPlugins": ["crit@crit"]}, "enabledPlugins"),
            ("bad id", {"enabledPlugins": {"crit": True}}, "enabledPlugins.crit"),
            ("array top", [], "(top)"),
        ):
            with self.subTest(case=name):
                self.refused(lambda: records.load_claude_enabled(self.write("s.json", data)), field)

    def test_claude_marketplace_listing(self) -> None:
        listing = [{"name": "crit", "source": "github", "repo": "tomasz-tomczyk/crit"}]
        self.assertEqual(
            "registered", records.claude_marketplace_state(json.dumps(listing), "crit", "tomasz-tomczyk/crit")
        )
        self.assertEqual("absent", records.claude_marketplace_state("[]", "crit", "tomasz-tomczyk/crit"))
        for name, text, field in (
            ("foreign source", json.dumps([{"name": "crit", "source": "github", "repo": "fork/crit"}]), "[0]"),
            ("directory source", json.dumps([{"name": "crit", "source": "directory", "path": "/x"}]), "[0]"),
            ("no name", json.dumps([{"source": "github"}]), "[0].name"),
            ("not JSON", "", "not JSON"),
            ("object", "{}", "must be a list"),
        ):
            with self.subTest(case=name):
                self.refused(lambda: records.claude_marketplace_state(text, "crit", "tomasz-tomczyk/crit"), field)

    def test_codex_plugin_copy(self) -> None:
        root = self.dir / "cache/tail/tail"
        self.assertIsNone(records.load_codex_copy(root, "tail", MODIFY))
        self.write("cache/tail/tail/5.0.0/.codex-plugin/plugin.json", {"name": "tail", "version": "5.0.0"})
        self.assertEqual("5.0.0", records.load_codex_copy(root, "tail", MODIFY).version)
        for name, manifest, field in (
            ("foreign name", {"name": "fork", "version": "5.0.0"}, "name"),
            ("no name", {"version": "5.0.0"}, "name: is missing"),
            ("null version", {"name": "tail", "version": None}, "version: must be str"),
            ("not JSON", "{", "not JSON"),
        ):
            with self.subTest(case=name):
                self.write("cache/tail/tail/5.0.0/.codex-plugin/plugin.json", manifest)
                self.refused(lambda: records.load_codex_copy(root, "tail", MODIFY), field)
        (root / "5.0.0/.codex-plugin/plugin.json").unlink()
        self.refused(lambda: records.load_codex_copy(root, "tail", MODIFY), "is missing")
        for entry in root.iterdir():
            subprocess.run(["rm", "-rf", str(entry)], check=True)
        self.refused(lambda: records.load_codex_copy(root, "tail", MODIFY), "no version directory")

    def test_marketplace_install_record(self) -> None:
        source = "https://example.invalid/tail.git"
        good = {"source_type": "git", "source": source, "ref_name": None, "sparse_paths": [], "revision": COMMIT}
        self.assertEqual(COMMIT, records.load_marketplace_install(self.write("m.json", good), source).revision)
        self.assertIsNone(records.load_marketplace_install(self.dir / "absent.json", source))
        for name, change, field in (
            ("foreign source", {"source": "https://example.invalid/fork.git"}, "source"),
            ("local source type", {"source_type": "local"}, "source_type"),
            ("short revision", {"revision": "abc"}, "revision"),
            ("numeric revision", {"revision": 1}, "revision: must be str"),
        ):
            with self.subTest(case=name):
                self.refused(
                    lambda: records.load_marketplace_install(self.write("m.json", {**good, **change}), source), field
                )

    def test_codex_config(self) -> None:
        good = (
            '[plugins."tail@tail"]\nenabled = true\n\n[marketplaces.tail]\nsource_type = "git"\n'
            'source = "https://example.invalid/tail.git"\nref = "' + COMMIT + '"\n'
        )
        config = records.load_codex_config(self.write("config.toml", good))
        self.assertIs(True, config.plugins["tail@tail"])
        self.assertEqual(
            "registered",
            records.codex_marketplace_state(self.dir / "config.toml", "tail", "https://example.invalid/tail.git"),
        )
        self.assertEqual("absent", records.codex_marketplace_state(self.dir / "absent.toml", "tail", "x"))
        for name, text, field in (
            ("string enabled", '[plugins."tail@tail"]\nenabled = "true"\n', "plugins.tail@tail.enabled"),
            ("no enabled", '[plugins."tail@tail"]\n', "plugins.tail@tail.enabled: is missing"),
            ("bad id", '[plugins."tail"]\nenabled = true\n', "plugins.tail"),
            ("no source", '[marketplaces.tail]\nsource_type = "git"\n', "marketplaces.tail.source"),
            ("not TOML", "[plugins\n", "not TOML"),
        ):
            with self.subTest(case=name):
                self.refused(lambda: records.load_codex_config(self.write("config.toml", text)), field)
        self.write("config.toml", good)
        self.refused(
            lambda: records.codex_marketplace_state(
                self.dir / "config.toml", "tail", "https://example.invalid/fork.git"
            ),
            "marketplaces.tail.source",
        )

    def test_gh_extension_manifest(self) -> None:
        data = self.dir / "data"
        self.assertIsNone(records.load_gh_extension(data, "seachicken/gh-poi"))
        good = "owner: seachicken\nname: gh-poi\nhost: github.com\ntag: v0.18.5\nispinned: true\npath: /x/gh-poi\n"
        self.write("data/gh/extensions/gh-poi/manifest.yml", good)
        extension = records.load_gh_extension(data, "seachicken/gh-poi")
        self.assertEqual(("v0.18.5", True), (extension.tag, extension.pinned))
        for name, text, field in (
            ("fork (audit case)", good.replace("owner: seachicken", "owner: forker"), "owner/name"),
            ("other host", good.replace("github.com", "ghe.example"), "host"),
            ("no ispinned", good.replace("ispinned: true\n", ""), "ispinned: is missing"),
            ("ispinned yes", good.replace("ispinned: true", "ispinned: yes"), "ispinned"),
            ("duplicate key", good + "tag: v9\n", "line 7"),
            ("not key-value", good + "- item\n", "line 7"),
        ):
            with self.subTest(case=name):
                self.write("data/gh/extensions/gh-poi/manifest.yml", text)
                self.refused(lambda: records.load_gh_extension(data, "seachicken/gh-poi"), field)
        (data / "gh/extensions/gh-poi/manifest.yml").unlink()
        self.write("data/gh/extensions/gh-poi/gh-poi", "binary")
        self.refused(lambda: records.load_gh_extension(data, "seachicken/gh-poi"), "cannot verify its pin")

    def test_mise_holds(self) -> None:
        good = '[tools]\n# Held: reason\nfd = "10.3.0"\njq = "latest"\n\n# Held: http\n[tools."http:bats"]\nversion = "1"\n'
        self.assertEqual(["fd", "http:bats"], records.load_mise_holds(self.write("mise.toml", good)))
        self.assertEqual(
            ["npm:ccstatusline", "npm:ccusage", "npm:pnpm"], records.load_mise_holds(ROOT / "home/dot_mise/config.toml")
        )
        for name, text in (
            ("hold above a setting", '[settings]\n# Held: x\nminimum_release_age = "72h"\n'),
            ("hold above a blank line", '[tools]\n# Held: x\n\nfd = "1"\n'),
            ("dangling hold", '[tools]\nfd = "1"\n# Held: x\n'),
        ):
            with self.subTest(case=name):
                self.refused(lambda: records.load_mise_holds(self.write("mise.toml", text)), "Held comment")
        self.refused(lambda: records.load_mise_holds(self.dir / "absent.toml"), "is missing")

    def test_unreadable_is_never_absent(self) -> None:
        locked = self.dir / "locked"
        locked.mkdir()
        (locked / "f.json").write_text("{}")
        locked.chmod(0)
        self.addCleanup(locked.chmod, 0o755)
        self.refused(lambda: records.load_claude_installs(locked / "f.json"), "cannot")
        self.refused(lambda: records.present(locked / "f.json"), "cannot stat")

    def test_json_null_and_wrong_top_types_are_errors_not_absent(self) -> None:
        loaders = {
            "installed_plugins.json": records.load_claude_installs,
            "settings.json": records.load_claude_enabled,
            "plugin-pins.json": records.load_plugin_pins,
            "install record": lambda path: records.load_marketplace_install(path, "x"),
        }
        for name, load in loaders.items():
            for top in ("null", "[]", "1", '"text"'):
                with self.subTest(record=name, top=top):
                    self.refused(lambda: load(self.write("r.json", top)), "(top)")

    def test_control_characters_never_reach_an_output_row(self) -> None:
        # A projectPath that would forge a user row at the pin in tab/newline-separated output is refused.
        cache = "/h/.claude/plugins/cache/crit/crit/9.9.9"
        forged = {"scope": "project", "version": "9.9.9", "installPath": cache, "projectPath": "/w\nuser\t1.8.14\t"}
        path = self.write("i.json", {"plugins": {"crit@crit": [forged]}})
        self.refused(lambda: records.load_claude_installs(path), "projectPath: contains a control character")
        manifest = "owner: seachicken\nname: gh-poi\nhost: github.com\ntag: v1\tx\nispinned: true\npath: /x\n"
        self.write("data/gh/extensions/gh-poi/manifest.yml", manifest)
        self.refused(lambda: records.load_gh_extension(self.dir / "data", "seachicken/gh-poi"), "tag")
        self.refused(
            lambda: records.load_plugin_pins(
                self.write("p.json", {"claude": {"crit@crit\n": {}}, "codex": {}, "gh_extensions": {}})
            ),
            "claude.crit@crit",
        )
        # The command line prints one JSON list, which the shell reads with jq.
        good = {
            "plugins": {
                "crit@crit": [{"scope": "user", "version": "1.8.14", "installPath": cache.replace("9.9.9", "1.8.14")}]
            }
        }
        result = subprocess.run(
            [
                sys.executable,
                "-I",
                str(ROOT / "scripts/pin_records.py"),
                "claude-installs",
                str(self.write("i.json", good)),
                "crit@crit",
            ],
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual("1.8.14", json.loads(result.stdout)[0]["version"])

    def test_command_line_fails_with_the_field(self) -> None:
        path = self.write("s.json", {"enabledPlugins": {"crit@crit": "false"}})
        result = subprocess.run(
            [sys.executable, "-I", str(ROOT / "scripts/pin_records.py"), "claude-enabled", str(path), "crit@crit"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("enabledPlugins.crit@crit: must be a boolean", result.stderr)


if __name__ == "__main__":
    unittest.main()
