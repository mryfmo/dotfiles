# T32b sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `fix/audit-pane-hardening` from `origin/main` (c48e614). The worktree was
  clean before the switch.
- herdr and codex were exercised only through the fake CLIs of
  `tests/unit/test_herdr_agents.py`. The test-side decoder runs `bash`
  `eval "set -- …"` with an empty PATH, so nothing it decodes can execute a
  binary. No real herdr tab or pane was created and no codex was invoked.
- The mutation baseline ran the new tests against the untouched 6b9babc
  script: I edited the tests first and confirmed the script had no diff
  against `origin/main` before running them.
- No `make apply` or `chezmoi apply` was run. The local Bats suite was not run
  (repo policy). There was no force push and no merge.
