#!/usr/bin/env python3
"""Generate agent-native configuration from the shared AI-agent manifest."""

from __future__ import annotations

import argparse
import copy
import glob
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, NoReturn

try:
    import yaml
except ImportError:  # pragma: no cover - CI installs PyYAML for this script.
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "home/dot_agents/agent-config.yaml"
GENERATED_HEADER = "Generated from home/dot_agents/agent-config.yaml by scripts/generate-agent-configs.py."


def fail(message: str) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_exact(path: Path) -> str:
    """A file's exact text: UTF-8 with no newline translation, so a CRLF byte stays visible to every comparison."""
    return path.read_bytes().decode()


def write_exact(path: Path, content: str) -> None:
    path.write_bytes(content.encode())


def load_manifest(text: str | None = None) -> dict[str, Any]:
    """The parsed manifest: `text` when given (main's in-memory copy with refreshed lever pins), else the file."""
    return parse_manifest(read_exact(MANIFEST_PATH) if text is None else text)


def parse_manifest(text: str) -> dict[str, Any]:
    if yaml is None:
        fail("PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        fail(f"{MANIFEST_PATH} must contain a YAML mapping")
    if data.get("schema_version") != 1:
        fail(f"{MANIFEST_PATH} schema_version must be 1")
    return data


# The coordinator's levers (regime-cutover U31): the checkout script is the source, the generated chezmoi file installs
# the same bytes (mode 0755, owner-writable) under ~/.local/bin/common, and claude.levers.sha256 pins them for the
# lever's own self-check, which detects a rewritten copy rather than preventing one.
LEVER_SOURCE_DIR = "scripts/orchestrator"
LEVER_INSTALL_DIR = "home/dot_local/bin/common"
LEVER_PIN_LINE = re.compile(r"^(      )([A-Za-z0-9][A-Za-z0-9_.-]*): ([0-9a-f]{64})$")


def lever_names(manifest: dict[str, Any]) -> list[str]:
    return sorted(manifest.get("claude", {}).get("levers", {}).get("sha256", {}))


def lever_sha256(name: str) -> str:
    source = ROOT / LEVER_SOURCE_DIR / name
    if not source.is_file():
        fail(f"claude.levers.sha256 names {name}, but {LEVER_SOURCE_DIR}/{name} is not a file")
    return hashlib.sha256(source.read_bytes()).hexdigest()


def refresh_lever_pins(text: str) -> str:
    """Rewrite each `claude.levers.sha256.<name>` line with the checkout script's sha256, keeping every other line."""
    lines = text.splitlines(keepends=True)
    try:
        start = lines.index("claude:\n")
        levers = lines.index("  levers:\n", start)
        block = lines.index("    sha256:\n", levers)
    except ValueError:
        return text
    index = block + 1
    while index < len(lines) and (pin := LEVER_PIN_LINE.match(lines[index].rstrip("\n"))):
        lines[index] = f"{pin[1]}{pin[2]}: {lever_sha256(pin[2])}\n"
        index += 1
    return "".join(lines)


def lever_pins(manifest: dict[str, Any]) -> dict[Path, str]:
    """Each lever's chezmoi copy and the sha256 claude.levers.sha256 pins it to."""
    pins = manifest.get("claude", {}).get("levers", {}).get("sha256", {})
    return {ROOT / LEVER_INSTALL_DIR / f"executable_{name}": pins[name] for name in lever_names(manifest)}


def render_lever_installs(manifest: dict[str, Any]) -> dict[Path, str]:
    return {
        ROOT / LEVER_INSTALL_DIR / f"executable_{name}": read_exact(ROOT / LEVER_SOURCE_DIR / name)
        for name in lever_names(manifest)
    }


def lever_pin_drift(manifest: dict[str, Any]) -> list[str]:
    """Each lever copy whose bytes do not hash to its pin, so a source and a copy corrupted alike still fail."""
    return [
        f"{path.relative_to(ROOT)} (does not hash to its claude.levers.sha256 pin)"
        for path, pin in lever_pins(manifest).items()
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != pin
    ]


def json_dumps(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def quote_toml(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(quote_toml(item) for item in value) + "]"
    if isinstance(value, dict):
        return (
            "{ " + ", ".join(f"{quote_toml_key(str(key))} = {quote_toml(item)}" for key, item in value.items()) + " }"
        )
    fail(f"unsupported TOML value: {value!r}")


def quote_toml_key(key: str) -> str:
    if re.match(r"^[A-Za-z0-9_-]+$", key):
        return key
    return json.dumps(key, ensure_ascii=False)


def enabled_for(server: dict[str, Any], agent: str) -> bool:
    return bool(server.get("agents", {}).get(agent, False))


PROFILE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
PROFILE_VALUE_RE = re.compile(r"^[A-Za-z0-9._\[\]-]+$")
PROFILE_AGENT_KEYS = {
    "claude": ("model", "effort"),
    "codex": ("model", "model_reasoning_effort"),
    "omp": ("model", "effort"),
}
PROFILE_OPTIONAL_KEYS = {"claude": ("advisor",)}
# The levels omp's `defaultThinkingLevel` setting accepts besides `auto` (omp 18.11.3 src/session/settings.ts:196-201,
# values THINKING_EFFORTS from @oh-my-pi/pi-catalog src/effort.ts:11-18). A seat's level is stated, never `auto`.
OMP_THINKING_LEVELS = ("minimal", "low", "medium", "high", "xhigh", "max")
# omp roles on a Claude model route through the pi-claude-bridge provider, on an OpenAI model through openai-siwc
# (D-024-129/130); anthropic stays expressible as the API-key fallback (gates G1). The openai-codex
# fallback is retired (plan 025 E1, decision 29) and refused with a message of its own.
OMP_MODEL_RE = re.compile(r"^(openai-siwc|anthropic|claude-bridge)/[A-Za-z0-9._-]+$")
# The same routes as a set, for omp.disabled_providers; a test keeps it equal to OMP_MODEL_RE's alternation.
OMP_MODEL_ROUTES = ("openai-siwc", "anthropic", "claude-bridge")
OMP_RETIRED_ROUTES = ("openai-codex",)
# The routes omp itself provides; every other model route exists only while the extension that registers it is loaded,
# so omp.extension_providers must name exactly the remaining routes.
OMP_BUILTIN_ROUTES = ("anthropic",)
OMP_ACCEPTED_ROUTES = "claude-bridge, openai-siwc or anthropic"
CODEX_SANDBOX_MODES = ("read-only", "workspace-write", "danger-full-access")
RUNTIME_PREFIXES = (
    "hooks.state",
    "marketplaces",
    "tui.model_availability_nux",
    "projects",
)


def model_profiles(manifest: dict[str, Any]) -> dict[str, Any]:
    profiles = manifest.get("model_profiles")
    if not isinstance(profiles, dict) or not profiles:
        fail("model_profiles must be a non-empty mapping")
    for required in ("express", "standard"):
        if required not in profiles:
            fail(f"model_profiles must define the {required} profile")
    for name, profile in profiles.items():
        if not PROFILE_NAME_RE.match(str(name)):
            fail(f"model profile name is not launcher-safe: {name}")
        if not isinstance(profile, dict):
            fail(f"model profile {name} must be a mapping")
        for agent, keys in PROFILE_AGENT_KEYS.items():
            mapping = profile.get(agent)
            if not isinstance(mapping, dict):
                fail(f"model profile {name} is missing {agent}")
            optional = PROFILE_OPTIONAL_KEYS.get(agent, ())
            for key in keys + tuple(key for key in optional if key in mapping):
                value = mapping.get(key)
                if agent == "omp" and key == "effort":
                    if value not in OMP_THINKING_LEVELS:
                        fail(
                            f"model profile {name}.omp.effort must be one of {', '.join(OMP_THINKING_LEVELS)}: {value!r}"
                        )
                elif agent == "omp":
                    route = value.split("/", 1)[0] if isinstance(value, str) else None
                    if route in OMP_RETIRED_ROUTES:
                        fail(
                            f"model profile {name}.omp.model names the retired {route} route; use {OMP_ACCEPTED_ROUTES}"
                        )
                    if not isinstance(value, str) or not OMP_MODEL_RE.fullmatch(value):
                        fail(
                            f"model profile {name}.omp.model must be <provider>/<id> "
                            f"with provider {OMP_ACCEPTED_ROUTES}"
                        )
                elif not isinstance(value, str) or not PROFILE_VALUE_RE.match(value):
                    fail(f"model profile {name}.{agent}.{key} must be a launcher-safe string")
        sandbox_mode = profile["codex"].get("sandbox_mode")
        if sandbox_mode is not None and sandbox_mode not in CODEX_SANDBOX_MODES:
            fail(
                f"model profile {name}.codex.sandbox_mode must be one of "
                f"{', '.join(CODEX_SANDBOX_MODES)}: {sandbox_mode!r}"
            )
    return profiles


def interactive_profile(manifest: dict[str, Any]) -> dict[str, Any]:
    profiles = model_profiles(manifest)
    name = manifest.get("interactive_profile")
    if name not in profiles:
        fail(f"interactive_profile must name a model profile: {name!r}")
    return profiles[name]


def codex_marketplace_revision(manifest: dict[str, Any], name: str) -> dict[str, Any]:
    """Return the pinned marketplace revision recorded in assets.codex-plugins."""
    plugin = manifest.get("assets", {}).get("codex-plugins", {}).get("plugins", {}).get(name, {})
    return {key: plugin[key] for key in ("last_updated", "last_revision") if key in plugin}


def asset_field(asset: dict[str, Any], path: str) -> str:
    value: Any = asset
    for part in path.split("."):
        value = value[part]
    return str(value)


PLAIN_PIN_VALUE = re.compile(r"[A-Za-z0-9._+-]+")
SETTABLE_ASSET_FIELD = re.compile(r"(?:fallback\.)?(?:pin|sha256|sha256\.[A-Za-z0-9-]+)")


def set_asset_field(text: str, name: str, path: str, value: str) -> str:
    """Rewrite one scalar under assets.<name> in the manifest text, keeping comments."""
    if not SETTABLE_ASSET_FIELD.fullmatch(path):
        fail(f"--set-asset may change only pin, sha256, or sha256.<arch>, optionally under fallback.: {name}.{path}")
    if not PLAIN_PIN_VALUE.fullmatch(value):
        fail(f"assets.{name}.{path} is not a plain pin value: {value!r}")
    lines = text.splitlines(keepends=True)
    try:
        index = lines.index("assets:\n")
        index = lines.index(f"  {name}:\n", index)
    except ValueError:
        fail(f"agent-config.yaml has no assets.{name} entry")
    parts = path.split(".")
    for depth, part in enumerate(parts):
        indent = " " * (4 + 2 * depth)
        key = f"{indent}{part}:"
        for index in range(index + 1, len(lines)):
            line = lines[index]
            if line.strip() and len(line) - len(line.lstrip(" ")) < len(indent):
                fail(f"assets.{name} has no field {path}")
            if line.startswith(key + " ") or line.rstrip("\n") == key:
                break
        else:
            fail(f"assets.{name} has no field {path}")
    lines[index] = f"{' ' * (4 + 2 * (len(parts) - 1))}{parts[-1]}: {value}\n"
    return "".join(lines)


def render_asset_constants(manifest: dict[str, Any]) -> dict[Path, str]:
    """Rewrite each asset's NAME="..." assignments in its render target files.

    `render:` is one {file, constants} mapping or a list of them, so one pin can
    reach several files; `readonly` and `declare -r` assignments are rewritten.
    """
    outputs: dict[Path, str] = {}
    # One snapshot per real file: entries reaching it through a symlink alias
    # share the first-seen path, so no write restores another entry's values.
    snapshot_paths: dict[Path, Path] = {}
    for name, asset in manifest.get("assets", {}).items():
        render = asset.get("render")
        if not render:
            continue
        for entry in render if isinstance(render, list) else [render]:
            path = snapshot_paths.setdefault((ROOT / entry["file"]).resolve(), ROOT / entry["file"])
            text = outputs.get(path)
            if text is None:
                text = read_exact(path)
            for constant, field in entry["constants"].items():
                pattern = re.compile(rf'^((?:readonly |declare -r )?{re.escape(constant)}=)"[^"$`\\]*"$', re.M)
                value = asset_field(asset, field)
                if not PLAIN_PIN_VALUE.fullmatch(value):
                    fail(f"assets.{name}.{field} is not a plain pin value: {value!r}")
                text, count = pattern.subn(lambda match: f'{match.group(1)}"{value}"', text)
                if count != 1:
                    fail(f"{entry['file']} must assign {constant} exactly once for assets.{name}")
            outputs[path] = text
    return outputs


def codex_command_hook_lines(event: str, hook: dict[str, Any]) -> list[str]:
    """Render one Codex command hook as a [[hooks.<event>]] matcher group."""
    return [
        "",
        f"[[hooks.{quote_toml_key(event)}]]",
        'matcher = "*"',
        "",
        f"[[hooks.{quote_toml_key(event)}.hooks]]",
        'type = "command"',
        f"command = {quote_toml(hook['command'])}",
        f"timeout = {quote_toml(hook['timeout'])}",
        "statusMessage = " + quote_toml(hook["status_message"]),
    ]


def render_codex(manifest: dict[str, Any]) -> str:
    codex = manifest["codex"]
    lines = [
        "#:schema https://developers.openai.com/codex/config-schema.json",
        "# Codex CLI user configuration managed by chezmoi.",
        f"# {GENERATED_HEADER}",
        "# Keep secrets and OAuth state out of this file; use environment variables or",
        "# Codex-managed credential storage for MCP authentication.",
        "",
    ]
    profile_codex = interactive_profile(manifest)["codex"]
    lines.append(f"model = {quote_toml(profile_codex['model'])}")
    lines.append(f"model_reasoning_effort = {quote_toml(profile_codex['model_reasoning_effort'])}")
    for key in (
        "model_reasoning_summary",
        "model_verbosity",
        "personality",
        "approval_policy",
        "sandbox_mode",
        "web_search",
        "check_for_update_on_startup",
        "project_doc_max_bytes",
        "project_doc_fallback_filenames",
    ):
        lines.append(f"{key} = {quote_toml(codex[key])}")
    if codex.get("tui"):
        lines.extend(["", "[tui]"])
        for key, value in codex["tui"].items():
            if isinstance(value, dict):
                continue
            lines.append(f"{key} = {quote_toml(value)}")
        for key, value in codex["tui"].items():
            if not isinstance(value, dict):
                continue
            lines.extend(["", f"[tui.{quote_toml_key(key)}]"])
            for nested_key, nested_value in value.items():
                lines.append(f"{quote_toml_key(str(nested_key))} = {quote_toml(nested_value)}")
    lines.extend(["", "[sandbox_workspace_write]"])
    lines.append(f"network_access = {quote_toml(codex['sandbox_workspace_write']['network_access'])}")
    if codex["sandbox_workspace_write"].get("writable_roots") is not None:
        lines.append(f"writable_roots = {quote_toml(codex['sandbox_workspace_write']['writable_roots'])}")
    lines.extend(["", "[shell_environment_policy]"])
    for key, value in codex["shell_environment_policy"].items():
        lines.append(f"{quote_toml_key(str(key))} = {quote_toml(value)}")

    for name, server in manifest.get("mcp_servers", {}).items():
        if not enabled_for(server, "codex"):
            continue
        lines.extend(["", f"[mcp_servers.{name}]"])
        if server["transport"] == "stdio":
            lines.append(f"command = {quote_toml(server['command'])}")
            if server.get("args"):
                lines.append(f"args = {quote_toml(server['args'])}")
            if server.get("env"):
                lines.append(f"env = {quote_toml(server['env'])}")
            if server.get("env_vars"):
                lines.append(f"env_vars = {quote_toml(server['env_vars'])}")
        elif server["transport"] == "http":
            lines.append(f"url = {quote_toml(server['url'])}")
            if server.get("bearer_token_env_var"):
                lines.append(f"bearer_token_env_var = {quote_toml(server['bearer_token_env_var'])}")
            if server.get("http_headers"):
                lines.append(f"http_headers = {quote_toml(server['http_headers'])}")
            if server.get("env_http_headers"):
                lines.append(f"env_http_headers = {quote_toml(server['env_http_headers'])}")
        else:
            fail(f"unsupported MCP transport for {name}: {server['transport']}")
        for key in (
            "enabled",
            "required",
            "startup_timeout_sec",
            "tool_timeout_sec",
            "supports_parallel_tool_calls",
            "default_tools_approval_mode",
        ):
            if key in server:
                lines.append(f"{key} = {quote_toml(server[key])}")
        if "enabled_tools" in server:
            lines.append(f"enabled_tools = {quote_toml(server['enabled_tools'])}")
        elif "include_tools" in server:
            lines.append(f"enabled_tools = {quote_toml(server['include_tools'])}")
        if "disabled_tools" in server:
            lines.append(f"disabled_tools = {quote_toml(server['disabled_tools'])}")

    lines.extend(["", "[features]"])
    for key, value in codex.get("features", {}).items():
        lines.append(f"{key} = {quote_toml(value)}")
    for plugin_id, plugin_config in codex.get("plugins", {}).items():
        lines.extend(["", f"[plugins.{quote_toml_key(plugin_id)}]"])
        for key, value in plugin_config.items():
            lines.append(f"{quote_toml_key(str(key))} = {quote_toml(value)}")
    for marketplace_name, marketplace_config in codex.get("marketplaces", {}).items():
        lines.extend(["", f"[marketplaces.{quote_toml_key(marketplace_name)}]"])
        marketplace_config = {
            **codex_marketplace_revision(manifest, marketplace_name),
            **marketplace_config,
        }
        for key, value in marketplace_config.items():
            lines.append(f"{quote_toml_key(str(key))} = {quote_toml(value)}")
    # Codex lists every skill under ~/.agents/skills; one whose skills.audience leaves out Codex is disabled by its
    # SKILL.md path (Codex 0.163.0, measured: the directory path disables nothing). The managed baseline owns the
    # array, so the merge replaces every [[skills.config]] entry the live file held.
    for name in codex_disabled_skills(manifest):
        path = f"{{{{ .chezmoi.homeDir }}}}/{SHARED_SKILLS_ROOT.removeprefix('~/')}/{name}/SKILL.md"
        lines.extend(["", "[[skills.config]]", f"path = {quote_toml(path)}", "enabled = false"])
    hooks = codex.get("hooks", {})
    if hooks.get("permission_request"):
        lines.extend(codex_command_hook_lines("PermissionRequest", hooks["permission_request"]))
    # Each entry gets its own [[hooks.<Event>]] table, in manifest order; Codex merges the arrays.
    for hook in hooks.get("command_hooks", []):
        lines.extend(codex_command_hook_lines(hook["event"], hook))
    if hooks.get("state"):
        lines.extend(["", "[hooks.state]"])
        for hook_key, hook_config in hooks["state"].items():
            lines.extend(["", f"[hooks.state.{quote_toml_key(hook_key)}]"])
            for key, value in hook_config.items():
                lines.append(f"{quote_toml_key(str(key))} = {quote_toml(value)}")
    for project_path, project_config in codex.get("projects", {}).items():
        lines.extend(["", f"[projects.{quote_toml_key(project_path)}]"])
        for key, value in project_config.items():
            lines.append(f"{quote_toml_key(str(key))} = {quote_toml(value)}")
    return "\n".join(lines) + "\n"


def render_claude_sandbox(manifest: dict[str, Any], os_name: str = "darwin") -> dict[str, Any]:
    """Render the Claude sandbox; allowWrite reuses the Codex writable roots.

    `filesystem.denyRead` and `credentials` render on every OS: the Linux sandbox enforces `denyRead` globs and
    credential entries but drops the glob forms of Read/Edit permission rules (regime-cutover U17). Per OS (U68):
    Mach services and `allowUnixSockets` are macOS-only keys that Claude Code ignores on Linux.
    """
    sandbox = manifest["claude"]["sandbox"]
    filesystem = sandbox.get("filesystem", {})
    network = copy.deepcopy(sandbox["network"])
    if os_name != "darwin":
        network.pop("allowMachLookup", None)
        network.pop("allowUnixSockets", None)
    deny_read = [
        *filesystem.get("deny_read", []),
        *(filesystem.get("darwin_deny_read", []) if os_name == "darwin" else []),
    ]
    credentials = sandbox.get("credentials", {})
    return {
        "enabled": sandbox["enabled"],
        "failIfUnavailable": sandbox["failIfUnavailable"],
        "autoAllowBashIfSandboxed": sandbox["autoAllowBashIfSandboxed"],
        "allowUnsandboxedCommands": sandbox["allowUnsandboxedCommands"],
        "excludedCommands": sandbox["excludedCommands"]
        + (sandbox.get("linux_excluded_commands", []) if os_name == "linux" else []),
        "filesystem": {
            "allowWrite": [
                *manifest["codex"]["sandbox_workspace_write"]["writable_roots"],
                *filesystem.get("extra_allow_write", []),
                *(filesystem.get("darwin_extra_allow_write", []) if os_name == "darwin" else []),
            ],
            **({"denyRead": deny_read} if deny_read else {}),
        },
        **(
            {
                "credentials": {
                    key: copy.deepcopy(credentials[key]) for key in ("files", "envVars") if key in credentials
                }
            }
            if credentials
            else {}
        ),
        "network": network,
    }


def render_claude_allow(manifest: dict[str, Any], os_name: str = "darwin") -> list[str]:
    """Render `permissions.allow` for one OS: the shared rules, plus `darwin_allow` on macOS only (U31, D-024-144)."""
    permissions = manifest["claude"]["permissions"]
    return [*permissions.get("allow", []), *(permissions.get("darwin_allow", []) if os_name == "darwin" else [])]


def render_claude_settings(manifest: dict[str, Any]) -> str:
    claude = manifest["claude"]
    hooks = claude.get("hooks", {})
    post_hooks: list[dict[str, str]] = []
    if hooks.get("format_edited_files_hook"):
        post_hooks.append(
            {
                "type": "command",
                "command": hooks["format_edited_files_hook"],
            }
        )
    if hooks.get("project_map_reload_hook"):
        post_hooks.append(
            {
                "type": "command",
                "command": hooks["project_map_reload_hook"],
            }
        )
    profile_claude = interactive_profile(manifest)["claude"]
    permission_request = hooks.get("permission_request")
    settings: dict[str, Any] = {
        "$schema": claude["schema"],
        "model": profile_claude["model"],
        "effortLevel": profile_claude["effort"],
        **({"advisorModel": profile_claude["advisor"]} if "advisor" in profile_claude else {}),
        "alwaysThinkingEnabled": claude["alwaysThinkingEnabled"],
        "plansDirectory": claude["plansDirectory"],
        "permissions": {
            **(
                {"allow": None if "darwin_allow" in claude["permissions"] else claude["permissions"]["allow"]}
                if "allow" in claude["permissions"]
                else {}
            ),
            "deny": claude["permissions"]["deny"],
            "defaultMode": claude["permissions"]["defaultMode"],
            "ask": claude["permissions"]["ask"],
        },
        **({"sandbox": None} if "sandbox" in claude else {}),
        **({"env": claude["env"]} if "env" in claude else {}),
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": hooks["enforce_uv_hook"],
                        }
                    ],
                }
            ],
            "SessionStart": hooks.get("session_start", []),
            "PostToolUse": [
                {
                    "matcher": "Write|Edit",
                    "hooks": post_hooks,
                }
            ],
            **(
                {
                    "PermissionRequest": [
                        {
                            "matcher": "*",
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": permission_request["command"],
                                    "timeout": permission_request["timeout"],
                                    "statusMessage": permission_request["status_message"],
                                }
                            ],
                        }
                    ]
                }
                if permission_request
                else {}
            ),
        },
        "statusLine": claude["statusLine"],
        "disableSkillShellExecution": claude["disableSkillShellExecution"],
        "includeGitInstructions": claude["includeGitInstructions"],
    }
    text = json_dumps(settings)
    if "sandbox" in claude:
        variants = [json_dumps(render_claude_sandbox(manifest, os_name)).strip() for os_name in ("darwin", "linux")]
        sandbox_template = (
            '{{ if eq .chezmoi.os "darwin" }}\n' + variants[0] + "\n{{ else }}\n" + variants[1] + "\n{{ end }}"
        )
        text = text.replace('"sandbox": null', '"sandbox": ' + sandbox_template, 1)
    if "darwin_allow" in claude["permissions"]:
        variants = [json_dumps(render_claude_allow(manifest, os_name)).strip() for os_name in ("darwin", "linux")]
        allow_template = (
            '{{ if eq .chezmoi.os "darwin" }}\n' + variants[0] + "\n{{ else }}\n" + variants[1] + "\n{{ end }}"
        )
        text = text.replace('"allow": null', '"allow": ' + allow_template, 1)
    return text


