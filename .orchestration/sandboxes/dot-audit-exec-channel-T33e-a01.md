# T33e sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `fix/audit-exec-channel` from `origin/main` (04746ca). The worktree was
  clean before the switch.
- herdr and codex were exercised only through the fake CLIs of
  `tests/unit/test_herdr_agents.py`, with pre-created transcript and
  last-message files. No codex invocation was made, and no real herdr tab
  or pane was created.
- The validator false positive was inspected by pattern shape only; the
  matched values were redacted and never printed.
- No `make apply` or `chezmoi apply` was run. The local Bats suite was not
  run. There was no force push and no merge.
