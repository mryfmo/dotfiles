---
format: 2
task_id: dotfiles-T133-task-generator-plan-check-a02
kind: code
security: true
allowed_files:
  - scripts/orchestrator/task-from-plan.py
  - scripts/orchestrator/plan-check.py
  - scripts/orchestrator/task-consistency-check.py
  - scripts/orchestrator/task-template.md
  - tests/unit/test_task_from_plan.py
  - tests/unit/test_plan_check.py
  - tests/unit/test_task_consistency_c11_c15.py
  - tests/unit/test_task_checkers.py
  - .orchestration/dotfiles-T133-task-generator-plan-check-a02/**
after: []
reset_of: [dotfiles-T133-task-generator-plan-check-a01]
threat_table:
  - control: "scripts/orchestrator/task-from-plan.py (generation from the committed plan group, bundled template, command outputs and scratch-worktree checks)"
    disposition: "residual: the generator executes the orchestrator's committed plan commands in the orchestrator's sandbox after the clean-plan check; the generator regressions and final-head security review assess this execution boundary."
  - control: "scripts/orchestrator/plan-check.py (form, concrete scope intersections, timestamped drift and forbidden patterns)"
    disposition: "closed: tests/unit/test_plan_check.py::test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan"
  - control: "scripts/orchestrator/task-consistency-check.py (C11 to C15, concrete glob matches, trusted premise execution and assigned invariant ids); item 20: C10 literals as git grep -e operands and C6 paths confined to the checkout)"
    disposition: "residual: the checker executes premise commands only for bytes matching the caller's trusted SHA256; the dedicated regressions cover that gate, warnings, wildcard coverage and invariant completeness."
  - control: "scripts/orchestrator/task-template.md (the bundled task rows, Check defaults and Completion wording)"
    disposition: "closed: tests/unit/test_task_from_plan.py::test_generator_uses_the_bundled_template_without_task_records"
  - control: "tests/unit/test_task_from_plan.py (temporary committed plan groups, real local Git repositories and isolated command fixtures)"
    disposition: "residual: fixtures execute controlled commands in temporary repositories and verify output provenance, refusal before execution, generated scope and scratch-worktree cleanup."
  - control: "tests/unit/test_plan_check.py (temporary plan groups, concrete tree paths, acceptance events and a stub gh)"
    disposition: "residual: fixtures use temporary repositories and a stub gh placed first inside the uv invocation; no fixture contacts live GitHub."
  - control: "tests/unit/test_task_consistency_c11_c15.py (shape, wildcard, SHA, warning and invariant regressions)"
    disposition: "residual: temporary task files and repositories isolate premise side effects; explicit trusted hashes authorize only the fixture bytes under test."
  - control: "tests/unit/test_task_checkers.py (amendment 1's C4 fixture disposition and historical expected-set edits)"
    disposition: "residual: only the two amendment-1 edits remain against origin/main; report.md justifies every added historical check id and the audit compares the module's complete diff."
  - control: ".orchestration/dotfiles-T133-task-generator-plan-check-a02/** (the reset task's branch artifacts)"
    disposition: "residual: artifacts stay in this task's directory, distinguish historical observations from final-head results and identify commands, tested revisions and evidence hashes."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md)"
    disposition: "residual: the worker's first push deletes the named predecessor copy and adds the byte-identical dispatched a02 text; the a02 copy's own SHA256 appears in TASK and RESULT and is compared at acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-task-generator-plan-check-a02/ (report.md, validation.md, sandbox.md, learning.md, measure.md and authorized revise evidence)"
    disposition: "residual: records preserve command outputs, exits, production revisions and regression-source hashes; the final-head audit checks claims against the implementation, records and CI."
  - control: task metadata
    disposition: "residual: PyYAML reads the front matter and the consistency checker validates its cross-field rules before dispatch and at acceptance; the dispatched-file comparison covers subsequent changes."
  - control: metadata separators
    disposition: "residual: the first document separators bound the YAML front matter and the byte comparison covers the complete dispatched task copy."
  - control: in-process effects
    disposition: "residual: task-from-plan.py executes the plan's backticked commands, which are the orchestrator's own text, in the orchestrator's sandbox; it refuses execution when git status of the 024-* plan group is not clean and executes commands read from the committed revision. It writes the named task file and creates and removes a scratch worktree for Check commands. C14 executes a premise command only when --premises-sha equals the SHA256 of the same file bytes from which that command was parsed. plan-check writes no files."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow changes; scripts use the existing uv and PyYAML invocation with python -I, premise reruns use bash with pipefail and the specified PATH, and plan-check uses read-only gh and git calls."
  - control: new or renamed scripts
    disposition: "residual: the inherited two new Python scripts and one new bundled Markdown template are the complete new production-file inventory; the audit checks the final inventory against allowed_files."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges through gh pr merge --squash --match-head-commit <audited head> after Orchestrator Playbook step 10; the worker has no merge assignment."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch changes the head, so the required CI, feedback sweep, audit and security-review evidence bind the resulting final head before the gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state in the acceptance record."
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

# AGMSG-TASK dotfiles-T133-task-generator-plan-check-a02 — INV-6 reset of dotfiles-T133-task-generator-plan-check-a01 (plan 006 S2; plan 024 P1-12)

This text is the independent redesign by a review-profile context other than the author of a01. Amendment 1 and the C14 specification change sent as a revise constitute two amendments. Plan 006 INV-6 S2 stopped a01. The task-level audit of `9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab` returned `incorrect` with three P1 and twelve P2. Files items 5 to 19 disposition those fifteen findings through fixes, regression checks and corrected ownership.

PR #417 continues on the same branch, `tools/task-generator-plan-check-a01`, from `9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab`. The worker's first push deletes `.orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md` and adds this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md`. The orchestrator directs that exact predecessor-copy deletion as reset bookkeeping outside `allowed_files`. Every other worker edit stays within `allowed_files`. One branch and one implementation PR carry this reset.

The a01 task, acceptance history, reports and counters remain historical evidence. Its C14 revise remains recorded as an amendment in substance. The five premises above preserve a01's write-time observations verbatim. Fresh validation records the repository and revision actually checked and identifies any premise that has since drifted.

## Goal

The generator produces a format-2 task skeleton from one plan todo row using a bundled template, proposed file scope and actual command outputs. The consistency checker validates disposition shapes, concrete wildcard coverage, trusted premise reruns and complete invariant assignments. The plan checker reports form, drift and forbidden-pattern violations without changing the plan.

## Files

1. `scripts/orchestrator/task-from-plan.py <todo-id> [--out .orchestration/tasks/<id>.md] [--seat <identity>] [--worktree <path>]` retains the existing Python, standard-library and PyYAML implementation. It reads the exact todo row from `.orchestration/plans/024-todo.md`, the numbered program items that row names in `024-design-programs.md`, the quality row in `024-design-quality.md` and the matching section-6 wave row in `024-omp-cutover-and-corrective-order.md`.

   `scripts/orchestrator/task-template.md` supplies the task-copy, evidence, non-path and orchestrator-effect rows, default Check commands and complete Completion wording. The template is located beside the generator. The generator reads no file under `.orchestration/tasks/`. The former sibling-task Check lookup, row-template lookup and Completion-record dependency are replaced by bundled content. Program-specific Check commands come from the committed program items, and bundled defaults supply the common checks.

   The generated front matter carries `format: 2`, the output filename's task id, `kind: code`, the quality row's security classification, `after: []`, premises and threat rows. Proposed `allowed_files` preserve paths and wildcard scopes named by the row and its program items, add relevant `git grep -l -F` hits and include the task's evidence directory. Files contains each proposal's `# from: <grep hit>` provenance. The threat table contains one draft row per allowed entry, concrete rows required by C12 and the bundled control rows with the generated task id substituted.

   The generator executes the orchestrator's backticked plan commands in the orchestrator's sandbox after item 6's clean-plan gate. Each premise records its actual stdout and exit status; a failed command remains a `verify:` claim with that status. Network commands retained without execution carry an explicit `verify:` not-run explanation. They carry no invented exit status. Check commands run once in a detached scratch worktree of `origin/main`; their output and exit status appear in the generated Check section with their tested revision. Cleanup uses `git worktree remove --force` and removes the temporary parent directory.

   The body contains Goal, Files, Out of scope, Check, Completion and the dispatch Checks block. The generator writes the named output and passes it to the consistency checker with the SHA256 of its own generated bytes. It prints the checker's findings and warnings and exits 0 when its applicable checks pass, 1 otherwise. A generated file with findings remains available for editing. The bundled Completion wording retains the inherited contract with `<id>-followup-a01` as advisory owner and the generated task's own copy hash in RESULT.

2. `scripts/orchestrator/task-consistency-check.py` retains C1 to C10 and C7b unchanged and documents C11 to C15 after C10. C11 requires a `closed:` payload shaped as `tests/<path>::<identifier>`, an `out-of-scope:` payload naming an existing `.orchestration/tasks/<id>.md`, and a `residual:` payload of at least 20 characters. C12 examines concrete glob matches and requires a row for each executed or applied file, with the existing exemptions for `tests/fixtures/` and the task's own evidence directory. C13 requires exactly one of `closed: `, `residual: ` or `out-of-scope: `.

   C14 executes premise commands only when `--premises-sha <sha256>` equals the SHA256 of the file bytes being checked. The hash and parsed commands come from the same read. The caller supplies the trusted dispatched hash. Acceptance of a branch copy supplies no trusted hash. A missing or mismatching hash executes no premise command and prints `C14: not run (no trusted sha)` as an explicit warning. A no-sha structural pass does not establish that premises passed.

   An authorized C14 rerun uses the repository root, `bash -c`, `set -o pipefail`, PATH `<root>/bin:/usr/bin:/bin` and the retained HOME value. Output comparison collapses whitespace runs as amendment 1 specified. Commands naming `gh`, `curl` or a URL produce `C14 skipped network premise`. A tool absent from the mandated PATH produces `C14: tool absent <name>`, including absence within a pipeline. These cases remain visible warnings or skip notes. An actual output mismatch remains a C14 finding.

   C15 reads the named design from `origin/main`. It compares the task's invariant id set with the design's assignment to that task in `implementing_tasks` and compares each assigned sentence byte for byte. An omitted or empty task invariant map cannot bypass an existing assignment. Missing assigned ids, extra ids and changed sentences produce C15 findings. A missing named design produces a finding. A design task carrying its own definitions retains its existing treatment. Findings keep the existing indented stdout format, and warnings and skip notes remain visible on stderr.

3. `scripts/orchestrator/plan-check.py [--root <repo>] [--drift] [--invariants]` retains the eleven-file plan-024 scope and one violation per line. F1 requires every todo row's completion column. F2 compares simultaneous tasks' concrete allowed scopes once their task files exist. F3 requires each P1 row to name a bottleneck id present in mechanism 5.0 or quality 5.10. F4 requires each checklist DoD row to contain a backtick command or explicit file path. F5 requires each section-2 decision row's bold default. F6 checks task and decision references locally and PR existence through read-only `gh` when `--drift` is requested.

   Drift checks compare every nearby cited PR head and state with `gh pr view <pr> --json headRefOid,mergeStateStatus,isDraft,state`. Progress rows naming a task are compared with that task's latest timestamped acceptance event. Differences retain `drift: <file>:<line> <cited> != <live>`. Invariant checks cover nonempty `ANTHROPIC_OAUTH_TOKEN` assignments, direct main pushes, prohibited merge flags and added `claude.permissions.ask` entries against `origin/main`. The script writes no records, exits 1 on a violation and exits 0 otherwise. CI wiring remains P1-11's work.

4. The three dedicated modules retain the original end-to-end and per-rule tests. `tests/unit/test_task_from_plan.py::test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs` exercises real successful and failed commands, provenance, threat rows, bundled content and scratch cleanup. `tests/unit/test_plan_check.py::test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan` retains one isolated violation per form rule, clean-plan success, stubbed drift and invariant cases. `tests/unit/test_task_consistency_c11_c15.py::test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged` retains the check-specific fixtures, whitespace normalization, absent-tool warnings and historical structural checks.

   Amendment 1's two edits in `tests/unit/test_task_checkers.py` remain. The C4 path-boundary fixture carries a well-formed disposition. The historical exact expected sets include the justified C11 and C15 findings. No historical fixture executes premises without a trusted hash, and no C14 finding id is added for a no-sha warning. No other part of that module changes. `report.md` explains each expected-set addition. Fixture lines count against the test cap.

5. Audit finding 1, P1, is fixed by bundling `scripts/orchestrator/task-template.md` and removing every generator input dependency on `.orchestration/tasks/`. A missing records file no longer prevents generation. The prior `fixed:b3c6b7ea` disposition addressed error presentation and did not fix this cause.

   `tests/unit/test_task_from_plan.py::test_generator_uses_the_bundled_template_without_task_records` uses a committed fixture plan group with no task-record directory and the production bundled template. Generation succeeds, produces the required rows and Check and Completion content, and passes the real checker. The test is red against the generator at `9da0ed3` because that generator requires task records and is green after the dependency removal. The orchestrator supersedes the erroneous missing-template disposition with the actual fix commit and this evidence.

6. Audit finding 2, P1, is fixed by stating and enforcing the generator's execution contract. Its backticked commands are the orchestrator's own plan text and execute in the orchestrator's sandbox through the existing runner. Before executing any premise or Check command, the generator checks git status for the entire `.orchestration/plans/024-*` group, including staged, unstaged and untracked changes. A dirty group produces an explicit refusal before command execution or output creation. The generator records the resolved committed revision and reads executable command text from that revision, so the executed text equals committed plan text. The in-process-effects row above describes these effects.

   `tests/unit/test_task_from_plan.py::test_generator_refuses_dirty_plan_commands_before_execution` commits a plan command that writes a temporary marker and exercises unstaged, staged and untracked plan-group changes. Each dirty case refuses generation and leaves the marker absent. The committed clean case runs and records the command's output and revision. The test is red against `9da0ed3` and green after the gate is added.

7. Audit finding 3, P1, is fixed by making item 2's C14 SHA gate part of this dispatched specification and correcting its amendment accounting. The a01 acceptance record names the C14 revise as the second amendment in substance, records S2 and retains the original history. This reset does not relabel that change as an implementation-only round.

   `tests/unit/test_task_consistency_c11_c15.py::test_c14_executes_premise_commands_only_for_the_dispatched_sha` retains the marker proof: no hash and a wrong hash execute nothing; the correct dispatched hash executes the premise; changing the file invalidates the old hash; an authorized rerun with mismatching output reports C14. Its red production reference is the pre-gate implementation at `ff4d25a8`, and it runs green on this task's final head. Validation also contains a read-only comparison of the original acceptance decision with its explicit amendment and S2 correction. The orchestrator supplies that record evidence outside the worker's edit boundary.

8. Audit finding 4, P2, is fixed at the checker interface by making the no-trusted-SHA outcome an explicit warning carrying `C14: not run (no trusted sha)`. The dispatch check's evidence preserves that warning and records C14 as not run. A successful structural exit does not become an unqualified C14 success.

   The checker invocation presently at `scripts/orchestrator/dispatch.sh:238` is the integration point for `--premises-sha <the TASK line's validated task_sha256>` before `"${tf}"`. That line belongs to P1-6 in the serialized dispatch lineage following `dotfiles-T133-result-precheck-a03`. Its owner also preserves warning output from successful checker calls. This task names the line and its required argument in `report.md` and does not edit `dispatch.sh`. Until that wiring lands, the report and dispatch evidence state the warning and the pending integration.

   `tests/unit/test_task_consistency_c11_c15.py::test_c14_without_a_trusted_sha_reports_an_explicit_warning` checks the ordinary no-sha invocation, explicit warning severity, the exact not-run message and absence of the premise marker. It is red against `9da0ed3`'s unqualified note and green after the warning contract is implemented. The test does not claim that unchanged dispatch wiring passes a trusted hash.

9. Audit finding 5, P2, is fixed by comparing assigned invariant ids as well as sentences. C15 obtains the assignment from the design on `origin/main`, including when the task omits `invariants`.

   `tests/unit/test_task_consistency_c11_c15.py::test_c15_requires_the_design_assigned_invariant_id_set` assigns INV-1 and INV-2, supplies only the correct INV-1 sentence and expects C15. It also covers an absent map, an extra id, a changed sentence and the complete byte-identical assignment. The missing-id case is red against `9da0ed3` and all cases are green after the fix.

10. Audit finding 6, P2, is fixed by expanding each glob before deciding which matched files require concrete threat rows. A matched `.sh`, `.py`, `.yaml`, `.yml`, `.json` or `.toml` file, or a file under `home/`, `scripts/`, `.githooks/` or `.github/`, receives the executed-or-applied treatment regardless of the glob's spelling. The fixture and own-evidence exemptions remain.

    `tests/unit/test_task_consistency_c11_c15.py::test_c12_classifies_concrete_glob_matches_before_the_glob_spelling` places a tracked shell script under `install/`, permits `install/**` and omits its concrete row. That case reports C12; adding the concrete row clears it. The test also retains the exempt-directory cases. It is red against `9da0ed3` and green after the fix.

11. Audit finding 7, P2, is fixed by expanding wildcard scopes to their concrete tree matches before F2 compares simultaneous tasks. Literal paths remain represented, and overlap diagnostics identify a shared concrete path. Comparing glob spellings against each other does not establish disjointness.

    `tests/unit/test_plan_check.py::test_f2_detects_intersecting_globs_through_concrete_tree_matches` gives two simultaneous tasks `scripts/test_*.py` and `scripts/*_check.py` and creates `scripts/test_check.py`. It expects one F2 overlap. Disjoint concrete matches pass, and the existing glob-versus-literal case remains covered. The intersecting-glob case is red against `9da0ed3` and green after the fix.

12. Audit finding 8, P2, is fixed by selecting wave rows through whole todo-id tokens in the selected seat column. `P1-1` does not match `P1-10`, `P1-11` or `P1-12`.

    `tests/unit/test_task_from_plan.py::test_wave_selection_matches_whole_todo_ids` places the longer ids in an earlier wave and `P1-1` in its own wave, with distinguishable Check commands. It asserts the correct wave, seat and Check provenance. It is red against `9da0ed3` and green after the fix.

13. Audit finding 9, P2, is fixed by preserving explicit wildcard scopes in generated `allowed_files` and threat rows. Path extraction accepts `scripts/*.py` and `home/dot_config/**` as scopes and retains their proposal provenance. Required concrete C12 rows accompany applicable matches.

    `tests/unit/test_task_from_plan.py::test_generator_preserves_wildcard_scopes_and_their_threat_rows` names both scopes in a committed fixture program item, creates concrete matches and asserts that the generated front matter preserves both scopes and their required rows. The generated fixture passes the real checker. It is red against `9da0ed3` and green after the fix.

14. Audit finding 10, P2, is fixed by reading a numbered program item through the next numbered program heading or end of file. Blank lines, fenced schemas and subsequent paragraphs remain inside the current item.

    `tests/unit/test_task_from_plan.py::test_program_item_continues_until_the_next_numbered_heading` places a required path and command after a blank line and fenced block, followed by another numbered item. The generated Files and premises include the entire selected item and exclude the next item. It is red against `9da0ed3` and green after the fix.

15. Audit finding 11, P2, is fixed by retaining command spans without requiring that their executable currently exists. Single-word commands and commands containing redirects remain executable command candidates. Path and wildcard spans retain their separate scope role. Actual execution supplies stdout and exit status; an unavailable executable or shell syntax failure remains a `verify:` record with the observed status. Check-command extraction follows the same recognition rule.

    `tests/unit/test_task_from_plan.py::test_generator_retains_unavailable_single_word_and_redirecting_commands` includes an unavailable executable, a single-word `pwd` and a command redirecting output to a temporary fixture file. It asserts the retained command strings, actual statuses, stdout and `verify:` treatment, and exercises the same forms in Check extraction. It is red against `9da0ed3` and green after the fix.

16. Audit finding 12, P2, is fixed by selecting acceptance events through their timestamps and task identity. The last textual match is not the latest event. An event for another task does not determine this task's progress state.

    `tests/unit/test_plan_check.py::test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task` supplies a newer acceptance before an older revision in textual order and includes a still newer event for another task. The matching accepted progress row passes; changing it to revise produces one drift finding. It is red against `9da0ed3` and green after the fix.

17. Audit finding 13, P2, is fixed by collecting every nearby SHA and state associated with each PR occurrence. Association stays within that occurrence's line and context and stops before the next PR occurrence. Each assertion is compared independently. A matching head does not suppress a conflicting live state.

    `tests/unit/test_plan_check.py::test_drift_checks_every_sha_and_state_for_each_pr_occurrence` includes `#77 abc1234 merged` with a matching live head and live state OPEN and expects the merged-versus-OPEN finding. It also covers multiple nearby SHAs and repeated PR occurrences with distinct assertions. It is red against `9da0ed3` and green after the fix.

18. Audit finding 14, P2, is fixed by recognizing nonempty quoted values immediately after `ANTHROPIC_OAUTH_TOKEN=`. Single-quoted, double-quoted and unquoted nonempty assignments produce invariant findings.

    `tests/unit/test_plan_check.py::test_invariants_reject_nonempty_quoted_oauth_token_assignments` constructs harmless fixture values at runtime and checks both quote forms and the existing unquoted case. Empty assignments remain distinct from nonempty values, and diagnostics contain no assigned value. The quoted cases are red against `9da0ed3` and green after the fix.

19. Audit finding 15, P2, is fixed by assigning the C12 remedy to this task through item 10. The advisory owner does not need a future amendment to acquire the checker or its test module for this finding. The other inherited findings fixed above are also superseded by this reset's ownership.

    The orchestrator records the corrected ownership in the lineage's acceptance records and withdraws the corresponding remedy from `dotfiles-T133-task-generator-plan-check-followup-a01`. The worker reports the finding, item 10's selector and its actual fix commit. `tests/unit/test_task_consistency_c11_c15.py::test_c12_classifies_concrete_glob_matches_before_the_glob_spelling` supplies the red-then-green implementation proof. A read-only record assertion contrasts the old assignment requiring an amendment with the corrected assignment to a02 and its fix evidence. The worker does not edit the canonical owner task or acceptance records.

20. The checker's own hardening, found by the regime job's review of PR #418 (a008, 21:37:56Z) and assigned here: C10 passes every backticked literal to `git grep` as a pattern operand after `-e` (or as a positional after `--`), never as a bare argument that `git grep` can parse as an option, so a literal such as `--open-files-in-pager=CMD` searches for that text and runs nothing; every path the checker opens or passes to a subprocess (C6's design path included) is resolved and confined to the checkout root given by `--root`, and a path outside it is a finding, not a read. `tests/unit/test_task_consistency_c11_c15.py::test_c10_never_passes_a_literal_as_a_git_grep_option` (a fixture task whose backticked literal is `--open-files-in-pager=<marker command>`: the marker is never written and C10 reports the literal as unmatched) and `::test_c6_confines_design_paths_to_the_checkout` are written first and red against 9da0ed3.

## Out of scope

`reset-task.sh` remains the later C-69 item. `scripts/orchestrator/dispatch.sh`, including `--next`, the trusted-SHA argument and warning forwarding, remains in the P1-5 to P1-6 dispatch lineage identified in item 8. The regime CI job and validate wiring remain P1-11. `ruleset-request.sh`, `ruleset-verify.sh` and permission-policy changes remain P1-14.

Plan files, progress records, canonical predecessor tasks, acceptance records and advisory-owner task files remain outside the worker's edit boundary. The orchestrator performs the reset, disposition and ownership bookkeeping named above. Plan-check reports violations without repairing those records.

## Check

`.orchestration/dotfiles-T133-task-generator-plan-check-a02/validation.md` contains commands, verbatim stdout and stderr, exit statuses and tested revisions for `make unit-test`, `make format` and `uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers -v`. The four task modules are green. An inherited full-suite or formatting failure is reproduced against the unchanged base in the same sandbox and recorded as a failure with that comparison. It is not labelled green or repaired outside `allowed_files`. Final-head GitHub Actions checks pass before RESULT.

The checker run is `uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T133-*.md`. Its complete output and exit status are pasted in validation. C1 to C15 and C7b are accounted for separately from warnings. Without `--premises-sha`, C14 is recorded as not run with its warning. Authorized premise reruns use the orchestrator's trusted dispatched hash and paste their results. Acceptance does not authorize branch commands by calculating a replacement trusted hash from a branch copy. Stale historical premises are reported with their tested root and revision.

The plan checker runs once as `uv run --no-project --with pyyaml python -I scripts/orchestrator/plan-check.py`. Its output and exit status are pasted in validation. Violations in the real plan group are reported and left for the orchestrator. The dedicated fixture tests exercise `--drift` and `--invariants` without live GitHub.

Each audit item has the named regression or record check and red-then-green evidence. New regressions execute their current test source against production code at `9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab` before the corresponding fix, then pass on the final implementation. The retained C14 gate uses the pre-gate revision named in item 7 for its red proof. Record checks identify the exact before and after record text. Each proof records the production revision, regression-source hash, command, output and exit status. A missing test, import error, unavailable runner or zero-test run does not establish a red regression.

`git diff --numstat origin/main...HEAD` shows at most 700 changed lines outside `tests/` and `.orchestration/`, and at most 800 changed lines under `tests/`. Changed lines are additions plus deletions, including fixtures and the bundled template. `measure.md` and RESULT record both totals and the final changed-file inventory. The totals cover the whole PR, including inherited a01 changes.

The orchestrator checks the canonical a02 text before dispatch and checks the task-copy replacement and byte identity at acceptance. Local Bats tests do not run. GitHub Actions supplies any required Bats result.

## Completion

One branch, `tools/task-generator-plan-check-a01`, continues PR #417 from `9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab`. The worker's first push contains the predecessor task-copy deletion and this text's byte-identical a02 copy. No second implementation branch or PR is created.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's scope, caps, reset branch and explicit review restrictions. `dotfiles-T133-task-generator-plan-check-followup-a01` owns new advisory P2 findings after the inherited findings assigned above are removed from its ownership. The orchestrator writes any required owner update before recording that disposition.

RESULT carries `task_copy=<sha256 of .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md>`. It carries `precheck=<the precheck evidence hash>` when PR #411 has merged and the applicable precheck has run; otherwise it carries `precheck=pending-411`. It also names the final head, base, branch, changed files, named tests, caps, feedback dispositions and evidence paths. The report explicitly identifies the dispatch SHA wiring and warning-forwarding work owned outside this task.

The worker's own pre-push review has at most one correction round. A P0 or P1 surviving that round appears in RESULT as open and goes to the orchestrator for the operator's decision. An inherited Bot P0/P1 receives its actual root-cause disposition or remains open. A surviving thread is reported as `open:<thread id>`, and a review-body finding as `open:review-<review id>`. No further worker correction round is hidden before RESULT. Every worker-side round counts toward INV-6, and the a01 stopped history and amendment accounting remain recorded.

A Codex seat writes evidence at the same relative paths in its own worktree and states that location in RESULT. Worker review evidence uses the required `-worker-` infix. The orchestrator copies worktree evidence by absolute path before review. Evidence distinguishes inherited observations, new red proofs and final-head green results.

This task is `security: true`. The orchestrator runs the task-level audit and a separate security-profile review on the final head. Final-head CI, the complete feedback sweep, finding dispositions, acceptance record and gate follow Orchestrator Playbook step 10 in its prescribed order. Changed heads receive the required fresh evidence. The orchestrator runs `make require-crit-review` with the required review evidence before completion and uses the integration evidence required by step 10 before merging.

No `@codex review` comment is posted. Automatic reviews are observed for the inherited bounded window, and absence after 15 minutes is recorded as `bot: none`. Every `gh` command and every Git write runs as an individual command without shell chaining or a wrapper combining writes. A classifier or permission denial produces a blocked PONG with the exact command and output. An alternate command or API does not bypass the denial.

Until P1-14 lands, any string containing the words `gh pr merge` or `gh pr create` is written with the file-edit tool, never in a Bash heredoc or `echo`.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-task-generator-plan-check-a02.md: OK
premises 1 to 5: copied from a01 verbatim (write-time outputs of 2026-10-18 18:0x JST; premise 5 is stale since PR #413 merged at 10:46Z, a C14 finding at acceptance)
masked 0 match(es) in .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md
```

Local Bats runs and live deployment remain outside this task.
Plan commands execute with the orchestrator sandbox's permissions.