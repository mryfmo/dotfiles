## agmsg orchestration

- When the operator requests agmsg/Codex collaboration or an orchestration regime is active, act only as orchestrator: lightweight grep/read, judgment, task authoring, and acceptance review.
- Delegate all repository-mutating work — file edits, builds, test runs, git state changes — to one resident Codex worker in a herdr pane; agmsg/herdr control-plane commands (delivery.sh, watch.sh, actas-claim.sh, send.sh, join.sh, herdr agent/pane) are orchestrator-side and exempt; assign worker tasks sequentially, never through parallel codex exec or per-task Codex spawning.
- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot-checks as full verification.
- Do not idle-wait while worker work is in flight; prepare or delegate independent work.
- Keep `make require-crit-review` as the orchestrator's final integration step; never assign it to a worker.
- On regime activation, verify delivery with `delivery.sh status <type> <repo>`; if it is weaker than `both`, run `delivery.sh set both <type> <repo>`, start the SessionStart-printed `watch.sh <session_id> <repo> <type>` command as a persistent in-session monitor, and claim exclusivity with `actas-claim.sh <project> <type> <name> <session_id>`.
- Detect worker completion only when an AGMSG-RESULT message arrives through monitor/turn delivery; send worker liveness and status checks only as AGMSG-PING/AGMSG-PONG over the bus, never by reading worker panes or screens; limit pane interaction to prompt injection and the submit key, never infer completion from pane or agent status, and never use ad-hoc polling sleep loops.
- If an out-of-band Codex completion signal is ever needed, use the official `notify` config: the `agent-turn-complete` event sends a JSON payload to an external command.
- Give each physical agent one unique identity derived from the current directory: `<runtime>-<model+effort>-<project-suffix>` (for example, `codex-gpt56sol-dot` for dotfiles or a `-flue` suffix for flue-pi); task-scoped workers append `-aNNN`.
- Before any join, search every `~/.agents/skills/agmsg/teams/*/config.json` for the candidate name; on collision, choose a suffixed unique name and never reuse one identity for different physical agents.
- Always register `project` as the current directory's real repository path; `$HOME` registrations are forbidden because they create codex-hook ambiguity and steal inbox messages.
- At worker setup run delivery.sh set turn codex <repo> so the worker Stop hook auto-delivers inbox messages each turn from the repo-scoped .codex/hooks.json (gitignored); pane nudges are only generic wakes for idle workers — message content always flows over the bus.
- Give concurrent resident workers separate stores with AGMSG_STORAGE_PATH; the orchestrator must prefix the SAME AGMSG_STORAGE_PATH on its send/watch/history calls for that worker, or results and pongs land in an unreachable database.
- Invoke the `agmsg-orchestration` skill for AGMSG-TASK/RESULT/ACCEPTANCE message contracts and playbooks.
