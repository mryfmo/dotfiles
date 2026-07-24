# T19 validation

Worktree: `/Users/mryfmo/Workspace/dotfiles-t18`
Commit: `968637c`

## `uv run pytest tests/unit/test_herdr_agents.py`

Exit: `0`

```text
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/mryfmo/Workspace/dotfiles-t18
collected 53 items

tests/unit/test_herdr_agents.py ........................................ [ 75%]
.............                                                            [100%]

============================== 53 passed in 4.02s ==============================
```

## TOML parse

Command:

```text
python3 -c "import tomllib,pathlib;
tomllib.loads(pathlib.Path('home/dot_config/herdr/config.toml').read_text());
print('config.toml parses')"
```

Exit: `0`

```text
config.toml parses
```

## `git diff --check`

Exit: `0`

```text
<no output>
```

## Review gate

Command:

```text
env AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/T19-herdr-file-viewer-popup-config-review-receipt.md make require-crit-review
```

Exit: `0`

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```
