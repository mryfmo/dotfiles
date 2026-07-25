# Orchestration task: T29 make the agmsg orchestration regime default-on

## Assignment

- Task ID: `T29-agmsg-regime-default-on`
- Repo: `/Users/mryfmo/Workspace/dotfiles`
- The main worktree is dirty with UNRELATED changes (`home/dot_mise/*`).
  Create a separate git worktree from `origin/main` (e.g. `git worktree add
../dotfiles-t29 -b docs/agmsg-regime-default-on origin/main`) and do ALL
  work there. Report the worktree path in your result report. Do NOT touch
  the main worktree except for the expected artifact paths below.

## Problem (operator decision, 2026-07-25)

The activation clause of the shared agmsg orchestration rule reads:
"When the operator requests agmsg/Codex collaboration or an orchestration
regime is active, act only as orchestrator". In practice this made the
regime opt-in: with no explicit request, the Claude orchestrator performed
repository-mutating work itself while the resident Codex worker idled. The
operator has decided the regime must be default-on: agmsg is the always-on
communication bus between agents, and work must follow each agent's
configured responsibilities.

## Desired behavior

Edit `home/dot_config/claude/rules/agmsg-orchestration.md` (first bullet
only) so that:

1. The orchestration regime is ACTIVE BY DEFAULT whenever the agmsg bus is
   available and a resident Codex worker exists for the repository (for
   example in a herdr-managed agent workspace). No explicit operator
   request is needed.
2. agmsg is described as the always-on communication path between agents.
3. The operator may explicitly opt out for the current task; only then may
   the orchestrator mutate the repository directly.
4. The orchestrator-role sentence (lightweight grep/read, judgment, task
   authoring, and acceptance review) is preserved.

Keep it to the first bullet; do not reflow or reword the other bullets.
Keep the file in English, matching the existing style (one bullet per
rule, no headings added).

## Constraints

- allowed_files:
  - `home/dot_config/claude/rules/agmsg-orchestration.md`
  - the expected artifact paths below (in the MAIN worktree)
- forbidden_actions: `edits-outside-allowed-files; git-push (until
orchestrator authorizes); chezmoi-apply; live-herdr-mutation;
deps-or-ci-changes; local-bats; llm-calls`
- Commit on `docs/agmsg-regime-default-on` in the T29 worktree with a
  Conventional Commit message in English
  (suggested type/scope: `docs(rules): ...`).

## Validation commands (full output into the validation artifact)

- `git -C <t29-worktree> diff --stat` (only the rule file)
- `git -C <t29-worktree> status --short`
- `uv run --with pyyaml scripts/validate-agent-assets.py` (run from the
  T29 worktree root; record output or its absence)

## Expected artifacts (exact paths, MAIN worktree)

- report: `.orchestration/reports/T29-agmsg-regime-default-on.md`
- validation: `.orchestration/validation/T29-agmsg-regime-default-on.md`
- sandbox: `.orchestration/sandboxes/T29-agmsg-regime-default-on.md`
- learning: `.orchestration/learning/T29-agmsg-regime-default-on.md`
- autoskill: `.orchestration/autoskill/runs/T29-agmsg-regime-default-on.md`

## STOP conditions

- validate-agent-assets.py asserts tokens in the rule file that conflict
  with the required wording → STOP and report.

When done send:
`AGMSG-RESULT v1 task_id=T29-agmsg-regime-default-on status=ready_for_review report=... validation=... sandbox=... learning=... autoskill=...`
Max turns: 15.
