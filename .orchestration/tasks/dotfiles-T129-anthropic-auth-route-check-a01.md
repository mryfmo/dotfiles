---
format: 2
task_id: dotfiles-T129-anthropic-auth-route-check-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/validate-agent-assets.py
  - tests/unit/test_validate_agent_assets.py
  - .orchestration/dotfiles-T129-anthropic-auth-route-check-a01/**
after: []
threat_table:
  - control: "the PR edits scripts/validate-agent-assets.py in two places (the function validate_anthropic_auth_route and its one call in main beside validate_no_obvious_secrets)"
    disposition: "closed: tests/unit/test_validate_agent_assets.py::test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment"
  - control: the PR edits tests/unit/test_validate_agent_assets.py only for the new case
    disposition: "residual: one new test beside the existing ones, which stay byte-identical; the fixture tree is written by the test"
  - control: "the applied files as an input (every tracked file under home/ and install/, read as text)"
    disposition: "residual: read-only text scan with two fixed rules; a file the rules refuse fails the validator in the agent-assets workflow, which is the check's purpose; no file is executed or rendered"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-anthropic-auth-route-check-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the test runs the validator as a subprocess on a fixture tree in a temporary directory, as the module's secret-scan tests do, and imports only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the validator runs under uv with pyyaml in the agent-assets workflow as today (premise 3), reads the tracked files git ls-files lists and nothing from the environment; a PR checkout as cwd chooses nothing new"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script (one function in the existing validator); any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: no applied file on origin/main names ANTHROPIC_OAUTH_TOKEN or ANTHROPIC_API_KEY today, so the check lands green and its first refusal will be a real one
    command: git grep -lE "ANTHROPIC_(OAUTH_TOKEN|API_KEY)" origin/main -- home install | wc -l | tr -d " "
    output: |-
      0
  - claim: the validator on origin/main has a committed-secret scan over tracked files (one function) and no Anthropic rule yet
    command: a=$(git show origin/main:scripts/validate-agent-assets.py | /usr/bin/grep -c "^def validate_no_obvious_secrets"); b=$(git show origin/main:scripts/validate-agent-assets.py | /usr/bin/grep -c "ANTHROPIC" || true); echo "$a $b"
    output: |-
      1 0
  - claim: the agent-assets workflow runs the validator (one line), so the new rule is a CI check with no workflow change
    command: git show origin/main:.github/workflows/agent-assets.yml | /usr/bin/grep -c "scripts/validate-agent-assets.py"
    output: |-
      1
  - claim: the validator test module has secret-scan cases to sit beside (count of test_secret_scan methods)
    command: git show origin/main:tests/unit/test_validate_agent_assets.py | /usr/bin/grep -c "def test_secret_scan"
    output: |-
      10
---

# AGMSG-TASK dotfiles-T129-anthropic-auth-route-check-a01 — the validator refuses an Anthropic OAuth route and a literal API key in the applied files (plan 023 PR D, repository half)

Written 2026-10-17 by the orchestrator seat as the repository half of plan 023's PR D (the operator's decision: Anthropic through an API key only, Anthropic OAuth in omp forbidden by its terms, secrets never committed, only through the environment or omp's auth store). The run-time half (omp's auth store holds no Anthropic OAuth credential, a check-tools probe that ANTHROPIC_OAUTH_TOKEN is unset) is a later task after PR A merges, because check-tools.sh and its bats module are PR A's files today. This task is dependency-free: two rules in the validator, one test.

## Goal

`uv run --with pyyaml scripts/validate-agent-assets.py` (the agent-assets workflow, premise 3) fails when a tracked file under `home/` or `install/` names `ANTHROPIC_OAUTH_TOKEN`, or assigns `ANTHROPIC_API_KEY` a literal value instead of referencing the environment.

## Files

1. `scripts/validate-agent-assets.py`: `validate_anthropic_auth_route()`, called from `main` right after `validate_no_obvious_secrets`, over the files `git ls-files -z -- home install` lists (read as text, undecodable bytes replaced), with two rules, each failing with `fail(...)` naming the file, the line number and the rule: (R1) the line contains `ANTHROPIC_OAUTH_TOKEN` (any occurrence: an export, a template value, a comment that documents the route; the applied files never name it, the OAuth route does not exist on these machines); (R2) the line assigns `ANTHROPIC_API_KEY` (a `=` or `:` after the name) a value that is not empty, not a `$` reference (`$NAME`, `${NAME}`, quoted or not) and not a template expression (`{{ … }}`); the regex is the worker's, the test lines of item 2 are the specification (Amendment 1): a reference such as `apiKey: ANTHROPIC_API_KEY`, `${ANTHROPIC_API_KEY}`, `$ANTHROPIC_API_KEY`, `env: ANTHROPIC_API_KEY` passes. Nothing else changes: `SECRET_PATTERN`, the placeholders and `validate_no_obvious_secrets` stay byte-identical.
2. `tests/unit/test_validate_agent_assets.py`: `test_anthropic_auth_route_refuses_an_oauth_token_in_applied_files_and_a_literal_api_key_assignment`, written as the module's secret-scan tests are (a fixture tree in a temporary directory, the validator run as a subprocess or the function called on the fixture root as those tests do): a file under `home/` with `export ANTHROPIC_OAUTH_TOKEN=x` fails naming R1; `ANTHROPIC_<redacted:secret-pattern>` and `ANTHROPIC_API_KEY: literal` fail naming R2; `ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY`, `apiKey: ANTHROPIC_API_KEY`, `ANTHROPIC_API_KEY=` and `ANTHROPIC_<redacted:secret-pattern>` pass; the same OAuth line under `scripts/` passes (the rule covers applied files only, the checks may name the token).

## Out of scope

check-tools.sh and its bats module (PR A's files; the run-time probe comes with omp's auth-store check after PR A merges); omp's configuration (PR B); any change to SECRET_PATTERN or the placeholders; any workflow file.

## Check

`uv run python -m unittest tests/unit/test_validate_agent_assets.py -v` green and `uv run --offline --with pyyaml scripts/validate-agent-assets.py` (exit 0 on the branch: premise 1) pasted in the validation file, with `ruff check scripts/validate-agent-assets.py tests/unit/test_validate_agent_assets.py` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (no other merge is a precondition). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50; every fix round, before or after the first RESULT, counts toward INV-6's cap of two, C-61); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59); a later review's P2 and every P3 are advisory (C-61), as is any other P2, owned by `dotfiles-T129-anthropic-auth-route-check-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T129-anthropic-auth-route-check-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T129-anthropic-auth-route-check-a01/task.md>` and the evidence paths.

## Amendment 1 (round 1, 2026-10-17T11:11:16Z)

a007's question 1 (PONG 11:08Z): the R2 regex as written tested its lookahead at the optional quote or the whitespace and flagged lines item 2 passes. Decided by default: R2 is stated as its intent and the test lines of item 2 are the specification; the worker writes and tests the regex. Nothing else changes.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-anthropic-auth-route-check-a01.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
premise 4: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-a01.md
```
