#!/usr/bin/env python3
"""Check whether active HOME agent runtime files match this chezmoi source tree.

This script is intentionally read-only. Run it after `chezmoi apply` to prove that
Codex, Claude Code, Hermes, MCP, hooks, plugins, and shared skills are actually
using the generated source state.
"""

from __future__ import annotations

import argparse
import re
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "home"
HOME = Path.home()


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


def source_files(root: Path) -> dict[Path, Path]:
    return {path.relative_to(root): path for path in sorted(root.rglob("*")) if path.is_file()}


def applied_files(root: Path) -> set[Path]:
    if not root.exists():
        return set()
    return {path.relative_to(root) for path in sorted(root.rglob("*")) if path.is_file() or path.is_symlink()}


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


def compare_tree_contents(label: str, expected: dict[Path, str], target_root: Path) -> list[str]:
    failures: list[str] = []
    actual = applied_files(target_root)
    expected_rels = set(expected)
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
    return failures


def compare_shared_skills() -> list[str]:
    source_root = SOURCE_ROOT / "dot_agents/skills"
    target_root = HOME / ".agents/skills"
    if not target_root.exists():
        return ["shared skill directory is missing: ~/.agents/skills"]
    expected = {rel: path.read_text() for rel, path in source_files(source_root).items()}
    return compare_tree_contents("shared skill directory", expected, target_root)


def compare_claude_skills() -> list[str]:
    target_root = HOME / ".claude/skills"
    if not target_root.exists():
        return ["Claude shared-skill symlink tree is missing: ~/.claude/skills"]
    return compare_tree_contents("Claude shared-skill tree", expected_claude_skill_targets(), target_root)


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
        (SOURCE_ROOT / "dot_codex/private_config.toml.tmpl", HOME / ".codex/config.toml", True, "Codex config"),
        (SOURCE_ROOT / "dot_claude/private_settings.json", HOME / ".claude/settings.json", False, "Claude settings"),
        (SOURCE_ROOT / "dot_claude/private_mcp.json.tmpl", HOME / ".claude/mcp.json", True, "Claude MCP config"),
        (SOURCE_ROOT / "dot_hermes/private_config.yaml.tmpl", HOME / ".hermes/config.yaml", True, "Hermes config"),
    ]
    for source, target, template, label in checks:
        if not same_text(source, target, template=template):
            failures.append(f"{label} differs or is missing: {target}")

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
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1
    print("active agent runtime files match this chezmoi source tree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
