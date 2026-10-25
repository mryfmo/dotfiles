#!/usr/bin/env python3
"""Generate agent-native configuration from the shared AI-agent manifest."""

from __future__ import annotations

import argparse
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


def load_manifest() -> dict[str, Any]:
    return parse_manifest(MANIFEST_PATH.read_text())


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
# the same bytes read-only under ~/.local/bin/common, and claude.levers.sha256 pins them for the lever's own self-check.
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


def render_lever_installs(manifest: dict[str, Any]) -> dict[Path, str]:
    return {
        ROOT / LEVER_INSTALL_DIR / f"executable_{name}": (ROOT / LEVER_SOURCE_DIR / name).read_text()
        for name in lever_names(manifest)
    }


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


def target_agents(manifest: dict[str, Any]) -> set[str]:
    return set(manifest.get("target_agents", []))


def enabled_for(server: dict[str, Any], agent: str) -> bool:
    return bool(server.get("agents", {}).get(agent, False))


PROFILE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
PROFILE_VALUE_RE = re.compile(r"^[A-Za-z0-9._\[\]-]+$")
PROFILE_AGENT_KEYS = {
    "claude": ("model", "effort"),
    "codex": ("model", "model_reasoning_effort"),
    "omp": ("model",),
}
PROFILE_OPTIONAL_KEYS = {"claude": ("advisor",)}
# Claude seats route through the pi-claude-bridge provider and OpenAI seats through openai-siwc
# (D-024-129/130); anthropic stays expressible as the API-key fallback (gates G1). The openai-codex
# fallback is retired (plan 025 E1, decision 29) and refused with a message of its own.
OMP_MODEL_RE = re.compile(r"^(openai-siwc|anthropic|claude-bridge)/[A-Za-z0-9._-]+$")
# The same routes as a set, for omp.disabled_providers; a test keeps it equal to OMP_MODEL_RE's alternation.
OMP_MODEL_ROUTES = ("openai-siwc", "anthropic", "claude-bridge")
OMP_RETIRED_ROUTES = ("openai-codex",)
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
                if agent == "omp":
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
                text = path.read_text()
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

    `filesystem.denyRead` and `credentials` render the same on every OS: the Linux sandbox enforces `denyRead` globs
    and credential denies but drops the glob forms of Read/Edit permission rules (regime-cutover U17).
    """
    sandbox = manifest["claude"]["sandbox"]
    filesystem = sandbox.get("filesystem", {})
    network = dict(sandbox["network"])
    if os_name != "darwin":
        network.pop("allowMachLookup", None)
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
            **({"denyRead": list(filesystem["deny_read"])} if "deny_read" in filesystem else {}),
        },
        **(
            {"credentials": {"files": [dict(entry) for entry in sandbox["credentials"]["files"]]}}
            if "credentials" in sandbox
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
                    "matcher": "Write|Edit|MultiEdit",
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


def claude_mcp_entry(server: dict[str, Any]) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "disabled": not bool(server.get("enabled", False)),
        "timeout": server.get("timeout"),
    }
    if server["transport"] == "stdio":
        entry["type"] = "stdio"
        entry["command"] = server["command"]
        entry["args"] = server.get("args", [])
        if server.get("env"):
            entry["env"] = server["env"]
    elif server["transport"] == "http":
        entry["type"] = "http"
        entry["url"] = server["url"]
        if server.get("headers"):
            entry["headers"] = server["headers"]
    else:
        fail(f"unsupported MCP transport: {server['transport']}")
    return {key: value for key, value in entry.items() if value is not None}


def render_claude_mcp(manifest: dict[str, Any]) -> str:
    data = {
        "mcpServers": {
            name: claude_mcp_entry(server)
            for name, server in manifest.get("mcp_servers", {}).items()
            if enabled_for(server, "claude")
        }
    }
    return "{{/* " + GENERATED_HEADER + " */}}\n" + json_dumps(data)


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


def render_codex_plugin(plugin: dict[str, Any]) -> str:
    for key in ("version", "description", "author", "license", "skills", "interface"):
        if key not in plugin:
            fail(f"managed Codex plugin {plugin['name']} is missing {key}")
    data = {
        "name": plugin["name"],
        "version": plugin["version"],
        "description": plugin["description"],
        "author": {"name": plugin["author"]},
        "license": plugin["license"],
        "skills": plugin["skills"],
        "interface": {
            "displayName": plugin["interface"]["displayName"],
            "shortDescription": plugin["interface"]["shortDescription"],
            "category": plugin["category"],
            "capabilities": plugin["interface"]["capabilities"],
        },
    }
    return json_dumps(data)


def render_claude_skill_symlink(source_file: Path) -> str:
    rel = source_file.relative_to(ROOT / "home")
    return "{{ .chezmoi.sourceDir }}/" + str(rel) + "\n"


def chezmoi_target_name(source_name: str) -> str:
    return source_name.removeprefix("executable_")


def claude_skill_symlink_outputs() -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    skills_root = ROOT / "home/dot_agents/skills"
    claude_root = ROOT / "home/dot_claude/skills"
    if not skills_root.exists():
        return outputs
    for source_file in sorted(path for path in skills_root.rglob("*") if path.is_file()):
        if source_file.name.startswith("."):
            continue
        rel = source_file.relative_to(skills_root)
        target_path = rel.with_name(chezmoi_target_name(rel.name))
        target_dir = claude_root / target_path.parent
        outputs[target_dir / f"symlink_{target_path.name}.tmpl"] = render_claude_skill_symlink(source_file)
    return outputs


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
# Apply-time Codex hook trust, shared by the base and profile modify scripts. Codex runs a config or
# plugin hook only when [hooks.state."<key>"] holds the trust hash of its current definition, and that
# hash covers the absolute command path, so it is computed on each host from the hook it names.
HOOK_TRUST_CODE = """import functools
import hashlib
import json
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