def render_marketplace(manifest: dict[str, Any]) -> str:
    plugins = manifest["plugins"]
    data = {
        "interface": {"displayName": plugins["marketplace"]["displayName"]},
        "name": plugins["marketplace"]["name"],
        "plugins": [
            {
                "category": plugin["category"],
                "name": plugin["name"],
                "policy": {
                    "authentication": plugin["authentication"],
                    "installation": plugin["installation"],
                },
                "source": {"path": plugin["source_path"], "source": "local"},
            }
            for plugin in plugins.get("codex_plugins", [])
        ],
    }
    return json_dumps(data)


def render_claude_skill_symlink(source_file: Path) -> str:
    rel = source_file.relative_to(ROOT / "home")
    return "{{ .chezmoi.sourceDir }}/" + str(rel) + "\n"


def chezmoi_target_name(source_name: str) -> str:
    return source_name.removeprefix("executable_")


def claude_skill_symlink_outputs(manifest: dict[str, Any]) -> dict[Path, str]:
    """One ~/.claude/skills link per file of each home/dot_agents/skills skill whose audience names Claude Code."""
    outputs: dict[Path, str] = {}
    skills_root = ROOT / SKILLS_SOURCE_DIR
    claude_root = ROOT / "home/dot_claude/skills"
    if not skills_root.exists():
        return outputs
    declared, _, _ = skill_audiences(manifest)
    for source_file in sorted(path for path in skills_root.rglob("*") if path.is_file()):
        if source_file.name.startswith("."):
            continue
        rel = source_file.relative_to(skills_root)
        if "claude" not in declared.get(rel.parts[0], []):
            continue
        target_path = rel.with_name(chezmoi_target_name(rel.name))
        target_dir = claude_root / target_path.parent
        outputs[target_dir / f"symlink_{target_path.name}.tmpl"] = render_claude_skill_symlink(source_file)
    return outputs


