"""Keep every directory an agent tool resolves inside a test's scratch tree.

pin_records.agent_home, update-agent-assets.sh, upgrade-tools.sh and install/common/gh_extensions.sh read
HOME, XDG_DATA_HOME, GH_DATA_DIR, GH_CONFIG_DIR, CLAUDE_CONFIG_DIR and CODEX_HOME. A test that inherits any of
them from the operator's shell can act on the real ~/.claude, ~/.codex or gh extensions (regime-cutover U73
round 15 deleted the operator's gh-poi that way). Two layers:

- isolate_agent_homes() (each harness module's setUpModule): HOME becomes a scratch directory and the other
  five are removed, so a test that runs a script without an env of its own resolves everything under the
  scratch HOME, and one that sets only HOME resolves everything under that fixture home.
- scratch_env(home) (each harness helper that builds a subprocess env): all six set explicitly under the
  fixture home, with the tools' own defaults, and checked by assert_isolated.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import Mapping

VARIABLES = ("HOME", "XDG_DATA_HOME", "GH_DATA_DIR", "GH_CONFIG_DIR", "CLAUDE_CONFIG_DIR", "CODEX_HOME")
SCRATCH_ROOT = Path(os.path.realpath(tempfile.gettempdir()))
_saved: dict[str, str | None] | None = None
_root: Path | None = None


def under_scratch(value: str) -> bool:
    try:
        Path(os.path.realpath(value)).relative_to(SCRATCH_ROOT)
    except ValueError:
        return False
    return True


def assert_isolated(env: Mapping[str, str]) -> None:
    """Fail unless every agent-home variable in ENV is set and lies under the temporary directory."""
    for name in VARIABLES:
        value = env.get(name)
        if not value:
            raise AssertionError(f"{name} is unset in a test env, so the tool would fall back to a real directory")
        if not under_scratch(value):
            raise AssertionError(f"{name}={value!r} is not under {SCRATCH_ROOT}: a test env inherited a real path")


def scratch_env(home: Path, **overrides: str) -> dict[str, str]:
    """The six variables for fixture HOME, with each tool's default layout; OVERRIDES replace some of them."""
    home = Path(home)
    env = {
        "HOME": str(home),
        "XDG_DATA_HOME": str(home / ".local/share"),
        "GH_DATA_DIR": str(home / ".local/share/gh"),
        "GH_CONFIG_DIR": str(home / ".config/gh"),
        "CLAUDE_CONFIG_DIR": str(home / ".claude"),
        "CODEX_HOME": str(home / ".codex"),
        **overrides,
    }
    if "XDG_DATA_HOME" in overrides and "GH_DATA_DIR" not in overrides:
        env["GH_DATA_DIR"] = str(Path(overrides["XDG_DATA_HOME"]) / "gh")  # gh's own order
    assert_isolated(env)
    return env


def complete_env(env: Mapping[str, str]) -> dict[str, str]:
    """ENV with every agent-home variable it leaves unset derived from its HOME, then checked.

    An ENV without HOME gets the process's (scratch, under isolate_agent_homes) one: with no HOME at all a tool
    falls back to the password database, which names the operator's real home.
    """
    result = dict(env)
    result.setdefault("HOME", os.environ["HOME"])
    for name, value in scratch_env(Path(result["HOME"])).items():
        if not result.get(name):
            result[name] = value
    assert_isolated(result)
    return result


def isolate_agent_homes() -> Path:
    """setUpModule: a scratch HOME for the process, the other five removed; undone by restore_agent_homes."""
    global _saved, _root
    if _saved is None:
        _saved = {name: os.environ.get(name) for name in VARIABLES}
        _root = Path(tempfile.mkdtemp(prefix="agent-homes-"))
    home = _root / "home"
    home.mkdir(exist_ok=True)
    os.environ["HOME"] = str(home)
    for name in VARIABLES[1:]:
        os.environ.pop(name, None)
    assert_isolated(complete_env(os.environ))
    return home


def restore_agent_homes() -> None:
    """tearDownModule: put the process environment back and remove the scratch HOME."""
    global _saved, _root
    if _saved is None:
        return
    for name, value in _saved.items():
        if value is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = value
    shutil.rmtree(_root, ignore_errors=True)
    _saved = _root = None
