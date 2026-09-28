# Rule candidate: worktree-registered worker identities receive no turn delivery from a main-path pane

Diagnosis (orchestrator, read-only, 2026-09-28; T30/T31/T32 delivery misses, three occurrences):

- `herdr-agents` starts the worker pane with `--cwd <workdir>` = the main checkout. The worker's SessionStart hook is `session-start.sh claude-code /home/moriya/Workspace/dotfiles`, and `identities.sh <main path> claude-code` returns two names (`claude-remediation-dot`, `claude-standard-dot-a006`); `whoami` reports `multiple=true`.
- Tasks are addressed to `claude-standard-dot-a005`, registered at `.claude/worktrees/worker-c`. No Claude Code session runs with that cwd, so no watcher and no Stop hook ever observe a005's inbox. `~/.agents/skills/agmsg/run/` holds one watcher pidfile (the orchestrator's) although two `cc-instance.*` files exist.
- Consequence: every dispatch to a005 is found only by an explicit `inbox.sh dotfiles claude-standard-dot-a005`, which the worker runs by convention. `agmsg-dispatch` still reports delivery because its wake text names that inbox command and the worker reads it during its turn.

Interim rule (until the herdr-agents role/seat model launches the worker pane inside its own worktree): a worker acting under a worktree-registered identity from a main-path pane runs `inbox.sh <team> <identity>` at each milestone (task start, push, CI green, before RESULT, after any PONG), and the orchestrator assumes revision/PING pickup at the worker's next inbox check rather than as a turn notice.

Root fix: T34 (T22 r3 revision 4) — worker pane `--cwd` = its worktree, identity registered there, delivery hooks installed on that path.
