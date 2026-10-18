---
format: 2
task_id: dotfiles-T133-task-generator-plan-check-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/task-from-plan.py
  - scripts/orchestrator/plan-check.py
  - scripts/orchestrator/task-consistency-check.py
  - tests/unit/test_task_from_plan.py
  - tests/unit/test_plan_check.py
  - tests/unit/test_task_consistency_c11_c15.py
  - tests/unit/test_task_checkers.py
  - .orchestration/dotfiles-T133-task-generator-plan-check-a01/**
after: []
threat_table:
  - control: "the PR adds scripts/orchestrator/task-from-plan.py (plan 024 programs (12): a task.md skeleton from one todo row, allowed_files proposed by git grep, every premise command run and its output pasted, threat rows drafted per allowed_files entry, the Check commands run once in a scratch worktree with their exit codes pasted; it writes only the named task file and prints the checker's verdict)"
    disposition: "closed: tests/unit/test_task_from_plan.py::test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs"
  - control: "the PR adds scripts/orchestrator/plan-check.py (programs (15): form, drift and invariant checks over the plan 024 files; one violation per line, exit 1; drift read through gh and git, invariants through fixed forbidden patterns)"
    disposition: "closed: tests/unit/test_plan_check.py::test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan"
  - control: "the PR edits scripts/orchestrator/task-consistency-check.py by adding C11 to C15 after C10 (the three shape rules of a disposition, the wildcard unit rule, the three disposition forms, premises re-run, INV-2 byte equality); C1 to C10 and C7b unchanged"
    disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged"
  - control: "tests/unit/test_task_from_plan.py (new; a fixture todo table, a fixture repository and a stub gh on PATH; the generated file is checked by the real checker)"
    disposition: "residual: fixtures in a temporary directory; the generator never writes outside the named task file"
  - control: "tests/unit/test_plan_check.py (new; fixture plan files, a stub gh and a temporary git repository for the drift checks)"
    disposition: "residual: fixtures only; no live GitHub"
  - control: "tests/unit/test_task_consistency_c11_c15.py (new; one red fixture per new check and the current task files as the green set)"
    disposition: "residual: the fixtures are task files in a temporary directory; the audit reads each case"
  - control: "tests/unit/test_task_checkers.py (amendment 1: two expected-set edits only, the C4 fixture's disposition and the historical expectation's new ids, after PR #413 merges)"
    disposition: "residual: the diff of that module against origin/main after the rebase holds exactly the two edits named in amendment 1, each justified in report.md; the task-level audit compares the diff against them"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: "the branch evidence records under .orchestration/dotfiles-T133-task-generator-plan-check-a01/ (report.md, validation.md, sandbox.md, learning.md)"
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C15 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the generator writes one task file and a scratch worktree under $TMPDIR that it removes; plan-check writes nothing (its --drift report goes to stdout; the progress.tsv write is the orchestrator's); the checker stays read-only; every premise and Check command the generator runs comes from the plan text and runs under python -I or bash with set -euo pipefail, never through a shell string the plan controls"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow file is in allowed_files (the validate CI wiring of plan-check is P1-11 s regime job); the scripts run under uv run --offline --with pyyaml python -I; gh is read-only (pr view, api GET)"
  - control: new or renamed scripts
    disposition: "residual: 2 new scripts under scripts/orchestrator, both named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: none of the five new files exists on origin/main
    command: git ls-files scripts/orchestrator/task-from-plan.py scripts/orchestrator/plan-check.py tests/unit/test_task_from_plan.py tests/unit/test_plan_check.py tests/unit/test_task_consistency_c11_c15.py | wc -l
    output: |-
      0
  - claim: the checker documents eleven checks today (C1 to C10 and C7b), so C11 to C15 are additions at the end of its list
    command: /usr/bin/grep -c '^C[0-9]*b\? ' scripts/orchestrator/task-consistency-check.py
    output: |-
      11
  - claim: the plan 024 group is eleven files (ten Markdown documents and the progress TSV), the set plan-check reads
    command: /bin/ls .orchestration/plans/024-*.md .orchestration/plans/024-progress.tsv | wc -l
    output: |-
      11
  - claim: the todo table has fifteen P1 rows, the rows task-from-plan reads
    command: /usr/bin/grep -c '^| P1-' .orchestration/plans/024-todo.md
    output: |-
      15
  - claim: tests/unit/test_task_checkers.py is in flight in PR #413, so the new checks get their own test module
    command: git ls-files tests/unit/test_task_checkers.py | wc -l
    output: |-
      1
---

# AGMSG-TASK dotfiles-T133-task-generator-plan-check-a01 — the task generator, the checker's C11 to C15 and the plan checker (plan 024 P1-12)

Written 2026-10-18 by the orchestrator seat from plan 024 (`024-todo.md` row P1-12, `024-design-programs.md` items (12) and (15), `024-design-quality.md` 5.10 M4 and 5.13, and today's mistakes M-20261018-09 (Check commands never run in a seat before dispatch; C-68), M-20261018-10 (INV-6 overrun; C-69's `reset-task.sh` is a later item, not this task) and M-20261018-11 (ruleset by prose; C-71 is P1-14's)). Seat: claude-standard-dot-a009 (worker-c). Harness-independent Python; no file in flight elsewhere (`tests/unit/test_task_checkers.py` is PR #413's, so the new checks are tested in their own module).

## Goal

A task text is generated from its todo row with every premise and Check command actually run, the consistency check refuses the disposition and premise shapes the reviewers kept finding by hand, and the plan group is checked for form, drift and forbidden patterns by a script instead of by reading.

## Files

1. `scripts/orchestrator/task-from-plan.py <todo-id> [--out .orchestration/tasks/<id>.md] [--seat <identity>] [--worktree <path>]` (new, python, stdlib plus PyYAML through `uv run --offline --with pyyaml python -I`): reads the row `<todo-id>` of `.orchestration/plans/024-todo.md` (the four columns: purpose, work, completion), the program items it names in `024-design-programs.md` (by their `(n)` numbers) and the wave table row of `024-omp-cutover-and-corrective-order.md` section 6 for the seat; writes a format-2 task file: `task_id` from `--out`, `kind: code`, `security: true` when the todo's quality row names the id, `allowed_files` = every path the row or its program items name plus the paths `git grep -l` finds for each named script or test (proposed, each with a `# from: <grep hit>` trailing comment line in the body's Files section, not in the YAML), `after: []`, a threat table with one row per allowed_files entry (control: the path, followed by a space and a short clause from the row's text; disposition `residual: <the row's completion sentence>` as a draft the orchestrator replaces), the task-copy, evidence, non-path and orchestrator-effect rows copied from `.orchestration/tasks/dotfiles-T133-result-precheck-a01.md` (the regime's current wording), and `premises` built by running each `command:` the row's program items quote in backticks and pasting its real output (a command that fails to run is pasted with its exit code and marked `verify:` in the claim); the body carries Goal (the todo's purpose), Files (the program items' sentences, one numbered item per program), Out of scope, Check (the Check commands of the sibling task file the row's wave names, each run once in a scratch worktree `git worktree add --detach $TMPDIR/<id> origin/main` and pasted as `# exit <n> on origin/main` beside the command, the worktree removed with `git worktree remove --force`) and Completion (the Completion clause sentence of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applied as written with `<id>-followup-a01` as the advisory owner), then the `## Checks (pasted by the orchestrator before each send)` block; finally it runs `task-consistency-check.py` on the file and prints its output; exit 0 when the checker passes, 1 otherwise (the file is still written for editing). Nothing is recalled: a premise output is always the command's own stdout.
2. `scripts/orchestrator/task-consistency-check.py` gains, after C10 and in the docstring's list: C11 the disposition shape rules (a `closed:` payload is `tests/<path>::<name>` with `<name>` a Python identifier; an `out-of-scope:` payload is a task id that exists as `.orchestration/tasks/<id>.md`; a `residual:` payload is at least 20 characters); C12 the wildcard unit rule (an `allowed_files` entry with a glob that matches an executed or applied kind, `*.sh`, `*.py`, `*.yaml`, `*.yml`, `*.json`, `*.toml` or a path under `home/`, `scripts/`, `.githooks/` or `.github/`, needs one row per concrete file the glob matches in the tree, except a glob under `tests/fixtures/` or the task's own `.orchestration/<id>/`); C13 every disposition is exactly one of the three forms (the prefix `closed:`, `residual:` or `out-of-scope:` followed by a space); C14 premises re-run (every premise's `command` is run from the repository root under `bash -c` with `set -o pipefail`, PATH limited to the repository's bin and `/usr/bin:/bin`, and its stdout must equal the pasted `output` byte for byte; a command naming `gh`, `curl` or a URL is skipped with a `C14 skipped network premise` note, never a failure); C15 INV-2 (when the front matter carries `invariants`, each listed id's sentence in the design file the front matter names, read from `origin/main`, equals the task's quoted sentence byte for byte). Each check prints one `C<n> …` line per finding as the existing ones do.
3. `scripts/orchestrator/plan-check.py [--root <repo>] [--drift] [--invariants]` (new): form, over the eleven `024-*` files: every `024-todo.md` row has a non-empty completion column; rows the wave table places in one wave have pairwise-disjoint `allowed_files` once their task files exist (read from `.orchestration/tasks/`); every `P1-<n>` row names at least one bottleneck id `B<n>` or `M<n>` present in `024-design-mechanism.md` 5.0 or `024-design-quality.md` 5.10; every DoD row of `024-checklists.md` holds a backtick command or an explicit file path; every decision row of the plan's section 2 has a bold default; every `#<pr>`, `dotfiles-T<n>-…` id and `D-…` id the files cite exists (PR numbers by `gh pr view` when `--drift`, task ids as files, decision ids in `.orchestration/decisions.tsv`). `--drift`: for every `#<pr>` cited with a head sha or a state word (CLEAN, BEHIND, draft, merged, closed), compare with `gh pr view <pr> --json headRefOid,mergeStateStatus,isDraft,state`; for every `024-progress.tsv` row whose id is a task, compare its state word with the latest `AGMSG-ACCEPTANCE` status in `.orchestration/acceptance/<id>.md`; print one `drift: <file>:<line> <cited> != <live>` per difference. `--invariants`: the forbidden patterns `ANTHROPIC_OAUTH_TOKEN=` with a value, `git push origin main`, `--admin`, `--auto` (as `gh pr merge` flags), and a `permissions.ask` entry added in a diff against `origin/main`; one line per hit. Exit 1 on any violation, 0 otherwise; the orchestrator runs it at each boundary (the `validate` CI wiring is P1-11's).
4. Tests: `tests/unit/test_task_from_plan.py` (`test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs`: a fixture todo table and program file with two backtick commands, one that prints a known string and one that exits 3; the generated file passes C1 to C15, carries the string as its first premise output and `verify:` with `exit 3` on the second, lists `git grep` proposals, and the scratch worktree is gone afterwards), `tests/unit/test_plan_check.py` (`test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan`: a clean fixture plan group passes; one fixture per rule fails with exactly one line; `--drift` against a stub gh that answers a different head; `--invariants` on a fixture holding `--admin`), `tests/unit/test_task_consistency_c11_c15.py` (`test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged`: one task fixture per new check, each red on exactly its check; every current file under `.orchestration/tasks/dotfiles-T133-*.md` passes C1 to C13 and C15 (C14 re-runs premises, so the fixture set for C14 is the task's own file with a premise whose output is edited)). Fixture lines count against the test cap.

## Out of scope

`reset-task.sh` (C-69, a later P1-12 item once this lands), `dispatch.sh --next` (P1-6), the `regime` CI job and the `validate` wiring (P1-11), `ruleset-request.sh` and `ruleset-verify.sh` (P1-14), any change to the plan files themselves (plan-check reports; the orchestrator edits).

## Check

`make unit-test`, `make format`, `uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers -v` green, `uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T133-*.md` green (C1 to C15), `uv run --no-project --with pyyaml python -I scripts/orchestrator/plan-check.py` run once with its output pasted (violations in the plan files are reported, not fixed), all pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 600 changed lines outside `tests/` and `.orchestration/`, 700 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main`. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-task-generator-plan-check-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears) and `task_copy=<sha256 of .orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md>` in the RESULT; the RESULT also carries `precheck=` when `scripts/orchestrator/result-precheck.sh` has merged (PR #411), else `precheck=pending-411`. `security: true`: the orchestrator runs the task-level audit and the security-profile review on the final head. No `@codex review` comment; single commands for every gh and git write; a classifier denial is a blocked PONG.

## Amendment 1 (round 1, 2026-10-18T10:3xZ): the two exact-set tests of tests/unit/test_task_checkers.py

a009's question PONG (10:13:51Z). Option (a) applies. `tests/unit/test_task_checkers.py` joins `allowed_files` for exactly two edits: the C4 boundary test's fixture gets a well-formed disposition (one of the three forms), so C13 leaves its expected set, and the ten-historical-files test's expected sets gain the ids among C11, C14 and C15 that the new checks report on those files, each added id justified in report.md by the check's finding on that file. No other line of that module changes. That file is in flight in PR #413 (`dotfiles-T129-audit-inherit-replan-json-followup-a01`), so this branch takes #413's merge first: commit and push everything else now (the generator, plan-check.py, C11 to C15, the three new modules; no PR yet), hold the two test edits uncommitted, and when the orchestrator's `AGMSG-PING … reason=413-merged sha=<main sha>` arrives, rebase onto `origin/main` (single commands), apply the two edits, run `uv run python -m unittest tests.unit.test_task_checkers -v` and the task's modules, push, open the PR and send the RESULT. Two clarifications from the real-run results, not new items: C14 compares the recorded premise output with the rerun after collapsing runs of whitespace (BSD `wc` pads its counts), and a premise whose command needs a tool absent from the mandated PATH (`uv`, `codex`) reports `C14: tool absent <name>` as a warning, never as a failure; a premise that differs because a merge moved the repository is a real C14 finding and stays one. The six plan-check violations are findings for report.md, not fixes in this task. This is INV-6's first amendment (C-61); the counters are pasted below.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-task-generator-plan-check-a01.md: OK
premises 1 to 5: outputs pasted at write time (2026-10-18 18:0x JST)
masked 0 match(es)
```