def declared_hook_state(home: str) -> list:
    \"\"\"[hooks.state] chunks for the hooks the manifest trusts, hashed from their definitions on this host.\"\"\"
    chunks = []
    for entry in HOOK_TRUST["declared"]:
        key = entry["key"].replace(HOOK_TRUST_HOME, home)
        found = declared_hook(home, key)
        digest = codex_hook_hash(*found) if isinstance(found, tuple) else None
        if digest is None:
            digest = entry.get("trusted_hash")
            reason = found if isinstance(found, str) else "not a command hook"
            fallback = "using the manifest's pinned hash" if digest else "leaving it untrusted"
            print(f"warning: cannot compute hook trust for {key} ({reason}); {fallback}", file=sys.stderr)
        quoted = json.dumps(key, ensure_ascii=False)
        lines = [f"[hooks.state.{quoted}]"]
        if digest:
            lines.append(f'trusted_hash = "{digest}"')
        if "enabled" in entry:
            lines.append("enabled = " + ("true" if entry["enabled"] else "false"))
        chunks.append((f"hooks.state.{quoted}", "\\n".join(lines) + "\\n\\n"))
    return chunks


try:
    import tomllib as hook_trust_toml
except ModuleNotFoundError:  # Python < 3.11: fall back to the key grammar below.
    hook_trust_toml = None
