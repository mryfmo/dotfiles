---
task_id: dotfiles-T133-result-precheck-a02
round: 1
reset_of: dotfiles-T133-result-precheck-a01
---

# Validation

Fresh results of this reset task. Tested code head 38b9178b7a25df16ac26e01110294edfdd30d61c on base `origin/main` 99a4a80f, branch `tools/result-precheck-a01` (PR #411), worker-c worktree, inside the Claude seat's Bash sandbox; the final commit adds only `.orchestration/dotfiles-T133-result-precheck-a02/` evidence. The reviewed production implementation of the red runs is a01's last head a5cb73b4. a01's records under `.orchestration/dotfiles-T133-result-precheck-a01/` are inherited history, not results of this task. Every block is verbatim output with its exit status.

## Items 5 to 7: red on a5cb73b4, green on 38b9178b

Each red run copies the current test source into a detached temporary worktree at a5cb73b4 (the reviewed production implementation) and runs the three regressions there; every failure is an assertion (`FAIL`), none an import error, missing test or runner failure (`ERROR`). The green run is the same three tests on 38b9178b.

```text
$ bash red-a02.sh a5cb73b489235bb177e346dd00dd9aca28a432e8 test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit test_precheck_records_failed_commands_as_not_ok test_dispatch_rejects_malformed_checks_and_missing_requested_selectors
checkout=a5cb73b489235bb177e346dd00dd9aca28a432e8 test_source_sha256=d465d2eb1af1ff53e6d4c9828e6498ac55aa5ec5fbd69b872f8806924656bfac
unittest exit=1
test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit ... 
  test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit (branch='diff-attr') ... FAIL
  test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit (branch='binary-attr') ... FAIL
  test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit (branch='nul') ... FAIL
  test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit (branch='added-then-removed') ... FAIL
test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit ... FAIL
test_precheck_records_failed_commands_as_not_ok ... FAIL
test_dispatch_rejects_malformed_checks_and_missing_requested_selectors ... 
  test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='an empty entry') ... FAIL
  test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a missing check') ... FAIL
  test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='only an unrelated check') ... FAIL
  test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a duplicate name') ... FAIL
  test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a missing ok') ... FAIL
  test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a string ok') ... FAIL
  test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a numeric ok') ... FAIL
  test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a null ok') ... FAIL
  test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a null without the marker') ... FAIL
  test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='missing selectors') ... FAIL
  test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='one requested selector omitted') ... FAIL
FAIL: test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit (branch='diff-attr')
AssertionError: False != True : To /private/tmp/claude-501/tmptbofz81x/origin.git
FAIL: test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit (branch='binary-attr')
AssertionError: False != True : To /private/tmp/claude-501/tmptbofz81x/origin.git
FAIL: test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit (branch='nul')
AssertionError: False != True : To /private/tmp/claude-501/tmptbofz81x/origin.git
FAIL: test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit (branch='added-then-removed')
AssertionError: False != True : To /private/tmp/claude-501/tmptbofz81x/origin.git
FAIL: test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit
AssertionError: 0 != 1 : result-precheck: unit-test exit 0
FAIL: test_precheck_records_failed_commands_as_not_ok
AssertionError: 0 != 1 : result-precheck: unit-test exit 0
FAIL: test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='an empty entry')
AssertionError: Tuples differ: (0, True) != (1, False)
FAIL: test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a missing check')
AssertionError: Tuples differ: (0, True) != (1, False)
FAIL: test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='only an unrelated check')
AssertionError: Tuples differ: (0, True) != (1, False)
FAIL: test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a duplicate name')
AssertionError: Tuples differ: (0, True) != (1, False)
FAIL: test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a missing ok')
AssertionError: Tuples differ: (0, True) != (1, False)
FAIL: test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a string ok')
AssertionError: Tuples differ: (0, True) != (1, False)
FAIL: test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a numeric ok')
AssertionError: Tuples differ: (0, True) != (1, False)
FAIL: test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a null ok')
AssertionError: Tuples differ: (0, True) != (1, False)
FAIL: test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='a null without the marker')
AssertionError: Tuples differ: (0, True) != (1, False)
FAIL: test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='missing selectors')
AssertionError: Tuples differ: (0, True) != (1, False)
FAIL: test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (case='one requested selector omitted')
AssertionError: Tuples differ: (0, True) != (1, False)
Ran 3 tests in 9.079s
FAILED (failures=17)
removed=0
exit=0
```

```text
$ uv run python -m unittest test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit test_precheck_records_failed_commands_as_not_ok test_dispatch_rejects_malformed_checks_and_missing_requested_selectors -v
test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit) ... ok
test_precheck_records_failed_commands_as_not_ok (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_records_failed_commands_as_not_ok) ... ok
test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_rejects_malformed_checks_and_missing_requested_selectors) ... ok

----------------------------------------------------------------------
Ran 3 tests in 17.956s

OK
exit=0
```

## The Check (all but the precheck runs) on 38b9178b

`make format` exits 2 on this head and on `origin/main` alike, its `shfmt --diff .` flagging the identical twelve files outside CI's scope (a01's Amendment 1); CI's three formatting commands in CI's scopes, the precheck's `format` check, pass.

