---
task_id: dotfiles-T128-seat-liveness-followup-a01
seat: claude-standard-dot-a002
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T128-seat-liveness-followup-a01

- Period: from the AGMSG-TASK (2026-10-16T22:46:03Z) to the RESULT.
- Inside the sandbox ran:
  - the HTTPS `git fetch` and `git push`;
  - the branch, the commits and the evidence;
  - every test, lint and mutation run.
- uv ran with `UV_OFFLINE=1`.
- No local mutation was chained onto a call that ran outside the sandbox.
- One sandboxed call was denied by the permission check (a scratch repository set up with `rm -rf` before its `git commit`). It was not retried in that form; the same check ran in a fresh `mktemp -d` directory with no removal.
- The temporary `origin/main` worktree for the baseline run was added and removed with `git worktree add` and `git worktree remove`, inside the sandbox.

Calls outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`) and `agmsg-dispatch` through `excludedCommands`. These rows are planned in advance, so no evidence update moves the head after the Bot's review:

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head tools/seat-liveness-followup …` | `gh` |
| 2 | `gh pr ready <pr>` | `gh` |
| 3 | the Bot wait (`bot-wait.sh`, background; `gh pr view`, `gh api` reads, and `gh pr comment … '@codex review'` only at 10 minutes without a review) | `gh` |
| 4 | `gh pr checks <pr> --watch` (background, exit status joined) | `gh` |
| 5 | `gh api` reads of the Bot's review and comments on the head | `gh` |
| 6 | after a P0/P1 fix round only: the push, then `gh pr comment <pr> --body '@codex review'` and the same Bot wait for the re-review (`bot_rounds=2`) | `gh` |
| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-seat-liveness-followup-a01 …` | `agmsg-dispatch` |
