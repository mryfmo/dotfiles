#!/usr/bin/env python3
"""Validate Codex, Claude Code, Hermes, MCP, plugin, and skill assets."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - CI installs PyYAML for this script.
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SECRET_PATTERN = re.compile(
    r"""(?ix)
    (
        ghp_[A-Za-z0-9_]{20,}
        | github_pat_[A-Za-z0-9_]{20,}
        | sk-[A-Za-z0-9_-]{20,}
        | api[_-]?key\s*[:=]\s*["'][^"']+["']
        | password\s*=\s*["'][^"']+["']
        | secret\s*[:=]\s*["'][^"']+["']
        | token\s*[:=]\s*["'][^"']+["']
    )
    """,
)
DEPRECATED_MCP_PACKAGES = {
    "@modelcontextprotocol/server-github": "Use the official ghcr.io/github/github-mcp-server container instead.",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        fail("PyYAML is required")
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        fail(f"{path} must be a mapping")
    return data


def render_template_text(path: Path) -> str:
    text = path.read_text()
    # This repository uses .chezmoiroot=home, so .chezmoi.sourceDir resolves
    # to the chezmoi source root that contains dot_agents/, dot_codex/, etc.
    text = text.replace("{{ .chezmoi.sourceDir }}", str(ROOT / "home"))
    text = re.sub(r"\{\{/\*.*?\*/\}\}", "", text, flags=re.DOTALL)
    return text


def read_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text()
    if not text.startswith("---\n"):
        fail(f"{path} is missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        fail(f"{path} has unterminated YAML frontmatter")
    if yaml is None:
        fail("PyYAML is required to validate skill frontmatter")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        fail(f"{path} frontmatter must be a mapping")
    return data


def shared_skill_names() -> set[str]:
    skills_root = ROOT / "home/dot_agents/skills"
    return {path.name for path in skills_root.iterdir() if path.is_dir()}


def validate_skills() -> None:
    skills_root = ROOT / "home/dot_agents/skills"
    if not skills_root.exists():
        fail(f"{skills_root} is missing")
    for skill_dir in sorted(p for p in skills_root.iterdir() if p.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            fail(f"{skill_dir} is missing SKILL.md")
        data = read_frontmatter(skill_file)
        for key in ("name", "description"):
            if not data.get(key):
                fail(f"{skill_file} is missing frontmatter key: {key}")
        if data["name"] != skill_dir.name:
            fail(f"{skill_file} name does not match directory name")
        openai_yaml = skill_dir / "agents/openai.yaml"
        if openai_yaml.exists():
            parsed = load_yaml(openai_yaml)
            if not isinstance(parsed, dict):
                fail(f"{openai_yaml} must be a mapping")


def validate_claude_skill_parity() -> None:
    expected = shared_skill_names()
    claude_root = ROOT / "home/dot_claude/skills"
    actual = {path.name for path in claude_root.iterdir() if path.is_dir()} if claude_root.exists() else set()
    if actual != expected:
        fail(f"Claude skill set differs from shared skills: missing={sorted(expected - actual)} extra={sorted(actual - expected)}")
    for name in sorted(expected):
        symlink = claude_root / name / "symlink_SKILL.md.tmpl"
        expected_target = f"{{{{ .chezmoi.sourceDir }}}}/dot_agents/skills/{name}/SKILL.md\n"
        if not symlink.exists() or symlink.read_text() != expected_target:
            fail(f"{symlink} must point at the shared skill tree")


def validate_codex_plugins() -> None:
    marketplace_path = ROOT / "home/dot_agents/plugins/marketplace.json"
    marketplace = json.loads(marketplace_path.read_text())
    if not marketplace.get("name"):
        fail(f"{marketplace_path} is missing name")
    plugins = marketplace.get("plugins", [])
    if not isinstance(plugins, list) or not plugins:
        fail(f"{marketplace_path} must define at least one plugin")
    for plugin in plugins:
        source = plugin.get("source", {})
        if source.get("source") == "local":
            path_value = source.get("path", "")
            if Path(path_value).is_absolute():
                fail(f"{marketplace_path} must not use absolute local plugin paths")
            manifest_path = ROOT / "home/dot_agents" / path_value.removeprefix("./") / ".codex-plugin/plugin.json"
            manifest = json.loads(manifest_path.read_text())
            for key in ("name", "version", "description"):
                if not manifest.get(key):
                    fail(f"{manifest_path} is missing {key}")
            skills_path = manifest.get("skills")
            if not skills_path:
                fail(f"{manifest_path} must expose shared skills")
            if Path(skills_path).is_absolute():
                fail(f"{manifest_path} must not use an absolute skills path")


def validate_claude_settings() -> None:
    settings_path = ROOT / "home/dot_claude/private_settings.json"
    settings = json.loads(settings_path.read_text())
    if settings.get("$schema") != "https://json.schemastore.org/claude-code-settings.json":
        fail(f"{settings_path} must declare the Claude Code settings schema")
    commands = json.dumps(settings.get("hooks", {}), ensure_ascii=False)
    legacy_type_checker = "uvx " + "my" + "py"
    if legacy_type_checker in commands:
        fail(f"{settings_path} still references the legacy type checker")
    if "format-edited-files.py" not in commands:
        fail(f"{settings_path} must use the robust Python post-edit hook")
    enabled_plugins = settings.get("enabledPlugins", {})
    if enabled_plugins:
        fail(f"{settings_path} must not enable Claude plugins that are not installed by this repository")


def validate_codex_config() -> dict[str, Any]:
    codex_path = ROOT / "home/dot_codex/private_config.toml.tmpl"
    text = render_template_text(codex_path)
    if not text.startswith("#:schema https://developers.openai.com/codex/config-schema.json"):
        fail(f"{codex_path} must declare the Codex config schema")
    data = tomllib.loads(text)
    if data.get("sandbox_mode") != "workspace-write":
        fail(f"{codex_path} should default to workspace-write sandbox")
    if data.get("sandbox_workspace_write", {}).get("network_access") is not False:
        fail(f"{codex_path} should keep sandbox command network access disabled")
    for name, server in data.get("mcp_servers", {}).items():
        if not isinstance(server, dict):
            fail(f"Codex MCP server {name} must be a table")
        if server.get("enabled", False) is not False:
            fail(f"Codex MCP server {name} should be disabled by default")
    return data


def validate_claude_mcp_config() -> dict[str, Any]:
    path = ROOT / "home/dot_claude/private_mcp.json.tmpl"
    data = json.loads(render_template_text(path))
    servers = data.get("mcpServers", {})
    if not isinstance(servers, dict) or not servers:
        fail(f"{path} must define mcpServers")
    for name, server in servers.items():
        if server.get("disabled") is not True:
            fail(f"Claude MCP server {name} should be disabled by default")
        if server.get("type") == "stdio" and not server.get("command"):
            fail(f"Claude stdio MCP server {name} must define command")
    return data


def validate_hermes_config_template() -> dict[str, Any]:
    hermes_path = ROOT / "home/dot_hermes/private_config.yaml.tmpl"
    data = yaml.safe_load(render_template_text(hermes_path))
    if not isinstance(data, dict):
        fail(f"{hermes_path} must render to a mapping")
    external_dirs = data.get("skills", {}).get("external_dirs", [])
    if "~/.agents/skills" not in external_dirs:
        fail(f"{hermes_path} must expose ~/.agents/skills as an external skill directory")
    for name, server in data.get("mcp_servers", {}).items():
        if server.get("enabled", False) is not False:
            fail(f"Hermes MCP server {name} should be disabled by default")
        if server.get("sampling", {}).get("enabled") is not False:
            fail(f"Hermes MCP server {name} should disable sampling by default")
    return data


def validate_agent_manifest() -> dict[str, Any]:
    manifest_path = ROOT / "home/dot_agents/agent-config.yaml"
    manifest = load_yaml(manifest_path)
    if manifest.get("schema_version") != 1:
        fail(f"{manifest_path} schema_version must be 1")
    targets = set(manifest.get("target_agents", []))
    if targets != {"codex", "claude", "hermes"}:
        fail(f"{manifest_path} must target exactly Codex, Claude Code, and Hermes")
    canonical_dir = manifest.get("skills", {}).get("canonical_dir")
    if canonical_dir != "~/.agents/skills":
        fail(f"{manifest_path} must keep ~/.agents/skills as the canonical skill directory")
    for name, server in manifest.get("mcp_servers", {}).items():
        if server.get("enabled", False) is not False:
            fail(f"MCP server {name} must be disabled by default in the shared manifest")
        agents = server.get("agents", {})
        if set(agent for agent, enabled in agents.items() if enabled) != targets:
            fail(f"MCP server {name} must be exposed to every target agent")
        transport = server.get("transport")
        if transport == "stdio":
            if not server.get("command"):
                fail(f"stdio MCP server {name} must define command")
        elif transport == "http":
            if not server.get("url"):
                fail(f"http MCP server {name} must define url")
        else:
            fail(f"MCP server {name} has unsupported transport: {transport}")
        if server.get("sampling", False) is not False:
            fail(f"MCP server {name} must disable sampling by default")
        serialized = json.dumps(server, ensure_ascii=False)
        for package, replacement in DEPRECATED_MCP_PACKAGES.items():
            if package in serialized:
                fail(f"MCP server {name} uses deprecated {package}. {replacement}")
    return manifest


def validate_mcp_parity(codex: dict[str, Any], claude: dict[str, Any], hermes: dict[str, Any], manifest: dict[str, Any]) -> None:
    manifest_names = set(manifest.get("mcp_servers", {}))
    codex_names = set(codex.get("mcp_servers", {}))
    claude_names = set(claude.get("mcpServers", {}))
    hermes_names = set(hermes.get("mcp_servers", {}))
    if not (manifest_names == codex_names == claude_names == hermes_names):
        fail(
            "MCP server names differ: "
            f"manifest={sorted(manifest_names)} codex={sorted(codex_names)} "
            f"claude={sorted(claude_names)} hermes={sorted(hermes_names)}"
        )


def validate_generated_agent_configs() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/generate-agent-configs.py"), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        fail(result.stdout.strip() or "generated agent configs are stale")


def validate_no_removed_claude_skill() -> None:
    removed_skill = "high-impact" + "-journal-publishing"
    matches = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "site", "__pycache__"} for part in path.parts):
            continue
        if removed_skill in path.read_text(errors="ignore"):
            matches.append(path)
    if matches:
        fail("removed Claude skill references remain: " + ", ".join(str(p.relative_to(ROOT)) for p in matches[:10]))


def validate_no_obvious_secrets() -> None:
    checked_suffixes = {".json", ".toml", ".yaml", ".yml", ".md", ".tmpl", ".py", ".sh"}
    allowed_secret_placeholders = {
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "FIGMA_OAUTH_TOKEN",
    }
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in checked_suffixes:
            continue
        if any(part in {".git", "docs", "site", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(errors="ignore")
        sanitized = text
        for placeholder in allowed_secret_placeholders:
            sanitized = sanitized.replace(placeholder, "")
        if SECRET_PATTERN.search(sanitized):
            fail(f"possible committed secret in {path.relative_to(ROOT)}")


def main() -> None:
    manifest = validate_agent_manifest()
    validate_generated_agent_configs()
    validate_skills()
    validate_claude_skill_parity()
    validate_claude_settings()
    validate_codex_plugins()
    codex = validate_codex_config()
    claude = validate_claude_mcp_config()
    hermes = validate_hermes_config_template()
    validate_mcp_parity(codex, claude, hermes, manifest)
    validate_no_removed_claude_skill()
    validate_no_obvious_secrets()
    print("agent asset validation ok")


if __name__ == "__main__":
    main()
