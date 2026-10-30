"""A small Codex plugin copy for the tests that need one make doctor can judge by its content.

tests/fixtures/ponytail is synthetic: a dozen tiny files covering the kinds a plugin copy holds, the code and
configuration the content pin covers (a hook, .mcp.json, the manifests, a script) and the inert kinds it leaves
out (Markdown, an image, the translated README, upstream CI, the licence). hooks/claude-codex-hooks.json alone is
upstream's file verbatim, because the codex.hooks.state trusted_hash pins are recorded from it. No recorded pin
hashes this tree: the ponytail content_sha256 in scripts/plugin-pins.json is computed from a scratch clone of
upstream at the pinned ref, and a test that needs a copy at that pin records reviewed_content_sha256 of the copy it
builds. reviewed_content_sha256 is this module's own reading of the pin's definition, independent of
scripts/pin_records.py.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PONYTAIL = ROOT / "tests/fixtures/ponytail"
MANIFEST = ".codex-plugin/plugin.json"
IMAGES = (".svg", ".png", ".jpg", ".jpeg", ".gif", ".ico")


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


def inert(relative: str) -> bool:
    """The inert kinds, written out plainly: Markdown anywhere, a top-level LICENSE*, an image anywhere, the top-level
    .gitignore, and everything under .github/, i18n/ and docs/."""
    name = relative.rsplit("/", 1)[-1]
    return (
        name.endswith(".md")
        or ("/" not in relative and name.startswith("LICENSE"))
        or name.endswith(IMAGES)
        or relative == ".gitignore"
        or relative.startswith((".github/", "i18n/", "docs/"))
    )


def reviewed_content_sha256(copy: Path) -> str:
    """The content_sha256 definition written out plainly: sha256 over one line per file, `<relative path> NUL <sha256
    hex of its bytes> LF`, for every file of COPY that is not inert, sorted by the bytes of its relative POSIX path.
    The top-level .git is skipped only when it is a real directory; a regular file named .git is a file like any
    other."""
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
    lines = [
        relative.encode() + b"\0" + hashlib.sha256((copy / relative).read_bytes()).hexdigest().encode() + b"\n"
        for relative in relatives
        if not inert(relative)
    ]
    return hashlib.sha256(b"".join(lines)).hexdigest()
