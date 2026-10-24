# Validation: dotfiles-T128-chain-glue-finish-a02

Verbatim outputs (worker, Claude seat). Home paths are written `~` and the sandbox temporary directory `$TMPDIR`.

## 1. Red at b09c88c6 (the test committed in cf0aa46c ran against b09c88c6's script): the behavioural assertion and the lint

```text
$ git rev-parse HEAD   # worker (Claude seat)
b09c88c6deaed78ca7c06bfb314cd52bff1123e8
$ python3.15 -m unittest tests.unit.test_chain_glue.ChainIntegrateTest.test_shim_exclusion_compares_the_resolved_path -v
test_shim_exclusion_compares_the_resolved_path (tests.unit.test_chain_glue.ChainIntegrateTest.test_shim_exclusion_compares_the_resolved_path) ... 
  test_shim_exclusion_compares_the_resolved_path (tests.unit.test_chain_glue.ChainIntegrateTest.test_shim_exclusion_compares_the_resolved_path) (found=PosixPath('$TMPDIR/tmpjm5a4nn9/linked/jq')) ... FAIL

======================================================================
FAIL: test_shim_exclusion_compares_the_resolved_path (tests.unit.test_chain_glue.ChainIntegrateTest.test_shim_exclusion_compares_the_resolved_path) (found=PosixPath('$TMPDIR/tmpjm5a4nn9/linked/jq'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_chain_glue.py", line 761, in test_shim_exclusion_compares_the_resolved_path
    result = self.finish(code=10, env={"PATH": f"{found.parent}{os.pathsep}{self.env['PATH']}"})
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_chain_glue.py", line 631, in finish
    self.assertEqual(code, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 10 != 0 : resolve-threads rc=0
pr-feedback rc=0
fill-sweep rc=0
orch
fill-sweep rc=0
{"id":1,"body":"a"}
{"id":2,"body":"b,\nc"}
fill-sweep rc=0
record rc=0
4280648512	class-a
audit:abcdef1:2	class-b
record rc=0
gate rc=0
merge rc=0
merge rc=0
6424530f51f7945b70993895a85cb78b6fa62583
merge rc=0
ff-main rc=0
pr-cost rc=0
AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-x-a01 status=accepted reason=merged-as-6424530f51f7945b70993895a85cb78b6fa62583-pr-7-head-86ba221 next_action=<the orchestrator fills this before sending>


----------------------------------------------------------------------
Ran 1 test in 6.900s

FAILED (failures=1)
exit 1
$ python3.15 -I scripts/lint-comparisons.py --changed scripts/orchestrator/chain-finish.sh
scripts/orchestrator/chain-finish.sh:67: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
scripts/orchestrator/chain-finish.sh:111: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
exit 1
```

## 2. Green at 4628fc06: both modules, the lint, the shell checks, ruff, this reset's numstat