def skill_removals(manifest: dict[str, Any], current: str) -> list[str]:
    """Every Claude skill link target no skill gets now, so chezmoi apply removes the link a host still holds.

    A skill under home/dot_agents/skills whose audience leaves out Claude Code has its ~/.claude/skills directory
    listed; the block's earlier entries stay, so a skill deleted from the source keeps its removal, and a skill
    linked again leaves the block.
    """
    declared, _, _ = skill_audiences(manifest)
    root = ROOT / SKILLS_SOURCE_DIR
    sources = sorted(path.name for path in root.iterdir() if path.is_dir()) if root.is_dir() else []
    linked = {f".claude/skills/{name}" for name in sources if "claude" in declared[name]}
    retired = {f".claude/skills/{name}" for name in sources if "claude" not in declared[name]}
    earlier = removal_block_entries(current, SKILL_REMOVALS_BEGIN, SKILL_REMOVALS_END)
    return sorted((retired | earlier) - linked)


def render_codex_profile(name: str, profile: dict[str, Any]) -> str:
    codex = profile["codex"]
    lines = [
        f'# Codex model profile "{name}"; launch with: codex --profile {name}',
        f"# {GENERATED_HEADER}",
        "",
        f"model = {quote_toml(codex['model'])}",
        f"model_reasoning_effort = {quote_toml(codex['model_reasoning_effort'])}",
    ]
    # Overrides the global sandbox_mode; profiles without it inherit the base config.
    if sandbox_mode := codex.get("sandbox_mode"):
        lines.append(f"sandbox_mode = {quote_toml(sandbox_mode)}")
    if notify := codex.get("notify"):
        lines.append(f"notify = {quote_toml(notify)}")
    lines.extend(
        [
            "",
            "[features]",
            "hooks = true",
            "",
            "[hooks.state]",
        ]
    )
    return "\n".join(lines) + "\n"


