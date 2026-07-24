# Orchestration task: Plan 003

## Assignment

- Task ID: `plan-003`
- Executor model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Worktree: `/private/tmp/dotfiles-plan-003`
- Branch: `orchestrator/plan-003`
- Base: `c3e69ade4d3700b4d624416ce2e5d59b31dce191`
- Plan: `/Users/mryfmo/Workspace/dotfiles/plans/003-make-bootstrap-safe-and-publicly-testable.md`

High reasoning is required because this is a cross-platform bootstrap and CI
change with package-state, data-loss, shell parsing, template trust-boundary,
and fork-PR behavior risks. A smaller model is not selected for implementation.

## Objective

Implement every A001-A018 item in order with the smallest correct diff. Preserve
unrelated user data and make public bootstrap validation run from PR checkout
without secrets on Ubuntu client/server and macOS client.

## Required workflow

1. Read the repository `AGENTS.md`, learn index and relevant learn files, the
   full Plan 003, Ponytail full rules, Shdoc skill and shdoc rules before edits.
2. Re-measure the current files and all callers before changing behavior.
3. Write/adjust tests before each production behavior. Do not run Bats locally.
4. Complete phases sequentially and stop on any Plan 003 STOP condition.
5. Use `apply_patch` for edits. Do not modify files outside the allowed list.
6. Run all Plan 003 local gates except Bats. Run `make require-crit-review`; if
   required, use real repo-local Crit data and a receipt, never a bare marker.
7. Do not push, open a PR, or merge. Commit the accepted local implementation
   with Conventional Commits only after validations pass.
8. Write every required orchestration artifact listed below.

## Allowed implementation files

- `setup.sh`
- `README.md`
- `install/ubuntu/common/dependencies.sh`
- `tests/install/ubuntu/common/dependencies.bats`
- `tests/install/ubuntu/common/dependencies_unit.bats`
- `tests/install/common/setup.bats`
- `.github/workflows/remote.yaml`
- `home/.chezmoi.yaml.tmpl`
- one focused role-render test under `tests/install/common/` only if an
  existing test file cannot express the cases

Ignored review evidence under `.agents/worklog/codex/review/` may be created but
must not be committed. Orchestration artifacts are written only to the main
worktree paths below and must not be committed.

## Forbidden actions

- No local Bats execution.
- No network installer execution, live `chezmoi apply`, mutation of the real
  HOME, dependency changes, force push, push, PR creation, or merge.
- No checksum/version pinning owned by Plan 004.
- No new installer framework, rollback daemon, package-command map, role checks
  outside the input boundary/tests, or speculative abstraction.
- No edits to `plans/`, `.agents/worklog/`, or unrelated source files.

## Required validation

- `bash -n setup.sh install/ubuntu/common/dependencies.sh`
- `shfmt -i 4 -sr -d setup.sh install/ubuntu/common/dependencies.sh`
- `shellcheck -x setup.sh install/ubuntu/common/dependencies.sh`
- `make unit-test`
- `make validate-agent-assets`
- exact client/server/macOS role-render checks without persisting invalid input
- adversarial static/fixture evidence for wget-only, no-fetcher, package states,
  locally drifted targets, failed status/diff/apply, and sentinel preservation
- `git diff --check`
- allowed-file audit and diff review against the base SHA
- `make require-crit-review` following repository Crit-data instructions

Record unavailable tools as explicit evidence; do not silently skip them or
install dependencies without authorization.

## Expected artifacts

- Report: `/Users/mryfmo/Workspace/dotfiles/.orchestration/reports/plan-003.md`
- Validation: `/Users/mryfmo/Workspace/dotfiles/.orchestration/validation/plan-003.md`
- Sandbox: `/Users/mryfmo/Workspace/dotfiles/.orchestration/sandboxes/plan-003.md`
- Learning: `/Users/mryfmo/Workspace/dotfiles/.orchestration/learning/plan-003.md`
- AutoSkill: `/Users/mryfmo/Workspace/dotfiles/.orchestration/autoskill/runs/plan-003.md`

The report must include commit SHA, file list, phase/task completion, deviations,
STOP-condition audit, known limitations, and a concise negative-risk assessment.
The validation artifact must distinguish executed tests from static inspection.

## Completion signal

Return `AGMSG-RESULT v1 task_id=plan-003 status=ready_for_review|blocked` and all
five artifact paths. Do not claim GitHub CI, bot, PR, or merge acceptance.