```text
$ git rev-parse HEAD   # worker (Claude seat)
4628fc06efc6d8f126d6d4fe9619dea80d30781f
$ python3.15 -m unittest tests.unit.test_chain_glue tests.unit.test_lint_comparisons -v
test_finish_checks_each_audit_finding_line_in_full (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_checks_each_audit_finding_line_in_full) ... ok
test_finish_counts_the_trimmed_reason (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_counts_the_trimmed_reason) ... ok
test_finish_prints_the_acceptance_line_and_sends_nothing (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_prints_the_acceptance_line_and_sends_nothing) ... ok
test_finish_reads_the_last_nonblank_line_as_the_verdict (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_reads_the_last_nonblank_line_as_the_verdict) ... ok
test_finish_refuses_a_head_that_differs_from_the_audit (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_head_that_differs_from_the_audit) ... ok
test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head) ... ok
test_finish_requires_an_audit_finding_line_per_incorrect_finding (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_requires_an_audit_finding_line_per_incorrect_finding) ... ok
test_finish_runs_gate_before_merge_and_cost_after (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_gate_before_merge_and_cost_after) ... ok
test_finish_runs_pr_cost_with_a_path_of_resolved_links (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_pr_cost_with_a_path_of_resolved_links) ... ok
test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward) ... ok
test_finish_waits_for_the_merge_to_land_before_reading_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_waits_for_the_merge_to_land_before_reading_main) ... ok
test_inheritance_requires_a_parent_verdict_the_gate_accepts (tests.unit.test_chain_glue.ChainIntegrateTest.test_inheritance_requires_a_parent_verdict_the_gate_accepts) ... ok
test_inheritance_requires_the_merge_tree_reproduction_to_equal_the_head_tree (tests.unit.test_chain_glue.ChainIntegrateTest.test_inheritance_requires_the_merge_tree_reproduction_to_equal_the_head_tree) ... ok
test_inheritance_requires_the_parent_chain_log_to_name_its_full_sha (tests.unit.test_chain_glue.ChainIntegrateTest.test_inheritance_requires_the_parent_chain_log_to_name_its_full_sha) ... ok
test_integrate_inherits_the_audit_across_an_update_branch_only_head (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_inherits_the_audit_across_an_update_branch_only_head) ... ok
test_integrate_refuses_a_main_checkout_script_that_is_not_heads (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_a_main_checkout_script_that_is_not_heads) ... ok
test_integrate_refuses_a_stale_main_checkout_after_the_restart (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_a_stale_main_checkout_after_the_restart) ... ok
test_integrate_refuses_an_absent_owner_task_before_the_advisory_step (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_an_absent_owner_task_before_the_advisory_step) ... ok
test_integrate_refuses_an_extra_tsv_outside_the_main_checkout (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_an_extra_tsv_outside_the_main_checkout) ... ok
test_integrate_refuses_when_main_is_not_on_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_when_main_is_not_on_main) ... ok
test_integrate_resolves_binaries_before_the_checkout (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_resolves_binaries_before_the_checkout) ... ok
test_integrate_restarts_after_update_branch (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restarts_after_update_branch) ... ok
test_integrate_restarts_when_the_base_moves_during_the_waits (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restarts_when_the_base_moves_during_the_waits) ... ok
test_integrate_restores_the_review_worktree_after_the_audit (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restores_the_review_worktree_after_the_audit) ... ok
test_integrate_runs_gh_without_forced_colour (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_runs_gh_without_forced_colour) ... ok
test_integrate_runs_the_steps_in_order_and_logs_each (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_runs_the_steps_in_order_and_logs_each) ... ok
test_integrate_stops_on_a_sandbox_scan_hit (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_stops_on_a_sandbox_scan_hit) ... ok
test_shim_exclusion_compares_the_resolved_path (tests.unit.test_chain_glue.ChainIntegrateTest.test_shim_exclusion_compares_the_resolved_path) ... ok
test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails) ... ok
test_a_baseline_row_matching_no_hit_fails_as_stale (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_matching_no_hit_fails_as_stale) ... ok
test_a_hit_in_a_changed_file_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_hit_in_a_changed_file_fails) ... ok
test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning) ... ok
test_a_jq_normaliser_name_inside_a_string_literal_is_no_application (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_jq_normaliser_name_inside_a_string_literal_is_no_application) ... ok
test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails) ... ok
test_a_single_quoted_jq_option_value_is_not_read_as_the_program (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) ... ok
test_a_stale_row_for_a_changed_file_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_stale_row_for_a_changed_file_fails) ... ok
test_a_stale_row_for_an_unchanged_file_warns (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_stale_row_for_an_unchanged_file_warns) ... ok
test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted (tests.unit.test_lint_comparisons.LintComparisonsTest.test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted) ... ok
test_every_f_string_interpolation_in_a_regex_is_escaped (tests.unit.test_lint_comparisons.LintComparisonsTest.test_every_f_string_interpolation_in_a_regex_is_escaped) ... ok
test_the_changed_files_are_clean_against_the_baseline (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_changed_files_are_clean_against_the_baseline) ... ok
test_the_jq_normaliser_is_required_on_each_operand_side (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_jq_normaliser_is_required_on_each_operand_side) ... ok
test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails) ... ok

----------------------------------------------------------------------
Ran 42 tests in 157.631s

OK
exit 0
$ python3.15 -I scripts/lint-comparisons.py --changed scripts/orchestrator/chain-finish.sh
exit 0
$ bash -n scripts/orchestrator/chain-finish.sh
exit 0
$ shellcheck scripts/orchestrator/chain-finish.sh
exit 0
$ ruff check tests/unit/test_chain_glue.py
All checks passed!
exit 0
$ git diff --numstat b09c88c6deaed78ca7c06bfb314cd52bff1123e8 HEAD
2	2	scripts/orchestrator/chain-finish.sh
15	0	tests/unit/test_chain_glue.py
```

## R4.1 Round 4, red at 2b586637: the two Bot-thread tests (worker, Claude seat)

