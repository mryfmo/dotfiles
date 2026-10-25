#!/usr/bin/env python3
"""Validate Codex, Claude Code, MCP, plugin, and skill assets."""

from __future__ import annotations

import importlib.util
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterable
from functools import cache
from pathlib import Path
from typing import Any

import tomllib

try:
    import yaml
except ImportError:  # pragma: no cover - CI installs PyYAML for this script.
    yaml = None

ROOT = Path(__file__).resolve().parents[1]


@cache
def generator() -> Any:
    """scripts/generate-agent-configs.py, the one owner of the manifest's rendering rules and expected outputs.

    Loaded on first use, never at import: `--mask-secrets` is a standalone mode that records-sync.sh runs from a tree
    holding this script alone, and it needs nothing from the generator.
    """
    path = Path(__file__).resolve().parent / "generate-agent-configs.py"
    spec = importlib.util.spec_from_file_location("generate_agent_configs", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SECRET_PATTERN = re.compile(
    r"""(?ix)
    (
        # A key prefix starts after a non-word character or the start, or right
        # after an escape sequence (a backslash and 1-9 letters or digits: \n,
        # \u000a, \U0000000A, \x0a); the zero-width lookbehinds keep the escape
        # out of the match, so --mask-secrets leaves it intact.
        (?:(?<![A-Za-z0-9_])|(?<=\\[A-Za-z0-9])|(?<=\\[A-Za-z0-9]{2})|(?<=\\[A-Za-z0-9]{3})|(?<=\\[A-Za-z0-9]{4})|(?<=\\[A-Za-z0-9]{5})|(?<=\\[A-Za-z0-9]{6})|(?<=\\[A-Za-z0-9]{7})|(?<=\\[A-Za-z0-9]{8})|(?<=\\[A-Za-z0-9]{9}))
        (?:ghp_[A-Za-z0-9_]{20,} | github_pat_[A-Za-z0-9_]{20,}
           # An sk- key body holds a run of 20+ hyphen-free key characters within
           # its first 64 characters (an sk-proj- key right after proj-); a
           # hyphenated slug such as ...-sk-boundary-a01-review-receipt never
           # does. The bound keeps a long hyphenated run from rescanning (O(n^2)).
           | sk-(?=[A-Za-z0-9_-]{0,64}[A-Za-z0-9_]{20})[A-Za-z0-9_-]{20,})
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
SYNC_TIMEOUT_BUDGET_S = 30  # PLAN H3 pins the per-source, per-event synchronous budget.
HOOK_COMPOSITION_SOURCES = {
    "claude": (Path("home/.chezmoitemplates/claude-settings-managed.json"), "json"),
    "codex": (Path("home/.chezmoitemplates/codex-config-managed.toml"), "toml"),
    "compactiondb": (
        Path("vendor/compactiondb/.claude/settings.fragment.json"),
        "json",
    ),
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


def render_template_text(path: Path, os_name: str = "darwin") -> str:
    text = path.read_text()
    # This repository uses .chezmoiroot=home, so .chezmoi.sourceDir resolves
    # to the chezmoi source root that contains dot_agents/, dot_codex/, etc.
    text = text.replace("{{ .chezmoi.sourceDir }}", str(ROOT / "home"))
    text = re.sub(r"\{\{/\*.*?\*/\}\}", "", text, flags=re.DOTALL)
    text = re.sub(
        r'\{\{ if eq \.chezmoi\.os "darwin" \}\}(.*?)\{\{ else \}\}(.*?)\{\{ end \}\}',
        lambda match: match[1] if os_name == "darwin" else match[2],
        text,
        flags=re.DOTALL,
    )
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
            match = next(
                (index for index in range(position, len(commands)) if substring in commands[index]),
                None,
            )
            if match is None:
                findings.append(f"sessionstart-order source={source} expected={list(expected)!r} actual={commands!r}")
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


# The Agent Skills frontmatter (agentskills.io/specification): name and description are required, the other four
# fields optional, and no other field is defined. A name is 1-64 lowercase letters, digits and single hyphens, not at
# either end; a description 1-1024 characters; compatibility at most 500; metadata maps strings to strings.
SKILL_FIELDS = frozenset({"name", "description", "license", "compatibility", "metadata", "allowed-tools"})
SKILL_NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SKILL_NAME_MAX = 64
SKILL_DESCRIPTION_MAX = 1024
SKILL_COMPATIBILITY_MAX = 500


def validate_skill_frontmatter(skill_file: Path, directory_name: str, data: dict[str, Any]) -> None:
    unknown = sorted(str(key) for key in data if key not in SKILL_FIELDS)
    if unknown:
        fail(f"{skill_file} frontmatter has fields the Agent Skills specification does not define: {unknown}")
    name = data.get("name")
    if not isinstance(name, str) or len(name) > SKILL_NAME_MAX or not SKILL_NAME_RE.fullmatch(name):
        fail(f"{skill_file} name must be 1-{SKILL_NAME_MAX} lowercase letters, digits and single inner hyphens")
    if name != directory_name:
        fail(f"{skill_file} name does not match directory name")
    description = data.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > SKILL_DESCRIPTION_MAX:
        fail(f"{skill_file} description must be a non-empty string of at most {SKILL_DESCRIPTION_MAX} characters")
    compatibility = data.get("compatibility")
    if compatibility is not None and (
        not isinstance(compatibility, str) or not compatibility or len(compatibility) > SKILL_COMPATIBILITY_MAX
    ):
        fail(f"{skill_file} compatibility must be a non-empty string of at most {SKILL_COMPATIBILITY_MAX} characters")
    metadata = data.get("metadata")
    if metadata is not None and (
        not isinstance(metadata, dict)
        or not all(isinstance(key, str) and isinstance(value, str) for key, value in metadata.items())
    ):
        fail(f"{skill_file} metadata must map strings to strings")
    for key in ("license", "allowed-tools"):
        if key in data and not isinstance(data[key], str):
            fail(f"{skill_file} {key} must be a string")


def validate_skills() -> None:
    skills_root = ROOT / "home/dot_agents/skills"
    if not skills_root.exists():
        fail(f"{skills_root} is missing")
    for skill_dir in sorted(p for p in skills_root.iterdir() if p.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            fail(f"{skill_dir} is missing SKILL.md")
        validate_skill_frontmatter(skill_file, skill_dir.name, read_frontmatter(skill_file))
        openai_yaml = skill_dir / "agents/openai.yaml"
        if openai_yaml.exists():
            parsed = load_yaml(openai_yaml)
            if not isinstance(parsed, dict):
                fail(f"{openai_yaml} must be a mapping")


# The home the overlays' {{ .chezmoi.homeDir }} is read as when validate_skill_audience parses them.
SKILL_CONFIG_HOME = "/validator-home"


def rendered_omp_skill_configs(manifest: dict[str, Any]) -> dict[str, Path]:
    """Each omp consumer's rendered config: the plain-launch template and one overlay per omp.roles entry."""
    rendered = {"omp": ROOT / "home/.chezmoitemplates/omp-config-managed.yml"}
    rendered |= {
        f"omp-{role}": ROOT / f"home/dot_agents/omp/profiles/{role}.yml.tmpl"
        for role in generator().omp_roles(manifest)
    }
    return rendered


def validate_skill_audience(manifest: dict[str, Any], omp_configs: dict[str, Any] | None = None) -> None:
    """Parse each rendered agent config and refuse one that would list a skill outside its skills.audience.

    Codex: the managed baseline's `[[skills.config]]` entries are exactly one `enabled = false` per ~/.agents/skills
    skill that leaves out Codex, by its SKILL.md path. omp: each role overlay and the plain-launch config carry the
    consumer's skill settings (skills.enabled false, or the roots and skills.ignoredSkills). Claude Code: a
    ~/.claude/skills link exists only for a skill that names it. `omp_configs` maps each consumer to its parsed
    config (its {{ .chezmoi.homeDir }} read as SKILL_CONFIG_HOME); without it the files are read here, which needs
    PyYAML.
    """
    gen = generator()
    declared, _, _ = gen.skill_audiences(manifest)
    codex = tomllib.loads((ROOT / manifest["codex"]["config_path"]).read_text())
    entries = codex.get("skills", {}).get("config", [])
    expected = [
        {"path": f"{{{{ .chezmoi.homeDir }}}}/.agents/skills/{name}/SKILL.md", "enabled": False}
        for name in gen.codex_disabled_skills(manifest)
    ]
    if entries != expected:
        fail(f"{manifest['codex']['config_path']} [[skills.config]] must disable exactly {expected}: {entries}")
    rendered = rendered_omp_skill_configs(manifest)
    if omp_configs is None:
        if yaml is None:
            fail("PyYAML is required to read the rendered omp configs")
        omp_configs = {
            consumer: yaml.safe_load(path.read_text().replace("{{ .chezmoi.homeDir }}", SKILL_CONFIG_HOME))
            for consumer, path in rendered.items()
        }
    home = SKILL_CONFIG_HOME
    for consumer, path in rendered.items():
        parsed = omp_configs.get(consumer)
        skills = parsed.get("skills") if isinstance(parsed, dict) else None
        settings = gen.omp_skill_settings(manifest, consumer)
        if settings["enabled"]:
            # The overlays carry the absolute home through the chezmoi template; the plain config keeps ~/.
            prefix = "~/" if consumer == "omp" else f"{home}/"
            want = {
                "enabled": True,
                "customDirectories": [re.sub(r"^~/", prefix, d) for d in settings["customDirectories"]],
                "ignoredSkills": settings["ignoredSkills"],
            }
        else:
            want = {"enabled": False}
        if skills != want:
            fail(f"{path.relative_to(ROOT)} skills must be {want} for {consumer}: {skills}")
    claude_links = {path.name for path in (ROOT / "home/dot_claude/skills").iterdir() if path.is_dir()}
    wrong = sorted(name for name in claude_links if "claude" not in declared.get(name, []))
    if wrong:
        fail(f"home/dot_claude/skills links skills whose audience leaves out claude: {wrong}")


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
            fail(
                f"{manifest_path}:{number} must not hard-code a home directory; use {{{{ .chezmoi.homeDir }}}} so the rendered value stays byte-identical to what the agent runtimes write"
            )


def validate_codex_plugins(manifest: dict[str, Any]) -> None:
    marketplace_path = ROOT / manifest["plugins"]["marketplace_path"]
    marketplace = json.loads(marketplace_path.read_text())
    if not marketplace.get("name"):
        fail(f"{marketplace_path} is missing name")
    plugins = marketplace.get("plugins", [])
    if not isinstance(plugins, list) or not plugins:
        fail(f"{marketplace_path} must define at least one plugin")
    # Every plugin ships its own .codex-plugin/plugin.json at install time (crit: `crit install codex-plugin`); a file
    # of ours under home/dot_agents/plugins other than the marketplace is an orphan the generator refuses (F127).
    for plugin in plugins:
        source = plugin.get("source", {})
        if source.get("source") == "local" and Path(source.get("path", "")).is_absolute():
            fail(f"{marketplace_path} must not use absolute local plugin paths")


def validate_exact_keys(actual: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    actual_keys = set(actual)
    expected_keys = set(expected)
    if actual_keys != expected_keys:
        fail(
            f"{label} keys must match the shared manifest: "
            f"missing={sorted(expected_keys - actual_keys)} extra={sorted(actual_keys - expected_keys)}"
        )


SANDBOX_HOSTNAME = re.compile(r"[a-z0-9-]+(\.[a-z0-9-]+)+")
# The only directories a sandboxed command may write beyond the working directory and its session TMPDIR (U68): an
# exact allowlist, compared byte for byte, for every write-root list the manifest renders (Claude allowWrite, which
# includes the Codex writable_roots, the Codex writable_roots themselves, Claude additionalDirectories). No spelling
# is normalised, so a case variant, a `..` route, a symlink or another home anchor is refused because it is not on the
# list, not because it was recognised as dangerous. Adding a root is a change to this list, reviewed as a
# trust-boundary change; none may hold an executable on PATH (~/.local/bin, the uv tools, mise's installs) or state an
# unsandboxed run trusts (mise's trusted-configs).
SANDBOX_WRITE_ROOTS = (
    # The uv cache: every `uv run` target needs it writable (T39 live E2E leg 1).
    "~/.cache/uv",
    # The hcom stores: the dotfiles program's store until its one-time move, and the derived per-repository stores.
    "~/.local/state/hcom-regime",
    "~/.local/state/hcom",
    # The omp seat worktrees, which `hcom-seat worker` creates and reuses.
    "~/.local/state/omp-seats",
)
# mise's macOS cache directory; Linux keeps mise's cache under ~/.cache/mise, which is not listed.
DARWIN_SANDBOX_WRITE_ROOTS = ("~/Library/Caches/mise",)


def validate_write_roots(roots: Any, label: str, os_name: str = "linux") -> None:
    """Refuse a write root that is not byte-identical to an allowlisted spelling for `os_name` (U68)."""
    if not isinstance(roots, list):
        fail(f"{label} must be a list: {roots!r}")
    permitted = (*SANDBOX_WRITE_ROOTS, *(DARWIN_SANDBOX_WRITE_ROOTS if os_name == "darwin" else ()))
    # Byte-for-byte on purpose: any normalisation would re-open the spellings this list exists to refuse.
    unlisted = [r for r in roots if not isinstance(r, str) or r not in permitted]  # lint-comparisons: allow exact text
    if unlisted:
        fail(
            f"{label} entries must be exactly one of {list(permitted)} (an exact allowlist in "
            f"validate-agent-assets.py; adding a root is a reviewed trust-boundary change): {unlisted}"
        )


# Credential stores every sandboxed command is denied (U68): SSH keys, the gh token, the agents' login stores, the
# age key. Every credential entry is a plain deny: a `mask` lets the sandbox proxy put the real value into any request
# body to its injectHosts, so a sandboxed client can send the placeholder to an endpoint that echoes it (GitHub's
# POST /markdown) and read the real token back (audit round 6, on the installed Claude Code 2.1.310 transformer).
SANDBOX_CREDENTIAL_DENIES = (
    "~/.ssh",
    "~/.config/gh/hosts.yml",
    "~/.claude/.credentials.json",
    "~/.config/claude-code/oauth-token",
    "~/.codex/auth.json",
    "~/.omp/agent/agent.db*",
    "~/.omp/profiles/*/agent/agent.db*",
    "~/.config/age/key.txt",
)
SANDBOX_ENV_DENIES = ("CLAUDE_CODE_OAUTH_TOKEN",)
# Strict sandbox mode (U68): `allowUnsandboxedCommands` is false, so Claude Code ignores the
# `dangerouslyDisableSandbox` retry, and exactly these exclusions run outside the sandbox, each behind an identical
# `Bash(<pattern>)` ask rule. `git push` needs ~/.ssh and `gh` needs its hosts file, both denied inside. Claude Code
# 2.1.310 parses a `Bash(dangerouslyDisableSandbox:true)` rule as a literal command, so no rule may name the parameter.
SANDBOX_EXCLUSIONS = ("git push *", "gh *")
RETRY_PARAMETER = "dangerouslyDisableSandbox"


def validate_claude_sandbox_credentials(sandbox: dict[str, Any], label: str) -> None:
    """Require every credential store denied, each entry exactly `{path|name, mode: deny}`, each named once (U68).

    Every entry is checked: Claude Code 2.1.310 merges credential entries and keeps the later of two entries for one
    path, so a duplicate is refused outright. No mask is accepted, and so no TLS termination either.
    """
    credentials = sandbox.get("credentials", {})
    files = credentials.get("files") if isinstance(credentials, dict) else None
    if not isinstance(files, list) or not all(isinstance(e, dict) and isinstance(e.get("path"), str) for e in files):
        fail(f"{label}.credentials.files must contain a list of entries: {files!r}")
    paths = [entry["path"] for entry in files]
    duplicated = sorted({path for path in paths if paths.count(path) > 1})
    if duplicated:
        fail(f"{label}.credentials.files must name each path once (Claude Code keeps the later entry): {duplicated}")
    not_deny = [entry for entry in files if entry.get("mode") != "deny" or set(entry) != {"path", "mode"}]
    if not_deny:
        fail(f"{label}.credentials.files entries must all be exactly path and deny (no mask): {not_deny}")
    missing = [path for path in SANDBOX_CREDENTIAL_DENIES if path not in paths]  # lint-comparisons: allow settings text
    if missing:
        fail(f"{label}.credentials.files must contain a deny entry for each credential store: missing={missing}")
    env_vars = credentials.get("envVars", [])
    if not isinstance(env_vars, list) or not all(
        isinstance(e, dict) and isinstance(e.get("name"), str) for e in env_vars
    ):
        fail(f"{label}.credentials.envVars must deny {list(SANDBOX_ENV_DENIES)}: {env_vars!r}")
    names = [entry["name"] for entry in env_vars]
    duplicated = sorted({name for name in names if names.count(name) > 1})
    if duplicated:
        fail(
            f"{label}.credentials.envVars must name each variable once (Claude Code keeps the later entry): {duplicated}"
        )
    not_deny = [entry for entry in env_vars if entry.get("mode") != "deny" or set(entry) != {"name", "mode"}]
    if not_deny:
        fail(f"{label}.credentials.envVars entries must all be exactly name and deny (no mask): {not_deny}")
    if not set(SANDBOX_ENV_DENIES) <= set(names):
        fail(f"{label}.credentials.envVars must deny {list(SANDBOX_ENV_DENIES)}: {env_vars!r}")
    for key in ("allowPlaintextInject", "awsPairs", "sigv4"):
        if key in credentials:
            fail(f"{label}.credentials.{key} must not be set: no credential is ever injected")
    if "tlsTerminate" in sandbox.get("network", {}):
        fail(f"{label}.network.tlsTerminate must not be set: no mask needs it")


def validate_claude_sandbox(sandbox: Any, writable_roots: list[str], label: str, os_name: str = "darwin") -> None:
    """Require the confined, prompt-free Claude sandbox that mirrors the Codex one."""
    if not isinstance(sandbox, dict):
        fail(f"{label} must define the sandbox object")
    for key in ("enabled", "autoAllowBashIfSandboxed"):
        if sandbox.get(key) is not True:
            fail(f"{label}.{key} must be true")
    if sandbox.get("failIfUnavailable") is not True:
        fail(f"{label}.failIfUnavailable must be true: a sandbox that cannot start must stop Claude Code")
    allow_write = sandbox.get("filesystem", {}).get("allowWrite", [])
    missing = set(writable_roots) - set(allow_write)
    if missing:
        fail(f"{label}.filesystem.allowWrite must include every Codex writable root: missing={sorted(missing)}")
    validate_write_roots(allow_write, f"{label}.filesystem.allowWrite", os_name)
    deny_read = sandbox.get("filesystem", {}).get("denyRead")
    entries = deny_read if isinstance(deny_read, list) else []
    rooted = [entry for entry in entries if isinstance(entry, str) and entry.startswith(("/", "~/"))]
    if not entries or len(rooted) != len(entries):
        fail(
            f"{label}.filesystem.denyRead must be a non-empty list of absolute or ~/ paths "
            f"(globs are allowed here, unlike allowWrite): {deny_read!r}"
        )
    domains = sandbox.get("network", {}).get("allowedDomains")
    if not isinstance(domains, list) or not domains:
        fail(f"{label}.network.allowedDomains must be a non-empty list")
    invalid = [domain for domain in domains if not isinstance(domain, str) or not SANDBOX_HOSTNAME.fullmatch(domain)]
    if invalid:
        fail(f"{label}.network.allowedDomains must contain only hostnames: {invalid}")
    forbidden = {"cafe.github.com", "datadoghq.com", "checkpoint-api.hashicorp.com", "api.anthropic.com"}
    if any(domain in forbidden or domain.endswith(".datadoghq.com") for domain in domains):
        fail(f"{label} must not allow telemetry or metadata domains")
    validate_claude_sandbox_credentials(sandbox, label)
    network = sandbox.get("network", {})
    mach = network.get("allowMachLookup", [])
    if not isinstance(mach, list) or any(
        service != "com.apple.trustd.agent" or os_name != "darwin" for service in mach
    ):
        fail(f"{label} Mach services must stay within the macOS trustd allowlist")
    if network.get("allowAllUnixSockets") is True:
        fail(f"{label}.network.allowAllUnixSockets must not be true")
    if sandbox.get("allowUnsandboxedCommands") is not False:
        fail(f"{label}.allowUnsandboxedCommands must be false: no command may leave the sandbox by an unprompted retry")
    exclusions = sandbox.get("excludedCommands", [])
    exact = isinstance(exclusions, list) and sorted(map(str, exclusions)) == sorted(SANDBOX_EXCLUSIONS)
    if not exact:
        fail(
            f"{label} {'macOS' if os_name == 'darwin' else 'Linux'} excludedCommands must be exactly "
            f"{list(SANDBOX_EXCLUSIONS)}: {exclusions!r}"
        )
    # Each reachable socket is a way out of the sandbox (the herdr socket starts host processes), and Linux ignores
    # the list (U68): no socket is listed.
    if "allowUnixSockets" in network and (os_name != "darwin" or network["allowUnixSockets"] != []):
        fail(f"{label}.network.allowUnixSockets must not list a socket: {network['allowUnixSockets']!r}")


# The managed allow rules (regime-cutover U16, U31): the read-only `hcom list` and the coordinator
# levers, one `Bash(~/.local/bin/common/<lever> *)` per deterministic wrapper script, naming the copy chezmoi installs
# outside every sandbox write root. An allow rule skips the auto-mode classifier unless it could run arbitrary code
# (code.claude.com/docs/en/settings, `autoMode.classifyAllShell`), so nothing else is accepted: no `Bash(*)`, no
# `Bash(hcom *)` (hcom launches agents), no interpreter or shell prefix, and no path inside the rewritable checkout.
FIXED_ALLOW_RULES = ("Bash(hcom list *)",)
LEVER_INSTALL_PREFIX = "~/.local/bin/common/"
LEVER_ALLOW_RULE = re.compile(r"Bash\(~/\.local/bin/common/([A-Za-z0-9][A-Za-z0-9_.-]*) \*\)")
CHECKOUT_LEVER_RULE = re.compile(r"Bash\((?:\./)?scripts/orchestrator/")
INTERPRETERS = frozenset(
    {"sh", "bash", "zsh", "dash", "ksh", "fish", "env", "xargs", "osascript", "python", "python3", "perl", "ruby"}
    | {"node", "bun", "deno", "uv", "uvx", "npx"}
)


def lever_refusal(name: str) -> str | None:
    """Return why `<name>` cannot carry an allow rule, or None when it can.

    The source `scripts/orchestrator/<name>` must be a regular executable shebang script not named as an interpreter,
    and `home/dot_local/bin/common/executable_<name>`, the copy chezmoi installs, must hold the same bytes.
    """
    path = ROOT / "scripts/orchestrator" / name
    if path.is_symlink() or not path.is_file():
        return "is not a regular file"
    if not os.access(path, os.X_OK):
        return "is not executable"
    if name in INTERPRETERS or Path(name).stem in INTERPRETERS:
        return "is named as an interpreter"
    with path.open("rb") as script:
        if script.read(2) != b"#!":
            return "is not a script with a shebang line"
    installed = ROOT / "home/dot_local/bin/common" / f"executable_{name}"
    if not installed.is_file() or installed.read_bytes() != path.read_bytes():
        return f"has no byte-identical installed copy {installed.relative_to(ROOT)} (run the generator)"
    return None


def validate_claude_permissions_allow(permissions: Any, label: str, pinned: Iterable[str] | None = None) -> None:
    allow = permissions.get("allow", []) if isinstance(permissions, dict) else []
    if not isinstance(allow, list) or not all(isinstance(rule, str) and rule.strip() for rule in allow):
        fail(f"{label}.allow must be a list of non-empty permission rules")
    for rule in allow:
        if rule in FIXED_ALLOW_RULES:
            continue
        if CHECKOUT_LEVER_RULE.match(rule):
            fail(
                f"{label}.allow rule {rule!r} names a lever inside the rewritable checkout; "
                f"name the installed copy, Bash({LEVER_INSTALL_PREFIX}<lever> *) (regime-cutover U31)"
            )
        lever = LEVER_ALLOW_RULE.fullmatch(rule)
        if not lever:
            fail(
                f"{label}.allow rule {rule!r} is not {' or '.join(FIXED_ALLOW_RULES)} "
                f"or Bash({LEVER_INSTALL_PREFIX}<lever> *)"
            )
        reason = lever_refusal(lever.group(1))
        if reason:
            fail(f"{label}.allow rule {rule!r}: scripts/orchestrator/{lever.group(1)} {reason}")
        if pinned is not None and lever.group(1) not in pinned:
            fail(f"{label}.allow rule {rule!r}: no claude.levers.sha256 pin for {lever.group(1)}")


# The omp writing seats' allow rows (regime-cutover U28): an allow in orchestrator.yml or worker.yml is one lever by its
# installed path, `~/.local/bin/common/<lever> *`, `~/.local/bin/common/<lever> --<flag> *` or the exact bare
# `~/.local/bin/common/<lever>` (U28b F3), held to the same lever checks as a Claude allow rule. audit.yml keeps its
# read-only allows under `always-ask`; tests/unit/test_omp_seat_policy.py holds its decision table.
OMP_POLICY_DIR = "home/dot_agents/omp/policies"
OMP_WRITING_POLICIES = ("orchestrator", "worker")
# GitHub reach (U71, audit rounds 3, 8 and 9): enumerating merge spellings always missed one (`/merges`, then GraphQL
# `mergePullRequest`), so in every policy file under OMP_POLICY_DIR, found by glob so a new or renamed file is covered
# too, an allow row that mentions `gh`, `graphql`, `api.github.com`, `curl` or `wget` must be byte-identical to an
# entry of its role's list below; any other such row is refused. The lists are today's rows, small and exact, so the
# single manifest list U76 renders the policies from can adopt them. The orchestrator merges only through pr-merge.sh.
OMP_GITHUB_REACH = re.compile(r"\bgh\b|graphql|api\.github\.com|\bcurl\b|\bwget\b", re.IGNORECASE)
OMP_GITHUB_ALLOWLIST = {
    # the auditor's read-only GitHub reads, behind audit.yml's common and write-method denies
    "audit": ("gh pr view *", "gh pr diff *", "gh pr checks *", "gh run view *", "gh api repos/*"),
    # the orchestrator's GitHub writes go through its levers only; no raw gh row
    "orchestrator": (),
    # the worker's one GitHub-write lever; its gh pr create/ready/comment run under the yolo default, not an allow row
    "worker": (),
}
OMP_LEVER_ALLOW = re.compile(r"~/\.local/bin/common/([A-Za-z0-9][A-Za-z0-9_.-]*)(?:(?: --[a-z][a-z-]*)? \*)?")
OMP_CHECKOUT_LEVER = re.compile(r"\*?(?:\./)?scripts/orchestrator/")
# The worker's own-branch pushes (regime-cutover U76): the only allow rows besides levers in a writing policy, worker.yml
# only. Exact lines without a wildcard (omp patterns have no character class, so a branch word could not be limited to
# a safe character set), followed by the catch-all push denies, in this order; omp takes the first matching rule.
OMP_WORKER_PUSH_ALLOW = ("git push", "git push origin HEAD", "git push -u origin HEAD")
OMP_WORKER_PUSH_CATCH = ("*git push*", "*git -* push*")


def validate_omp_worker_push(patterns: list[dict[str, Any]], label: str) -> None:
    """The worker's push rows are exactly the three allows and the catch-all denies, contiguous and in that order; a
    change to any of them is a reviewed change to these constants."""
    expected = [
        *({"match": match, "approval": "allow"} for match in OMP_WORKER_PUSH_ALLOW),
        *({"match": match, "approval": "deny"} for match in OMP_WORKER_PUSH_CATCH),
    ]
    starts = [index for index, rule in enumerate(patterns) if rule == expected[0]]
    if len(starts) != 1 or patterns[starts[0] : starts[0] + len(expected)] != expected:
        fail(f"{label} must hold the worker push rows of validate-agent-assets.py exactly once, in order")


def validate_omp_policy_allow(policy: Any, label: str, pinned: Iterable[str] | None = None, role: str = "") -> None:
    patterns = policy.get("bash", {}).get("patterns") if isinstance(policy, dict) else None
    if not isinstance(patterns, list) or not all(isinstance(rule, dict) for rule in patterns):
        fail(f"{label} bash.patterns must be a list of rules")
    if role == "worker":
        validate_omp_worker_push(patterns, label)
    for rule in patterns:
        if rule.get("approval") != "allow":
            continue
        match = rule.get("match")
        if not isinstance(match, str):
            fail(f"{label} allow rule {match!r} is not a string")
        if role == "worker" and match in OMP_WORKER_PUSH_ALLOW:
            continue
        if OMP_CHECKOUT_LEVER.match(match):
            fail(
                f"{label} allow rule {match!r} names a lever inside the rewritable checkout; "
                f"name the installed copy, {LEVER_INSTALL_PREFIX}<lever> * (regime-cutover U28)"
            )
        lever = OMP_LEVER_ALLOW.fullmatch(match)
        if not lever:
            fail(f"{label} allow rule {match!r} is not {LEVER_INSTALL_PREFIX}<lever> [[--<flag>] *]")
        reason = lever_refusal(lever.group(1))
        if reason:
            fail(f"{label} allow rule {match!r}: scripts/orchestrator/{lever.group(1)} {reason}")
        if pinned is not None and lever.group(1) not in pinned:
            fail(f"{label} allow rule {match!r}: no claude.levers.sha256 pin for {lever.group(1)}")


def omp_policy_roles() -> list[str]:
    """The role of every policy file under OMP_POLICY_DIR (`<role>.yml`), found by glob."""
    roles = sorted(path.stem for path in (ROOT / OMP_POLICY_DIR).glob("*.yml"))
    if not roles:
        fail(f"{ROOT / OMP_POLICY_DIR} holds no omp seat policy")
    return roles


def validate_omp_github_allow(policy: Any, label: str, role: str) -> None:
    """Refuse an allow rule that mentions GitHub reach unless it is byte-identical to an OMP_GITHUB_ALLOWLIST entry of
    its role (U71); a role without a list allows no such row."""
    patterns = policy.get("bash", {}).get("patterns") if isinstance(policy, dict) else None
    if not isinstance(patterns, list) or not all(isinstance(rule, dict) for rule in patterns):
        fail(f"{label} bash.patterns must be a list of rules")
    for rule in patterns:
        match = rule.get("match")
        if rule.get("approval") != "allow" or not isinstance(match, str) or not OMP_GITHUB_REACH.search(match):
            continue
        if match not in OMP_GITHUB_ALLOWLIST.get(role, ()):
            fail(
                f"{label} allow rule {match!r} reaches GitHub and is not on the {role} allowlist in "
                f"validate-agent-assets.py; seats merge only through {LEVER_INSTALL_PREFIX}pr-merge.sh (regime-cutover U71)"
            )


def validate_omp_policies(manifest: dict[str, Any], policies: dict[str, Any] | None = None) -> None:
    """Check every seat policy's GitHub-reaching allow rows against its allowlist and the writing seats' allow rows; `policies` maps each role of
    omp_policy_roles() to its parsed overlay, else PyYAML reads the files."""
    if policies is None and yaml is None:
        fail("PyYAML is required to read the omp seat policies")
    pinned = manifest.get("claude", {}).get("levers", {}).get("sha256", {})
    roles = omp_policy_roles()
    if policies is not None and sorted(policies) != roles:
        fail(f"the parsed omp policies {sorted(policies)} are not the policy files {roles}")
    for role in roles:
        path = ROOT / OMP_POLICY_DIR / f"{role}.yml"
        policy = policies[role] if policies is not None else yaml.safe_load(path.read_text())
        validate_omp_github_allow(policy, str(path), role)
        if role in OMP_WRITING_POLICIES:
            validate_omp_policy_allow(policy, str(path), pinned, role)


# The glob forms of Read/Edit permission rules are dropped by the Linux sandbox (claude doctor: "On Linux, glob patterns
# in Edit/Read rules will be ignored"); a trailing `/**` is the directory form and is enforced. Only the `.env` pair
# keeps its glob, because `sandbox.filesystem.denyRead` covers it for subprocesses (regime-cutover U17).
GLOB_DENY_RULES = ("Read(.env.*)", "Edit(.env*)")
FILE_RULE = re.compile(r"(Read|Edit)\((.+)\)")


def validate_claude_permissions_deny(permissions: Any, label: str) -> None:
    deny = permissions.get("deny", []) if isinstance(permissions, dict) else []
    for rule in deny:
        match = FILE_RULE.fullmatch(rule) if isinstance(rule, str) else None
        if not match or rule in GLOB_DENY_RULES:
            continue
        path = match.group(2).removesuffix("/**")
        if any(char in path.rsplit("/", 1)[-1] for char in "*?["):
            fail(
                f"{label}.deny rule {rule!r} ends in a glob segment, which the Linux sandbox ignores; only "
                f"{' and '.join(GLOB_DENY_RULES)} keep a glob, covered for subprocesses by sandbox.filesystem.denyRead"
            )


def validate_claude_settings(manifest: dict[str, Any], os_name: str = "darwin") -> None:
    settings_path = ROOT / manifest["claude"]["settings_path"]
    settings = json.loads(render_template_text(settings_path, os_name))
    if settings.get("$schema") != manifest["claude"]["schema"]:
        fail(f"{settings_path} must declare the Claude Code settings schema claude.schema names")
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
    pinned = manifest.get("claude", {}).get("levers", {}).get("sha256", {})
    validate_claude_permissions_allow(settings.get("permissions"), f"{settings_path} {os_name} permissions", pinned)
    validate_claude_permissions_deny(settings.get("permissions"), f"{settings_path} permissions")
    validate_claude_sandbox(
        settings.get("sandbox"),
        manifest.get("codex", {}).get("sandbox_workspace_write", {}).get("writable_roots", []),
        f"{settings_path} {os_name} sandbox",
        os_name,
    )
    permissions = settings.get("permissions") or {}
    ask = permissions.get("ask") or []
    unprompted = [entry for entry in settings["sandbox"].get("excludedCommands", []) if f"Bash({entry})" not in ask]
    if unprompted:
        fail(
            f"{settings_path} {os_name} permissions.ask must hold Bash(<pattern>) for each excluded command: {unprompted}"
        )
    named = [
        rule
        for kind in ("allow", "ask", "deny")
        for rule in permissions.get(kind) or []
        if isinstance(rule, str) and RETRY_PARAMETER in rule
    ]
    if named:
        fail(
            f"{settings_path} {os_name} permissions must not name {RETRY_PARAMETER}, a literal command to Claude Code: {named}"
        )
    # additionalDirectories grant sandboxed commands write access like allowWrite (code.claude.com/docs/en/sandboxing).
    validate_write_roots(
        (settings.get("permissions") or {}).get("additionalDirectories", []),
        f"{settings_path} {os_name} permissions.additionalDirectories",
        os_name,
    )
    enabled_plugins = settings.get("enabledPlugins", {})
    if enabled_plugins:
        fail(f"{settings_path} must not enable Claude plugins that are not installed by this repository")
    if os_name == "darwin":
        validate_claude_settings(manifest, "linux")


# The HooksToml event properties of https://developers.openai.com/codex/config-schema.json.
CODEX_HOOK_EVENTS = frozenset(
    {
        "Interrupt",
        "PermissionRequest",
        "PostCompact",
        "PostToolUse",
        "PreCompact",
        "PreToolUse",
        "SessionEnd",
        "SessionStart",
        "Stop",
        "SubagentStart",
        "SubagentStop",
        "UserPromptSubmit",
    }
)


CODEX_SHORT_HOOK_EVENTS = frozenset({"Interrupt", "SessionEnd"})


def codex_hook_table(hook: dict[str, Any]) -> dict[str, Any]:
    """The parsed [[hooks.<Event>]] matcher group that generate-agent-configs.py renders for one hook."""
    handler = {"type": "command", "command": hook["command"], "timeout": hook["timeout"]}
    return {"matcher": "*", "hooks": [{**handler, "statusMessage": hook["status_message"]}]}


def validate_codex_command_hooks(
    manifest_hooks: dict[str, Any], rendered_hooks: dict[str, Any], codex_path: Path
) -> None:
    """Check codex.hooks.command_hooks and require the template to hold exactly the declared hook tables."""
    # Only a missing key defaults to no hooks; a falsey non-list value is a malformed declaration.
    command_hooks = manifest_hooks.get("command_hooks", [])
    if not isinstance(command_hooks, list):
        fail("codex.hooks.command_hooks must be a list")
    expected: dict[str, list[dict[str, Any]]] = {}
    if manifest_hooks.get("permission_request"):
        expected["PermissionRequest"] = [codex_hook_table(manifest_hooks["permission_request"])]
    for index, hook in enumerate(command_hooks):
        label = f"codex.hooks.command_hooks[{index}]"
        if not isinstance(hook, dict):
            fail(f"{label} must be a mapping")
        if hook.get("event") not in CODEX_HOOK_EVENTS:
            fail(f"{label} event {hook.get('event')!r} is not a Codex hook event: {sorted(CODEX_HOOK_EVENTS)}")
        if not isinstance(hook.get("command"), str) or not hook["command"].strip():
            fail(f"{label} must set a non-empty command")
        timeout = hook.get("timeout")
        if not isinstance(timeout, int) or isinstance(timeout, bool) or timeout <= 0:
            fail(f"{label} timeout must be a positive integer: {timeout!r}")
        # https://developers.openai.com/codex/hooks/: these two events support up to 3 seconds.
        if hook["event"] in CODEX_SHORT_HOOK_EVENTS and timeout > 3:
            fail(f"{label} timeout must be at most 3 seconds for {hook['event']}: {timeout!r}")
        if not isinstance(hook.get("status_message"), str):
            fail(f"{label} must set status_message as a string")
        expected.setdefault(hook["event"], []).append(codex_hook_table(hook))
    rendered = {event: tables for event, tables in rendered_hooks.items() if event != "state"}
    if rendered != expected:
        counts = {event: len(tables) if isinstance(tables, list) else tables for event, tables in rendered.items()}
        declared = {event: len(tables) for event, tables in expected.items()}
        fail(f"{codex_path} must hold exactly the manifest's Codex hook tables: rendered {counts}, declared {declared}")


def validate_codex_config(manifest: dict[str, Any]) -> dict[str, Any]:
    codex_path = ROOT / manifest["codex"]["config_path"]
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
    if data.get("sandbox_workspace_write") != manifest_codex.get("sandbox_workspace_write"):
        fail(f"{codex_path} must render codex.sandbox_workspace_write from the shared manifest")
    # The Codex config is one file for both OSes, so its roots must be on the list shared by both.
    validate_write_roots(
        data.get("sandbox_workspace_write", {}).get("writable_roots", []),
        f"{codex_path} sandbox_workspace_write.writable_roots",
    )
    features = data.get("features", {})
    for feature in ("plugins", "hooks", "plugin_hooks"):
        if features.get(feature) is not True:
            fail(f"{codex_path} must enable Codex feature {feature} for Crit plugin hooks")
    if data.get("shell_environment_policy") != manifest_codex.get("shell_environment_policy"):
        fail(f"{codex_path} must render codex.shell_environment_policy from the shared manifest")
    shell_path = data.get("shell_environment_policy", {}).get("set", {}).get("PATH", "")
    if HARD_CODED_HOME_RE.search(shell_path):
        fail(f"{codex_path} must not hard-code a home directory in shell_environment_policy.set.PATH")
    if "{{ .chezmoi.homeDir }}" not in shell_path:
        fail(f"{codex_path} must derive shell_environment_policy.set.PATH from the target chezmoi homeDir")
    for project_path in data.get("projects", {}):
        if HARD_CODED_HOME_RE.search(project_path):
            fail(f"{codex_path} must not hard-code a home directory in [projects] keys")
        if "{{ .chezmoi.workingTree }}" not in project_path:
            fail(f"{codex_path} must key managed Codex project trust with {{{{ .chezmoi.workingTree }}}}")
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
        revision = manifest.get("assets", {}).get("codex-plugins", {}).get("plugins", {}).get(marketplace_name, {})
        expected = {
            **{key: revision[key] for key in ("last_updated", "last_revision") if key in revision},
            **marketplace_config,
        }
        if data.get("marketplaces", {}).get(marketplace_name) != expected:
            fail(f"{codex_path} must render Codex marketplace {marketplace_name}")
    validate_exact_keys(
        data.get("marketplaces", {}),
        manifest_codex.get("marketplaces", {}),
        f"{codex_path} Codex marketplaces",
    )
    manifest_hook_state = manifest_codex.get("hooks", {}).get("state", {})
    if data.get("hooks", {}).get("state", {}) != manifest_hook_state:
        fail(f"{codex_path} must render Codex hook trust state from the shared manifest")
    validate_codex_command_hooks(manifest_codex.get("hooks", {}), data.get("hooks", {}), codex_path)
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


ASSET_VERIFY_BY_SOURCE = {
    "github-release": {"sha256", "release-shasums", "release-sha256", "gpg", "github-release-attestation"},
    "https-download": {"sha256", "gpg"},
    "crates": {"cargo-locked"},
    "git-commit": {"sha256"},
    "installer-script": {"installer-sha256"},
    "vendored": {"manifest-sha256", "none"},
    "claude-plugin": {"none"},
    "codex-plugin": {"none"},
    "gh-extension": {"none"},
}
# `release: latest` resolves at install time; only these sources can do that.
ROLLING_ASSET_SOURCES = {"github-release", "https-download", "crates"}
# A rolling asset carries no version or checksum of its own.
ROLLING_ASSET_FORBIDDEN_FIELDS = ("pin", "ref", "ref_commit", "sha256")
# A rolling asset needs a check independent of the release page it comes from: a release attestation,
# a signature with a pinned key, or an immutable registry. A checksum file from the same mutable
# release only re-checks the download, so it rolls only with `attestation` beside it.
ROLLING_INDEPENDENT_VERIFY = {"github-release-attestation", "gpg", "cargo-locked"}
# A pinned asset from these sources must say why its publisher's verification cannot replace the pin.
PINNED_RELEASE_SOURCES = {
    "github-release",
    "https-download",
    "crates",
    "git-commit",
    "installer-script",
}
INSTALLING_ASSET_SOURCES = {
    "github-release",
    "https-download",
    "crates",
    "git-commit",
    "installer-script",
    "vendored",
}
# A literal value is double-quoted without $, single-quoted, or an unquoted
# token without quotes, $, backticks, or parentheses; derived values pass.
LITERAL_VERSION_ASSIGNMENT = re.compile(
    r"""^\s*(?:readonly |declare -r |export |local )?([A-Z0-9_]*_VERSION|[a-z0-9_]*version)="""
    r"""(?:"[^"$`]*"|'[^']*'|[^\s"'$`;()]+)(?=\s|;|$)""",
    re.MULTILINE,
)


def asset_pin_values(asset: dict[str, Any]) -> list[tuple[str, Any]]:
    """Return every pin and checksum value an asset declares, with its field path."""
    values: list[tuple[str, Any]] = [] if asset.get("release") == "latest" else [("pin", asset.get("pin"))]
    sha256 = asset.get("sha256")
    if isinstance(sha256, dict):
        values.extend((f"sha256.{arch}", value) for arch, value in sha256.items())
    elif sha256 is not None:
        values.append(("sha256", sha256))
    for plugin, config in asset.get("plugins", {}).items():
        values.append((f"plugins.{plugin}.pin", config.get("pin")))
    fallback = asset.get("fallback")
    if isinstance(fallback, dict):
        values.append(("fallback.pin", fallback.get("pin")))
        if isinstance(fallback.get("sha256"), dict):
            values.extend((f"fallback.sha256.{arch}", value) for arch, value in fallback["sha256"].items())
    return values


def validate_assets(manifest: dict[str, Any]) -> None:
    """Require one complete declaration per asset and no hand-written installer versions."""
    assets = manifest.get("assets")
    if not isinstance(assets, dict) or not assets:
        fail("agent-config.yaml must declare third-party assets under assets:")
    rendered: set[tuple[str, str]] = set()
    # Keyed on the resolved real path, so symlinked aliases of one file collide.
    render_claims: dict[tuple[Path, str], tuple[str, str, str]] = {}
    for name, asset in assets.items():
        rolling = "release" in asset
        required = ("source", "upstream", "verify") if rolling else ("source", "upstream", "pin", "verify")
        missing = [key for key in required if not asset.get(key)]
        if missing:
            fail(f"assets.{name} is missing {missing}")
        if rolling:
            if asset["release"] != "latest" or asset["source"] not in ROLLING_ASSET_SOURCES:
                fail(
                    f"assets.{name}.release must be 'latest' on a {sorted(ROLLING_ASSET_SOURCES)} source, "
                    f"not {asset['release']!r} on {asset.get('source')!r}"
                )
            present = [key for key in ROLLING_ASSET_FORBIDDEN_FIELDS if key in asset]
            if present:
                fail(f"assets.{name} has release: latest and must not record {present}")
            if asset.get("reason"):
                fail(f"assets.{name} has release: latest; a reason belongs only to a pinned asset")
            if asset["verify"] not in ROLLING_INDEPENDENT_VERIFY and "attestation" not in asset:
                fail(
                    f"assets.{name} has release: latest, but verify {asset['verify']!r} checks only a file from the "
                    "same release; roll only with an attestation, a pinned-key signature or an immutable registry, "
                    "or pin it with a reason"
                )
        elif asset["source"] in PINNED_RELEASE_SOURCES and not asset.get("reason"):
            fail(f"assets.{name} keeps a pin and must give the reason its publisher's verification cannot replace it")
        if "attestation" in asset and (
            asset["attestation"] != "when-gh-authenticated" or asset["source"] != "github-release"
        ):
            fail(f"assets.{name}.attestation must be 'when-gh-authenticated' on a github-release asset")
        # Nothing runs before an independent check: a rolling asset whose attestation needs gh
        # bootstraps a reviewed fallback release where gh cannot check it first.
        fallback = asset.get("fallback")
        if rolling and "attestation" in asset:
            if (
                not isinstance(fallback, dict)
                or not fallback.get("pin")
                or not isinstance(fallback.get("sha256"), dict)
                or not fallback["sha256"]
                or not fallback.get("reason")
            ):
                fail(
                    f"assets.{name} has release: latest and attestation: when-gh-authenticated, so it must record "
                    "fallback.pin, fallback.sha256 (per platform) and fallback.reason for a host without gh"
                )
        elif fallback is not None:
            fail(f"assets.{name}.fallback belongs only to a release: latest asset with an attestation")
        allowed = ASSET_VERIFY_BY_SOURCE.get(asset["source"])
        if allowed is None:
            fail(f"assets.{name} has an unknown source: {asset['source']!r}")
        if asset["verify"] not in allowed:
            fail(f"assets.{name} verify {asset['verify']!r} is not valid for source {asset['source']!r}")
        if asset["verify"] in {"sha256", "installer-sha256"} and not asset.get("sha256"):
            fail(f"assets.{name} must record sha256 for verify {asset['verify']!r}")
        if asset["verify"] == "gpg" and not asset.get("gpg_fingerprint"):
            fail(f"assets.{name} must record gpg_fingerprint for verify 'gpg'")
        if asset["source"] in INSTALLING_ASSET_SOURCES:
            absent = [key for key in ("install_path", "installer") if not asset.get(key)]
            if absent:
                fail(f"assets.{name} installs from {asset['source']} and is missing {absent}")
        for field, value in asset_pin_values(asset):
            if not isinstance(value, str):
                fail(f"assets.{name}.{field} must be a string, not {type(value).__name__}: {value!r}")
        render = asset.get("render")
        for entry in (render if isinstance(render, list) else [render]) if render else []:
            constants = entry.get("constants") if isinstance(entry, dict) else None
            if (
                not isinstance(entry, dict)
                or not isinstance(entry.get("file"), str)
                # One canonical relative spelling per target: no "..", "./" or
                # absolute path, so conflict detection sees every file once.
                or posixpath.normpath(entry["file"]) != entry["file"]
                or entry["file"].startswith(("/", "../"))
                or entry["file"] == ".."
                or not isinstance(constants, dict)
                or not constants
                or not all(isinstance(key, str) and isinstance(value, str) for key, value in constants.items())
            ):
                fail(
                    f"assets.{name}.render entries must each be a mapping with a normalized relative file and a "
                    f"non-empty constants mapping of string to string: {entry!r}"
                )
            real = (ROOT / entry["file"]).resolve()
            for constant, field in constants.items():
                if rolling and field.split(".")[0] in ROLLING_ASSET_FORBIDDEN_FIELDS:
                    fail(f"assets.{name} has release: latest and must not render {constant} from {field}")
                rendered.add((entry["file"], constant))
                # Two entries rendering one assignment would overwrite each other.
                source = render_claims.setdefault((real, constant), (name, field, entry["file"]))
                if source[:2] != (name, field):
                    fail(
                        f"{entry['file']} {constant} is rendered from both assets.{source[0]}.{source[1]} "
                        f"(via {source[2]}) and assets.{name}.{field}; render each assignment from one field"
                    )
    # setup.sh is the bootstrap entry point; its pins render like the installers'. A shell script is one named *.sh or
    # one whose shebang runs a shell, so an extensionless script (scripts/orchestrator/hcom-seat) is scanned too.
    scanned = [
        ROOT / "setup.sh",
        *(
            path
            for root in ("install", "scripts")
            for path in sorted((ROOT / root).rglob("*"))
            if is_shell_script(path)
        ),
    ]
    for path in scanned:
        if not path.is_file():
            continue
        relative = str(path.relative_to(ROOT))
        for match in LITERAL_VERSION_ASSIGNMENT.finditer(path.read_text()):
            if (relative, match.group(1)) not in rendered:
                fail(f"{relative} hard-codes {match.group(1)}; declare it in assets: and render it into this file")


SHELL_SHEBANG = re.compile(rb"#!\s*(?:/usr/bin/env\s+(?:-S\s+)?)?(?:\S*/)?(?:ba|z|da|k)?sh(?:\s|$)")


def is_shell_script(path: Path) -> bool:
    if not path.is_file() or path.is_symlink():
        return False
    if path.suffix == ".sh":
        return True
    with path.open("rb") as handle:
        return SHELL_SHEBANG.match(handle.readline(256)) is not None


def omp_extension_providers(manifest_path: Path, manifest: dict[str, Any]) -> dict[str, str]:
    """omp.extension_providers: the model provider each extension directory registers, declared once.

    Every directory there and in omp.extensions must be one of claude.levers.extensions, the only directories a seat
    loads with -e, so a provider the manifest routes to is one a seat can reach.
    """
    omp = manifest.get("omp") if isinstance(manifest.get("omp"), dict) else {}
    providers = omp.get("extension_providers")
    if (
        not isinstance(providers, dict)
        or not providers
        or not all(isinstance(key, str) and isinstance(value, str) for key, value in providers.items())
    ):
        fail(f"{manifest_path} omp.extension_providers must map omp provider ids to extension directories")
    # Exact set: every model route omp does not provide itself, and nothing else, so a route can never lose the entry
    # that says which extension a plain launch must load for it.
    expected_routes = set(generator().OMP_MODEL_ROUTES) - set(generator().OMP_BUILTIN_ROUTES)
    if set(providers) != expected_routes:
        fail(
            f"{manifest_path} omp.extension_providers must name exactly the extension-registered model routes "
            f"{sorted(expected_routes)}: {sorted(providers)}"
        )
    extensions = omp.get("extensions", [])
    if not isinstance(extensions, list):
        fail(f"{manifest_path} omp.extensions must be a list of extension directories")
    seat_extensions = manifest.get("claude", {}).get("levers", {}).get("extensions", [])
    outside = sorted(
        {*providers.values(), *extensions} - set(seat_extensions if isinstance(seat_extensions, list) else [])
    )
    if outside:
        fail(f"{manifest_path} omp extension directories must be listed in claude.levers.extensions: {outside}")
    return providers


def validate_omp_interactive_provider(manifest_path: Path, manifest: dict[str, Any]) -> None:
    """A plain omp launch reaches the interactive model's provider only through omp.extensions.

    omp 18.11.3 findInitialModel (src/config/model-resolver.ts:2391-2407) skips a `modelRoles.default` whose
    provider no loaded extension registered and silently starts on another authenticated provider, or ends with
    `No default model selected.`.
    """
    model = manifest["model_profiles"][manifest["interactive_profile"]]["omp"]["model"]
    provider = model.split("/", 1)[0]
    providers = omp_extension_providers(manifest_path, manifest)
    if provider in generator().OMP_BUILTIN_ROUTES:
        return
    needed = providers.get(provider)
    extensions = manifest["omp"].get("extensions", [])
    if needed is None or needed not in extensions:
        fail(
            f"{manifest_path} interactive_profile omp model {model} needs {needed} in omp.extensions; "
            f"a plain omp launch skips a default model whose provider {provider} is not registered"
        )


def validate_agent_manifest() -> dict[str, Any]:
    manifest_path = ROOT / "home/dot_agents/agent-config.yaml"
    manifest = load_yaml(manifest_path)
    if manifest.get("schema_version") != 1:
        fail(f"{manifest_path} schema_version must be 1")
    # Each model profile's keys and values follow the generator's rules (scripts/generate-agent-configs.py
    # model_profiles): one implementation for both the renderer and this check.
    generator().model_profiles(manifest)
    codex_plugins = manifest.get("codex", {}).get("plugins", {})
    if codex_plugins.get("crit@mryfmo-personal-plugins", {}).get("enabled") is not True:
        fail(f"{manifest_path} must enable the Crit Codex plugin")
    claude = manifest.get("claude", {})
    profiles = manifest.get("model_profiles", {})
    required_profiles = {"express", "standard", "review", "deep", "security", "audit"}
    if set(profiles) != required_profiles:
        fail(f"{manifest_path} must define the six base profiles and no others")
    # Operator decision (2026-09-29): security runs codex gpt-6-astra high under
    # ChatGPT login; gpt-daybreak-blue-latest needs API-key auth. It audits pending
    # changes without editing them, so it is read-only like the audit profile (U70).
    security_codex = profiles["security"].get("codex", {})
    for key, expected in (("model", "gpt-6-astra"), ("model_reasoning_effort", "high"), ("sandbox_mode", "read-only")):
        if security_codex.get(key) != expected:
            fail(
                f"{manifest_path} security profile must set codex.{key}: {expected} "
                f"(operator decision 2026-09-29): {security_codex.get(key)!r}"
            )
    # Operator pin (2026-10-09, T115): the auditor is codex gpt-6-astra xhigh, read-only.
    audit_codex = profiles["audit"].get("codex", {})
    for key, expected in (
        ("model", "gpt-6-astra"),
        ("model_reasoning_effort", "xhigh"),
        ("sandbox_mode", "read-only"),
    ):
        if audit_codex.get(key) != expected:
            fail(
                f"{manifest_path} audit profile must set codex.{key}: {expected} "
                f"(operator pin): {audit_codex.get(key)!r}"
            )
    if manifest.get("interactive_profile") not in profiles:
        fail(f"{manifest_path} interactive_profile must name a defined model profile")
    # Operator pin (2026-09-27): worker claude launches carry --advisor fable. The pin read its profile from the
    # manifest's worker-profile key, standard, until U40 removed that key; it stays on the profile it
    # checked.
    advisor_profile = "standard"
    if profiles.get(advisor_profile, {}).get("claude", {}).get("advisor") != "fable":
        fail(f"{manifest_path} worker profile {advisor_profile!r} must set claude.advisor: fable (operator pin)")
    # INV-7 (operator decision 2026-10-13, plan 007 T717): the Claude review profile is the deep profile's model and
    # effort, so review independence rests on a fresh context, not a different model.
    for key in ("model", "effort"):
        if profiles["review"]["claude"].get(key) != profiles["deep"]["claude"].get(key):
            fail(f"{manifest_path} review profile claude.{key} must equal deep's (INV-7)")
    validate_omp_interactive_provider(manifest_path, manifest)
    if claude.get("model") or claude.get("effortLevel") or manifest.get("codex", {}).get("model"):
        fail(f"{manifest_path} must keep model settings in model_profiles only")
    for name, server in manifest.get("mcp_servers", {}).items():
        if server.get("enabled", False) is not False:
            fail(f"MCP server {name} must be disabled by default in the shared manifest")
        agents = server.get("agents", {})
        if agents.get("claude"):
            # Claude Code reads user-scope MCP servers from ~/.claude.json, which this repo does not manage.
            fail(f"MCP server {name} cannot target claude: add it with `claude mcp add --scope user`")
        # The generator renders MCP servers into the Codex config only (render_codex: enabled_for(server, "codex")).
        if {agent for agent, enabled in agents.items() if enabled} != {"codex"}:
            fail(f"MCP server {name} must be exposed to Codex, the one agent whose MCP config this repo renders")
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


def validate_mcp_parity(codex: dict[str, Any], manifest: dict[str, Any]) -> None:
    manifest_names = set(manifest.get("mcp_servers", {}))
    codex_names = set(codex.get("mcp_servers", {}))
    if manifest_names != codex_names:
        fail(f"MCP server names differ: manifest={sorted(manifest_names)} codex={sorted(codex_names)}")


def validate_codex_modify_script() -> None:
    path = ROOT / "home/dot_codex/modify_private_config.toml"
    if not path.exists():
        fail(f"{path} is missing")
    if path.stat().st_mode & 0o111 == 0:
        fail(f"{path} must be executable")
    text = path.read_text()
    for token in (
        "RUNTIME_PREFIXES",
        "hooks.state",
        "marketplaces",
        "tui.model_availability_nux",
        "projects",
    ):
        if token not in text:
            fail(f"{path} must preserve Codex runtime-owned table token {token!r}")


def validate_codex_profile_modify_scripts(manifest: dict[str, Any]) -> None:
    for name, profile in manifest.get("model_profiles", {}).items():
        path = ROOT / "home/dot_codex" / f"modify_private_{name}.config.toml"
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
        if profile_data.get("sandbox_mode") != profile.get("codex", {}).get("sandbox_mode"):
            fail(f"{path} must render the {name} profile sandbox_mode override")
        if profile_data.get("features", {}).get("hooks") is not True:
            fail(f"{path} must enable hooks for the {name} profile")
        if "state" not in profile_data.get("hooks", {}):
            fail(f"{path} must preserve hook trust state for the {name} profile")


def standing_rule_text(manifest: dict[str, Any], agent: str) -> str:
    """The rule sources generate-agent-configs.py renders for one audience, in manifest order."""
    section = manifest.get("standing_rules", {})
    source_dir = ROOT / section.get("source_dir", "")
    names = [name for name, audience in section.get("rules", {}).items() if agent in audience]
    if not names:
        fail(f"standing_rules declares no rule for {agent}")
    return "\n".join((source_dir / f"{name}.md").read_text() for name in names)


def validate_crit_install_assets(manifest: dict[str, Any]) -> None:
    updater = (ROOT / "scripts/update-agent-assets.sh").read_text()
    for token in (
        "crit-darwin-amd64",
        "crit-darwin-arm64",
        "crit@crit",
        "claude plugin enable",
        "claude_crit_plugin_is_enabled",
        "if claude_crit_plugin_is_enabled; then",
        "crit install codex-plugin --force",
        "tomasz-tomczyk/crit",
    ):
        if token not in updater:
            fail(f"scripts/update-agent-assets.sh must manage Crit asset token {token!r}")
    codex_agents = standing_rule_text(manifest, "codex")
    for token in (
        "Crit plugin",
        "CRIT_PLAN_REVIEW=off",
    ):
        if token not in codex_agents:
            fail(f"the Codex standing rules (~/.codex/AGENTS.md) must document Codex Crit rule token {token!r}")


def validate_ponytail_assets(manifest: dict[str, Any], codex: dict[str, Any]) -> None:
    updater = (ROOT / "scripts/update-agent-assets.sh").read_text()
    for token in (
        "DietrichGebert/ponytail",
        "ponytail@ponytail",
        "CODEX_PONYTAIL_MARKETPLACE_SOURCE",
        "codex_marketplace_has_source",
        'codex plugin marketplace upgrade "${CODEX_PONYTAIL_MARKETPLACE_NAME}"',
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
    if (
        codex.get("marketplaces", {}).get("ponytail", {}).get("source")
        != "https://github.com/DietrichGebert/ponytail.git"
    ):
        fail("home/.chezmoitemplates/codex-config-managed.toml must render the Ponytail Codex marketplace source")
    hook_state = codex.get("hooks", {}).get("state", {})
    for key in (
        "ponytail@ponytail:hooks/claude-codex-hooks.json:session_start:0:0",
        "ponytail@ponytail:hooks/claude-codex-hooks.json:user_prompt_submit:0:0",
        "ponytail@ponytail:hooks/claude-codex-hooks.json:subagent_start:0:0",
    ):
        if not hook_state.get(key, {}).get("trusted_hash", "").startswith("sha256:"):
            fail(f"home/.chezmoitemplates/codex-config-managed.toml must render trusted Ponytail hook state for {key}")

    codex_agents = standing_rule_text(manifest, "codex")
    for token in ("Ponytail", "ponytail@ponytail", "YAGNI", "standard library"):
        if token not in codex_agents:
            fail(f"the Codex standing rules (~/.codex/AGENTS.md) must document Ponytail token {token!r}")

    claude_rule = ROOT / "home/dot_config/claude/rules/ponytail.md"
    if not claude_rule.exists():
        fail("Claude Code Ponytail rule is missing")
    claude_rule_text = claude_rule.read_text()
    for token in (
        "Ponytail",
        "ponytail@ponytail",
        "YAGNI",
        "standard library",
        "native platform",
    ):
        if token not in claude_rule_text:
            fail(f"{claude_rule} must document Ponytail token {token!r}")

    if "claude" not in manifest.get("standing_rules", {}).get("rules", {}).get("ponytail", []):
        fail("standing_rules.rules.ponytail must reach claude")

    readme = (ROOT / "README.md").read_text()
    for token in (
        "Ponytail",
        "DietrichGebert/ponytail",
        "ponytail@ponytail",
        "review and trust",
    ):
        if token not in readme:
            fail(f"README.md must document Ponytail lifecycle token {token!r}")


def validate_understand_anything_assets(manifest: dict[str, Any]) -> None:
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

    codex_agents = standing_rule_text(manifest, "codex")
    for token in (
        "Understand-Anything",
        "$understand",
        "knowledge-graph.json",
        ".ua/intermediate/",
        ".ua/diff-overlay.json",
    ):
        if token not in codex_agents:
            fail(f"the Codex standing rules (~/.codex/AGENTS.md) must document Understand-Anything token {token!r}")

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

    if "claude" not in manifest.get("standing_rules", {}).get("rules", {}).get("understand-anything", []):
        fail("standing_rules.rules.understand-anything must reach claude")

    readme = (ROOT / "README.md").read_text()
    for token in (
        "Understand-Anything",
        "Egonex-AI/Understand-Anything",
        "understand-anything@understand-anything",
        "version-matched Claude release artifact",
    ):
        if token not in readme:
            fail(f"README.md must document Understand-Anything lifecycle token {token!r}")


def validate_permgate_policy(policy_path: Path) -> None:
    policy = json.loads(policy_path.read_text())
    if not isinstance(policy, dict):
        fail(f"{policy_path} must be a JSON object")
    if set(policy) != {"schema_version", "allow_patterns", "deny_patterns"}:
        fail(f"{policy_path} must hold only schema_version, allow_patterns and deny_patterns")
    if policy["schema_version"] != 3:
        fail(f"{policy_path} must declare schema_version 3")
    for key in ("allow_patterns", "deny_patterns"):
        patterns = policy[key]
        if not isinstance(patterns, list) or not all(
            isinstance(pattern, dict) and isinstance(pattern.get("tool"), str) and isinstance(pattern.get("regex"), str)
            for pattern in patterns
        ):
            fail(f"{policy_path} {key} must be a list of objects with string tool and regex")


def validate_model_profile_assets(manifest: dict[str, Any]) -> None:
    codex_path = ROOT / manifest["codex"]["config_path"]
    codex_text = render_template_text(codex_path)
    if "hooks.PermissionRequest" not in codex_text or "permgate codex" not in codex_text:
        fail(f"{codex_path} must wire the permgate PermissionRequest hook")
    if "ccgate" in codex_text:
        fail(f"{codex_path} must not wire ccgate")

    claude_settings_path = ROOT / manifest["claude"]["settings_path"]
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
    validate_permgate_policy(policy_path)
    permgate_text = permgate_path.read_text()
    for token in (
        "--no-cache",
        "PERMGATE_INNER",
        "decisions.jsonl",
    ):
        if token not in permgate_text:
            fail(f"{permgate_path} must contain {token!r}")

    for stale in (
        ROOT / "home/dot_codex/ccgate.jsonnet",
        ROOT / "home/dot_claude/ccgate.jsonnet",
    ):
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
    for token in (
        "MODEL_PROFILE_INTERACTIVE",
        "MODEL_PROFILE_STANDARD_CODEX_ARGS",
        "MODEL_PROFILE_EXPRESS_CLAUDE_ARGS",
    ):
        if token not in env_text:
            fail(f"{env_path} must define {token}")

    express_agent = ROOT / "home/dot_claude/agents/express-explorer.md"
    if not express_agent.exists() or "model:" not in express_agent.read_text():
        fail(f"{express_agent} must define the low-cost explorer subagent")

    codex_agents = standing_rule_text(manifest, "codex")
    for token in ("model_profiles", "--profile standard", "model-profiles.env"):
        if token not in codex_agents:
            fail(f"the Codex standing rules (~/.codex/AGENTS.md) must document model profile token {token!r}")

    claude_rule = ROOT / "home/dot_config/claude/rules/model-selection.md"
    if not claude_rule.exists():
        fail("Claude Code model-selection rule is missing")
    claude_rule_text = claude_rule.read_text()
    for token in ("model_profiles", "express-explorer", "review"):
        if token not in claude_rule_text:
            fail(f"{claude_rule} must document model profile token {token!r}")


GIT_SIGNING_KEYS = ("user.signingkey", "gpg.format", "commit.gpgsign")
# An [include] or [includeIf] section pulls in config the render check never sees.
GIT_INCLUDE_SECTION = re.compile(r"^\s*\[\s*include(if)?\b", re.IGNORECASE | re.MULTILINE)


def git_config_read(git: str, config_file: Path, *args: str) -> subprocess.CompletedProcess:
    """Run `git config --file <config_file> <args>` with no system or global config in play."""
    try:
        return subprocess.run(
            [git, "config", "--file", str(config_file), *args],
            env={
                "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                "HOME": str(config_file.parent),
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
            },
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        fail(f"git config could not read the rendered {config_file.name}: {error}")


def render_git_config(template: Path, with_key: bool) -> tuple[dict[str, list[str]], str, str | None]:
    """Render the git config template with chezmoi in a scratch HOME and read the output with git itself.

    The scratch HOME holds `~/.ssh/id_ed25519.pub` only when `with_key` is set, so the two renders
    show what the template does on a host with and without the signing key. Git parses the render
    (`git config --file <render> --list`), so section and key names are matched the way git matches
    them (case-insensitively). Returns every entry by canonical name, the scratch HOME, and
    commit.gpgsign read as a git boolean (None when unset).
    """
    relative = template.relative_to(ROOT)
    chezmoi = os.environ.get("DOTFILES_CHEZMOI") or shutil.which("chezmoi")
    if not chezmoi:
        fail(f"chezmoi is required to render {relative}; install it or set DOTFILES_CHEZMOI")
    git = shutil.which("git")
    if not git:
        fail(f"git is required to read the rendered {relative}")
    with tempfile.TemporaryDirectory(prefix="validate-git-config-") as temporary:
        home = Path(temporary)
        if with_key:
            (home / ".ssh").mkdir()
            (home / ".ssh/id_ed25519.pub").write_text("ssh-ed25519 AAAA validate-agent-assets\n")
        config = home / "chezmoi.toml"
        config.write_text('[data]\nemail = "validate@example.invalid"\n')
        try:
            result = subprocess.run(
                [
                    chezmoi,
                    "execute-template",
                    "--config",
                    str(config),
                    "--persistent-state",
                    str(home / "chezmoistate.boltdb"),
                    "--source",
                    str(ROOT / "home"),
                    "--destination",
                    str(home),
                    "--file",
                    str(template),
                ],
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(home)},
                capture_output=True,
                text=True,
                check=False,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            fail(f"chezmoi could not render {relative}: {error}")
        if result.returncode != 0:
            fail(f"chezmoi could not render {relative}: {result.stderr.strip()}")
        rendered = home / "gitconfig"
        rendered.write_text(result.stdout)
        listing = git_config_read(git, rendered, "--null", "--list")
        if listing.returncode != 0:
            fail(f"{relative} does not render to a valid git config: {listing.stderr.strip()}")
        entries: dict[str, list[str]] = {}
        for entry in listing.stdout.split("\0"):
            if entry:
                name, _, value = entry.partition("\n")
                entries.setdefault(name, []).append(value)
        gpgsign = None
        if "commit.gpgsign" in entries:
            boolean = git_config_read(git, rendered, "--type=bool", "--get-all", "commit.gpgsign")
            if boolean.returncode != 0:
                fail(f"{relative} renders a commit.gpgsign git cannot read as a boolean: {boolean.stderr.strip()}")
            gpgsign = boolean.stdout.strip()
        return entries, str(home), gpgsign


def validate_git_config() -> None:
    """Validate managed Git commit signing by rendering the template on a host with and without the key.

    With `~/.ssh/id_ed25519.pub` present the rendered config signs commits with that key over SSH;
    without it none of the three signing settings is rendered, so commits are unsigned instead of failing.
    Git reads each render, and the template may carry no include directive the check could not follow.
    """
    path = ROOT / "home/dot_config/git/config.tmpl"
    relative = path.relative_to(ROOT)
    text = path.read_text()
    if "signingkey = D55D775A7951407C" in text:
        fail(f"{relative} must not reference the removed GPG signing key")
    if GIT_INCLUDE_SECTION.search(text):
        fail(f"{relative} must not use [include] or [includeIf]: the render check cannot follow them")
    for with_key in (True, False):
        entries, home, gpgsign = render_git_config(path, with_key=with_key)
        state = "with the signing key present" if with_key else "without the signing key"
        includes = sorted(name for name in entries if name.startswith(("include.", "includeif.")))
        if includes:
            fail(f"{relative} rendered {state} must not include other config: {', '.join(includes)}")
        if not with_key:
            for name in GIT_SIGNING_KEYS:
                if name in entries:
                    fail(f"{relative} rendered {state} must not set {name}")
            continue
        expected = {
            "user.signingkey": f"{home}/.ssh/id_ed25519.pub",
            "gpg.format": "ssh",
        }
        for name in GIT_SIGNING_KEYS:
            if len(entries.get(name, [])) != 1:
                fail(f"{relative} rendered {state} must set {name} exactly once, not {entries.get(name, [])!r}")
        for name, expected_value in expected.items():
            if entries[name][0] != expected_value:
                fail(f"{relative} rendered {state} must set {name} = {expected_value}, not {entries[name][0]!r}")
        if gpgsign != "true":
            fail(f"{relative} rendered {state} must set commit.gpgsign = true, not {gpgsign!r}")
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


@cache
def gitignored_paths(root: Path) -> frozenset[Path]:
    """The paths git ignores under root (ignored directories collapsed); none outside a work tree."""
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--others", "--ignored", "--exclude-standard", "--directory"],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return frozenset()
    # Filesystem decoding, as Path uses: git emits a non-UTF-8 file name as raw bytes.
    return frozenset(root / os.fsdecode(name).rstrip("/") for name in result.stdout.split(b"\0") if name)


def is_gitignored(path: Path) -> bool:
    """Local state such as the CompactionDB ledger is never committed, so the repository-wide scans skip it."""
    ignored = gitignored_paths(ROOT)
    return any(candidate in ignored for candidate in (path, *path.parents))


@cache
def is_nested_git_tree(directory: Path) -> bool:
    """Check directory ancestors for a Git boundary, excluding ROOT itself."""
    if directory == ROOT:
        return False
    return (directory / ".git").exists() or is_nested_git_tree(directory.parent)


def validate_no_removed_claude_skill() -> None:
    removed_skill = "high-impact" + "-journal-publishing"
    matches = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "site", "__pycache__"} for part in path.parts):
            continue
        if is_nested_git_tree(path.parent) or is_gitignored(path):
            continue
        if removed_skill in path.read_text(errors="ignore"):
            matches.append(path)
    if matches:
        fail("removed Claude skill references remain: " + ", ".join(str(p.relative_to(ROOT)) for p in matches[:10]))


def read_scannable_text(path: Path) -> str | None:
    data = path.read_bytes()
    offset = data.find(b"\0")
    # Orchestration evidence is UTF-8 text; a NUL or a UTF-16 encoding there
    # would hide it from the scan, so both fail before any decode.
    if path.relative_to(ROOT).parts[:1] == (".orchestration",):
        if offset != -1:
            fail(f"{path.relative_to(ROOT)} holds a NUL byte at offset {offset}; evidence must be UTF-8 text")
        if data.startswith((b"\xff\xfe", b"\xfe\xff")):
            fail(f"{path.relative_to(ROOT)} is UTF-16; evidence must be UTF-8 text")
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        try:
            return data.decode("utf-16")
        except UnicodeDecodeError:
            return None
    if offset != -1:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


ALLOWED_SECRET_PLACEHOLDERS = frozenset(
    {
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "FIGMA_OAUTH_TOKEN",
    }
)
SECRET_MASK = "<redacted:secret-pattern>"
HOME_MASK = "~"


@cache
def compiled_home_path_pattern(root: Path, home: str) -> re.Pattern[str]:
    repo_home = root / "home"
    entries = sorted(entry.name for entry in repo_home.iterdir()) if repo_home.is_dir() else []
    not_repo_path = "".join(f"(?!{re.escape(name)}(?![\\w.-]))" for name in entries)
    # Not glued to a word (`dotfiles/home/x`), except right after a namespace root (`/proc/self/root/home/x`).
    boundary = r"(?:(?<![\w.~-])|(?<=/root))"
    forms = [
        # GitHub-hosted runner homes match anywhere, like a multi-segment `$HOME`, so a workstation
        # rewrites a glued runner path (`..F/home/runner/.ssh/id` from an Actions log) as a runner flags it.
        r"/(?:home|Users)/runner",
        # Any Unicode account name (`/home/éclair`), also under `/var/home` (Fedora Atomic) and `/export/home`.
        rf"{boundary}(?:(?:/var|/export)?/home|/Users)/{not_repo_path}[\w][\w.-]*",
        # macOS root's home, any child (`/var/root/Library/...`), also through its physical `/private/var`.
        rf"{boundary}(?:/private)?/var/root",
        # ponytail: plain `/root` only bare or as `/root/.<dir>` (where credentials live); a Codex
        # sub-agent path such as `/root/t97_evidence_review` stays. Widen when evidence quotes other
        # `/root/<dir>` paths.
        rf"{boundary}/root(?=/\.|(?!/))",
    ]
    # Root's `/root` is covered by its restricted form above; adding it here would bypass that restriction.
    if home and home != "/root":
        # A one-segment home is also a path component (`/proc/self/root`), so it keeps the boundary.
        forms.insert(0, re.escape(home) if home.count("/") > 1 else boundary + re.escape(home))
    return re.compile(rf"(?:{'|'.join(forms)})(?![\w.-])")


def home_path_pattern() -> re.Pattern[str]:
    """A home directory, as the `.orchestration` scan flags it and the masker rewrites it.

    The machine-independent forms are `/home/<user>`, `/Users/<user>`, root's
    `/root`, and macOS `/var/root` and `/private/var/root`. A segment that names a
    top-level entry of the repository's `home/` tree (`dot_config`,
    `.chezmoiscripts`, ...) is a repository path, not a user, and a path glued to
    a word character (`dotfiles/home/x`, a temporary `.../home/worker`) never
    matches, except beneath a namespace root (`/proc/self/root/home/<user>`). CI
    flags these forms the same way on every machine.

    The running user's `$HOME` is added as a machine-dependent backstop: a
    multi-segment home (`/srv/operator`) matches anywhere, and a one-segment home
    (`/root`) keeps the boundary, so `/proc/self/root` stays intact. That part
    flags only on the workstation whose home it is, which is where the evidence is
    written and masked.
    """
    return compiled_home_path_pattern(ROOT, os.path.expanduser("~").rstrip("/"))


def mask_home_paths(text: str) -> tuple[str, int]:
    """Normalise every home_path_pattern() match to `~`, so masked evidence always passes the scan."""
    return home_path_pattern().subn(HOME_MASK, text)


def strip_allowed_secret_placeholders(text: str) -> str:
    for placeholder in ALLOWED_SECRET_PLACEHOLDERS:
        text = text.replace(placeholder, "")
    return text


def mask_secret_matches(text: str) -> tuple[str, int]:
    """Replace the SECRET_PATTERN matches the committed-secret scan would flag, and normalise home paths.

    Mirrors validate_no_obvious_secrets(): allowed placeholders are stripped
    before matching, so a line is masked only when its stripped form still
    matches and every other line is kept byte for byte. A final whole-text
    pass covers a match that spans lines, so masked text always passes the
    scan. Home directory prefixes then become `~` (mask_home_paths), which
    the scan requires of `.orchestration` evidence.
    """
    count = 0
    lines = []
    for line in text.splitlines(keepends=True):
        sanitized = strip_allowed_secret_placeholders(line)
        if SECRET_PATTERN.search(sanitized):
            sanitized, matches = SECRET_PATTERN.subn(SECRET_MASK, sanitized)
            count += matches
            lines.append(sanitized)
        else:
            lines.append(line)
    masked = "".join(lines)
    if SECRET_PATTERN.search(strip_allowed_secret_placeholders(masked)):
        masked, matches = SECRET_PATTERN.subn(SECRET_MASK, strip_allowed_secret_placeholders(masked))
        count += matches
    masked, homes = mask_home_paths(masked)
    return masked, count + homes


def mask_json_strings(value: Any) -> tuple[Any, int]:
    """Mask every string in a parsed JSON value, so the document stays parseable."""
    if isinstance(value, str):
        return mask_secret_matches(value)
    if isinstance(value, list):
        pairs = [mask_json_strings(item) for item in value]
        return [item for item, _ in pairs], sum(count for _, count in pairs)
    if isinstance(value, dict):
        return mask_members(value.items())
    return value, 0


class MaskedKeyCollision(Exception):
    """Two distinct object keys mask to one name, so masking would drop a member."""


def mask_members(pairs: Iterable[tuple[str, Any]]) -> tuple[dict[str, Any], int]:
    """Mask an object's keys and values; a repeated original key keeps its last value."""
    masked: dict[str, Any] = {}
    originals: dict[str, str] = {}
    count = 0
    for key, item in pairs:
        masked_key, key_count = mask_secret_matches(key)
        if originals.setdefault(masked_key, key) != key:
            raise MaskedKeyCollision(f"keys {originals[masked_key]!r} and {key!r} both mask to {masked_key!r}")
        masked[masked_key], item_count = mask_json_strings(item)
        count += key_count + item_count
    return masked, count


def json_strings(text: str) -> list[str] | None:
    """Every key and string value of a JSON document, or None when text is not JSON.

    Objects are read as pair tuples, so a duplicate key's earlier value is kept.
    """
    try:
        document = json.loads(text, object_pairs_hook=tuple)
    except (ValueError, RecursionError):
        return None
    strings: list[str] = []
    stack = [document]
    while stack:
        value = stack.pop()
        if isinstance(value, str):
            strings.append(value)
        elif isinstance(value, list):
            stack.extend(value)
        elif isinstance(value, tuple):
            for key, item in value:
                strings.append(key)
                stack.append(item)
    return strings


def mask_secrets(paths: list[str]) -> int:
    """Mask SECRET_PATTERN matches and home paths in place (evidence); 2 if any file is missing, 1 on a key collision.

    A file whose whole text parses as JSON, whatever its suffix (the test
    json_strings() applies for the scan), is masked per key and string value
    and rewritten as `json.dumps(indent=2, ensure_ascii=False)`, so a saved body equals
    mask_secret_matches() of the collected one; any other file is masked as text. Every member is
    masked as it is parsed, and an earlier duplicate member is then dropped, as
    json.loads (and so the gate) reads the file.
    """
    missing = [name for name in paths if not Path(name).is_file()]
    if missing:
        for name in missing:
            print(f"--mask-secrets: no such file: {name}", file=sys.stderr)
        return 2
    status = 0
    for name in paths:
        path = Path(name)
        # Bytes in and out: universal newlines would turn a carriage return in
        # pasted terminal output into a newline and change evidence beyond the masks.
        text = path.read_bytes().decode()
        member_count = 0

        def mask_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            nonlocal member_count
            masked, count = mask_members(pairs)
            member_count += count
            return masked

        try:
            document = json.loads(text, object_pairs_hook=mask_object)
        except (ValueError, RecursionError):
            document = None
        except MaskedKeyCollision as error:
            print(f"--mask-secrets: {path}: {error}; rename one key, the file is unchanged", file=sys.stderr)
            status = 1
            continue
        if document is None:
            masked, count = mask_secret_matches(text)
        else:
            # Objects are already masked; this pass covers strings outside any object.
            document, count = mask_json_strings(document)
            count += member_count
            masked = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
        if count:
            path.write_bytes(masked.encode())
        print(f"masked {count} match(es) in {path}")
    return status


def validate_no_obvious_secrets() -> None:
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
        if is_nested_git_tree(path.parent) or is_gitignored(path):
            continue
        if path.relative_to(ROOT) in compactiondb_dummy_secret_fixtures:
            continue
        text = read_scannable_text(path)
        if text is None:
            continue
        # A JSON document is scanned per key and string value, so a match never
        # spans JSON syntax between two fields; any other text is scanned whole.
        strings = json_strings(text) or [text]
        if any(SECRET_PATTERN.search(strip_allowed_secret_placeholders(s)) for s in strings):
            fail(f"possible committed secret in {path.relative_to(ROOT)}")
        # Decoded JSON strings too: a JSON writer may escape the slashes (`\/home\/...`).
        if path.relative_to(ROOT).parts[:1] == (".orchestration",) and any(
            home_path_pattern().search(s) for s in (text, *strings)
        ):
            fail(
                f"{path.relative_to(ROOT)} names a home directory; normalise it with "
                "`uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`"
            )


def validate_compactiondb_project_copy() -> None:
    """The project's CompactionDB runtime and hook scripts must be byte-identical to the vendor tree."""
    vendor = ROOT / "vendor/compactiondb/.claude"
    if not vendor.is_dir():
        return
    project = ROOT / ".claude"
    pairs: dict[str, tuple[Path | None, Path | None]] = {}
    for base, files in (
        (vendor, [*(vendor / "contextdb/contextdb").rglob("*"), *(vendor / "hooks").glob("contextdb_*.py")]),
        (project, [*(project / "contextdb/contextdb").rglob("*"), *(project / "hooks").glob("contextdb_*.py")]),
    ):
        for path in files:
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            relative = str(path.relative_to(base))
            vendor_path, project_path = pairs.get(relative, (None, None))
            pairs[relative] = (path, project_path) if base == vendor else (vendor_path, path)
    for relative, (vendor_path, project_path) in sorted(pairs.items()):
        if vendor_path is None or project_path is None or vendor_path.read_bytes() != project_path.read_bytes():
            fail(
                f".claude/{relative} differs from vendor/compactiondb/.claude/{relative}; "
                "refresh the project copy with vendor/compactiondb/install.py --project ."
            )


def validate_repo_claude_settings_portable() -> None:
    """Hook commands committed in the repo's own .claude/settings.json must not pin one machine's home."""
    settings_path = ROOT / ".claude/settings.json"
    if not settings_path.exists():
        return
    data = json.loads(settings_path.read_text())
    for event, groups in data.get("hooks", {}).items():
        for group in groups:
            for handler in group.get("hooks", []):
                command = str(handler.get("command") or "")
                if command.startswith(("/Users/", "/home/")):
                    fail(f"{settings_path} hook {event} must not hard-code a machine-specific home path: {command}")


def main() -> None:
    manifest = validate_agent_manifest()
    validate_assets(manifest)
    validate_generated_agent_configs()
    validate_hook_composition()
    validate_skills()
    validate_skill_audience(manifest)
    validate_manifest_home_paths()
    validate_claude_settings(manifest)
    validate_omp_policies(manifest)
    validate_repo_claude_settings_portable()
    validate_compactiondb_project_copy()
    validate_codex_plugins(manifest)
    validate_codex_modify_script()
    codex = validate_codex_config(manifest)
    validate_mcp_parity(codex, manifest)
    validate_crit_install_assets(manifest)
    validate_ponytail_assets(manifest, codex)
    validate_understand_anything_assets(manifest)
    validate_model_profile_assets(manifest)
    validate_git_config()
    validate_no_removed_claude_skill()
    validate_no_obvious_secrets()
    print("agent asset validation ok")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--mask-secrets"]:
        raise SystemExit(mask_secrets(sys.argv[2:]))
    main()
