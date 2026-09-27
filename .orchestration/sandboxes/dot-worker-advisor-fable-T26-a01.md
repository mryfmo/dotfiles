# Sandbox

OpenSandbox not used.

- Writes: worktree `.claude/worktrees/worker-c` only, on branch `feat/worker-advisor-fable` from origin/main `030273d`; one commit `a63666b`, pushed; opened PR #188. In the main checkout, only these five `.orchestration` artifacts and one CompactionDB decision record (`a7c20de3-85d6-460c-91e4-3264ddefda5e`).
- Live herdr: read-only `herdr agent --help` / `herdr agent send-keys --help` only, to confirm that the `send-keys <TARGET> <KEY>...` form exists. No pane, agent, or workspace was touched. Tests use only the fake-herdr pattern, plus a no-op `sleep` shim in the test bin dir.
- Not run: `make apply`, `chezmoi apply`, local bats, merge, force push, the Understand-Anything graph update (`.ua/` is outside allowed_files).
