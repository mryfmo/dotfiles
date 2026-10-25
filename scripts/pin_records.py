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

import errno
import functools
import hashlib
import io
import json
import os
import re
import stat
import sys
from contextlib import redirect_stderr
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

# One path component taken from record data (see confined): it starts with a letter or digit, so it is never
# empty, `.`, `..` or absolute, and holds no separator.
COMPONENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]*")
PLUGIN_ID = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)@([A-Za-z0-9][A-Za-z0-9._-]*)$")
REPOSITORY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
# A Claude Code plugin whose listing and manifest give no version gets the marketplace commit as its version, which
# moves with every commit to the marketplace; its pin is then the content it was reviewed at (content_sha256).
CONTENT_PIN = re.compile(r"^sha256:[0-9a-f]{64}$")
# Claude Code's own bookkeeping at the top of a cache version directory, not plugin content: the cleanup marker
# written into a superseded version (plugins loading reference, "Cleanup of previous versions") and the lock
# directory a running session keeps there.
CLAUDE_CACHE_MARKERS = (".orphaned_at", ".in_use")
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
    """The text of PATH exactly as stored (no newline translation, so a \\r is seen, not turned into a line
    break), None when absent; any other failure raises RecordError."""
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return handle.read()
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


def field(record: object, data: Any, name: str, kind: type, where: str = "", ascii: bool = False) -> Any:
    """DATA[NAME] with exactly type KIND (bool is never an int, an int never a str); a string is clean, and
    with ASCII (an id, version, tag, scope, source or commit: an identity value) ASCII and never empty."""
    label = f"{where}{name}"
    if not isinstance(data, dict):
        raise RecordError(record, where.rstrip(".") or "(top)", f"must be an object, not {type(data).__name__}")
    if name not in data:
        raise RecordError(record, label, "is missing")
    value = data[name]
    if type(value) is not kind:
        raise RecordError(record, label, f"must be {kind.__name__}, not {type(value).__name__}")
    if kind is str:
        clean(record, label, value, ascii)
    return value


# Every C0/C1 control character and the Unicode line and paragraph separators: str.splitlines() breaks a line at
# \x0b, \x0c, \x1c-\x1e, \x85, \u2028 and \u2029 as well as \n, so any of them could forge a record line or field.
CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f\u2028\u2029]")
CONTROL_BUT_TAB = re.compile(r"[\x00-\x08\x0a-\x1f\x7f-\x9f\u2028\u2029]")


def record_lines(record: object, text: str, tab: bool = False) -> List[str]:
    """TEXT split into lines at \\n only, after refusing the whole file when it holds any other control
    character (a tab only when TAB: the format allows it) or a Unicode line separator."""
    lines = text.split("\n")
    for number, line in enumerate(lines, 1):
        found = (CONTROL_BUT_TAB if tab else CONTROL).search(line)
        if found:
            raise RecordError(
                record, f"line {number}", f"contains a control character or line separator: {found.group()!r}"
            )
    return lines[:-1] if lines and lines[-1] == "" else lines


def clean(record: object, label: str, value: str, ascii: bool = False) -> str:
    """VALUE exactly as recorded, else RecordError: it holds no control character (tab, newline, carriage
    return, NUL, ...), so no field can forge a row or a record boundary in any output; it has no leading or
    trailing whitespace of any kind (str.isspace: NBSP, U+2009, U+3000, ...), which a reader that stripped
    it would have turned into another value; and with ASCII (an identity value: id, version, tag, scope,
    source, commit) it is not empty and holds ASCII only, so an empty version never reads as "no version".
    Values are never stripped: every comparison is of the exact string."""
    if CONTROL.search(value):
        raise RecordError(record, label, f"contains a control character: {value!r}")
    if value and (value[0].isspace() or value[-1].isspace()):
        raise RecordError(record, label, f"has leading or trailing whitespace: {value!r}")
    if ascii and not value:
        raise RecordError(record, label, "is empty")
    if ascii and not value.isascii():
        raise RecordError(record, label, f"must be ASCII: {value!r}")
    return value


def optional(record: object, data: Dict[str, Any], name: str, kind: type, where: str = "", ascii: bool = False) -> Any:
    """DATA[NAME] when the key is there, None only when it is missing: a present key, explicit null
    included, must have type KIND, so null never stands in for "not recorded"."""
    if not isinstance(data, dict):
        raise RecordError(record, where.rstrip(".") or "(top)", f"must be an object, not {type(data).__name__}")
    return field(record, data, name, kind, where, ascii) if name in data else None


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
            ref = optional(path, entry, "ref", str, where, ascii=True)
            if ref is not None and not COMMIT.fullmatch(ref):
                raise RecordError(path, f"{where}ref", "must be a 40-hex commit")
            agents[agent][plugin_id] = Pin(
                field(path, entry, "marketplace", str, where, ascii=True),
                content_pin(path, entry, where, agent),
                ref,
            )
    extensions = field(path, data, "gh_extensions", dict)
    for repository, tag in extensions.items():
        if not REPOSITORY.fullmatch(repository):
            raise RecordError(path, f"gh_extensions.{repository}", "must be <owner>/<repository>")
        if type(tag) is not str or not tag or re.search(r"\s", tag):
            raise RecordError(path, f"gh_extensions.{repository}", "must be one tag string")
        clean(path, f"gh_extensions.{repository}", tag, ascii=True)
    return PluginPins(agents["claude"], agents["codex"], dict(extensions))


