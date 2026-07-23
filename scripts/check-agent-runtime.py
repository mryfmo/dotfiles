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
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "home"
HOME = Path.home()
CHEZMOI_SOURCE_PREFIXES = ("executable_", "private_")
AGMSG_RUNTIME_IGNORES = (
    Path("agmsg/.agmsg"),
    Path("agmsg/db"),
    Path("agmsg/run"),
    Path("agmsg/teams"),
)


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
    return any(
        rel == ignored or ignored in rel.parents for ignored in AGMSG_RUNTIME_IGNORES
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
    for profile_source in sorted(SOURCE_ROOT.glob("dot_codex/*.config.toml")):
        checks.append(
            (
                profile_source,
                HOME / ".codex" / profile_source.name,
                False,
                f"Codex model profile {profile_source.stem}",
            )
        )
    for source, target, template, label in checks:
        if not same_text(source, target, template=template):
            failures.append(f"{label} differs or is missing: {target}")
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
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    failures = check()
    errors = [failure for failure in failures if not is_warning(failure)]
    for failure in failures:
        if is_warning(failure):
            print(failure)
        else:
            print(f"ERROR: {failure}", file=sys.stderr)
    if errors:
        return 1
    print("active agent runtime files match this chezmoi source tree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
