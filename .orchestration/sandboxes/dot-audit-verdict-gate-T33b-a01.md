# T33b sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `fix/audit-verdict-gate` from `origin/main` (4e112fd). The worktree was
  clean before the switch.
- herdr and codex were exercised only through the fake CLIs of
  `tests/unit/test_herdr_agents.py`, with pre-created evidence files. No
  codex invocation was made at all, not even `--help`, and no real herdr
  tab or pane was created.
- The mutation baseline ran the new tests against the untouched
  `origin/main` script: the tests were written first and the script diff was
  checked before the run.
- No `make apply` or `chezmoi apply` was run. The local Bats suite was not
  run. There was no force push and no merge.
