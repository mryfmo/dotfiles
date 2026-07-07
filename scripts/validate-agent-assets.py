#!/usr/bin/env python3
"""Validate Codex, Claude Code, MCP, plugin, and skill assets."""

from __future__ import annotations

import configparser
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
REQUIRED_AGMSG_WRITABLE_ROOTS = {
    "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db",
    "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams",
    "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run",
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
    crit_rule = ROOT / "home/dot_config/claude/rules/crit-review.md"
    if not crit_rule.exists() or "/crit" not in crit_rule.read_text():
        fail("Claude Code Crit review rule must require /crit")


def validate_codex_config(manifest: dict[str, Any]) -> dict[str, Any]:
    codex_path = ROOT / "home/dot_codex/private_config.toml.tmpl"
    text = render_template_text(codex_path)
    if not text.startswith("#:schema https://developers.openai.com/codex/config-schema.json"):
        fail(f"{codex_path} must declare the Codex config schema")
    data = tomllib.loads(text)
    manifest_codex = manifest.get("codex", {})
    for key in ("model", "model_reasoning_effort"):
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


def validate_cognee_install_assets(manifest: dict[str, Any]) -> None:
    if "cognee_memory" not in manifest.get("mcp_servers", {}):
        return
    required_paths = [
        ROOT / "install/common/cognee.sh",
        ROOT / "home/.chezmoiscripts/common/run_once_after_05-install-cognee.sh.tmpl",
        ROOT / "home/dot_local/bin/common/executable_start-cognee-mcp",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_paths if not path.exists()]
    if missing:
        fail("cognee_memory requires install/runtime assets: " + ", ".join(missing))
    installer = (ROOT / "install/common/cognee.sh").read_text()
    for token in ("tool install", "cognee-mcp", "COGNEE_MCP_PYTHON", "resolve_uv", ".local/share/mise/shims"):
        if token not in installer:
            fail(f"install/common/cognee.sh must contain {token!r}")
    mise_config = (ROOT / "home/dot_mise/config.toml").read_text()
    if 'cmake = "latest"' not in mise_config:
        fail("Cognee MCP install needs cmake available through mise for source-built Python dependencies")
    template = (ROOT / "home/.chezmoiscripts/common/run_once_after_05-install-cognee.sh.tmpl").read_text()
    for token in ("hasKey . \"cognee\"", "get .cognee \"install\"", "install/common/cognee.sh"):
        if token not in template:
            fail(f"Cognee install template must contain {token!r}")
    bootstrap = (ROOT / "home/.chezmoi.yaml.tmpl").read_text()
    for token in ("cognee:", "install: false"):
        if token not in bootstrap:
            fail(f"home/.chezmoi.yaml.tmpl must define default Cognee data with {token!r}")
    runner_path = ROOT / "home/dot_local/bin/common/executable_start-cognee-mcp"
    runner = runner_path.read_text()
    for token in ("cognee-mcp", "--transport", "COGNEE_MCP_TRANSPORT", "COGNEE_MCP_HOST", "COGNEE_MCP_PORT", "COGNEE_MCP_PATH"):
        if token not in runner:
            fail(f"{runner_path.relative_to(ROOT)} must contain {token!r}")


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
        fail("home/dot_codex/private_config.toml.tmpl must render the Ponytail Codex plugin")
    if codex.get("marketplaces", {}).get("ponytail", {}).get("source") != "https://github.com/DietrichGebert/ponytail.git":
        fail("home/dot_codex/private_config.toml.tmpl must render the Ponytail Codex marketplace source")
    hook_state = codex.get("hooks", {}).get("state", {})
    for key in (
        "ponytail@ponytail:hooks/claude-codex-hooks.json:session_start:0:0",
        "ponytail@ponytail:hooks/claude-codex-hooks.json:user_prompt_submit:0:0",
        "ponytail@ponytail:hooks/claude-codex-hooks.json:subagent_start:0:0",
    ):
        if not hook_state.get(key, {}).get("trusted_hash", "").startswith("sha256:"):
            fail(f"home/dot_codex/private_config.toml.tmpl must render trusted Ponytail hook state for {key}")

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
    expected_target = "{{ .chezmoi.sourceDir }}/home/dot_config/claude/rules/ponytail.md\n"
    if not claude_symlink.exists() or claude_symlink.read_text() != expected_target:
        fail(f"{claude_symlink} must point at the managed Ponytail Claude rule")

    readme = (ROOT / "README.md").read_text()
    for token in ("Ponytail", "DietrichGebert/ponytail", "ponytail@ponytail", "review and trust"):
        if token not in readme:
            fail(f"README.md must document Ponytail lifecycle token {token!r}")


def validate_ccgate_assets() -> None:
    updater = (ROOT / "scripts/update-agent-assets.sh").read_text()
    for token in (
        "aqua:tak848/ccgate",
        "ccgate --version",
    ):
        if token not in updater:
            fail(f"scripts/update-agent-assets.sh must manage ccgate asset token {token!r}")
    mise_config = (ROOT / "home/dot_mise/config.toml").read_text()
    if '"aqua:tak848/ccgate" = "latest"' not in mise_config:
        fail("home/dot_mise/config.toml must activate aqua:tak848/ccgate")

    codex_path = ROOT / "home/dot_codex/private_config.toml.tmpl"
    codex_text = render_template_text(codex_path)
    for token in ("[[hooks.PermissionRequest]]", "ccgate codex", "ccgate evaluating request"):
        if token not in codex_text:
            fail(f"{codex_path} must configure Codex ccgate hook token {token!r}")

    claude_settings = json.loads((ROOT / "home/dot_claude/private_settings.json").read_text())
    claude_hooks = json.dumps(claude_settings.get("hooks", {}), ensure_ascii=False)
    for token in ("PermissionRequest", "ccgate claude"):
        if token not in claude_hooks:
            fail(f"home/dot_claude/private_settings.json must configure Claude ccgate hook token {token!r}")

    ccgate_configs = {
        ROOT / "home/dot_codex/ccgate.jsonnet": (
            "ccgate codex",
            "HookInput.model",
            "proportionality context",
            "Do not deny necessary read-only inspection",
            "Use metrics later",
        ),
        ROOT / "home/dot_claude/ccgate.jsonnet": (
            "ccgate claude",
            "does not expose the active task model",
            "claude-haiku-4-5",
            "Use metrics later",
        ),
    }
    for path, tokens in ccgate_configs.items():
        if not path.exists():
            fail(f"{path} is missing")
        text = path.read_text()
        for token in tokens:
            if token not in text:
                fail(f"{path} must contain ccgate policy token {token!r}")

    codex_agents = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
    for token in ("ccgate", "HookInput.model", "provider.model", "metrics --details 5", "最小限のモデル"):
        if token not in codex_agents:
            fail(f"home/dot_config/codex/AGENTS.md must document ccgate model token {token!r}")

    claude_rule = ROOT / "home/dot_config/claude/rules/model-selection.md"
    if not claude_rule.exists():
        fail("Claude Code model-selection rule is missing")
    claude_rule_text = claude_rule.read_text()
    for token in ("ccgate", "PermissionRequest", "provider.model", "metrics --details 5", "smallest Claude Code model"):
        if token not in claude_rule_text:
            fail(f"{claude_rule} must document ccgate model token {token!r}")


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
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "site", "__pycache__"} for part in path.parts):
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
    validate_skills()
    validate_claude_skill_parity()
    validate_agmsg_script_modes()
    validate_claude_settings()
    validate_codex_plugins()
    codex = validate_codex_config(manifest)
    claude = validate_claude_mcp_config()
    validate_mcp_parity(codex, claude, manifest)
    validate_cognee_install_assets(manifest)
    validate_crit_install_assets()
    validate_ponytail_assets(manifest, codex)
    validate_ccgate_assets()
    validate_git_config()
    validate_no_removed_claude_skill()
    validate_no_obvious_secrets()
    print("agent asset validation ok")


if __name__ == "__main__":
    main()
