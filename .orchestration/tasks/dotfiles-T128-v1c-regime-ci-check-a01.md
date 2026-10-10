---
format: 2
task_id: dotfiles-T128-v1c-regime-ci-check-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round4.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/regime-check.sh
  - .github/workflows/regime.yml
  - tests/unit/test_regime_check.py
  - home/dot_agents/agent-config.yaml
  - scripts/validate-task.py
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - README.md
invariants:
  INV-1: "every task is a format-2 file whose front matter validates against schemas/task.json (jsonschema + PyYAML, no hand-written parser); the tier (docs, review, design) is derived from allowed_files by the shared high-risk module, with the regime's own rule prose (home/dot_config/claude/rules/**, the agmsg-orchestration SKILL, AGENTS.md, README) listed in the review tier, and selects the pipeline from process_tiers in agent-config.yaml; every AGMSG-TASK for the task, the first and each amendment, carries task_sha256= of the task file as sent, the worker commits the file byte-identical to .orchestration/<task id>/task.md (first commit, recommitted after each amendment), the CI regime job validates that copy with main's schema and refuses a PR that changes .github/workflows/** unless its task.md is design tier and lists the file, the host gate compares the copy's sha256 with the latest AGMSG-TASK's token in history, and the regime check binds only once the ruleset lists it as required (an operator action named in V1's acceptance record); the orchestrator can add or skip a stage only with an operator waiver named in the acceptance record"
premises:
  - claim: "a pull_request_target workflow job is eligible as a required status check and runs the base branch's workflow file"
    command: "WebFetch docs.github.com troubleshooting-required-status-checks; events-that-trigger-workflows"
    output: "eligible events: push, pull_request, pull_request_review, pull_request_target, deployment, deployment_status; pull_request_target runs in the context of the default branch of the base repository"
  - claim: "required checks must always report, so the job has no path filter and reports success on an unrelated diff"
    command: "sed -n 1,12p .github/workflows/test.yaml"
    output: "comment: Do not add workflow-level path or branch filters here: GitHub can leave skipped required checks in a pending state and block merges"
  - claim: "the manifest validator and renderer ignore an unknown top-level key, so process_tiers needs no validator change"
    command: "grep -n 'process_tiers\\|unknown' scripts/validate-agent-assets.py scripts/generate-agent-configs.py"
    output: "only `assets.<name> has an unknown source` at validate-agent-assets.py:719; no top-level key check"
  - claim: "workflow_dispatch runs a workflow only once its file is on the default branch, so regime.yml is merged unlisted, dry-run from main against a closed PR, then listed as required"
    command: "WebFetch docs.github.com events-that-trigger-workflows (workflow_dispatch)"
    output: "This event will only trigger a workflow run if the workflow file exists on the default branch"
---

# AGMSG-TASK dotfiles-T128-v1c-regime-ci-check-a01 — regime v3 wave V1c: the main-pinned CI `regime` check

