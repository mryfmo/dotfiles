"""Keep git from starting background work in the tests' scratch repositories (regime-cutover U100).

`git commit` and other writing commands run `git maintenance run --auto` after their work, and with
maintenance.autoDetach (default true) it detaches and keeps running. Since git 2.55 it holds
`.git/objects/maintenance.lock` while it runs (RelNotes/2.55.0.adoc: "git maintenance" that goes background did
not use the lockfile ..., which has been corrected). A test that removes or lists its scratch repository right
after a commit then races that process: PR #559's `shutil.rmtree` failed with `FileNotFoundError:
'maintenance.lock'` (test_pinned_lint_tools), and main's test_hcom_seat dry-run test saw the lock in its `.git`
listing (ubuntu-24.04, git 2.55.0). Measured with git 2.56: after three commits the lock was there in 187 of 200
fresh repositories, and in none with maintenance.auto=false.

The settings, per git-config(1):
- maintenance.auto=false: no command starts `git maintenance run --auto`;
- maintenance.autoDetach=false and gc.autoDetach=false: anything that still runs maintenance or `gc --auto`
  stays in the foreground;
- gc.auto=0: `git gc --auto` does nothing.

Layers:
- git_init()/git_clone() (every repository a test creates; test_scratch_git's sweep checks the call sites):
  create the repository and write the settings into its own config, so no env a later git runs under can drop
  them, not even one that strips every GIT_* variable;
- quiet_git_env(env): the shard runner (scripts/ci/unittest-shards.py) passes quiet_git_env(os.environ) to every
  shard, and every env a test builds from scratch for git is wrapped with it.

The environment layers use `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n` (git-config(1),
ENVIRONMENT), which git reads like `-c` options, after every config file; the last value of a key wins.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Mapping

SETTINGS = (
    ("maintenance.auto", "false"),
    ("maintenance.autoDetach", "false"),
    ("gc.autoDetach", "false"),
    ("gc.auto", "0"),
)


def quiet_git_env(env: Mapping[str, str] | None = None) -> dict[str, str]:
    """ENV (default empty) with SETTINGS appended after its GIT_CONFIG_* entries.

    Always appended, never merged with an entry already there: git takes the last value of a key, so the settings
    win over any earlier entry for the same key, and applying this twice leaves the same effective values."""
    result = dict(env or {})
    count = int(result.get("GIT_CONFIG_COUNT") or 0)
    for key, value in SETTINGS:
        result[f"GIT_CONFIG_KEY_{count}"] = key
        result[f"GIT_CONFIG_VALUE_{count}"] = value
        count += 1
    result["GIT_CONFIG_COUNT"] = str(count)
    return result


def quiet_repository(path: Path) -> None:
    """Append SETTINGS to the config of the repository at PATH: a work tree whose .git is a directory or a
    `gitdir:` file, or a bare repository. Written by Python, so a test's fake git logs no extra call."""
    dotgit = path / ".git"
    if dotgit.is_dir():
        gitdir = dotgit
    elif dotgit.is_file():
        gitdir = Path(dotgit.read_text().removeprefix("gitdir:").strip())
        gitdir = gitdir if gitdir.is_absolute() else path / gitdir
    else:
        gitdir = path
    config = gitdir / "config"
    if not config.is_file():
        raise FileNotFoundError(f"no repository config at {config}")
    sections: dict[str, list[str]] = {}
    for key, value in SETTINGS:
        section, name = key.split(".")
        sections.setdefault(section, []).append(f"\t{name} = {value}\n")
    with config.open("a") as handle:
        handle.write("".join(f"[{section}]\n{''.join(lines)}" for section, lines in sections.items()))


def _run(argv: list[str], env: Mapping[str, str] | None, cwd: Path | str | None) -> None:
    subprocess.run(argv, cwd=cwd, env=quiet_git_env(os.environ if env is None else env), check=True, timeout=120)


def git_init(path: Path | str, *options: str, env: Mapping[str, str] | None = None, cwd=None) -> Path:
    """`git init -q OPTIONS PATH` under ENV (default os.environ) plus SETTINGS, then SETTINGS in the new repository's
    own config. Returns PATH."""
    _run(["git", "init", "-q", *options, str(path)], env, cwd)
    path = Path(cwd or ".", path)
    quiet_repository(path)
    return path


def git_clone(source: Path | str, path: Path | str, *options: str, env: Mapping[str, str] | None = None, cwd=None):
    """`git clone -q OPTIONS SOURCE PATH` under ENV (default os.environ) plus SETTINGS, then SETTINGS in the clone's
    own config. Returns PATH."""
    _run(["git", "clone", "-q", *options, str(source), str(path)], env, cwd)
    path = Path(cwd or ".", path)
    quiet_repository(path)
    return path
