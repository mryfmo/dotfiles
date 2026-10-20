# Sandbox record: dotfiles-T133-pre-send-check-a02

- **Seat:** `claude-standard-dot-a008` in `.claude/worktrees/worker-f`, under Worker Playbook step 4 and plan 024 §5.14 item 10.
- **Inside the sandbox ran:** `git fetch`, commits (`git -c commit.gpgsign=false`), the push, the `gh` reads and PR edit, the module under the task's `env -i` command, bash -n, shellcheck, shfmt, ruff, the preflight and `make require-crit-review`.
- **Outside the sandbox:** only `agmsg-dispatch`, through `excludedCommands`, the documented step 4 exception. No command was refused.
- **Python:** the test module and the preflight's helper ran on the pinned `~/.local/share/mise/installs/python/3.15.0/bin/python3` with `-I`; the record edits ran as `python3.15 -I` scripts.
- **The red proof:** it swapped `11584e19`'s script into the worktree and restored the new one (validation §1). No live record changed, and no Bats or network fetch ran.