def content_pin(path: Path, entry: Any, where: str, agent: str) -> str:
    """A plugin's recorded pin; one in the content form (CONTENT_PIN) is valid only for Claude Code."""
    pin = field(path, entry, "pin", str, where, ascii=True)
    if pin.startswith("sha256:") and (agent != "claude" or not CONTENT_PIN.fullmatch(pin)):
        raise RecordError(path, f"{where}pin", "a content pin is sha256:<64 lowercase hex>, for Claude Code only")
    return pin


def canonical_entry(entry: Any) -> bytes:
    """A marketplace catalog entry as canonical JSON: sorted keys, no whitespace, UTF-8, no NaN or Infinity."""
    if not isinstance(entry, dict):
        raise RecordError("marketplace.json", "(entry)", "a catalog entry must be a JSON object")
    try:
        return json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
    except (ValueError, UnicodeEncodeError) as error:
        raise RecordError("marketplace.json", "(entry)", f"has no canonical JSON form ({error})") from None


def content_digest(files: Iterable[Tuple[bytes, bytes]], entry: Any) -> str:
    """The content pin of a Claude Code plugin: what Claude Code loads for it, which is its catalog entry in the
    marketplace's .claude-plugin/marketplace.json (with `strict: false` the entry alone may define hooks, commands,
    MCP or LSP servers) and the regular files of its plugin directory, given as (relative POSIX path, bytes).

    `sha256:` and the hex SHA-256 over, in this order: `catalog-entry NUL <size> NUL <canonical_entry(entry)>`, then
    each file in the byte order of its path as `<relative path> NUL <size> NUL <bytes>`. The entry record always
    comes first and every record carries its size, so the stream has one reading. The one definition: content_sha256
    feeds it an installed copy and the entry from the installed marketplace clone, scripts/drift-watch.py the upstream
    directory's blobs and the upstream catalog entry. A path whose first component is one of CLAUDE_CACHE_MARKERS is
    left out."""
    digest = hashlib.sha256()
    canonical = canonical_entry(entry)
    digest.update(b"catalog-entry\0" + str(len(canonical)).encode() + b"\0" + canonical)
    for relative, data in sorted(files, key=lambda item: item[0]):
        if relative.split(b"/", 1)[0].decode("utf-8", "surrogateescape") in CLAUDE_CACHE_MARKERS:
            continue
        digest.update(relative + b"\0" + str(len(data)).encode() + b"\0" + data)
    return "sha256:" + digest.hexdigest()


def unique_object(pairs: List[Tuple[str, Any]]) -> Dict[str, Any]:
    keys = [key for key, _ in pairs]
    if len(set(keys)) != len(keys):
        raise ValueError(f"duplicate key in {keys}")
    return dict(pairs)


def refuse_constant(name: str) -> Any:
    raise ValueError(f"{name} is not JSON")


def read_catalog_entry(marketplace_root: Path, plugin: str) -> Dict[str, Any]:
    """PLUGIN's entry in the marketplace clone MARKETPLACE_ROOT (.claude-plugin/marketplace.json), read fd-relative:
    the root is opened with O_DIRECTORY|O_NOFOLLOW, then .claude-plugin and marketplace.json below it without
    following a symlink, the file regular and the same device and inode as its lstat. The JSON must have no duplicate
    key and no NaN or Infinity, and the catalog must list PLUGIN exactly once."""
    where = marketplace_root / ".claude-plugin/marketplace.json"
    fds: List[int] = []
    try:
        try:
            fds.append(os.open(marketplace_root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW))
            fds.append(os.open(".claude-plugin", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fds[-1]))
            status = os.stat("marketplace.json", dir_fd=fds[-1], follow_symlinks=False)
            if not stat.S_ISREG(status.st_mode):
                raise RecordError(where, "(file)", "is not a regular file")
            fd = open_regular("marketplace.json", status, fds[-1])
            if fd is None:
                raise RecordError(where, "(file)", "changed while it was read")
            with os.fdopen(fd, "rb") as handle:
                raw = handle.read()
        except OSError as error:
            raise RecordError(where, "(file)", f"cannot read ({error})") from None
    finally:
        for opened in fds:
            os.close(opened)
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object, parse_constant=refuse_constant)
    except ValueError as error:
        raise RecordError(where, "(file)", f"not strict JSON: {error}") from None
    plugins = field(where, data, "plugins", list)
    matches = [item for item in plugins if isinstance(item, dict) and item.get("name") == plugin]
    if len(matches) != 1:
        raise RecordError(where, f"plugins[{plugin}]", f"is listed {len(matches)} times, not once")
    return matches[0]