```text
$ git rev-parse HEAD   # worker (Claude seat)
2b5866370d3796c90b9b9a96499f20fe8dd4d4fe
$ python3.15 -m unittest tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_ff_main_with_the_pre_merge_links tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_pr_whose_base_is_not_main -v
test_finish_runs_ff_main_with_the_pre_merge_links (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_ff_main_with_the_pre_merge_links) ... FAIL
test_finish_refuses_a_pr_whose_base_is_not_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_pr_whose_base_is_not_main) ... FAIL

======================================================================
FAIL: test_finish_runs_ff_main_with_the_pre_merge_links (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_ff_main_with_the_pre_merge_links)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_chain_glue.py", line 773, in test_finish_runs_ff_main_with_the_pre_merge_links
    self.assertEqual(f"{self.v}/{TASK}-pr-cost-bin-{self.head[:7]}", path)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: '/pri[27 chars]ffpw/main/.orchestration/validation/dotfiles-T[25 chars]0483' != '/pri[27 chars]ffpw/bin:/usr/bin:/bin'
- $TMPDIR/tmpmt3dffpw/main/.orchestration/validation/dotfiles-T128-x-a01-pr-cost-bin-c260483
+ $TMPDIR/tmpmt3dffpw/bin:/usr/bin:/bin


======================================================================
FAIL: test_finish_refuses_a_pr_whose_base_is_not_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_pr_whose_base_is_not_main)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_chain_glue.py", line 780, in test_finish_refuses_a_pr_whose_base_is_not_main
    result = self.finish(code=10)
  File "~/Workspace/dotfiles/.claude/worktrees/worker-f/tests/unit/test_chain_glue.py", line 632, in finish
    self.assertEqual(code, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 10 != 0 : resolve-threads rc=0
pr-feedback rc=0
fill-sweep rc=0
orch
fill-sweep rc=0
{"id":1,"body":"a"}
{"id":2,"body":"b,\nc"}
fill-sweep rc=0
record rc=0
4280648512	class-a
audit:abcdef1:2	class-b
record rc=0
gate rc=0
merge rc=0
merge rc=0
9c685539a3246801edd54a228e9a589ab20ff5c0
merge rc=0
ff-main rc=0
pr-cost rc=0
AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-x-a01 status=accepted reason=merged-as-9c685539a3246801edd54a228e9a589ab20ff5c0-pr-7-head-138f9a5 next_action=<the orchestrator fills this before sending>
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-afsTUFBR' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-PPj6aBYN' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-u3k4uukB' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-b5NoIUZd' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-Rm8kfFNH' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-8OQKeZEy' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-iGnnaJx5' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-lY78yIBO' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-hGFLPbMr' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-Nw03d5ru' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-qE6rtdJN' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-T2uEyDef' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-zUk1hRTg' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-a1OTvrac' (errno=Operation not permitted)
python3: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-mJkD14mv' (errno=Operation not permitted)
python3: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-BZrGDZOW' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-NgjWcNvi' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-LEwCpaYB' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-8XIMVCcr' (errno=Operation not permitted)
git: error: couldn't create cache file '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/xcrun_db-XLFMGvE2' (errno=Operation not permitted)


----------------------------------------------------------------------
Ran 2 tests in 9.229s

FAILED (failures=2)
exit 1
```

## R4.2 Round 4, green at afbe3d4d: both modules, the shell checks, ruff, the lint, the caps (worker, Claude seat)

