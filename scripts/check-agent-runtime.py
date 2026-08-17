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
AGENT_ROOT_ALLOWLIST = {"compactiondb", "db", "run", "teams", "worklog"}
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
ASSET_STEP_FUNCTIONS = {
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
}
MISE_STEP_IDENTITIES = {
    "claude": "npm:@anthropic-ai/claude-code",
    "codex": "npm:@openai/codex",
}
UPDATER_SOURCE_COMMAND = (
    'source "$1"; export PATH="$HOME/.local/share/mise/shims:$PATH"; shift; "$@"'
)
CHEZMOI_APPLY_COMMAND = ("chezmoi", "apply", "--force")
MODE_ONLY_DIFF = re.compile(
    r"\Adiff --git .+\nold mode [0-7]+\nnew mode [0-7]+\n?\Z"
)


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
        rel == ignored
        or ignored in rel.parents
        or (ignored == Path("agmsg/db") and str(rel).startswith("agmsg/db-"))
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
        if path.is_file()
        and not is_ignored_runtime_path(deployed_relative_path(path.relative_to(root)))
    }


def applied_files(root: Path) -> set[Path]:
    if not root.exists():
        return set()
    return {
        path.relative_to(root)
        for path in sorted(root.rglob("*"))
        if (path.is_file() or path.is_symlink())
        and not is_ignored_runtime_path(path.relative_to(root))
    }


def expects_executable(source: Path) -> bool:
    return source.name.startswith("executable_")


def is_warning(message: str) -> bool:
    return message.startswith("WARN: ")


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
        if diff_result.returncode == 0 and MODE_ONLY_DIFF.fullmatch(
            diff_result.stdout
        ):
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


def compare_tree_contents(
    label: str,
    expected: dict[Path, str],
    target_root: Path,
    expected_sources: dict[Path, Path] | None = None,
    warn_unmanaged_top_level: bool = False,
) -> list[str]:
    failures: list[str] = []
    actual = applied_files(target_root)
    expected_rels = set(expected)
    if warn_unmanaged_top_level:
        managed_top_levels = {rel.parts[0] for rel in expected_rels if rel.parts}
        unmanaged_top_levels = sorted(
            {
                rel.parts[0]
                for rel in actual
                if rel.parts and rel.parts[0] not in managed_top_levels
            }
        )
        for top_level in unmanaged_top_levels:
            failures.append(f"WARN: unmanaged skill dir: {target_root / top_level}")
        actual = {
            rel for rel in actual if rel.parts and rel.parts[0] in managed_top_levels
        }
    missing = sorted(expected_rels - actual)
    extra = sorted(actual - expected_rels)
    if missing:
        failures.append(
            f"{label} is missing files: {', '.join(str(path) for path in missing[:20])}"
        )
    if extra:
        failures.append(
            f"{label} has unexpected files: {', '.join(str(path) for path in extra[:20])}"
        )
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
        if (
            source is not None
            and expects_executable(source)
            and not target.stat().st_mode & stat.S_IXUSR
        ):
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
        "Claude shared-skill tree", expected_claude_skill_targets(), target_root
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
    return (
        f"asset manifest step {finding.step!r} has missing paths: "
        + ", ".join(str(path) for path in finding.missing_paths)
    )


def asset_repair_action(
    finding: AssetFinding, updater: Path | None = None
) -> RepairAction | None:
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
    root_names = {
        deployed_relative_path(path.relative_to(agents_source)).parts[0]
        for path in agents_source.iterdir()
        if path.is_dir()
    } if agents_source.is_dir() else set()
    skills_source = agents_source / "skills"
    skill_names = {
        deployed_relative_path(path.relative_to(skills_source)).parts[0]
        for path in skills_source.iterdir()
        if path.is_dir() or path.is_symlink()
    } if skills_source.is_dir() else set()
    return root_names, skill_names


def direct_asset_directories(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(
        path for path in root.iterdir() if path.is_dir() or path.is_symlink()
    )


def orphaned_asset_warnings(
    home: Path | None = None, source_root: Path | None = None
) -> list[str]:
    home = HOME if home is None else home
    source_root = SOURCE_ROOT if source_root is None else source_root
    agents_root = home / ".agents"
    skills_root = agents_root / "skills"
    source_root_names, source_skill_names = source_derived_directory_names(source_root)
    owners = manifest_path_owners(agents_root / ".installed-manifest.json")
    warnings: list[str] = []

    candidates = [
        (path, source_root_names, AGENT_ROOT_ALLOWLIST)
        for path in direct_asset_directories(agents_root)
    ] + [
        (path, source_skill_names, UNDERSTAND_SKILL_ALLOWLIST | {"db", "run", "teams"})
        for path in direct_asset_directories(skills_root)
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
                warnings.append(
                    f"WARN: stale agent asset: {path}; suggested: remove-agent-asset {shlex.quote(step)}"
                )
        else:
            warnings.append(
                f"WARN: orphaned agent asset: {path}; manual review required"
            )
    return warnings


def deployed_target_path(value: str, home: Path) -> Path:
    if value == "~":
        return home
    if value.startswith("~/"):
        return home / value[2:]
    return Path(value)


def repair_actions(
    failures: list[str], home: Path | None = None
) -> list[RepairAction]:
    home = HOME if home is None else home
    actions: list[RepairAction] = []
    tree_roots = {
        "shared skill directory": home / ".agents/skills",
        "Claude shared-skill tree": home / ".claude/skills",
    }

    for failure in failures:
        if is_warning(failure):
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
                category = (
                    "content differs"
                    if target.exists() or target.is_symlink()
                    else "missing file"
                )
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
            command = (
                ("chmod", "+x", str(target))
                if command_name == "chmod"
                else (*CHEZMOI_APPLY_COMMAND, str(target))
            )
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
        if is_warning(failure):
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
        target_name = deployed_relative_path(
            Path(profile_source.name.removeprefix("modify_"))
        ).name
        target = HOME / ".codex" / target_name
        if not same_modified(profile_source, target):
            failures.append(
                f"Codex model profile {target_name.removesuffix('.config.toml')} managed keys differ or profile is missing: {target}"
            )
    if not same_modified(
        SOURCE_ROOT / "dot_codex/modify_private_config.toml",
        HOME / ".codex/config.toml",
    ):
        failures.append(
            f"Codex config managed keys differ or config is missing: {HOME / '.codex/config.toml'}"
        )
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
        failures.append(
            f"installed manifest unreadable or invalid: {manifest_path} ({manifest_error})"
        )
    else:
        failures.extend(
            asset_failure_message(finding) for finding in manifest_asset_findings()
        )
        failures.extend(orphaned_asset_warnings())
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
                print(
                    f"repaired: {action.category} {action.target} "
                    f"({shlex.join(action.command)})"
                )
        remaining = check()
        if repair_actions(remaining):
            print("non-convergent after repair", file=sys.stderr)
            return 1
        failures = remaining
    errors = [failure for failure in failures if not is_warning(failure)]
    if errors:
        return 1
    print("active agent runtime files match this chezmoi source tree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
