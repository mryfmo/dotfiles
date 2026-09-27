# T27 sandbox record

- OpenSandbox was not used; the change is a bounded shell-function edit with
  hermetic unit tests (fake `herdr`/`jq` on PATH, temp HOME).
- Git work used the dedicated worker worktree
  `.claude/worktrees/worker-c` on branch `fix/restart-worker-name-wait`
  created from `origin/main` (02a0069).
- No live herdr session, workspace, or pane was touched; live `--restart-worker`
  E2E is left to the orchestrator.
- The local Bats suite was not run (repo policy); bats runs in CI.
