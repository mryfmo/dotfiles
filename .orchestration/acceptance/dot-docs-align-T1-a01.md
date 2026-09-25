# Acceptance: dot-docs-align-T1-a01

status: revise
date: 2026-09-25
reviewer: claude-deep-dot (orchestrator, adversarial review)
cost: n/a

## Findings

- Items 1-8 are substantively correct (Dockerfile 24.04 build proven green in adh-test VM with cleanup; validator green; unit suite green).
- Blocking: README hunks around L289-L325 (herdr-agents pane split / agent start wording) do not apply onto origin/main c5193e4 because d004ddb and 4d4767b rewrote that section for the manifest-driven worker kind. Must be re-merged against the current README text, preserving the new `worker_kind` wording.
- Shares the worktree with dot-herdr-sheldon-T1-a01; both revise together as one rebase.

## next_action

Same rebase as dot-herdr-sheldon-T1-a01; re-verify `rg` stale-text check and `validate-agent-assets.py` after the rebase; re-send AGMSG-RESULT.