def content_sha256(root: Path, entry: Any) -> str:
    """The content pin (content_digest) of the plugin directory ROOT with its catalog entry ENTRY.

    File order on disk, mtimes, modes and empty directories do not count, and CLAUDE_CACHE_MARKERS at the top level
    are not read. The walk is fd-relative end to end: the root is opened with O_DIRECTORY|O_NOFOLLOW, and every entry
    below it is lstat'ed (fstatat) and opened (openat, O_NOFOLLOW) relative to its parent's open directory, never by
    a path walked again. So no symlink is followed anywhere below the root (the root included), and each directory
    and file read is the one its lstat showed (same device and inode). A symlink, or anything that is neither a
    regular file nor a directory, refuses: it is not reviewable content.
    """
    try:
        root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as error:
        if error.errno in (errno.ELOOP, errno.ENOTDIR):
            raise RecordError(root, "(directory)", "is not a real directory") from None
        raise RecordError(root, "(directory)", f"cannot open ({error})") from None
    contents: List[Tuple[bytes, bytes]] = []

    def walk(dir_fd: int, prefix: str) -> None:
        try:
            names = [entry.name for entry in os.scandir(dir_fd)]
        except OSError as error:
            raise RecordError(root, prefix or ".", f"cannot list ({error})") from None
        for name in names:
            relative = f"{prefix}{name}"
            if not prefix and name in CLAUDE_CACHE_MARKERS:
                continue
            try:
                status = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
            except OSError as error:
                raise RecordError(root, relative, f"cannot lstat ({error})") from None
            if stat.S_ISDIR(status.st_mode):
                try:
                    child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=dir_fd)
                except OSError as error:
                    if error.errno in (errno.ELOOP, errno.ENOTDIR):
                        raise RecordError(root, relative, "changed while it was read") from None
                    raise RecordError(root, relative, f"cannot open ({error})") from None
                try:
                    opened = os.fstat(child)
                    if (opened.st_dev, opened.st_ino) != (status.st_dev, status.st_ino):
                        raise RecordError(root, relative, "changed while it was read")
                    walk(child, relative + "/")
                finally:
                    os.close(child)
            elif stat.S_ISREG(status.st_mode):
                try:
                    fd = open_regular(name, status, dir_fd)
                    if fd is None:
                        raise RecordError(root, relative, "changed while it was read")
                    with os.fdopen(fd, "rb") as handle:
                        contents.append((os.fsencode(relative), handle.read()))
                except OSError as error:
                    raise RecordError(root, relative, f"cannot read ({error})") from None
            else:
                raise RecordError(
                    root, relative, "is a symlink or special file; a content pin covers regular files only"
                )

    try:
        walk(root_fd, "")
    finally:
        os.close(root_fd)
    return content_digest(contents, entry)


def open_regular(name: Any, status: os.stat_result, dir_fd: Optional[int] = None) -> Optional[int]:
    """Open NAME (relative to DIR_FD when given), which lstat showed as the regular file STATUS, for reading; None
    when it is now something else.

    O_NOFOLLOW refuses a symlink swapped in, O_NONBLOCK keeps a FIFO swapped in from blocking the open, and fstat
    must show the same regular file (device and inode) lstat showed.
    """
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=dir_fd)
    except OSError as error:
        if error.errno == errno.ELOOP:
            return None
        raise
    opened = os.fstat(fd)
    if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (status.st_dev, status.st_ino):
        os.close(fd)
        return None
    return fd


