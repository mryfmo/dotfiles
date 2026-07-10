# T10 Herdr Files Pane Validation

## 1. Bash syntax

Command:

```text
bash -n home/dot_local/bin/common/executable_herdr-agents
```

Exit code: `0`

Output: none.

## 2. ShellCheck

Command:

```text
shellcheck home/dot_local/bin/common/executable_herdr-agents
```

Exit code: `0`

ShellCheck findings: none.

Environment warning emitted by mise while resolving the command:

```text
mise WARN  failed to write cache file: /Users/mryfmo/Library/Caches/mise/gcloud/575.0.0/exec_env_effb79b8cb720327-3c8cd.msgpack.z Operation not permitted (os error 1)
```

The warning is unrelated to the checked script and did not affect the exit code.

## 3. Unit tests

Command:

```text
make unit-test
```

Exit code: `0`

Output summary:

```text
uv run python -m unittest discover -s tests/unit -v
Ran 82 tests in 6.503s
OK
```

Relevant passing tests included:

- `test_uses_initial_workspace_pane_for_claude_and_splits_codex_right`
- `test_ghostty_herdr_starts_left_right_agents_with_working_agmsg`
- `test_existing_workspace_adds_missing_files_pane`
- `test_existing_files_pane_is_not_reused_for_claude_or_split_again`
- `test_existing_agents_workspace_focuses_without_recreating_agents`

## Supporting checks

Focused command before the full suite:

```text
uv run python -m unittest tests.unit.test_herdr_agents -v
Ran 20 tests in 1.671s
OK
```

`git diff --check` exited `0` with no output.

## Review guard

Command:

```text
make require-crit-review
```

Exit code: `2` (expected review gate)

Output summary:

```text
Native agent review required before completion.
- review-sensitive path changed: .orchestration/autoskill/runs/T10-herdr-files-pane.md
- broad diff touches 8 files
- broad diff changes 369 lines
```

The task remains `ready_for_review`. No Crit JSON or receipt was created because
the task's allowed-files list does not include an additional review evidence
path.
