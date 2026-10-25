"""A user-scope Claude Code installation at its recorded pin, for the tests that need every pinned plugin at its pin.

A version pin is met by the record's version. A content pin (sha256:..., scripts/pin_records.py content_digest) is met
by what Claude Code loads: the reviewed copy of the plugin under tests/fixtures/claude-plugins/<plugin> is copied into
the cache directory, under the marketplace commit Claude Code would record as its version, and the reviewed catalog
entry under tests/fixtures/claude-plugins/marketplaces/<marketplace> into the installed marketplace clone.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEWED = ROOT / "tests/fixtures/claude-plugins"
# The commit-version a content-pinned plugin is installed under here; any other would do (the content decides).
CONTENT_VERSION = "58267944f921"


def install_reviewed(home: Path, plugin_id: str, version: str = CONTENT_VERSION) -> Path:
    """Put PLUGIN_ID's reviewed tree in its cache directory at VERSION and its reviewed marketplace clone in place."""
    plugin, marketplace = plugin_id.split("@", 1)
    install_path = home / ".claude/plugins/cache" / marketplace / plugin / version
    shutil.copytree(REVIEWED / plugin, install_path)
    clone = home / ".claude/plugins/marketplaces" / marketplace
    shutil.copytree(REVIEWED / "marketplaces" / marketplace, clone, dirs_exist_ok=True)
    return install_path


def pinned_install(home: Path, plugin_id: str, pin: str) -> dict:
    """The installed_plugins.json entry of PLUGIN_ID at PIN; for a content pin its reviewed files are put in place."""
    plugin, marketplace = plugin_id.split("@", 1)
    if pin.startswith("sha256:"):
        return {"scope": "user", "version": CONTENT_VERSION, "installPath": str(install_reviewed(home, plugin_id))}
    install_path = home / ".claude/plugins/cache" / marketplace / plugin / pin
    return {"scope": "user", "version": pin, "installPath": str(install_path)}