```text
$ git rev-parse HEAD origin/main
38b9178b7a25df16ac26e01110294edfdd30d61c
99a4a80f5a5b32a70cf7eb4f4d0db5a02d113841
exit=0

$ make render-check
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
exit=0

$ shellcheck -x scripts/orchestrator/result-precheck.sh .githooks/pre-commit .githooks/pre-push scripts/orchestrator/dispatch.sh
exit=0

$ shfmt -d -i 4 -sr scripts/orchestrator/result-precheck.sh .githooks/pre-commit .githooks/pre-push scripts/orchestrator/dispatch.sh
exit=0

$ git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs shfmt -i 4 -sr -d
exit=0

$ git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check
62 files already formatted
exit=0

$ git ls-files -z '*.md' | xargs -0 prettier --check
Checking formatting...
All matched files use Prettier code style!
exit=0

$ make format > format.txt 2>&1   (this head)
exit=2
$ (cd <origin/main worktree> && make format > format-base.txt 2>&1)
exit=2
$ the files shfmt flags: this head 12, origin/main 12
cmp: identical flagged sets
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
home/dot_claude/hooks/executable_project-map-reload.sh
tests/install/macos/common/brew.bats

$ uv run python -m unittest tests.unit.test_result_precheck tests.unit.test_orchestrator_tools -v
test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required (tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required) ... ok
test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_rejects_malformed_checks_and_missing_requested_selectors) ... ok
test_pre_commit_hook_checks_the_staged_blobs_not_the_working_tree (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_commit_hook_checks_the_staged_blobs_not_the_working_tree) ... ok
test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure) ... ok
test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern) ... ok
test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit) ... ok
test_precheck_exits_1_and_records_ok_false_for_each_failing_check (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_exits_1_and_records_ok_false_for_each_failing_check) ... ok
test_precheck_records_failed_commands_as_not_ok (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_records_failed_commands_as_not_ok) ... ok
test_precheck_records_the_local_review_as_deferred_by_default (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_records_the_local_review_as_deferred_by_default) ... ok
test_precheck_secrets_mode_counts_and_never_prints_the_match (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_secrets_mode_counts_and_never_prints_the_match) ... ok
test_precheck_selector_proof_requires_red_on_previous_head_and_green_on_head (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_selector_proof_requires_red_on_previous_head_and_green_on_head) ... ok
test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record) ... ok
test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit) ... ok
test_boundary_commits_pushes_and_queues_the_pr (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_commits_pushes_and_queues_the_pr) ... ok
test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path) ... ok
test_boundary_deletes_a_name_with_glob_characters_literally (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_deletes_a_name_with_glob_characters_literally) ... ok
test_boundary_keeps_a_name_with_a_newline_one_path (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_keeps_a_name_with_a_newline_one_path) ... ok
test_boundary_stops_before_commit_when_the_validator_fails (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_stops_before_commit_when_the_validator_fails) ... ok
test_bus_read_closes_a_task_on_any_non_revise_acceptance (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_closes_a_task_on_any_non_revise_acceptance) ... ok
test_bus_read_ignores_closers_between_other_endpoints (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_ignores_closers_between_other_endpoints) ... ok
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event) ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_refuses_a_read_that_reaches_its_limit) ... ok
test_bus_read_skips_and_counts_malformed_rows (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_bus_read_skips_and_counts_malformed_rows) ... ok
test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash) ... ok
test_design_keydiff_names_the_changed_invariant (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_design_keydiff_names_the_changed_invariant) ... ok
test_dispatch_line_grammar_table (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_line_grammar_table) ... ok
test_dispatch_passes_the_line_byte_identical (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_passes_the_line_byte_identical) ... ok
test_dispatch_reads_a_bounded_history_window (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_reads_a_bounded_history_window) ... ok
test_dispatch_record_path_tokenizes_and_locks (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_record_path_tokenizes_and_locks) ... ok
test_dispatch_records_the_sent_line_with_its_read_marker (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_records_the_sent_line_with_its_read_marker) ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file) ... ok
test_dispatch_refuses_a_line_without_a_task_id (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_line_without_a_task_id) ... ok
test_dispatch_refuses_a_malformed_record_block_before_sending (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_malformed_record_block_before_sending) ... ok
test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields) ... ok
test_dispatch_refuses_a_task_file_failing_the_checker (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_task_file_failing_the_checker) ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line) ... ok
test_dispatch_refuses_an_unwritable_record_before_sending (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_an_unwritable_record_before_sending) ... ok
test_dispatch_refuses_malformed_lines (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_malformed_lines) ... ok
test_dispatch_resolves_its_root_without_inherited_git_variables (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_resolves_its_root_without_inherited_git_variables) ... ok
test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state) ... ok
test_ff_main_keeps_a_local_deletion_across_the_fast_forward (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_ff_main_keeps_a_local_deletion_across_the_fast_forward) ... ok
test_ff_main_keeps_local_edits_across_the_fast_forward (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_ff_main_keeps_local_edits_across_the_fast_forward) ... ok
test_fill_sweep_fills_only_a_commented_review (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_fills_only_a_commented_review) ... ok
test_fill_sweep_fills_only_notice_annotations_and_success_statuses (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_fills_only_notice_annotations_and_success_statuses) ... ok
test_fill_sweep_ignores_a_disposition_reply_from_another_login (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_ignores_a_disposition_reply_from_another_login) ... ok
test_fill_sweep_leaves_a_badged_review_body_a_gap (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_leaves_a_badged_review_body_a_gap) ... ok
test_fill_sweep_quotes_the_url_form_evidence (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_quotes_the_url_form_evidence) ... ok
test_fill_sweep_refuses_a_not_applicable_without_evidence (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_refuses_a_not_applicable_without_evidence) ... ok
test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id) ... ok
test_fill_sweep_sees_a_collision_after_the_discussion_r_strip (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_sees_a_collision_after_the_discussion_r_strip) ... ok
test_fill_sweep_selects_a_null_url_status_by_source_and_check (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_selects_a_null_url_status_by_source_and_check) ... ok
test_orch_audit_refuses_a_ledger_check_that_differs_from_head (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_refuses_a_ledger_check_that_differs_from_head) ... ok
test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt) ... ok
test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap) ... ok
test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules) ... ok
test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout) ... ok
test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree) ... ok
test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration) ... ok
test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves) ... ok
test_orch_gate_restores_the_review_worktree_when_setup_fails (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_restores_the_review_worktree_when_setup_fails) ... ok
test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree) ... ok
test_orch_gate_runs_the_gate_under_an_explicit_environment (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_runs_the_gate_under_an_explicit_environment) ... ok
test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs) ... ok
test_replay_propagates_the_command_status (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_replay_propagates_the_command_status) ... ok
test_three_repeat_prints_body_matches_and_states_a_capped_memory_count (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_three_repeat_prints_body_matches_and_states_a_capped_memory_count) ... ok
test_three_repeat_prints_the_records_search_line (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_three_repeat_prints_the_records_search_line) ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout) ... ok

----------------------------------------------------------------------
Ran 67 tests in 118.489s

OK
exit=0

$ git diff --numstat origin/main...HEAD
13	0	.githooks/pre-commit
34	0	.githooks/pre-push
14	0	.orchestration/dotfiles-T133-result-precheck-a01/learning.md
3	0	.orchestration/dotfiles-T133-result-precheck-a01/precheck-format.log
2	0	.orchestration/dotfiles-T133-result-precheck-a01/precheck-render-check.log
1	0	.orchestration/dotfiles-T133-result-precheck-a01/precheck-secrets.log
5	0	.orchestration/dotfiles-T133-result-precheck-a01/precheck-selector-1-head.log
5	0	.orchestration/dotfiles-T133-result-precheck-a01/precheck-selector-1-previous.log
0	0	.orchestration/dotfiles-T133-result-precheck-a01/precheck-shellcheck.log
69	0	.orchestration/dotfiles-T133-result-precheck-a01/precheck-unit-test.log
52	0	.orchestration/dotfiles-T133-result-precheck-a01/precheck.json
61	0	.orchestration/dotfiles-T133-result-precheck-a01/report.md
1	0	.orchestration/dotfiles-T133-result-precheck-a01/result.txt
8	0	.orchestration/dotfiles-T133-result-precheck-a01/revise.yaml
21	0	.orchestration/dotfiles-T133-result-precheck-a01/sandbox.md
109	0	.orchestration/dotfiles-T133-result-precheck-a01/task.md
646	0	.orchestration/dotfiles-T133-result-precheck-a01/validation.md
160	0	.orchestration/dotfiles-T133-result-precheck-a02/task.md
79	1	scripts/orchestrator/dispatch.sh
271	0	scripts/orchestrator/result-precheck.sh
446	0	tests/unit/test_result_precheck.py
exit=0

$ git diff --numstat origin/main...HEAD -- scripts .githooks | sum; -- tests | sum
outside tests and .orchestration: 398
under tests: 446

$ git diff --name-only origin/main...HEAD
.githooks/pre-commit
.githooks/pre-push
.orchestration/dotfiles-T133-result-precheck-a01/learning.md
.orchestration/dotfiles-T133-result-precheck-a01/precheck-format.log
.orchestration/dotfiles-T133-result-precheck-a01/precheck-render-check.log
.orchestration/dotfiles-T133-result-precheck-a01/precheck-secrets.log
.orchestration/dotfiles-T133-result-precheck-a01/precheck-selector-1-head.log
.orchestration/dotfiles-T133-result-precheck-a01/precheck-selector-1-previous.log
.orchestration/dotfiles-T133-result-precheck-a01/precheck-shellcheck.log
.orchestration/dotfiles-T133-result-precheck-a01/precheck-unit-test.log
.orchestration/dotfiles-T133-result-precheck-a01/precheck.json
.orchestration/dotfiles-T133-result-precheck-a01/report.md
.orchestration/dotfiles-T133-result-precheck-a01/result.txt
.orchestration/dotfiles-T133-result-precheck-a01/revise.yaml
.orchestration/dotfiles-T133-result-precheck-a01/sandbox.md
.orchestration/dotfiles-T133-result-precheck-a01/task.md
.orchestration/dotfiles-T133-result-precheck-a01/validation.md
.orchestration/dotfiles-T133-result-precheck-a02/task.md
scripts/orchestrator/dispatch.sh
scripts/orchestrator/result-precheck.sh
tests/unit/test_result_precheck.py
exit=0

```

