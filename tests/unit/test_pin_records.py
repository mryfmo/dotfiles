"""Every record the pin checks read has one strict parser: valid shapes parse, the rest raise naming the field."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("pin_records", ROOT / "scripts/pin_records.py")
records = importlib.util.module_from_spec(spec)
sys.modules["pin_records"] = records
spec.loader.exec_module(records)
MODIFY = ROOT / "home/dot_codex/modify_private_config.toml"
COMMIT = "a" * 40


sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes


def setUpModule() -> None:
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


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
        cache = f"{self.dir}/cache/crit/crit/1.8.14"
        good = {"version": 2, "plugins": {"crit@crit": [{"scope": "user", "version": "1.8.14", "installPath": cache}]}}
        self.assertEqual("1.8.14", records.load_claude_installs(self.write("i.json", good))["crit@crit"][0].version)
        self.assertIsNone(records.load_claude_installs(self.dir / "absent.json"))
        entry = good["plugins"]["crit@crit"][0]
        for name, bad, field in (
            ("no installPath (audit case)", {"scope": "user", "version": "9.9.9"}, "installPath: is missing"),
            ("numeric version", {**entry, "version": 1.8}, "version: must be str"),
            ("unknown scope", {**entry, "scope": "global"}, "scope"),
            ("foreign cache", {**entry, "installPath": f"{self.dir}/cache/other/crit/1.8.14"}, "installPath"),
            ("version contradicts path (audit case)", {**entry, "version": "9.9.9"}, "installPath"),
            (
                "another claude directory",
                {**entry, "installPath": "/h/.claude/plugins/cache/crit/crit/1.8.14"},
                "installPath",
            ),
            ("dot-dot", {**entry, "installPath": f"{self.dir}/cache/crit/crit/../crit/1.8.14"}, "installPath"),
            ("project without path", {**entry, "scope": "project"}, "projectPath: is missing"),
            (
                "duplicate user record (audit case)",
                [entry, {**entry, "version": "99.0.0", "installPath": cache.replace("1.8.14", "99.0.0")}],
                "a second user-scope record",
            ),
            ("not an object", "crit", "must be an object"),
        ):
            with self.subTest(case=name):
                data = {"plugins": {"crit@crit": bad if isinstance(bad, list) else [bad]}}
                self.refused(lambda: records.load_claude_installs(self.write("i.json", data)), field)
        self.refused(lambda: records.load_claude_installs(self.write("i.json", {"plugins": []})), "plugins")
        self.refused(lambda: records.load_claude_installs(self.write("i.json", "{truncated")), "not JSON")

    # Audit round 23: a record value joined into a path replaced the root (absolute) or left it (`..`).
    BAD_COMPONENTS = ("/abs", "..", "a/b", "", ".")

    def test_no_record_value_used_as_a_path_component_can_leave_its_root(self) -> None:
        cache = self.dir / "cache"

        def claude_install(plugin: str, marketplace: str, version: str):
            # installPath is what a plain join of the record's own fields gives, so only confinement refuses it.
            install_path = str(cache / marketplace / plugin / version)
            data = {
                "plugins": {
                    f"{plugin}@{marketplace}": [{"scope": "user", "version": version, "installPath": install_path}]
                }
            }
            return lambda: records.load_claude_installs(self.write("i.json", data))

        cases = {
            "installed_plugins.json version": lambda bad: claude_install("crit", "crit", bad),
            "installed_plugins.json plugin": lambda bad: claude_install(bad, "crit", "1.8.14"),
            "installed_plugins.json marketplace": lambda bad: claude_install("crit", bad, "1.8.14"),
            "gh extension name": lambda bad: lambda: records.load_gh_extension(self.dir / "gh", f"seachicken/{bad}"),
            "gh extension owner": lambda bad: lambda: records.load_gh_extension(self.dir / "gh", f"{bad}/gh-poi"),
            "Codex version directory": lambda bad: lambda: records.confined(cache, "(version directory)", cache, bad),
        }
        (self.dir / "gh/extensions").mkdir(parents=True)
        for field_name, make in cases.items():
            for bad in self.BAD_COMPONENTS:
                with self.subTest(field=field_name, value=bad):
                    with self.assertRaises(records.RecordError):
                        make(bad)()
        # The pins' own ids reach the doctor's Codex cache and marketplace paths: each refused, never "absent".
        spec = importlib.util.spec_from_file_location(
            "check_agent_runtime_paths", ROOT / "scripts/check-agent-runtime.py"
        )
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        home = self.dir / "home"
        (home / ".codex").mkdir(parents=True)
        for part in ("plugin", "marketplace"):
            for bad in self.BAD_COMPONENTS:
                with self.subTest(field=f"codex pin {part}", value=bad):
                    plugin_id = f"{bad}@tail" if part == "plugin" else f"tail@{bad}"
                    pins = {plugin_id: checker.records.Pin("https://example.invalid/tail.git", "5.0.0", COMMIT)}
                    findings = checker.codex_plugin_pin_findings(home, pins, MODIFY)
                    self.assertTrue([f for f in findings if "is not one path component" in f], findings)
                    self.assertFalse([f for f in findings if checker.is_warning(f)], findings)
        # A strict component still joins.
        self.assertEqual(cache / "crit" / "1.8.14+build", records.confined(cache, "x", cache, "crit", "1.8.14+build"))

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
        for text in (
            json.dumps([{"name": "crit", "source": "github", "repo": "fork/crit"}]),
            json.dumps([{"name": "crit", "source": "directory", "path": "/x"}]),
        ):
            with self.subTest(foreign=text):
                self.assertEqual("foreign", records.claude_marketplace_state(text, "crit", "tomasz-tomczyk/crit"))
        for name, text, field in (
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
        data = self.dir / "data/gh"
        self.assertIsNone(records.load_gh_extension(data, "seachicken/gh-poi"))
        binary = data / "extensions/gh-poi/gh-poi"
        good = f"owner: seachicken\nname: gh-poi\nhost: github.com\ntag: v0.18.5\nispinned: true\npath: {binary}\n"
        self.write("data/gh/extensions/gh-poi/manifest.yml", good)
        extension = records.load_gh_extension(data, "seachicken/gh-poi")
        self.assertEqual(("v0.18.5", True), (extension.tag, extension.pinned))
        for name, text, field in (
            ("fork (audit case)", good.replace("owner: seachicken", "owner: forker"), "owner/name"),
            ("other host", good.replace("github.com", "ghe.example"), "host"),
            ("other path", good.replace(str(binary), "/elsewhere/gh-poi"), "path"),
            ("no ispinned", good.replace("ispinned: true\n", ""), "ispinned: is missing"),
            ("ispinned yes", good.replace("ispinned: true", "ispinned: yes"), "ispinned"),
            ("duplicate key", good + "tag: v9\n", "line 7"),
            ("not key-value", good + "- item\n", "line 7"),
        ):
            with self.subTest(case=name):
                self.write("data/gh/extensions/gh-poi/manifest.yml", text)
                self.refused(lambda: records.load_gh_extension(data, "seachicken/gh-poi"), field)
        (data / "extensions/gh-poi/manifest.yml").unlink()
        self.write("data/gh/extensions/gh-poi/gh-poi", "binary")
        self.refused(lambda: records.load_gh_extension(data, "seachicken/gh-poi"), "cannot verify its pin")

    def test_no_line_separator_but_newline_can_forge_a_text_record_field(self) -> None:
        # Audit round 25: str.splitlines() also breaks at \x0b, \x0c, \x1c-\x1e, \x85, \u2028 and \u2029, so
        # `tag: v0.18.5\x0bispinned: true` read as two fields. The whole file is refused instead.
        data = self.dir / "data/gh"
        binary = data / "extensions/gh-poi/gh-poi"
        base = f"owner: seachicken\nname: gh-poi\nhost: github.com\npath: {binary}\n"
        self.write("data/gh/extensions/gh-poi/manifest.yml", base + "tag: v0.18.5\nispinned: true\n")
        self.assertTrue(records.load_gh_extension(data, "seachicken/gh-poi").pinned)
        holds = '[tools]\n# Held: reason\nnode = "22"\n'
        self.assertEqual(["node"], records.load_mise_holds(self.write("mise.toml", holds)))
        self.assertEqual(["node"], records.load_mise_holds(self.write("mise.toml", holds.replace(" = ", "\t= "))))
        for separator in ("\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029", "\r"):
            with self.subTest(record="gh manifest", separator=repr(separator)):
                forged = base + f"tag: v0.18.5{separator}ispinned: true\n"
                self.write("data/gh/extensions/gh-poi/manifest.yml", forged)
                self.refused(lambda: records.load_gh_extension(data, "seachicken/gh-poi"), "line 5")
            with self.subTest(record="mise holds", separator=repr(separator)):
                # A Held comment that splitlines() would end early, putting `node` directly under it.
                forged = f'[tools]\n# Held: reason{separator}node = "22"\n'
                self.refused(lambda: records.load_mise_holds(self.write("mise.toml", forged)), "line 2")
        with self.subTest(record="gh manifest", separator="tab"):
            self.write("data/gh/extensions/gh-poi/manifest.yml", base + "tag: v0.18.5\tx\nispinned: true\n")
            self.refused(lambda: records.load_gh_extension(data, "seachicken/gh-poi"), "line 5")

    def test_no_record_value_is_stripped_into_another_value(self) -> None:
        # Audit round 26: `.strip()` turned `v0.18.5\u00a0` into the pin. Values are compared exactly, and one
        # with leading or trailing whitespace of any kind is refused; ASCII formats refuse non-ASCII.
        data = self.dir / "data/gh"
        binary = data / "extensions/gh-poi/gh-poi"
        gh = f"owner: seachicken\nname: gh-poi\nhost: github.com\ntag: {{tag}}\nispinned: true\npath: {binary}\n"
        pins = {
            "claude": {"crit@crit": {"marketplace": "tomasz-tomczyk/crit", "pin": "1.8.14"}},
            "codex": {},
            "gh_extensions": {},
        }
        cache = self.dir / "cache/crit/crit/1.8.14"
        install = {"plugins": {"crit@crit": [{"scope": "user", "version": "1.8.14", "installPath": str(cache)}]}}
        listing = [{"name": "crit", "source": "github", "repo": "tomasz-tomczyk/crit"}]
        root = self.dir / "codex/tail/tail"
        cases = {
            "gh manifest tag": lambda v: (
                self.write("data/gh/extensions/gh-poi/manifest.yml", gh.format(tag=v)),
                lambda: records.load_gh_extension(data, "seachicken/gh-poi"),
            )[1],
            "pins pin": lambda v: (
                pins["claude"]["crit@crit"].update(pin=v),
                self.write("pins.json", pins),
                lambda: records.load_plugin_pins(self.dir / "pins.json"),
            )[2],
            "pins gh tag": lambda v: (
                self.write("pins2.json", {**pins, "claude": {}, "gh_extensions": {"seachicken/gh-poi": v}}),
                lambda: records.load_plugin_pins(self.dir / "pins2.json"),
            )[1],
            "claude marketplace listing": lambda v: (
                lambda: records.claude_marketplace_state(
                    json.dumps([{**listing[0], "repo": v}]), "crit", "tomasz-tomczyk/crit"
                )
            ),
            "codex copy version": lambda v: (
                self.write("codex/tail/tail/5.0.0/.codex-plugin/plugin.json", {"name": "tail", "version": v}),
                lambda: records.load_codex_copy(root, "tail", MODIFY),
            )[1],
            "mise held tool": lambda v: (
                self.write("mise.toml", f'# Held: reason\n[tools."{v}"]\nversion = "1"\n'),
                lambda: records.load_mise_holds(self.dir / "mise.toml"),
            )[1],
        }
        for field_name, make in cases.items():
            for value in ("v0.18.5\u00a0", "\u2009v0.18.5", "v0.18.5\u3000", "v0.18.5\t", "v0.18.\u0665"):
                if field_name == "claude marketplace listing":
                    value = value.replace("v0.18.5", "tomasz-tomczyk/crit").replace("v0.18.", "tomasz-tomczyk/cri")
                with self.subTest(field=field_name, value=repr(value)):
                    with self.assertRaises(records.RecordError):
                        make(value)()
        # Claude's install record version (also a path component) refuses them too.
        for value in ("1.8.14\u00a0", "\u20091.8.14"):
            with self.subTest(field="installed_plugins.json version", value=repr(value)):
                entry = {
                    **install["plugins"]["crit@crit"][0],
                    "version": value,
                    "installPath": str(self.dir / "cache/crit/crit" / value),
                }
                self.refused(
                    lambda: records.load_claude_installs(self.write("i.json", {"plugins": {"crit@crit": [entry]}})),
                    "version",
                )
        # An exact value still parses.
        self.write("data/gh/extensions/gh-poi/manifest.yml", gh.format(tag="v0.18.5"))
        self.assertEqual("v0.18.5", records.load_gh_extension(data, "seachicken/gh-poi").tag)
        self.assertEqual(["v0.18.5"], cases["mise held tool"]("v0.18.5")())
        self.assertEqual("v0.18.5", cases["codex copy version"]("v0.18.5")().version)
        self.assertEqual("v0.18.5", cases["pins pin"]("v0.18.5")().claude["crit@crit"].pin)
        self.assertEqual("registered", cases["claude marketplace listing"]("tomasz-tomczyk/crit")())

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
        cache = f"{self.dir}/cache/crit/crit/9.9.9"
        forged = {"scope": "project", "version": "9.9.9", "installPath": cache, "projectPath": "/w\nuser\t1.8.14\t"}
        path = self.write("i.json", {"plugins": {"crit@crit": [forged]}})
        self.refused(lambda: records.load_claude_installs(path), "projectPath: contains a control character")
        manifest = "owner: seachicken\nname: gh-poi\nhost: github.com\ntag: v1\tx\nispinned: true\npath: /x\n"
        self.write("data/gh/extensions/gh-poi/manifest.yml", manifest)
        # Refused as a whole file at the line that holds it (record_lines), before any field is read.
        self.refused(lambda: records.load_gh_extension(self.dir / "data/gh", "seachicken/gh-poi"), "line 4")
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

    def test_explicit_null_in_an_optional_field_is_an_error(self) -> None:
        # An optional key may be missing; present, it must have its type: null never means "not recorded".
        pins = {
            "claude": {},
            "codex": {"tail@tail": {"marketplace": "m", "pin": "1", "ref": None}},
            "gh_extensions": {},
        }
        listing = json.dumps([{"name": "crit", "source": "github", "repo": None}])
        config = '[marketplaces.tail]\nsource_type = "git"\nsource = "s"\nref = 1\n'
        for name, call, field in (
            (
                "plugin-pins codex ref",
                lambda: records.load_plugin_pins(self.write("p.json", pins)),
                "codex.tail@tail.ref",
            ),
            (
                "settings enabledPlugins",
                lambda: records.load_claude_enabled(self.write("s.json", {"enabledPlugins": None})),
                "enabledPlugins",
            ),
            ("marketplace list repo", lambda: records.claude_marketplace_state(listing, "crit", "o/crit"), "[0].repo"),
            (
                "config marketplace ref",
                lambda: records.load_codex_config(self.write("c.toml", config)),
                "marketplaces.tail.ref",
            ),
        ):
            with self.subTest(field=name):
                self.refused(call, field)
        # Missing optional keys stay allowed.
        del pins["codex"]["tail@tail"]["ref"]
        self.assertIsNone(records.load_plugin_pins(self.write("p.json", pins)).codex["tail@tail"].ref)
        self.assertEqual({}, records.load_claude_enabled(self.write("s.json", {})))
        with self.assertRaises(records.RecordError):
            records.optional("r", {"ref": None}, "ref", str)
        self.assertIsNone(records.optional("r", {}, "ref", str))

    def test_every_string_passes_clean_including_extension_tags(self) -> None:
        base = {"claude": {}, "codex": {}, "gh_extensions": {"seachicken/gh-poi": "v1\nFORGED"}}
        self.refused(lambda: records.load_plugin_pins(self.write("p.json", base)), "gh_extensions.seachicken/gh-poi")
        base["gh_extensions"]["seachicken/gh-poi"] = "v1\x00"
        self.refused(lambda: records.load_plugin_pins(self.write("p.json", base)), "gh_extensions.seachicken/gh-poi")
        self.refused(
            lambda: records.load_codex_config(
                self.write("c.toml", '[marketplaces."a\\nb"]\nsource_type = "git"\nsource = "s"\n')
            ),
            "marketplaces",
        )

    def test_yes_no_questions_exit_0_1_and_2_on_failure(self) -> None:
        script = [sys.executable, "-I", str(ROOT / "scripts/pin_records.py")]
        config = self.write("mise.toml", '[tools]\n# Held: x\nfd = "1"\njq = "latest"\n')
        pins = self.write("p.json", {"claude": {}, "codex": {}, "gh_extensions": {"seachicken/gh-poi": "v1"}})
        for args, code in (
            (["is-held", str(config), "fd"], 0),
            (["is-held", str(config), "jq"], 1),
            (["is-held", str(self.dir / "absent.toml"), "fd"], 2),
            (["is-pinned-extension", str(pins), "seachicken/gh-poi"], 0),
            (["is-pinned-extension", str(pins), "fork/gh-poi"], 0),
            (["is-pinned-extension", str(pins), "dlvhdr/gh-dash"], 1),
            (["is-pinned-extension", str(pins), "not a repository"], 2),
            (["is-pinned-extension", str(self.write("bad.json", "{")), "dlvhdr/gh-dash"], 2),
        ):
            with self.subTest(args=args[0:1] + args[2:]):
                self.assertEqual(code, subprocess.run([*script, *args], capture_output=True, check=False).returncode)

    def test_agent_homes_follow_each_tools_own_variables(self) -> None:
        home = Path("/h")
        cases = (
            ("claude", {}, "/h/.claude"),
            ("claude", {"CLAUDE_CONFIG_DIR": "/c"}, "/c"),
            ("codex", {}, "/h/.codex"),
            ("codex", {"CODEX_HOME": "/x"}, "/x"),
            ("codex", {"CODEX_HOME": ""}, "/h/.codex"),
            ("gh", {}, "/h/.local/share/gh"),
            ("gh", {"XDG_DATA_HOME": "/d"}, "/d/gh"),
            ("gh", {"GH_DATA_DIR": "/g", "XDG_DATA_HOME": "/d"}, "/g"),
        )
        for agent, env, expected in cases:
            with self.subTest(agent=agent, env=env):
                clear = {name: "" for name in ("CLAUDE_CONFIG_DIR", "CODEX_HOME", "GH_DATA_DIR", "XDG_DATA_HOME")}
                with mock.patch.dict(os.environ, {**clear, **env}):
                    self.assertEqual(Path(expected), records.agent_home(agent, home))

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
