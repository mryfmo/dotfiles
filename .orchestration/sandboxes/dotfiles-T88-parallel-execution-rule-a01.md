# dotfiles-T88-parallel-execution-rule-a01 — sandbox

- Isolation: dedicated git worktree `~/Workspace/dotfiles/.claude/worktrees/worker-d`, branch `docs/parallel-execution-rule`. It was created from `origin/main` 3a0816e6 and rebased onto 40d9eb6c (#241, no overlap with this task's files) before the first push. Worker identity: `claude-standard-dot-a006` (Claude Code, `standard`). The T66 branch `chore/permgate-dead-lanes` was kept as instructed.
- Edits, the docs test, `make unit-test`, `make validate-agent-assets` and prettier ran in the Claude Code Bash sandbox. These ran unsandboxed through the normal permission gate:
  - `git fetch`/`rebase`/`push`, `gh pr create`/`checks`/`api`;
  - `python3 .claude/hooks/contextdb_cli.py memory add` in the main checkout (state dir read-only from this worktree's sandbox);
  - `agmsg-dispatch` (herdr socket).
- No code, `README.md` or `AGENTS.md` change, no `make update`/`make apply`, no local bats, no merge.
- No Plan Mode was used for T88. This seat's original plan server (pid 4129281) was stopped during T66.
- Host-side Crit operations (revise round 1 addendum), all unsandboxed through the permission gate, and their cleanup:
  - **Scratch plan server.** `crit plan --name t88-scratch-a006 --no-open --quiet .agents/worklog/claude/t88-scratch-plan.md` started a plan server (pid 3730777, session record `~/.crit/sessions/65c04120b1d7.json`, cwd worker-d, branch `docs/parallel-execution-rule`) to test `crit stop` targeting.
    - It was stopped by an unsandboxed bare `crit stop` on its start branch ("Daemon stopped."), confirmed by `pgrep -fl _serve | grep -w crit` rc=1. The session record was gone afterwards (`ls` reported no such file).
    - The worktree scratch plan file and `~/.crit/plans/t88-scratch-a006` were removed.
  - **Stray daemon.** A mistaken `crit version` (crit takes `version` as a file argument) printed "Started crit daemon at http://localhost:44763 (session b8359df9be5d, PID 3736107)" and then "Error: file not found: version".
    - Immediately after, `pgrep -fl _serve | grep -w crit` returned rc=1 and `ps -o pid,args -p 3736107` was empty, so that daemon had already exited.
    - It left a stale session record, `~/.crit/sessions/b8359df9be5d.json` (pid 3736107, args `["version"]`, cwd worker-d). In round 2, `ps -o args= -p 3736107` returned rc=1, so the pid was gone and the record was stale. It was removed with `rm`, not killed, per step 14. No `~/.crit/reviews/b8359df9be5d` directory existed.
  - The version was then read with `crit -v`: `crit v0.21.1 (2026-10-02, bb3d0b1)`.
  - Branch switches during the test (`docs/parallel-execution-rule` ↔ `feat/gate-audit-evidence`) were between clean committed branches in worker-d.
- Sandbox phantom stubs (`.bash_profile`, `.bashrc`, `.claude/agents`, …) remain untracked and unstaged.