def claude_observed(pin: str, version: str, install_path: str) -> str:
    """What a Claude Code installation is compared with its pin by: its content for a content pin, else its version.

    installPath is <plugins>/cache/<marketplace>/<plugin>/<version> (load_claude_installs checks that shape), so the
    catalog entry Claude Code loads beside the copy is read from the installed marketplace clone
    <plugins>/marketplaces/<marketplace>."""
    if not CONTENT_PIN.fullmatch(pin):
        return version
    copy = Path(install_path)
    plugin, marketplace, plugins_dir = copy.parent.name, copy.parent.parent.name, copy.parents[3]
    entry = read_catalog_entry(plugins_dir / "marketplaces" / marketplace, plugin)
    return content_sha256(copy, entry)


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
            scope = field(path, entry, "scope", str, where, ascii=True)
            if scope not in CLAUDE_SCOPES:
                raise RecordError(path, f"{where}scope", f"{scope!r} is not one of {CLAUDE_SCOPES}")
            version = field(path, entry, "version", str, where, ascii=True)
            install_path = field(path, entry, "installPath", str, where)
            plugin_dir = confined(path, f"plugins.{plugin_id}", path.parent / "cache", marketplace, plugin)
            expected = confined(path, f"{where}version", plugin_dir, version)
            if Path(install_path) != expected:
                raise RecordError(path, f"{where}installPath", f"{install_path!r} is not {str(expected)!r}")
            project = field(path, entry, "projectPath", str, where) if scope in ("project", "local") else None
            if project == "":
                raise RecordError(path, f"{where}projectPath", "is empty")
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
        if field(record, entry, "name", str, f"[{index}].", ascii=True) != name:
            continue
        if field(record, entry, "source", str, f"[{index}].", ascii=True) != "github":
            return "foreign"
        return "registered" if field(record, entry, "repo", str, f"[{index}].", ascii=True) == recorded else "foreign"
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
    name = field(manifest_path, manifest, "name", str, ascii=True)
    if name != plugin:
        raise RecordError(manifest_path, "name", f"{name!r} is not {plugin!r}")
    return CodexCopy(active, name, field(manifest_path, manifest, "version", str, ascii=True))


@dataclass(frozen=True)
class MarketplaceInstall:
    source: str
    revision: str


def load_marketplace_install(path: Path, expected_source: str) -> Optional[MarketplaceInstall]:
    """The git marketplace clone's install record, None when absent; its source must be the pinned one."""
    data = load_json(path)
    if data is ABSENT:
        return None
    if field(path, data, "source_type", str, ascii=True) != "git":
        raise RecordError(path, "source_type", "must be git")
    source = field(path, data, "source", str, ascii=True)
    if source != expected_source:
        raise RecordError(path, "source", f"{source!r} is not the pinned {expected_source!r}")
    revision = field(path, data, "revision", str, ascii=True)
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
        clean(path, f"marketplaces.{name!r}", name, ascii=True)
        field(path, table, "source_type", str, f"marketplaces.{name}.", ascii=True)
        field(path, table, "source", str, f"marketplaces.{name}.", ascii=True)
        optional(path, table, "ref", str, f"marketplaces.{name}.", ascii=True)
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
    for number, line in enumerate(record_lines(manifest, text), 1):
        if line == "":
            continue
        # gh writes `key: value` with one space; the value is taken exactly, never stripped (clean refuses
        # leading or trailing whitespace of any kind).
        match = re.fullmatch(r"([a-z]+):(?: (.*))?", line)
        if not match or match.group(1) in values:
            raise RecordError(manifest, f"line {number}", f"is not one `key: value` line: {line!r}")
        key, value = match.group(1), match.group(2) or ""
        values[key] = clean(manifest, key, value, ascii=key != "path")
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
    # TOML allows a tab as whitespace; nothing else.
    for number, line in enumerate(record_lines(path, text, tab=True), 1):
        # TOML whitespace is a space or a tab, nothing else (a no-break space is part of the line).
        stripped = line.strip(" \t")
        if stripped.startswith("#"):
            held = held or (number if "Held" in stripped else None)
            continue
        header = re.fullmatch(r"\[([^\]]+)\]", stripped)
        key = re.match(r'^("[^"]+"|[A-Za-z0-9_.:@/-]+)[ \t]*=', stripped)
        name = None
        if header:
            section = header.group(1)
            tool = re.fullmatch(r'tools\."([^"]+)"', section)
            name = tool.group(1) if tool else None
        elif key and section == "tools":
            name = key.group(1).strip('"')
        if held is not None:
            if name is not None:
                clean(path, f"line {number}", name, ascii=True)
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
        # Explicit for the shell: `absent`, or `copy <version>`; an empty answer is never a state.
        copy = load_codex_copy(Path(args[0]), args[1], Path(args[2]))
        print("absent" if copy is None else f"copy {copy.version}")
    elif command == "marketplace-install":
        install = load_marketplace_install(Path(args[0]), args[1])
        print("absent" if install is None else f"revision {install.revision}")
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
    elif command == "content-sha256":
        # PLUGIN_DIR MARKETPLACE_ROOT PLUGIN: the content pin of a plugin directory with its entry in that clone.
        print(content_sha256(Path(args[0]), read_catalog_entry(Path(args[1]), args[2])))
    elif command == "claude-observed":
        # PIN VERSION INSTALL_PATH: the value make update compares with the pin (claude_observed).
        print(claude_observed(args[0], args[1], args[2]))
    else:
        raise RecordError("pin_records.py", command, "is not a command")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (RecordError, IndexError, ImportError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2) from None
