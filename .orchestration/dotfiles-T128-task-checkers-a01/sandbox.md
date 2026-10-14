---
task_id: dotfiles-T128-task-checkers-a01
seat: claude-standard-dot-a002
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T128-task-checkers-a01

- Period: from the liveness PING (2026-10-14T00:28:11Z) and the AGMSG-TASK (04:14:57Z) to the RESULT.
- Inside the sandbox ran:
  - the HTTPS `git fetch` and `git push`;
  - the branch, the commits, the fixtures and the task copy;
  - every test, lint and format run;
  - the replay, the port-against-input comparison and the mutation pass.
- In the sandbox uv cannot reach pypi, so the tests and checker runs used `UV_OFFLINE=1` from the uv cache (validation, header). CI runs them online.
- A PreToolUse hook refuses bare `python3` in Bash. Python ran as `uv run --no-project python -I` instead.
- No local mutation was chained onto a call that ran outside the sandbox.

The table lists every call that ran outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`, since `gh` fails TLS inside the sandbox) and `agmsg-dispatch` through `excludedCommands`. Rows after the evidence commit are completed in the evidence update.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-task-checkers-a01 status=alive …` (00:28:35Z) | `agmsg-dispatch` |
| 2 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-task-checkers-a01 status=question …` (04:18Z, the pinned fixture) | `agmsg-dispatch` |
| 3 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head regime/task-checkers …` (PR #352) | `gh` |
