#!/usr/bin/env python3
"""Validate Codex, Claude Code, MCP, plugin, and skill assets."""

from __future__ import annotations

import configparser
import hashlib
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
# Regenerate with: shasum -a 256 home/dot_pi/agent/extensions/permgate.ts
PI_PERMGATE_EXTENSION_SHA256 = "e3591dcba2be96dad59174de4649fca702213dadd0d8217c4b2d9535445c43d6"
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
REQUIRED_AGMSG_WRITABLE_ROOTS = {
    "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db",
    "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams",
    "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run",
}
SYNC_TIMEOUT_BUDGET_S = 30  # PLAN H3 pins the per-source, per-event synchronous budget.
HOOK_COMPOSITION_SOURCES = {
    "claude": (Path("home/.chezmoitemplates/claude-settings-managed.json"), "json"),
    "codex": (Path("home/.chezmoitemplates/codex-config-managed.toml"), "toml"),
    "compactiondb": (Path("vendor/compactiondb/.claude/settings.fragment.json"), "json"),
}
# PLAN H3 pins the current relative SessionStart order across managed sources.
SESSIONSTART_EXPECTED_COMMAND_SUBSTRINGS = {
    "claude": ("herdr-agent-state.sh",),
    "codex": (),
    "compactiondb": ("contextdb_hook.py", "contextdb_recover.py"),
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


def hook_command_string(hook: dict[str, Any]) -> str:
    parts = [str(hook.get("command") or "")]
    args = hook.get("args") or []
    if isinstance(args, list):
        parts.extend(str(arg) for arg in args)
    return " ".join(part for part in parts if part)


def managed_hook_inventory() -> dict[tuple[str, str], list[dict[str, Any]]]:
    inventory: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for source, (relative_path, file_type) in HOOK_COMPOSITION_SOURCES.items():
        text = render_template_text(ROOT / relative_path)
        data = tomllib.loads(text) if file_type == "toml" else json.loads(text)
        for event, groups in data.get("hooks", {}).items():
            if not isinstance(groups, list):
                continue
            entries = inventory.setdefault((source, event), [])
            for group in groups:
                for hook in group.get("hooks", []):
                    if hook.get("type") == "command":
                        entries.append(hook)
    return inventory


def validate_hook_composition() -> None:
    inventory = managed_hook_inventory()
    findings: list[str] = []
    for (source, event), hooks in inventory.items():
        seen: set[str] = set()
        for hook in hooks:
            command = hook_command_string(hook)
            if command in seen:
                findings.append(f"duplicate-command source={source} event={event} command={command!r}")
            seen.add(command)

        commands = [hook_command_string(hook) for hook in hooks]
        if event == "PermissionRequest" and any("permgate" in command for command in commands):
            if not commands or "permgate" not in commands[0]:
                findings.append(f"permgate-first source={source} event={event} first={commands[0]!r}")

        sync_timeout = sum(hook.get("timeout", 0) for hook in hooks if not hook.get("async", False))
        if sync_timeout > SYNC_TIMEOUT_BUDGET_S:
            findings.append(
                f"sync-timeout-budget source={source} event={event} "
                f"total={sync_timeout}s limit={SYNC_TIMEOUT_BUDGET_S}s"
            )

    for source, expected in SESSIONSTART_EXPECTED_COMMAND_SUBSTRINGS.items():
        commands = [hook_command_string(hook) for hook in inventory.get((source, "SessionStart"), [])]
        position = 0
        for substring in expected:
            match = next((index for index in range(position, len(commands)) if substring in commands[index]), None)
            if match is None:
                findings.append(
                    f"sessionstart-order source={source} expected={list(expected)!r} actual={commands!r}"
                )
                break
            position = match + 1

    if findings:
        fail("hook composition violations:\n- " + "\n- ".join(findings))


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


def validate_claude_command_parity() -> None:
    symlink = ROOT / "home/dot_claude/commands/symlink_agmsg.md.tmpl"
    expected_target = "{{ .chezmoi.sourceDir }}/dot_agents/skills/agmsg/templates/cmd.claude-code.md\n"
    if not symlink.exists() or symlink.read_text() != expected_target:
        fail(f"{symlink} must point at the shared agmsg command template")
    target = ROOT / "home" / expected_target.strip().removeprefix("{{ .chezmoi.sourceDir }}/")
    if not target.is_file():
        fail(f"{symlink} points at a missing template: {target}")
    duplicate = ROOT / "home/dot_claude/commands/agmsg.md"
    if duplicate.exists():
        fail(f"{duplicate} duplicates the shared agmsg command template; keep the symlink only")


HARD_CODED_HOME_RE = re.compile(r"/(?:Users|home)/[^/\s'\"]+/")


def validate_manifest_home_paths() -> None:
    # Scanned as text rather than parsed YAML so the check still runs under
    # `make unit-test`, which does not install PyYAML.
    manifest_path = ROOT / "home/dot_agents/agent-config.yaml"
    top_level = ""
    projects_indent: int | None = None
    for number, line in enumerate(manifest_path.read_text().splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0:
            top_level = stripped.split(":", 1)[0]
        if projects_indent is not None and indent <= projects_indent:
            projects_indent = None
        if projects_indent is None and top_level == "codex" and stripped.startswith("projects:"):
            # Only codex.projects is runtime-owned state keyed by absolute project
            # path; it is preserved by home/dot_codex/modify_private_config.toml.
            projects_indent = indent
            continue
        if projects_indent is not None:
            continue
        if HARD_CODED_HOME_RE.search(line):
            fail(f"{manifest_path}:{number} must not hard-code a home directory; use {{{{ .chezmoi.homeDir }}}} so the rendered value stays byte-identical to what the agent runtimes write")


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
            if plugin.get("name") == "crit" and path_value == "./.codex/plugins/crit":
                # Crit is installed dynamically and does not ship a static plugin manifest.
                continue
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


def validate_exact_keys(actual: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    actual_keys = set(actual)
    expected_keys = set(expected)
    if actual_keys != expected_keys:
        fail(
            f"{label} keys must match the shared manifest: "
            f"missing={sorted(expected_keys - actual_keys)} extra={sorted(actual_keys - expected_keys)}"
        )


def validate_agmsg_script_modes() -> None:
    scripts_root = ROOT / "home/dot_agents/skills/agmsg/scripts"
    entrypoint_dirs = [scripts_root, scripts_root / "release"]
    for entrypoint_dir in entrypoint_dirs:
        for path in sorted(entrypoint_dir.glob("*.sh")):
            if not path.name.startswith("executable_"):
                fail(f"{path.relative_to(ROOT)} must use chezmoi executable_ prefix")
            if path.stat().st_mode & 0o111 == 0:
                fail(f"{path.relative_to(ROOT)} must stay executable for direct invocation")


def validate_codex_agmsg_writable_roots(sandbox_workspace_write: dict[str, Any], label: str) -> None:
    writable_roots = sandbox_workspace_write.get("writable_roots", [])
    missing = REQUIRED_AGMSG_WRITABLE_ROOTS - set(writable_roots)
    if missing:
        fail(f"{label} must include agmsg writable roots: missing={sorted(missing)}")


def validate_claude_settings(manifest: dict[str, Any]) -> None:
    settings_path = ROOT / "home/.chezmoitemplates/claude-settings-managed.json"
    settings = json.loads(render_template_text(settings_path))
    if settings.get("$schema") != "https://json.schemastore.org/claude-code-settings.json":
        fail(f"{settings_path} must declare the Claude Code settings schema")
    interactive = manifest.get("model_profiles", {}).get(manifest.get("interactive_profile"), {}).get("claude", {})
    if settings.get("model") != interactive.get("model"):
        fail(f"{settings_path} must render the interactive profile model")
    if settings.get("effortLevel") != interactive.get("effort"):
        fail(f"{settings_path} must render the interactive profile effort")
    if "[1m]" in str(settings.get("model")):
        fail(f"{settings_path} must not use the redundant [1m] suffix")
    commands = json.dumps(settings.get("hooks", {}), ensure_ascii=False)
    legacy_type_checker = "uvx " + "my" + "py"
    if legacy_type_checker in commands:
        fail(f"{settings_path} still references the legacy type checker")
    if "format-edited-files.py" not in commands:
        fail(f"{settings_path} must use the robust Python post-edit hook")
    enabled_plugins = settings.get("enabledPlugins", {})
    if enabled_plugins:
        fail(f"{settings_path} must not enable Claude plugins that are not installed by this repository")
    crit_rule = ROOT / "home/dot_config/claude/rules/crit-review.md"
    if not crit_rule.exists() or "/crit" not in crit_rule.read_text():
        fail("Claude Code Crit review rule must require /crit")


def validate_codex_config(manifest: dict[str, Any]) -> dict[str, Any]:
    codex_path = ROOT / manifest.get("codex", {}).get("config_path", "home/.chezmoitemplates/codex-config-managed.toml")
    text = render_template_text(codex_path)
    if not text.startswith("#:schema https://developers.openai.com/codex/config-schema.json"):
        fail(f"{codex_path} must declare the Codex config schema")
    data = tomllib.loads(text)
    manifest_codex = manifest.get("codex", {})
    interactive = manifest.get("model_profiles", {}).get(manifest.get("interactive_profile"), {}).get("codex", {})
    if data.get("model") != interactive.get("model"):
        fail(f"{codex_path} must render the interactive profile model")
    if data.get("model_reasoning_effort") != interactive.get("model_reasoning_effort"):
        fail(f"{codex_path} must render the interactive profile reasoning effort")
    for key in ("model_reasoning_summary", "model_verbosity", "personality"):
        if manifest_codex.get(key) != data.get(key):
            fail(f"{codex_path} must render codex.{key} from the shared manifest")
    if data.get("sandbox_mode") != "workspace-write":
        fail(f"{codex_path} should default to workspace-write sandbox")
    if data.get("sandbox_workspace_write", {}).get("network_access") is not False:
        fail(f"{codex_path} should keep sandbox command network access disabled")
    validate_codex_agmsg_writable_roots(manifest_codex.get("sandbox_workspace_write", {}), "codex.sandbox_workspace_write")
    if data.get("sandbox_workspace_write") != manifest_codex.get("sandbox_workspace_write"):
        fail(f"{codex_path} must render codex.sandbox_workspace_write from the shared manifest")
    features = data.get("features", {})
    for feature in ("plugins", "hooks", "plugin_hooks"):
        if features.get(feature) is not True:
            fail(f"{codex_path} must enable Codex feature {feature} for Crit plugin hooks")
    if data.get("shell_environment_policy") != manifest_codex.get("shell_environment_policy"):
        fail(f"{codex_path} must render codex.shell_environment_policy from the shared manifest")
    shell_path = data.get("shell_environment_policy", {}).get("set", {}).get("PATH", "")
    if "/Users/mryfmo/" in shell_path:
        fail(f"{codex_path} must not hard-code a macOS home directory in shell_environment_policy.set.PATH")
    if "{{ .chezmoi.homeDir }}" not in shell_path:
        fail(f"{codex_path} must derive shell_environment_policy.set.PATH from the target chezmoi homeDir")
    for key, value in manifest_codex.get("tui", {}).items():
        if data.get("tui", {}).get(key) != value:
            fail(f"{codex_path} must render codex.tui.{key} from the shared manifest")
    validate_exact_keys(data.get("tui", {}), manifest_codex.get("tui", {}), f"{codex_path} codex.tui")
    for plugin_id, plugin_config in manifest_codex.get("plugins", {}).items():
        if data.get("plugins", {}).get(plugin_id) != plugin_config:
            fail(f"{codex_path} must render Codex plugin {plugin_id}")
    validate_exact_keys(
        data.get("plugins", {}),
        manifest_codex.get("plugins", {}),
        f"{codex_path} Codex plugins",
    )
    for marketplace_name, marketplace_config in manifest_codex.get("marketplaces", {}).items():
        if data.get("marketplaces", {}).get(marketplace_name) != marketplace_config:
            fail(f"{codex_path} must render Codex marketplace {marketplace_name}")
    validate_exact_keys(
        data.get("marketplaces", {}),
        manifest_codex.get("marketplaces", {}),
        f"{codex_path} Codex marketplaces",
    )
    manifest_hook_state = manifest_codex.get("hooks", {}).get("state", {})
    if data.get("hooks", {}).get("state", {}) != manifest_hook_state:
        fail(f"{codex_path} must render Codex hook trust state from the shared manifest")
    for project_path, project_config in manifest_codex.get("projects", {}).items():
        if data.get("projects", {}).get(project_path) != project_config:
            fail(f"{codex_path} must render Codex project trust for {project_path}")
    validate_exact_keys(
        data.get("projects", {}),
        manifest_codex.get("projects", {}),
        f"{codex_path} Codex projects",
    )
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


def validate_agent_manifest() -> dict[str, Any]:
    manifest_path = ROOT / "home/dot_agents/agent-config.yaml"
    manifest = load_yaml(manifest_path)
    if manifest.get("schema_version") != 1:
        fail(f"{manifest_path} schema_version must be 1")
    targets = set(manifest.get("target_agents", []))
    if targets != {"codex", "claude"}:
        fail(f"{manifest_path} must target exactly Codex and Claude Code")
    canonical_dir = manifest.get("skills", {}).get("canonical_dir")
    if canonical_dir != "~/.agents/skills":
        fail(f"{manifest_path} must keep ~/.agents/skills as the canonical skill directory")
    codex_plugins = manifest.get("codex", {}).get("plugins", {})
    if codex_plugins.get("crit@mryfmo-personal-plugins", {}).get("enabled") is not True:
        fail(f"{manifest_path} must enable the Crit Codex plugin")
    claude = manifest.get("claude", {})
    profiles = manifest.get("model_profiles", {})
    required_profiles = {"express", "standard", "review", "deep", "security"}
    if set(profiles) != required_profiles:
        fail(
            f"{manifest_path} must define exactly model profiles "
            f"{sorted(required_profiles)}"
        )
    if profiles["security"].get("codex", {}).get("model") != "gpt-daybreak-blue-latest":
        fail(
            f"{manifest_path} security Codex profile must use "
            "gpt-daybreak-blue-latest"
        )
    if manifest.get("interactive_profile") not in profiles:
        fail(f"{manifest_path} interactive_profile must name a defined model profile")
    for name, profile in profiles.items():
        for agent, keys in (("claude", ("model", "effort")), ("codex", ("model", "model_reasoning_effort"))):
            for key in keys:
                if not profile.get(agent, {}).get(key):
                    fail(f"{manifest_path} model profile {name}.{agent}.{key} is required")
    if claude.get("model") or claude.get("effortLevel") or manifest.get("codex", {}).get("model"):
        fail(f"{manifest_path} must keep model settings in model_profiles only")
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


def validate_mcp_parity(codex: dict[str, Any], claude: dict[str, Any], manifest: dict[str, Any]) -> None:
    manifest_names = set(manifest.get("mcp_servers", {}))
    codex_names = set(codex.get("mcp_servers", {}))
    claude_names = set(claude.get("mcpServers", {}))
    if not (manifest_names == codex_names == claude_names):
        fail(
            "MCP server names differ: "
            f"manifest={sorted(manifest_names)} codex={sorted(codex_names)} "
            f"claude={sorted(claude_names)}"
        )


def validate_codex_modify_script() -> None:
    path = ROOT / "home/dot_codex/modify_private_config.toml"
    if not path.exists():
        fail(f"{path} is missing")
    if path.stat().st_mode & 0o111 == 0:
        fail(f"{path} must be executable")
    text = path.read_text()
    for token in ("RUNTIME_PREFIXES", "hooks.state", "marketplaces", "tui.model_availability_nux", "projects"):
        if token not in text:
            fail(f"{path} must preserve Codex runtime-owned table token {token!r}")


def validate_codex_profile_modify_scripts(manifest: dict[str, Any]) -> None:
    for name, profile in manifest.get("model_profiles", {}).items():
        path = ROOT / "home/dot_codex" / f"modify_{name}.config.toml"
        if not path.exists():
            fail(f"{path} is missing for model profile {name}")
        if path.stat().st_mode & 0o111 == 0:
            fail(f"{path} must be executable")
        result = subprocess.run(
            [str(path)],
            input="",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            fail(f"{path} must run successfully: {result.stderr.strip()}")
        profile_data = tomllib.loads(result.stdout)
        if profile_data.get("model") != profile.get("codex", {}).get("model"):
            fail(f"{path} must render the {name} profile model")
        if profile_data.get("model_reasoning_effort") != profile.get("codex", {}).get("model_reasoning_effort"):
            fail(f"{path} must render the {name} profile reasoning effort")
        if profile_data.get("features", {}).get("hooks") is not True:
            fail(f"{path} must enable hooks for the {name} profile")
        if "state" not in profile_data.get("hooks", {}):
            fail(f"{path} must preserve hook trust state for the {name} profile")


def validate_crit_install_assets() -> None:
    updater = (ROOT / "scripts/update-agent-assets.sh").read_text()
    for token in (
        "brew install crit",
        "crit@crit",
        "claude plugin enable",
        "claude_crit_plugin_is_enabled",
        "if claude_crit_plugin_is_enabled; then",
        "crit install codex-plugin --force",
        "tomasz-tomczyk/crit",
    ):
        if token not in updater:
            fail(f"scripts/update-agent-assets.sh must manage Crit asset token {token!r}")
    codex_agents = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
    for token in ("$crit", "Crit plugin", "CRIT_PLAN_REVIEW=off", "TUI", "http://localhost"):
        if token not in codex_agents:
            fail(f"home/dot_config/codex/AGENTS.md must document Codex Crit rule token {token!r}")
    guard_path = ROOT / "scripts/require-crit-review.py"
    if not guard_path.exists():
        fail("scripts/require-crit-review.py must enforce meaningful review triggers")
    guard_text = guard_path.read_text()
    for token in (
        "CRIT_REVIEWED",
        "AGENT_REVIEWED",
        "REVIEW_EVIDENCE",
        "review_surface",
        "reviewer",
        "review_outcome",
        "SELF_REVIEWER_TOKENS",
        "CRIT_REVIEW=off",
        "agent lifecycle",
        "broad diff",
        "Crit data",
        "review_source",
    ):
        if token not in guard_text:
            fail(f"scripts/require-crit-review.py must contain Crit guard token {token!r}")
    readme = (ROOT / "README.md").read_text()
    for token in ("scripts/require-crit-review.py", "AGENT_REVIEWED=1", "REVIEW_EVIDENCE", "review_source", "crit-data", "CRIT_REVIEW=off"):
        if token not in readme:
            fail(f"README.md must document Crit guard token {token!r}")


def validate_ponytail_assets(manifest: dict[str, Any], codex: dict[str, Any]) -> None:
    updater = (ROOT / "scripts/update-agent-assets.sh").read_text()
    for token in (
        "DietrichGebert/ponytail",
        "ponytail@ponytail",
        "CODEX_PONYTAIL_MARKETPLACE_SOURCE",
        "codex_marketplace_has_source",
        "codex plugin marketplace upgrade \"${CODEX_PONYTAIL_MARKETPLACE_NAME}\"",
        "update_claude_ponytail",
        "update_codex_ponytail",
        "PONYTAIL_DEFAULT_MODE",
    ):
        if token not in updater:
            fail(f"scripts/update-agent-assets.sh must manage Ponytail asset token {token!r}")

    manifest_plugins = manifest.get("codex", {}).get("plugins", {})
    if manifest_plugins.get("ponytail@ponytail", {}).get("enabled") is not True:
        fail("home/dot_agents/agent-config.yaml must enable the Ponytail Codex plugin")
    if codex.get("plugins", {}).get("ponytail@ponytail", {}).get("enabled") is not True:
        fail("home/.chezmoitemplates/codex-config-managed.toml must render the Ponytail Codex plugin")
    if codex.get("marketplaces", {}).get("ponytail", {}).get("source") != "https://github.com/DietrichGebert/ponytail.git":
        fail("home/.chezmoitemplates/codex-config-managed.toml must render the Ponytail Codex marketplace source")
    hook_state = codex.get("hooks", {}).get("state", {})
    for key in (
        "ponytail@ponytail:hooks/claude-codex-hooks.json:session_start:0:0",
        "ponytail@ponytail:hooks/claude-codex-hooks.json:user_prompt_submit:0:0",
        "ponytail@ponytail:hooks/claude-codex-hooks.json:subagent_start:0:0",
    ):
        if not hook_state.get(key, {}).get("trusted_hash", "").startswith("sha256:"):
            fail(f"home/.chezmoitemplates/codex-config-managed.toml must render trusted Ponytail hook state for {key}")

    codex_agents = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
    for token in ("Ponytail", "/hooks", "ponytail@ponytail", "YAGNI", "stdlib"):
        if token not in codex_agents:
            fail(f"home/dot_config/codex/AGENTS.md must document Ponytail token {token!r}")

    claude_rule = ROOT / "home/dot_config/claude/rules/ponytail.md"
    if not claude_rule.exists():
        fail("Claude Code Ponytail rule is missing")
    claude_rule_text = claude_rule.read_text()
    for token in ("Ponytail", "ponytail@ponytail", "YAGNI", "standard library", "native platform"):
        if token not in claude_rule_text:
            fail(f"{claude_rule} must document Ponytail token {token!r}")

    claude_symlink = ROOT / "home/dot_claude/rules/symlink_ponytail.md.tmpl"
    expected_target = "{{ .chezmoi.sourceDir }}/dot_config/claude/rules/ponytail.md\n"
    if not claude_symlink.exists() or claude_symlink.read_text() != expected_target:
        fail(f"{claude_symlink} must point at the managed Ponytail Claude rule")

    readme = (ROOT / "README.md").read_text()
    for token in ("Ponytail", "DietrichGebert/ponytail", "ponytail@ponytail", "review and trust"):
        if token not in readme:
            fail(f"README.md must document Ponytail lifecycle token {token!r}")


def validate_understand_anything_assets() -> None:
    updater = (ROOT / "scripts/update-agent-assets.sh").read_text()
    for token in (
        "Egonex-AI/Understand-Anything",
        "understand-anything@understand-anything",
        "CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL",
        "CODEX_UNDERSTAND_ANYTHING_INSTALLER_SHA256",
        'claude plugin enable "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}"',
        "if claude_understand_anything_plugin_is_enabled; then",
        "update_claude_understand_anything",
        "update_codex_understand_anything",
        "provision_codex_understand_anything_runtime",
        "packages/core/dist",
        "packages/core/node_modules",
        "except ValueError:",
        '[ -d "${release_root}/${source}" ] || continue',
        "Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact",
    ):
        if token not in updater:
            fail(f"scripts/update-agent-assets.sh must manage Understand-Anything asset token {token!r}")

    codex_agents = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
    for token in ("Understand-Anything", "$understand", "knowledge-graph.json", ".ua/intermediate/", ".ua/diff-overlay.json"):
        if token not in codex_agents:
            fail(f"home/dot_config/codex/AGENTS.md must document Understand-Anything token {token!r}")

    claude_rule = ROOT / "home/dot_config/claude/rules/understand-anything.md"
    if not claude_rule.exists():
        fail("Claude Code Understand-Anything rule is missing")
    claude_rule_text = claude_rule.read_text()
    for token in (
        "Understand-Anything",
        "understand-anything@understand-anything",
        "knowledge-graph.json",
        "/understand",
        ".ua/intermediate/",
        ".ua/diff-overlay.json",
    ):
        if token not in claude_rule_text:
            fail(f"{claude_rule} must document Understand-Anything token {token!r}")

    claude_symlink = ROOT / "home/dot_claude/rules/symlink_understand-anything.md.tmpl"
    expected_target = "{{ .chezmoi.sourceDir }}/dot_config/claude/rules/understand-anything.md\n"
    if not claude_symlink.exists() or claude_symlink.read_text() != expected_target:
        fail(f"{claude_symlink} must point at the managed Understand-Anything Claude rule")

    readme = (ROOT / "README.md").read_text()
    for token in (
        "Understand-Anything",
        "Egonex-AI/Understand-Anything",
        "understand-anything@understand-anything",
        "version-matched Claude release artifact",
    ):
        if token not in readme:
            fail(f"README.md must document Understand-Anything lifecycle token {token!r}")


def validate_pi_assets() -> None:
    pi_root = ROOT / "home/dot_pi"
    if pi_root.exists():
        settings_path = pi_root / "agent/settings.json"
        if not settings_path.is_file():
            fail(f"{settings_path} is missing")
        try:
            settings = json.loads(settings_path.read_text())
        except json.JSONDecodeError:
            fail(f"{settings_path} must contain valid JSON")
        if not isinstance(settings, dict) or settings.get("defaultProjectTrust") != "never":
            fail(f'{settings_path} must set defaultProjectTrust to "never"')

        extensions_path = pi_root / "agent/extensions"
        if not extensions_path.is_dir():
            fail(f"{extensions_path} is missing")
        permgate_extension = extensions_path / "permgate.ts"
        if not permgate_extension.is_file():
            fail(f"{permgate_extension} is missing")
        extension_hash = hashlib.sha256(permgate_extension.read_bytes()).hexdigest()
        if extension_hash != PI_PERMGATE_EXTENSION_SHA256:
            fail(f"{permgate_extension} content hash does not match the managed asset")

    mise_path = ROOT / "home/dot_mise/config.toml"
    try:
        mise = tomllib.loads(mise_path.read_text())
    except (FileNotFoundError, tomllib.TOMLDecodeError):
        fail(f"{mise_path} must contain valid TOML")
    pi_version = mise.get("tools", {}).get("npm:@earendil-works/pi-coding-agent")
    if pi_version is not None and pi_version != "0.84.1":
        fail(f"{mise_path} must pin npm:@earendil-works/pi-coding-agent to 0.84.1")


def validate_model_profile_assets(manifest: dict[str, Any]) -> None:
    codex_path = ROOT / "home/.chezmoitemplates/codex-config-managed.toml"
    codex_text = render_template_text(codex_path)
    if "hooks.PermissionRequest" not in codex_text or "permgate codex" not in codex_text:
        fail(f"{codex_path} must wire the permgate PermissionRequest hook")
    if "ccgate" in codex_text:
        fail(f"{codex_path} must not wire ccgate")

    claude_settings_path = ROOT / "home/.chezmoitemplates/claude-settings-managed.json"
    claude_settings = json.loads(render_template_text(claude_settings_path))
    claude_hooks = json.dumps(claude_settings.get("hooks", {}), ensure_ascii=False)
    if "PermissionRequest" not in claude_hooks or "permgate claude" not in claude_hooks:
        fail(f"{claude_settings_path} must wire the permgate PermissionRequest hook")
    if "ccgate" in claude_hooks:
        fail(f"{claude_settings_path} must not wire ccgate")

    policy_path = ROOT / "home/dot_agents/permgate-policy.yaml"
    permgate_path = ROOT / "home/dot_local/bin/common/executable_permgate"
    if not policy_path.exists() or not permgate_path.exists():
        fail("permgate policy and executable must exist")
    policy = json.loads(policy_path.read_text())
    providers = policy.get("providers", {})
    if set(providers) != {"claude", "codex"}:
        fail("permgate must define claude and codex providers")
    if any(provider.get("llm_enabled") is not False for provider in providers.values()):
        fail("permgate providers must ship in shadow mode")
    if not providers.get("claude", {}).get("model", "").startswith(
        "claude-haiku-4-5-20"
    ):
        fail("permgate Claude provider must pin a dated Haiku model")
    if providers.get("codex", {}).get("model") != "gpt-5.6-luna":
        fail("permgate Codex provider must use the express Codex model")
    if any(
        not 0 < provider.get("timeout_seconds", 0) <= 8
        for provider in providers.values()
    ):
        fail("permgate provider timeouts must leave hook headroom")
    if set(policy.get("classifier_actions", {})) != set(policy.get("categories", [])):
        fail("permgate must bound every classifier category to explicit actions")
    permgate_text = permgate_path.read_text()
    for token in (
        "--no-cache",
        "PERMGATE_INNER",
        "PERMGATE_CODEX_COMMAND",
        "--safe-mode",
        '--tools',
        "--disable-slash-commands",
        "--ignore-user-config",
        "--ignore-rules",
        "classification_subject",
        "decisions.jsonl",
    ):
        if token not in permgate_text:
            fail(f"{permgate_path} must contain {token!r}")

    for stale in (ROOT / "home/dot_codex/ccgate.jsonnet", ROOT / "home/dot_claude/ccgate.jsonnet"):
        if stale.exists():
            fail(f"{stale} must be removed while ccgate hooks are disabled")
    removals = (ROOT / "home/.chezmoiremove").read_text() if (ROOT / "home/.chezmoiremove").exists() else ""
    for target in (".codex/ccgate.jsonnet", ".claude/ccgate.jsonnet"):
        if target not in removals:
            fail(f"home/.chezmoiremove must clean up {target}")

    validate_codex_profile_modify_scripts(manifest)

    env_path = ROOT / "home/dot_agents/model-profiles.env"
    if not env_path.exists():
        fail(f"{env_path} is missing")
    env_text = env_path.read_text()
    for token in ("MODEL_PROFILE_INTERACTIVE", "MODEL_PROFILE_STANDARD_CODEX_ARGS", "MODEL_PROFILE_EXPRESS_CLAUDE_ARGS"):
        if token not in env_text:
            fail(f"{env_path} must define {token}")

    express_agent = ROOT / "home/dot_claude/agents/express-explorer.md"
    if not express_agent.exists() or "model:" not in express_agent.read_text():
        fail(f"{express_agent} must define the low-cost explorer subagent")

    herdr = (ROOT / "home/dot_local/bin/common/executable_herdr-agents").read_text()
    fanout = (ROOT / "home/dot_local/bin/common/executable_agent-fanout").read_text()
    for launcher_text, label in ((herdr, "herdr-agents"), (fanout, "agent-fanout")):
        for token in ("claude-fable-5", "gpt-5.6", "model_reasoning_effort="):
            if token in launcher_text:
                fail(f"{label} must not hardcode model settings: {token!r}")
    if "HERDR_AGENTS_CODEX_PROFILE" not in herdr:
        fail("herdr-agents must launch the Codex worker with a model profile")
    if "model-profiles.env" not in fanout:
        fail("agent-fanout must resolve profile args from model-profiles.env")

    codex_agents = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
    for token in ("model_profiles", "--profile standard", "model-profiles.env"):
        if token not in codex_agents:
            fail(f"home/dot_config/codex/AGENTS.md must document model profile token {token!r}")

    claude_rule = ROOT / "home/dot_config/claude/rules/model-selection.md"
    if not claude_rule.exists():
        fail("Claude Code model-selection rule is missing")
    claude_rule_text = claude_rule.read_text()
    for token in ("model_profiles", "express-explorer", "review"):
        if token not in claude_rule_text:
            fail(f"{claude_rule} must document model profile token {token!r}")


def validate_git_config() -> None:
    """Validate managed Git commit signing configuration."""
    path = ROOT / "home/dot_config/git/config.tmpl"
    text = path.read_text()
    if "signingkey = D55D775A7951407C" in text:
        fail(f"{path.relative_to(ROOT)} must not reference the removed GPG signing key")
    config = configparser.ConfigParser(strict=False)
    config.read_string(text)
    expected = {
        ("user", "signingkey"): "{{ .chezmoi.homeDir }}/.ssh/id_ed25519.pub",
        ("gpg", "format"): "ssh",
        ("commit", "gpgsign"): "true",
    }
    for (section, key), expected_value in expected.items():
        actual_value = config.get(section, key, fallback="").strip()
        if actual_value != expected_value:
            fail(
                f"{path.relative_to(ROOT)} must configure SSH commit signing with "
                f"[{section}] {key} = {expected_value}"
            )
    setup_path = ROOT / "home/dot_local/bin/common/executable_setup-gh"
    setup_text = setup_path.read_text()
    for token in ("admin:ssh_signing_key", "--type signing"):
        if token not in setup_text:
            fail(f"{setup_path.relative_to(ROOT)} must register the default SSH key for commit signing with {token!r}")


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


def read_scannable_text(path: Path) -> str | None:
    data = path.read_bytes()
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        try:
            return data.decode("utf-16")
        except UnicodeDecodeError:
            return None
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def validate_no_obvious_secrets() -> None:
    allowed_secret_placeholders = {
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "FIGMA_OAUTH_TOKEN",
    }
    # CompactionDB uses intentional dummy credentials to exercise its redaction boundary.
    compactiondb_dummy_secret_fixtures = {
        Path("vendor/compactiondb/validate.py"),
        Path("vendor/compactiondb/tests/test_migration.py"),
        Path("vendor/compactiondb/tests/test_redaction.py"),
        Path("vendor/compactiondb/.claude/contextdb/contextdb/redaction.py"),
    }
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "site", "__pycache__"} for part in path.parts):
            continue
        if path.relative_to(ROOT) in compactiondb_dummy_secret_fixtures:
            continue
        text = read_scannable_text(path)
        if text is None:
            continue
        sanitized = text
        for placeholder in allowed_secret_placeholders:
            sanitized = sanitized.replace(placeholder, "")
        if SECRET_PATTERN.search(sanitized):
            fail(f"possible committed secret in {path.relative_to(ROOT)}")


def main() -> None:
    manifest = validate_agent_manifest()
    validate_generated_agent_configs()
    validate_hook_composition()
    validate_skills()
    validate_claude_skill_parity()
    validate_claude_command_parity()
    validate_manifest_home_paths()
    validate_agmsg_script_modes()
    validate_claude_settings(manifest)
    validate_codex_plugins()
    validate_codex_modify_script()
    codex = validate_codex_config(manifest)
    claude = validate_claude_mcp_config()
    validate_mcp_parity(codex, claude, manifest)
    validate_crit_install_assets()
    validate_ponytail_assets(manifest, codex)
    validate_understand_anything_assets()
    validate_pi_assets()
    validate_model_profile_assets(manifest)
    validate_git_config()
    validate_no_removed_claude_skill()
    validate_no_obvious_secrets()
    print("agent asset validation ok")


if __name__ == "__main__":
    main()
