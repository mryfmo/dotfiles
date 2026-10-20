---
format: 2
task_id: dotfiles-T133-hold-playbook-a01
kind: code
security: false
allowed_files:
  - scripts/orchestrator/hold-playbook.sh
  - tests/unit/test_hold_playbook.py
  - .orchestration/dotfiles-T133-hold-playbook-a01/**
after: []
threat_table:
  - control: scripts/orchestrator/hold-playbook.sh
    disposition: "residual: the fixed Python helper reads records as data, writes only the replan file and the conditional decisions row, and never executes record text or dispatches work; the temporary-directory tests verify these effects."
  - control: tests/unit/test_hold_playbook.py
    disposition: "residual: script executions use a copied script and fixture records in temporary directories; the vocabulary test reads the real learning tree without changing it."
  - control: .orchestration/dotfiles-T133-hold-playbook-a01/**
    disposition: "residual: branch artifacts stay in this task's directory and contain the dispatched copy, source attribution and validation evidence for the final-head audit."
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-hold-playbook-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched text; the TASK and RESULT bind its own sha256 and the orchestrator compares it at acceptance."
  - control: the branch evidence records under .orchestration/dotfiles-T133-hold-playbook-a01/ (report.md, validation.md, sandbox.md, learning.md and worker review evidence)
    disposition: "residual: records contain prose and command output; sandbox.md lists every refused command and the audit compares the claims with the final diff and CI."
  - control: task metadata
    disposition: "residual: the orchestrator checks C1 to C10 and C7b before dispatch and at acceptance; the byte comparison authenticates the complete dispatched front matter."
  - control: metadata separators
    disposition: "residual: the helper reads only the bounded first YAML front-matter document of the input task; the task-copy byte comparison covers every separator."
  - control: in-process effects
    disposition: "residual: the helper creates only .orchestration/tasks/<task>-replan.md and conditionally appends one row to .orchestration/decisions.tsv; it preserves the source task and existing replans and executes no command derived from records."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or environment configuration changes; the script runs its embedded Python helper through uv run --no-project --with pyyaml python -I and loads YAML with yaml.safe_load."
  - control: new or renamed scripts
    disposition: "residual: hold-playbook.sh is the only new script; its Python helper is embedded, and any sibling helper or additional script falls outside allowed_files."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges only through gh pr merge --squash --match-head-commit <audited head> after the integration gate in Orchestrator Playbook step 10.5."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the feedback sweep and the task-level audit bind the new final head before the gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal records the discarded uncommitted state in acceptance."
premises: []
---

# AGMSG-TASK dotfiles-T133-hold-playbook-a01 — plan 024 P1-13 hold playbook

## Goal

`scripts/orchestrator/hold-playbook.sh <task> <class>` expands a pinned corrective procedure into a replan skeleton and records a pending decision when its prospective changes exceed the task's `allowed_files`. It implements item (13) of `.orchestration/plans/024-design-programs.md` and the class-specific playbook of `.orchestration/plans/024-design-quality.md` section 5.13. This task is `security: false`: the script reads records and writes records and executes no PR-controlled input. Existing controls own hold detection at three findings of one class, INV-6's S2 thresholds including two revises, and a P0 finding. The P0 rule remains an immediate revert PR for a defect already on main and hold for an unmerged artifact.

## Files

1. `.orchestration/learning/classes.yaml` is a new tracked mapping keyed by class slug. It contains one entry for every distinct slug in the `classes:` lines of `.orchestration/learning/mistakes/M-*.md`. The worker recounts the records and distinct slugs at start and records both counts in `validation.md`.

   Each entry has `remedy:` and `blast_radius:`. The remedy is one or two plain sentences describing a corrective procedure derived from the records' Corrections lines and their references in `.orchestration/learning/corrections-inventory.tsv`. The blast radius is a list of repository-relative globs naming files a fix of that class touches, derived from the records' Evidence lines. The report attributes each entry to its source mistake records and correction references. A class without a known corrective procedure has `remedy: unknown` and `blast_radius: []`. Review titles and illustrative class names do not add vocabulary entries.

   `tests/unit/test_hold_playbook.py::HoldPlaybookTests::test_vocabulary_covers_mistake_classes` reads the real mistake records and asserts that every recorded slug appears in this mapping. `tests/unit/test_hold_playbook.py::HoldPlaybookTests::test_known_class_without_remedy_is_reported` verifies the explicit unknown-remedy representation.

2. `scripts/orchestrator/hold-playbook.sh` accepts exactly `<task> <class>`. A small Python helper embedded in the shell script performs parsing and record generation through `uv run --no-project --with pyyaml python -I`. It uses `yaml.safe_load` for the class mapping and the task's first YAML front-matter document. Shell comments use English shdoc annotations.

   The task id matches `^[A-Za-z0-9][A-Za-z0-9._-]*$`. An invalid task id exits 2 before constructing output paths. A class absent from `classes.yaml` exits 2 and names the supplied slug in its diagnostic. These refusals leave the replan and decision ledger unchanged.

   The helper reads `.orchestration/tasks/<task>.md` for `allowed_files` and creates `.orchestration/tasks/<task>-replan.md`. Creation refuses an existing filesystem entry at that destination with exit 4 and preserves its contents. The script never edits the source task text and never dispatches.

   The replan contains the cause class, the remedy sentence, every blast-radius glob, and the task's allowed-files entries that cover each glob. Uncovered globs are explicitly marked outside `allowed_files`. Coverage concerns the entire prospective scope denoted by a glob, including paths that do not exist yet. Matching a pattern string as though it were a filename or expanding only currently existing files does not establish coverage.

   The replan includes a new Completion sentence skeleton with placeholders for the observable result, verification selectors and evidence. It includes this four-field line:

   ```text
   re-plan: specification — <fill>; design — <fill>; implementation — <fill>; verification — <fill>
   ```

   The four fields follow the structure of the S1 re-plan in `.orchestration/acceptance/dotfiles-T133-permission-guard-gate-a04.md` and its `replans` JSON object. The skeleton remains a proposal until the orchestrator supplies concrete content. The script leaves the acceptance record unchanged.

   Every blast-radius glob covered by `allowed_files` produces exit 0. The orchestrator fills the skeleton and re-dispatches through the applicable hold procedure. A known class with `remedy: unknown` is reported explicitly with its empty blast radius; it follows the same coverage rule and acquires no invented corrective procedure. Exit 0 establishes scope coverage only.

   Any uncovered glob produces the replan, appends exactly one six-column TSV row to `.orchestration/decisions.tsv`, and exits 3. The row has `id` equal to `D-<task>-replan`, `when` equal to the current UTC timestamp, `what` naming the uncovered globs, `why` naming the class, `basis` equal to `hold-playbook`, and `result` equal to `pending`. It contains no default or deadline that consumes a default.

   `tests/unit/test_hold_playbook.py::HoldPlaybookTests::test_three_classes_expand_into_replans`, `test_uncovered_scope_appends_pending_decision`, `test_unknown_class_exits_2`, `test_existing_replan_exits_4`, `test_invalid_task_id_is_refused`, `test_scope_comparison_covers_the_whole_glob` and `test_record_text_is_never_executed` verify these statements.

3. `tests/unit/test_hold_playbook.py` uses `unittest` and temporary repository layouts containing a copied script, fixture `classes.yaml`, source task text and decision ledger. Its three-class expansion fixture uses `colored-json-parse`, `concurrent-ff-clobber` and `records-form`. Each class produces its own replan skeleton with the expected remedy, scope classification, Completion placeholder and four re-plan fields.

   The scope decision test verifies exit 3, the exact decision id and six fields, preservation of existing ledger rows and absence of a default. Refusal tests verify their exit codes and unchanged records. The overwrite test also repeats an out-of-scope invocation and verifies that exit 4 appends no second decision row. The literal-data test uses command-looking record text and verifies that it remains text without executing.

   The known-class unknown-remedy test verifies the reported `unknown`, empty blast radius and coverage exit status. The whole-glob test includes an exact permitted scope, a scope covered by an allowed directory glob and a broader scope that extends outside the allowed files. The vocabulary test reads the real tree without invoking the script there.

   The behavioral tests are written before implementation and have red results followed by green results. The vocabulary test has a red result before the tracked mapping is added and a green result with the completed mapping.

4. `.orchestration/dotfiles-T133-hold-playbook-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md` and worker review evidence. The report maps the Files requirements to their test selectors and records the class-source attribution. Worker review filenames carry the required `-worker-` infix.

## Out of scope

`dispatch.sh` changes, including refusal of TASK or revise sends during hold, are deferred until P1-6 merges. That follow-on work includes the hold-send-refusal fixture named by the plan. This task has no dependency on that merge.

`verdict.sh`, `scripts/regime-counters.sh`, hold detection, counter output and P0 enforcement remain outside this implementation. The existing S1 and S2 lines supply context for the orchestrator; this helper neither parses review titles into classes nor releases a hold.

Editing any mistake record, correction record, correction inventory or acceptance record is outside this task. Tests exercise replan creation and decision appends in temporary directories. Live recovery records are written only when the orchestrator later invokes the completed helper.

## Check

`make format`, `shellcheck scripts/orchestrator/hold-playbook.sh`, `shfmt -d scripts/orchestrator/hold-playbook.sh` and `uv run --no-project --with pyyaml python -m unittest tests.unit.test_hold_playbook -v` have their commands, verbatim output, exit statuses and tested heads pasted in `.orchestration/dotfiles-T133-hold-playbook-a01/validation.md`. The script passes shellcheck and shfmt, and the unit module is green.

The three-class expansion tests and the decision, refusal, literal-data and vocabulary tests carry their red-before-implementation and green-final-head evidence. Every script execution uses a temporary fixture tree. No local Bats tests run.

An inherited formatting failure is reproduced on the unchanged base and recorded with its output. It remains a reported failure and receives no repair outside `allowed_files`.

`git diff --numstat origin/main...HEAD` shows at most 350 changed lines outside `tests/` and `.orchestration/`, and at most 400 changed lines under `tests/`. Changed lines are additions plus deletions, and fixtures count against the test cap. Validation includes the totals and changed-file inventory.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The task copy remains byte-identical to the dispatched file.

## Completion

The Completion clause of `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a01.md` applies with `dotfiles-T133-hold-playbook-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-hold-playbook-a01/task.md>` in the RESULT. This task's scope, Check, `security: false`, fresh-branch rule and prohibition on `@codex review` comments govern that reference.

One PR starts from a fresh branch off `origin/main`. The orchestrator writes the advisory owner task before recording its first ownership disposition. A small in-scope P2 follows the inherited `check=` revise procedure while INV-6 permits it.

The worker's own pre-push review is one round at most. Every worker-side fix round counts toward INV-6. A surviving P0/P1 is sent in the RESULT as `open:<finding-or-thread-id>` and stops integration for the operator's decision. The third finding of one class stops further rounds until the orchestrator's re-plan.

The RESULT identifies the final head, base, branch, changed files, test selectors, caps, evidence paths, task-copy hash and every Bot finding's disposition. It carries the precheck evidence required by the applicable RESULT procedure.

The orchestrator runs the task-level audit on the final head and dispositions every finding before the gate. Final-head CI, the feedback sweep, audit, acceptance record, gate and merge follow Orchestrator Playbook step 10 in its prescribed order. A changed head receives fresh evidence.

No `@codex review` comment is issued. Every `gh` write and Git write runs as an individual command without shell chaining or a wrapper combining writes. A classifier denial produces a blocked PONG naming the command and refusal.

## Orchestrator note (2026-10-19T03:2xZ): classes.yaml is a record, not a worker file

`.orchestration/learning/classes.yaml` is written by the orchestrator (checker C2 keeps every `.orchestration/` path except the task directory out of a worker's allowed_files); the orchestrator seeds it from the `classes:` lines of the mistake records before this task is dispatched and keeps it current. The worker therefore does not edit it: item 1 is read as the file format the script consumes, the pinned-vocabulary check is implemented as `hold-playbook.sh --check-vocabulary <classes.yaml> <mistakes dir>` (exit 2 listing every class slug of the records that the file lacks, exit 0 otherwise) and tested with fixtures only; the orchestrator runs it against the real tree at acceptance and pastes the output. No test reads the real `.orchestration/learning/` tree.

## Checks (pasted by the orchestrator before each send)

```
2026-10-19T03:2xZ dispatch 1
task=dotfiles-T133-hold-playbook-a01 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 source=live
C-78: no in-flight task names scripts/orchestrator/hold-playbook.sh or tests/unit/test_hold_playbook.py (P1-5 a04, #412 a05, worker-write-boundary-a01 checked)
task-consistency-check: OK after the classes.yaml entry moved to the orchestrator (C2)
```

Implementation and runtime verification remain pending worker execution.
Unknown remedies and pending scope decisions require orchestrator resolution before recovery.