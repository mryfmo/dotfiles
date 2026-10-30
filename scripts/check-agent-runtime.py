#!/usr/bin/env python3
"""Check whether active HOME agent runtime files match this chezmoi source tree.

This script is intentionally read-only. Run it after `chezmoi apply` to prove that
Codex, Claude Code, MCP, hooks, plugins, and shared skills are actually
using the generated source state.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import hashlib
import json
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "home"
HOME = Path.home()
CHEZMOI_SOURCE_PREFIXES = ("executable_", "private_")
# backups/ holds the pre-install state copies that earlier `make update` runs made.
AGENT_ROOT_ALLOWLIST = {"backups", "compactiondb", "worklog"}
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
    "update_pi_claude_bridge",
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


def exact_text(path: Path) -> str:
    """A file's text with every byte kept: no newline translation, undecodable bytes round-trip through encode_bytes."""
    return path.read_bytes().decode(errors="surrogateescape")


def encode_bytes(text: str) -> bytes:
    return text.encode(errors="surrogateescape")


def render_template(path: Path) -> str:
    text = exact_text(path)
    # This repository uses .chezmoiroot=home, so .chezmoi.sourceDir resolves to
    # the chezmoi source root that contains dot_agents/, dot_codex/, etc.
    text = text.replace("{{ .chezmoi.sourceDir }}", str(SOURCE_ROOT))
    text = re.sub(r"\{\{/\*.*?\*/\}\}", "", text, flags=re.DOTALL)
    return text


def same_text(source: Path, target: Path, template: bool = False) -> bool:
    """Whether target holds exactly the bytes of source (or of its rendering): a CRLF or BOM difference is a mismatch."""
    if not target.is_file():
        return False
    expected = encode_bytes(render_template(source)) if template else source.read_bytes()
    return target.read_bytes() == expected


def same_modified(
    source: Path, target: Path, json_target: bool = False, working_tree: str | None = None, quiet: bool = False
) -> bool:
    """Whether running the modify script `source` on `target` leaves it unchanged.

    The script reads this checkout's managed baseline (CHEZMOI_SOURCE_DIR) and, when given, the working tree chezmoi
    applies from (CHEZMOI_WORKING_TREE), which the Codex config keys its project trust with (F058). `quiet` makes any
    stderr output a mismatch, for a script that degrades to passing its input through with a warning.
    """
    if not target.is_file():
        return False
    current = target.read_bytes()
    env = os.environ.copy()
    env["CHEZMOI_SOURCE_DIR"] = str(SOURCE_ROOT)
    if working_tree is not None:
        env["CHEZMOI_WORKING_TREE"] = working_tree
    # Bytes in and out: no newline translation on either side, so the script's output must equal the file exactly.
    result = subprocess.run([str(source)], input=current, capture_output=True, env=env, check=False)
    if result.returncode != 0 or (quiet and result.stderr):
        return False
    if json_target:
        try:
            return json.loads(result.stdout) == json.loads(current)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return False
    return result.stdout == current


def deployed_relative_path(source_rel: Path) -> Path:
    name = source_rel.name
    for prefix in CHEZMOI_SOURCE_PREFIXES:
        if name.startswith(prefix):
            return source_rel.with_name(name.removeprefix(prefix))
    return source_rel


def source_files(root: Path) -> dict[Path, Path]:
    return {deployed_relative_path(path.relative_to(root)): path for path in sorted(root.rglob("*")) if path.is_file()}