## The default precheck run and its unit-test baseline (before the final proof)

The default `unit-test` check runs `make unit-test`, which fails inside the Claude seat's sandbox; the identical failing set fails on a pristine `origin/main` worktree in the same sandbox, and none is in this task's modules. Every other check of the run passed.

```text
$ scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a02
head=38b9178b7a25df16ac26e01110294edfdd30d61c
result-precheck: unit-test exit 2
result-precheck: render-check exit 0
result-precheck: format exit 0
result-precheck: shellcheck exit 0
result-precheck: secrets exit 0
precheck=c11752e33a26762cd9d8509adabd350d7c40a3697db3d52681c49fcb7fddbbed
exit=1
$ cat precheck.json (this run)
{
  "head": "38b9178b7a25df16ac26e01110294edfdd30d61c",
  "tree": "d3ffbc80008e5502ceb6952ddf186e99667b7d97",
  "generated_at": "2026-10-18T07:51:00Z",
  "checks": [
    {
      "name": "unit-test",
      "ok": false,
      "exit": 2,
      "output_sha256": "8bfa0b26aa81cec015e98b131f64e82565440a144e06d17efde3a5e33c7a3d66"
    },
    {
      "name": "render-check",
      "ok": true,
      "exit": 0,
      "output_sha256": "3cc07aa4e482b20772e8ba404d3c0d9e338adcd0cd2d4ff6edf14de8bf23db93"
    },
    {
      "name": "format",
      "ok": true,
      "exit": 0,
      "output_sha256": "f170e34f5d9c464c7dd7be27fb8f87bb26969019903d50b6636103c97a779796"
    },
    {
      "name": "shellcheck",
      "ok": true,
      "exit": 0,
      "output_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "name": "secrets",
      "ok": true,
      "exit": 0,
      "output_sha256": "ec427b4abbf24ab3958dd1498e28cc76113d99c85519521cfc6951635053f42a"
    },
    {
      "name": "local-review",
      "ok": null,
      "deferred": "orchestrator"
    }
  ],
  "selectors": []
}

base=99a4a80f5a5b32a70cf7eb4f4d0db5a02d113841
make unit-test exit=2
removed=0
$ compare the sorted FAIL/ERROR names of this head and origin/main
head: Ran 1187 tests in 557.345s FAILED (failures=189, errors=107, skipped=2) 
base: Ran 1176 tests in 428.876s FAILED (failures=189, errors=107, skipped=2) 
head failing names: 296; base failing names: 296
cmp: identical failing sets
in this task's modules: 0
```

