---
format: 2
task_id: dotfiles-T128-v1-task-schema-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - schemas/task.json
  - scripts/validate-task.py
  - scripts/lib/high_risk_paths.py
  - scripts/legacy-task-ids.txt
  - .github/workflows/regime.yml
  - scripts/regime-check.sh
  - tests/unit/test_validate_task.py
  - tests/unit/test_regime_check.py
  - home/dot_agents/agent-config.yaml
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - README.md
invariants:
  INV-1: every task is a format-2 file whose front matter validates against schemas/task.json (jsonschema + PyYAML, no hand-written parser); the tier (docs, review, design) is derived from allowed_files by the shared high-risk module and selects the pipeline from process_tiers in agent-config.yaml; the CI job validates every task file the PR adds or changes, and the orchestrator can add or skip a stage only with an operator waiver named in the acceptance record
premises:
  - claim: PyYAML is already used via uv in the Makefile and CI; jsonschema is not named anywhere yet (this wave adds --with jsonschema); both resolve through uv on the host
    command: "uv run --no-project --with jsonschema --with pyyaml python -c 'import jsonschema, yaml; print(jsonschema.__version__, yaml.__version__)'"
    output: "4.26.0 6.0.3"
  - claim: the manifest validator and renderer ignore an unknown top-level key, so process_tiers needs no validator change
    command: "grep -n 'process_tiers\\|unknown' scripts/validate-agent-assets.py scripts/generate-agent-configs.py"
    output: "only `assets.<name> has an unknown source` at validate-agent-assets.py:719; no top-level key check"
  - claim: a pull_request_target workflow job is eligible as a required status check and runs the base branch's workflow file
    command: "WebFetch docs.github.com troubleshooting-required-status-checks; events-that-trigger-workflows"
    output: "eligible events: push, pull_request, pull_request_review, pull_request_target, deployment, deployment_status; pull_request_target runs in the context of the default branch of the base repository"
  - claim: required checks must always report, so the job has no path filter and reports success on an unrelated diff
    command: "sed -n 1,12p .github/workflows/test.yaml"
    output: "comment: Do not add workflow-level path or branch filters here: GitHub can leave skipped required checks in a pending state and block merges"
  - claim: the design-tier path list and the process-tier table exist on the closed reference branch and are salvaged, not re-invented
    command: "git show origin/feat/task-validator:scripts/lib/high_risk_paths.py | sed -n 61,95p; git show origin/feat/task-validator:home/dot_agents/agent-config.yaml | sed -n 346,380p"
    output: "DESIGN_TIER = (Makefile, install/**, home/.chezmoiscripts/**, setup.sh, scripts/lib/github-release.sh, …, home/dot_agents/permgate-policy.yaml, home/dot_config/git/config.tmpl); process_tiers: docs/review/design with stages, profiles, limits"
---

# AGMSG-TASK dotfiles-T128-v1-task-schema-a01 — regime v3 wave V1: task schema, validator, tier derivation, main-pinned CI check

