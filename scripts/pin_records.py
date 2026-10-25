#!/usr/bin/env python3
"""Strict parsers for every external record the pin checks read; the only readers make update and make doctor use.

Each parser returns a typed record or raises RecordError naming the record and the field. A record is absent
only when its path does not exist (FileNotFoundError or NotADirectoryError, see `present`); any other read
failure, a required key that is missing or has another type, or an identity field (owner, repository, name,
marketplace, source) that differs from the pin is an error, never "absent" and never a pass. Keys a tool adds
beyond the required ones are tolerated, since Claude Code, Codex and gh add fields over time.

scripts/check-agent-runtime.py imports this module; scripts/update-agent-assets.sh, scripts/upgrade-tools.sh
and install/common/gh_extensions.sh run its command-line form (`python3 -I scripts/pin_records.py <command>`),
which prints the parsed value and exits 2 with `ERROR: <record>: <field>: <why>` on stderr otherwise; the
yes/no questions (is-held, is-pinned-extension) exit 0 for yes and 1 for no, so any other exit is a failure. It keeps
to Python 3.9 syntax so a fresh macOS's /usr/bin/python3 can run the gh commands; only the TOML readers need
tomllib (Python 3.11+).
"""

from __future__ import annotations

import functools
import io
import json
import os
import re
import stat
import sys
from contextlib import redirect_stderr
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# One path component taken from record data (see confined): it starts with a letter or digit, so it is never
# empty, `.`, `..` or absolute, and holds no separator.
COMPONENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]*")
PLUGIN_ID = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)@([A-Za-z0-9][A-Za-z0-9._-]*)$")
REPOSITORY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
CLAUDE_SCOPES = ("user", "project", "local", "managed")


class RecordError(Exception):
    """A record that exists but cannot be read, has an unknown shape, or names a foreign identity."""

    def __init__(self, record: object, field: str, why: str) -> None:
        super().__init__(f"{record}: {field}: {why}")


def present(path: Path) -> bool:
    """False only when PATH (or a parent) is absent; any other stat failure raises RecordError."""
    try:
        path.stat()
    except (FileNotFoundError, NotADirectoryError):
        return False
    except OSError as error:
        raise RecordError(path, "(file)", f"cannot stat: {error!r}") from error
    return True


def read_text(path: Path) -> Optional[str]:
    """The text of PATH, None when absent; any other failure raises RecordError."""
    try:
        return path.read_text()
    except (FileNotFoundError, NotADirectoryError):
        return None
    except (OSError, UnicodeDecodeError) as error:
        raise RecordError(path, "(file)", f"cannot read: {error!r}") from error


class Absent:
    """The record's path does not exist; distinct from every parsed value, JSON null included."""

    def __repr__(self) -> str:
        return "ABSENT"


ABSENT = Absent()


def load_json(path: Path) -> Any:
    """The parsed JSON of PATH, or ABSENT when the path does not exist; a top-level null is an error."""
    text = read_text(path)
    if text is None:
        return ABSENT
    try:
        data = json.loads(text)
    except ValueError as error:
        raise RecordError(path, "(file)", f"not JSON: {error}") from error
    if data is None:
        raise RecordError(path, "(top)", "is JSON null, not a record")
    return data


def load_toml(path: Path) -> Any:
    """The parsed TOML of PATH, or ABSENT when the path does not exist."""
    text = read_text(path)
    if text is None:
        return ABSENT
    import tomllib

    try:
        return tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise RecordError(path, "(file)", f"not TOML: {error}") from error


def field(record: object, data: Any, name: str, kind: type, where: str = "") -> Any:
    """DATA[NAME] with exactly type KIND (bool is never an int, an int never a str)."""
    label = f"{where}{name}"
    if not isinstance(data, dict):
        raise RecordError(record, where.rstrip(".") or "(top)", f"must be an object, not {type(data).__name__}")
    if name not in data:
        raise RecordError(record, label, "is missing")
    value = data[name]
    if type(value) is not kind:
        raise RecordError(record, label, f"must be {kind.__name__}, not {type(value).__name__}")
    if kind is str:
        clean(record, label, value)
    return value


CONTROL = re.compile(r"[\x00-\x1f\x7f]")


def clean(record: object, label: str, value: str) -> str:
    """VALUE when it holds no control character (tab, newline, carriage return, NUL, ...), else RecordError:
    no field can then forge a row or a record boundary in any output."""
    if CONTROL.search(value):
        raise RecordError(record, label, f"contains a control character: {value!r}")
    return value


