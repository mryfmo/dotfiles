---
task_id: dotfiles-T133-task-generator-plan-check-a02
round: 1
code_head: 6e07d29193e9a3b56b299dd9d55538788bc48b7b
merge_base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
---

# Validation

Every block is the command's own output, run in the seat's sandbox (sandbox.md). A block names its tested revision. "Exact id" means `uv run python -m unittest <module>.<Class>.<name>`; no proof uses `-k`.

## Task copy

```
$ shasum -a 256 .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
a3ab8ea6addda207fa9a9ff5d96921e080dab7a1025117f33cbd087e6b805f98  .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
$ git show --stat --format=%H 6da92853
6da92853c6d05013020b6337eeac80eb07020952

 .../task.md                                        | 111 ----------
 .../task.md                                        | 231 +++++++++++++++++++++
 2 files changed, 231 insertions(+), 111 deletions(-)
```

## Red: the fifteen new regressions and the updated end-to-end test against 9da0ed3f (exact id)

Each run copies the code head's test modules (hashes below) into a scratch worktree of the production commit, which is removed afterwards. Every run is `Ran 1 test` with failures only and no errors.

```
production=9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab, test sources from the working tree of 6e07d291:
  453823892bb6e5cd50dd2e7371a0035bc90cbd65fbc0836c1a6b088a497ad4d4  tests/unit/test_task_from_plan.py
  c1b198a933cade44456943338b94d2dba407c331be46fc9a193180bce1462fa7  tests/unit/test_task_consistency_c11_c15.py
  ff8202456c02e2d67bf36feec40c58261559ac8054c43ef770993eff30d936c2  tests/unit/test_plan_check.py
$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs
exit=1
FAIL: test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs
AssertionError: '- `make unit-test`: exit 0 on origin/main 0324ae26c3fb' not found in "---\nformat: 2\ntask_id: dotfiles-T9-demo-a01\nkind: code\nsecurity: true\nallowed_files:\n- scripts/demo.sh\n- tests/unit/test_demo.
Ran 1 test in 0.456s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_uses_the_bundled_template_without_task_records
exit=1
FAIL: test_generator_uses_the_bundled_template_without_task_records
AssertionError: 1 != 0 : task-from-plan: missing under /private/tmp/claude-501/tmpi0fkpm5v/repo: .orchestration/tasks/dotfiles-T133-result-precheck-a01.md, .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a0
Ran 1 test in 0.431s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_refuses_dirty_plan_commands_before_execution
exit=1
FAIL: test_generator_refuses_dirty_plan_commands_before_execution (dirty='unstaged')
AssertionError: Tuples differ: (False, True, {'format': 2, 'task_id': 'do[2278 chars]'}]}) != (True, False, None)
FAIL: test_generator_refuses_dirty_plan_commands_before_execution (dirty='staged')
AssertionError: Tuples differ: (False, True, {'format': 2, 'task_id': 'do[2278 chars]'}]}) != (True, False, None)
FAIL: test_generator_refuses_dirty_plan_commands_before_execution (dirty='untracked')
AssertionError: Tuples differ: (False, True, {'format': 2, 'task_id': 'do[2278 chars]'}]}) != (True, False, None)
FAIL: test_generator_refuses_dirty_plan_commands_before_execution
AssertionError: 'plan group at 8d29699d4f933cd439a75828c760016bddf60613' not found in "---\nformat: 2\ntask_id: dotfiles-T9-demo-a01\nkind: code\nsecurity: true\nallowed_files:\n- scripts/demo.sh\n- tests/unit/test_demo.
Ran 1 test in 1.382s
FAILED (failures=4)
$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_wave_selection_matches_whole_todo_ids
exit=1
FAIL: test_wave_selection_matches_whole_todo_ids
AssertionError: 'wave P-W1' not found in "---\nformat: 2\ntask_id: dotfiles-T9-demo-a01\nkind: code\nsecurity: true\nallowed_files:\n- scripts/demo.sh\n- tests/unit/test_demo.py\n- .orchestration/dotfiles-T9-demo-a01/**\
Ran 1 test in 0.683s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_preserves_wildcard_scopes_and_their_threat_rows
exit=1
FAIL: test_generator_preserves_wildcard_scopes_and_their_threat_rows
AssertionError: False is not true : ['scripts/demo.sh', 'tests/unit/test_demo.py', '.orchestration/dotfiles-T9-demo-a01/**']
Ran 1 test in 0.679s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_program_item_continues_until_the_next_numbered_heading
exit=1
FAIL: test_program_item_continues_until_the_next_numbered_heading
AssertionError: 'scripts/late.sh' not found in ['scripts/demo.sh', 'tests/unit/test_demo.py', '.orchestration/dotfiles-T9-demo-a01/**']
Ran 1 test in 0.726s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_retains_unavailable_single_word_and_redirecting_commands
exit=1
FAIL: test_generator_retains_unavailable_single_word_and_redirecting_commands
AssertionError: False is not true : {'printf known-output': {'claim': 'the program item quotes `printf known-output`', 'command': 'printf known-output', 'output': 'known-output'}}
Ran 1 test in 1.043s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_plan_check.PlanCheckTest.test_f2_detects_intersecting_globs_through_concrete_tree_matches
exit=1
FAIL: test_f2_detects_intersecting_globs_through_concrete_tree_matches
AssertionError: Tuples differ: (0, []) != (1, ['F2 024-omp-cutover-and-corrective-or[54 chars]py'])
Ran 1 test in 0.166s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_plan_check.PlanCheckTest.test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task
exit=1
FAIL: test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task
AssertionError: Tuples differ: (1, ['drift: 024-progress.tsv:2 dotfiles-T1-one-a01 accepted != accepted`']) != (0, [])
Ran 1 test in 0.111s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_plan_check.PlanCheckTest.test_drift_checks_every_sha_and_state_for_each_pr_occurrence
exit=1
FAIL: test_drift_checks_every_sha_and_state_for_each_pr_occurrence
AssertionError: Tuples differ: (1, [[26 chars] #77 def4567 != abc123400000']) != (1, [[26 chars] #77 merged != OPEN', 'drift: 024-execution.md[28 chars]00'])
Ran 1 test in 0.122s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_plan_check.PlanCheckTest.test_invariants_reject_nonempty_quoted_oauth_token_assignments
exit=1
FAIL: test_invariants_reject_nonempty_quoted_oauth_token_assignments
AssertionError: Tuples differ: (1, [[24 chars]n.md:5 ANTHROPIC_OAUTH_TOKEN with a value']) != (1, [[24 chars]n.md:3 ANTHROPIC_OAUTH_TOKEN with a value', 'i[129 chars]ue'])
Ran 1 test in 0.084s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c14_without_a_trusted_sha_reports_an_explicit_warning
exit=1
FAIL: test_c14_without_a_trusted_sha_reports_an_explicit_warning
AssertionError: Tuples differ: (0, F[40 chars]iles-T9-base-a01.md: C14: not run (no trusted sha)\n') != (0, F[40 chars]iles-T9-base-a01.md: warning: C14: not run (no trusted sha)\n')
Ran 1 test in 0.303s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c15_requires_the_design_assigned_invariant_id_set
exit=1
FAIL: test_c15_requires_the_design_assigned_invariant_id_set (case='only INV-1')
AssertionError: Lists differ: [] != ['C15 invariant INV-2 that .orchestration/[71 chars]ing']
FAIL: test_c15_requires_the_design_assigned_invariant_id_set (case='no map')
AssertionError: Lists differ: [] != ['C15 invariant INV-1 that .orchestration/[189 chars]ing']
FAIL: test_c15_requires_the_design_assigned_invariant_id_set (case='an extra id')
AssertionError: Lists differ: ['C15[19 chars] not byte-equal to .orchestration/tasks/dotfil[31 chars]ain'] != ['C15[19 chars] not one .orchestration/tasks/dotfiles-T9-desi[38 chars]a01']
FAIL: test_c15_requires_the_design_assigned_invariant_id_set (case='a mistyped design')
AssertionError: Lists differ: [] != ['C15 design .orchestration/tasks/dotfiles[34 chars]ain']
Ran 1 test in 0.911s
FAILED (failures=4)
$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c12_classifies_concrete_glob_matches_before_the_glob_spelling
exit=1
FAIL: test_c12_classifies_concrete_glob_matches_before_the_glob_spelling
AssertionError: Tuples differ: (0, []) != (1, ['  C12 the glob install/** matches in[45 chars]es'])
Ran 1 test in 0.492s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c10_never_passes_a_literal_as_a_git_grep_option
exit=1
FAIL: test_c10_never_passes_a_literal_as_a_git_grep_option
AssertionError: True is not false : dotfiles-T9-base-a01.md: OK
Ran 1 test in 0.433s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c6_confines_design_paths_to_the_checkout
exit=1
FAIL: test_c6_confines_design_paths_to_the_checkout
AssertionError: 'C6 design path ../outside/design.md is outside the checkout' not found in "dotfiles-T9-base-a01.md: FAIL\n  C6 design_review.receipt r1 is not the design's current receipt r9-outside\n  C15 invariant INV
Ran 1 test in 0.404s
FAILED (failures=1)
removed=0
```

## Red: the retained C14 gate against ff4d25a8, the revision before it (item 7)

```
production=ff4d25a89fcf301fddd6cd218aa6c9c91fe4a6ad, test sources from the working tree of 6e07d291:
  c1b198a933cade44456943338b94d2dba407c331be46fc9a193180bce1462fa7  tests/unit/test_task_consistency_c11_c15.py
$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c14_executes_premise_commands_only_for_the_dispatched_sha
exit=1
FAIL: test_c14_executes_premise_commands_only_for_the_dispatched_sha (sha=None)
AssertionError: Tuples differ: (0, True) != (0, False)
FAIL: test_c14_executes_premise_commands_only_for_the_dispatched_sha (sha='0000000000000000000000000000000000000000000000000000000000000000')
AssertionError: Tuples differ: (2, True) != (0, False)
FAIL: test_c14_executes_premise_commands_only_for_the_dispatched_sha
AssertionError: Tuples differ: (2, 'usage: task-consistency-check.py [-h][109 chars]a\n') != (0, 'dotfiles-T9-base-a01.md: OK\n')
Ran 1 test in 0.450s
FAILED (failures=3)
removed=0
```

## Red: the correction round's cases against eb20d063, the reviewed head

The item 16 case, the mistyped-design case of C15 and the C7b case of the wildcard test fail there. The item 17 and C12 additions fill coverage gaps, so they pass there, and they are red against 9da0ed3f above.

```
production=eb20d063e0a73b17fca84df4689225b0005cf867, test sources from the working tree of 6e07d291:
  453823892bb6e5cd50dd2e7371a0035bc90cbd65fbc0836c1a6b088a497ad4d4  tests/unit/test_task_from_plan.py
  c1b198a933cade44456943338b94d2dba407c331be46fc9a193180bce1462fa7  tests/unit/test_task_consistency_c11_c15.py
  ff8202456c02e2d67bf36feec40c58261559ac8054c43ef770993eff30d936c2  tests/unit/test_plan_check.py
$ uv run python -m unittest tests.unit.test_plan_check.PlanCheckTest.test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task
exit=1
FAIL: test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task
AssertionError: Tuples differ: (1, ['drift: 024-progress.tsv:2 dotfiles-T1-one-a01 accepted != withdrawn`']) != (0, [])
Ran 1 test in 0.113s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_plan_check.PlanCheckTest.test_drift_checks_every_sha_and_state_for_each_pr_occurrence
exit=0
Ran 1 test in 0.111s
OK
$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c15_requires_the_design_assigned_invariant_id_set
exit=1
FAIL: test_c15_requires_the_design_assigned_invariant_id_set (case='a mistyped design')
AssertionError: Lists differ: [] != ['C15 design .orchestration/tasks/dotfiles[34 chars]ain']
Ran 1 test in 0.953s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c12_classifies_concrete_glob_matches_before_the_glob_spelling
exit=0
Ran 1 test in 0.752s
OK
$ uv run python -m unittest tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_preserves_wildcard_scopes_and_their_threat_rows
exit=1
FAIL: test_generator_preserves_wildcard_scopes_and_their_threat_rows
AssertionError: 1 != 0 : dotfiles-T9-demo-a01.md: FAIL
Ran 1 test in 1.103s
FAILED (failures=1)
removed=0
```

## Green: the four task modules on 6e07d291

```
$ uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers -v
test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs (tests.unit.test_task_from_plan.TaskFromPlanTest.test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs) ... ok
test_generator_preserves_wildcard_scopes_and_their_threat_rows (tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_preserves_wildcard_scopes_and_their_threat_rows) ... ok
test_generator_refuses_dirty_plan_commands_before_execution (tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_refuses_dirty_plan_commands_before_execution) ... ok
test_generator_retains_unavailable_single_word_and_redirecting_commands (tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_retains_unavailable_single_word_and_redirecting_commands) ... ok
test_generator_uses_the_bundled_template_without_task_records (tests.unit.test_task_from_plan.TaskFromPlanTest.test_generator_uses_the_bundled_template_without_task_records) ... ok
test_program_item_continues_until_the_next_numbered_heading (tests.unit.test_task_from_plan.TaskFromPlanTest.test_program_item_continues_until_the_next_numbered_heading) ... ok
test_wave_selection_matches_whole_todo_ids (tests.unit.test_task_from_plan.TaskFromPlanTest.test_wave_selection_matches_whole_todo_ids) ... ok
test_drift_checks_every_sha_and_state_for_each_pr_occurrence (tests.unit.test_plan_check.PlanCheckTest.test_drift_checks_every_sha_and_state_for_each_pr_occurrence) ... ok
test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task (tests.unit.test_plan_check.PlanCheckTest.test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task) ... ok
test_f2_detects_intersecting_globs_through_concrete_tree_matches (tests.unit.test_plan_check.PlanCheckTest.test_f2_detects_intersecting_globs_through_concrete_tree_matches) ... ok
test_invariants_reject_nonempty_quoted_oauth_token_assignments (tests.unit.test_plan_check.PlanCheckTest.test_invariants_reject_nonempty_quoted_oauth_token_assignments) ... ok
test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan (tests.unit.test_plan_check.PlanCheckTest.test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan) ... ok
test_c10_never_passes_a_literal_as_a_git_grep_option (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c10_never_passes_a_literal_as_a_git_grep_option) ... ok
test_c12_classifies_concrete_glob_matches_before_the_glob_spelling (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c12_classifies_concrete_glob_matches_before_the_glob_spelling) ... ok
test_c14_executes_premise_commands_only_for_the_dispatched_sha (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c14_executes_premise_commands_only_for_the_dispatched_sha) ... ok
test_c14_without_a_trusted_sha_reports_an_explicit_warning (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c14_without_a_trusted_sha_reports_an_explicit_warning) ... ok
test_c15_requires_the_design_assigned_invariant_id_set (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c15_requires_the_design_assigned_invariant_id_set) ... ok
test_c6_confines_design_paths_to_the_checkout (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_c6_confines_design_paths_to_the_checkout) ... ok
test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged) ... 
  test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged) (green='the current dotfiles-T133 task files') ... skipped 'no dotfiles-T133 task file in this tree yet (they land with a boundary records PR)'
