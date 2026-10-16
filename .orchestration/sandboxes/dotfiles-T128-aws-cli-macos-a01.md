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
| 3 | `gh pr ready 363 --repo mryfmo/dotfiles; date +%s; date -u +%FT%TZ` (01:23:38Z) | `gh` |
| 4 | the Bot wait on `c2638b32` (`scratchpad/bot-wait.sh`, background: `gh pr view` and `gh api` reads every 30 seconds, one failing on the host's sleep, and its `gh pr comment 363 --body '@codex review'` at 2741 seconds) | `gh` |
| 5 | `gh pr checks 363 --watch` (background, after a `gh pr checks` poll for the first check; exit 1 on the network drop, listing all pass) | `gh` |
| 6 | `agmsg-dispatch … AGMSG-PONG v1 … status=alive …` (03:54:56Z, the answer to the 03:54:05Z PING) | `agmsg-dispatch` |
| 7 | `gh api` reads of the PR's issue comments, reviews and review comments, of `gh pr view 363 --json headRefOid,mergeStateStatus`, and of the two Bot comments' bodies | `gh` |
| 8 | `gh run view --repo mryfmo/dotfiles --job 116196069142 --log`, saved to a scratch file and read with grep (validation §9) | `gh` |
| 9 | `gh pr checks 363 --watch` on the final head, after a `gh pr checks` poll (background, exit status joined) | `gh` |
| 10 | `gh api` reads of the PR's reviews and review comments on the final head | `gh` |
| 11 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-aws-cli-macos-a01 …` | `agmsg-dispatch` |

The pushes of `fe392450`, `c2638b32` and the evidence update ran inside the sandbox over HTTPS.