DRAFT; dispatched after V1 merges (it calls V1's validator). Implements the CI half of T128 INV-1 (split by responsibility on operator direction 2026-10-11). Design tier (workflow and gate-adjacent script). Claude seat, `.claude/worktrees/worker-c`, branch `feat/regime-ci-check` from `origin/main`.

## Ponytail constraints (binding)

- The workflow is a thin caller; every decision lives in `scripts/regime-check.sh` (under 80 lines, shdoc header, unit-tested with a scratch repository). Reuse V1's `scripts/validate-task.py`; no second parser. Size caps: 15 files, 500 added lines outside tests/ and .orchestration/ (self-measure). One deterministic fact per round.

## What to build

1. `scripts/regime-check.sh <base-ref> <head-ref> [--pr <n>]`: (a) list `.orchestration/*/task.md` added or modified in `$(git merge-base <base> <head>)..<head>`, write each head copy with `git show <head>:<path>` into a temporary directory never on `PATH`, run `uv run --no-project --with jsonschema --with pyyaml scripts/validate-task.py` (the caller's checkout, i.e. `main`'s) on them, success when none; (b) a PR carries exactly one `.orchestration/<id>/task.md`: when the range changes anything outside `.orchestration/` (a workflow edit included) exactly one task.md must be in the range, a second one is refused, and an `.orchestration/`-only range with no task.md passes (the boundary PR); (c) require every changed path outside `.orchestration/` to match one of that task.md's `allowed_files` globs (`fnmatch`, `**` and literals), so the tier derived from the declared list is the tier of the real diff; (d) refuse when the range changes `.github/workflows/**` unless the task.md derives design tier (`--print-tier`) and lists each changed workflow; (e) print a one-line summary per step. Exit 1 on refusal with the reason. (b) and (c) answer the Codex Bot's P1 findings on PR #316, threads 4239305427 and 4239305428.
2. `.github/workflows/regime.yml`: `on: pull_request_target: {branches: [main]}` and `workflow_dispatch` with a `pr` input (dry run); `permissions: {contents: read}`; one job `regime` on ubuntu-24.04: default checkout (`main` at the workspace root under `pull_request_target`), `git fetch --no-tags origin "+refs/pull/<n>/head:refs/remotes/pr/head"`, setup-uv (SHA-pinned as in `agent-assets.yml`), `scripts/regime-check.sh origin/main pr/head --pr <n>`, step summary. Discipline (design section 9): never check out the PR head at the root; `uv run --no-project`; no `make`, script or dependency file from the PR tree; no secrets; the diff range from the merge-base, never `github.sha`.
3. `scripts/validate-task.py`: the `process_tiers.<tier>` lookup (PyYAML read of `home/dot_agents/agent-config.yaml` resolved from the script's own location; a missing table is a failure).
4. `home/dot_agents/agent-config.yaml`: `process_tiers` (the table salvaged from the reference branch with v3's stage names: docs = CI+Bot, orchestrator read, merge, 1 revise; review = worker checks, CI+Bot, one schema audit, gate, 2 revises then reset; design = design review, worker checks, CI+Bot, schema audit with invariant map, gate, reset rule, permgate check, 2 revises then reset; profiles per tier; `audit_budget_usd` per tier, 5 by default, INV-9's one field added early because V2's runner reads it, the other budgets are V5b's; no `redesign` profile). `make render-check` must pass.
5. Prose, one paragraph each: SKILL Orchestrator Playbook step 3 (format-2 task files, the validator, the derived tier, the CI `regime` check and the task.md copy) and README (one sentence). No other SKILL section.
6. `tests/unit/test_regime_check.py` (stdlib `unittest`; the script and V1's validator are driven as subprocesses on a scratch repository): the validator fails on a task whose tier has no `process_tiers` entry in a manifest copy and passes when the entry exists (the item-3 rule, tested here because `test_validate_task.py` is V1's file); a PR adding a valid task.md passes; a second task.md in the range is refused; an invalid one fails with the validator's message; a code change with no task.md in the range is refused while an `.orchestration/`-only diff passes; a changed path outside the task.md's `allowed_files` is refused; a workflow edit without a design-tier task.md is refused and with one is accepted; each fails when its rule is removed.

## Validation

the module under `make unit-test`; `shellcheck scripts/regime-check.sh`; `make render-check`; `prettier --check` on the two prose files; YAML-parse the workflow; the size measurement; `invariant: INV-1 → …` lines. After the merge the orchestrator runs the `workflow_dispatch` dry run from `main` against closed PR #313 and then lists `regime` as a required check (acceptance record).

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-v1c-regime-ci-check-a01/task.md`; evidence files beside it on the branch.

## Completion

Draft PR within 30 minutes (`feat(regime): main-pinned CI check that validates task files and guards workflow edits`), CI, Bot wait, artifacts, `memory add`, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=10. Forbidden: `scripts/require-crit-review.py`, `Makefile`, anything else; `make update`; thread resolution.
