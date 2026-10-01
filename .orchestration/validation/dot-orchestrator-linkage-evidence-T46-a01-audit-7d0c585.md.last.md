- [P2] high home/dot_local/bin/common/executable_herdr-agents:828 `team.sh --json` in agmsg 1.5.0 reads Codex screens via `agmsg_cli_session_observed → terminal_peek → herdr pane read`, violating the explicit prohibition on reading worker panes.
- [P2] high home/dot_local/bin/common/executable_herdr-agents:863 The PONG query accepts historical replies without correlating them to the current PING; reproduced with an unanswered current PING and an old PONG, falsely producing `pong=yes`.
- [P2] high scripts/check-regime-boundary.sh:53 Running from `.claude/worktrees/worker-c` filters for `worker-c worker `, while workspaces are labeled `dotfiles worker …`, silently missing leftover workers.

Syntax and ShellCheck passed. Full tests were not run; GitHub CI was inaccessible, and no matching RESULT evidence was committed. Audit used Git objects to exclude unrelated checkout changes.

📝 まとめ: Audited only `7d0c585`; identified three defects requiring correction. No files changed.

Verdict: incorrect