"""A user-scope Claude Code installation at its recorded pin, for the tests that need every pinned plugin at its pin.

A version pin is met by the record's version. A content pin (sha256:..., scripts/pin_records.py content_sha256) is met
by the files: the reviewed copy of the plugin under tests/fixtures/claude-plugins/<plugin> is copied into the cache
directory, under the marketplace commit Claude Code would record as its version.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEWED = ROOT / "tests/fixtures/claude-plugins"
# The commit-version a content-pinned plugin is installed under here; any other would do (the content decides).
CONTENT_VERSION = "58267944f921"


def pinned_install(home: Path, plugin_id: str, pin: str) -> dict:
    """The installed_plugins.json entry of PLUGIN_ID at PIN; for a content pin its reviewed files are put in place."""
    plugin, marketplace = plugin_id.split("@", 1)
    version = CONTENT_VERSION if pin.startswith("sha256:") else pin
    install_path = home / ".claude/plugins/cache" / marketplace / plugin / version
    if version != pin:  # lint-comparisons: allow version and pin are plain strings
        shutil.copytree(REVIEWED / plugin, install_path)
    return {"scope": "user", "version": version, "installPath": str(install_path)}
