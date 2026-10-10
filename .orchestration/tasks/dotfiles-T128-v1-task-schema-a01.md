---
format: 2
task_id: dotfiles-T128-v1-task-schema-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round4.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - schemas/task.json
  - scripts/validate-task.py
  - scripts/lib/high_risk_paths.py
  - scripts/legacy-task-ids.txt
  - tests/unit/test_validate_task.py
invariants:
  INV-1: "every task is a format-2 file whose front matter validates against schemas/task.json (jsonschema + PyYAML, no hand-written parser); the tier (docs, review, design) is derived from allowed_files by the shared high-risk module, with the regime's own rule prose (home/dot_config/claude/rules/**, the agmsg-orchestration SKILL, AGENTS.md, README) listed in the review tier, and selects the pipeline from process_tiers in agent-config.yaml; every AGMSG-TASK for the task, the first and each amendment, carries task_sha256= of the task file as sent, the worker commits the file byte-identical to .orchestration/<task id>/task.md (first commit, recommitted after each amendment), the CI regime job validates that copy with main's schema and refuses a PR that changes .github/workflows/** unless its task.md is design tier and lists the file, the host gate compares the copy's sha256 with the latest AGMSG-TASK's token in history, and the regime check binds only once the ruleset lists it as required (an operator action named in V1's acceptance record); the orchestrator can add or skip a stage only with an operator waiver named in the acceptance record"
premises:
  - claim: PyYAML is already used via uv in the Makefile and CI; jsonschema is not named anywhere yet (this wave adds --with jsonschema); both resolve through uv on the host
    command: "uv run --no-project --with jsonschema --with pyyaml python -c 'import jsonschema, yaml; print(jsonschema.__version__, yaml.__version__)'"
    output: "4.26.0 6.0.3"
  - claim: "bare uv run python (what make unit-test runs) cannot import yaml or jsonschema, so the test module drives the validator as a subprocess under uv run --no-project --with jsonschema --with pyyaml and imports only the stdlib module scripts/lib/high_risk_paths.py directly"
    command: "uv run python -c 'import yaml'; uv run python -c 'import jsonschema'"
    output: "ModuleNotFoundError: No module named 'yaml'; ModuleNotFoundError: No module named 'jsonschema'"
  - claim: "fnmatch's * crosses /, so the tier lists keep only ** and literal patterns (true of the salvaged list)"
    command: "uv run --no-project python -c \"import fnmatch; print(fnmatch.fnmatch('a/b/c.py','a/*.py'))\""
    output: "True"
  - claim: the design-tier path list and the process-tier table exist on the closed reference branch and are salvaged, not re-invented
    command: "git show origin/feat/task-validator:scripts/lib/high_risk_paths.py | sed -n 61,95p; git show origin/feat/task-validator:home/dot_agents/agent-config.yaml | sed -n 346,380p"
    output: "DESIGN_TIER = (Makefile, install/**, home/.chezmoiscripts/**, setup.sh, scripts/lib/github-release.sh, …, home/dot_agents/permgate-policy.yaml, home/dot_config/git/config.tmpl); process_tiers: docs/review/design with stages, profiles, limits"
---

# AGMSG-TASK dotfiles-T128-v1-task-schema-a01 — regime v3 wave V1: task schema, validator, tier derivation (validation only; the CI check is V1c)

