# E2E leg: Codex orchestrator → codex worker (Linux)

Status: **not run in the 2026-10-05 Claude-orchestrated session; operator-run procedure below.** Recorded by the orchestrator seat `claude-remediation-dot`.

## Why it did not run here

- `codex-orchestrate` (T86) clears `HERDR_AGENTS_ORCHESTRATOR_KIND`, sources the rendered `~/.agents/model-profiles.env`, and exits 2 unless that file says `codex` ("select the codex orchestrator in the manifest used by herdr-agents"). The T87 draft's environment override is therefore ignored by design (model-selection rule: kinds live in the manifest).
- The manifest renders `HERDR_AGENTS_ORCHESTRATOR_KIND="claude"` today (`home/dot_agents/agent-config.yaml:74`). Switching it is a repository change (worker task + PR) plus `make update`; under `codex`, `herdr-agents` refuses the Claude-pair modes (T85), so the switch cannot be made while this Claude orchestrator seat runs: the README says "Stop the current orchestrator before launching".

## Operator procedure (Linux host)

1. Worker task: set `orchestrator_kind: codex` in the manifest; merge; `make update` (renders `HERDR_AGENTS_ORCHESTRATOR_KIND="codex"`).
2. Keep the codex worker seated (`herdr-agents --add-worker <worktree> --kind codex` if none), stop the Claude orchestrator session, then from the main checkout root in a plain shell:
   `codex-orchestrate --max-turns 3 --timeout 1800 --team dotfiles "Dispatch dotfiles-T87-probe to the seated worker: run make render-check in its worktree and send AGMSG-RESULT; then ORCHESTRATION-DONE."`
3. Evidence: paste `uname -s`, the `Doctor summary` line, the launcher's repository transcript `.orchestration/validation/codex-orchestrate-<date>-<n>.md` (turn numbers, exit codes, marker status), the `messages.db` rows of the probe's TASK/RESULT with `read_at`, and `make check-regime-boundary` output into this file.
4. Worker task: revert `orchestrator_kind: claude`; merge; `make update`; restart the pair with `herdr-agents <DIR>`.

Worker for this leg: codex (worker-e, codex-security-dot-a007 or a re-seated Codex worker).