def optional(record: object, data: Dict[str, Any], name: str, kind: type, where: str = "") -> Any:
    """DATA[NAME] when the key is there, None only when it is missing: a present key, explicit null
    included, must have type KIND, so null never stands in for "not recorded"."""
    if not isinstance(data, dict):
        raise RecordError(record, where.rstrip(".") or "(top)", f"must be an object, not {type(data).__name__}")
    return field(record, data, name, kind, where) if name in data else None


def plugin_parts(record: object, label: str, plugin_id: str) -> Tuple[str, str]:
    match = PLUGIN_ID.fullmatch(plugin_id)
    if not match:
        raise RecordError(record, label, f"{plugin_id!r} is not <plugin>@<marketplace>")
    return match.group(1), match.group(2)


def confined(record: object, label: str, root: Path, *parts: object) -> Path:
    """ROOT joined with PARTS taken from record data, each one strict COMPONENT.

    The join is refused unless its components are exactly ROOT's followed by PARTS, so no record value can
    replace ROOT (an absolute value), climb out of it (`..`) or reach a deeper directory (`a/b`).
    """
    for part in parts:
        if type(part) is not str or not COMPONENT.fullmatch(part):
            raise RecordError(record, label, f"{part!r} is not one path component")
    joined = root.joinpath(*parts)
    if joined.parts != (*root.parts, *parts):
        raise RecordError(record, label, f"{str(joined)!r} is not {str(root)!r} plus {list(parts)!r}")
    return joined


# --- agent homes ----------------------------------------------------------------------------------------------


def agent_home(agent: str, home: Optional[Path] = None) -> Path:
    """The directory each tool keeps its records in, resolved the way the tool itself does; the one resolver
    make doctor and update-agent-assets.sh share (the shell asks `pin_records.py agent-home <agent>`).

    claude: CLAUDE_CONFIG_DIR, else ~/.claude. codex: CODEX_HOME, else ~/.codex. gh: GH_DATA_DIR, else
    $XDG_DATA_HOME/gh, else ~/.local/share/gh (gh's config.DataDir). An empty variable counts as unset, as
    `${VAR:-default}` does.
    """
    env = os.environ
    base = home if home is not None else Path.home()
    if agent == "claude":
        return Path(env["CLAUDE_CONFIG_DIR"]) if env.get("CLAUDE_CONFIG_DIR") else base / ".claude"
    if agent == "codex":
        return Path(env["CODEX_HOME"]) if env.get("CODEX_HOME") else base / ".codex"
    if agent == "gh":
        if env.get("GH_DATA_DIR"):
            return Path(env["GH_DATA_DIR"])
        return Path(env["XDG_DATA_HOME"]) / "gh" if env.get("XDG_DATA_HOME") else base / ".local/share/gh"
    raise RecordError("agent-home", agent, "is not claude, codex or gh")


# --- scripts/plugin-pins.json (rendered from assets.* in agent-config.yaml) ---------------------------------


@dataclass(frozen=True)
class Pin:
    marketplace: str
    pin: str
    ref: Optional[str] = None


@dataclass(frozen=True)
class PluginPins:
    claude: Dict[str, Pin]
    codex: Dict[str, Pin]
    gh_extensions: Dict[str, str]


def load_plugin_pins(path: Path) -> PluginPins:
    data = load_json(path)
    if data is ABSENT:
        raise RecordError(path, "(file)", "is missing")
    if not isinstance(data, dict) or set(data) != {"claude", "codex", "gh_extensions"}:
        raise RecordError(path, "(top)", "must hold exactly claude, codex and gh_extensions")
    agents: Dict[str, Dict[str, Pin]] = {}
    for agent in ("claude", "codex"):
        table = field(path, data, agent, dict)
        agents[agent] = {}
        for plugin_id, entry in table.items():
            where = f"{agent}.{plugin_id}."
            plugin_parts(path, where.rstrip("."), plugin_id)
            allowed = {"marketplace", "pin", "ref"} if agent == "codex" else {"marketplace", "pin"}
            if not isinstance(entry, dict) or not set(entry) <= allowed:
                raise RecordError(path, where.rstrip("."), f"may hold only {sorted(allowed)}")
            ref = optional(path, entry, "ref", str, where)
            if ref is not None and not COMMIT.fullmatch(ref):
                raise RecordError(path, f"{where}ref", "must be a 40-hex commit")
            agents[agent][plugin_id] = Pin(
                field(path, entry, "marketplace", str, where), field(path, entry, "pin", str, where), ref
            )
    extensions = field(path, data, "gh_extensions", dict)
    for repository, tag in extensions.items():
        if not REPOSITORY.fullmatch(repository):
            raise RecordError(path, f"gh_extensions.{repository}", "must be <owner>/<repository>")
        if type(tag) is not str or not tag or re.search(r"\s", tag):
            raise RecordError(path, f"gh_extensions.{repository}", "must be one tag string")
        clean(path, f"gh_extensions.{repository}", tag)
    return PluginPins(agents["claude"], agents["codex"], dict(extensions))