DRAFT, not dispatched until the T128 design review (`dotfiles-T128-design-review-a01`) returns `Design verdict: accept` and this file has been read by a fresh context. Drafted 2026-10-11 by the orchestrator seat. Implements T128 INV-1 only (INV-2's caps are the next two-file PR, V1b). Design tier (gate script and workflow). Claude seat on the `standard` profile; worktree `.claude/worktrees/worker-c` on a fresh branch `feat/task-schema` from `origin/main` (`git switch -c feat/task-schema --no-track origin/main`).

## Ponytail constraints (binding)

- Reuse: PyYAML for front matter, `jsonschema` for validation (`uv run --no-project --with jsonschema --with pyyaml`), `fnmatch` for the tier globs, the existing `HIGH_RISK_*` constants of `scripts/require-crit-review.py` (copied into `scripts/lib/high_risk_paths.py` with one test asserting equality with the gate's tuples; the gate itself is not edited in this PR). No hand-written YAML parser, no glob automaton, no canonical-hash code (that is V4's).
- Size: at most 11 files; `scripts/legacy-task-ids.txt` is data and excluded from the added-line measurement; `scripts/validate-task.py` under 120 lines; `schemas/task.json` under 120 lines; `scripts/lib/high_risk_paths.py` under 80 lines; the test module under 250 lines. The CI check for INV-2 does not exist yet, so you measure yourself: `git diff --numstat origin/main...HEAD | awk '$3 !~ /^(tests\/|\.orchestration\/)/ && $3 != "scripts/legacy-task-ids.txt" {a+=$1} END {print a}'` must stay at or under 500.
- One deterministic fact per round: every Bot or CI finding you fix gets a test that fails on the previous head first; a finding you believe wrong is answered on the thread with the refuting command and output, never silently.

## What to build

1. `schemas/task.json` (JSON Schema 2020-12): `format` const 2; `task_id` pattern `^[a-z0-9-]+-T[0-9]+[a-z0-9-]*-a[0-9]{2}$`; `kind` enum `code|review|docs|design`; `security` boolean; `allowed_files` array of strings (required when `kind` is `code`); `invariants` object with keys matching `^INV-[0-9]+$` and string values (at least one when `security` is true); `threat_model` object of strings and `trust_anchors` array of strings (required for `kind: design`); `design_review` object `{receipt, design}` (required when `security` is true); `implementing_tasks`, `supersedes`, `reset_of`, `continuation_of` arrays of task ids; `superseded_by` string; `premises` array of `{claim, command, output}` objects (required for `kind: code` and `kind: design`); `tier` enum `docs|review|design` optional (stamped, must equal the derived tier when present); `additionalProperties: false`.
2. `scripts/lib/high_risk_paths.py`: `REVIEW_TIER_PREFIXES`, `REVIEW_TIER_FILES`, `REVIEW_TIER_TOKENS`, `LOW_RISK_SUFFIXES` (copies of the gate's constants, same values), `DESIGN_TIER` (the salvaged glob list from the reference branch), and one function `tier_of(paths) -> "docs"|"review"|"design"` using `fnmatch.fnmatch` for the design globs and the gate's prefix, file and token rules for the review tier; prose-only paths (every path ends in a `LOW_RISK_SUFFIXES` suffix and matches no design glob) are `docs`.
3. `scripts/validate-task.py <file>...`: read the YAML front matter with `yaml.safe_load`, validate with `jsonschema.Draft202012Validator` (every error printed as `<file>: <json pointer>: <message>`), skip a file whose task id is listed in `scripts/legacy-task-ids.txt` (PR #313's list, 310 ids, only ever shrinks) with a `grandfathered` note and fail any other file without `format: 2`, derive the tier, fail when `security` is false for a design-tier task or when a stamped `tier` differs, require `process_tiers.<tier>` to exist in the manifest (read with PyYAML from `home/dot_agents/agent-config.yaml`, path resolved from the script's own location), `--print-tier`, exit 1 on any failure. No other behaviour.
4. `.github/workflows/regime.yml`: `on: pull_request_target: {branches: [main]}`, `permissions: {contents: read}`, one job `regime` on ubuntu-24.04. Discipline (T128 section 9): `main` stays at the workspace root (default checkout under `pull_request_target`); the PR head is fetched as data (`git fetch --no-tags origin "+refs/pull/${{ github.event.pull_request.number }}/head:refs/remotes/pr/head"`); the diff range is `$(git merge-base origin/main pr/head)..pr/head`, never `github.sha`; PR files are read with `git show pr/head:<path>` into a temporary directory never on `PATH`; `uv run --no-project`; no `make`, script or dependency file from the PR tree; no secrets. Steps: (a) validate every `.orchestration/*/task.md` added or modified in the range with main's `scripts/validate-task.py` (success when none); (b) refuse the PR when the range changes `.github/workflows/**` unless its `task.md` is design tier (`--print-tier`) and lists the changed workflow in `allowed_files`; (c) a step summary listing the validated files. The job's logic lives in `scripts/regime-check.sh` (under 80 lines, shdoc header, unit-tested with a scratch repository) so the workflow is a thin caller and the script is exercised by `make unit-test`; `regime.yml` also accepts `workflow_dispatch` with a PR number for a dry run against a closed PR. Pin actions by SHA as the other workflows do.
5. `home/dot_agents/agent-config.yaml`: `process_tiers` (salvaged table with v3's stage names: docs = CI+Bot, orchestrator read, merge, 1 revise; review = worker checks, CI+Bot, one schema audit, gate, 2 revises then reset; design = design review, worker checks, CI+Bot, schema audit with invariant map, gate, reset rule, permgate check, 2 revises then reset; profiles per tier; no `redesign` profile).
6. Prose, one paragraph each: SKILL "Orchestrator Playbook" step 3 (task files are format 2, validated by `scripts/validate-task.py`; the tier is derived; the CI `regime` check validates them) and README (one sentence under the agent review assets section). No other SKILL section.
7. Tests `tests/unit/test_validate_task.py`: a valid design file (use `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` as a fixture copy) passes; each required key missing fails with the pointer; `additionalProperties`; a design-tier `allowed_files` with `security: false` fails; a stamped wrong tier fails; grandfather note for a legacy file; the constants equal the gate's (import `scripts/require-crit-review.py` by path as the existing tests do); `tier_of` on docs, review and design examples; each test fails when its rule is removed (show one removal per rule in the validation file).

## Validation (paste verbatim output)

`uv run --no-project --with jsonschema --with pyyaml scripts/validate-task.py .orchestration/tasks/dotfiles-T128-regime-v3-a01.md .orchestration/tasks/dotfiles-T128-v1-task-schema-a01.md --print-tier`; `make unit-test` (or the single module under `uv run --no-project --with pytest --with jsonschema --with pyyaml -m pytest tests/unit/test_validate_task.py`); `shellcheck`-free (no shell); `prettier --check` on the two prose files; `actionlint` on the workflow if installed, otherwise `python -c 'import yaml; yaml.safe_load(open(".github/workflows/regime.yml"))'`; the size measurement above; `invariant: INV-1 → tests/unit/test_validate_task.py::<test>, <file:line>` lines.

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-v1-task-schema-a01/task.md` as the first commit (T128 INV-1/INV-8: the CI check validates that copy; every AGMSG-TASK carries its sha256; after an amendment you recommit the new file). Never edit that copy; your evidence files, and any `revise.yaml`, go beside it under the same directory on the branch. Precondition met by the orchestrator: the T128 design is on `main` through a boundary PR before this TASK is sent.

## Completion

Draft PR within 30 minutes of the TASK (`gh pr create --draft --head feat/task-schema`, English title `feat(regime): validate format-2 task files against a JSON Schema in a main-pinned CI check`), then push, CI, Bot wait (Worker Playbook step 15), artifacts at the expected paths, `memory add`, `AGMSG-RESULT v1 task_id=dotfiles-T128-v1-task-schema-a01 …` via `agmsg-dispatch dotfiles-conformance <you> claude-deep-dot w5:p1 "<line>"`. A question is `AGMSG-PONG status=question` with your default stated; you proceed on the default. max_turns=12.

Forbidden: `scripts/require-crit-review.py`, `Makefile`, any other file; `make update`; thread resolution; a second hand-written parser of any kind.
