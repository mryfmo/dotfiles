# Sandbox record: dotfiles-T129-hcom-dispatch-bus-a02

- **Producer:** worker (Claude seat a008), in `.claude/worktrees/worker-f`, under Worker Playbook step 4.
- **Amendment 2's denial, measured (validation §1, 2026-10-22T07:58:12Z):**
  - `mkdir -p ~/Workspace/dotfiles/.agents/worklog/uv-tools` printed `mkdir: ~/Workspace/dotfiles/.agents/worklog/uv-tools: Operation not permitted` (exit 1);
  - `: > ~/Workspace/dotfiles/.agents/worklog/uv-tools-probe` printed `operation not permitted` (exit 1);
  - the directory did not exist before or after.
- **Inside the sandbox ran:** `git fetch`, `git switch -c … --no-track`, the hcom probes against disposable stores under `$TMPDIR`, and `sqlite3` on copies of those stores.
- **Refused by the permission layer:** one probe command that began with `rm -rf` of a scratch store; it was rerun with a fresh `mktemp -d` directory instead.
- **Outside the sandbox:** only `agmsg-dispatch`, through the permission gate (the deployed `excludedCommands` is empty, Checks).
- **Not run:** Bats; the live `~/.hcom` store.
