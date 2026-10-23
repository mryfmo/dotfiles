# Sandbox record: dotfiles-T133-pre-send-check-a01

- **Seat:** `claude-standard-dot-a008` in `.claude/worktrees/worker-f`, under Worker Playbook step 4 and plan 024 §5.14 item 10.
- **Inside the sandbox ran:**
  - `git fetch`, `git switch -c … --no-track`, commits (`git -c commit.gpgsign=false`) and the push, each one command;
  - the unit module under the task's `env -i` command;
  - `bash -n`, shellcheck, shfmt, ruff, the comparison lint, the preflight itself and `make require-crit-review`;
  - the `gh` PR and checks calls.
- **Outside the sandbox:** only `agmsg-dispatch`, through `excludedCommands`. No command was refused.
- **Python:** every run used the pinned `~/.local/share/mise/installs/python/3.15.0/bin/python3` with `-I`; the preflight runs its checker through `uv run --no-config --no-project --offline`.
- **Not run:** no network fetch, no local Bats, and no `git worktree prune`. No live record changed: the tests use a temporary root.