HOOK_TRUST_BEGIN = "# >>> codex hook trust (generated by scripts/generate-agent-configs.py; edit it there) >>>\n"
HOOK_TRUST_END = "# <<< codex hook trust <<<\n"
# The source a config hook's hooks.state key names; every other declared key is a plugin hook.
CODEX_CONFIG_HOOK_SOURCE = "{{ .chezmoi.homeDir }}/.codex/config.toml"
# Apply-time Codex hook trust, shared by the base and profile modify scripts. Codex runs a config or
# plugin hook only when [hooks.state."<key>"] holds the trust hash of its current definition, and that
# hash covers the absolute command path, so it is computed on each host from the hook it names.
HOOK_TRUST_CODE = """import functools
import hashlib
import json
import os
import re

HOOK_TRUST_HOME = "{{ .chezmoi.homeDir }}"
NO_MATCHER_HOOK_EVENTS = frozenset({"user_prompt_submit", "stop", "interrupt"})
SHORT_TIMEOUT_HOOK_EVENTS = frozenset({"session_end", "interrupt"})


def hook_event_label(event: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", event).lower()


def with_home(value, home: str):
    if isinstance(value, str):
        return value.replace(HOOK_TRUST_HOME, home)
    if isinstance(value, list):
        return [with_home(item, home) for item in value]
    if isinstance(value, dict):
        return {key: with_home(item, home) for key, item in value.items()}
    return value


def codex_hook_hash(event: str, matcher, handler: dict):
    \"\"\"Codex's trust hash for one command hook (codex-rs hooks/src/engine/discovery.rs hook_hash, rust-v0.160.0).

    sha256 over the key-sorted compact JSON of {event_name, matcher, hooks: [normalized handler]};
    None for a hook this function does not model, so the caller falls back to the pinned hash.
    \"\"\"
    if not isinstance(handler, dict) or handler.get("type") != "command" or not isinstance(handler.get("command"), str):
        return None
    if handler.get("additionalContextLimit") is not None:
        return None
    timeout = handler.get("timeout")
    if event in SHORT_TIMEOUT_HOOK_EVENTS:
        timeout = min(max(1 if timeout is None else timeout, 1), 3)
    else:
        timeout = max(600 if timeout is None else timeout, 1)
    normalized = {
        "type": "command",
        "command": handler["command"],
        "timeout": timeout,
        "async": bool(handler.get("async", False)),
    }
    if handler.get("statusMessage") is not None:
        normalized["statusMessage"] = handler["statusMessage"]
    identity = {"event_name": event, "hooks": [normalized]}
    if matcher is not None and event not in NO_MATCHER_HOOK_EVENTS:
        identity["matcher"] = matcher
    text = json.dumps(identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()


SEMVER = re.compile(
    r"^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?(?:\\+([0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?$"
)
PLUGIN_VERSION_SEGMENT = re.compile(r"^[A-Za-z0-9._+-]+$")


U64_MAX = 2**64 - 1


def all_ascii_digits(text: str) -> bool:
    \"\"\"Rust's bytes().all(u8::is_ascii_digit): true for the empty string.\"\"\"
    return all("0" <= ch <= "9" for ch in text)


def compare_prerelease(left: str, right: str) -> int:
    \"\"\"semver 1.0.27 Prerelease::cmp: a release (empty) sorts above any pre-release.\"\"\"
    if left == right:
        return 0
    if not left:
        return 1
    if not right:
        return -1
    lhs, rhs = left.split("."), right.split(".")
    for index, a in enumerate(lhs):
        if index >= len(rhs):
            return 1
        b = rhs[index]
        if all_ascii_digits(a) and all_ascii_digits(b):
            ordering = (len(a) > len(b)) - (len(a) < len(b)) or (a > b) - (a < b)
        elif all_ascii_digits(a) != all_ascii_digits(b):
            return -1 if all_ascii_digits(a) else 1
        else:
            ordering = (a > b) - (a < b)
        if ordering:
            return ordering
    return 0 if len(rhs) == len(lhs) else -1


def compare_build(left: str, right: str) -> int:
    \"\"\"semver 1.0.27 BuildMetadata::cmp: empty < non-empty; numeric identifiers by stripped length,
    stripped value, then original length (0 < 00 < 1 < 01 < 001 < 2).\"\"\"
    if left == right:
        return 0
    lhs, rhs = left.split("."), right.split(".")
    for index, a in enumerate(lhs):
        if index >= len(rhs):
            return 1
        b = rhs[index]
        if all_ascii_digits(a) and all_ascii_digits(b):
            sa, sb = a.lstrip("0"), b.lstrip("0")
            key_a, key_b = (len(sa), sa, len(a)), (len(sb), sb, len(b))
            ordering = (key_a > key_b) - (key_a < key_b)
        elif all_ascii_digits(a) != all_ascii_digits(b):
            return -1 if all_ascii_digits(a) else 1
        else:
            ordering = (a > b) - (a < b)
        if ordering:
            return ordering
    return 0 if len(rhs) == len(lhs) else -1


def parse_semver(version: str):
    \"\"\"A semver match as the `semver` crate (1.0.27) accepts it, else None.

    Numeric pre-release identifiers may not have leading zeros (build identifiers may), and
    major, minor and patch must fit in a u64.
    \"\"\"
    match = SEMVER.match(version)
    if not match or any(int(part) > U64_MAX for part in match.groups()[:3]):
        return None
    if match.group(4):
        for identifier in match.group(4).split("."):
            if all_ascii_digits(identifier) and len(identifier) > 1 and identifier.startswith("0"):
                return None
    return match


def compare_plugin_versions(left: str, right: str) -> int:
    \"\"\"Codex's version order (core-plugin-common installed.rs compare_plugin_versions, rust-v0.160.0):
    semver Version::cmp (major, minor, patch, pre, build) when both parse, else plain string order.\"\"\"
    a, b = parse_semver(left), parse_semver(right)
    if not (a and b):
        return (left > right) - (left < right)
    for x, y in zip(a.groups()[:3], b.groups()[:3]):
        if int(x) != int(y):
            return -1 if int(x) < int(y) else 1
    return compare_prerelease(a.group(4) or "", b.group(4) or "") or compare_build(a.group(5) or "", b.group(5) or "")


def active_plugin_version(root: Path):
    \"\"\"The cached version Codex loads (installed.rs active_plugin_version): `local`, else the highest.\"\"\"
    try:
        versions = [
            entry.name
            for entry in root.iterdir()
            # Codex reads the entry's own type, so a symlinked version directory is not a version.
            if not entry.is_symlink()
            and entry.is_dir()
            and entry.name not in (".", "..")
            and PLUGIN_VERSION_SEGMENT.match(entry.name)
        ]
    except OSError:
        return None
    if not versions:
        return None
    if "local" in versions:
        return "local"
    return max(versions, key=functools.cmp_to_key(compare_plugin_versions))


def declared_hook(home: str, key: str):
    \"\"\"The (event, matcher, handler) a declared key names on this host, or why it cannot be read.\"\"\"
    try:
        source, event, group_index, handler_index = key.rsplit(":", 3)
        group_index, handler_index = int(group_index), int(handler_index)
    except ValueError:
        return "malformed key"
    if source == home + "/.codex/config.toml":
        groups = with_home(HOOK_TRUST["config_hooks"].get(event, []), home)
    else:
        plugin_id, _, relative = source.partition(":")
        plugin, _, marketplace = plugin_id.partition("@")
        if not (plugin and marketplace and relative):
            return "unknown hook source " + source
        root = Path(home) / ".codex/plugins/cache" / marketplace / plugin
        version = active_plugin_version(root)
        if version is None:
            return f"no installed copy under {root}"
        hook_file = root / version / relative
        try:
            hooks = json.loads(hook_file.read_text()).get("hooks", {})
            groups = next((value for name, value in hooks.items() if hook_event_label(name) == event), [])
        except (OSError, ValueError, AttributeError) as error:
            return f"unreadable {hook_file}: {error}"
    try:
        group = groups[group_index]
        return event, group.get("matcher"), group["hooks"][handler_index]
    except (IndexError, KeyError, TypeError, AttributeError):
        return f"no {event} hook {group_index}:{handler_index}"


def declared_hook_trust(home: str) -> list:
    \"\"\"(key, entry, trusted hash or None, kind, warning or None) for each hook the manifest declares.

    A config hook is trusted at the hash of its manifest definition. A plugin hook is trusted only at its
    manifest pin: `make update` upgrades plugins, so an installed hook whose hash differs from the pin is a
    release nobody reviewed and stays untrusted (kind "changed") until it is reviewed in /hooks and the
    reviewed hash is recorded as the pin. When the hash cannot be computed, the pin is written as is
    (kind "fallback"): Codex trusts only content with that hash, so the pin never trusts anything else.
    \"\"\"
    results = []
    for entry in HOOK_TRUST["declared"]:
        key = entry["key"].replace(HOOK_TRUST_HOME, home)
        pin = entry.get("trusted_hash")
        found = declared_hook(home, key)
        digest = codex_hook_hash(*found) if isinstance(found, tuple) else None
        kind, warning = "trusted", None
        if digest is None:
            reason = found if isinstance(found, str) else "not a command hook"
            fallback = "using the manifest's pinned hash" if pin else "leaving it untrusted"
            kind, warning = "fallback", f"cannot compute hook trust for {key} ({reason}); {fallback}"
            digest = pin
        elif not key.startswith(home + "/.codex/config.toml:") and digest != pin:
            kind = "changed"
            warning = (
                f"hook {key} is not trusted: the installed hook hashes to {digest}, not the manifest pin {pin}; "
                "review it with /hooks in Codex and record the reviewed hash as its trusted_hash in agent-config.yaml"
            )
            digest = None
        results.append((key, entry, digest, kind, warning))
    return results


def declared_hook_state(home: str) -> list:
    \"\"\"[hooks.state] chunks for the hooks the manifest declares, trusted as declared_hook_trust decides.\"\"\"
    chunks = []
    for key, entry, digest, _, warning in declared_hook_trust(home):
        if warning:
            print(f"warning: {warning}", file=sys.stderr)
        quoted = json.dumps(key, ensure_ascii=False)
        lines = [f"[hooks.state.{quoted}]"]
        if digest:
            lines.append(f'trusted_hash = "{digest}"')
        if "enabled" in entry:
            lines.append("enabled = " + ("true" if entry["enabled"] else "false"))
        chunks.append((f"hooks.state.{quoted}", "\\n".join(lines) + "\\n\\n"))
    return chunks


def refuse(message: str):
    \"\"\"Stop the apply of this Codex config: a merge that cannot read hook trust never writes or keeps it.\"\"\"
    print(f"ERROR: codex config merge: {message}; refusing to apply this file", file=sys.stderr)
    raise SystemExit(1)


try:
    import tomllib as hook_trust_toml
except ModuleNotFoundError:
    refuse("reading hook trust needs Python 3.11 or later (tomllib)")


def parse_config(text: str, label: str) -> dict:
    try:
        return hook_trust_toml.loads(text)
    except ValueError as error:  # tomllib.TOMLDecodeError is a ValueError.
        refuse(f"{label} is not valid TOML ({error})")


def hook_state_key(name):
    \"\"\"The decoded TOML key of a `hooks.state.<key>` table name, however it is quoted, else None.\"\"\"
    path = key_path(name) if name else None
    return path[2] if path and len(path) == 3 and path[:2] == ["hooks", "state"] else None


def declared_trusted_hash(chunk: str):
    match = re.search(r'^trusted_hash = "([^"]+)"$', chunk, re.MULTILINE)
    return match.group(1) if match else None


DOTTED_KEY_ASSIGNMENT = re.compile(
    r\"\"\"^\\s*((?:"(?:[^"\\\\]|\\\\.)*"|'[^']*'|[A-Za-z0-9_-]+)(?:\\s*\\.\\s*(?:"(?:[^"\\\\]|\\\\.)*"|'[^']*'|[A-Za-z0-9_-]+))*)\\s*=\"\"\"
)
BARE_KEY = re.compile(r"[A-Za-z0-9_-]+")


def report_divergence(name: str, old, new) -> None:
    if old != new:
        print(f"warning: hook trust divergence for {name}: replacing {old} with {new}", file=sys.stderr)


def key_path(raw: str):
    \"\"\"The decoded segments of a dotted TOML key, bare or quoted, else None.\"\"\"
    try:
        node = hook_trust_toml.loads(f"[{raw}]\\n")
    except ValueError:
        return None
    segments = []
    while isinstance(node, dict) and len(node) == 1:
        key, node = next(iter(node.items()))
        segments.append(key)
    return segments if node == {} and segments else None


def toml_key(segment: str) -> str:
    return segment if BARE_KEY.fullmatch(segment) else json.dumps(segment, ensure_ascii=False).replace("\\x7f", "\\\\u007f")


def canonical_table_name(raw: str) -> str:
    \"\"\"One spelling per decoded key path: bare segments where TOML allows them, basic strings otherwise.\"\"\"
    segments = key_path(raw)
    if segments is None:
        return raw
    return ".".join(toml_key(segment) for segment in segments)


def defines_hook_state(path: list) -> bool:
    \"\"\"An assignment at this key path writes hook state: `hooks = {…}`, `hooks.state = {…}` or below it.\"\"\"
    return bool(path) and path[0] == "hooks" and (len(path) == 1 or path[1] == "state")


def drop_hook_state_assignments(chunk: str, scope: list, defines=defines_hook_state):
    \"\"\"The chunk without its assignments that `defines` reads as its own (hook state by default), and whether it had any.\"\"\"
    kept, found = [], False
    string = None
    for line in chunk.splitlines(keepends=True):
        if string is None:
            match = DOTTED_KEY_ASSIGNMENT.match(line)
            if match and defines(scope + (key_path(match.group(1)) or [""])):
                # TOML 1.0 keeps an inline table on one line, so the assignment is this line.
                found = True
                continue
        kept.append(line)
        string = multiline_string_after(line, string)
    return "".join(kept), found


def toml_value(value, label: str, table: str = "hooks.state") -> str:
    \"\"\"A parsed TOML value written back as TOML; a date or time refuses (nothing hook state or a project holds).\"\"\"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False).replace("\\x7f", "\\\\u007f")
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(item, label, table) for item in value) + "]"
    if isinstance(value, dict):
        return "{ " + ", ".join(f"{toml_key(key)} = {toml_value(item, label, table)}" for key, item in value.items()) + " }"
    refuse(f"cannot rewrite a {type(value).__name__} value in {table} of {label}")


def normalize_hook_state(text: str, label: str = "the current file") -> str:
    \"\"\"The config with every hook-state entry in its own [hooks.state."<key>"] table, whatever valid TOML form held it.

    Inline tables and dotted keys (under [hooks.state], under [hooks], at the root) are rewritten as tables, so the
    merge reads one spelling and replaces declared entries wherever they were written. Text already in table form is
    returned unchanged. Invalid TOML, or hook state that cannot be rewritten without changing any other setting,
    stops the apply: the merge never keeps or writes trust it could not read.
    \"\"\"
    if not text.strip():
        return text
    data = parse_config(text, label)
    hooks = data.get("hooks", {})
    state = hooks.get("state", {}) if isinstance(hooks, dict) else None
    if not isinstance(state, dict):
        refuse(f"hooks.state in {label} is not a table")
    chunks, inline = [], False
    for name, chunk in split_chunks(text):
        scope = [] if name is None else key_path(name)
        if scope is None:
            refuse(f"cannot read the table name [{name}] in {label}")
        if scope in ([], ["hooks"], ["hooks", "state"]):
            chunk, found = drop_hook_state_assignments(chunk, scope)
            inline = inline or found
        chunks.append((scope, chunk))
    if not inline:
        return text
    body = "".join(chunk for scope, chunk in chunks if scope[:2] != ["hooks", "state"]).rstrip("\\n")
    header = ["[hooks.state]"] + [f"{toml_key(key)} = {toml_value(value, label)}" for key, value in state.items() if not isinstance(value, dict)]
    tables = ["\\n".join(header)] if "state" in hooks else []
    for key, fields in state.items():
        if isinstance(fields, dict):
            lines = [f"[hooks.state.{toml_key(key)}]"]
            lines.extend(f"{toml_key(field)} = {toml_value(value, label)}" for field, value in fields.items())
            tables.append("\\n".join(lines))
    normalized = "\\n\\n".join(([body] if body.strip() else []) + tables) + "\\n"
    if parse_config(normalized, label) != data:
        refuse(f"cannot rewrite hooks.state in {label} without changing its other settings")
    return normalized


def defines_projects(path: list) -> bool:
    \"\"\"An assignment at this key path writes project trust: `projects = {…}` or anything below it.\"\"\"
    return bool(path) and path[0] == "projects"


def normalize_projects(text: str, label: str = "the current file") -> str:
    \"\"\"The config with every project entry in its own [projects.<path>] table, whatever valid TOML form held it.

    Inline tables and dotted keys (under [projects] or at the root) are rewritten from the parsed data as tables, so
    drop_missing_path_state reads every trusted project by its table name. Text already in table form is returned
    unchanged. Invalid TOML, or projects that cannot be rewritten without changing any other setting, stops the apply:
    the merge never keeps trust it could not read.
    \"\"\"
    if not text.strip():
        return text
    data = parse_config(text, label)
    projects = data.get("projects", {})
    if not isinstance(projects, dict):
        refuse(f"projects in {label} is not a table")
    chunks, inline = [], False
    for name, chunk in split_chunks(text):
        scope = [] if name is None else key_path(name)
        if scope is None:
            refuse(f"cannot read the table name [{name}] in {label}")
        if scope in ([], ["projects"]):
            chunk, found = drop_hook_state_assignments(chunk, scope, defines_projects)
            inline = inline or found
        chunks.append((scope, chunk))
    if not inline:
        return text
    body = "".join(chunk for scope, chunk in chunks if scope[:1] != ["projects"]).rstrip("\\n")
    header = ["[projects]"] + [
        f"{toml_key(key)} = {toml_value(value, label, 'projects')}" for key, value in projects.items() if not isinstance(value, dict)
    ]
    tables = ["\\n".join(header)] if len(header) > 1 else []
    for key, fields in projects.items():
        if isinstance(fields, dict):
            lines = [f"[projects.{toml_key(key)}]"]
            lines.extend(f"{toml_key(field)} = {toml_value(value, label, 'projects')}" for field, value in fields.items())
            tables.append("\\n".join(lines))
    normalized = "\\n\\n".join(([body] if body.strip() else []) + tables) + "\\n"
    try:
        same = hook_trust_toml.loads(normalized) == data
    except ValueError:
        same = False
    if not same:
        refuse(f"cannot rewrite projects in {label} without changing its other settings")
    return normalized


def declared_trusted_hash(chunk: str):
    match = re.search(r'^trusted_hash = "([^"]+)"$', chunk, re.MULTILINE)
    return match.group(1) if match else None


def drop_declared_hook_state(chunks: list, declared: list) -> list:
    \"\"\"Drop existing entries for declared keys (the managed ones replace them), reporting each change once.

    The chunks come from normalize_hook_state's output, so every entry is its own table.
    \"\"\"
    by_key = {hook_state_key(name): (name, chunk) for name, chunk in declared}
    kept = []
    for name, chunk in chunks:
        key = hook_state_key(name)
        if key is not None and key in by_key:
            report_divergence(name, declared_trusted_hash(chunk), declared_trusted_hash(by_key[key][1]))
            continue
        kept.append((name, chunk))
    return kept


# Codex keys trust by absolute path: a project by its directory, a config-layer hook by the hooks.json or
# config.toml that holds it (codex-rs hooks/src/lib.rs hook_key, rust-v0.160.0: "<source>:<event>:<group>:<handler>").
HOOK_SOURCE_NAMES = ("hooks.json", "config.toml")


def path_is_gone(path: str, entry: str) -> bool:
    \"\"\"True only when nothing exists at the path; any other failed check keeps the entry and says so.\"\"\"
    try:
        os.lstat(path)
    except (FileNotFoundError, NotADirectoryError):
        return True
    except OSError as error:
        print(f"warning: cannot check {path} ({error}); keeping {entry}", file=sys.stderr)
    return False


def trusted_path(name):
    \"\"\"The absolute path a [projects.<path>] table or a hooks.json/config.toml [hooks.state.<key>] trusts, else None.\"\"\"
    path = key_path(name) if name else None
    if path and len(path) >= 2 and path[0] == "projects":
        return path[1] if os.path.isabs(path[1]) else None
    key = hook_state_key(name)
    parts = key.rsplit(":", 3) if key else []
    if len(parts) == 4 and os.path.isabs(parts[0]) and os.path.basename(parts[0]) in HOOK_SOURCE_NAMES:
        return parts[0]
    return None


def drop_missing_path_state(chunks: list) -> list:
    \"\"\"Drop project and hook trust whose absolute path no longer exists on this host; plugin keys stay.\"\"\"
    kept = []
    for name, chunk in chunks:
        path = trusted_path(name)
        if path is not None and path_is_gone(path, f"[{name}]"):
            continue
        kept.append((name, chunk))
    return kept


def verified_merge(merged: str, declared) -> str:
    \"\"\"The merged config once it parses and every declared key holds exactly the managed entry; else refuse.\"\"\"
    hooks = parse_config(merged, "the merged config").get("hooks", {})
    state = hooks.get("state", {}) if isinstance(hooks, dict) else None
    for name, chunk in declared:
        key = hook_state_key(name)
        expected = hook_trust_toml.loads(chunk)["hooks"]["state"][key]
        if not isinstance(state, dict) or state.get(key) != expected:
            refuse(f"the merged hooks.state entry for {key} is not the managed one")
    return merged
"""


def codex_hook_trust(manifest: dict[str, Any]) -> dict[str, Any]:
    """The declared trusted hooks and the config hook definitions the modify scripts hash at apply time."""
    hooks = manifest["codex"].get("hooks", {})
    config_hooks: dict[str, list[dict[str, Any]]] = {}
    definitions = [("PermissionRequest", hooks["permission_request"])] if hooks.get("permission_request") else []
    definitions += [(hook["event"], hook) for hook in hooks.get("command_hooks", [])]
    for event, hook in definitions:
        # Mirrors codex_command_hook_lines(): one matcher group per definition, in render order.
        config_hooks.setdefault(re.sub(r"(?<!^)(?=[A-Z])", "_", event).lower(), []).append(
            {
                "matcher": "*",
                "hooks": [
                    {
                        "type": "command",
                        "command": hook["command"],
                        "timeout": hook["timeout"],
                        "statusMessage": hook["status_message"],
                    }
                ],
            }
        )
    declared = []
    for key, state in hooks.get("state", {}).items():
        if not isinstance(state, dict) or set(state) - {"trusted_hash", "enabled"}:
            fail(f"codex.hooks.state.{key} may only set trusted_hash and enabled")
        # A plugin hook is trusted only at its reviewed pin; see declared_hook_trust.
        config_hook = key.startswith(CODEX_CONFIG_HOOK_SOURCE + ":")  # lint-comparisons: allow a hook key, not a path
        if not config_hook and not state.get("trusted_hash"):
            fail(f"codex.hooks.state.{key} is a plugin hook and must pin its reviewed trusted_hash")
        declared.append({"key": key, **state})
    return {"declared": declared, "config_hooks": config_hooks}


def render_hook_trust_block(manifest: dict[str, Any]) -> str:
    return HOOK_TRUST_BEGIN + f"HOOK_TRUST = {codex_hook_trust(manifest)!r}\n" + HOOK_TRUST_CODE + HOOK_TRUST_END