# --- ~/.claude/plugins/installed_plugins.json ----------------------------------------------------------------


@dataclass(frozen=True)
class ClaudeInstall:
    scope: str
    version: str
    install_path: str
    project_path: Optional[str]


def load_claude_installs(path: Path) -> Optional[Dict[str, List[ClaudeInstall]]]:
    """Every installation record, or None when the file is absent.

    Required per entry: scope (one of Claude Code's scopes), version, installPath (exactly
    <this file's directory>/cache/<marketplace>/<plugin>/<version>, with the record's own version: the identity), and projectPath for project or local scope.
    """
    data = load_json(path)
    if data is ABSENT:
        return None
    plugins = field(path, data, "plugins", dict)
    result: Dict[str, List[ClaudeInstall]] = {}
    for plugin_id, entries in plugins.items():
        plugin, marketplace = plugin_parts(path, f"plugins.{plugin_id}", plugin_id)
        if type(entries) is not list:
            raise RecordError(path, f"plugins.{plugin_id}", "must be a list of installations")
        result[plugin_id] = []
        for index, entry in enumerate(entries):
            where = f"plugins.{plugin_id}[{index}]."
            scope = field(path, entry, "scope", str, where)
            if scope not in CLAUDE_SCOPES:
                raise RecordError(path, f"{where}scope", f"{scope!r} is not one of {CLAUDE_SCOPES}")
            version = field(path, entry, "version", str, where)
            install_path = field(path, entry, "installPath", str, where)
            plugin_dir = confined(path, f"plugins.{plugin_id}", path.parent / "cache", marketplace, plugin)
            expected = confined(path, f"{where}version", plugin_dir, version)
            if Path(install_path) != expected:
                raise RecordError(path, f"{where}installPath", f"{install_path!r} is not {str(expected)!r}")
            project = field(path, entry, "projectPath", str, where) if scope in ("project", "local") else None
            # One record per identity (scope, project): a second one would let a reader pick either version.
            if any((seen.scope, seen.project_path) == (scope, project) for seen in result[plugin_id]):
                raise RecordError(
                    path, f"{where}scope", f"a second {scope}-scope record{' for ' + project if project else ''}"
                )
            result[plugin_id].append(ClaudeInstall(scope, version, install_path, project))
    return result


# --- ~/.claude/settings.json enabledPlugins -------------------------------------------------------------------


def load_claude_enabled(path: Path) -> Optional[Dict[str, bool]]:
    """enabledPlugins as {plugin id: bool}, {} when unset, None when the settings file is absent."""
    data = load_json(path)
    if data is ABSENT:
        return None
    if not isinstance(data, dict):
        raise RecordError(path, "(top)", "must be an object")
    if "enabledPlugins" not in data:
        return {}
    enabled = data["enabledPlugins"]
    if not isinstance(enabled, dict):
        raise RecordError(path, "enabledPlugins", f"must be an object, not {type(enabled).__name__}")
    for plugin_id, value in enabled.items():
        plugin_parts(path, f"enabledPlugins.{plugin_id}", plugin_id)
        if type(value) is not bool:
            raise RecordError(path, f"enabledPlugins.{plugin_id}", f"must be a boolean, not {type(value).__name__}")
    return dict(enabled)


# --- `claude plugin marketplace list --json` -------------------------------------------------------------------


def claude_marketplace_state(listing: str, name: str, recorded: str) -> str:
    """`registered` when NAME is registered from RECORDED (GitHub owner/repo), `foreign` when NAME is registered
    from anything else, `absent` when it is not registered; an unreadable listing raises."""
    record = "claude plugin marketplace list --json"
    try:
        data = json.loads(listing)
    except ValueError as error:
        raise RecordError(record, "(output)", f"not JSON: {error}") from error
    if type(data) is not list:
        raise RecordError(record, "(output)", "must be a list")
    for index, entry in enumerate(data):
        if field(record, entry, "name", str, f"[{index}].") != name:
            continue
        if field(record, entry, "source", str, f"[{index}].") != "github":
            return "foreign"
        return "registered" if field(record, entry, "repo", str, f"[{index}].") == recorded else "foreign"
    return "absent"


