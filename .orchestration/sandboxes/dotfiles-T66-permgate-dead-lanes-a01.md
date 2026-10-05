# dotfiles-T66-permgate-dead-lanes-a01 — sandbox

- Isolation: dedicated git worktree `~/Workspace/dotfiles/.claude/worktrees/worker-d`, branch `chore/permgate-dead-lanes` from `origin/main` 523fda06. Worker identity: `claude-standard-dot-a006` (Claude Code, `standard`).
- Edits, unit tests, smoke runs, prettier and ruff ran in the Claude Code Bash sandbox. These ran unsandboxed through the normal permission gate:
  - `git push`, `gh pr create`/`checks`/`api`;
  - `python3 .claude/hooks/contextdb_cli.py memory add` in the main checkout (state dir read-only from this worktree's sandbox);
  - `agmsg-dispatch` (herdr socket);
  - `pgrep`/`kill` of this seat's own Crit plan server (pid 4129281, `plan-agmsg-actas-claude-standard-dot-a006-2026-10-04`, started by the Plan Mode hook at session start). Sandboxed `pgrep` cannot see it because of the pid namespace. The a007 seat's Crit server (pid 4150161) was left running.
- One validation-capture command was refused by Claude Code's built-in removal safety check: its `bash -c "$1"` wrapper could not be analysed. It contained no removal. The same commands were rerun inline without the wrapper.
- The smoke runs wrote decision logs only under `/tmp/claude-1000/`. The live `~/.local/state/permgate/decisions.jsonl`, `~/.agents/permgate-policy.yaml` and `~/.local/bin/common/permgate` were not modified. No `make update`/`make apply`, local bats or merge was run.
- `git status` shows sandbox phantom stubs (`.bash_profile`, `.bashrc`, `.claude/agents`, …) as untracked. They were not staged.