def render_codex_base_modify(manifest: dict[str, Any]) -> str:
    """The hand-maintained base modify script with its generated hook-trust block refreshed."""
    relative = "home/dot_codex/modify_private_config.toml"
    # A fixture ROOT (unit tests) has no base script of its own; take the repository's copy then.
    source = ROOT / relative if (ROOT / relative).exists() else Path(__file__).resolve().parents[1] / relative
    text = read_exact(source)
    start, end = text.find(HOOK_TRUST_BEGIN), text.find(HOOK_TRUST_END)
    if start == -1 or end < start:
        fail("home/dot_codex/modify_private_config.toml must keep the codex hook trust block markers")
    return text[:start] + render_hook_trust_block(manifest) + text[end + len(HOOK_TRUST_END) :]


def render_codex_profile_modify(name: str, profile: dict[str, Any], manifest: dict[str, Any]) -> str:
    managed = render_codex_profile(name, profile)
    render_helper = ""
    managed_source = "MANAGED"
    if "{{ .chezmoi.homeDir }}" in managed:
        render_helper = """\n\ndef render_managed_paths(text: str) -> str:
    return text.replace("{{ .chezmoi.homeDir }}", str(Path.home()))
"""
        managed_source = "render_managed_paths(MANAGED)"
    return f'''#!/usr/bin/env python3
"""Merge the managed Codex {name} profile with Codex-owned runtime state."""

from __future__ import annotations

import sys
from pathlib import Path
import re

RUNTIME_PREFIXES = {RUNTIME_PREFIXES!r}
MANAGED = {managed!r}
{render_helper}
__HOOK_TRUST_BLOCK__

def table_name(header: str) -> str | None:
    """The raw name of a `[table]` or `[[array]]` header line, which may end in a `# comment`, else None."""
    stripped = header.strip()
    if not stripped.startswith("["):
        return None
    double = stripped.startswith("[[")
    start = index = 2 if double else 1
    quote = None
    while index < len(stripped):
        char = stripped[index]
        if quote == '"' and char == "\\\\":
            index += 2
            continue
        if char == quote:
            quote = None
        elif quote is None and char in ('"', "'"):
            quote = char
        elif quote is None and char == "]":
            break
        index += 1
    else:
        return None
    rest = stripped[index + 1 :]
    if double:
        if not rest.startswith("]"):
            return None
        rest = rest[1:]
    rest = rest.lstrip()
    if rest and not rest.startswith("#"):
        return None
    return canonical_table_name(stripped[start:index].strip())


def multiline_string_after(line: str, delimiter: str | None) -> str | None:
    """The multiline string delimiter still open after this line, given the one open before it, else None."""
    index = 0
    while index < len(line):
        if delimiter is not None:
            if delimiter == '"""' and line[index] == "\\\\":
                index += 2
            elif line.startswith(delimiter, index):
                # Up to two more quotes before the closing delimiter belong to the string.
                index += len(line[index:]) - len(line[index:].lstrip(delimiter[0]))
                delimiter = None
            else:
                index += 1
            continue
        char = line[index]
        if char == "#":
            return None
        if line.startswith('"""', index) or line.startswith("\'\'\'", index):
            delimiter = line[index : index + 3]
            index += 3
        elif char == '"':
            index += 1
            while index < len(line) and line[index] != '"':
                index += 2 if line[index] == "\\\\" else 1
            index += 1
        elif char == "'":
            end = line.find("'", index + 1)
            index = len(line) if end == -1 else end + 1
        else:
            index += 1
    return delimiter


def split_chunks(text: str) -> list[tuple[str | None, str]]:
    chunks: list[tuple[str | None, str]] = []
    current_name: str | None = None
    current_lines: list[str] = []
    pending_lines: list[str] = []
    string = None
    for line in text.splitlines(keepends=True):
        # A header-like line inside a multiline string is string content, never a chunk boundary.
        name = table_name(line) if string is None else None
        string = multiline_string_after(line, string)
        if name is None:
            if current_name is None:
                pending_lines.append(line)
            else:
                current_lines.append(line)
            continue
        if current_name is None:
            if pending_lines:
                split_at = len(pending_lines)
                while split_at and not pending_lines[split_at - 1].strip():
                    split_at -= 1
                if split_at:
                    chunks.append((None, "".join(pending_lines[:split_at])))
                pending_lines = pending_lines[split_at:]
        else:
            chunks.append((current_name, "".join(current_lines)))
        current_name = name
        current_lines = pending_lines + [line]
        pending_lines = []
    if current_name is None:
        if pending_lines:
            chunks.append((None, "".join(pending_lines)))
    else:
        chunks.append((current_name, "".join(current_lines)))
    return chunks


def runtime_prefix(name: str | None) -> str | None:
    if name is None:
        return None
    for prefix in RUNTIME_PREFIXES:
        if name == prefix or name.startswith(f"{{prefix}}."):
            return prefix
    return None


def base_hook_state() -> list[tuple[str, str]]:
    """Harvest operator-granted hook trust from the base Codex config."""
    path = Path.home() / ".codex/config.toml"
    if not path.is_file():
        return []
    return [
        (name, chunk)
        for name, chunk in drop_missing_path_state(split_chunks(normalize_hook_state(path.read_text(), str(path))))
        if runtime_prefix(name) == "hooks.state"
    ]


def trusted_hash(chunk: str) -> str | None:
    """Parse a persisted hook-trust hash without recalculating or trusting it."""
    match = re.search(r'^trusted_hash = "([^"]+)"$', chunk, re.MULTILINE)
    return match.group(1) if match else None


def merge_config(current: str) -> str:
    """Keep profile trust authoritative and only warn when base trust diverges."""
    managed_chunks = split_chunks({managed_source})
    declared = declared_hook_state(str(Path.home()))
    declared_keys = {{hook_state_key(name) for name, _ in declared}}
    current_chunks = drop_declared_hook_state(split_chunks(normalize_projects(normalize_hook_state(current))) if current.strip() else [], declared)
    current_chunks = drop_missing_path_state(current_chunks)
    current_by_name: dict[str, list[str]] = {{}}
    current_by_runtime_prefix: dict[str, list[tuple[int, str, str]]] = {{}}
    managed_by_runtime_prefix: dict[str, list[tuple[str, str]]] = {{}}
    for current_index, (current_name, current_chunk) in enumerate(current_chunks):
        if current_name is not None:
            current_by_name.setdefault(current_name, []).append(current_chunk)
            prefix = runtime_prefix(current_name)
            if prefix is not None:
                current_by_runtime_prefix.setdefault(prefix, []).append((current_index, current_name, current_chunk))
    for managed_name, managed_chunk in managed_chunks:
        prefix = runtime_prefix(managed_name)
        if managed_name is not None and prefix is not None:
            managed_by_runtime_prefix.setdefault(prefix, []).append((managed_name, managed_chunk))
    managed_by_runtime_prefix.setdefault("hooks.state", []).extend(declared)
    for base_name, base_chunk in base_hook_state():
        if hook_state_key(base_name) in declared_keys:
            continue
        if base_name in current_by_name:
            profile_hash = trusted_hash(current_by_name[base_name][0])
            base_hash = trusted_hash(base_chunk)
            if profile_hash and base_hash and profile_hash != base_hash:
                print(
                    f"warning: hook trust divergence for {{base_name}}: profile={{profile_hash}} base={{base_hash}}",
                    file=sys.stderr,
                )
        if base_name not in current_by_name and base_name not in {{
            name for name, _ in managed_by_runtime_prefix.get("hooks.state", [])
        }}:
            managed_by_runtime_prefix.setdefault("hooks.state", []).append((base_name, base_chunk))
    managed_names = {{table_name for table_name, _ in managed_chunks if table_name is not None}}
    emitted_current: set[int] = set()
    emitted_runtime_prefixes: set[str] = set()
    output: list[str] = []
    for managed_name, managed_chunk in managed_chunks:
        prefix = runtime_prefix(managed_name)
        if prefix is not None:
            if prefix in emitted_runtime_prefixes:
                continue
            current_group = current_by_runtime_prefix.get(prefix, [])
            if current_group:
                for runtime_name, runtime_chunk in managed_by_runtime_prefix.get(prefix, []):
                    if runtime_name == prefix and runtime_name not in current_by_name:
                        output.append(runtime_chunk)
                for current_index, current_name, current_chunk in current_group:
                    output.append(current_chunk)
                    emitted_current.add(current_index)
                for runtime_name, runtime_chunk in managed_by_runtime_prefix.get(prefix, []):
                    if runtime_name != prefix and runtime_name not in current_by_name:
                        output.append(runtime_chunk)
            else:
                output.extend(chunk for _, chunk in managed_by_runtime_prefix.get(prefix, []))
            emitted_runtime_prefixes.add(prefix)
        else:
            output.append(managed_chunk)
    for current_index, (current_name, current_chunk) in enumerate(current_chunks):
        if current_name is None or current_index in emitted_current:
            continue
        prefix = runtime_prefix(current_name)
        if prefix is not None:
            if prefix in emitted_runtime_prefixes:
                continue
            for grouped_index, _, grouped_chunk in current_by_runtime_prefix[prefix]:
                output.append(grouped_chunk)
                emitted_current.add(grouped_index)
            emitted_runtime_prefixes.add(prefix)
        elif current_name not in managed_names:
            output.append(current_chunk)
            emitted_current.add(current_name)
    merged = "".join(output)
    return verified_merge(merged if merged.endswith("\\n") else merged + "\\n", declared)


sys.stdout.write(merge_config(sys.stdin.read()))
'''.replace("__HOOK_TRUST_BLOCK__\n", render_hook_trust_block(manifest))


def render_model_profiles_env(manifest: dict[str, Any]) -> str:
    profiles = model_profiles(manifest)
    interactive_profile(manifest)
    lines = [
        "# Shell fragment of the model profiles for agent launchers.",
        f"# {GENERATED_HEADER}",
        f'MODEL_PROFILE_INTERACTIVE="{manifest["interactive_profile"]}"',
    ]
    for name, profile in sorted(profiles.items()):
        var = str(name).upper()
        claude = profile["claude"]
        claude_args = f"--model {claude['model']} --effort {claude['effort']}"
        if "advisor" in claude:
            claude_args += f" --advisor {claude['advisor']}"
        lines.append(f'MODEL_PROFILE_{var}_CLAUDE_ARGS="{claude_args}"')
        lines.append(f'MODEL_PROFILE_{var}_CODEX_ARGS="--profile {name}"')
    return "\n".join(lines) + "\n"


SKILLS_DIRECTORY_RE = re.compile(r"^(?:~/|/)[A-Za-z0-9._/-]+$")


def omp_skills_directories(manifest: dict[str, Any]) -> list[str]:
    directories = manifest.get("omp", {}).get("skills_directories")
    if not isinstance(directories, list) or not directories:
        fail("omp.skills_directories must be a non-empty list")
    for directory in directories:
        if not isinstance(directory, str) or not SKILLS_DIRECTORY_RE.fullmatch(directory):
            fail(f"omp.skills_directories entries must be ~/ or absolute paths: {directory!r}")
    return directories


OMP_PROVIDER_ID_RE = re.compile(r"^[a-z0-9][a-z0-9.-]*$")


def omp_disabled_providers(manifest: dict[str, Any], key: str = "disabled_providers") -> list[str]:
    """omp providers listed under `omp.<key>`, switched off as `disabledProviders`; none when absent.

    `disabled_providers` goes to the seat overlays and the plain-launch config, `seat_disabled_providers` to the seat
    overlays only. omp 18.11.3 reads one `disabledProviders` set for discovery providers
    (src/capability/index.ts:306-308) and for model providers (src/main.ts:1627), so a model route here would turn a
    seat's model off.
    """
    providers = manifest.get("omp", {}).get(key, [])
    if not isinstance(providers, list):
        fail(f"omp.{key} must be a list of omp provider ids")
    for provider in providers:
        if not isinstance(provider, str) or not OMP_PROVIDER_ID_RE.fullmatch(provider):
            fail(f"omp.{key} entries must be omp provider ids: {provider!r}")
        if provider in OMP_MODEL_ROUTES:
            fail(f"omp.{key} must not name the model route {provider}; disabledProviders turns it off")
    return providers


def omp_seat_disabled_providers(manifest: dict[str, Any]) -> list[str]:
    """The seat overlays' `disabledProviders`: the shared list, then the seat-only entries it lacks."""
    shared = omp_disabled_providers(manifest)
    return shared + [
        provider for provider in omp_disabled_providers(manifest, "seat_disabled_providers") if provider not in shared
    ]


def omp_roles(manifest: dict[str, Any]) -> dict[str, str]:
    """Seat role -> model profile; one overlay renders per key."""
    roles = manifest.get("omp", {}).get("roles")
    if not isinstance(roles, dict) or not roles:
        fail("omp.roles must be a non-empty mapping of seat role to model profile")
    profiles = model_profiles(manifest)
    for role, profile in roles.items():
        if not PROFILE_NAME_RE.match(str(role)):
            fail(f"omp.roles key is not launcher-safe: {role!r}")
        if profile not in profiles:
            fail(f"omp.roles.{role} must name a model profile: {profile!r}")
    return roles


