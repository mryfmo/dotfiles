"""A small Codex plugin copy for the tests that need one make doctor can judge by its content.

tests/fixtures/ponytail is synthetic: a dozen tiny files covering the kinds a plugin copy holds, the code,
configuration and instructions the content pin covers (a hook, .mcp.json, the manifests, a script, a skill) and
the inert files it leaves out (the README, a document under docs/, an image, the translated README, upstream CI,
the licence). Its manifest points `skills` at ./docs/skills/, so docs/skills/y/SKILL.md is pinned although it is
under docs/ (the reference reaches the file, so Codex loads it), while docs/guide.md beside it stays inert;
skills/x/SKILL.md is an instruction file no manifest reference reaches and is pinned because Markdown is
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


def identity(path: Path) -> tuple[int, int]:
    """What the filesystem knows PATH as, whatever name reaches it: its lstat (st_dev, st_ino)."""
    status = os.lstat(path)
    return (status.st_dev, status.st_ino)


def referenced(copy: Path) -> set[tuple[int, int]]:
    """The files COPY's manifest points at, by filesystem identity, written out plainly: every string value anywhere
    in the manifest that starts with ./ or names an existing path relative to the copy is resolved by the
    filesystem (so ./DOCS/skills/ reaches docs/skills/ where names are case-insensitive, and nothing where they
    are not); a reference to a file contributes that file, one to a directory every file below it."""
    manifest = json.loads((copy / MANIFEST).read_text())
    identities = set()
    for value in strings(manifest):
        if value.startswith("./") or (value and not value.startswith("/") and os.path.lexists(copy / value)):
            target = copy / posixpath.normpath(value)
            if target.is_file():
                identities.add(identity(target))
            elif target.is_dir():
                identities.update(identity(path) for path in target.rglob("*") if path.is_file())
    return identities


def inert(relative: str) -> bool:
    """The files Codex never loads by convention, written out plainly: a README with a documentation extension
    (none, .md, .txt, .rst) at any depth, everything under docs/, i18n/ and .github/, a top-level LICENSE*, an
    image anywhere and the top-level .gitignore. Markdown as such is not inert: a skill, an AGENTS.md or any other
    instruction file is pinned; a README.js or README.sh is code and pinned. The convention applies only to a
    file the manifest does not point at (referenced, by identity); reviewed_content_sha256 asks it about those."""
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
    hex of its bytes> LF`, for every file of COPY its manifest points at (by identity) or that is not inert, sorted
    by the bytes of its relative POSIX path. The top-level .git is skipped only when it is a real directory; a
    regular file named .git is a file like any other."""
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
    pointed = referenced(copy)
    lines = [
        relative.encode() + b"\0" + hashlib.sha256((copy / relative).read_bytes()).hexdigest().encode() + b"\n"
        for relative in relatives
        if identity(copy / relative) in pointed or not inert(relative)
    ]
    return hashlib.sha256(b"".join(lines)).hexdigest()
