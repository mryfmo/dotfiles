"""The reviewed Codex Ponytail plugin copy at its pin, for the tests that need a copy make doctor accepts.

tests/fixtures/ponytail holds upstream's hooks/ tree and .codex-plugin/plugin.json at the pinned ref byte for byte
(SOURCE.json names the commit, the tree and the blob). hooks_sha256 in scripts/plugin-pins.json is their digest, so a
copy built from them is at its pin and a copy with any hook file changed is off it. reviewed_hooks_sha256 is this
module's own reading of the pin's definition, independent of scripts/pin_records.py.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PONYTAIL = ROOT / "tests/fixtures/ponytail"
MANIFEST = ".codex-plugin/plugin.json"


def install_ponytail_copy(copy: Path, version: str | None = None, change: dict[str, bytes] | None = None) -> Path:
    """Write the reviewed tree at COPY. VERSION, when given, replaces the manifest with a minimal one declaring it;
    CHANGE maps relative paths to bytes written over (or added as) those files."""
    shutil.copytree(PONYTAIL / "hooks", copy / "hooks")
    shutil.copytree(PONYTAIL / ".codex-plugin", copy / ".codex-plugin")
    if version is not None:
        (copy / MANIFEST).write_text(json.dumps({"name": "ponytail", "version": version}))
    for relative, data in (change or {}).items():
        path = copy / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return copy


def reviewed_hooks_sha256(copy: Path) -> str:
    """The hooks_sha256 definition written out plainly: sha256 over one line per file, `<relative path> NUL <sha256 hex
    of its bytes> LF`, for every file under hooks/ (recursive, sorted by the bytes of its relative POSIX path), then
    .codex-plugin/plugin.json."""
    files = sorted(
        (path for path in (copy / "hooks").rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(copy).as_posix().encode(),
    )
    lines = [
        path.relative_to(copy).as_posix().encode() + b"\0" + hashlib.sha256(path.read_bytes()).hexdigest().encode()
        for path in files
    ]
    lines.append(MANIFEST.encode() + b"\0" + hashlib.sha256((copy / MANIFEST).read_bytes()).hexdigest().encode())
    return hashlib.sha256(b"".join(line + b"\n" for line in lines)).hexdigest()


def git_tree_id(directory: Path) -> str:
    """The git tree object id of DIRECTORY's files as plain 100644 blobs (upstream's hooks/ holds nothing else), so a
    fixture can be checked against the tree id `git ls-tree` prints upstream."""
    entries = []
    for path in sorted(directory.iterdir(), key=lambda path: path.name.encode() + (b"/" if path.is_dir() else b"")):
        if path.is_dir():
            mode, object_id = b"40000", bytes.fromhex(git_tree_id(path))
        else:
            data = path.read_bytes()
            mode, object_id = b"100644", hashlib.sha1(b"blob %d\0" % len(data) + data).digest()
        entries.append(mode + b" " + path.name.encode() + b"\0" + object_id)
    body = b"".join(entries)
    return hashlib.sha1(b"tree %d\0" % len(body) + body).hexdigest()
