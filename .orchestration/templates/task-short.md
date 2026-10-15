# Short-form task template (plan 021 step 7.1)

A short-form task is one mechanism, its own test module, no rule text, at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2). The file is `.orchestration/tasks/<task-id>.md`; its sha256 is the TASK line's `task_sha256`, pair-confirmed by the review seat and the Codex half before dispatch (one round, fixed stop conditions), and the text is committable as written (`validate-agent-assets.py --mask-secrets` changes nothing in it, C-44).

Copy the skeleton below, fill every `<…>`, delete nothing a row or a section stands for, and run before each send: `scripts/orchestrator/task-consistency-check.py <file>` (C1 to C10, C7b), the premise replay (every `output:` is the stdout of its own `command:`, run from a worktree on `origin/main`: a premise reads `origin/main`, a section of a committed file or a tracked input, never the orchestrator's untracked files or a status log, C-35 and C-45), the structure counts (controls, claims) and the mask check (C-44).

```markdown
---
format: 2
task_id: <lineage>-a0<n>
kind: code
security: false
design_review:
  receipt: <the design review receipt the lineage cites>
  design: <the design file>
allowed_files:
  - <one path per file the items touch; globs only for an evidence directory>
  - .orchestration/<task-id>/**
after: [<the task whose merge this one waits for, or nothing>]
threat_table:
  # one row per allowed_files entry that is code, config or test: closed when a named test closes its risk, residual otherwise
  - control: the PR adds|edits <path>, which <what the change does in one clause>
    disposition: "closed: tests/unit/<module>.py::<test_name>"
  - control: the PR adds tests/unit/<module>.py, the oracle of the rows above (<the stubs and fixtures, what they record and answer>)
    disposition: "residual: the stubs record and answer, nothing else; the audit reads each case against the Files items"
  # one row per non-path control the mechanism touches (a worktree, a daemon, a credentialed write, an environment seam)
  - control: "<the control, in quotes when it holds a colon>"
    disposition: "residual: <why the risk is bounded, and which closed row's case covers it>"
  # the generic rows, verbatim
  - control: the task-file copy on the branch (.orchestration/<task-id>/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/<task-id>/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: <what the tests import and what they run as subprocesses>; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; <every binary each script runs by name, how it is resolved, and the seam the tests use>; <what a PR checkout as cwd can and cannot choose: a binary resolved in the trusted root before any checkout, shims refused, the absolute path used afterwards>"
  - control: new or renamed scripts
    disposition: "residual: <n> new script(s) under <dir>, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: '<one sentence the items rest on, replayable from a worktree on origin/main>'
    command: '<the command; a count reads one section, never a whole file the orchestrator edits>'
    output: |-
      <its stdout, written by the premise runner, never typed>
---

# AGMSG-TASK <task-id> — <the mechanism in one line> (<the plan step or the finding it answers>)

<One paragraph: who drafted it, the form, the source (the audit line, the plan step, the operator decision), the sibling or lineage it belongs to, the attached inputs if any (their sha256 prefixes as facts, read from the orchestrator's main checkout).>

## Goal

<One sentence: the state the repository is in when the PR merges.>

## Files

1. `<path>`: <the behaviour, every argument, output line, exit code and written file; for an attached input, "the input's behaviour (…) with these changes: …", and every failure path the script keeps stated as a failure mode the reviewers judge (fail closed or open, and why)>.
2. `tests/unit/<module>.py` (new), run by `uv run python -m unittest` without PyYAML, importing only the standard library: one test per closed row, named verbatim as the row names it, with the stubs, the fixtures, the cases and the assertions that make the row's risk impossible to pass by accident (an ordering claim needs a case that fails when the order is wrong; a resolution claim needs a decoy that would run under the other resolution).

## Out of scope

<The neighbouring files and mechanisms this task leaves alone, by name.>

## Check

`uv run python -m unittest tests/unit/<module>.py -v` green, pasted in the validation file with `shellcheck <scripts>` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (<after which merge>). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory, owned by `<lineage>-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by <lineage>-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/<task-id>/task.md>` and the evidence paths.
```

## What the orchestrator does around the file

- Create `.orchestration/acceptance/<task-id>.md` with the JSON block `{"dispatch": []}` before the first dispatch (Orchestrator Playbook step 6); `dispatch.sh` appends every TASK line with its read marker; the chain's block writer keeps those lines in a `## Dispatch (bus lines)` section (C-43).
- Write the review brief `<task-id>-review-a01.md` with four stop conditions (sources and premises; `allowed_files` complete and disjoint from in-flight tasks; each closed row's test closes its risk and the Completion matches plan 020 step 4; the checker, the counts and the mask) and run both halves in parallel: the review seat by TASK line, the Codex half by `scripts/orchestrator/codex-review.sh`. A round's edits are line edits with count asserts and an explicit `|| exit 1` on every assertion (`set -e` is inert in the orchestrator's shell, C-40); the files a premise reads stay frozen while the review runs (C-45).
- Every time in a record is the clock read in the writing command or a bus timestamp (C-46); every disposition reason is free of semicolons (C-47); a Bot thread of the final head gets its `<id><TAB><class>` row in the record together with its `extra.tsv` row (C-42).
- An amendment after dispatch travels as a hashed, pair-confirmed TASK line (`amendment=<n>`, `previous_task_sha256` computed from the pre-amendment copy kept under `.orchestration/validation/<task-id>-pre-amend<n>.md`), never as a PONG answer; the worker holds the push until it arrives.

Proposed checker growth (step 7.1, for `scripts/orchestrator/task-consistency-check.py`): C11 the premise replay from a clean worktree on `origin/main`; C12 the mask check; C13 the generic rows present verbatim and one row per allowed file; C14 every closed row's test name present in the test item.
