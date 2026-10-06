#!/usr/bin/env python3
"""Check whether active HOME agent runtime files match this chezmoi source tree.

This script is intentionally read-only. Run it after `chezmoi apply` to prove that
Codex, Claude Code, MCP, hooks, plugins, and shared skills are actually
using the generated source state.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import stat
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "home"
HOME = Path.home()
CHEZMOI_SOURCE_PREFIXES = ("executable_", "private_")
AGMSG_RUNTIME_IGNORES = (
    Path("agmsg/.agmsg"),
    # agmsg-orchestration permits separate stores such as db-flue-pi.
    Path("agmsg/db"),
    Path("agmsg/run"),
    Path("agmsg/teams"),
)
AGMSG_LEGACY_RUNTIME_FILES = {
    Path("agmsg/messages.db"),
    Path("agmsg/messages.db-shm"),
    Path("agmsg/messages.db-wal"),
}
# backups/ holds update_agmsg's pre-install state copies (agmsg-state-<UTC>).
AGENT_ROOT_ALLOWLIST = {"backups", "compactiondb", "db", "run", "teams", "worklog"}
UNDERSTAND_SKILL_ALLOWLIST = {
    "understand",
    "understand-chat",
    "understand-dashboard",
    "understand-diff",
    "understand-domain",
    "understand-explain",
    "understand-figma",
    "understand-knowledge",
    "understand-onboard",
}
# Codex-side Crit skills are installed by update-agent-assets.sh's
# update_codex_crit, not rendered from the chezmoi source tree.
CRIT_PLUGIN_SKILLS = {"crit", "crit-cli", "crit-story"}
ASSET_STEP_FUNCTIONS = {
    "ensure_crit_cli",
    "ensure_herdr_integrations",
    "ensure_mise_npm_agent_cli",
    "update_claude_crit",
    "update_claude_ponytail",
    "update_claude_superpowers",
    "update_claude_understand_anything",
    "update_codex_crit",
    "update_codex_ponytail",
    "update_codex_superpowers",
    "update_codex_understand_anything",
    "update_compactiondb",
    "update_terminal_browser",
    "update_terminal_code",
}
MISE_STEP_IDENTITIES = {
    "claude": "npm:@anthropic-ai/claude-code",
    "codex": "npm:@openai/codex",
}
UPDATER_SOURCE_COMMAND = 'source "$1"; export PATH="$HOME/.local/share/mise/shims:$PATH"; shift; "$@"'
CHEZMOI_APPLY_COMMAND = ("chezmoi", "apply", "--force")
MODE_ONLY_DIFF = re.compile(r"\Adiff --git .+\nold mode [0-7]+\nnew mode [0-7]+\n?\Z")


class RepairAction(NamedTuple):
    category: str
    target: Path
    command: tuple[str, ...]


class AssetFinding(NamedTuple):
    step: str
    missing_paths: tuple[Path, ...]
    entry: dict[str, object]


def render_template(path: Path) -> str:
    text = path.read_text()
    # This repository uses .chezmoiroot=home, so .chezmoi.sourceDir resolves to
    # the chezmoi source root that contains dot_agents/, dot_codex/, etc.
    text = text.replace("{{ .chezmoi.sourceDir }}", str(SOURCE_ROOT))
    text = re.sub(r"\{\{/\*.*?\*/\}\}", "", text, flags=re.DOTALL)
    return text


def same_text(source: Path, target: Path, template: bool = False) -> bool:
    if not target.exists():
        return False
    expected = render_template(source) if template else source.read_text()
    return target.read_text() == expected


def same_modified(source: Path, target: Path, json_target: bool = False) -> bool:
    if not target.exists():
        return False
    current = target.read_text()
    env = os.environ.copy()
    env["CHEZMOI_SOURCE_DIR"] = str(SOURCE_ROOT)
    result = subprocess.run(
        [str(source)],
        input=current,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        check=False,
    )
    if result.returncode != 0:
        return False
    if json_target:
        try:
            return json.loads(result.stdout) == json.loads(current)
        except json.JSONDecodeError:
            return False
    return result.stdout == current


def is_ignored_runtime_path(rel: Path) -> bool:
    return rel in AGMSG_LEGACY_RUNTIME_FILES or any(
        rel == ignored or ignored in rel.parents or (ignored == Path("agmsg/db") and str(rel).startswith("agmsg/db-"))
        for ignored in AGMSG_RUNTIME_IGNORES
    )


def deployed_relative_path(source_rel: Path) -> Path:
    name = source_rel.name
    for prefix in CHEZMOI_SOURCE_PREFIXES:
        if name.startswith(prefix):
            return source_rel.with_name(name.removeprefix(prefix))
    return source_rel


def source_files(root: Path) -> dict[Path, Path]:
    return {
        deployed_relative_path(path.relative_to(root)): path
        for path in sorted(root.rglob("*"))
        if path.is_file() and not is_ignored_runtime_path(deployed_relative_path(path.relative_to(root)))
    }


def applied_files(root: Path) -> set[Path]:
    if not root.exists():
        return set()
    return {
        path.relative_to(root)
        for path in sorted(root.rglob("*"))
        if (path.is_file() or path.is_symlink()) and not is_ignored_runtime_path(path.relative_to(root))
    }


def expects_executable(source: Path) -> bool:
    return source.name.startswith("executable_")


def is_warning(message: str) -> bool:
    return message.startswith("WARN: ")


def is_info(message: str) -> bool:
    """A report line that is neither a failure nor a warning."""
    return message.startswith("found: ")


def chezmoi_drift_warnings() -> list[str]:
    """Classify managed-target drift without changing the destination state."""
    try:
        status_result = subprocess.run(
            ["chezmoi", "--no-pager", "status"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        return [f"WARN: unable to inspect chezmoi drift: {error}"]
    if status_result.returncode != 0:
        detail = status_result.stderr.strip() or f"exit {status_result.returncode}"
        return [f"WARN: unable to inspect chezmoi drift: {detail}"]

    warnings: list[str] = []
    for line in status_result.stdout.splitlines():
        if len(line) < 4:
            continue
        status, target = line[:2], line[3:]
        target_path = Path(target)
        if not target_path.is_absolute():
            target_path = HOME / target_path
        diff_result = subprocess.run(
            ["chezmoi", "--no-pager", "diff", "--", str(target_path)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if diff_result.returncode == 0 and MODE_ONLY_DIFF.fullmatch(diff_result.stdout):
            hint = "permission divergence (mode-only)"
        elif status == " M":
            hint = "unapplied source update"
        elif status == "MM":
            hint = "two-sided drift"
        else:
            hint = "managed target drift"
        warnings.append(f"WARN: chezmoi drift {status} {target}: {hint}")
    return warnings


def expected_claude_skill_targets() -> dict[Path, str]:
    """Return applied Claude skill relative paths and their expected file content."""
    outputs: dict[Path, str] = {}
    source_root = SOURCE_ROOT / "dot_claude/skills"
    for template in sorted(source_root.rglob("symlink_*.tmpl")):
        rel = template.relative_to(source_root)
        applied_name = template.name.removeprefix("symlink_").removesuffix(".tmpl")
        applied_rel = rel.with_name(applied_name)
        linked_source_text = render_template(template).strip()
        linked_source = Path(linked_source_text)
        if linked_source.exists():
            outputs[applied_rel] = linked_source.read_text()
        else:
            outputs[applied_rel] = f"__BROKEN_EXPECTED_LINK__:{linked_source_text}"
    return outputs


def terminal_browser_receipt_paths(home: Path | None = None) -> set[Path]:
    """Return symlink paths recorded by the terminal-browser installer receipt."""
    home = HOME if home is None else home
    receipt = home / ".local/state/terminal-browser/skills.links"
    try:
        lines = receipt.read_text().splitlines()
    except OSError:
        return set()
    return {normalized_path(Path(line)) for line in lines if line.strip()}


def compare_tree_contents(
    label: str,
    expected: dict[Path, str],
    target_root: Path,
    expected_sources: dict[Path, Path] | None = None,
    warn_unmanaged_top_level: bool = False,
    ignored_paths: set[Path] | None = None,
) -> list[str]:
    failures: list[str] = []
    actual = applied_files(target_root)
    if ignored_paths:
        actual = {
            rel for rel in actual if not any(paths_overlap(target_root / rel, ignored) for ignored in ignored_paths)
        }
    expected_rels = set(expected)
    if warn_unmanaged_top_level:
        managed_top_levels = {rel.parts[0] for rel in expected_rels if rel.parts}
        unmanaged_top_levels = sorted(
            {rel.parts[0] for rel in actual if rel.parts and rel.parts[0] not in managed_top_levels}
        )
        for top_level in unmanaged_top_levels:
            failures.append(f"WARN: unmanaged skill dir: {target_root / top_level}")
        actual = {rel for rel in actual if rel.parts and rel.parts[0] in managed_top_levels}
    missing = sorted(expected_rels - actual)
    extra = sorted(actual - expected_rels)
    if missing:
        failures.append(f"{label} is missing files: {', '.join(str(path) for path in missing[:20])}")
    if extra:
        failures.append(f"{label} has unexpected files: {', '.join(str(path) for path in extra[:20])}")
    for rel in sorted(expected_rels & actual):
        target = target_root / rel
        try:
            actual_text = target.read_text()
        except OSError as error:
            failures.append(f"{label} cannot read {target}: {error}")
            continue
        if actual_text != expected[rel]:
            failures.append(f"{label} differs: {target}")
        source = expected_sources.get(rel) if expected_sources is not None else None
        if source is not None and expects_executable(source) and not target.stat().st_mode & stat.S_IXUSR:
            failures.append(f"{label} is not executable: {target}")
    return failures


def compare_shared_skills() -> list[str]:
    source_root = SOURCE_ROOT / "dot_agents/skills"
    target_root = HOME / ".agents/skills"
    if not target_root.exists():
        return ["shared skill directory is missing: ~/.agents/skills"]
    expected_sources = source_files(source_root)
    expected = {rel: path.read_text() for rel, path in expected_sources.items()}
    return compare_tree_contents(
        "shared skill directory",
        expected,
        target_root,
        expected_sources,
        warn_unmanaged_top_level=True,
    )


def compare_claude_skills() -> list[str]:
    target_root = HOME / ".claude/skills"
    if not target_root.exists():
        return ["Claude shared-skill symlink tree is missing: ~/.claude/skills"]
    return compare_tree_contents(
        "Claude shared-skill tree",
        expected_claude_skill_targets(),
        target_root,
        # Cowork syncs its own skills into this subtree; chezmoi does not own it.
        ignored_paths=terminal_browser_receipt_paths() | {HOME / ".claude/skills/synced"},
    )


def check_executable_hook(source: Path, target: Path, label: str) -> list[str]:
    failures: list[str] = []
    if not same_text(source, target):
        failures.append(f"{label} differs or is missing: {target}")
        return failures
    mode = target.stat().st_mode
    if not mode & stat.S_IXUSR:
        failures.append(f"{label} is not executable: {target}")
    return failures


def normalized_path(path: Path) -> Path:
    return Path(os.path.abspath(os.path.normpath(path)))


def paths_overlap(left: Path, right: Path) -> bool:
    left = normalized_path(left)
    right = normalized_path(right)
    return left == right or left in right.parents or right in left.parents


def installed_manifest_error(manifest_path: Path) -> str | None:
    if not manifest_path.exists() and not manifest_path.is_symlink():
        return None
    try:
        manifest = json.loads(manifest_path.read_text())
    except OSError as error:
        return f"unreadable: {error}"
    except json.JSONDecodeError as error:
        return f"invalid JSON: {error.msg}"
    if not isinstance(manifest, dict):
        return "root must be an object"
    if type(manifest.get("version")) is not int or manifest["version"] != 1:
        return "version must be 1"
    if not isinstance(manifest.get("steps"), dict):
        return "steps must be an object"
    return None


def manifest_path_owners(manifest_path: Path) -> dict[str, list[Path]]:
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}
    if manifest.get("version") != 1 or not isinstance(manifest.get("steps"), dict):
        return {}

    owners: dict[str, list[Path]] = {}
    for step, entry in manifest["steps"].items():
        if not isinstance(step, str) or not isinstance(entry, dict):
            continue
        paths = entry.get("paths")
        if not isinstance(paths, list) or not all(isinstance(path, str) for path in paths):
            continue
        owners[step] = [normalized_path(Path(path).expanduser()) for path in paths]
    return owners


def manifest_asset_findings(home: Path | None = None) -> list[AssetFinding]:
    home = HOME if home is None else home
    try:
        manifest = json.loads((home / ".agents/.installed-manifest.json").read_text())
    except (OSError, json.JSONDecodeError):
        return []
    if manifest.get("version") != 1 or not isinstance(manifest.get("steps"), dict):
        return []

    findings: list[AssetFinding] = []
    for step, entry in sorted(manifest["steps"].items()):
        if not isinstance(step, str) or not isinstance(entry, dict):
            continue
        paths = entry.get("paths")
        if not isinstance(paths, list) or not all(isinstance(path, str) for path in paths):
            continue
        missing = tuple(
            normalized_path(Path(recorded).expanduser())
            for recorded in paths
            if not Path(recorded).expanduser().exists()
        )
        if missing:
            findings.append(AssetFinding(step, missing, entry))
    return findings


def asset_failure_message(finding: AssetFinding) -> str:
    return f"asset manifest step {finding.step!r} has missing paths: " + ", ".join(
        str(path) for path in finding.missing_paths
    )


def asset_repair_action(finding: AssetFinding, updater: Path | None = None) -> RepairAction | None:
    step, separator, identity = finding.step.partition(":")
    if step not in ASSET_STEP_FUNCTIONS:
        return None
    arguments: tuple[str, ...] = ()
    if step == "ensure_mise_npm_agent_cli":
        mise_tool = MISE_STEP_IDENTITIES.get(identity) if separator else None
        if mise_tool is None:
            return None
        arguments = (identity, mise_tool)
    elif separator:
        return None
    updater = ROOT / "scripts/update-agent-assets.sh" if updater is None else updater
    return RepairAction(
        "asset step missing",
        finding.missing_paths[0],
        (
            "bash",
            "-c",
            UPDATER_SOURCE_COMMAND,
            "bash",
            str(updater),
            step,
            *arguments,
        ),
    )


def source_derived_directory_names(source_root: Path) -> tuple[set[str], set[str]]:
    agents_source = source_root / "dot_agents"
    root_names = (
        {
            deployed_relative_path(path.relative_to(agents_source)).parts[0]
            for path in agents_source.iterdir()
            if path.is_dir()
        }
        if agents_source.is_dir()
        else set()
    )
    skills_source = agents_source / "skills"
    skill_names = (
        {
            deployed_relative_path(path.relative_to(skills_source)).parts[0]
            for path in skills_source.iterdir()
            if path.is_dir() or path.is_symlink()
        }
        if skills_source.is_dir()
        else set()
    )
    return root_names, skill_names


def direct_asset_directories(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir() or path.is_symlink())


def orphaned_asset_warnings(home: Path | None = None, source_root: Path | None = None) -> list[str]:
    home = HOME if home is None else home
    source_root = SOURCE_ROOT if source_root is None else source_root
    agents_root = home / ".agents"
    skills_root = agents_root / "skills"
    source_root_names, source_skill_names = source_derived_directory_names(source_root)
    owners = manifest_path_owners(agents_root / ".installed-manifest.json")
    warnings: list[str] = []

    # Skill links installed by terminal-browser are receipt-tracked, not
    # source-managed; treat them like the understand-anything allowlist.
    receipt_skill_names = {
        path.name for path in terminal_browser_receipt_paths(home) if path.parent == normalized_path(skills_root)
    }
    skill_allowlist = (
        UNDERSTAND_SKILL_ALLOWLIST
        | CRIT_PLUGIN_SKILLS
        | receipt_skill_names
        # agmsg is owned by its upstream installer (update_agmsg), not chezmoi.
        | {"agmsg", "db", "run", "teams"}
    )
    candidates = [(path, source_root_names, AGENT_ROOT_ALLOWLIST) for path in direct_asset_directories(agents_root)] + [
        (path, source_skill_names, skill_allowlist) for path in direct_asset_directories(skills_root)
    ]
    for path, source_names, allowlist in candidates:
        if path.name in source_names or path.name in allowlist:
            continue
        matching_steps = sorted(
            step
            for step, recorded_paths in owners.items()
            if any(paths_overlap(path, recorded_path) for recorded_path in recorded_paths)
        )
        if matching_steps:
            for step in matching_steps:
                warnings.append(f"WARN: stale agent asset: {path}; suggested: remove-agent-asset {shlex.quote(step)}")
        else:
            warnings.append(f"WARN: orphaned agent asset: {path}; manual review required")
    return warnings


def understand_anything_core_warnings(home: Path | None = None) -> list[str]:
    """Warn when the Codex-side Understand-Anything core build is missing or stale.

    `prepare-incremental.mjs` imports packages/core/dist/index.js, so `.ua/`
    incremental updates fail until `make update` builds it. Stale uses the same
    rule as the update-agent-assets.sh build guard: dist/index.js is older than
    any file under packages/core/src or the root pnpm-lock.yaml.
    """
    home = home or HOME
    core = home / ".understand-anything/repo/understand-anything-plugin/packages/core"
    if not core.is_dir():
        return []
    dist = core / "dist/index.js"
    if not dist.is_file():
        return [f"WARN: Understand-Anything core not built: {dist} is missing; run make update"]
    src = core / "src"
    lockfile = core.parents[1] / "pnpm-lock.yaml"
    inputs = [path for path in src.rglob("*") if path.is_file()]
    if lockfile.is_file():
        inputs.append(lockfile)
    newest_input = max((path.stat().st_mtime for path in inputs), default=0.0)
    if newest_input > dist.stat().st_mtime:
        return [
            f"WARN: Understand-Anything core build is stale: {dist} is older than {src} or {lockfile}; run make update"
        ]
    return []


def live_claude_session(project: Path, proc: Path) -> bool:
    """True when a process named `claude` runs with its cwd at PROJECT (Linux /proc)."""
    for entry in proc.glob("[0-9]*"):
        try:
            if (entry / "comm").read_text().strip() == "claude" and (entry / "cwd").resolve() == project:
                return True
        except OSError:
            continue
    return False


def orchestrator_seat_lock_warnings(
    project: Path | None = None,
    skill_dir: Path | None = None,
    proc: Path = Path("/proc"),
) -> list[str]:
    """Warn when the orchestrator's actas lock holds a bare session id.

    The Stop-hook inbox check compares the lock owner with the composite
    `<sid>.<pid>`; a claim from sandboxed Bash cannot see the claude pid (pid
    namespace) and writes the bare sid, so turn delivery skips silently. Only
    the non-worker (no -aNNN) claude-code identities at PROJECT are checked,
    only at the legacy lock path, and only while a claude session runs there.
    The live-session scan reads /proc, so off Linux (where the pid-namespaced
    sandbox does not exist) the check finds nothing.
    """
    project = (project or ROOT).resolve()
    skill_dir = skill_dir or HOME / ".agents/skills/agmsg"
    identities = skill_dir / "scripts/identities.sh"
    if not identities.is_file() or not live_claude_session(project, proc):
        return []
    rows = subprocess.run(
        [str(identities), str(project), "claude-code"],
        env={**os.environ, "AGMSG_RESOLVE_PROJECT": "0"},
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    warnings = []
    for row in sorted(set(rows.splitlines())):
        team, _, name = row.partition("\t")
        if not name or re.search(r"-a\d{3}$", name):
            continue
        lock = skill_dir / "run" / f"actas.{team}__{name}.session"
        try:
            owner = lock.read_text().splitlines()[0].strip()
        except (OSError, IndexError):
            continue
        if owner and not re.search(r"\.\d+$", owner):
            warnings.append(
                f"WARN: orchestrator seat lock {lock} holds the bare session id {owner} "
                f"while a claude session runs in {project}; turn delivery skips silently. "
                "Run `herdr-agents --attach` from the orchestrator pane outside the sandbox "
                "(it replaces a stale lock: bare, or same-session composite whose pid is dead or not a claude process)"
            )
    return warnings


GH_TOKEN_VARIABLES = ("GH_TOKEN", "GITHUB_TOKEN", "GH_ENTERPRISE_TOKEN", "GITHUB_ENTERPRISE_TOKEN")
GH_LOGIN_HINT = "run make gh-auth"


def gh_login_findings(gh: str = "gh") -> list[str]:
    """Report this machine's one GitHub login, the one every seat acts as.

    Present means `gh auth status` finds exactly one account in gh's default
    configuration, it works, and its token sits in gh's own file at mode 0600 (the
    Claude sandbox cannot reach the OS keyring): a `found:` line naming the login.
    Anything else is a warning with the `make gh-auth` hint. Never prompts, and never
    reads or prints a token: the login and its token source come from gh's JSON
    status, with token variables stripped so an environment token cannot stand in for
    the stored login, and CLICOLOR_FORCE stripped so gh prints plain JSON.
    """
    env = {key: value for key, value in os.environ.items() if key not in (*GH_TOKEN_VARIABLES, "CLICOLOR_FORCE")}
    try:
        status = subprocess.run(
            [gh, "auth", "status", "--hostname", "github.com", "--json", "hosts"],
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        accounts = json.loads(status.stdout)["hosts"]["github.com"]
        logins = [account["login"] for account in accounts if account.get("state") == "success"]
    except (OSError, subprocess.TimeoutExpired, ValueError, KeyError, TypeError, AttributeError):
        return [f"WARN: GitHub login: gh auth status failed or gh is missing; {GH_LOGIN_HINT}"]
    if len(accounts) != 1 or len(logins) != 1:
        message = (
            f"WARN: GitHub login: gh holds {len(logins)} working of {len(accounts)} logins; keep exactly one "
            f"(gh auth logout --user <login> for any other, or {GH_LOGIN_HINT})"
        )
        return [message]
    # gh names the file it read the token from; a keyring token shows "keyring", or "default" where unreachable.
    source = str(accounts[0].get("tokenSource", ""))
    if not source.endswith("hosts.yml"):
        message = (
            "WARN: GitHub login is stored in the OS keyring, which the Claude sandbox cannot reach; "
            "run make gh-auth to store it in gh's file"
        )
        return [message]
    try:
        mode = Path(source).stat().st_mode & 0o777
    except OSError:
        return [f"WARN: GitHub login: cannot read the mode of {source}; {GH_LOGIN_HINT}"]
    if mode != 0o600:
        return [f"WARN: GitHub login: {source} has mode {mode:04o}, not 0600; {GH_LOGIN_HINT}"]
    return [f"found: GitHub login {logins[0]} (every seat on this machine acts as it)"]


def deployed_target_path(value: str, home: Path) -> Path:
    if value == "~":
        return home
    if value.startswith("~/"):
        return home / value[2:]
    return Path(value)


def repair_actions(failures: list[str], home: Path | None = None) -> list[RepairAction]:
    home = HOME if home is None else home
    actions: list[RepairAction] = []
    tree_roots = {
        "shared skill directory": home / ".agents/skills",
        "Claude shared-skill tree": home / ".claude/skills",
    }

    for failure in failures:
        if is_warning(failure) or is_info(failure):
            continue
        if " is missing files: " in failure:
            label, _, values = failure.partition(" is missing files: ")
            root = tree_roots.get(label)
            if root is not None:
                for value in values.split(", "):
                    target = root / value
                    actions.append(
                        RepairAction(
                            "missing file",
                            target,
                            (*CHEZMOI_APPLY_COMMAND, str(target)),
                        )
                    )
            continue

        target_value = ""
        category = ""
        command_name = "chezmoi"
        for marker in (
            " differs or is missing: ",
            " managed keys differ or profile is missing: ",
            " directory is missing: ",
            " is missing: ",
        ):
            if marker in failure:
                _, _, target_value = failure.partition(marker)
                target = deployed_target_path(target_value, home)
                category = "content differs" if target.exists() or target.is_symlink() else "missing file"
                break
        if not target_value and " differs: " in failure:
            _, _, target_value = failure.partition(" differs: ")
            category = "content differs"
        if not target_value and " is not executable: " in failure:
            _, _, target_value = failure.partition(" is not executable: ")
            category = "executable bit missing"
            command_name = "chmod"
        if target_value:
            target = deployed_target_path(target_value, home)
            command = ("chmod", "+x", str(target)) if command_name == "chmod" else (*CHEZMOI_APPLY_COMMAND, str(target))
            actions.append(RepairAction(category, target, command))

    failure_set = set(failures)
    for finding in manifest_asset_findings(home):
        if asset_failure_message(finding) not in failure_set:
            continue
        action = asset_repair_action(finding)
        if action is not None:
            actions.append(action)

    unique: list[RepairAction] = []
    commands: set[tuple[str, ...]] = set()
    for action in actions:
        if action.command not in commands:
            unique.append(action)
            commands.add(action.command)
    return unique


def execute_repair(action: RepairAction) -> bool:
    return subprocess.run(action.command, check=False).returncode == 0


def print_failures(failures: list[str]) -> None:
    for failure in failures:
        if is_warning(failure) or is_info(failure):
            print(failure)
        else:
            print(f"ERROR: {failure}", file=sys.stderr)


def check() -> list[str]:
    failures: list[str] = []
    checks = [
        (
            SOURCE_ROOT / "dot_claude/private_mcp.json.tmpl",
            HOME / ".claude/mcp.json",
            True,
            "Claude MCP config",
        ),
        (
            SOURCE_ROOT / "dot_agents/model-profiles.env",
            HOME / ".agents/model-profiles.env",
            False,
            "model profile fragment",
        ),
        (
            SOURCE_ROOT / "dot_claude/agents/express-explorer.md",
            HOME / ".claude/agents/express-explorer.md",
            False,
            "Claude express-explorer agent",
        ),
    ]
    for source, target, template, label in checks:
        if not same_text(source, target, template=template):
            failures.append(f"{label} differs or is missing: {target}")
    for profile_source in sorted(SOURCE_ROOT.glob("dot_codex/modify_*.config.toml")):
        target_name = deployed_relative_path(Path(profile_source.name.removeprefix("modify_"))).name
        target = HOME / ".codex" / target_name
        if not same_modified(profile_source, target):
            failures.append(
                f"Codex model profile {target_name.removesuffix('.config.toml')} managed keys differ or profile is missing: {target}"
            )
    if not same_modified(
        SOURCE_ROOT / "dot_codex/modify_private_config.toml",
        HOME / ".codex/config.toml",
    ):
        failures.append(f"Codex config managed keys differ or config is missing: {HOME / '.codex/config.toml'}")
    if not same_modified(
        SOURCE_ROOT / "dot_claude/modify_private_settings.json",
        HOME / ".claude/settings.json",
        json_target=True,
    ):
        failures.append(
            f"Claude settings managed keys differ or settings file is missing: {HOME / '.claude/settings.json'}"
        )

    failures.extend(compare_shared_skills())
    failures.extend(compare_claude_skills())
    failures.extend(
        check_executable_hook(
            SOURCE_ROOT / "dot_claude/hooks/executable_enforce-uv.sh",
            HOME / ".claude/hooks/enforce-uv.sh",
            "Claude enforce-uv hook",
        )
    )
    failures.extend(
        check_executable_hook(
            SOURCE_ROOT / "dot_claude/hooks/executable_format-edited-files.py",
            HOME / ".claude/hooks/format-edited-files.py",
            "Claude format-edited-files hook",
        )
    )
    manifest_path = HOME / ".agents/.installed-manifest.json"
    manifest_error = installed_manifest_error(manifest_path)
    if manifest_error is not None:
        failures.append(f"installed manifest unreadable or invalid: {manifest_path} ({manifest_error})")
    else:
        failures.extend(asset_failure_message(finding) for finding in manifest_asset_findings())
        failures.extend(orphaned_asset_warnings())
    failures.extend(understand_anything_core_warnings())
    failures.extend(orchestrator_seat_lock_warnings())
    failures.extend(gh_login_findings())
    failures.extend(chezmoi_drift_warnings())
    return failures


def run_session_staleness(epoch: str | None) -> int:
    command = [str(HOME / ".local/bin/common/agent-session-staleness")]
    if epoch is not None:
        command.extend(["check", "--since", epoch])
    return subprocess.run(command, check=False).returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--session-staleness",
        nargs="?",
        const="",
        metavar="EPOCH",
        help="show recent managed-asset updates, or compare them with EPOCH",
    )
    args = parser.parse_args(argv)
    if args.session_staleness is not None:
        return run_session_staleness(args.session_staleness or None)
    failures = check()
    print_failures(failures)
    if os.environ.get("REPAIR") == "1":
        for action in repair_actions(failures):
            if execute_repair(action):
                print(f"repaired: {action.category} {action.target} ({shlex.join(action.command)})")
        remaining = check()
        if repair_actions(remaining):
            print("non-convergent after repair", file=sys.stderr)
            return 1
        failures = remaining
    errors = [failure for failure in failures if not is_warning(failure) and not is_info(failure)]
    if errors:
        return 1
    print("active agent runtime files match this chezmoi source tree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
