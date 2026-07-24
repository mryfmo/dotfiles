# T11 validation evidence

## Required commands

### `uv run pytest tests/unit/test_agmsg_join_unique_guard.py -v`

Exit: 2

```text
error: Failed to spawn: `pytest`
  Caused by: No such file or directory (os error 2)
```

### `uv run pytest tests/unit -q`

Exit: 2

```text
error: Failed to spawn: `pytest`
  Caused by: No such file or directory (os error 2)
```

### `shellcheck home/dot_agents/skills/agmsg/scripts/executable_join.sh`

Available. Exit: 0. Full output: empty.

### `git diff --stat`

Exit: 0

```text
 .../skills/agmsg/scripts/executable_join.sh        |  44 ++++++-
 home/dot_mise/config.toml                          |  16 +--
 home/dot_mise/mise.lock                            | 132 +++++++++++----------
 3 files changed, 116 insertions(+), 76 deletions(-)
```

The two mise files were pre-existing dirty files named in the task and were not touched. Git omits the untracked new test from ordinary `git diff --stat`. Task-scoped stats:

```text
 .../skills/agmsg/scripts/executable_join.sh        | 44 ++++++++++++++++++++--
 1 file changed, 40 insertions(+), 4 deletions(-)
 .../unit/test_agmsg_join_unique_guard.py           | 93 ++++++++++++++++++++++
 1 file changed, 93 insertions(+)
```

## Passing fallback checks

### Direct execution of the four plain test functions

Exit: 0

```text
PASS test_cross_team_identity_reuse_fails_without_writing
PASS test_join_into_new_team_succeeds
PASS test_same_agent_flag_allows_cross_team_identity_reuse
PASS test_same_team_rejoin_extends_registration
```

The `--same-agent` test inserts the flag at every index from 0 through 4.

### Syntax and whitespace

- `bash -n home/dot_agents/skills/agmsg/scripts/executable_join.sh`: PASS
- `git diff --check`: PASS

### Existing unittest discovery

`python3 -m unittest discover tests/unit -q` ran 145 tests. It reported 10 errors, all from `test_claude_settings_merge` invoking the same unavailable `uv run python` environment; no T11 test or join guard failure occurred.

## RED evidence before implementation

```text
first_status=0
second_status=0
second_config_exists=yes
second_stderr=
```

This demonstrated the original cross-team collision and write before the guard was added.

## Review gate

`make require-crit-review` exited 1 and requested native agent review. Its scope includes 51 files and 3671 lines because the shared worktree contains many pre-existing untracked orchestration/docs files. No bypass environment variable was used. Crit JSON and receipt creation are left to the orchestrator because the required `.agents/worklog/...` paths are outside the T11 allowed-file list.
