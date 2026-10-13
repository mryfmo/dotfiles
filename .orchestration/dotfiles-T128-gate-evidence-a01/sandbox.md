---
task_id: dotfiles-T128-gate-evidence-a01
seat: claude-standard-dot-a002
---

# Sandbox record: dotfiles-T128-gate-evidence-a01

- Period: from the AGMSG-TASK (2026-10-12T11:58:43Z) to the RESULT. Edits, the unit tests, ruff, prettier, the mutation checks, the records-only `make require-crit-review` and the commit ran inside the sandbox. No `allowed_domains`.
- Worktree `.claude/worktrees/worker-f`, branch `regime/gate-evidence` from `origin/main` `683384ea` (`git switch -c regime/gate-evidence --no-track origin/main`, so `.git/config` gained no upstream). The parked branch `docs/worker-stop-and-watch` (PR #323) was left as it is.
- Two sandbox effects on test runs, both environment-only (no file changed for them):
  - The global `commit.gpgsign` reads `~/.ssh/id_ed25519.pub`, which the sandbox denies, so every `git commit` inside the test fixtures failed (`Couldn't load public key … fatal: failed to write commit object`) and the module showed 73 failures on unmodified `origin/main`. Every test run therefore sets `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` for its own process; with it, `origin/main` runs 71 tests OK (validation §2). The branch commit uses `git -c commit.gpgsign=false`.
  - PyPI is not reachable from the sandbox; `--with pyyaml` runs use `UV_OFFLINE=1` (the uv cache).
- The full unit suite shows 68 failures and 10 errors in six other modules (`test_agent_stop_gate`, `test_aws_cli_acquisition`, `test_gh_auth`, `test_herdr_agents`, `test_runtime_health`, `test_supply_chain_policy`) on this branch and the same set on `origin/main` (validation §7); none reads a file this task changes.
- A scratch worktree of `origin/main` (`$TMPDIR/basewt`, detached) served the base comparisons and was removed with `git worktree remove`.
- Out-of-sandbox actions go through the permission gate only for the Worker Playbook step 4 cases: `git push`, `gh`, the main-checkout CompactionDB `memory add`, writing and masking the main-checkout evidence copies, and `agmsg-dispatch` (`excludedCommands`). The main-checkout copy of this file lists them as run.