## Whole-blob scanning: tracked files the masker already flags

Item 5 scans the whole content of every blob a pushed commit adds or changes. This measures, over a printable-text copy of every tracked file, which ones the repository masker flags today: a push touching any of them is refused once the hooks are live (P1-7).

```text
$ bash flag-scan.sh <worktree root>
masker exit=0
files scanned: 5485
files with matches: 13
45 match(es) in tests/unit/test_validate_agent_assets.py
38 match(es) in tests/install/common/setup.bats
16 match(es) in scripts/validate-agent-assets.py
4 match(es) in tests/unit/test_claude_settings_merge.py
3 match(es) in tests/install/ubuntu/client/default_shell.bats
3 match(es) in tests/unit/test_generate_agent_configs.py
3 match(es) in vendor/compactiondb/tests/test_redaction.py
2 match(es) in plans/005-make-runtime-health-and-verification-truthful.md
2 match(es) in tests/unit/test_permgate.py
2 match(es) in vendor/compactiondb/tests/test_migration.py
1 match(es) in home/dot_config/powerlevel10k/p10k.zsh
1 match(es) in tests/unit/test_herdr_agents.py
1 match(es) in vendor/compactiondb/validate.py
exit=0
```

## The final proof on 38b9178b (the committed record)

```text
$ scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a02 --tests tests.unit.test_result_precheck tests.unit.test_orchestrator_tools
head=38b9178b7a25df16ac26e01110294edfdd30d61c
result-precheck: unit-test exit 0
result-precheck: render-check exit 0
result-precheck: format exit 0
result-precheck: shellcheck exit 0
result-precheck: secrets exit 0
precheck=67de44ecedc495308e539fae5a48518ff081b2208bac6ca02288d7d20dd6eed8
exit=0
$ grep -E '^Ran |^(OK|FAILED)' precheck-unit-test.log
Ran 67 tests in 80.187s
OK
$ cat precheck.json
{
  "head": "38b9178b7a25df16ac26e01110294edfdd30d61c",
  "tree": "d3ffbc80008e5502ceb6952ddf186e99667b7d97",
  "generated_at": "2026-10-18T08:05:58Z",
  "checks": [
    {
      "name": "unit-test",
      "ok": true,
      "exit": 0,
      "output_sha256": "eb072bd947ebdd4159f5bc11d11e9362080787990377d0043b2bb57781141db7"
    },
    {
      "name": "render-check",
      "ok": true,
      "exit": 0,
      "output_sha256": "3cc07aa4e482b20772e8ba404d3c0d9e338adcd0cd2d4ff6edf14de8bf23db93"
    },
    {
      "name": "format",
      "ok": true,
      "exit": 0,
      "output_sha256": "f170e34f5d9c464c7dd7be27fb8f87bb26969019903d50b6636103c97a779796"
    },
    {
      "name": "shellcheck",
      "ok": true,
      "exit": 0,
      "output_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "name": "secrets",
      "ok": true,
      "exit": 0,
      "output_sha256": "ec427b4abbf24ab3958dd1498e28cc76113d99c85519521cfc6951635053f42a"
    },
    {
      "name": "local-review",
      "ok": null,
      "deferred": "orchestrator"
    }
  ],
  "selectors": []
}
$ cat result.txt
AGMSG-RESULT v1 task_id=dotfiles-T133-result-precheck-a02 status=ready_for_review head=38b9178b7a25df16ac26e01110294edfdd30d61c precheck=67de44ecedc495308e539fae5a48518ff081b2208bac6ca02288d7d20dd6eed8 task_copy=fda18e21e738bb222a50ebd29be302fa009fd1a2822b660311abe81aa1397e61 report=.orchestration/dotfiles-T133-result-precheck-a02/report.md validation=.orchestration/dotfiles-T133-result-precheck-a02/validation.md sandbox=.orchestration/dotfiles-T133-result-precheck-a02/sandbox.md learning=.orchestration/dotfiles-T133-result-precheck-a02/learning.md
```

