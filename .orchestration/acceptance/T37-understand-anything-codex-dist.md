# T37 acceptance

status: accepted (after one revise round)
task_id: T37-understand-anything-codex-dist
reviewed_by: claude-deep-dot (orchestrator)
date: 2026-08-11

## Review history

- Round 1: revise — the copy loop ran `rm -rf` on the destination before
  checking the source existed in the release artifact, so a partial artifact
  could delete a working runtime without replacement; version sort crashed on
  non-numeric directory names.
- Round 2: verified fixed — `[ -d source ] || continue` now precedes the
  delete; version sort falls back to string ordering with a safe empty
  default.

## Independent verification

Orchestrator re-ran `bash -n`, `shellcheck -x`, `shfmt -i 4 -sr -d`, and
`uv run --with pyyaml scripts/validate-agent-assets.py` on the final tree —
all pass. New bats greps, validator tokens, and the README sentence match the
implementation. No live `~/.understand-anything` or `~/.claude/plugins`
mutation occurred (script code only), per the sandbox record.

next_action: orchestrator commits via a separate worktree, opens the PR, and
watches CI; batched T35+T36+T37 evidence sync follows at the regime boundary.
