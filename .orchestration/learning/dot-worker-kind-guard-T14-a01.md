# Learning
- Candidate (not promoted): in zsh, an unquoted glob such as `--include=*.bats` that matches nothing aborts the whole command line (`no matches found`), so later chained commands never run. Quote globs meant for the called tool.
- Candidate (not promoted): the Write/Edit PostToolUse formatter (ruff format / prettier) reformats whole files. For minimal diffs in files not already formatter-clean, apply edits with a scripted replace and check `git diff --stat` for unrelated hunks.
- Candidate (not promoted): the claude-worker guard needs every existing claude-kind fixture to register a second claude-code identity. A shared test helper keeps that to one call per test.
No rule or skill promotion.