HOOK_STATE_TABLE = re.compile(
    r\"\"\"^hooks\\s*\\.\\s*state\\s*\\.\\s*(?:"((?:[^"\\\\]|\\\\.)*)"|'([^']*)'|([A-Za-z0-9_-]+))\\s*$\"\"\"
)


def hook_state_key(name):
    \"\"\"The decoded TOML key of a `hooks.state.<key>` table name, however it is quoted, else None.\"\"\"
    if not name:
        return None
    if hook_trust_toml is not None:
        try:
            data = hook_trust_toml.loads(f"[{name}]\\n")
        except ValueError:
            return None
        hooks = data.get("hooks") if list(data) == ["hooks"] else None
        state = hooks.get("state") if isinstance(hooks, dict) and list(hooks) == ["state"] else None
        if isinstance(state, dict) and len(state) == 1:
            key, value = next(iter(state.items()))
            return key if value == {} else None
        return None
    match = HOOK_STATE_TABLE.match(name)
    if not match:
        return None
    if match.group(1) is not None:
        try:
            return json.loads('"' + match.group(1) + '"')
        except ValueError:
            return None
    return match.group(2) if match.group(2) is not None else match.group(3)


def declared_trusted_hash(chunk: str):
    match = re.search(r'^trusted_hash = "([^"]+)"$', chunk, re.MULTILINE)
    return match.group(1) if match else None


DOTTED_KEY_ASSIGNMENT = re.compile(
    r\"\"\"^\\s*((?:"(?:[^"\\\\]|\\\\.)*"|'[^']*'|[A-Za-z0-9_-]+)(?:\\s*\\.\\s*(?:"(?:[^"\\\\]|\\\\.)*"|'[^']*'|[A-Za-z0-9_-]+))*)\\s*=\"\"\"
)
# The key path each chunk opens (the root, [hooks], [hooks.state]); an assignment's dotted key extends it.
HOOK_STATE_SCOPES = {None: [], "hooks": ["hooks"], "hooks.state": ["hooks", "state"]}
INLINE_TRUSTED_HASH = re.compile(r'trusted_hash\\s*=\\s*"([^"]+)"')


def report_divergence(name: str, old, new) -> None:
    if old != new:
        print(f"warning: hook trust divergence for {name}: replacing {old} with {new}", file=sys.stderr)