```text
$ git rev-parse HEAD   # worker (Claude seat)
afbe3d4dbc7ddf5e53b6847d16026018db140237
$ python3.15 -m unittest tests.unit.test_chain_glue tests.unit.test_lint_comparisons -v
test_finish_checks_each_audit_finding_line_in_full (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_checks_each_audit_finding_line_in_full) ... ok
test_finish_counts_the_trimmed_reason (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_counts_the_trimmed_reason) ... ok
test_finish_prints_the_acceptance_line_and_sends_nothing (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_prints_the_acceptance_line_and_sends_nothing) ... ok
test_finish_reads_the_last_nonblank_line_as_the_verdict (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_reads_the_last_nonblank_line_as_the_verdict) ... ok
test_finish_refuses_a_head_that_differs_from_the_audit (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_head_that_differs_from_the_audit) ... ok
test_finish_refuses_a_pr_whose_base_is_not_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_pr_whose_base_is_not_main) ... ok
test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head) ... ok
test_finish_requires_an_audit_finding_line_per_incorrect_finding (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_requires_an_audit_finding_line_per_incorrect_finding) ... ok
test_finish_runs_ff_main_with_the_pre_merge_links (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_ff_main_with_the_pre_merge_links) ... ok
test_finish_runs_gate_before_merge_and_cost_after (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_gate_before_merge_and_cost_after) ... ok
test_finish_runs_pr_cost_with_a_path_of_resolved_links (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_pr_cost_with_a_path_of_resolved_links) ... ok
test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward) ... ok
test_finish_waits_for_the_merge_to_land_before_reading_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_waits_for_the_merge_to_land_before_reading_main) ... ok
test_inheritance_requires_a_parent_verdict_the_gate_accepts (tests.unit.test_chain_glue.ChainIntegrateTest.test_inheritance_requires_a_parent_verdict_the_gate_accepts) ... ok
test_inheritance_requires_the_merge_tree_reproduction_to_equal_the_head_tree (tests.unit.test_chain_glue.ChainIntegrateTest.test_inheritance_requires_the_merge_tree_reproduction_to_equal_the_head_tree) ... ok
test_inheritance_requires_the_parent_chain_log_to_name_its_full_sha (tests.unit.test_chain_glue.ChainIntegrateTest.test_inheritance_requires_the_parent_chain_log_to_name_its_full_sha) ... ok
test_integrate_inherits_the_audit_across_an_update_branch_only_head (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_inherits_the_audit_across_an_update_branch_only_head) ... ok
test_integrate_refuses_a_main_checkout_script_that_is_not_heads (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_a_main_checkout_script_that_is_not_heads) ... ok
test_integrate_refuses_a_stale_main_checkout_after_the_restart (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_a_stale_main_checkout_after_the_restart) ... ok
test_integrate_refuses_an_absent_owner_task_before_the_advisory_step (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_an_absent_owner_task_before_the_advisory_step) ... ok
test_integrate_refuses_an_extra_tsv_outside_the_main_checkout (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_an_extra_tsv_outside_the_main_checkout) ... ok
test_integrate_refuses_when_main_is_not_on_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_when_main_is_not_on_main) ... ok
test_integrate_resolves_binaries_before_the_checkout (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_resolves_binaries_before_the_checkout) ... ok
test_integrate_restarts_after_update_branch (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restarts_after_update_branch) ... ok
test_integrate_restarts_when_the_base_moves_during_the_waits (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restarts_when_the_base_moves_during_the_waits) ... ok
test_integrate_restores_the_review_worktree_after_the_audit (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restores_the_review_worktree_after_the_audit) ... ok
test_integrate_runs_gh_without_forced_colour (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_runs_gh_without_forced_colour) ... ok
test_integrate_runs_the_steps_in_order_and_logs_each (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_runs_the_steps_in_order_and_logs_each) ... ok
test_integrate_stops_on_a_sandbox_scan_hit (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_stops_on_a_sandbox_scan_hit) ... ok
test_shim_exclusion_compares_the_resolved_path (tests.unit.test_chain_glue.ChainIntegrateTest.test_shim_exclusion_compares_the_resolved_path) ... ok
test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_is_consumed_once_so_a_duplicate_hit_fails) ... ok
test_a_baseline_row_matching_no_hit_fails_as_stale (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_matching_no_hit_fails_as_stale) ... ok
test_a_hit_in_a_changed_file_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_hit_in_a_changed_file_fails) ... ok
test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_hit_main_introduced_in_an_unchanged_file_passes_with_a_warning) ... ok
test_a_jq_normaliser_name_inside_a_string_literal_is_no_application (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_jq_normaliser_name_inside_a_string_literal_is_no_application) ... ok
test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_normaliser_is_matched_by_its_qualified_name_so_a_foreign_receiver_fails) ... ok
test_a_single_quoted_jq_option_value_is_not_read_as_the_program (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_single_quoted_jq_option_value_is_not_read_as_the_program) ... ok
test_a_stale_row_for_a_changed_file_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_stale_row_for_a_changed_file_fails) ... ok
test_a_stale_row_for_an_unchanged_file_warns (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_stale_row_for_an_unchanged_file_warns) ... ok
test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted (tests.unit.test_lint_comparisons.LintComparisonsTest.test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted) ... ok
test_every_f_string_interpolation_in_a_regex_is_escaped (tests.unit.test_lint_comparisons.LintComparisonsTest.test_every_f_string_interpolation_in_a_regex_is_escaped) ... ok
test_the_changed_files_are_clean_against_the_baseline (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_changed_files_are_clean_against_the_baseline) ... ok
test_the_jq_normaliser_is_required_on_each_operand_side (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_jq_normaliser_is_required_on_each_operand_side) ... ok
test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails (tests.unit.test_lint_comparisons.LintComparisonsTest.test_with_no_mode_flag_the_change_is_origin_main_to_head_and_a_missing_base_fails) ... ok

----------------------------------------------------------------------
Ran 44 tests in 180.362s

OK
exit 0
$ bash -n scripts/orchestrator/chain-finish.sh
exit 0
$ shellcheck scripts/orchestrator/chain-finish.sh
exit 0
$ ruff check tests/unit/test_chain_glue.py
All checks passed!
exit 0
$ python3.15 -I scripts/lint-comparisons.py --changed scripts/orchestrator/chain-finish.sh
exit 0
$ git merge-base origin/main HEAD; git diff --numstat <merge-base> HEAD
7da0cdfab9de9fbea673b82379acd4e317115065
183	0	scripts/orchestrator/chain-finish.sh
312	2	tests/unit/test_chain_glue.py
$ git diff --numstat 2b5866370d3796c90b9b9a96499f20fe8dd4d4fe HEAD   # this round
9	4	scripts/orchestrator/chain-finish.sh
26	2	tests/unit/test_chain_glue.py
```