test_ledger_check_counts_what_the_gate_counts (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_counts_what_the_gate_counts) ... ok
test_ledger_check_passes_a_complete_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_passes_a_complete_record) ... ok
test_ledger_check_reads_inherited_audit_ids_from_the_marker (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_reads_inherited_audit_ids_from_the_marker) ... ok
test_ledger_check_reports_the_gaps_of_the_pre_fix_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_reports_the_gaps_of_the_pre_fix_record) ... ok
test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary) ... ok
test_task_consistency_check_c9_probes_the_landed_checker_path (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_c9_probes_the_landed_checker_path) ... ok
test_task_consistency_check_detects_the_ten_historical_files (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_detects_the_ten_historical_files) ... ok
test_task_consistency_check_passes_a_complete_task_file (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_passes_a_complete_task_file) ... ok
test_task_consistency_check_reaches_every_other_check (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_reaches_every_other_check) ... ok

----------------------------------------------------------------------
Ran 28 tests in 26.653s

OK (skipped=1)
```

The one skip is the green-set subtest of `test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged`. It runs once the T133 task files are on `main`.

## Green: the other modules that run these scripts

```
$ uv run python -m unittest tests.unit.test_orchestrator_tools tests.unit.test_agmsg_orchestration_docs
Ran 110 tests in 69.920s
OK
```

## make unit-test: 6e07d291, and pristine origin/main 3e41e36a in the same sandbox

```
$ make unit-test   (a detached scratch worktree of 6e07d291, removed afterwards)
Ran 1226 tests in 756.051s
FAILED (failures=194, errors=111, skipped=3)
make: *** [unit-test] Error 1
$ make unit-test   (a detached scratch worktree of 3e41e36a, removed afterwards)
Ran 1207 tests in 1111.171s
FAILED (failures=194, errors=111, skipped=2)
make: *** [unit-test] Error 1
failing names: 310 on 6e07d291, 310 on 3e41e36a; identical: True
new failing names on 6e07d291: none
```

Each failing name is a sandbox-denied operation, the same on both sides, and none is in this task's modules. The extra tests on 6e07d291 are this task's, and all pass. CI's `make unit-test` decides the full suite.

## make format: 6e07d291, and pristine origin/main 3e41e36a

```
$ make format   (6e07d291)
make: *** [format] Error 1
shfmt --diff files: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh, .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh, home/dot_claude/hooks/executable_project-map-reload.sh, tests/install/macos/common/brew.bats
$ make format   (3e41e36a)
make: *** [format] Error 1
shfmt --diff files: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh, .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh, home/dot_claude/hooks/executable_project-map-reload.sh, tests/install/macos/common/brew.bats
identical: True
```

`make format` stops at its first command, `shfmt --diff .`, on the same twelve pre-existing files, so its ruff and prettier lines never run. They are run here on every changed file:

```
7 files already formatted
ruff=0
Checking formatting...
All matched files use Prettier code style!
prettier=0
```

## The checker on the T133 task files (item 2's Check), on 6e07d291

The T133 task files and the plan group exist only untracked in the main checkout, so it is `--root`. There is no `--premises-sha`, so C14 executes nothing and is recorded as not run.

```
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root ~/Workspace/dotfiles ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-*.md
(root at 740772efb9d7928e810a7d799f2bd32a88d9b8ff, origin/main 740772ef after #416)
-- stdout
dotfiles-T133-audit-pool-a01.md: OK
dotfiles-T133-ci-efficiency-a01.md: OK
dotfiles-T133-ci-efficiency-a02.md: OK
dotfiles-T133-ci-efficiency-followup-a01.md: OK
dotfiles-T133-ci-efficiency-followup-a02.md: OK
dotfiles-T133-dispositions-a01.md: OK
dotfiles-T133-dispositions-followup-a01.md: OK
dotfiles-T133-permission-guard-gate-a01.md: OK
dotfiles-T133-permission-guard-gate-a02.md: OK
dotfiles-T133-permission-guard-gate-a03.md: OK
dotfiles-T133-permission-guard-gate-followup-a01.md: OK
dotfiles-T133-regime-ci-a01.md: OK
dotfiles-T133-regime-ci-a02.md: OK
dotfiles-T133-regime-ci-followup-a01.md: OK
dotfiles-T133-result-precheck-a01.md: OK
dotfiles-T133-result-precheck-a02.md: OK
dotfiles-T133-result-precheck-a03.md: OK
dotfiles-T133-result-precheck-followup-a01.md: OK
dotfiles-T133-task-generator-plan-check-a01.md: OK
dotfiles-T133-task-generator-plan-check-a02.md: OK
dotfiles-T133-task-generator-plan-check-followup-a01.md: OK
dotfiles-T133-verdict-audit-pool-a01.md: OK
dotfiles-T133-verdict-audit-pool-a02.md: OK
dotfiles-T133-verdict-audit-pool-a03.md: OK
dotfiles-T133-verdict-audit-pool-followup-a01.md: OK
dotfiles-T133-worker-cap-hookspath-a01.md: OK
dotfiles-T133-worker-cap-hookspath-a02.md: OK
dotfiles-T133-worker-cap-hookspath-followup-a01.md: OK
dotfiles-T133-worker-hooks-path-a01.md: OK
-- stderr
dotfiles-T133-audit-pool-a01.md: warning: C14: not run (no trusted sha)
dotfiles-T133-ci-efficiency-a01.md: warning: C14: not run (no trusted sha)
dotfiles-T133-ci-efficiency-a02.md: warning: C14: not run (no trusted sha)
dotfiles-T133-dispositions-a01.md: warning: C14: not run (no trusted sha)
dotfiles-T133-permission-guard-gate-a01.md: warning: C14: not run (no trusted sha)
dotfiles-T133-permission-guard-gate-a02.md: warning: C14: not run (no trusted sha)
dotfiles-T133-permission-guard-gate-a03.md: warning: C14: not run (no trusted sha)
dotfiles-T133-regime-ci-a01.md: warning: C14: not run (no trusted sha)
dotfiles-T133-regime-ci-a02.md: warning: C14: not run (no trusted sha)
dotfiles-T133-result-precheck-a01.md: warning: C14: not run (no trusted sha)
dotfiles-T133-result-precheck-a02.md: warning: C14: not run (no trusted sha)
dotfiles-T133-result-precheck-a03.md: warning: C14: not run (no trusted sha)
dotfiles-T133-task-generator-plan-check-a01.md: warning: C14: not run (no trusted sha)
dotfiles-T133-task-generator-plan-check-a02.md: warning: C14: not run (no trusted sha)
dotfiles-T133-verdict-audit-pool-a01.md: warning: C14: not run (no trusted sha)
dotfiles-T133-verdict-audit-pool-a02.md: warning: C14: not run (no trusted sha)
dotfiles-T133-verdict-audit-pool-a03.md: warning: C14: not run (no trusted sha)
dotfiles-T133-worker-cap-hookspath-a01.md: warning: C14: not run (no trusted sha)
dotfiles-T133-worker-cap-hookspath-a02.md: warning: C14: not run (no trusted sha)
dotfiles-T133-worker-hooks-path-a01.md: warning: C14: not run (no trusted sha)
exit=0
```

C1 to C13, C15 and C7b found nothing in any of the files. C14: not run on each of the 20 files with premises, with the warning above. That is not a pass.

## plan-check, once (eb20d063's code; the correction changed only `--drift`)

```
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/plan-check.py --root ~/Workspace/dotfiles
F3 024-todo.md:22 P1-13 names no bottleneck id of 5.0 or 5.10
F3 024-todo.md:23 P1-14 names no bottleneck id of 5.0 or 5.10
F4 024-checklists.md:9 P1-a holds no backtick command or file path
F6 024-omp-cutover-and-corrective-order.md:39 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file
F6 024-omp-cutover-and-corrective-order.md:70 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file
F6 024-todo.md:9 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file
exit=1
```

These six violations are in the real plan group. They are reported and left for the orchestrator; a01 reported the same six.

## Caps

```
$ git diff --numstat origin/main...HEAD   (code head 6e07d291, merge base 3e41e36a)
16	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/learning.md
107	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/report.md
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/revise.yaml
20	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/sandbox.md
603	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/validation.md
231	0	.orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
232	0	scripts/orchestrator/plan-check.py
140	11	scripts/orchestrator/task-consistency-check.py
242	0	scripts/orchestrator/task-from-plan.py
34	0	scripts/orchestrator/task-template.md
166	0	tests/unit/test_plan_check.py
9	3	tests/unit/test_task_checkers.py
265	0	tests/unit/test_task_consistency_c11_c15.py
214	0	tests/unit/test_task_from_plan.py
outside tests/ and .orchestration/: 659 (cap 700); under tests/: 657 (cap 800)
```

## CompactionDB memory

```
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T133 P1-12 a02: task-from-plan.py reads only scripts/orchestrator/task-template.md …'
b5f77b7f-dde3-4401-b29c-3860ec126856
exit=0
```

## Amendment 1: the CI-repair round (code head eb0b1c06, on 63b6acae, the update-branch onto b22a5580)

The task copy, amendment 1:

```
$ shasum -a 256 .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
60d4c2db70ec6e8783945f3b6f2052cafe07da85700d574c0f70e477f7c7d1e9  .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md
```

Red: the regime tests on 63b6acae, before the repair:

```
$ uv run python -m unittest tests.unit.test_regime_ci
FAIL: test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage (reset_of=True, predecessor_copy_kept=True)
AssertionError: 0 != 1 : regime-ci: warning: t1-a01: predecessor copy .orchestration/t1-a01/task.md (reset_of of t1-a02)
FAIL: test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage (reset_of=True, predecessor_copy_kept=False)
AssertionError: 0 != 1 : regime-ci: t1-a02: checker: C13 disposition is not closed:, residual: or out-of-scope: and a space: residual
FAIL: test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier (expected=0, phrase=None)
AssertionError: 0 != 1 : regime-ci: warning: the diff changes scripts/orchestrator/regime-ci.py; this run executed the base's version, the audit reads the change
FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr
AssertionError: Tuples differ: (0, 'regime-ci: ok 1 task(s)\n') != (1, 'regime-ci: t1-a01: checker: C13 dispo[1170 chars]l\n')
FAIL: test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config
AssertionError: Tuples differ: (0, 'regime-ci: ok 1 task(s)\n') != (1, 'regime-ci: t1-a01: checker: C13 dispo[1170 chars]l\n')
Ran 15 tests in 20.702s
FAILED (failures=5)
```

Green on eb0b1c06: the regime tests, the four task modules and the orchestrator tool tests.

```
$ uv run python -m unittest tests.unit.test_regime_ci tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers tests.unit.test_orchestrator_tools -v
Ran 101 tests in 125.509s
OK (skipped=1)
```

Caps (`git diff --numstat` against the merge base b22a5580, outside `.orchestration/`):

```
232	0	scripts/orchestrator/plan-check.py
140	11	scripts/orchestrator/task-consistency-check.py
242	0	scripts/orchestrator/task-from-plan.py
34	0	scripts/orchestrator/task-template.md
166	0	tests/unit/test_plan_check.py
11	5	tests/unit/test_regime_ci.py
9	3	tests/unit/test_task_checkers.py
265	0	tests/unit/test_task_consistency_c11_c15.py
214	0	tests/unit/test_task_from_plan.py
```
