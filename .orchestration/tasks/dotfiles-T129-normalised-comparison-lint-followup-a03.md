---
format: 2
task_id: dotfiles-T129-normalised-comparison-lint-followup-a03
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/lint-comparisons.py
  - scripts/lint-comparisons-baseline.tsv
  - tests/unit/test_lint_comparisons.py
  - .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/**
after: []
reset_of: [dotfiles-T129-normalised-comparison-lint-followup-a01]
threat_table:
  - control: scripts/lint-comparisons.py
    disposition: "residual: the changed-file set controls failure severity while the existing scan supplies hits and stale rows; the four drift fixtures and the changed-files checkout test verify the invariant, and the final-head audit checks preservation of the inherited rules."
  - control: scripts/lint-comparisons-baseline.tsv
    disposition: "residual: the exact-row baseline and its inherited rows remain unchanged; fixture tests verify content-hash matching, duplicate consumption and changed-file stale-row refusal, and the audit checks that no regime-ci.py row is added."
  - control: tests/unit/test_lint_comparisons.py
    disposition: "residual: fixtures run the lint as an isolated Python subprocess against temporary files; the checkout test reads the tracked tree and computes its changed set with the specified Git environment."
  - control: .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/**
    disposition: "residual: new branch artifacts stay in this task's directory and contain the dispatched copy and evidence for the final-head audit."
  - control: the reset task-file copies (.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/task.md and .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/task.md)
    disposition: "residual: the first push deletes the a01 copy and adds the byte-identical dispatched a03 copy; TASK and RESULT bind the a03 copy's own sha256, and the orchestrator checks the replacement and bytes at acceptance."
  - control: the branch evidence records under .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence)
    disposition: "residual: records contain prose and command output; sandbox.md lists refused and permission-gated commands, and the audit compares the claims with the final diff and CI."
  - control: task metadata
    disposition: "residual: the orchestrator checks C1 to C10 and C7b before dispatch and at acceptance; the task-copy byte comparison covers the complete dispatched front matter."
  - control: metadata separators
    disposition: "residual: the checker reads the bounded first YAML front-matter document; the task-copy byte comparison covers every separator."
  - control: in-process effects
    disposition: "residual: the lint remains a standard-library script run through Python -I; tests execute it as a subprocess and import none of its code into the test process."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: workflows and interpreter configuration remain unchanged; changed-set discovery follows plan 024 section 5.14 item 2 with env -i, an absolute Git executable, explicit -C, isolated Git configuration and disabled external diff and textconv."
  - control: new or renamed scripts
    disposition: "residual: no script is added or renamed; implementation changes remain in the existing lint and unit module, and the audit checks the changed-file inventory."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges only through gh pr merge --squash --match-head-commit <audited head> after the integration gate in Orchestrator Playbook step 10.5."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the feedback sweep and the task-level audit bind the new final head before the gate; unrelated baseline drift produces warnings."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and forced removal records the discarded uncommitted state in acceptance."
premises: []
---

# AGMSG-TASK dotfiles-T129-normalised-comparison-lint-followup-a03 — INV-6 reset of followup-a01 on PR #415, seat a008, worker-f, branch lint/normalised-comparisons-followup-a01 continuing from c0eb536c

This task implements the `baseline-drift` re-plan in `.orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a01.md` for plan 023 F2. The predecessor stopped under plan 006 INV-6 S2 at 2026-10-19T04:03Z after the chain updated PR #415 onto b22a5580, producing c0eb536c. The branch, inherited fixes and baseline rows continue on PR #415.

## Goal

The comparison lint guards the files a pull request changes. A hit outside the baseline fails only in a changed file. A baseline row without a matching hit fails only for a changed file. Hits outside the baseline and stale rows in unchanged files are counted and printed as warnings and contribute no failure.

The full-tree reporting mode prints every hit and every stale row and exits 0. The invariant survives update-branch when other merges add or remove comparisons in unchanged files.

## Files

1. `scripts/lint-comparisons.py` gains `--changed <path>...` and `--all`. The existing tracked-file scan supplies the hits and stale rows, and the changed-file set determines their severity.

   With `--changed`, an unbaselined hit in a changed file exits 1, and a stale baseline row for a changed file exits 1. Unbaselined hits and stale rows in unchanged files are printed as warnings with their counts. A run containing only those warnings exits 0. A matching baseline row continues to accept one matching hit, including the existing duplicate-consumption behavior.

   With `--all`, every hit, including a baseline-matched hit, and every stale baseline row is printed. This reporting mode exits 0 and is available for a main-push or scheduled reporting run.

   With neither mode flag, the script computes the changed-file set internally from `git diff --name-only origin/main...HEAD` and applies the `--changed` behavior. An empty changed-file set remains empty.

   Changed-set discovery follows `.orchestration/plans/024-design-quality.md` section 5.14 item 2. It enters `env -i`, executes an absolute Git binary with an explicit absolute `-C`, and sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`. Git receives `-c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always -c core.attributesFile=/dev/null -c core.sshCommand=false`. The diff receives `--no-ext-diff --no-textconv`; NUL-delimited output preserves filenames. Any retained PATH follows item 2's private-directory contract, and the executed Git binary is addressed by its absolute path.

   The no-flag behavior supplies the existing unit-test CI entry point. No workflow change is needed. The rule table, `--list-rules`, allow-marker behavior, statement-local limit and inherited fixes remain unchanged.

2. `scripts/lint-comparisons-baseline.tsv` retains its exact-row form: `<file><TAB><rule><TAB><sha256 of the normalized line>`. Line normalization remains stripping leading and trailing whitespace before hashing. The inherited baseline rows at c0eb536c remain unchanged.

   No baseline row is added for `scripts/orchestrator/regime-ci.py:65`. That file is unchanged by PR #415, and the P1-11 owner normalizes its comparison. Its unbaselined hit is a warning in this task's changed-file gate.

3. `tests/unit/test_lint_comparisons.py` replaces `LintComparisonsTest.test_the_tracked_tree_is_clean_against_the_baseline` with `LintComparisonsTest.test_the_changed_files_are_clean_against_the_baseline`. The test computes the changed set from `origin/main...HEAD` with the same Git environment described in item 1. Its checkout run exercises the no-flag invocation, requires exit 0 and permits warnings for unchanged files.

   The red evidence at c0eb536c identifies the existing checkout failure on the unchanged `scripts/orchestrator/regime-ci.py:65` hit. The green evidence demonstrates that the renamed checkout test passes after the invariant changes, with that hit reported as a warning and no baseline row added.

   `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning` verifies exit 0, the warning identifying the unbaselined hit and its warning count.

   `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_a_hit_in_a_changed_file_fails` verifies exit 1 and the changed-file hit diagnostic.

   `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_a_stale_row_for_a_changed_file_fails` verifies exit 1 and the changed-file stale-row diagnostic.

   `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_a_stale_row_for_an_unchanged_file_warns` verifies exit 0, the warning identifying the stale row and its warning count.

   The four fixture tests are written before implementation and carry red-then-green evidence. Their reporting-mode assertions also verify that `--all` prints the fixture hits and stale rows and exits 0, including a baseline-matched hit.

   Existing fixture calls supply explicit changed-file sets while retaining their explicit scan files. The rule, normalizer, marker, exact-row and duplicate-consumption assertions remain effective. The inherited selectors `test_a_single_quoted_jq_option_value_is_not_read_as_the_program`, `test_a_jq_normaliser_name_inside_a_string_literal_is_no_application` and `test_every_f_string_interpolation_in_a_regex_is_escaped` remain green.

4. `.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence. Worker review filenames carry the required `-worker-` infix.

   The first push deletes `.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/task.md` and adds `.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/task.md` as the C3 reset-copy replacement. Other inherited branch content remains unchanged apart from this task's implementation and evidence.

## Out of scope

Changes to `scripts/orchestrator/regime-ci.py`, workflows, other comparison rules or any implementation file outside `allowed_files` are out of scope. The predecessor task-copy deletion in item 4 is the C3 reset bookkeeping.

The 10 advisory rows of PR #415 remain owned by `dotfiles-T129-normalised-comparison-lint-followup-a02`. This reset does not repair or transfer those rows. Additional baseline refreshes for unrelated main-branch drift and changes to other inherited evidence are out of scope.

## Check

`make format`, `uv run python -m unittest tests/unit/test_lint_comparisons.py -v` and `ruff check scripts/lint-comparisons.py` exit 0. Their commands, verbatim output, exit statuses and tested heads are pasted in `.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/validation.md`.

`uv run --no-project python -I scripts/lint-comparisons.py` exits 0 with unchanged-file drift reported as warnings. `uv run --no-project python -I scripts/lint-comparisons.py --all` prints the full report and exits 0. Both outputs are pasted in the validation file. The checkout failure at c0eb536c and the four fixtures have the red and green evidence described in Files.

At c0eb536c, `git diff --numstat b22a5580...c0eb536c` measures 293 changed lines outside `tests/` and `.orchestration/`, including the baseline's 93 lines, and 271 changed lines under `tests/`.

The final `git diff --numstat origin/main...HEAD` shows at most 400 changed lines outside `tests/` and `.orchestration/` and at most 450 changed lines under `tests/`. Both caps count additions plus deletions, and the baseline counts in the first cap. These caps replace the predecessor's script-length and diff caps. The validation file contains the totals and changed-file inventory.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The task copy remains byte-identical to the dispatched text. No local Bats tests run.

## Completion

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with `dotfiles-T129-normalised-comparison-lint-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a03/task.md>` in the RESULT. This task's continuing-branch rule, scope, Check, `security: false` and prohibition on `@codex review` comments govern the corresponding inherited clauses.

PR #415 continues on `lint/normalised-comparisons-followup-a01` from c0eb536c in seat a008's worker-f worktree. Its first push contains the C3 task-copy replacement. The inherited fixes and baseline rows remain present.

The worker's own pre-push review is one round at most. Every worker-side fix round counts toward INV-6. A surviving P0/P1 is sent in the RESULT as `open:<finding-or-thread-id>` and stops integration for the operator's decision. A surviving Bot P0/P1 carries the inherited `bot_rounds` accounting. The third finding of one class stops further rounds until the orchestrator's re-plan.

The required checks are green, and the automatic-review wait follows the bounded Worker Playbook procedure. No `@codex review` comment is issued. Every `gh` write and Git write runs as an individual command without shell chaining or a wrapper combining writes. A permission or sandbox refusal produces a blocked PONG naming the exact command and refusal.

The RESULT identifies the final head, base, branch, changed files, test selectors, caps, evidence paths, task-copy hash and every Bot finding's disposition. Advisory P2 dispositions name `dotfiles-T129-normalised-comparison-lint-followup-a02`, and the existing 10 advisory rows retain that owner.

The orchestrator runs the task-level audit on the final head and dispositions every finding before the gate. The final-head feedback sweep, task-level audit, acceptance record, gate and merge follow Orchestrator Playbook step 10 in its prescribed order. Every update-branch receives green CI and fresh final-head integration evidence.

## Checks (pasted by the orchestrator before each send)

```
2026-10-19T04:1xZ dispatch 1 (the INV-6 S2 reset of followup-a01 on PR #415)
task=dotfiles-T129-normalised-comparison-lint-followup-a03 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 source=live
followup-a01 at its stop: tasks=2 amendments=1 questions=0 results=2 withdrawn=0 revises=1; a second baseline repair would be revise 2 (S2)
C-78: scripts/lint-comparisons-baseline.tsv is also in dotfiles-T129-assets-omp-hcom-followup-a03 (not dispatched; it starts after PR #415 merges); no in-flight task names the three code files
task-consistency-check: OK
```

Implementation and runtime verification remain pending worker execution.
Unchanged-file drift remains a warning until a task changes that file.