def omp_extensions(manifest: dict[str, Any]) -> list[str]:
    """Extension directories a plain omp launch loads through the top-level `extensions` setting; none when absent.

    validate-agent-assets.py checks that they register the interactive profile's omp provider.
    """
    extensions = manifest.get("omp", {}).get("extensions", [])
    if not isinstance(extensions, list):
        fail("omp.extensions must be a list of extension directories")
    for extension in extensions:
        if not isinstance(extension, str) or not SKILLS_DIRECTORY_RE.fullmatch(extension):
            fail(f"omp.extensions entries must be ~/ or absolute paths: {extension!r}")
    return extensions


SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILLS_SOURCE_DIR = "home/dot_agents/skills"
# The shared root Codex (its user skill root) and omp's agents provider read; every skills.audience skill lives here.
SHARED_SKILLS_ROOT = "~/.agents/skills"
# The pstack external's own root (home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl): no agent scans it by
# default, so only an omp consumer whose skills.customDirectories names it lists the pstack skills.
PSTACK_SKILLS_ROOT = "~/.agents/pstack/skills"


def skill_consumers(manifest: dict[str, Any]) -> list[str]:
    """Every audience a skill may name: Claude Code, Codex, the plain omp launch and each omp seat role."""
    return ["claude", "codex", "omp", *(f"omp-{role}" for role in omp_roles(manifest))]


def skill_audience_list(manifest: dict[str, Any], label: str, audience: Any) -> list[str]:
    allowed = skill_consumers(manifest)
    if not isinstance(audience, list) or not audience or len(set(audience)) != len(audience):
        fail(f"{label} needs a non-empty audience list without repeats")
    unknown = [agent for agent in audience if agent not in allowed]
    if unknown:
        fail(f"{label} names unknown audience {unknown}; expected some of {allowed}")
    return audience


def skill_audiences(manifest: dict[str, Any]) -> tuple[dict[str, list[str]], list[str], list[str]]:
    """Skill name -> audience, the pstack audience and the pstack skills no agent lists.

    Every directory under home/dot_agents/skills must be declared, and a pstack audience naming Claude Code or Codex is
    refused: neither reads the pstack root, so the declaration would claim a listing that never happens.
    """
    section = manifest.get("skills")
    if not isinstance(section, dict) or sorted(section) != ["audience", "pstack"]:
        fail("skills must be a mapping of exactly audience and pstack")
    declared = section["audience"]
    if not isinstance(declared, dict) or not declared:
        fail("skills.audience must be a non-empty mapping of skill name to audience")
    for name, audience in declared.items():
        if not isinstance(name, str) or not SKILL_NAME_RE.fullmatch(name):
            fail(f"skill name must match {SKILL_NAME_RE.pattern}: {name!r}")
        skill_audience_list(manifest, f"skill {name}", audience)
    source_root = ROOT / SKILLS_SOURCE_DIR
    sources = {path.name for path in source_root.iterdir() if path.is_dir()} if source_root.is_dir() else set()
    undeclared = sorted(sources - set(declared))
    if undeclared:
        fail(f"directories in {SKILLS_SOURCE_DIR} are not declared in skills.audience: {undeclared}")
    pstack = section["pstack"]
    if not isinstance(pstack, dict) or not set(pstack) <= {"audience", "exclude"} or "audience" not in pstack:
        fail("skills.pstack must be a mapping of audience and an optional exclude list")
    pstack_audience = skill_audience_list(manifest, "skills.pstack", pstack["audience"])
    outside = [agent for agent in pstack_audience if agent in ("claude", "codex")]
    if outside:
        fail(f"skills.pstack cannot name {outside}: only omp consumers read {PSTACK_SKILLS_ROOT}")
    exclude = pstack.get("exclude", [])
    if not isinstance(exclude, list) or len(set(exclude)) != len(exclude):
        fail("skills.pstack.exclude must be a list of skill names without repeats")
    for name in exclude:
        if not isinstance(name, str) or not SKILL_NAME_RE.fullmatch(name):
            fail(f"skills.pstack.exclude entries must match {SKILL_NAME_RE.pattern}: {name!r}")
        if name in declared:
            fail(f"skills.pstack.exclude names {name}, which skills.audience declares under {SHARED_SKILLS_ROOT}")
    return declared, pstack_audience, exclude


def codex_disabled_skills(manifest: dict[str, Any]) -> list[str]:
    """The shared-root skills whose audience leaves out Codex, each disabled by a `[[skills.config]]` entry."""
    declared, _, _ = skill_audiences(manifest)
    return sorted(name for name, audience in declared.items() if "codex" not in audience)


def omp_skill_settings(manifest: dict[str, Any], consumer: str) -> dict[str, Any]:
    """One omp consumer's skills: off when no skill names it, else its roots and the declared names it is not given.

    omp matches `skills.ignoredSkills` against the raw name of every skill from every source, custom directories
    included (omp 18.11.3 src/extensibility/skills.ts:354-375, :495-496), and `skills.enabled: false` returns no skill
    at all (:307-310).
    """
    declared, pstack_audience, exclude = skill_audiences(manifest)
    has_pstack = consumer in pstack_audience
    if not has_pstack and not any(consumer in audience for audience in declared.values()):
        return {"enabled": False, "pstack": False}
    directories = list(omp_skills_directories(manifest)) + ([PSTACK_SKILLS_ROOT] if has_pstack else [])
    ignored = [name for name, audience in declared.items() if consumer not in audience]
    return {
        "enabled": True,
        "pstack": has_pstack,
        "customDirectories": directories,
        "ignoredSkills": sorted(ignored + (exclude if has_pstack else [])),
    }


def omp_skills_yaml(settings: dict[str, Any], home: str) -> str:
    """The `skills:` block; `home` replaces a leading ~/ of each directory (the overlays carry the absolute home)."""
    if not settings["enabled"]:
        return "skills:\n  enabled: false\n"
    entries = "".join(f"    - {re.sub(r'^~/', home, directory)}\n" for directory in settings["customDirectories"])
    ignored = "".join(f"    - {name}\n" for name in settings["ignoredSkills"])
    return (
        "skills:\n  customDirectories:\n"
        + entries
        + ("  ignoredSkills:\n" + ignored if ignored else "  ignoredSkills: []\n")
    )


def omp_config_yaml(model: str, skills: str) -> str:
    return f"# {GENERATED_HEADER}\nmodelRoles:\n  default: {model}\n{skills}"


OMP_TOOL_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


def omp_interactive_policy(manifest: dict[str, Any]) -> str:
    """The `tools.approval` and `bash.patterns` denies of a plain omp launch; empty when the key is absent.

    The approval mode is left to omp and the operator (U66 F043, coordinator decision): an operator-driven session
    keeps omp's default `yolo` and gets only outright denies, which omp honours in every mode
    (src/tools/approval.ts:240-257).
    """
    policy = manifest.get("omp", {}).get("interactive_policy")
    if policy is None:
        return ""
    if not isinstance(policy, dict) or sorted(policy) != ["bash_deny", "tool_deny"]:
        fail("omp.interactive_policy must be a mapping of exactly tool_deny and bash_deny")
    tools = policy["tool_deny"]
    if not isinstance(tools, list) or not all(isinstance(t, str) and OMP_TOOL_NAME_RE.fullmatch(t) for t in tools):
        fail("omp.interactive_policy.tool_deny must be a list of omp tool names")
    denies = policy["bash_deny"]
    if not isinstance(denies, list) or not denies or not all(isinstance(d, str) and d.strip() for d in denies):
        fail("omp.interactive_policy.bash_deny must be a non-empty list of bash.patterns match strings")
    if len(set(denies)) != len(denies) or len(set(tools)) != len(tools):
        fail("omp.interactive_policy repeats an entry")
    approval = "".join(f"    {tool}: deny\n" for tool in tools)
    rules = "".join(f"    - match: {json.dumps(deny)}\n      approval: deny\n" for deny in denies)
    return (f"tools:\n  approval:\n{approval}" if approval else "") + f"bash:\n  patterns:\n{rules}"


def render_omp_config(manifest: dict[str, Any]) -> str:
    skills = omp_skills_yaml(omp_skill_settings(manifest, "omp"), "~/")
    config = omp_config_yaml(interactive_profile(manifest)["omp"]["model"], skills)
    return (
        config
        + omp_list_yaml("extensions", omp_extensions(manifest))
        + omp_list_yaml("disabledProviders", omp_disabled_providers(manifest))
        + omp_interactive_policy(manifest)
    )


def omp_list_yaml(key: str, items: list[str]) -> str:
    # An empty list still renders, so the merge script owns the key on every apply.
    if not items:
        return f"{key}: []\n"
    return f"{key}:\n" + "".join(f"  - {item}\n" for item in items)


def render_omp_role_overlay(manifest: dict[str, Any], role: str) -> str:
    # A session expands ~ in skills.customDirectories (src/extensibility/skills.ts:471-473) but
    # `omp skill list` resolves a non-absolute entry against cwd (src/cli/skill-list.ts:58-64),
    # so the deployed overlay carries the absolute home through the chezmoi template.
    skills = omp_skills_yaml(omp_skill_settings(manifest, f"omp-{role}"), "{{ .chezmoi.homeDir }}/")
    omp = model_profiles(manifest)[omp_roles(manifest)[role]]["omp"]
    overlay = omp_config_yaml(omp["model"], skills)
    # A `modelRoles.default` without a `:<level>` suffix starts at the `defaultThinkingLevel` setting (omp 18.11.3
    # src/config/model-presets.ts:232-244), whose default is high (src/session/settings.ts:196-201); a `--config`
    # overlay is a settings layer above the profile's own config.yml (src/config/settings.ts:879).
    overlay += f"defaultThinkingLevel: {omp['effort']}\n"
    disabled = "".join(f"  - {provider}\n" for provider in omp_seat_disabled_providers(manifest))
    if disabled:
        overlay += f"disabledProviders:\n{disabled}"
    # A seat profile has no setup record, so omp's cold-launch gate (src/main.ts:668-677) would open the
    # first-run wizard over the pane: startup.setupWizard=false empties the scene list (pi-tui
    # src/setup/wizard.ts:52) and setupVersion=2 (CURRENT_SETUP_VERSION) skips the gate's wizard import.
    return overlay + "setupVersion: 2\nstartup:\n  setupWizard: false\n"


def render_claude_express_agent(manifest: dict[str, Any]) -> str:
    express = model_profiles(manifest)["express"]["claude"]
    return (
        "---\n"
        "name: express-explorer\n"
        "description: Read-only exploration on a low-cost model. Use for codebase searches, file location, and fact gathering whose verbose output should stay out of the main context.\n"
        "tools: Read, Glob, Grep\n"
        f"model: {express['model']}\n"
        f"effort: {express['effort']}\n"
        "---\n"
        "\n"
        f"<!-- {GENERATED_HEADER} -->\n"
        "\n"
        "You are a fast, read-only codebase explorer. Locate files, trace call\n"
        "paths, and report findings as compact summaries with file:line\n"
        "references. Never edit files and never run shell commands. Say so when a\n"
        "question needs deeper analysis than a read-only pass can support.\n"
        "When `.ua/knowledge-graph.json` exists and `.ua/meta.json` `gitCommitHash` matches HEAD, grep/read that graph first to locate nodes by `summary` and `filePath` before sweeping the tree.\n"
    )


def render_claude_project_map_agent(manifest: dict[str, Any]) -> str:
    standard = model_profiles(manifest)["standard"]["claude"]
    return (
        "---\n"
        "name: project-map\n"
        'description: Draws the project map, one double-click HTML file under .project-map/, with part status, milestones, items left to the next milestone, the suggested next step, and what changed since the last update. Use before a long solo run, after each milestone, and to answer "どこまで進んだ？".\n'
        "tools: Read, Glob, Grep, Bash, Write, Edit\n"
        f"model: {standard['model']}\n"
        f"effort: {standard['effort']}\n"
        "memory: user\n"
        "skills:\n"
        "  - project-map\n"
        "  - dataviz\n"
        "  - artifact-design\n"
        "color: cyan\n"
        "---\n"
        "\n"
        f"<!-- {GENERATED_HEADER} -->\n"
        "\n"
        "You draw the project map and nothing else. Follow the preloaded\n"
        "project-map skill exactly and in full; nothing in this body adds to\n"
        "it or narrows it.\n"
    )


