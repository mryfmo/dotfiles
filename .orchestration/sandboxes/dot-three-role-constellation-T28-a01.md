# T28 sandbox record

- OpenSandbox was not used; the change is a manifest/generator/validator edit
  with hermetic unit tests (temp ROOT fixtures) plus the repo's own
  `--check`/`validate-agent-assets` gates.
- Git work used the dedicated worker worktree `.claude/worktrees/worker-c` on
  branch `feat/three-role-constellation` created from `origin/main` (eb3cd4b).
- No `make apply`/`chezmoi apply` was run; `~/.codex/audit.config.toml` does
  not exist on this host yet (it appears after the orchestrator's next apply).
- `codex --profile <name> review --commit HEAD` probes were run read-only in
  the worktree under `timeout 8` to capture only the session header (model,
  sandbox, effort); each probe was killed before any review output.
- The local Bats suite was not run (repo policy); bats runs in CI.
