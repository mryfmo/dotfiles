"""A small Codex plugin copy for the tests that need one make doctor can judge by its content.

tests/fixtures/ponytail is synthetic: a dozen tiny files covering the kinds a plugin copy holds, the code,
configuration and instructions the content pin covers (a hook, .mcp.json, the manifests, a script, a skill) and
the inert files it leaves out (the README, a document under docs/, an image, the translated README, upstream CI,
the licence). Its manifest points `skills` at ./docs/skills/, so docs/skills/y/SKILL.md is pinned although it is
under docs/ (the manifest names the tree, so Codex loads it), while docs/guide.md beside it stays inert;
skills/x/SKILL.md is an instruction file outside every tree the manifest names and is pinned because Markdown is
never inert by convention. hooks/claude-codex-hooks.json alone is upstream's file verbatim, because the
codex.hooks.state trusted_hash pins are recorded from it. No recorded pin hashes this tree: the ponytail
content_sha256 in scripts/plugin-pins.json is computed from a scratch clone of upstream at the pinned ref, and a
test that needs a copy at that pin records reviewed_content_sha256 of the copy it builds. reviewed_content_sha256
is this module's own reading of the pin's definition, independent of scripts/pin_records.py.
"""

from __future__ import annotations

import hashlib
import json
import os
import posixpath
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PONYTAIL = ROOT / "tests/fixtures/ponytail"
MANIFEST = ".codex-plugin/plugin.json"
IMAGES = (".svg", ".png", ".jpg", ".jpeg", ".gif", ".ico")
READMES = ("README", "README.md", "README.txt", "README.rst")


def install_ponytail_copy(copy: Path, version: str | None = None, change: dict[str, bytes] | None = None) -> Path:
    """Write the fixture tree at COPY. VERSION, when given, replaces the manifest with a minimal one declaring it;
    CHANGE maps relative paths to bytes written over (or added as) those files."""
    shutil.copytree(PONYTAIL, copy, dirs_exist_ok=True)
    if version is not None:
        (copy / MANIFEST).write_text(json.dumps({"name": "ponytail", "version": version}))
    for relative, data in (change or {}).items():
        path = copy / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return copy


def strings(node: object) -> list[str]:
    """Every string value anywhere in the parsed JSON NODE."""
    if isinstance(node, dict):
        return [value for child in node.values() for value in strings(child)]
    if isinstance(node, list):
        return [value for child in node for value in strings(child)]
    return [node] if isinstance(node, str) else []


def referenced(copy: Path) -> list[str]:
    """The paths COPY's manifest points at, written out plainly: every string value anywhere in the manifest that
    starts with ./ or names an existing path relative to the copy, as a normalized relative POSIX path (`.` is the
    copy itself)."""
    manifest = json.loads((copy / MANIFEST).read_text())
    return [
        posixpath.normpath(value)
        for value in strings(manifest)
        if value.startswith("./") or (value and not value.startswith("/") and os.path.lexists(copy / value))
    ]


def inert(relative: str, referenced: list[str] | tuple[str, ...] = ()) -> bool:
    """The files Codex never loads, written out plainly: nothing under a path the manifest names (REFERENCED) is
    inert; elsewhere a README with a documentation extension (none, .md, .txt, .rst) at any depth, everything
    under docs/, i18n/ and .github/, a top-level LICENSE*, an image anywhere and the top-level .gitignore are.
    Markdown as such is not inert: a skill, an AGENTS.md or any other instruction file is pinned; a README.js or
    README.sh is code and pinned."""
    if any(root == "." or relative == root or relative.startswith(root + "/") for root in referenced):
        return False
    name = relative.rsplit("/", 1)[-1]
    return (
        name in READMES
        or ("/" not in relative and name.startswith("LICENSE"))
        or name.endswith(IMAGES)
        or relative == ".gitignore"
        or relative.startswith((".github/", "i18n/", "docs/"))
    )


def reviewed_content_sha256(copy: Path) -> str:
    """The content_sha256 definition written out plainly: sha256 over one line per file, `<relative path> NUL <sha256
    hex of its bytes> LF`, for every file of COPY that is not inert given the trees its manifest names, sorted by the
    bytes of its relative POSIX path. The top-level .git is skipped only when it is a real directory; a regular file
    named .git is a file like any other."""
    git = copy / ".git"
    skip_git = git.is_dir() and not git.is_symlink()
    relatives = sorted(
        (
            path.relative_to(copy).as_posix()
            for path in copy.rglob("*")
            if path.is_file() and not (skip_git and path.relative_to(copy).parts[0] == ".git")
        ),
        key=str.encode,
    )
    trees = referenced(copy)
    lines = [
        relative.encode() + b"\0" + hashlib.sha256((copy / relative).read_bytes()).hexdigest().encode() + b"\n"
        for relative in relatives
        if not inert(relative, trees)
    ]
    return hashlib.sha256(b"".join(lines)).hexdigest()