STANDING_RULE_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
STANDING_RULE_AGENTS = ("claude", "codex")
# Generated roots that hold nothing but rendered standing rules, so a file there outside the expected outputs is stale.
CLAUDE_RULES_DIR = "home/dot_claude/rules"
# The omp seats' rules: ~/.agents/omp/rules/<role>.md, which the seat launchers pass as --append-system-prompt. No
# discovery provider reads that path, and the explicit flag wins over every discovered APPEND_SYSTEM.md, a project's
# included (omp docs system-prompt-customization.md). The seat overlays disable the native provider (U66), so a
# profile's ~/.omp/profiles/<role>/agent/AGENTS.md, this unit's first delivery, never loaded; that root is retired
# and still scanned so a leftover file there is swept and its target removed from hosts.
OMP_RULES_DIR = "home/dot_agents/omp/rules"
OMP_PROFILES_DIR = "home/dot_omp/private_profiles"
CODEX_RULES_FILE = "home/dot_codex/AGENTS.md.tmpl"
CHEZMOIREMOVE = "home/.chezmoiremove"
REMOVALS_BEGIN = (
    "# >>> retired standing-rule targets (generated by scripts/generate-agent-configs.py; edit standing_rules) >>>\n"
)
REMOVALS_END = "# <<< retired standing-rule targets <<<\n"
SKILL_REMOVALS_BEGIN = (
    "# >>> retired skill link targets (generated by scripts/generate-agent-configs.py; edit skills.audience) >>>\n"
)
SKILL_REMOVALS_END = "# <<< retired skill link targets <<<\n"
PSTACK_ALIASES = ("opus", "sonnet", "haiku", "fable")
PSTACK_PARENT_VALUES = ("inherit-parent", "auto")


def standing_rule_audiences(manifest: dict[str, Any]) -> list[str]:
    """Every audience a standing rule may name: the two agents and each omp seat role except the audit."""
    return [*STANDING_RULE_AGENTS, *(f"omp-{role}" for role in omp_roles(manifest) if role != "audit")]


def standing_rules(manifest: dict[str, Any]) -> tuple[str, dict[str, list[str]]]:
    """The rule source directory and rule name -> audience, refusing a rule that could reach an agent it is not for."""
    section = manifest.get("standing_rules")
    if not isinstance(section, dict):
        fail("standing_rules must be a mapping")
    source_dir = section.get("source_dir")
    parts = Path(source_dir).parts if isinstance(source_dir, str) else ()
    if parts[:1] != ("home",) or len(parts) < 2 or any(part in ("..", ".") for part in parts):
        fail("standing_rules.source_dir must be a relative path under home/")
    rules = section.get("rules")
    if not isinstance(rules, dict) or not rules:
        fail("standing_rules.rules must be a non-empty mapping")
    allowed = standing_rule_audiences(manifest)
    for name, audience in rules.items():
        if not isinstance(name, str) or not STANDING_RULE_NAME_RE.match(name):
            fail(f"standing rule name must match {STANDING_RULE_NAME_RE.pattern}: {name!r}")
        if not isinstance(audience, list) or not audience or len(set(audience)) != len(audience):
            fail(f"standing rule {name} needs a non-empty audience list without repeats")
        if "omp-audit" in audience:
            fail(f"standing rule {name} cannot reach omp-audit: the audit's rules are origin/main AGENTS.md alone")
        unknown = [agent for agent in audience if agent not in allowed]
        if unknown:
            fail(f"standing rule {name} names unknown audience {unknown}; expected some of {allowed}")
        source = ROOT / source_dir / f"{name}.md"
        if not source.is_file():
            fail(f"standing rule {name} has no source file {source.relative_to(ROOT)}")
        if source.read_text().startswith("---") and audience != ["claude"]:
            fail(f"standing rule {name} has front matter, which only Claude Code reads; its audience must be [claude]")
    sources = {path.stem for path in (ROOT / source_dir).glob("*.md")}
    undeclared = sorted(sources - set(rules))
    if undeclared:
        fail(f"files in {source_dir} are not declared in standing_rules.rules: {undeclared}")
    return source_dir, rules


def render_rule_includes(source_dir: str, names: list[str]) -> str:
    """A chezmoi template whose output is the named rule sources, read from the source state at apply time.

    A blank line separates two rules; the last include trims the template's own final newline, so a one-rule
    file renders byte for byte as its source.
    """
    include_root = source_dir.removeprefix("home/")
    includes = "\n".join(f'{{{{ include "{include_root}/{name}.md" }}}}' for name in names)
    return "{{- /* " + GENERATED_HEADER + " */ -}}\n" + includes.removesuffix("}}") + "-}}\n"


def render_standing_rules(manifest: dict[str, Any]) -> dict[Path, str]:
    """Each agent's rendered standing rules; none when the manifest declares no standing_rules section."""
    if "standing_rules" not in manifest:
        return {}
    source_dir, rules = standing_rules(manifest)
    outputs: dict[Path, str] = {}
    for name, audience in rules.items():
        if "claude" in audience:
            outputs[ROOT / CLAUDE_RULES_DIR / f"{name}.md.tmpl"] = render_rule_includes(source_dir, [name])
    codex = [name for name, audience in rules.items() if "codex" in audience]
    if codex:
        outputs[ROOT / "home/dot_codex/AGENTS.md.tmpl"] = render_rule_includes(source_dir, codex)
    for role in omp_roles(manifest):
        names = [name for name, audience in rules.items() if f"omp-{role}" in audience]
        if names:
            outputs[ROOT / OMP_RULES_DIR / f"{role}.md.tmpl"] = render_rule_includes(source_dir, names)
    return outputs


def pstack_model_value(manifest: dict[str, Any], role: str, value: Any) -> str:
    if isinstance(value, list) and value:
        return ", ".join(pstack_model_value(manifest, role, item) for item in value)
    if not isinstance(value, str):
        fail(f"standing_rules.pstack_models role {role!r} must be a profile name, inherit-parent, auto or a list")
    if value in PSTACK_PARENT_VALUES:
        return value
    profile = model_profiles(manifest).get(value)
    if profile is None:
        fail(f"standing_rules.pstack_models role {role!r} names no model_profiles entry: {value!r}")
    model = profile["claude"]["model"]
    alias = model if model in PSTACK_ALIASES else re.sub(r"^claude-([a-z]+)-.*$", r"\1", model)
    if alias not in PSTACK_ALIASES:
        fail(f"model_profiles.{value}.claude.model {model!r} has no Claude Code alias among {PSTACK_ALIASES}")
    return f"{alias} {profile['claude']['effort']}"


def render_pstack_models(manifest: dict[str, Any]) -> str:
    """pstack's per-role model rule for Claude Code, in the shape setup-pstack writes (no front matter)."""
    section = manifest["standing_rules"].get("pstack_models")
    if not isinstance(section, dict) or not isinstance(section.get("roles"), dict) or not section["roles"]:
        fail("standing_rules.pstack_models needs a budget and a non-empty roles mapping")
    lines = [
        "# pstack model configuration. One line per role; a role without a line falls back to the skill default.",
        "",
        f"# {GENERATED_HEADER} Change standing_rules.pstack_models there; chezmoi apply replaces any other write.",
        "",
        (
            "# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit the Agent tool's"
            " `model`). Alias entries in a panel list still count toward its fan-out."
        ),
        "",
        f"# budget: {section['budget']}",
        "",
    ]
    lines += [f"{role}: {pstack_model_value(manifest, role, value)}" for role, value in section["roles"].items()]
    return "\n".join(lines) + "\n"


def expected_outputs(manifest: dict[str, Any]) -> dict[Path, str]:
    outputs = {
        ROOT / manifest["codex"]["config_path"]: render_codex(manifest),
        ROOT / manifest["claude"]["settings_path"]: render_claude_settings(manifest),
        ROOT / manifest["plugins"]["marketplace_path"]: render_marketplace(manifest),
    }
    for name, profile in sorted(model_profiles(manifest).items()):
        outputs[ROOT / "home/dot_codex" / f"modify_private_{name}.config.toml"] = render_codex_profile_modify(
            name, profile, manifest
        )
    outputs[ROOT / "home/dot_codex/modify_private_config.toml"] = render_codex_base_modify(manifest)
    outputs[ROOT / "home/dot_agents/model-profiles.env"] = render_model_profiles_env(manifest)
    outputs[ROOT / "home/.chezmoitemplates/omp-config-managed.yml"] = render_omp_config(manifest)
    for role in omp_roles(manifest):
        outputs[ROOT / "home/dot_agents/omp/profiles" / f"{role}.yml.tmpl"] = render_omp_role_overlay(manifest, role)
    outputs[ROOT / "home/dot_claude/agents/express-explorer.md"] = render_claude_express_agent(manifest)
    outputs[ROOT / "home/dot_claude/agents/project-map.md"] = render_claude_project_map_agent(manifest)
    outputs.update(claude_skill_symlink_outputs(manifest))
    outputs.update(render_asset_constants(manifest))
    outputs.update(render_lever_installs(manifest))
    outputs.update(render_standing_rule_outputs(manifest, outputs))
    remove_path = ROOT / CHEZMOIREMOVE
    current = outputs.get(remove_path)
    if current is None:
        current = read_exact(remove_path) if remove_path.exists() else ""
    outputs[remove_path] = render_chezmoiremove(
        current, skill_removals(manifest, current), SKILL_REMOVALS_BEGIN, SKILL_REMOVALS_END
    )
    outputs[ROOT / OUTPUT_INDEX_PATH] = render_output_index(outputs, lever_pins(manifest), skill_index(manifest))
    return outputs


def render_standing_rule_outputs(manifest: dict[str, Any], outputs: dict[Path, str] | None = None) -> dict[Path, str]:
    """The rendered standing rules, pstack's model rule, and the .chezmoiremove block that retires a target on hosts.

    `outputs` holds the other expected outputs, so a file in a rule root none of them names is read as stale.
    """
    if "standing_rules" not in manifest:
        return {}
    rules = render_standing_rules(manifest)
    if "pstack_models" in manifest["standing_rules"]:
        rules[ROOT / CLAUDE_RULES_DIR / "pstack-models.md"] = render_pstack_models(manifest)
    stale = stale_standing_rule_outputs({**(outputs or {}), **rules})
    remove_path = ROOT / CHEZMOIREMOVE
    current = read_exact(remove_path) if remove_path.exists() else ""
    rules[remove_path] = render_chezmoiremove(current, standing_rule_removals(manifest, rules, stale, current))
    return rules


# The only source names the generator emits for standing rules, each with the target chezmoi applies it to. A file in
# a generated rule root that matches none is not the generator's: it is refused, never guessed at, because chezmoi
# attributes (readonly_, empty_, ...) can change the target in ways the generator does not model.
GENERATED_RULE_TARGETS = (
    (re.compile(r"dot_claude/rules/([a-z][a-z0-9-]*)\.md\.tmpl"), r".claude/rules/\1.md"),
    (re.compile(r"dot_claude/rules/(pstack-models)\.md"), r".claude/rules/\1.md"),
    (re.compile(r"dot_codex/AGENTS\.md\.tmpl"), ".codex/AGENTS.md"),
    (re.compile(r"dot_agents/omp/rules/([a-z][a-z0-9_-]*)\.md\.tmpl"), r".agents/omp/rules/\1.md"),
    (
        re.compile(r"dot_omp/private_profiles/private_([a-z][a-z0-9_-]*)/private_agent/AGENTS\.md\.tmpl"),
        r".omp/profiles/\1/agent/AGENTS.md",
    ),
)


def generated_rule_target(source: Path) -> str | None:
    """The target of a standing-rule source the generator emits, or None for any other name."""
    name = source.relative_to(ROOT / "home").as_posix()
    for pattern, target in GENERATED_RULE_TARGETS:
        match = pattern.fullmatch(name)
        if match:
            return match.expand(target)
    return None


def removal_block_entries(text: str, begin: str = REMOVALS_BEGIN, end: str = REMOVALS_END) -> set[str]:
    if begin not in text:
        return set()
    block = text.split(begin, 1)[1].split(end, 1)[0]
    return {line for line in block.splitlines() if line and not line.startswith("#")}


def standing_rule_removals(
    manifest: dict[str, Any], rules: dict[Path, str], stale: list[Path], current: str
) -> list[str]:
    """Every standing-rule target no agent receives now, so chezmoi apply removes the copy a host still holds.

    The candidates are each declared rule's Claude file, the Codex AGENTS.md and every omp role's profile AGENTS.md
    (the audit's included); a stale rule output's target and the block's earlier entries stay, so a rule deleted from
    the manifest keeps its removal. A target rendered again leaves the block.
    """
    _, declared = standing_rules(manifest)
    candidates = {f".claude/rules/{name}.md" for name in declared}
    candidates.add(".codex/AGENTS.md")
    candidates |= {f".agents/omp/rules/{role}.md" for role in omp_roles(manifest)}
    candidates |= {f".omp/profiles/{role}/agent/AGENTS.md" for role in omp_roles(manifest)}
    rendered = {generated_rule_target(path) for path in rules if path.name != ".chezmoiremove"}
    if None in rendered:
        fail("a rendered standing rule has a source name GENERATED_RULE_TARGETS does not list")
    retired = candidates | {generated_rule_target(path) for path in stale} | removal_block_entries(current)
    return sorted(retired - rendered)


def render_chezmoiremove(text: str, removals: list[str], begin: str = REMOVALS_BEGIN, end: str = REMOVALS_END) -> str:
    block = begin + "".join(f"{target}\n" for target in removals) + end
    if begin not in text:
        return text + ("" if not text or text.endswith("\n") else "\n") + block
    head, rest = text.split(begin, 1)
    return head + block + rest.split(end, 1)[1]