# --- Codex: plugin cache, marketplace install record, config.toml ----------------------------------------------


@dataclass(frozen=True)
class CodexCopy:
    version_dir: str
    name: str
    version: str


def codex_version_order(script: Path) -> Tuple[Callable[[str, str], int], Any]:
    """Codex's version order and version-name rule, from the base modify script's generated hook-trust block."""
    text = read_text(script)
    if text is None:
        raise RecordError(script, "(file)", "is missing")
    try:
        block = text.split("# >>> codex hook trust", 1)[1].split("# <<< codex hook trust", 1)[0]
        namespace: Dict[str, Any] = {"sys": sys, "Path": Path}
        with redirect_stderr(io.StringIO()):
            exec(block.split("\n", 1)[1], namespace)
        return namespace["compare_plugin_versions"], namespace["PLUGIN_VERSION_SEGMENT"]
    except (Exception, SystemExit) as error:
        raise RecordError(script, "codex hook trust block", f"cannot evaluate: {error!r}") from error


def load_codex_copy(root: Path, plugin: str, script: Path) -> Optional[CodexCopy]:
    """The copy Codex loads from ROOT (~/.codex/plugins/cache/<marketplace>/<plugin>), None when ROOT is absent.

    Codex's rule (core-plugin-common installed.rs active_plugin_version): among ROOT's entries that are real
    directories (lstat: a symlink is not a version) named by the version segment, `local` wins, else the
    highest by Codex's version order. That copy's .codex-plugin/plugin.json must name PLUGIN and hold a
    string version.
    """
    try:
        entries = list(root.iterdir())
    except (FileNotFoundError, NotADirectoryError):
        return None
    except OSError as error:
        raise RecordError(root, "(directory)", f"cannot list: {error!r}") from error
    compare, segment = codex_version_order(script)
    versions = []
    for entry in entries:
        try:
            mode = entry.lstat().st_mode
        except FileNotFoundError:
            continue
        except OSError as error:
            raise RecordError(entry, "(entry)", f"cannot stat: {error!r}") from error
        if stat.S_ISDIR(mode) and segment.fullmatch(entry.name):
            versions.append(entry.name)
    if not versions:
        raise RecordError(root, "(directory)", "holds no version directory")
    active = "local" if "local" in versions else max(versions, key=functools.cmp_to_key(compare))
    manifest_path = confined(root, "(version directory)", root, active) / ".codex-plugin/plugin.json"
    manifest = load_json(manifest_path)
    if manifest is ABSENT:
        raise RecordError(manifest_path, "(file)", "is missing")
    name = field(manifest_path, manifest, "name", str)
    if name != plugin:
        raise RecordError(manifest_path, "name", f"{name!r} is not {plugin!r}")
    return CodexCopy(active, name, field(manifest_path, manifest, "version", str))


@dataclass(frozen=True)
class MarketplaceInstall:
    source: str
    revision: str


def load_marketplace_install(path: Path, expected_source: str) -> Optional[MarketplaceInstall]:
    """The git marketplace clone's install record, None when absent; its source must be the pinned one."""
    data = load_json(path)
    if data is ABSENT:
        return None
    if field(path, data, "source_type", str) != "git":
        raise RecordError(path, "source_type", "must be git")
    source = field(path, data, "source", str)
    if source != expected_source:
        raise RecordError(path, "source", f"{source!r} is not the pinned {expected_source!r}")
    revision = field(path, data, "revision", str)
    if not COMMIT.fullmatch(revision):
        raise RecordError(path, "revision", "must be a 40-hex commit")
    return MarketplaceInstall(source, revision)


@dataclass(frozen=True)
class CodexConfig:
    plugins: Dict[str, bool]
    marketplaces: Dict[str, Dict[str, Any]]


