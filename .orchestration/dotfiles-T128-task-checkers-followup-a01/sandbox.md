---
task_id: dotfiles-T128-task-checkers-followup-a01
seat: claude-standard-dot-a002
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T128-task-checkers-followup-a01

- Period: from the AGMSG-TASK (04:25:00Z) to the RESULT.
- Inside the sandbox ran:
  - the HTTPS `git fetch` and `git push`;
  - the branch, the commit, the task copy and the evidence;
  - every test, lint and format run;
  - the mutation pass and the validation script.
- uv ran with `UV_OFFLINE=1`; ruff ran as the installed `ruff` 0.17.0.
- No local mutation was chained onto a call that ran outside the sandbox.

The table lists every call that ran outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`, since `gh` fails TLS inside the sandbox) and `agmsg-dispatch` through `excludedCommands`. Rows after the evidence commit are completed in the evidence update.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-task-checkers-followup-a01 status=alive …` (04:26:56Z, the plan and the reading of audit:c1f60f7:3) | `agmsg-dispatch` |
| 2 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head tools/task-checkers-followup …` (PR #365) | `gh` |
| 3 | `agmsg-dispatch … AGMSG-PONG v1 … status=alive …` (the answer to the 04:53:36Z state PING) | `agmsg-dispatch` |
