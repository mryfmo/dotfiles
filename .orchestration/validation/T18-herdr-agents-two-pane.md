# T18 validation

Worktree: `/Users/mryfmo/Workspace/dotfiles-t18`
Commit: `b9b5eab`

## `uv run pytest tests/unit/test_herdr_agents.py`

Exit: `0`

```text
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/mryfmo/Workspace/dotfiles-t18
collected 51 items

tests/unit/test_herdr_agents.py ........................................ [ 78%]
...........                                                              [100%]

============================== 51 passed in 3.91s ==============================
```

## `shellcheck home/dot_local/bin/common/executable_herdr-agents`

Exit: `0`

```text
<no output>
```

## `shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_herdr-agents`

Exit: `0`

```text
<no output>
```

## `grep -c yazi home/dot_local/bin/common/executable_herdr-agents`

Exit: `1` (expected for zero matches)

```text
0
```

## `git diff --check`

Exit: `0`

```text
<no output>
```

## Review gate

Command:

```text
env AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/T18-herdr-agents-two-pane-review-receipt.md make require-crit-review
```

Exit: `0`

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```
