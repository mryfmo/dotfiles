# Orchestration task: T13 agmsg orchestration rule file

## Assignment

- Task ID: `T13-agmsg-orchestration-rule-file`
- Executor model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Repo: `/Users/mryfmo/Workspace/dotfiles` (current working tree, branch `main`)
- Pre-existing dirty/untracked paths (`home/dot_mise/*`, `plans/`,
  `docs/verification/`, `.orchestration/`) are NOT yours — do not touch.

## Objective

Create ONE new rule file `home/dot_config/claude/rules/agmsg-orchestration.md`
(deployed by chezmoi to `~/.config/claude/rules/`, injected into every Claude
Code session as a global instruction). Match the style of the existing rule
files in that directory (`model-selection.md`, `crit-review.md`: a single `##`
heading, terse English bullet points, no preamble). Do NOT modify any existing
rule file.

The file must codify, concisely (aim ≤ 40 lines), the operator-ruled regime:

### Section A — Delegation regime

- When the operator requests agmsg/codex collaboration (or an orchestration
  regime is active), Claude Code acts as orchestrator only: lightweight
  reads (grep/read), judgment, task authoring, and acceptance review.
- All real work — file edits, builds, test runs, git state changes, and other
  executing processes — is delegated via agmsg to ONE resident codex worker
  in a herdr pane, tasks assigned sequentially (no parallel `codex exec`,
  no per-task codex spawning).
- Acceptance review is adversarial and multi-lens (correctness, regression,
  security, reporting omissions): attempt to refute the worker's RESULT,
  independently re-derive findings, and never accept sampled spot-checks as
  full verification.
- Do not idle-wait: while a worker task is in flight, prepare or delegate
  independent work.
- The crit review guard (`make require-crit-review`) is the orchestrator's
  final integration step; never assign it to the worker.

### Section B — Identity and registration rules

- One physical agent = one unique identity name, derived from the current
  directory: `<runtime>-<model+effort>-<project-suffix>` (e.g.
  `codex-gpt56sol-dot` for dotfiles, `-flue` for flue-pi; task-scoped workers
  append `-aNNN`). Before any join, check every
  `~/.agents/skills/agmsg/teams/*/config.json` for the candidate name; on
  collision, pick a suffixed unique name — never reuse a name across
  different physical agents.
- Registration `project` is always the real repository path of the current
  directory. `$HOME` registrations are forbidden (they are the codex-hook
  ambiguity/inbox-stealing vector).
- At orchestrator session start in a team, claim session exclusivity with
  `actas-claim.sh <project> <type> <name> <session_id>` so concurrent
  sessions in the same directory cannot share an identity.
- Deliver worker messages by explicit nudge (team + identity named in the
  pane prompt); do not rely on automatic turn delivery. Concurrent resident
  workers require separated stores via `AGMSG_STORAGE_PATH`.
- Message contracts and playbooks live in the `agmsg-orchestration` skill;
  invoke it for the AGMSG-TASK/RESULT/ACCEPTANCE workflow.

## Workflow

1. Read the existing rule files for style; write the new file.
2. Create branch `rule/agmsg-orchestration` from `main` (do NOT commit yet —
   the orchestrator runs the crit review guard first and will instruct the
   commit separately).
3. Stage nothing; leave the new file untracked on the branch.

## Constraints

- allowed_files: `home/dot_config/claude/rules/agmsg-orchestration.md` + the
  expected artifact paths below
- forbidden_actions: `git-commit-push; chezmoi-apply; deps-or-ci-changes;
edits-outside-allowed-files; network-installs; llm-calls;
running-make-require-crit-review`
- Branch creation (`git switch -c rule/agmsg-orchestration`) is the ONLY git
  state change allowed.

## Validation commands (full output into the validation artifact)

- `git branch --show-current` (must be `rule/agmsg-orchestration`)
- `git status --short -- home/dot_config/claude/rules/` (only the new file)
- `wc -l home/dot_config/claude/rules/agmsg-orchestration.md`

## Expected artifacts

- report: `.orchestration/reports/T13-agmsg-orchestration-rule-file.md`
- validation: `.orchestration/validation/T13-agmsg-orchestration-rule-file.md`
- sandbox: `.orchestration/sandboxes/T13-agmsg-orchestration-rule-file.md`
- learning: `.orchestration/learning/T13-agmsg-orchestration-rule-file.md`
- autoskill: `.orchestration/autoskill/runs/T13-agmsg-orchestration-rule-file.md`

## STOP conditions

- The rules directory has a naming/format convention the new file cannot
  satisfy → STOP and report.
- Branch `rule/agmsg-orchestration` already exists → STOP and report.

When done send: `AGMSG-RESULT v1 task_id=T13-agmsg-orchestration-rule-file status=ready_for_review ...` with all artifact paths.
