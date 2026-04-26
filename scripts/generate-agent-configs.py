#!/usr/bin/env python3
"""Generate agent-native configuration from the shared AI-agent manifest."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - CI installs PyYAML for this script.
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "home/dot_agents/agent-config.yaml"
GENERATED_HEADER = "Generated from home/dot_agents/agent-config.yaml by scripts/generate-agent-configs.py."


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_manifest() -> dict[str, Any]:
    if yaml is None:
        fail("PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py")
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
        return "{ " + ", ".join(f"{key} = {quote_toml(item)}" for key, item in value.items()) + " }"
    fail(f"unsupported TOML value: {value!r}")


def target_agents(manifest: dict[str, Any]) -> set[str]:
    return set(manifest.get("target_agents", []))


def enabled_for(server: dict[str, Any], agent: str) -> bool:
    return bool(server.get("agents", {}).get(agent, False))


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
    for key in (
        "model",
        "approval_policy",
        "sandbox_mode",
        "web_search",
        "project_doc_max_bytes",
        "project_doc_fallback_filenames",
    ):
        lines.append(f"{key} = {quote_toml(codex[key])}")
    lines.extend(["", "[sandbox_workspace_write]"])
    lines.append(f"network_access = {quote_toml(codex['sandbox_workspace_write']['network_access'])}")
    lines.extend(["", "[shell_environment_policy]"])
    lines.append(f"inherit = {quote_toml(codex['shell_environment_policy']['inherit'])}")

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
    settings: dict[str, Any] = {
        "$schema": claude["schema"],
        "model": claude["model"],
        "alwaysThinkingEnabled": claude["alwaysThinkingEnabled"],
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
    return (
        "{{/* " + GENERATED_HEADER + " */}}\n"
        + json_dumps(data)
    )


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def render_hermes(manifest: dict[str, Any]) -> str:
    hermes = manifest["hermes"]
    base_path = ROOT / hermes["base_config_path"]
    base_data = yaml.safe_load(base_path.read_text()) or {}
    if not isinstance(base_data, dict):
        fail(f"{base_path} must contain a YAML mapping")
    data: dict[str, Any] = deep_merge(
        base_data,
        {
            "skills": {
                "external_dirs": [manifest["skills"]["canonical_dir"]],
                "creation_nudge_interval": manifest["skills"]["creation_nudge_interval"],
            },
            "terminal": hermes["terminal"],
            "plugins": hermes["plugins"],
            "mcp_servers": {},
        },
    )
    for name, server in manifest.get("mcp_servers", {}).items():
        if not enabled_for(server, "hermes"):
            continue
        entry: dict[str, Any] = {"enabled": server["enabled"]}
        if server["transport"] == "stdio":
            entry["command"] = server["command"]
            entry["args"] = server.get("args", [])
        elif server["transport"] == "http":
            entry["url"] = server["url"]
            if server.get("headers"):
                entry["headers"] = server["headers"]
        else:
            fail(f"unsupported MCP transport for {name}: {server['transport']}")
        for key in ("env", "timeout", "connect_timeout"):
            if key in server:
                entry[key] = server[key]
        tools: dict[str, Any] = {}
        if "include_tools" in server:
            tools["include"] = server["include_tools"]
        if "prompts" in server:
            tools["prompts"] = server["prompts"]
        if "resources" in server:
            tools["resources"] = server["resources"]
        if tools:
            entry["tools"] = tools
        if "sampling" in server:
            entry["sampling"] = {"enabled": server["sampling"]}
        data["mcp_servers"][name] = entry

    body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    return (
        "# Hermes Agent configuration managed by chezmoi.\n"
        f"# {GENERATED_HEADER}\n"
        "# Keep API keys and tokens in ~/.hermes/.env or a private chezmoi source, not here.\n\n"
        + body
    )


def render_marketplace(manifest: dict[str, Any]) -> str:
    plugins = manifest["plugins"]
    data = {
        "name": plugins["marketplace"]["name"],
        "interface": {"displayName": plugins["marketplace"]["displayName"]},
        "plugins": [
            {
                "name": plugin["name"],
                "source": {"source": "local", "path": plugin["source_path"]},
                "policy": {
                    "installation": plugin["installation"],
                    "authentication": plugin["authentication"],
                },
                "category": plugin["category"],
            }
            for plugin in plugins.get("codex_plugins", [])
        ],
    }
    return json_dumps(data)


def render_codex_plugin(plugin: dict[str, Any]) -> str:
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
        target_dir = claude_root / rel.parent
        outputs[target_dir / f"symlink_{rel.name}.tmpl"] = render_claude_skill_symlink(source_file)
    return outputs


def expected_outputs(manifest: dict[str, Any]) -> dict[Path, str]:
    outputs = {
        ROOT / manifest["codex"]["config_path"]: render_codex(manifest),
        ROOT / manifest["claude"]["settings_path"]: render_claude_settings(manifest),
        ROOT / manifest["claude"]["mcp_config_path"]: render_claude_mcp(manifest),
        ROOT / manifest["hermes"]["config_path"]: render_hermes(manifest),
        ROOT / manifest["plugins"]["marketplace_path"]: render_marketplace(manifest),
    }
    for plugin in manifest["plugins"].get("codex_plugins", []):
        source_path = plugin["source_path"].removeprefix("./")
        outputs[ROOT / "home/dot_agents" / source_path / ".codex-plugin/plugin.json"] = render_codex_plugin(plugin)
    outputs.update(claude_skill_symlink_outputs())
    return outputs


def remove_stale_generated_outputs(outputs: dict[Path, str]) -> None:
    generated_roots = [ROOT / "home/dot_claude/skills"]
    output_set = set(outputs)
    for generated_root in generated_roots:
        if not generated_root.exists():
            continue
        for path in sorted(generated_root.rglob("*"), reverse=True):
            if path.is_file() and path.name.startswith("symlink_") and path.suffix == ".tmpl" and path not in output_set:
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated files are up to date")
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
        fail("generated agent configs are stale: " + ", ".join(str(path) for path in stale))
    if args.check:
        print("generated agent configs are up to date")
    else:
        print("generated agent configs updated")


if __name__ == "__main__":
    main()
