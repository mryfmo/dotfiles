---
task_id: dotfiles-T128-chain-review-scripts-a01
seat: claude-standard-dot-a002
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T128-chain-review-scripts-a01

- Period: from the AGMSG-TASK (08:54:36Z) to the RESULT.
- Inside the sandbox ran:
  - the HTTPS `git fetch` and `git push`;
  - the branch, the commit, the task copy and the evidence;
  - every test, lint and format run;
  - the mutation pass and the validation script.
- In the sandbox uv cannot reach pypi, so every uv run used `UV_OFFLINE=1` from the uv cache (validation, header). `uvx ruff` could not write uv's tool directory, so ruff ran as the installed `ruff` 0.17.0.
- macOS `mktemp` without a template writes under `/var/folders/…`, which the sandbox denies. That is why item 1 now names a template (amendment 1, learning 1).
- `diff` cannot open a `/dev/fd` process substitution in the sandbox, so validation §3 diffs scratch files instead.
- The whole unit suite fails in the sandbox (validation, intro); CI's run is the evidence.
- No local mutation was chained onto a call that ran outside the sandbox.

The table lists every call that ran outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`, since `gh` fails TLS inside the sandbox) and `agmsg-dispatch` through `excludedCommands`. Rows after the evidence commit are completed in the evidence update.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-chain-review-scripts-a01 status=question …` (09:02Z, row 11 and the worktree guard) | `agmsg-dispatch` |
| 2 | `agmsg-dispatch … AGMSG-PONG v1 … status=working …` (09:05Z, the `mktemp` template) | `agmsg-dispatch` |
| 3 | `agmsg-dispatch … AGMSG-PONG v1 … status=working …` (12:15Z, the branch state) | `agmsg-dispatch` |
| 4 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head regime/chain-review-scripts …` (PR #357) | `gh` |