DRAFT, not dispatched until the T128 design review (`dotfiles-T128-design-review-a01`) returns `Design verdict: accept` and this file has been read by a fresh context. Drafted 2026-10-11 by the orchestrator seat. Implements the validation half of T128 INV-1 (the CI `regime` job, `process_tiers` and the prose are V1c, dispatched after this PR merges; INV-2's caps are V1b). Split by responsibility on operator direction 2026-10-11. Design tier (gate script and workflow). Claude seat on the `standard` profile; worktree `.claude/worktrees/worker-c` on a fresh branch `feat/task-schema` from `origin/main` (`git switch -c feat/task-schema --no-track origin/main`).

## Ponytail constraints (binding)

- Reuse: PyYAML for front matter, `jsonschema` for validation (`uv run --no-project --with jsonschema --with pyyaml`), `fnmatch` for the tier globs, the existing `HIGH_RISK_*` constants of `scripts/require-crit-review.py` (copied into `scripts/lib/high_risk_paths.py` with one test asserting equality with the gate's tuples; the gate itself is not edited in this PR). No hand-written YAML parser, no glob automaton, no canonical-hash code (that is V4's).
- Size: five files; `scripts/legacy-task-ids.txt` is data and excluded from the added-line measurement; `scripts/validate-task.py` under 120 lines; `schemas/task.json` under 120 lines; `scripts/lib/high_risk_paths.py` under 80 lines; the test module under 250 lines. The CI check for INV-2 does not exist yet, so you measure yourself: `git diff --numstat origin/main...HEAD | awk '$3 !~ /^(tests\/|\.orchestration\/)/ && $3 != "scripts/legacy-task-ids.txt" {a+=$1} END {print a}'` must stay at or under 500.
- One deterministic fact per round: every Bot or CI finding you fix gets a test that fails on the previous head first; a finding you believe wrong is answered on the thread with the refuting command and output, never silently.

## What to build

1. `schemas/task.json` (JSON Schema 2020-12): `format` const 2; `task_id` pattern `^[a-z0-9-]+-T[0-9]+[a-z0-9-]*-a[0-9]{2}$`; `kind` enum `code|review|docs|design`; `security` boolean; `allowed_files` array of strings (required when `kind` is `code`); `invariants` object with keys matching `^INV-[0-9]+$` and string values (at least one when `security` is true); `threat_model` object of strings and `trust_anchors` array of strings (required for `kind: design`); `design_review` object `{receipt, design}` (required when `security` is true); `implementing_tasks` object whose keys match the task-id pattern and whose values are arrays of `^INV-[0-9]+$` strings (the design's map); `supersedes` and `reset_of` arrays of task ids; `premises` array of `{claim, command, output}` objects (required for `kind: code` and `kind: design`); `tier` enum `docs|review|design` optional (stamped, must equal the derived tier when present); `additionalProperties: false`.
2. `scripts/lib/high_risk_paths.py`: `REVIEW_TIER_PREFIXES`, `REVIEW_TIER_FILES`, `REVIEW_TIER_TOKENS`, `LOW_RISK_SUFFIXES` (copies of the gate's constants, same values), `DESIGN_TIER` (the salvaged glob list from the reference branch plus `.github/workflows/**`, `scripts/regime-check.sh`, `scripts/pr-caps.sh`, `schemas/**`; only `**` and literal patterns), `README.md` added to `REVIEW_TIER_FILES` (the regime's rule prose is review tier: `home/dot_config/claude/rules/**`, the SKILL, `AGENTS.md`, README), and one function `tier_of(kind, paths) -> "docs"|"review"|"design"` with precedence design, then review, then docs: a `kind: design` task is design whatever its paths; any path matching a design glob makes the task design; otherwise any path matching the gate's prefix, file or token rules makes it review; otherwise docs; a `kind: review` or `docs` task without `allowed_files` is docs.
3. `scripts/validate-task.py <file>...`: read the YAML front matter with `yaml.safe_load`, validate with `jsonschema.Draft202012Validator` (every error printed as `<file>: <json pointer>: <message>`), skip a file whose task id is listed in `scripts/legacy-task-ids.txt` (PR #313's list, 310 ids, only ever shrinks) with a `grandfathered` note and fail any other file without `format: 2`, derive the tier, fail when `security` is false for a design-tier task or when a stamped `tier` differs, `--print-tier`, exit 1 on any failure; the `process_tiers` lookup arrives with V1c, which adds the table. No other behaviour.
4. Tests `tests/unit/test_validate_task.py` (stdlib `unittest`, run by `make unit-test` under bare `uv run python`, which cannot import yaml or jsonschema: the tests drive `scripts/validate-task.py` as a subprocess through `uv run --no-project --with jsonschema --with pyyaml` and import only `scripts/lib/high_risk_paths.py` directly): a valid design file (use `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` as a fixture copy) passes; each required key missing fails with the pointer; `additionalProperties`; a design-tier `allowed_files` with `security: false` fails; a stamped wrong tier fails; grandfather note for a legacy file; the constants equal the gate's (import `scripts/require-crit-review.py` by path as the existing tests do); `tier_of` on docs, review and design examples, including a rules file under `home/dot_config/claude/rules/` deriving review and a `kind: design` task with prose paths deriving design; each test fails when its rule is removed (show one removal per rule in the validation file).

## Validation (paste verbatim output)

`uv run --no-project --with jsonschema --with pyyaml scripts/validate-task.py .orchestration/tasks/dotfiles-T128-regime-v3-a01.md .orchestration/tasks/dotfiles-T128-v1-task-schema-a01.md --print-tier`; `make unit-test` (the module runs under bare `uv run python` and shells out as described); the size measurement above; `invariant: INV-1 → tests/unit/test_validate_task.py::<test>, <file:line>` lines.

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-v1-task-schema-a01/task.md` as the first commit (T128 INV-1/INV-8: the CI check validates that copy; every AGMSG-TASK carries its sha256; after an amendment you recommit the new file). Never edit that copy; your evidence files, and any `revise.yaml`, go beside it under the same directory on the branch. Precondition met by the orchestrator: the T128 design is on `main` through a boundary PR before this TASK is sent.

## Completion

Draft PR within 30 minutes of the TASK (`gh pr create --draft --head feat/task-schema`, English title `feat(regime): validate format-2 task files against a JSON Schema`), then push, CI, Bot wait (Worker Playbook step 15), artifacts at the expected paths, `memory add`, `AGMSG-RESULT v1 task_id=dotfiles-T128-v1-task-schema-a01 …` via `agmsg-dispatch dotfiles-conformance <you> claude-deep-dot w5:p1 "<line>"`. A question is `AGMSG-PONG status=question` with your default stated; you proceed on the default. max_turns=12.

Forbidden: `scripts/require-crit-review.py`, `Makefile`, any other file; `make update`; thread resolution; a second hand-written parser of any kind.
