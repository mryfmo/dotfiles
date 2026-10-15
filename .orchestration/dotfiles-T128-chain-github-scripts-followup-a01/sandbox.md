---
task_id: dotfiles-T128-chain-github-scripts-followup-a01
seat: claude-standard-dot-a002
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T128-chain-github-scripts-followup-a01

- Period: from the AGMSG-TASK (00:21:35Z) to the RESULT.
- Inside the sandbox ran:
  - the HTTPS `git fetch` and `git push`;
  - the branch, the commit, the task copy and the evidence;
  - every test, lint and format run;
  - `gh api --help`, which reads no network;
  - the mutation pass and the validation script.
- In the sandbox uv cannot reach pypi, so every uv run used `UV_OFFLINE=1` from the uv cache. ruff ran as the installed `ruff` 0.17.0.
- No local mutation was chained onto a call that ran outside the sandbox.

The table lists every call that ran outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`, since `gh` fails TLS inside the sandbox) and `agmsg-dispatch` through `excludedCommands`. Rows after the evidence commit are completed in the evidence update.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head tools/chain-github-scripts-followup …` (PR #360) | `gh` |
| 2 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-chain-github-scripts-followup-a01 status=alive …` (00:30:41Z, the readings and three candidates) | `agmsg-dispatch` |
