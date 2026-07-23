#!/usr/bin/env python3
"""Generate agent-native configuration from the shared AI-agent manifest."""

from __future__ import annotations

import argparse
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
    if yaml is None:
        fail(
            "PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py"
        )
    data = yaml.safe_load(MANIFEST_PATH.read_text())
    if not isinstance(data, dict):
        fail(f"{MANIFEST_PATH} must contain a YAML mapping")
    if data.get("schema_version") != 1:
        fail(f"{MANIFEST_PATH} schema_version must be 1")
    return data


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
            "{ "
            + ", ".join(
                f"{quote_toml_key(str(key))} = {quote_toml(item)}"
                for key, item in value.items()
            )
            + " }"
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
}


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
            for key in keys:
                value = mapping.get(key)
                if not isinstance(value, str) or not PROFILE_VALUE_RE.match(value):
                    fail(
                        f"model profile {name}.{agent}.{key} must be a launcher-safe string"
                    )
    return profiles


def interactive_profile(manifest: dict[str, Any]) -> dict[str, Any]:
    profiles = model_profiles(manifest)
    name = manifest.get("interactive_profile")
    if name not in profiles:
        fail(f"interactive_profile must name a model profile: {name!r}")
    return profiles[name]


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
    lines.append(
        f"model_reasoning_effort = {quote_toml(profile_codex['model_reasoning_effort'])}"
    )
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
                lines.append(
                    f"{quote_toml_key(str(nested_key))} = {quote_toml(nested_value)}"
                )
    lines.extend(["", "[sandbox_workspace_write]"])
    lines.append(
        f"network_access = {quote_toml(codex['sandbox_workspace_write']['network_access'])}"
    )
    if codex["sandbox_workspace_write"].get("writable_roots") is not None:
        lines.append(
            f"writable_roots = {quote_toml(codex['sandbox_workspace_write']['writable_roots'])}"
        )
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
                lines.append(
                    f"bearer_token_env_var = {quote_toml(server['bearer_token_env_var'])}"
                )
            if server.get("http_headers"):
                lines.append(f"http_headers = {quote_toml(server['http_headers'])}")
            if server.get("env_http_headers"):
                lines.append(
                    f"env_http_headers = {quote_toml(server['env_http_headers'])}"
                )
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
        for key, value in marketplace_config.items():
            lines.append(f"{quote_toml_key(str(key))} = {quote_toml(value)}")
    hooks = codex.get("hooks", {})
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


def render_claude_settings(manifest: dict[str, Any]) -> str:
    claude = manifest["claude"]
    hooks = claude.get("hooks", {})
    post_hooks: list[dict[str, str]] = []
    if hooks.get("python_post_edit") or hooks.get("markdown_post_edit"):
        post_hooks.append(
            {
                "type": "command",
                "command": hooks["format_edited_files_hook"],
            }
        )
    profile_claude = interactive_profile(manifest)["claude"]
    settings: dict[str, Any] = {
        "$schema": claude["schema"],
        "model": profile_claude["model"],
        "effortLevel": profile_claude["effort"],
        "alwaysThinkingEnabled": claude["alwaysThinkingEnabled"],
        "autoUpdates": claude["autoUpdates"],
        "autoUpdatesChannel": claude["autoUpdatesChannel"],
        "plansDirectory": claude["plansDirectory"],
        "permissions": {
            "deny": claude["permissions"]["deny"],
            "defaultMode": claude["permissions"]["defaultMode"],
            "ask": claude["permissions"]["ask"],
        },
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
        },
        "statusLine": claude["statusLine"],
        "disableSkillShellExecution": claude["disableSkillShellExecution"],
        "includeGitInstructions": claude["includeGitInstructions"],
        "enabledPlugins": claude["enabledPlugins"],
    }
    return json_dumps(settings)


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
    for source_file in sorted(
        path for path in skills_root.rglob("*") if path.is_file()
    ):
        if source_file.name.startswith("."):
            continue
        rel = source_file.relative_to(skills_root)
        target_path = rel.with_name(chezmoi_target_name(rel.name))
        target_dir = claude_root / target_path.parent
        outputs[target_dir / f"symlink_{target_path.name}.tmpl"] = (
            render_claude_skill_symlink(source_file)
        )
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
    return "\n".join(lines) + "\n"


def render_model_profiles_env(manifest: dict[str, Any]) -> str:
    profiles = model_profiles(manifest)
    interactive_profile(manifest)
    lines = [
        "# Shell fragment sourced by agent launchers (herdr-agents, agent-fanout).",
        f"# {GENERATED_HEADER}",
        f'MODEL_PROFILE_INTERACTIVE="{manifest["interactive_profile"]}"',
    ]
    for name, profile in sorted(profiles.items()):
        var = str(name).upper()
        claude = profile["claude"]
        lines.append(
            f'MODEL_PROFILE_{var}_CLAUDE_ARGS="--model {claude["model"]} --effort {claude["effort"]}"'
        )
        lines.append(f'MODEL_PROFILE_{var}_CODEX_ARGS="--profile {name}"')
    return "\n".join(lines) + "\n"


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
    )


def expected_outputs(manifest: dict[str, Any]) -> dict[Path, str]:
    outputs = {
        ROOT / manifest["codex"]["config_path"]: render_codex(manifest),
        ROOT / manifest["claude"]["settings_path"]: render_claude_settings(manifest),
        ROOT / manifest["claude"]["mcp_config_path"]: render_claude_mcp(manifest),
        ROOT / manifest["plugins"]["marketplace_path"]: render_marketplace(manifest),
    }
    for name, profile in sorted(model_profiles(manifest).items()):
        outputs[ROOT / "home/dot_codex" / f"{name}.config.toml"] = render_codex_profile(name, profile)
    outputs[ROOT / "home/dot_agents/model-profiles.env"] = render_model_profiles_env(manifest)
    outputs[ROOT / "home/dot_claude/agents/express-explorer.md"] = render_claude_express_agent(manifest)
    for plugin in manifest["plugins"].get("codex_plugins", []):
        if not plugin.get("managed_manifest", True):
            continue
        source_path = plugin["source_path"].removeprefix("./")
        outputs[
            ROOT / "home/dot_agents" / source_path / ".codex-plugin/plugin.json"
        ] = render_codex_plugin(plugin)
    outputs.update(claude_skill_symlink_outputs())
    return outputs


def remove_stale_generated_outputs(outputs: dict[Path, str]) -> None:
    generated_roots = [ROOT / "home/dot_claude/skills"]
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="verify generated files are up to date"
    )
    args = parser.parse_args()

    manifest = load_manifest()
    outputs = expected_outputs(manifest)
    stale: list[Path] = []
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(path.relative_to(ROOT))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    if not args.check:
        remove_stale_generated_outputs(outputs)
    if stale:
        fail(
            "generated agent configs are stale: "
            + ", ".join(str(path) for path in stale)
        )
    if args.check:
        print("generated agent configs are up to date")
    else:
        print("generated agent configs updated")


if __name__ == "__main__":
    main()