def load_codex_config(path: Path) -> Optional[CodexConfig]:
    """[plugins."<id>"] enabled flags and [marketplaces.<name>] tables, None when config.toml is absent."""
    data = load_toml(path)
    if data is ABSENT:
        return None
    plugins = data["plugins"] if "plugins" in data else {}
    if not isinstance(plugins, dict):
        raise RecordError(path, "plugins", "must be a table")
    enabled = {}
    for plugin_id, table in plugins.items():
        plugin_parts(path, f"plugins.{plugin_id}", plugin_id)
        enabled[plugin_id] = field(path, table, "enabled", bool, f"plugins.{plugin_id}.")
    marketplaces = data["marketplaces"] if "marketplaces" in data else {}
    if not isinstance(marketplaces, dict):
        raise RecordError(path, "marketplaces", "must be a table")
    for name, table in marketplaces.items():
        clean(path, f"marketplaces.{name!r}", name)
        field(path, table, "source_type", str, f"marketplaces.{name}.")
        field(path, table, "source", str, f"marketplaces.{name}.")
        optional(path, table, "ref", str, f"marketplaces.{name}.")
    return CodexConfig(enabled, dict(marketplaces))


def codex_marketplace_state(path: Path, name: str, expected_source: str) -> str:
    """`registered` when config.toml declares marketplace NAME from EXPECTED_SOURCE, else `absent`."""
    config = load_codex_config(path)
    if config is None or name not in config.marketplaces:
        return "absent"
    source = config.marketplaces[name]["source"]
    if source != expected_source:
        raise RecordError(path, f"marketplaces.{name}.source", f"{source!r} is not {expected_source!r}")
    return "registered"


# --- gh extension manifest.yml ---------------------------------------------------------------------------------


@dataclass(frozen=True)
class GhExtension:
    owner: str
    name: str
    tag: str
    pinned: bool


def load_gh_extension(gh_dir: Path, repository: str) -> Optional[GhExtension]:
    """gh's record of an installed binary extension, None when its directory is absent.

    gh writes <gh data dir>/extensions/<name>/manifest.yml as `key: value` lines (agent_home("gh")). owner, name, host, tag,
    ispinned and path are required; owner/name must be REPOSITORY and host github.com, so a fork's copy of
    the same name is foreign. A directory without a readable manifest cannot be verified and raises.
    """
    if not REPOSITORY.fullmatch(repository):
        raise RecordError(gh_dir, "repository", f"{repository!r} is not <owner>/<repository>")
    owner, name = repository.split("/", 1)
    directory = confined(gh_dir, "repository", gh_dir / "extensions", name)
    if not present(directory):
        return None
    manifest = directory / "manifest.yml"
    text = read_text(manifest)
    if text is None:
        raise RecordError(manifest, "(file)", "is missing beside an installed extension; cannot verify its pin")
    values: Dict[str, str] = {}
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([a-z]+): ?(.*)", line)
        if not match or match.group(1) in values:
            raise RecordError(manifest, f"line {number}", f"is not one `key: value` line: {line!r}")
        values[match.group(1)] = clean(manifest, match.group(1), match.group(2).strip())
    for key in ("owner", "name", "host", "tag", "ispinned", "path"):
        if not values.get(key):
            raise RecordError(manifest, key, "is missing")
    if (values["owner"], values["name"]) != (owner, name):
        raise RecordError(manifest, "owner/name", f"{values['owner']}/{values['name']} is not {repository}")
    binary = confined(manifest, "path", directory, name)
    if Path(values["path"]) != binary:
        raise RecordError(manifest, "path", f"{values['path']!r} is not {str(binary)!r}")
    if values["host"] != "github.com":
        raise RecordError(manifest, "host", f"{values['host']!r} is not github.com")
    if re.search(r"\s", values["tag"]):
        raise RecordError(manifest, "tag", f"{values['tag']!r} is not one tag")
    if values["ispinned"] not in ("true", "false"):
        raise RecordError(manifest, "ispinned", "must be true or false")
    return GhExtension(owner, name, values["tag"], values["ispinned"] == "true")


# --- the applied mise config's Held entries --------------------------------------------------------------------


