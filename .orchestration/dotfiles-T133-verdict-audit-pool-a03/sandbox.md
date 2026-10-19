---
task_id: dotfiles-T133-verdict-audit-pool-a03
seat: claude-standard-dot-a008
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T133-verdict-audit-pool-a03

- **Seat and arrival:** `claude-standard-dot-a008` in `.claude/worktrees/worker-f` (pane `wJ:p3`). The AGMSG-TASK arrived at 2026-10-19T00:39:47Z.
- **Delivery:** turn delivery only. The inbox is read at each milestone.
- **Branch:** `tools/verdict-audit-pool-a01`, fetched with `git fetch origin tools/verdict-audit-pool-a01` (one command) at `b8998de1`.
  - The seat's own stale local copy, `0db5f175`, is an ancestor of `b8998de1`, so resetting it loses nothing.
  - `git switch -C tools/verdict-audit-pool-a01 --track origin/tools/verdict-audit-pool-a01` failed at its last step, exit 1: `error: could not lock config file …/.git/config: Operation not permitted` and `unable to write upstream branch configuration`. The sandbox denies writes to `.git/config`.
  - By then the branch ref, the index and the working tree were already at `b8998de1`, so `git symbolic-ref HEAD refs/heads/tools/verdict-audit-pool-a01` completed the switch.
  - No upstream is configured, so every push names its refspec.
  - The other seat's branch, `verdict-audit-pool-a02-a011`, was not touched, and neither were this seat's branches for PRs #423, #418 and #415.
- **Inside the sandbox ran:**
  - every edit and every commit (`git -c commit.gpgsign=false`);
  - the unit tests, `make unit-test`, `make format`, `make render-check`, shellcheck, shfmt and ruff;
  - the task-consistency check;
  - the scratch worktrees under `$TMPDIR`, each removed with `git worktree remove --force`. `git worktree prune` never ran.
- **Python:** every Python run goes through `uv run … python -I`.
- **Restricted strings:** every text containing the gh merge or create command words was written with the file edit tool, never in a Bash heredoc or echo.
- **No chaining onto unsandboxed calls:** no local mutation was chained onto a call that ran outside the sandbox.

Calls outside the sandbox, each through the permission gate (Worker Playbook step 4), or through `excludedCommands` for `agmsg-dispatch`:

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin tools/verdict-audit-pool-a01`, one command per push | `git push` |
| 2 | `scripts/orchestrator/verdict.sh --shadow 410 --task dotfiles-T133-verdict-audit-pool-a03`, the Check's shadow invocation. Its re-exec reaches gh for `pr view` and `pr checks`, and gh needs the network. | `gh` |
| 3 | `gh pr checks 410` reads, and the Bot wait as `gh api` reads of the reviews and comments | `gh` |
| 4 | `agmsg-dispatch … 'AGMSG-RESULT v1 task_id=dotfiles-T133-verdict-audit-pool-a03 …'` | `agmsg-dispatch` |
