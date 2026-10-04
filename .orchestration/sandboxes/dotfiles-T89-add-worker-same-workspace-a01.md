# Sandbox: dotfiles-T89-add-worker-same-workspace-a01

- **Worktree and branch:** worker-c, branch `feat/add-worker-same-workspace` from `origin/main` a575b3cc. The sandboxed `git switch -c` created the ref but stopped on the `.git/config.lock` stub, so I finished the switch with `git symbolic-ref` and `git reset --hard HEAD` on the clean tree. After `gh pr update-branch`, I fast-forwarded to the merge head.
- **Live Herdr, read-only only:**
  - `herdr workspace list`;
  - `herdr tab --help`, `herdr tab create --help` and `herdr workspace create --help`;
  - the branch's `check-regime-boundary.sh --report`, which only lists and reads.
- **Live Herdr, never run:** no `tab create`, `pane split`, `workspace create/close`, `tab close` or `pane close`. The live migration is the operator's.
- **Read-only inspection:** `/proc/<pid>/environ` and `/proc/<pid>/cwd` of the running worker-d and worker-e agents. `pgrep` of host crit servers.
- **Untouched:** no upstream agmsg script under `~/.agents` was changed.
- **Unit tests** ran in the Claude sandbox, whose own pid namespace hides host crit servers.
- **Unsandboxed runs** (`dangerouslyDisableSandbox`):
  - `gh pr create/checks/update-branch` and `gh api`;
  - the read-only herdr and `/proc` reads;
  - CompactionDB `memory add`;
  - the writes to the main checkout's T89 `.orchestration` files;
  - `agmsg-dispatch` (PONG and RESULT).