## The helper scripts

`red-a02.sh`:

```bash
#!/usr/bin/env bash
# Run the current regression tests against a reviewed production head in a temporary detached checkout.
set -u
head=$1
shift
base="$(mktemp -d "${TMPDIR%/}/red-a02.XXXXXX")/wt"
git worktree add --detach -q "${base}" "${head}"
cp -- tests/unit/test_result_precheck.py "${base}/tests/unit/test_result_precheck.py"
echo "checkout=$(git -C "${base}" rev-parse HEAD) test_source_sha256=$(shasum -a 256 tests/unit/test_result_precheck.py | cut -d' ' -f1)"
tests=()
for t in "$@"; do tests+=("tests.unit.test_result_precheck.ResultPrecheckTest.${t}"); done
(cd -- "${base}" && uv run python -m unittest "${tests[@]}" -v) > "${base}.log" 2>&1
echo "unittest exit=$?"
grep -E ' \.\.\. |^(FAIL|ERROR):|^AssertionError|^Ran |^(OK|FAILED)' "${base}.log"
git worktree remove --force "${base}"
echo "removed=$?"
```

`a02-long.sh`:

```bash
#!/usr/bin/env bash
# The default precheck on this head, then the full unit suite on a pristine origin/main checkout, and the comparison.
set -u
out=$1
task=dotfiles-T133-result-precheck-a02
evidence=".orchestration/${task}"
mkdir -p "${out}"
{
    echo "\$ scripts/orchestrator/result-precheck.sh ${task}"
    echo "head=$(git rev-parse HEAD)"
    bash scripts/orchestrator/result-precheck.sh "${task}"
    echo "exit=$?"
} > "${out}/default.out" 2>&1
cp -p "${evidence}/precheck.json" "${evidence}/precheck-unit-test.log" "${out}/"
base="$(mktemp -d "${TMPDIR%/}/a02-base.XXXXXX")/wt"
git worktree add --detach -q "${base}" origin/main
{
    echo "base=$(git -C "${base}" rev-parse HEAD)"
    (cd -- "${base}" && make unit-test > "${out}/base-unit.log" 2>&1)
    echo "make unit-test exit=$?"
    git worktree remove --force "${base}"
    echo "removed=$?"
} > "${out}/base.out" 2>&1
pattern='^(FAIL|ERROR): test_[A-Za-z0-9_]+ \([A-Za-z0-9_.]+\)'
grep -oE "${pattern}" "${out}/precheck-unit-test.log" | sort > "${out}/head-fails.txt"
grep -oE "${pattern}" "${out}/base-unit.log" | sort > "${out}/base-fails.txt"
{
    echo "head: $(grep -E '^Ran |^(OK|FAILED)' "${out}/precheck-unit-test.log" | tr '\n' ' ')"
    echo "base: $(grep -E '^Ran |^(OK|FAILED)' "${out}/base-unit.log" | tr '\n' ' ')"
    echo "head failing names: $(wc -l < "${out}/head-fails.txt" | tr -d ' '); base failing names: $(wc -l < "${out}/base-fails.txt" | tr -d ' ')"
    if cmp -s "${out}/head-fails.txt" "${out}/base-fails.txt"; then echo "cmp: identical failing sets"; else echo "cmp: the sets differ"; diff "${out}/base-fails.txt" "${out}/head-fails.txt"; fi
    echo "in this task's modules: $(grep -c 'test_result_precheck\|test_orchestrator_tools' "${out}/head-fails.txt")"
} > "${out}/compare.out" 2>&1
cat "${out}/default.out" "${out}/base.out" "${out}/compare.out"
```