def stale_standing_rule_outputs(outputs: dict[Path, str]) -> list[Path]:
    """Generator-named files in the rule roots that no expected output names; any other file there is refused.

    Every file under the Claude rules, omp seat rules and retired omp profile roots, and the Codex AGENTS.md template,
    is the generator's. One no output names is stale when its name is one the generator emits (GENERATED_RULE_TARGETS,
    so its target is known); a file with any other name (a chezmoi attribute such as readonly_ or empty_, a hand-added
    file) fails the run, check or not, before anything is written or removed.
    """
    candidates: list[Path] = []
    for root in (ROOT / CLAUDE_RULES_DIR, ROOT / OMP_RULES_DIR, ROOT / OMP_PROFILES_DIR):
        if root.is_dir():
            candidates += [path for path in sorted(root.rglob("*")) if path.is_file()]
    codex = ROOT / CODEX_RULES_FILE
    if codex.is_file():
        candidates.append(codex)
    unknown = [path for path in candidates if generated_rule_target(path) is None]
    if unknown:
        names = ", ".join(str(path.relative_to(ROOT)) for path in unknown)
        fail(f"not generated by scripts/generate-agent-configs.py; remove or rename by hand: {names}")
    return [path for path in candidates if path not in outputs]  # lint-comparisons: allow Path-object keys


def remove_stale_generated_outputs(outputs: dict[Path, str]) -> None:
    """Delete the stale standing-rule sources and the omp profile directories they leave empty."""
    for path in stale_standing_rule_outputs(outputs):
        path.unlink()
    omp_root = ROOT / OMP_PROFILES_DIR
    if omp_root.is_dir():
        for path in sorted(omp_root.rglob("*"), reverse=True):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()


# The expected output set rendered for consumers that cannot load the manifest: make doctor runs
# scripts/check-agent-runtime.py on the system python3, without PyYAML. It lives outside home/, so chezmoi never
# deploys it.
OUTPUT_INDEX_PATH = "scripts/generated-agent-outputs.json"
# The generated directories: every file a glob matches here is a generator output, so one that expected_outputs()
# does not render is an orphan, which --check reports and a write run deletes (F056). Each entry is a source
# directory and a pathlib glob; generated_scopes() adds the lever rule, and the doctor checks the deployed side of
# every scope it returns.
GENERATED_SCOPES = (
    ("home/dot_agents/omp/profiles", "*"),
    ("home/dot_agents/plugins", "**/*"),
    ("home/dot_claude/agents", "*"),
    ("home/dot_claude/skills", "**/*"),
    ("home/dot_codex", "*.config.toml"),
)
# chezmoi source-state attributes, in the order chezmoi reads them (chezmoi.io reference/source-state-attributes);
# a generated output uses no other attribute, and chezmoi_target refuses one it does not know.
CHEZMOI_DIR_PREFIXES = ("exact_", "private_", "readonly_")
CHEZMOI_FILE_TYPES = ("create_", "modify_", "symlink_")
CHEZMOI_FILE_PREFIXES = ("private_", "readonly_", "empty_", "executable_")
CHEZMOI_UNSUPPORTED = ("encrypted_", "remove_", "run_", "external_", "literal_", "once_", "onchange_")


def chezmoi_target(source: Path) -> dict[str, Any] | None:
    """How chezmoi deploys one generated file: its HOME-relative target, the kind of entry, and its mode.

    None for a file chezmoi does not deploy by itself: anything outside home/, and any source entry whose name starts
    with a dot, which chezmoi ignores (chezmoi.io reference/source-state-attributes), the .chezmoitemplates that the
    modify scripts read among them.
    """
    rel = source.relative_to(ROOT)
    if rel.parts[0] != "home" or any(part.startswith(".") for part in rel.parts[1:]):
        return None
    parts: list[str] = []
    for name in rel.parts[1:-1]:
        for prefix in CHEZMOI_DIR_PREFIXES:
            name = name.removeprefix(prefix)
        parts.append("." + name.removeprefix("dot_") if name.startswith("dot_") else name)
    name = rel.parts[-1]
    if name.startswith(CHEZMOI_UNSUPPORTED):
        fail(f"{rel} uses a chezmoi attribute the generator does not deploy")
    kind = "file"
    for prefix in CHEZMOI_FILE_TYPES:
        if name.startswith(prefix):
            kind, name = prefix.removesuffix("_"), name.removeprefix(prefix)
            break
    executable = False
    for prefix in CHEZMOI_FILE_PREFIXES:
        if name.startswith(prefix):
            executable = executable or prefix == "executable_"
            name = name.removeprefix(prefix)
    template = name.endswith(".tmpl")
    name = name.removesuffix(".tmpl")
    parts.append("." + name.removeprefix("dot_") if name.startswith("dot_") else name)
    if template and kind == "file":
        kind = "template"
    return {"target": "/".join(parts), "kind": kind, "executable": executable}


def skill_index(manifest: dict[str, Any]) -> dict[str, Any]:
    """What make doctor needs to name a skill an agent lists outside its audience, without loading the manifest.

    The roots are HOME-relative; `codex_disabled` is the managed `[[skills.config]]` set and `omp` each consumer's
    rendered settings. The doctor reads the pstack names from the deployed pstack root, the pinned archive's own.
    """
    declared, pstack_audience, exclude = skill_audiences(manifest)
    consumers = [consumer for consumer in skill_consumers(manifest) if consumer.startswith("omp")]
    omp = {}
    for consumer in consumers:
        settings = omp_skill_settings(manifest, consumer)
        omp[consumer] = {
            "enabled": settings["enabled"],
            "pstack": settings["pstack"],
            "ignored": settings.get("ignoredSkills", []),
        }
    return {
        "shared_root": SHARED_SKILLS_ROOT.removeprefix("~/"),
        "pstack_root": PSTACK_SKILLS_ROOT.removeprefix("~/"),
        "audience": {name: declared[name] for name in sorted(declared)},
        "pstack": {"audience": pstack_audience, "exclude": exclude},
        "codex_disabled": codex_disabled_skills(manifest),
        "omp": omp,
    }


def render_output_index(
    outputs: dict[Path, str], pins: dict[Path, str] | None = None, skills: dict[str, Any] | None = None
) -> str:
    """The deployed side of the expected output set, for make doctor.

    `outputs` lists every generated file with its deployed target (none for one chezmoi does not deploy by itself),
    and a lever copy also with the sha256 it is pinned to; `scopes` lists each generated directory's deployed
    directory and glob, where a file no output deploys is an orphan on the host; `skills` is skill_index's.
    """
    pins = pins or {}
    entries = []
    for path in sorted(outputs):
        target = chezmoi_target(path)
        rel = path.relative_to(ROOT)
        # chezmoi reads its own .chezmoi* sources (.chezmoitemplates, the generated .chezmoiremove block) in place.
        if target is None and rel.parts[0] == "home" and not rel.parts[1].startswith(".chezmoi"):
            fail(f"{rel} is generated under home/ but chezmoi ignores its dot-prefixed name, so it never deploys")
        entry = {"source": rel.as_posix(), **(target or {"target": None})}
        pin = pins.get(path)
        if pin is not None:
            entry["sha256"] = pin
        entries.append(entry)
    scopes = []
    for directory, pattern in generated_scopes():
        root = chezmoi_target(ROOT / directory / "x")
        target = chezmoi_target(ROOT / directory / pattern)
        assert root is not None and target is not None
        host_root = root["target"].removesuffix("/x")
        scopes.append(
            {"source": directory, "target": host_root, "glob": target["target"].removeprefix(host_root + "/")}
        )
    index: dict[str, Any] = {"generated_by": GENERATED_HEADER, "outputs": entries, "scopes": scopes}
    if skills is not None:
        index["skills"] = skills
    return json_dumps(index)


def generated_scopes() -> list[tuple[str, str]]:
    """Every generated scope as (source directory, glob): the fixed directories, then the lever rule.

    A lever's chezmoi copy is generated from its checkout script, so the install name of every scripts/orchestrator
    script is a scope of its own; a copy of one that is not a pinned lever is an unsynchronised duplicate (F156). The
    generator checks the source tree and make doctor the deployed tree against this one list.
    """
    scopes = list(GENERATED_SCOPES)
    source_dir = ROOT / LEVER_SOURCE_DIR
    if source_dir.is_dir():
        scopes.extend(
            (LEVER_INSTALL_DIR, glob.escape(f"executable_{script.name}"))
            for script in sorted(source_dir.iterdir())
            if script.is_file()
        )
    return scopes


def generated_scope_files() -> set[Path]:
    """Every file now in a generated scope of the source tree."""
    files: set[Path] = set()
    for directory, pattern in generated_scopes():
        files.update(path for path in (ROOT / directory).glob(pattern) if path.is_file() or path.is_symlink())
    return files


def orphaned_outputs(outputs: dict[Path, str]) -> list[Path]:
    """Files in a generated directory that the expected output set does not hold."""
    return sorted(generated_scope_files() - set(outputs))


def output_drift(outputs: dict[Path, str]) -> list[str]:
    """Each expected output whose bytes are missing or differ, then each orphan; empty when the tree matches the set."""
    stale = sorted(
        path for path, content in outputs.items() if not path.is_file() or path.read_bytes() != content.encode()
    )
    return [str(path.relative_to(ROOT)) for path in stale] + [
        f"{path.relative_to(ROOT)} (orphan: no manifest entry renders it)" for path in orphaned_outputs(outputs)
    ]


def remove_orphaned_outputs(outputs: dict[Path, str]) -> None:
    for path in orphaned_outputs(outputs):
        path.unlink()
    for directory, _pattern in GENERATED_SCOPES:
        root = ROOT / directory
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*"), reverse=True):
            if path.is_dir() and not path.is_symlink() and not any(path.iterdir()):
                path.rmdir()


def write_outputs(outputs: dict[Path, str]) -> None:
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        write_exact(path, content)
        if (path.parent == ROOT / "home/dot_codex" and path.name.startswith("modify_")) or (
            path.parent == ROOT / LEVER_INSTALL_DIR and path.name.startswith("executable_")
        ):
            path.chmod(path.stat().st_mode | 0o111)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated files are up to date")
    parser.add_argument(
        "--set-asset",
        action="append",
        default=[],
        metavar="NAME.FIELD=VALUE",
        help="rewrite one assets: pin or checksum in the manifest, then regenerate",
    )
    args = parser.parse_args()
    if args.set_asset and args.check:
        fail("--set-asset cannot be combined with --check")

    if args.set_asset:
        manifest_path = ROOT / "home/dot_agents/agent-config.yaml"
        text = read_exact(manifest_path)
        updates = []
        for assignment in args.set_asset:
            target, separator, value = assignment.partition("=")
            name, dot, path = target.partition(".")
            if not separator or not dot:
                fail(f"--set-asset expects NAME.FIELD=VALUE: {assignment!r}")
            text = set_asset_field(text, name, path, value)
            updates.append((name, path, value))
        yaml_error = yaml.YAMLError if yaml is not None else ()
        try:
            manifest = parse_manifest(text)
        except yaml_error as error:
            fail(f"--set-asset produced an unparsable manifest: {error}")
        for name, path, value in updates:
            current: Any = manifest["assets"][name]
            for part in path.split("."):
                current = current[part]
            if not isinstance(current, str) or current != value:
                fail(f"assets.{name}.{path} did not update to the string {value!r}: {current!r}")
        outputs = render_asset_constants(manifest)
        write_exact(manifest_path, text)
        write_outputs(outputs)
        print("asset pins updated: " + ", ".join(f"{name}.{path}" for name, path, _ in updates))
        return

    # The lever pins live in the manifest itself; the outputs below read the refreshed pins from the text in memory. A
    # test ROOT without a manifest file has no pins to refresh (load_manifest fails on its own when the real one is
    # absent). Nothing is written until every output has rendered and every refusal (an unknown file in a generated
    # rule root, a bad audience) has had its chance to fail the run, so a refused run leaves every file as it was.
    manifest_path = ROOT / "home/dot_agents/agent-config.yaml"
    stale: list[str] = []
    pinned_text: str | None = None
    if manifest_path.exists():
        manifest_text = read_exact(manifest_path)
        refreshed = refresh_lever_pins(manifest_text)
        if refreshed != manifest_text:
            pinned_text = refreshed
            stale.append(str(manifest_path.relative_to(ROOT)))
    manifest = load_manifest(pinned_text)
    outputs = expected_outputs(manifest)
    stale_rules = stale_standing_rule_outputs(outputs)
    if args.check:
        stale.extend(output_drift(outputs) + lever_pin_drift(manifest))
        stale.extend(str(path.relative_to(ROOT)) for path in stale_rules)
    else:
        stale = []
        if pinned_text is not None:
            write_exact(manifest_path, pinned_text)
        write_outputs(outputs)
        remove_orphaned_outputs(outputs)
        remove_stale_generated_outputs(outputs)
    if stale:
        fail("generated agent configs are stale: " + ", ".join(str(path) for path in stale))
    if args.check:
        print("generated agent configs are up to date")
    else:
        print("generated agent configs updated")


if __name__ == "__main__":
    main()