def load_mise_holds(path: Path) -> List[str]:
    """The [tools] entries whose comment block directly above them says `Held`; every one must be a tool.

    Read as text, with no TOML library, so a host whose python3 predates tomllib (a fresh macOS) still runs
    it: a Held comment must sit directly above a key of the [tools] table or a [tools."<name>"] header, and a
    Held comment above anything else is an error, never a silently unheld tool.
    """
    text = read_text(path)
    if text is None:
        raise RecordError(path, "(file)", "is missing")
    section, held, names = None, None, []
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            held = held or (number if "Held" in stripped else None)
            continue
        header = re.fullmatch(r"\[([^\]]+)\]", stripped)
        key = re.match(r'^("[^"]+"|[A-Za-z0-9_.:@/-]+)\s*=', stripped)
        name = None
        if header:
            section = header.group(1)
            tool = re.fullmatch(r'tools\."([^"]+)"', section)
            name = tool.group(1) if tool else None
        elif key and section == "tools":
            name = key.group(1).strip('"')
        if held is not None:
            if name is not None:
                clean(path, f"line {number}", name)
            if name is None:
                raise RecordError(path, f"line {held}", "a Held comment must sit directly above a [tools] entry")
            names.append(name)
        held = None
    if held is not None:
        raise RecordError(path, f"line {held}", "a Held comment must sit directly above a [tools] entry")
    return names


# --- command line ----------------------------------------------------------------------------------------------


def main(argv: List[str]) -> int:
    command, args = argv[0], argv[1:]
    if command == "plugin-pin":
        pins = load_plugin_pins(Path(args[0]))
        entry = getattr(pins, args[1]).get(args[2])
        value = getattr(entry, args[3], None) if entry is not None else None
        if value is None:
            raise RecordError(args[0], f"{args[1]}.{args[2]}.{args[3]}", "is not recorded")
        print(value)
    elif command == "agent-home":
        print(agent_home(args[0]))
    elif command == "plugin-ids":
        print("\n".join(sorted(getattr(load_plugin_pins(Path(args[0])), args[1]))))
    elif command == "claude-installs":
        # Structured output: one JSON list, never field-separated text a value could forge rows in.
        installs = load_claude_installs(Path(args[0])) or {}
        rows = [
            {
                "scope": entry.scope,
                "version": entry.version,
                "installPath": entry.install_path,
                "projectPath": entry.project_path,
            }
            for entry in installs.get(args[1], [])
        ]
        print(json.dumps(rows))
    elif command == "claude-enabled":
        enabled = load_claude_enabled(Path(args[0])) or {}
        value = enabled.get(args[1])
        print("unset" if value is None else ("enabled" if value else "disabled"))
    elif command == "claude-marketplace":
        print(claude_marketplace_state(sys.stdin.read(), args[0], args[1]))
    elif command == "codex-copy":
        copy = load_codex_copy(Path(args[0]), args[1], Path(args[2]))
        if copy is not None:
            print(copy.version)
    elif command == "marketplace-install":
        install = load_marketplace_install(Path(args[0]), args[1])
        if install is not None:
            print(install.revision)
    elif command == "codex-marketplace":
        print(codex_marketplace_state(Path(args[0]), args[1], args[2]))
    elif command == "codex-marketplace-pinned":
        # Exit 0 when config.toml declares marketplace NAME from SOURCE at exactly REF, 1 when it is absent or
        # has another or no ref (an upgrade would then fetch something else), 2 when it cannot be read.
        config = load_codex_config(Path(args[0]))
        table = config.marketplaces.get(args[1]) if config is not ABSENT and config is not None else None
        if table is None:
            return 1
        if table["source"] != args[2]:
            raise RecordError(args[0], f"marketplaces.{args[1]}.source", f"{table['source']!r} is not {args[2]!r}")
        return 0 if table.get("ref") == args[3] else 1
    elif command == "gh-extension":
        extension = load_gh_extension(Path(args[0]), args[1])
        print("absent" if extension is None else f"{extension.tag} {'true' if extension.pinned else 'false'}")
    elif command == "mise-holds":
        print("\n".join(load_mise_holds(Path(args[0]))))
    elif command == "is-held":
        # One question for the shell: exit 0 held, 1 not held, 2 the config cannot be read (never "not held").
        return 0 if args[1] in load_mise_holds(Path(args[0])) else 1
    elif command == "is-pinned-extension":
        # Exit 0 when REPOSITORY, or any extension of the same name (gh upgrades by name, so a fork of a pinned
        # extension would move it), is pinned; 1 when not; 2 when the pins or the repository cannot be read.
        repository = args[1]
        if not REPOSITORY.fullmatch(repository):
            raise RecordError("gh extension list", repository, "is not <owner>/<repository>")
        pinned = load_plugin_pins(Path(args[0])).gh_extensions
        name = repository.split("/", 1)[1]
        return 0 if any(entry.split("/", 1)[1] == name for entry in pinned) else 1
    else:
        raise RecordError("pin_records.py", command, "is not a command")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (RecordError, IndexError, ImportError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2) from None
