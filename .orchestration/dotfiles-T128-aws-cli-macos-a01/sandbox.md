---
task_id: dotfiles-T128-aws-cli-macos-a01
seat: claude-standard-dot-a002
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T128-aws-cli-macos-a01

- Period: from the AGMSG-TASK (01:13:34Z) to the RESULT.
- Inside the sandbox ran:
  - the HTTPS `git fetch` and `git push`;
  - the branch, the commit, the task copy and the evidence;
  - every test, lint and format run;
  - the scratch worktree of `origin/main` for validation §5, added and removed with `git worktree add` and `git worktree remove` (no prune);
  - the mutation pass and the validation script.
- AWS's `install.sh` was read with the WebFetch tool (Worker Playbook step 4, an external reference), not with `curl`; nothing was downloaded into the repository.
- In the sandbox uv cannot reach pypi, so every uv run used `UV_OFFLINE=1` from the uv cache. ruff ran as the installed `ruff` 0.17.0.
- Two Linux tests fail in the sandbox, and on `origin/main` too (validation §5), because macOS `mktemp -d` writes under `/var/folders/…`, which the sandbox denies. CI runs them.
- No local mutation was chained onto a call that ran outside the sandbox.

The table lists every call that ran outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`, since `gh` fails TLS inside the sandbox) and `agmsg-dispatch` through `excludedCommands`. Rows after the evidence commit are completed in the evidence update.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head tools/aws-cli-macos …` (PR #363) | `gh` |
| 2 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-aws-cli-macos-a01 status=alive …` (01:22:11Z, the candidates) | `agmsg-dispatch` |