def applied_files(root: Path) -> set[Path]:
    if not root.exists():
        return set()
    return {path.relative_to(root) for path in sorted(root.rglob("*")) if path.is_file() or path.is_symlink()}


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
            # run_ scripts are listed on every status because they run on every apply; they are not drift.
            ["chezmoi", "--no-pager", "status", "--exclude=scripts"],
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

    entries: list[tuple[str, str]] = []
    for line in status_result.stdout.splitlines():
        if len(line) < 4:
            continue
        entries.append((line[:2], line[3:]))
    if not entries:
        return []

    # One diff for the whole destination: each chezmoi invocation loads the full
    # source state, so a per-target diff takes hours on hosts with thousands of entries.
    diff_result = subprocess.run(
        ["chezmoi", "--no-pager", "diff", "--exclude=scripts"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    diff_blocks = split_chezmoi_diff(diff_result.stdout) if diff_result.returncode == 0 else {}

    warnings: list[str] = []
    for status, target in entries:
        target_path = Path(target)
        if target_path.is_absolute():
            target_path = target_path.relative_to(HOME) if target_path.is_relative_to(HOME) else target_path
        block = diff_blocks.get(target_path.as_posix())
        if block is not None and MODE_ONLY_DIFF.fullmatch(block):
            hint = "permission divergence (mode-only)"
        elif status == " M":
            hint = "unapplied source update"
        elif status == "MM":
            hint = "two-sided drift"
        else:
            hint = "managed target drift"
        warnings.append(f"WARN: chezmoi drift {status} {target}: {hint}")
    return warnings


def split_chezmoi_diff(output: str) -> dict[str, str]:
    """Split `chezmoi diff` output into per-target blocks keyed by destination-relative path."""
    blocks: dict[str, str] = {}
    current: str | None = None
    lines: list[str] = []
    for line in output.splitlines(keepends=True):
        if line.startswith("diff --git a/"):  # lint-comparisons: allow a diff header prefix, not a path
            if current is not None:
                blocks[current] = "".join(lines)
            # chezmoi never renames, so the header is `a/<path> b/<path>` with equal halves.
            paths = line[len("diff --git ") :].rstrip("\n")
            current = paths[2 : (len(paths) - 1) // 2]
            lines = []
        if current is not None:
            lines.append(line)
    if current is not None:
        blocks[current] = "".join(lines)
    return blocks


def output_index_path() -> Path:
    """scripts/generate-agent-configs.py's expected output set, rendered for this script (which has no PyYAML)."""
    return SOURCE_ROOT.parent / "scripts/generated-agent-outputs.json"


OUTPUT_KINDS = frozenset({"file", "template", "modify", "create", "symlink"})
SHA256_HEX = re.compile(r"[0-9a-f]{64}")


def output_index_error(index: object) -> str | None:
    """Why `index` is not the generator's output index, field by field with exact types; None when it is.

    The shape is generate-agent-configs.py render_output_index's: exactly generated_by, outputs, scopes and skills; an
    output is {source, target: null} for a file chezmoi does not deploy by itself, else {source, target, kind,
    executable} with a known kind; a scope is {source, target, glob}; skills is skill_index's. Every path is a
    non-empty relative string.
    """

    def relative(value: object) -> bool:
        return (
            isinstance(value, str) and bool(value) and not Path(value).is_absolute() and ".." not in Path(value).parts
        )

    def names(value: object) -> bool:
        return isinstance(value, list) and all(isinstance(item, str) and item for item in value)

    if not isinstance(index, dict) or set(index) != {"generated_by", "outputs", "scopes", "skills"}:
        return "the top level must hold exactly generated_by, outputs, scopes and skills"
    if not isinstance(index["generated_by"], str):
        return "generated_by must be a string"
    if not isinstance(index["outputs"], list) or not isinstance(index["scopes"], list):
        return "outputs and scopes must be lists"
    skills = index["skills"]
    if (
        not isinstance(skills, dict)
        or set(skills) != {"shared_root", "pstack_root", "audience", "pstack", "codex_disabled", "omp"}
        or not relative(skills["shared_root"])
        or not relative(skills["pstack_root"])
        or not isinstance(skills["audience"], dict)
        or not all(names(audience) for audience in skills["audience"].values())
        or not isinstance(skills["pstack"], dict)
        or set(skills["pstack"]) != {"audience", "exclude"}
        or not all(names(value) for value in skills["pstack"].values())
        or not names(skills["codex_disabled"])
        or not isinstance(skills["omp"], dict)
        or not all(
            isinstance(entry, dict)
            and set(entry) == {"enabled", "pstack", "ignored"}
            and isinstance(entry["enabled"], bool)
            and isinstance(entry["pstack"], bool)
            and names(entry["ignored"])
            for entry in skills["omp"].values()
        )
    ):
        return (
            "skills must be {shared_root, pstack_root, audience, pstack, codex_disabled, omp} as skill_index renders it"
        )
    for number, entry in enumerate(index["outputs"]):
        if not isinstance(entry, dict) or not relative(entry.get("source")):
            return f"outputs[{number}] must be an object with a relative source"
        if set(entry) == {"source", "target"} and entry["target"] is None:
            continue
        keys = {"source", "target", "kind", "executable"}
        if (
            set(entry) - {"sha256"} != keys
            or not relative(entry["target"])
            or entry["kind"] not in OUTPUT_KINDS
            or not isinstance(entry["executable"], bool)
            or ("sha256" in entry and (entry["kind"] != "file" or not SHA256_HEX.fullmatch(str(entry["sha256"]))))
        ):
            return (
                f"outputs[{number}] must be {{source, target, kind, executable}} with a known kind, and a lowercase "
                f"hex sha256 only on a file: {entry!r}"
            )
    for number, scope in enumerate(index["scopes"]):
        if (
            not isinstance(scope, dict)
            or set(scope) != {"source", "target", "glob"}
            or not all(relative(scope[key]) for key in ("source", "target", "glob"))
        ):
            return f"scopes[{number}] must be {{source, target, glob}} of relative strings: {scope!r}"
    return None


def load_output_index() -> tuple[dict[str, list[dict[str, object]]] | None, str | None]:
    """The generated output index, or None and the reason it cannot be used; a bad index is never "no outputs"."""
    path = output_index_path()
    try:
        index = json.loads(path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return None, f"generated output index unreadable: {path} ({error})"
    error = output_index_error(index)
    if error is not None:
        return None, f"generated output index invalid: {path}: {error} (run scripts/generate-agent-configs.py)"
    return index, None


def chezmoi_working_tree() -> tuple[str | None, str | None]:
    """The working tree chezmoi applies from (its .chezmoi.workingTree), or None and why it could not be read."""
    try:
        result = subprocess.run(
            ["chezmoi", "--no-pager", "execute-template", "{{ .chezmoi.workingTree }}"],
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as error:
        return None, str(error)
    if result.returncode != 0 or not result.stdout.strip():
        return None, result.stderr.strip() or f"exit {result.returncode}"
    return result.stdout.strip(), None


def render_chezmoi_template(source: Path) -> tuple[bytes | None, str | None]:
    """chezmoi's own rendering of one source template with the host's data, as bytes, or None and why it failed."""
    try:
        result = subprocess.run(
            ["chezmoi", "--no-pager", "execute-template"],
            input=source.read_bytes(),
            capture_output=True,
            check=False,
        )
    except OSError as error:
        return None, str(error)
    if result.returncode != 0:
        return None, result.stderr.decode(errors="replace").strip() or f"exit {result.returncode}"
    return result.stdout, None


def scope_files(root: Path, pattern: str) -> set[Path]:
    if not root.is_dir():
        return set()
    return {path for path in root.glob(pattern) if path.is_file() or path.is_symlink()}


def generated_target_findings(index: dict[str, list[dict[str, object]]], working_tree: str | None) -> list[str]:
    """Compare every deployed generated file with this checkout's generated source, and find host orphans.

    A file target matches the source bytes (and its execute bit), a template target chezmoi's rendering, a modify
    target the result of its script, and a create target, which chezmoi never rewrites, at least exists. Claude's
    skill links are compare_claude_skills'. A file in a generated directory on the host that no output deploys is an
    orphan: an ERROR naming the file, which only the operator removes.
    """
    failures: list[str] = []
    targets: set[Path] = set()
    for entry in index["outputs"]:
        if entry["target"] is None:
            continue
        source = SOURCE_ROOT.parent / str(entry["source"])
        target = HOME / str(entry["target"])
        targets.add(normalized_path(target))
        kind = entry.get("kind")
        if kind == "symlink":
            continue
        if kind == "create":
            if not target.exists():
                failures.append(f"generated file differs or is missing: {target}")
            elif not same_text(source, target):
                failures.append(f"WARN: {target} differs from {entry['source']}; chezmoi creates it once and keeps it")
        elif kind == "modify":
            if working_tree is None:
                continue
            if not same_modified(source, target, working_tree=working_tree):
                failures.append(f"generated config managed keys differ or profile is missing: {target}")
        elif kind == "template":
            rendered, error = render_chezmoi_template(source)
            if rendered is None:
                failures.append(f"cannot render {entry['source']} with chezmoi: {error}")
            elif not target.is_file() or target.read_bytes() != rendered:
                failures.append(f"generated file differs or is missing: {target}")
        else:  # "file": output_index_error admits no other kind.
            if not same_text(source, target):
                failures.append(f"generated file differs or is missing: {target}")
            elif "sha256" in entry and hashlib.sha256(target.read_bytes()).hexdigest() != entry["sha256"]:
                # The source and the deployed copy can be corrupted alike; the pin cannot.
                failures.append(f"generated file does not hash to its pinned sha256: {target}")
            elif entry["executable"] and not target.stat().st_mode & stat.S_IXUSR:
                failures.append(f"generated file is not executable: {target}")
    for scope in index["scopes"]:
        if Path(str(scope["target"])).parts == (".claude", "skills"):
            continue
        for path in sorted(scope_files(HOME / str(scope["target"]), str(scope["glob"]))):
            if normalized_path(path) not in targets:
                failures.append(f"generated directory holds a file no manifest entry renders: {path}; remove it")
    return failures


def expected_claude_skill_targets(entries: list[dict[str, object]]) -> dict[Path, str]:
    """Return applied Claude skill relative paths and their expected file content, from the output index."""
    outputs: dict[Path, str] = {}
    for entry in entries:
        target = entry["target"]
        if entry.get("kind") != "symlink" or not isinstance(target, str):
            continue
        parts = Path(target).parts
        if parts[:2] != (".claude", "skills"):
            continue
        applied_rel = Path(*parts[2:])
        linked_source_text = render_template(SOURCE_ROOT.parent / str(entry["source"])).strip()
        linked_source = Path(linked_source_text)
        if linked_source.exists():
            outputs[applied_rel] = exact_text(linked_source)
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


def chezmoi_managed_child_names(root: Path) -> set[str]:
    """Names of the directories chezmoi manages directly under root, externals included.

    The pstack skills (assets.pstack) arrive as chezmoi externals, so they are managed without a copy under
    home/; chezmoi itself verifies them. Empty when chezmoi cannot answer.
    """
    try:
        result = subprocess.run(
            ["chezmoi", "--no-pager", "managed", "--include=dirs", "--path-style=absolute", str(root)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError:
        return set()
    if result.returncode != 0:
        return set()
    return {
        Path(line).name
        for line in result.stdout.splitlines()
        if line.strip() and os.path.realpath(os.path.dirname(line)) == os.path.realpath(root)
    }


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
            actual_text = exact_text(target)
        except OSError as error:
            failures.append(f"{label} cannot read {target}: {error}")
            continue
        if actual_text != expected[rel]:
            failures.append(f"{label} differs: {target}")
        source = expected_sources.get(rel) if expected_sources is not None else None
        if source is not None and expects_executable(source) and not target.stat().st_mode & stat.S_IXUSR:
            failures.append(f"{label} is not executable: {target}")
    return failures


def installer_owned_skill_names(home: Path | None = None) -> set[str]:
    """Skill directories under ~/.agents/skills that an installer or chezmoi external owns, not home/dot_agents/skills.

    One list for both the unmanaged-skill WARN and the orphan scan (F157).
    """
    home = HOME if home is None else home
    skills_root = home / ".agents/skills"
    # Skill links installed by terminal-browser are receipt-tracked, not source-managed.
    receipt_skill_names = {
        path.name for path in terminal_browser_receipt_paths(home) if path.parent == normalized_path(skills_root)
    }
    return (
        UNDERSTAND_SKILL_ALLOWLIST
        | CRIT_PLUGIN_SKILLS
        | receipt_skill_names
        # chezmoi externals (the pstack skills) have no copy under home/ but are chezmoi's.
        | chezmoi_managed_child_names(skills_root)
    )


def compare_shared_skills() -> list[str]:
    source_root = SOURCE_ROOT / "dot_agents/skills"
    target_root = HOME / ".agents/skills"
    if not target_root.exists():
        return ["shared skill directory is missing: ~/.agents/skills"]
    expected_sources = source_files(source_root)
    expected = {rel: exact_text(path) for rel, path in expected_sources.items()}
    owned_elsewhere = installer_owned_skill_names() - {rel.parts[0] for rel in expected if rel.parts}
    return compare_tree_contents(
        "shared skill directory",
        expected,
        target_root,
        expected_sources,
        warn_unmanaged_top_level=True,
        ignored_paths={target_root / name for name in owned_elsewhere},
    )


def compare_claude_skills(entries: list[dict[str, object]]) -> list[str]:
    target_root = HOME / ".claude/skills"
    if not target_root.exists():
        return ["Claude shared-skill symlink tree is missing: ~/.claude/skills"]
    return compare_tree_contents(
        "Claude shared-skill tree",
        expected_claude_skill_targets(entries),
        target_root,
        # Cowork syncs its own skills into this subtree; chezmoi does not own it.
        ignored_paths=terminal_browser_receipt_paths() | {HOME / ".claude/skills/synced"},
    )


def skill_names(root: Path) -> list[str]:
    """The skill directories directly under root (a symlinked one included), sorted; none when root is absent."""
    if not root.is_dir():
        return []
    return sorted(path.name for path in root.iterdir() if (path / "SKILL.md").is_file())


def skill_audience_findings(skills: dict, home: Path | None = None) -> list[str]:
    """An ERROR for each deployed skill an agent lists outside its skills.audience, from the deployed roots.

    What each agent lists: Claude Code every skill under ~/.claude/skills; Codex every one under ~/.agents/skills less
    the managed `[[skills.config]]` disables (codex_disabled; the managed keys of ~/.codex/config.toml are checked
    with the generated outputs); each omp consumer, unless its skills are off, every one under ~/.agents/skills and,
    when it loads the pstack root, under ~/.agents/pstack/skills, less its ignoredSkills. A name under the pstack
    root, or one under ~/.agents/skills that the pstack root also holds (a copy the retired external left), has the
    pstack audience; a name with no audience at all is a WARN.
    """
    home = HOME if home is None else home
    audience: dict[str, list[str]] = skills["audience"]
    pstack: dict[str, list[str]] = skills["pstack"]
    shared_root = home / str(skills["shared_root"])
    pstack_root = home / str(skills["pstack_root"])
    claude_root = home / ".claude/skills"
    shared = skill_names(shared_root)
    pstack_names = set(skill_names(pstack_root))
    # (name, path, whether the path is under the pstack root) for every skill each agent lists.
    listed: dict[str, list[tuple[str, Path, bool]]] = {
        "claude": [(name, claude_root / name, False) for name in skill_names(claude_root)]
    }
    disabled = set(skills["codex_disabled"])
    listed["codex"] = [(name, shared_root / name, False) for name in shared if name not in disabled]
    for consumer, entry in skills["omp"].items():
        if not entry["enabled"]:
            listed[consumer] = []
            continue
        ignored = set(entry["ignored"])
        roots = [(name, shared_root / name, False) for name in shared]
        if entry["pstack"]:
            roots += [(name, pstack_root / name, True) for name in sorted(pstack_names)]
        listed[consumer] = [root for root in roots if root[0] not in ignored]
    findings: list[str] = []
    undeclared: set[Path] = set()
    for consumer, entries in listed.items():
        for name, path, in_pstack_root in entries:
            if in_pstack_root or (name not in audience and name in pstack_names):
                allowed = [] if name in pstack["exclude"] else pstack["audience"]
            elif name in audience:
                allowed = audience[name]
            else:
                undeclared.add(path)
                continue
            if consumer not in allowed:
                findings.append(f"skill {name} is listed by {consumer} outside its audience {allowed}: {path}")
    findings.extend(
        f"WARN: skill {path.name} has no skills.audience entry in agent-config.yaml; every agent reading "
        f"{path.parent} lists it: {path}"
        for path in sorted(undeclared)
    )
    return findings


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

    skill_allowlist = installer_owned_skill_names(home)
    root_allowlist = AGENT_ROOT_ALLOWLIST | chezmoi_managed_child_names(agents_root)
    candidates = [(path, source_root_names, root_allowlist) for path in direct_asset_directories(agents_root)] + [
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


def codex_hook_trust_warnings(home: Path | None = None, script: Path | None = None) -> list[str]:
    """Warn for each declared Codex plugin hook whose installed definition differs from its manifest pin.

    The base modify script trusts such a hook nowhere, so it does not run until it is reviewed. The
    decision comes from the script's own generated hook-trust block, so doctor and apply never disagree.
    """
    home = home or HOME
    script = script or SOURCE_ROOT / "dot_codex/modify_private_config.toml"
    stderr = io.StringIO()
    try:
        block = script.read_text().split("# >>> codex hook trust", 1)[1].split("# <<< codex hook trust", 1)[0]
        namespace: dict[str, object] = {"sys": sys, "Path": Path}
        # The block's refuse() exits for the modify script; here that exit is a finding, never doctor's own exit.
        with contextlib.redirect_stderr(stderr):
            exec(block.split("\n", 1)[1], namespace)
            results = namespace["declared_hook_trust"](str(home))
    except (Exception, SystemExit) as error:  # A broken block must surface, not read as "every hook matches its pin".
        detail = stderr.getvalue().strip() or repr(error)
        return [f"WARN: Codex hook trust: cannot evaluate {script}: {detail}"]
    return [
        f"WARN: Codex hook trust: {warning}" for _key, _entry, _digest, kind, warning in results if kind == "changed"
    ]


PLUGIN_PINS = ROOT / "scripts/plugin-pins.json"
# Marketplaces whose plugins this repository does not pin: the ones OpenAI ships with Codex, and this
# repository's own (crit@mryfmo-personal-plugins is the copy the pinned crit CLI writes, assets.crit).
UNPINNED_CODEX_MARKETPLACES = frozenset(
    {"openai-bundled", "openai-primary-runtime", "openai-curated-remote", "mryfmo-personal-plugins"}
)


def load_pin_records():
    """scripts/pin_records.py, the one strict reader of every record the pin checks use."""
    spec = importlib.util.spec_from_file_location("pin_records", ROOT / "scripts/pin_records.py")
    if spec is None or spec.loader is None:
        raise ImportError("cannot load scripts/pin_records.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["pin_records"] = module
    spec.loader.exec_module(module)
    return module


records = load_pin_records()
RecordError = records.RecordError
present = records.present


def claude_plugin_pin_findings(home: Path, pins: dict) -> list[str]:
    """Fail for a user-scope Claude Code plugin at another version than its pin; warn for unpinned enabled ones.

    make update manages user scope only, the scope this repository installs: the pins are checked against the
    user-scope installations, and "enabled" is read from the user settings it manages. A project- or
    local-scope installation belongs to its project and is reported as not managed, never as a pass. Both
    records are read by pin_records, so a malformed entry is an error, never "not installed".
    """
    findings = []
    claude_dir = records.agent_home("claude", home)
    installed_path = claude_dir / "plugins/installed_plugins.json"
    try:
        installed = records.load_claude_installs(installed_path)
    except RecordError as error:
        return [f"Claude Code plugins: {error}; plugin pins not checked"]
    if installed is None:
        findings.append(
            f"WARN: Claude Code plugins: {installed_path} is missing, so no recorded plugin is installed; run make update"
        )
        installed = {}
    for plugin_id, entries in sorted(installed.items()):
        for entry in entries:
            if entry.scope != "user":
                findings.append(
                    f"WARN: plugin {plugin_id} installed in {entry.scope} scope at "
                    f"{entry.project_path or entry.install_path}: not managed"
                )
    for plugin_id, pin in sorted(pins.items()):
        users = [entry for entry in installed.get(plugin_id, []) if entry.scope == "user"]
        if not users:
            findings.append(f"WARN: Claude Code plugin {plugin_id} is not installed (pin {pin.pin})")
            continue
        # A content pin compares the installed files and the clone's catalog entry (pin_records.content_digest),
        # whatever commit the version names.
        try:
            observed = sorted(
                {
                    (entry.version, records.claude_observed(pin.pin, entry.version, entry.install_path))
                    for entry in users
                }
            )
        except RecordError as error:
            findings.append(f"Claude Code plugin {plugin_id}: {error}; its pin not checked")
            continue
        if {value for _, value in observed} != {pin.pin}:
            at = ", ".join(version if value == version else f"{version} ({value})" for version, value in observed)
            findings.append(
                f"Claude Code plugin {plugin_id} is installed at {at}, not its pin {pin.pin} "
                "(assets.claude-plugins in home/dot_agents/agent-config.yaml); review that release and record it, "
                "or run make update to return to the pin"
            )
    settings_path = claude_dir / "settings.json"
    try:
        enabled = records.load_claude_enabled(settings_path) or {}
    except RecordError as error:
        return [*findings, f"Claude Code plugins: {error}; unpinned plugins not checked"]
    # The user settings this repository manages; an enable only in a project is that project's own.
    for plugin_id in sorted(enabled):
        if enabled[plugin_id] and plugin_id not in pins:
            findings.append(
                f"WARN: Claude Code plugin {plugin_id} is enabled but has no pin in assets.claude-plugins; "
                "record its reviewed version there or disable it"
            )
    return findings


def codex_plugin_pin_findings(home: Path, pins: dict, script: Path) -> list[str]:
    """Fail for a Codex plugin at another version than its pin, one whose content is off its content_sha256 pin, or
    a git marketplace off its ref; warn for an enabled third-party plugin without a pin.

    The copy checked is the one Codex loads (pin_records.load_codex_copy documents Codex's rule), judged by the
    version its manifest declares, as the Claude copy of the same plugin is, and by its content when the pin records
    content_sha256 (pin_records.codex_content: every regular file of the copy except the inert kinds pin_records.INERT
    names; the codex.hooks.state trusted_hash pins cover the hook command strings only). The `ref` pins the
    marketplace catalog snapshot only: `codex plugin marketplace upgrade` fetches the copy from the source the
    catalog names (upstream main for ponytail), so the commit a copy came from is not compared with it; the
    marketplace's install record and the config.toml marketplace table must name the pinned source and ref.
    """
    findings = []
    codex_dir = records.agent_home("codex", home)
    config_path = codex_dir / "config.toml"
    try:
        config = records.load_codex_config(config_path)
    except (RecordError, ImportError) as error:
        return [f"Codex plugins: {error}; plugin pins not checked"]
    for plugin_id, pin in sorted(pins.items()):
        plugin, _, marketplace = plugin_id.partition("@")
        try:
            root = records.confined(PLUGIN_PINS, f"codex.{plugin_id}", codex_dir / "plugins/cache", marketplace, plugin)
            copy = records.load_codex_copy(root, plugin, script)
        except RecordError as error:
            findings.append(f"Codex plugin {plugin_id}: {error}; cannot verify its pin")
            continue
        # The marketplace clone at the pinned ref, when the install record proves it is there: the reference a content
        # finding names the differing files against. The verdict never depends on it, only the names.
        reference = None
        if pin.ref is not None:
            try:
                install_record = (
                    records.confined(PLUGIN_PINS, f"codex.{plugin_id}", codex_dir / ".tmp/marketplaces", marketplace)
                    / ".codex-marketplace-install.json"
                )
                install = records.load_marketplace_install(install_record, pin.marketplace)
                clone_present = present(install_record.parent)
                if config is not None and marketplace in config.marketplaces:
                    records.codex_marketplace_state(config_path, marketplace, pin.marketplace)
            except (RecordError, ImportError) as error:
                findings.append(f"Codex marketplace {marketplace}: {error}")
            else:
                if install is not None and install.revision != pin.ref:
                    findings.append(
                        f"Codex marketplace {marketplace} is at {install.revision}, not its pinned ref {pin.ref}; "
                        "run chezmoi apply, then make update"
                    )
                elif install is None and (copy is not None or clone_present):
                    findings.append(
                        f"Codex marketplace {marketplace}: {install_record} is missing, so its pinned ref {pin.ref} "
                        "cannot be checked; run make update"
                    )
                else:
                    reference = install_record.parent if install is not None else None
        if copy is None:
            findings.append(f"WARN: Codex plugin {plugin_id} is not installed (pin {pin.pin})")
            continue
        if copy.version != pin.pin:
            findings.append(
                f"Codex plugin {plugin_id} is installed at {copy.version}, not its pin {pin.pin} "
                "(assets.codex-plugins in home/dot_agents/agent-config.yaml); review that release and record it"
            )
        if pin.content_sha256 is not None:
            findings.extend(codex_content_findings(plugin_id, pin, root, copy, reference))
    for plugin_id, on in sorted((config.plugins if config else {}).items()):
        third_party = plugin_id.partition("@")[2] not in UNPINNED_CODEX_MARKETPLACES
        if on and third_party and plugin_id not in pins:
            findings.append(
                f"WARN: Codex plugin {plugin_id} is enabled but has no pin in assets.codex-plugins; "
                "record its reviewed version there or disable it"
            )
    return findings


def codex_content_findings(plugin_id: str, pin, root: Path, copy, reference: Path | None) -> list[str]:
    """The content_sha256 check of the Codex copy COPY under ROOT: its files (pin_records.codex_content) against
    the pin. A copy that cannot be read is a finding, never a pass.

    Off the pin, the finding names the files that differ from REFERENCE, the marketplace clone at the pinned ref,
    read by the same function: the per-file hashes computed for the copy's value are kept and compared, nothing is
    hashed twice. Without a usable reference the finding says so instead of naming files.
    """
    copy_dir = records.confined(root, "(version directory)", root, copy.version_dir)
    try:
        content = records.codex_content(copy_dir)
    except RecordError as error:
        return [f"Codex plugin {plugin_id}: {error}; cannot verify its content against its pin content_sha256"]
    if content.sha256 == pin.content_sha256:
        return []
    if reference is None:
        named = "the marketplace clone is not at the pinned ref, so the files that differ are not named"
    else:
        try:
            skip = (*records.CODEX_COPY_SKIP, records.CODEX_MARKETPLACE_RECORD)
            reviewed = records.codex_content(reference, skip).files
        except RecordError as error:
            named = f"the marketplace clone at the pinned ref cannot name the files that differ ({error})"
        else:
            differ = sorted(
                path for path in set(content.files) | set(reviewed) if content.files.get(path) != reviewed.get(path)
            )
            if differ:
                named = "files that differ from the marketplace clone at the pinned ref: " + ", ".join(differ)
            else:
                named = (
                    "no file differs from the marketplace clone at the pinned ref, so the pin itself is not that tree"
                )
    return [
        f"Codex plugin {plugin_id} copy {copy_dir} has content {content.sha256}, not its pin content_sha256 "
        f"{pin.content_sha256} (assets.codex-plugins in home/dot_agents/agent-config.yaml); {named}; review those "
        "files and record the value check-agent-runtime.py --codex-content-sha256 prints for a reviewed copy"
    ]


def gh_extension_pin_findings(home: Path, pins: dict[str, str]) -> list[str]:
    """Fail for a gh extension at another tag than its pin (assets.gh-extensions), installed unpinned, foreign
    (a fork of the same name) or without a readable manifest."""
    gh_dir = records.agent_home("gh", home)
    findings = []
    for repository, pin in sorted(pins.items()):
        try:
            extension = records.load_gh_extension(gh_dir, repository)
        except RecordError as error:
            findings.append(f"gh extension {repository}: {error}; run make update to reinstall it pinned")
            continue
        if extension is None:
            findings.append(
                f"WARN: gh extension {repository} is not installed (pin {pin}); run make update after make gh-auth"
            )
        elif extension.tag != pin:
            findings.append(
                f"gh extension {repository} is installed at {extension.tag}, not its pin {pin}; run make update"
            )
        elif not extension.pinned:
            findings.append(
                f"gh extension {repository} is at its pin {pin} but installed unpinned, so gh extension upgrade "
                "can move it; run make update to reinstall it pinned"
            )
    return findings


def plugin_pin_findings(
    home: Path | None = None, pins_path: Path | None = None, script: Path | None = None
) -> list[str]:
    """Compare every recorded plugin and gh extension pin with what this host runs."""
    home = home or HOME
    pins_path = pins_path or PLUGIN_PINS
    script = script or SOURCE_ROOT / "dot_codex/modify_private_config.toml"
    try:
        pins = records.load_plugin_pins(pins_path)
    except RecordError as error:
        return [f"plugin pins unreadable: {error}"]
    return [
        *claude_plugin_pin_findings(home, pins.claude),
        *codex_plugin_pin_findings(home, pins.codex, script),
        *gh_extension_pin_findings(home, pins.gh_extensions),
    ]


def asset_pin_findings(
    agent: str, asset_id: str, home: Path | None = None, pins_path: Path | None = None, script: Path | None = None
) -> list[str]:
    """The doctor's own pin check for one asset (agent claude, codex or gh; a plugin id or <owner>/<repo>).

    update-agent-assets.sh runs it (--pin-check) after each convergence step, so the updater and the doctor
    never judge a pin differently. The checks run with only that asset's pin, so every error they return
    concerns it (or a record it depends on); a warning about another plugin is dropped.
    """
    home = home or HOME
    pins_path = pins_path or PLUGIN_PINS
    script = script or SOURCE_ROOT / "dot_codex/modify_private_config.toml"
    try:
        pins = records.load_plugin_pins(pins_path)
    except RecordError as error:
        return [f"plugin pins unreadable: {error}"]
    table = {"claude": pins.claude, "codex": pins.codex, "gh": pins.gh_extensions}.get(agent)
    if table is None or asset_id not in table:
        return [f"plugin pins: {agent} {asset_id} is not recorded in {pins_path}"]
    subset = {asset_id: table[asset_id]}
    if agent == "claude":
        findings = claude_plugin_pin_findings(home, subset)
    elif agent == "codex":
        findings = codex_plugin_pin_findings(home, subset, script)
    else:
        findings = gh_extension_pin_findings(home, subset)
    return [finding for finding in findings if not is_warning(finding) or asset_id in finding]


GH_TOKEN_VARIABLES = ("GH_TOKEN", "GITHUB_TOKEN", "GH_ENTERPRISE_TOKEN", "GITHUB_ENTERPRISE_TOKEN")
GH_LOGIN_HINT = "run make gh-auth"


def gh_hosts_file_findings(config_dir: Path | None = None) -> list[str]:
    """Warn unless gh's hosts.yml, when it exists, is a user-owned regular file at mode 0600.

    The file is CONFIG_DIR/hosts.yml, by default gh's own
    `${GH_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/gh}/hosts.yml`, whatever gh reports.
    """
    if config_dir is None:
        xdg = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
        config_dir = Path(os.environ.get("GH_CONFIG_DIR") or xdg / "gh")
    hosts = config_dir / "hosts.yml"
    try:
        info = hosts.lstat()
    except FileNotFoundError:
        return []
    except OSError:
        return [f"WARN: GitHub login: cannot read the mode of {hosts}; {GH_LOGIN_HINT}"]
    mode = info.st_mode & 0o777
    if not stat.S_ISREG(info.st_mode):
        return [f"WARN: GitHub login: {hosts} is not a regular file; {GH_LOGIN_HINT}"]
    if info.st_uid != os.getuid():
        return [f"WARN: GitHub login: {hosts} is not owned by you; {GH_LOGIN_HINT}"]
    if mode != 0o600:
        return [f"WARN: GitHub login: {hosts} has mode {mode:04o}, not 0600; {GH_LOGIN_HINT}"]
    return []


def gh_login_findings(gh: str = "gh", config_dir: Path | None = None) -> list[str]:
    """Report this machine's one GitHub login, the one every seat acts as.

    Present means `gh auth status` finds exactly one account in gh's default
    configuration, it works, and its token sits in gh's own file at mode 0600 (the
    Claude sandbox cannot reach the OS keyring): a `found:` line naming the login.
    Anything else is one warning per problem with the `make gh-auth` hint. The status
    (gh missing or failing, the count, the active login's storage) and gh's hosts.yml
    (`gh_hosts_file_findings`) are checked independently, so the file is checked even
    when gh fails. Never prompts, and never reads or prints a token: the login and its
    token source come from gh's JSON status, with token variables stripped so an
    environment token cannot stand in for the stored login, and CLICOLOR_FORCE
    stripped so gh prints plain JSON.
    """
    file_findings = gh_hosts_file_findings(config_dir)
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
        return [f"WARN: GitHub login: gh auth status failed or gh is missing; {GH_LOGIN_HINT}", *file_findings]
    findings = []
    if len(accounts) != 1 or len(logins) != 1:
        message = (
            f"WARN: GitHub login: gh holds {len(logins)} working of {len(accounts)} logins; keep exactly one "
            f"(gh auth logout --user <login> for any other, or {GH_LOGIN_HINT})"
        )
        findings.append(message)
    # Storage is checked whatever the count and auth state. gh names the file it read a token from; a keyring
    # token shows "keyring", or, inside the sandbox where the keyring is unreachable, "default".
    active = [account for account in accounts if account.get("active")]
    if active and not str(active[0].get("tokenSource", "")).endswith("hosts.yml"):
        findings.append(
            "WARN: GitHub login is stored in the OS keyring, which the Claude sandbox cannot reach; "
            "run make gh-auth to store it in gh's file"
        )
    findings.extend(file_findings)
    if findings:
        return findings
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
    index, index_error = load_output_index()
    if index is None:
        failures.append(str(index_error))
        index = {"outputs": [], "scopes": []}
    working_tree, tree_error = chezmoi_working_tree()
    if working_tree is None:
        failures.append(
            f"cannot read chezmoi's working tree, which the Codex configs key project trust with: {tree_error}"
        )
    failures.extend(generated_target_findings(index, working_tree))
    if not same_text(SOURCE_ROOT / "dot_agents/agent-config.yaml", HOME / ".agents/agent-config.yaml"):
        failures.append(f"agent manifest differs or is missing: {HOME / '.agents/agent-config.yaml'}")
    if not same_modified(
        SOURCE_ROOT / "dot_claude/modify_private_settings.json",
        HOME / ".claude/settings.json",
        json_target=True,
    ):
        failures.append(
            f"Claude settings managed keys differ or settings file is missing: {HOME / '.claude/settings.json'}"
        )
    # The omp merge runs under uv; without uv it passes its input through with a warning, so a host without uv gets a
    # WARN naming what was not checked, and any stderr output from the merge counts as a mismatch, never a pass.
    omp_config = HOME / ".omp/agent/config.yml"
    if shutil.which("uv") is None:
        failures.append(f"WARN: {omp_config} not checked: the omp config merge needs uv, which is not on PATH")
    elif not same_modified(SOURCE_ROOT / "dot_omp/private_agent/modify_private_config.yml", omp_config, quiet=True):
        failures.append(f"omp config managed keys differ or config is missing: {omp_config}")

    failures.extend(compare_shared_skills())
    failures.extend(compare_claude_skills(index["outputs"]))
    if index.get("skills") is not None:
        failures.extend(skill_audience_findings(index["skills"]))
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
    failures.extend(
        check_executable_hook(
            SOURCE_ROOT / "dot_claude/hooks/executable_project-map-reload.sh",
            HOME / ".claude/hooks/project-map-reload.sh",
            "Claude project-map-reload hook",
        )
    )
    manifest_path = HOME / ".agents/.installed-manifest.json"
    manifest_error = installed_manifest_error(manifest_path)
    if manifest_error is not None:
        failures.append(f"installed manifest unreadable or invalid: {manifest_path} ({manifest_error})")
    else:
        # A host where scripts/update-agent-assets.sh never ran has no record to check its assets against (F167). A
        # WARN, never an ERROR: `make apply-check` runs this in a fresh container that installs no assets.
        if not manifest_path.exists() and not manifest_path.is_symlink():
            failures.append(
                f"WARN: installed asset manifest is missing: {manifest_path}; no third-party asset is checked until "
                "make update (scripts/update-agent-assets.sh) records one"
            )
        failures.extend(asset_failure_message(finding) for finding in manifest_asset_findings())
        failures.extend(orphaned_asset_warnings())
    failures.extend(understand_anything_core_warnings())
    failures.extend(codex_hook_trust_warnings())
    failures.extend(plugin_pin_findings())
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
    parser.add_argument(
        "--pin-check",
        nargs=2,
        metavar=("AGENT", "ID"),
        help="run the doctor's pin check for one asset (claude|codex|gh and its id); exit 1 on any error",
    )
    parser.add_argument(
        "--codex-content-sha256",
        metavar="COPY_DIR",
        help="print the content_sha256 pin value of a Codex plugin copy (every file but the inert kinds)",
    )
    args = parser.parse_args(argv)
    if args.pin_check is not None:
        findings = asset_pin_findings(*args.pin_check)
        print_failures(findings)
        return 1 if [finding for finding in findings if not is_warning(finding)] else 0
    if args.codex_content_sha256 is not None:
        try:
            print(records.codex_content(Path(args.codex_content_sha256)).sha256)
        except RecordError as error:
            print(f"ERROR: {error}", file=sys.stderr)
            return 1
        return 0
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