KEY_SEGMENT = re.compile(r\"\"\"\\s*("(?:[^"\\\\]|\\\\.)*"|'[^']*'|[A-Za-z0-9_-]+)\\s*(?:\\.|$)\"\"\")
BARE_KEY = re.compile(r"[A-Za-z0-9_-]+")


def key_path(raw: str):
    \"\"\"The decoded segments of a dotted TOML key, bare or quoted, else None.\"\"\"
    if hook_trust_toml is not None:
        try:
            node = hook_trust_toml.loads(f"[{raw}]\\n")
        except ValueError:
            return None
        segments = []
        while isinstance(node, dict) and len(node) == 1:
            key, node = next(iter(node.items()))
            segments.append(key)
        return segments if node == {} and segments else None
    segments, index = [], 0
    while index < len(raw):
        match = KEY_SEGMENT.match(raw, index)
        if not match:
            return None
        token = match.group(1)
        if token.startswith('"'):
            try:
                token = json.loads(token)
            except ValueError:
                return None
        elif token.startswith("'"):
            token = token[1:-1]
        segments.append(token)
        index = match.end()
    return segments or None


def canonical_table_name(raw: str) -> str:
    \"\"\"One spelling per decoded key path: bare segments where TOML allows them, basic strings otherwise.\"\"\"
    segments = key_path(raw)
    if segments is None:
        return raw
    return ".".join(
        segment if BARE_KEY.fullmatch(segment) else json.dumps(segment, ensure_ascii=False).replace("\\x7f", "\\\\u007f")
        for segment in segments
    )


def drop_declared_assignments(chunk: str, declared: dict, scope: list) -> str:
    \"\"\"Drop the assignments of declared keys (inline tables or dotted keys) from a chunk whose key path is scope.\"\"\"
    kept, removed = [], {}
    string = removing = None
    for line in chunk.splitlines(keepends=True):
        if removing is None and string is None:
            match = DOTTED_KEY_ASSIGNMENT.match(line)
            path = scope + (key_path(match.group(1)) or []) if match else []
            key = path[2] if len(path) > 2 and path[:2] == ["hooks", "state"] else None
            removing = key if key in declared else None
        if removing is None:
            kept.append(line)
        else:
            removed.setdefault(removing, []).append(line)
        string = multiline_string_after(line, string)
        if string is None:
            removing = None
    for key, lines in removed.items():
        name, declared_chunk = declared[key]
        match = INLINE_TRUSTED_HASH.search("".join(lines))
        report_divergence(name, match.group(1) if match else None, declared_trusted_hash(declared_chunk))
    return "".join(kept)


def drop_declared_hook_state(chunks: list, declared: list) -> list:
    \"\"\"Drop existing entries for declared keys (the managed ones replace them), reporting each change once.\"\"\"
    by_key = {hook_state_key(name): (name, chunk) for name, chunk in declared}
    kept = []
    for name, chunk in chunks:
        key = hook_state_key(name)
        if key is not None and key in by_key:
            report_divergence(name, declared_trusted_hash(chunk), declared_trusted_hash(by_key[key][1]))
            continue
        if name in HOOK_STATE_SCOPES:
            chunk = drop_declared_assignments(chunk, by_key, HOOK_STATE_SCOPES[name])
        kept.append((name, chunk))
    return kept


def guarded_merge(merged: str, current: str, declared_keys) -> str:
    \"\"\"The merged config, or the current content unchanged unless it is valid TOML holding every declared key.\"\"\"
    if hook_trust_toml is None:
        return merged
    try:
        state = hook_trust_toml.loads(merged).get("hooks", {}).get("state", {})
        valid = isinstance(state, dict) and all(key in state for key in declared_keys)
    except (ValueError, AttributeError):  # tomllib.TOMLDecodeError is a ValueError.
        valid = False
    if valid:
        return merged
    print("WARN: codex config merge produced invalid TOML; keeping the existing file", file=sys.stderr)
    return current
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
        declared.append({"key": key, **state})
    return {"declared": declared, "config_hooks": config_hooks}


def render_hook_trust_block(manifest: dict[str, Any]) -> str:
    return HOOK_TRUST_BEGIN + f"HOOK_TRUST = {codex_hook_trust(manifest)!r}\n" + HOOK_TRUST_CODE + HOOK_TRUST_END


def render_codex_base_modify(manifest: dict[str, Any]) -> str:
    """The hand-maintained base modify script with its generated hook-trust block refreshed."""
    relative = "home/dot_codex/modify_private_config.toml"
    # A fixture ROOT (unit tests) has no base script of its own; take the repository's copy then.
    source = ROOT / relative if (ROOT / relative).exists() else Path(__file__).resolve().parents[1] / relative
    text = source.read_text()
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
        for name, chunk in split_chunks(path.read_text())
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
    current_chunks = drop_declared_hook_state(split_chunks(current) if current.strip() else [], declared)
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
    return guarded_merge(merged if merged.endswith("\\n") else merged + "\\n", current, declared_keys)


sys.stdout.write(merge_config(sys.stdin.read()))
'''.replace("__HOOK_TRUST_BLOCK__\n", render_hook_trust_block(manifest))


def render_model_profiles_env(manifest: dict[str, Any]) -> str:
    profiles = model_profiles(manifest)
    interactive_profile(manifest)
    lines = [
        "# Shell fragment sourced by agent launchers (herdr-agents).",
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


def omp_disabled_providers(manifest: dict[str, Any]) -> list[str]:
    """omp providers the seat overlays and the plain-launch config switch off as `disabledProviders`; none when absent.

    omp 18.11.3 reads one `disabledProviders` set for discovery providers (src/capability/index.ts:306-308)
    and for model providers (src/main.ts:1627), so a model route here would turn a seat's model off.
    """
    providers = manifest.get("omp", {}).get("disabled_providers", [])
    if not isinstance(providers, list):
        fail("omp.disabled_providers must be a list of omp provider ids")
    for provider in providers:
        if not isinstance(provider, str) or not OMP_PROVIDER_ID_RE.fullmatch(provider):
            fail(f"omp.disabled_providers entries must be omp provider ids: {provider!r}")
        if provider in OMP_MODEL_ROUTES:
            fail(f"omp.disabled_providers must not name the model route {provider}; disabledProviders turns it off")
    return providers


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


def omp_config_yaml(model: str, directories: list[str]) -> str:
    entries = "".join(f"    - {directory}\n" for directory in directories)
    return f"# {GENERATED_HEADER}\nmodelRoles:\n  default: {model}\nskills:\n  customDirectories:\n{entries}"


def render_omp_config(manifest: dict[str, Any]) -> str:
    config = omp_config_yaml(interactive_profile(manifest)["omp"]["model"], omp_skills_directories(manifest))
    return (
        config
        + omp_list_yaml("extensions", omp_extensions(manifest))
        + omp_list_yaml("disabledProviders", omp_disabled_providers(manifest))
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
    directories = [
        re.sub(r"^~/", "{{ .chezmoi.homeDir }}/", directory) for directory in omp_skills_directories(manifest)
    ]
    model = model_profiles(manifest)[omp_roles(manifest)[role]]["omp"]["model"]
    overlay = omp_config_yaml(model, directories)
    disabled = "".join(f"  - {provider}\n" for provider in omp_disabled_providers(manifest))
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
OMP_PROFILES_DIR = "home/dot_omp/private_profiles"
CODEX_RULES_FILE = "home/dot_codex/AGENTS.md.tmpl"
CHEZMOIREMOVE = "home/.chezmoiremove"
REMOVALS_BEGIN = (
    "# >>> retired standing-rule targets (generated by scripts/generate-agent-configs.py; edit standing_rules) >>>\n"
)
REMOVALS_END = "# <<< retired standing-rule targets <<<\n"
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
            path = ROOT / OMP_PROFILES_DIR / f"private_{role}/private_agent/AGENTS.md.tmpl"
            outputs[path] = render_rule_includes(source_dir, names)
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
        ROOT / manifest["claude"]["mcp_config_path"]: render_claude_mcp(manifest),
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
    for plugin in manifest["plugins"].get("codex_plugins", []):
        if not plugin.get("managed_manifest", True):
            continue
        source_path = plugin["source_path"].removeprefix("./")
        outputs[ROOT / "home/dot_agents" / source_path / ".codex-plugin/plugin.json"] = render_codex_plugin(plugin)
    outputs.update(claude_skill_symlink_outputs())
    outputs.update(render_asset_constants(manifest))
    outputs.update(render_lever_installs(manifest))
    outputs.update(render_standing_rule_outputs(manifest, outputs))
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
    current = remove_path.read_text() if remove_path.exists() else ""
    rules[remove_path] = render_chezmoiremove(current, standing_rule_removals(manifest, rules, stale, current))
    return rules


def chezmoi_target(source: Path) -> str:
    """The destination path, relative to $HOME, that chezmoi applies a source file under home/ to."""
    parts = []
    for part in source.relative_to(ROOT / "home").parts:
        for prefix in ("private_", "executable_", "symlink_"):
            part = part.removeprefix(prefix)
        parts.append("." + part.removeprefix("dot_") if part.startswith("dot_") else part)
    return "/".join(parts).removesuffix(".tmpl")


def removal_block_entries(text: str) -> set[str]:
    if REMOVALS_BEGIN not in text:
        return set()
    block = text.split(REMOVALS_BEGIN, 1)[1].split(REMOVALS_END, 1)[0]
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
    candidates |= {f".omp/profiles/{role}/agent/AGENTS.md" for role in omp_roles(manifest)}
    rendered = {chezmoi_target(path) for path in rules if path.name != ".chezmoiremove"}
    retired = candidates | {chezmoi_target(path) for path in stale} | removal_block_entries(current)
    return sorted(retired - rendered)


def render_chezmoiremove(text: str, removals: list[str]) -> str:
    block = REMOVALS_BEGIN + "".join(f"{target}\n" for target in removals) + REMOVALS_END
    if REMOVALS_BEGIN not in text:
        return text + ("" if not text or text.endswith("\n") else "\n") + block
    head, rest = text.split(REMOVALS_BEGIN, 1)
    return head + block + rest.split(REMOVALS_END, 1)[1]


def stale_standing_rule_outputs(outputs: dict[Path, str]) -> list[Path]:
    """Files in the rule roots no expected output names: every file there is rendered, so any other one is stale."""
    stale: list[Path] = []
    for root in (ROOT / CLAUDE_RULES_DIR, ROOT / OMP_PROFILES_DIR):
        if root.is_dir():
            files = [path for path in sorted(root.rglob("*")) if path.is_file()]
            stale += [path for path in files if path not in outputs]  # lint-comparisons: allow Path-object keys
    codex = ROOT / CODEX_RULES_FILE
    if codex.is_file() and codex not in outputs:
        stale.append(codex)
    return stale


def remove_stale_generated_outputs(outputs: dict[Path, str]) -> None:
    for path in stale_standing_rule_outputs(outputs):
        path.unlink()
    generated_roots = [ROOT / "home/dot_claude/skills", ROOT / OMP_PROFILES_DIR]
    output_set = set(outputs)
    for generated_root in generated_roots:
        if not generated_root.exists():
            continue
        for path in sorted(generated_root.rglob("*"), reverse=True):
            if (
                path.is_file()
                and path.name.startswith("symlink_")
                and path.suffix == ".tmpl"
                and path not in output_set
            ):
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()


def write_outputs(outputs: dict[Path, str]) -> None:
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        if (path.parent == ROOT / "home/dot_codex" and path.name.startswith("modify_")) or (
            path.parent == ROOT / LEVER_INSTALL_DIR and path.name.startswith("executable_")
        ):
            path.chmod(path.stat().st_mode | 0o111)


def stale_profile_outputs(manifest: dict[str, Any]) -> list[Path]:
    return [
        ROOT / "home/dot_codex" / f"{name}.config.toml"
        for name in model_profiles(manifest)
        if (ROOT / "home/dot_codex" / f"{name}.config.toml").exists()
    ]


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
        text = manifest_path.read_text()
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
        manifest_path.write_text(text)
        write_outputs(outputs)
        print("asset pins updated: " + ", ".join(f"{name}.{path}" for name, path, _ in updates))
        return

    # The lever pins live in the manifest itself; refresh them first so the outputs below read current pins. A test
    # ROOT without a manifest file has no pins to refresh (load_manifest fails on its own when the real one is absent).
    manifest_path = ROOT / "home/dot_agents/agent-config.yaml"
    stale: list[Path] = []
    if manifest_path.exists():
        manifest_text = manifest_path.read_text()
        pinned_text = refresh_lever_pins(manifest_text)
        if pinned_text != manifest_text:
            if args.check:
                stale.append(manifest_path.relative_to(ROOT))
            else:
                manifest_path.write_text(pinned_text)
    manifest = load_manifest()
    outputs = expected_outputs(manifest)
    stale_profiles = stale_profile_outputs(manifest)
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(path.relative_to(ROOT))
    if args.check:
        stale.extend(path.relative_to(ROOT) for path in stale_profiles)
        stale.extend(path.relative_to(ROOT) for path in stale_standing_rule_outputs(outputs))
    if not args.check:
        write_outputs(outputs)
        for path in stale_profiles:
            path.unlink()
        remove_stale_generated_outputs(outputs)
    if stale:
        fail("generated agent configs are stale: " + ", ".join(str(path) for path in stale))
    if args.check:
        print("generated agent configs are up to date")
    else:
        print("generated agent configs updated")


if __name__ == "__main__":
    main()
