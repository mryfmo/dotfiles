#!/usr/bin/env python3
"""Generate agent-native configuration from the shared AI-agent manifest."""

from __future__ import annotations

import argparse
import json
import re
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
        return "{ " + ", ".join(f"{quote_toml_key(str(key))} = {quote_toml(item)}" for key, item in value.items()) + " }"
    fail(f"unsupported TOML value: {value!r}")


def quote_toml_key(key: str) -> str:
    if re.match(r"^[A-Za-z0-9_-]+$", key):
        return key
    return json.dumps(key, ensure_ascii=False)


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
        "model_reasoning_effort",
        "model_reasoning_summary",
        "model_verbosity",
        "personality",
        "approval_policy",
        "sandbox_mode",
        "web_search",
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
        for key, value in marketplace_config.items():
            lines.append(f"{quote_toml_key(str(key))} = {quote_toml(value)}")
    hooks = codex.get("hooks", {})
    if hooks.get("ccgate_permission_request_hook"):
        lines.extend(
            [
                "",
                "[[hooks.PermissionRequest]]",
                'matcher = ""',
                "",
                "[[hooks.PermissionRequest.hooks]]",
                'type = "command"',
                f"command = {quote_toml(hooks['ccgate_permission_request_hook'])}",
                'statusMessage = "ccgate evaluating request"',
            ]
        )
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
    settings: dict[str, Any] = {
        "$schema": claude["schema"],
        "model": claude["model"],
        "effortLevel": claude["effortLevel"],
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
            "PermissionRequest": [
                {
                    "matcher": "",
                    "hooks": [
                        {
                            "type": "command",
                            "command": hooks["ccgate_permission_request_hook"],
                        }
                    ],
                }
            ],
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


def render_ccgate_config(target: str) -> str:
    if target == "codex":
        schema = "https://raw.githubusercontent.com/tak848/ccgate/main/schemas/codex.schema.json"
        lines = [
            "{",
            f"  // {GENERATED_HEADER}",
            f"  ['$schema']: {json.dumps(schema)},",
            "  provider: {",
            "    name: 'anthropic',",
            "    model: 'claude-haiku-4-5',",
            "  },",
            "  fallthrough_strategy: 'ask',",
            "  append_environment: [",
            "    'ccgate codex is an LLM-backed PermissionRequest gate. Its purpose is to automate clear permission prompts while preserving safety, human review, and useful feedback to the agent.',",
            "    'The provider model is the ccgate classifier model, not the active Codex task model. Keep permission classification on a small structured-output model and do not spend premium task models on gating.',",
            "    'Codex HookInput.model is available. Use it as proportionality context, not as a deterministic block. Premium models such as gpt-5.5, gpt-5, and reasoning-tier models are appropriate for architecture, ambiguous debugging, multi-file design, security-sensitive review, and high-stakes decisions.',",
            "    'Do not deny necessary read-only inspection, search, or small setup commands solely because a premium model is active. Those operations are often part of a larger task that legitimately needs the active model.',",
            "    'Prefer fallthrough for ambiguous model-proportionality decisions in interactive TUI sessions. Use metrics later to tune repeated fallthrough or deny patterns.',",
            "  ],",
            "  append_allow: [",
            "    'Allow focused read-only inspection, search, status, diff, and version checks when they support the current task and do not expose secrets, escalate privilege, modify files, or access the network.',",
            "  ],",
            "  append_deny: [",
            "    'Deny only when the requested action is clearly unsafe, overbroad, destructive, privileged, network-executing without explicit need, or a repeated trivial operation under a premium active model that is unrelated to any complex user task. deny_message: Narrow the operation or switch to a smaller model before retrying; ccgate should guide model proportionality without blocking necessary task inspection.',",
            "  ],",
            "}",
            "",
        ]
    elif target == "claude":
        schema = "https://raw.githubusercontent.com/tak848/ccgate/main/schemas/claude.schema.json"
        lines = [
            "{",
            f"  // {GENERATED_HEADER}",
            f"  ['$schema']: {json.dumps(schema)},",
            "  provider: {",
            "    name: 'anthropic',",
            "    model: 'claude-haiku-4-5',",
            "  },",
            "  fallthrough_strategy: 'ask',",
            "  append_environment: [",
            "    'ccgate claude is an LLM-backed PermissionRequest gate. Its purpose is to automate clear permission prompts while preserving safety, human review, and useful feedback to the agent.',",
            "    'The provider model is the ccgate classifier model, not the active Claude Code task model. Keep permission classification on a small structured-output model and do not spend premium task models on gating.',",
            "    'Claude Code PermissionRequest input does not expose the active task model. Model governance for Claude Code must come from settings and agent rules; ccgate can only judge the requested tool action and return allow, deny, or fallthrough.',",
            "    'Prefer fallthrough for ambiguous model-proportionality decisions in interactive TUI sessions. Use metrics later to tune repeated fallthrough or deny patterns.',",
            "  ],",
            "  append_allow: [",
            "    'Allow focused read-only inspection, search, status, diff, and version checks when they support the current task and do not expose secrets, escalate privilege, modify files, or access the network.',",
            "  ],",
            "  append_deny: [",
            "    'Deny only when the requested action is clearly unsafe, overbroad, destructive, privileged, network-executing without explicit need, or too broad to be a permission-safe unit. deny_message: Narrow the operation and choose the smallest Claude Code model adequate for the task before retrying.',",
            "  ],",
            "}",
            "",
        ]
    else:
        fail(f"unsupported ccgate target: {target}")
    return "\n".join(lines)


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


def expected_outputs(manifest: dict[str, Any]) -> dict[Path, str]:
    outputs = {
        ROOT / manifest["codex"]["config_path"]: render_codex(manifest),
        ROOT / manifest["codex"]["ccgate_config_path"]: render_ccgate_config("codex"),
        ROOT / manifest["claude"]["settings_path"]: render_claude_settings(manifest),
        ROOT / manifest["claude"]["mcp_config_path"]: render_claude_mcp(manifest),
        ROOT / manifest["claude"]["ccgate_config_path"]: render_ccgate_config("claude"),
        ROOT / manifest["plugins"]["marketplace_path"]: render_marketplace(manifest),
    }
    for plugin in manifest["plugins"].get("codex_plugins", []):
        if not plugin.get("managed_manifest", True):
            continue
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