`a02-checks.sh`:

```bash
#!/usr/bin/env bash
# T133 a02's Check commands (all but the precheck runs), each verbatim with its exit status, from the worktree root.
set -u
out=$1
grep() { /usr/bin/grep "$@"; }
run() {
    printf '$ %s\n' "$*"
    "$@" 2>&1
    printf 'exit=%s\n\n' "$?"
}
scripts=(scripts/orchestrator/result-precheck.sh .githooks/pre-commit .githooks/pre-push scripts/orchestrator/dispatch.sh)
run git rev-parse HEAD origin/main
run make render-check
run shellcheck -x "${scripts[@]}"
run shfmt -d -i 4 -sr "${scripts[@]}"
printf "\$ git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs shfmt -i 4 -sr -d\n"
git ls-files -- ':(glob)install/**/*.sh' ':(glob)scripts/**/*.sh' | xargs shfmt -i 4 -sr -d 2>&1
printf 'exit=%s\n\n' "$?"
printf "\$ git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check\n"
git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check 2>&1
printf 'exit=%s\n\n' "$?"
printf "\$ git ls-files -z '*.md' | xargs -0 prettier --check\n"
git ls-files -z '*.md' | xargs -0 prettier --check 2>&1
printf 'exit=%s\n\n' "$?"
printf '$ make format > format.txt 2>&1   (this head)\n'
make format > "${out}/format.txt" 2>&1
printf 'exit=%s\n' "$?"
grep -E '^--- ' "${out}/format.txt" | sed 's/^--- //; s/\.orig$//' | sort -u > "${out}/format-head.txt"
base="$(mktemp -d "${TMPDIR%/}/a02-fmt.XXXXXX")/wt"
git worktree add --detach -q "${base}" origin/main
printf '$ (cd <origin/main worktree> && make format > format-base.txt 2>&1)\n'
(cd -- "${base}" && make format > "${out}/format-base.txt" 2>&1)
printf 'exit=%s\n' "$?"
git worktree remove --force "${base}"
grep -E '^--- ' "${out}/format-base.txt" | sed 's/^--- //; s/\.orig$//' | sort -u > "${out}/format-base-files.txt"
printf '$ the files shfmt flags: this head %s, origin/main %s\n' "$(wc -l < "${out}/format-head.txt" | tr -d ' ')" "$(wc -l < "${out}/format-base-files.txt" | tr -d ' ')"
cmp -s "${out}/format-head.txt" "${out}/format-base-files.txt" && echo 'cmp: identical flagged sets' || echo 'cmp: the sets differ'
cat "${out}/format-head.txt"
printf '\n'
run uv run python -m unittest tests.unit.test_result_precheck tests.unit.test_orchestrator_tools -v
run git diff --numstat origin/main...HEAD
printf '$ git diff --numstat origin/main...HEAD -- scripts .githooks | sum; -- tests | sum\n'
git diff --numstat origin/main...HEAD -- scripts .githooks | awk '{a+=$1+$2} END {print "outside tests and .orchestration:", a}'
git diff --numstat origin/main...HEAD -- tests | awk '{a+=$1+$2} END {print "under tests:", a}'
printf '\n'
run git diff --name-only origin/main...HEAD
```

`flag-scan.sh`:

```bash
#!/usr/bin/env bash
# Measure how many tracked files the repository masker would flag if a push scanned their whole content.
set -u
root=$1
masker="${root}/scripts/validate-agent-assets.py"
t="$(mktemp -d "${TMPDIR%/}/flag.XXXXXX")"
cd -- "${root}"
git ls-files -z | while IFS= read -r -d '' f; do
    [[ -f ${f} && ! -L ${f} ]] || continue
    mkdir -p -- "${t}/$(dirname -- "${f}")"
    LC_ALL=C tr -c '\11\12\40-\176' '\12' < "${f}" > "${t}/${f}"
done
cd -- "${t}"
find . -type f -print0 | xargs -0 uv run --no-project --with pyyaml "${masker}" --mask-secrets > "${t}.out" 2> "${t}.err"
echo "masker exit=$?"
tail -2 "${t}.err"
echo "files scanned: $(grep -c '^masked' "${t}.out")"
echo "files with matches: $(grep -vc '^masked 0 match' "${t}.out")"
grep -v '^masked 0 match' "${t}.out" | sed 's/^masked //' | sort -k1,1nr | head -40
rm -rf -- "${t}" "${t}.out" "${t}.err"
```

