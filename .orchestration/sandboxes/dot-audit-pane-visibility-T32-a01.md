# T32 sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `feat/audit-pane-visibility` created from `origin/main` (7f3164e). The
  worktree was clean before the switch.
- herdr and codex were exercised only through fake CLIs in
  `tests/unit/test_herdr_agents.py`, under a temporary HOME and PATH. No real
  herdr tab, pane, or codex process was created or run on this host.
- The read-only host herdr calls were `--help` pages, `herdr tab list`,
  `herdr pane list`, and one timed-out `pane wait-output` probe on the
  orchestrator pane. That probe is flagged in the report.
- The mutation baseline temporarily replaced the script with
  `git show origin/main:<script>`, ran the new tests, then restored the saved
  T32 copy from the scratchpad. `git diff --stat` afterwards confirmed the T32
  version was back.
- No `make apply` or `chezmoi apply` was run. The local Bats suite was not run
  (repo policy). There was no force push and no merge.
