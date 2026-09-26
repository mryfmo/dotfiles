---
task_id: dot-orchestrator-guardrails-T21-a01
revision: 2
supersedes: 1
created_at: 2026-09-26T01:25:00Z
---
# AGMSG-TASK dot-orchestrator-guardrails-T21-a01 (revision 2): enforce the orchestrator rules that prose could not hold (G1–G8 PreToolUse guardrails + checklist re-injection + rule text)

Operator finding (2026-09-25): most orchestrator deviations violated rules that already existed in prose (`home/dot_config/claude/rules/agmsg-orchestration.md`, `model-selection.md`, agmsg-orchestration SKILL): inferring worker state from `herdr agent list`, idle-waiting, bare `send.sh` to a herdr-paned worker, self-exploration, working inside the worker worktree. Some rules were missing (revise consolidation, GitHub feedback sweep, `make upgrade` never inside a worker task, plan-mode procedure). Prose alone does not hold across long sessions and compaction. Rules the orchestrator cannot keep must be enforced deterministically at the tool boundary and re-injected after compaction.

Repo: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c` (your own worktree, detached at origin/main; `git switch -c feat/orchestrator-guardrails origin/main`). You are `claude-standard-dot-a005` (herdr pane wE:p5). T16 (PR #182, rules/skills edits) is still open: rebase onto main when it lands (orchestrator notifies) and resolve overlaps in agmsg-orchestration SKILL/rules by keeping both changes.

## Design constraints
- Reuse the existing PreToolUse pattern (`home/dot_claude/hooks/executable_enforce-uv.sh` is wired as `PreToolUse` matcher `Bash` in `agent-config.yaml` → `claude-settings-managed.json`). permgate is wired on `PermissionRequest` only and fires just when a prompt would appear, so it cannot be the guardrail layer; do not extend it for this.
- Role detection: herdr-agents already labels panes; add `--env HERDR_AGENTS_ROLE=orchestrator|worker` on the panes it creates (orchestrator: the Claude pane it renames/starts; worker: the split pane). The hook treats a missing variable as `unknown` and enforces only the rules that are role-independent.
- Claude Code hook contract: PreToolUse command hooks receive JSON on stdin (`tool_name`, `tool_input.command`, `session_id`, `cwd`); exit 2 + stderr message denies the call; exit 0 allows; `hookSpecificOutput.permissionDecision` JSON is also accepted — read the official hooks reference and cite it in the script header.

## Deliverables
1. `home/dot_claude/hooks/executable_orchestrator-guardrails.py` (stdlib Python, shdoc-style module docstring) with deterministic rules, each with an id and a one-line remedy printed on deny:
   - `G1 no-status-inference` (role=orchestrator): deny Bash containing `herdr agent list`, `herdr pane list`, `herdr pane peek`, `herdr agent explain` → "use AGMSG-PING/PONG; completion arrives as AGMSG-RESULT".
   - `G2 no-bare-send` (role=orchestrator): deny direct `agmsg/scripts/send.sh` → "use agmsg-dispatch (or upstream poke after T19)". Allow when the command is the dispatcher itself.
   - `G3 worker-tree-isolation` (role=orchestrator): deny `cd`/writes (`>`, `tee`, `cp/mv/rm`, `git -C`, `sed -i`) targeting `.claude/worktrees/<name>` except `.claude/worktrees/orchestrator-review`; reads (`git show`, `cat`, `grep`, `diff`) stay allowed.
   - `G4 merge-gate` (role=orchestrator): deny `gh pr merge <n>` unless both `.orchestration/validation/*-pr-feedback*.json` mentioning `"number": <n>` (or `pr=<n>`) with zero empty dispositions AND a receipt `.agents/worklog/claude/crit/pr-<n>-receipt.md` exist; also deny `--delete-branch` while any `git worktree list` entry has that PR's head branch checked out (prints the worktree path).
   - `G5 no-make-upgrade-in-tasks` (role=worker): deny `make upgrade` / `scripts/upgrade-tools.sh` → "operator-run at a session boundary in the canonical clone".
   - `G6 no-self-exploration` (role=orchestrator, soft): when a Bash command is a broad search (`rg|grep -r|find . -name` over the repo root without a path under `.orchestration`/`.agents`), print a warning to stderr but allow (additionalContext), pointing to express-explorer. Keep it advisory to avoid blocking legitimate reads.
   - `G7 no-improvised-topology` (role=orchestrator): deny raw `herdr workspace create|close`, `herdr tab create|close`, `herdr pane split|move|swap|close`, `herdr agent start|stop`. Allowed: `herdr-agents` (documented lifecycle entrypoint), `agmsg-dispatch`/upstream `poke`, and read-only `herdr … list|get|read` only where G1 permits. Remedy: "topology changes go through herdr-agents; if it lacks the capability, file a task to extend it (T22)".
   - `G8 documented-procedure-or-ask` (role=orchestrator, enforceable): any Bash whose first word or a pipeline stage is `herdr`, `agmsg-dispatch`, `~/.agents/skills/agmsg/scripts/*.sh`, `git worktree`, `gh pr merge`, `chezmoi apply`, or `make update|upgrade` must carry a trailer comment `# ref: <repo-relative file>#<heading or line>` naming the documented procedure; the hook verifies the file exists and the heading/line text is present, otherwise denies with "cite the documented procedure or stop and ask". Read-only `git`/`gh api` queries are exempt. Tests: allow with a valid ref, deny without ref, deny with a ref to a missing heading.
   - Rules are configured in `agent-config.yaml` under `claude.guardrails` (enabled list + role env name) and rendered into the managed settings; `validate-agent-assets.py` requires G1–G5, G7, G8 enabled for the orchestrator profile.
2. Checklist re-injection: extend the existing agmsg `session-start.sh` directive path or add a small `SessionStart` (matchers `startup|resume|compact`) + `UserPromptSubmit` hook that prints a ≤12-line orchestrator checklist (PING-only liveness; tasking → dispatch → RESULT → adversarial review in `orchestrator-review` → feedback sweep → Crit → receipt → guard → merge without `--delete-branch` → records → sync commit; one consolidated revise per round; never idle-wait). Only for role=orchestrator.
3. Rule text: `agmsg-orchestration.md` (+ SKILL Orchestrator Playbook) gains: worker-worktree isolation; one consolidated revise per review round; `make upgrade` never in an AGMSG-TASK; plan-mode procedure (plan → one ExitPlanMode → run the regime end to end); the guardrail ids and how to override for an operator-sanctioned exception (`GUARDRAILS_ALLOW=G1,...` env for one command, logged).
4. herdr-agents: pass `--env HERDR_AGENTS_ROLE=...` on pane creation; README paragraph.
5. Tests: unit tests for every rule (deny/allow/role-missing/override), hook JSON contract, generator rendering, validator; bats if a file covers hooks; no local bats runs.
6. Live E2E (required): in a scratch git repo with a fake `.orchestration` layout, run the hook binary with crafted stdin for each rule and paste outputs; then confirm that in this real orchestrator session (`CLAUDE_CODE_SESSION_ID` set) the hook denies `herdr agent list` when `HERDR_AGENTS_ROLE=orchestrator` is exported for the test invocation — do this by invoking the hook script directly, not by editing live settings.

## Validation (verbatim)
Unit tests; validator; generator `--check`; E2E outputs; `gh pr checks`; pr-feedback JSON with every item dispositioned (CodeRabbit full review once on the final head; 1/hour limit).

## allowed_files
`home/dot_claude/hooks/executable_orchestrator-guardrails.py`, `home/dot_agents/agent-config.yaml`, `scripts/generate-agent-configs.py`, `scripts/validate-agent-assets.py`, `home/.chezmoitemplates/claude-settings-managed.json` (generated), `home/dot_local/bin/common/executable_herdr-agents` (env passing only), `home/dot_config/claude/rules/agmsg-orchestration.md`, the Codex rules mirror, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `README.md`, tests, artefacts.

## forbidden_actions
editing live `~/.claude/settings.json` or `~/.claude/hooks/`; `make update`/`chezmoi apply`; merging; local bats; force-push.

## Artefacts / Done signal
Standard five + pr-feedback JSON. `[memory:decision]`: "orchestrator rules that prose could not hold are enforced by a PreToolUse guardrail hook (G1-G8) with role detection from HERDR_AGENTS_ROLE and re-injected as a checklist on SessionStart/compact". RESULT via send.sh. max_turns=50.

## Revision history
- r1: G1–G6 + role detection + checklist; addenda added G7 (2026-09-25 23:0xZ) and enforceable G8 (23:1xZ).
- r2 (2026-09-26): addenda folded into the body; no scope change.
