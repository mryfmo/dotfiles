"""Keep git from starting background work in the tests' scratch repositories (regime-cutover U100).

`git commit` and other writing commands run `git maintenance run --auto` after their work, and with
maintenance.autoDetach (default true) it detaches and keeps running, holding `.git/objects/maintenance.lock`.
A test that removes its scratch repository right after a commit then races that process: PR #559's
`shutil.rmtree` failed with `FileNotFoundError: 'maintenance.lock'` (test_pinned_lint_tools, ubuntu-24.04).
Measured with git 2.56: after three commits the lock was there in 187 of 200 fresh repositories, and in none
with maintenance.auto=false.

The settings below go into the environment as `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n`
(git-config(1), ENVIRONMENT), which git reads like `-c` options, so they win over any repository's config:
- maintenance.auto=false: no command starts `git maintenance run --auto` (git-config(1), maintenance.auto);
- maintenance.autoDetach=false and gc.autoDetach=false: anything that still runs maintenance or `gc --auto`
  stays in the foreground;
- gc.auto=0: `git gc --auto` does nothing.

Two layers, as agent_home_isolation has:
- quiet_git() (module level in every test module that creates a git repository; test_scratch_git checks
  that): adds them to os.environ, so every subprocess that inherits the environment has them.
- quiet_git_env(env) (every env a test builds from scratch for git): adds them to that env.
"""

from __future__ import annotations

import os
from typing import Mapping

SETTINGS = (
    ("maintenance.auto", "false"),
    ("maintenance.autoDetach", "false"),
    ("gc.autoDetach", "false"),
    ("gc.auto", "0"),
)


def quiet_git_env(env: Mapping[str, str] | None = None) -> dict[str, str]:
    """ENV (default empty) with SETTINGS appended to its GIT_CONFIG_* entries; entries already there stay first."""
    result = dict(env or {})
    count = int(result.get("GIT_CONFIG_COUNT") or 0)
    present = {(result.get(f"GIT_CONFIG_KEY_{i}"), result.get(f"GIT_CONFIG_VALUE_{i}")) for i in range(count)}
    for key, value in SETTINGS:
        if (key, value) in present:
            continue
        result[f"GIT_CONFIG_KEY_{count}"] = key
        result[f"GIT_CONFIG_VALUE_{count}"] = value
        count += 1
    result["GIT_CONFIG_COUNT"] = str(count)
    return result


def quiet_git() -> None:
    """Apply SETTINGS to this process's environment, for every git command a test runs without an env of its own."""
    os.environ.update(quiet_git_env(os.environ))
