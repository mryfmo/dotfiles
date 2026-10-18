---
task_id: dotfiles-T133-result-precheck-a03
round: 1
code_head: 1ac3a1a674df895b541aff3a2fac8709b934abc9
base: de3b73cc4f8874a30be6adc47a0f07575869d0df
---

# Validation

Every block is the command's own output, in the seat's sandbox (sandbox.md), on the code head above unless a block names another commit.

## Task copy and the reset bookkeeping

```
$ shasum -a 256 .orchestration/dotfiles-T133-result-precheck-a03/task.md
f416aee0dd314b3dbb33db7ef71da78f261f06bb822ed684adc685ad77034e39  .orchestration/dotfiles-T133-result-precheck-a03/task.md
$ git show --stat --format=%H HEAD -- .orchestration/dotfiles-T133-result-precheck-a01/task.md .orchestration/dotfiles-T133-result-precheck-a02/task.md .orchestration/dotfiles-T133-result-precheck-a03/task.md
1ac3a1a674df895b541aff3a2fac8709b934abc9

 .../dotfiles-T133-result-precheck-a01/task.md      | 109 ------------
 .../dotfiles-T133-result-precheck-a02/task.md      | 160 ------------------
 .../dotfiles-T133-result-precheck-a03/task.md      | 186 +++++++++++++++++++++
 3 files changed, 186 insertions(+), 269 deletions(-)
```

## Red: the four new regressions against 4ed1b27a

```
production=4ed1b27a666ba939db76051243143a7d7ed2aaa5 test_source_sha256=edd94951d8abb4639c6463b0b8b04a83ea010e3e3b92736dad0ab9540ff7fef5 (tests/unit/test_result_precheck.py at 1ac3a1a6)
$ uv run python -m unittest tests.unit.test_result_precheck -k test_pre_push_scans_each_blob_on_its_own_and_keeps_json_decoding -k test_pre_push_fails_closed_on_an_undecodable_blob -k test_dispatch_acceptance_check_requires_a_result_newer_than_the_latest_revise -k test_pre_push_reports_home_path_rewrites_only_under_orchestration
exit=1
FAIL: test_dispatch_acceptance_check_requires_a_result_newer_than_the_latest_revise
AssertionError: Tuples differ: (0, True, False) != (1, False, True)
FAIL: test_pre_push_fails_closed_on_an_undecodable_blob
AssertionError: 0 != 1 : To /private/tmp/claude-501/tmp0tmdhxb0/origin.git
FAIL: test_pre_push_reports_home_path_rewrites_only_under_orchestration
AssertionError: 1 != 0
FAIL: test_pre_push_scans_each_blob_on_its_own_and_keeps_json_decoding
AssertionError: 0 != 1 : To /private/tmp/claude-501/tmptw2yzhrm/origin.git
Ran 4 tests in 2.710s
FAILED (failures=4)
removed=0
```

## Red: the three retained revise-1 regressions against 9cd5514a

```
production=9cd5514a790f6993136f5e74aaf3f3afa31b23d8 test_source_sha256=edd94951d8abb4639c6463b0b8b04a83ea010e3e3b92736dad0ab9540ff7fef5 (tests/unit/test_result_precheck.py at 1ac3a1a6)
$ uv run python -m unittest tests.unit.test_result_precheck -k test_pre_push_scans_each_blob_on_its_own_boundary -k test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan -k test_previous_head_proof_requires_an_executed_failing_test
exit=1
FAIL: test_pre_push_scans_each_blob_on_its_own_boundary
AssertionError: 0 != 1 : To /private/tmp/claude-501/tmplmvz49zk/origin.git
FAIL: test_previous_head_proof_requires_an_executed_failing_test (name='test_always')
AssertionError: 0 != 1 : result-precheck: unit-test exit 0
FAIL: test_previous_head_proof_requires_an_executed_failing_test (name='test_helper')
AssertionError: 0 != 1 : result-precheck: unit-test exit 0
FAIL: test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan (encoding='utf-16')
AssertionError: 0 != 1 : secrets: 0 match(es)
FAIL: test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan (encoding='utf-16-le')
AssertionError: 0 != 1 : secrets: 0 match(es)
FAIL: test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan (encoding='utf-16-be')
AssertionError: 0 != 1 : secrets: 0 match(es)
Ran 3 tests in 3.753s
FAILED (failures=6)
removed=0
```

## The Check commands

```
code head=1ac3a1a674df895b541aff3a2fac8709b934abc9 origin/main=3e41e36abc949acd7e6b4859c1a22df9e665c8d4 merge-base=de3b73cc4f8874a30be6adc47a0f07575869d0df
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
63 files already formatted
exit=0
$ git ls-files -z '*.md' | xargs -0 prettier --check
All matched files use Prettier code style!
exit=0
$ uv run python -m unittest tests.unit.test_result_precheck tests.unit.test_orchestrator_tools -v
test_dispatch_acceptance_check_requires_a_result_newer_than_the_latest_revise (tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_acceptance_check_requires_a_result_newer_than_the_latest_revise) ... ok
test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required (tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_refuses_an_accepted_acceptance_without_a_matching_precheck_when_required) ... ok
test_dispatch_rejects_malformed_checks_and_missing_requested_selectors (tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_rejects_malformed_checks_and_missing_requested_selectors) ... ok
test_pre_commit_hook_checks_the_staged_blobs_not_the_working_tree (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_commit_hook_checks_the_staged_blobs_not_the_working_tree) ... ok
test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_commit_hook_stops_a_commit_on_a_format_or_shellcheck_failure) ... ok
test_pre_push_fails_closed_on_an_undecodable_blob (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_fails_closed_on_an_undecodable_blob) ... ok
test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_hook_stops_a_push_whose_diff_matches_the_secret_pattern) ... ok
test_pre_push_reports_home_path_rewrites_only_under_orchestration (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_reports_home_path_rewrites_only_under_orchestration) ... ok
test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_scans_binary_marked_blobs_in_every_pushed_commit) ... ok
test_pre_push_scans_each_blob_on_its_own_and_keeps_json_decoding (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_scans_each_blob_on_its_own_and_keeps_json_decoding) ... ok
test_pre_push_scans_each_blob_on_its_own_boundary (tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_scans_each_blob_on_its_own_boundary) ... ok
test_precheck_exits_1_and_records_ok_false_for_each_failing_check (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_exits_1_and_records_ok_false_for_each_failing_check) ... ok
test_precheck_records_failed_commands_as_not_ok (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_records_failed_commands_as_not_ok) ... ok
test_precheck_records_the_local_review_as_deferred_by_default (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_records_the_local_review_as_deferred_by_default) ... ok
test_precheck_secrets_mode_counts_and_never_prints_the_match (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_secrets_mode_counts_and_never_prints_the_match) ... ok
test_precheck_selector_proof_requires_red_on_previous_head_and_green_on_head (tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_selector_proof_requires_red_on_previous_head_and_green_on_head) ... ok
test_previous_head_proof_requires_an_executed_failing_test (tests.unit.test_result_precheck.ResultPrecheckTest.test_previous_head_proof_requires_an_executed_failing_test) ... ok
test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan (tests.unit.test_result_precheck.ResultPrecheckTest.test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan) ... ok
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
test_front_matter_keeps_and_validates_the_replans_object (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_front_matter_keeps_and_validates_the_replans_object) ... ok
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
Ran 75 tests in 132.592s
OK
exit=0
```

## The default precheck run and the sandbox baseline

```
head make format exit=2
$ scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a03
result-precheck: unit-test exit 2
result-precheck: render-check exit 0
result-precheck: format exit 0
result-precheck: shellcheck exit 0
result-precheck: secrets exit 0
precheck=c566d0a6e5e9ae51857a5e819ac1a0031014dae1a79062c8ba2240d2e958ca8e
exit=1
base=3e41e36abc949acd7e6b4859c1a22df9e665c8d4
base make unit-test exit=2
base make format exit=2
removed=0
head: Ran 1213 tests in 608.062s FAILED (failures=194, errors=111, skipped=2) 
base: Ran 1207 tests in 529.230s FAILED (failures=194, errors=111, skipped=2) 
failing names: head 305, base 305
cmp unit: identical failing sets
in this task's modules: 0
shfmt diff files: head 12, base 12
cmp format: identical file lists
```

The twelve files `shfmt --diff .` lists on both sides:

```
--- .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh.orig
--- .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh.orig
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh.orig
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh.orig
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh.orig
--- home/dot_claude/hooks/executable_project-map-reload.sh.orig
--- tests/install/macos/common/brew.bats.orig
```

## The final proof

```
$ scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a03 --tests tests.unit.test_result_precheck tests.unit.test_orchestrator_tools --previous-head 4ed1b27a666ba939db76051243143a7d7ed2aaa5 --check <each of the four revise.yaml selectors>
code head=1ac3a1a674df895b541aff3a2fac8709b934abc9
result-precheck: unit-test exit 0
result-precheck: render-check exit 0
result-precheck: format exit 0
result-precheck: shellcheck exit 0
result-precheck: secrets exit 0
result-precheck: tests/unit/test_result_precheck.py::test_pre_push_scans_each_blob_on_its_own_and_keeps_json_decoding previous head exit 1, this head exit 0
result-precheck: tests/unit/test_result_precheck.py::test_pre_push_fails_closed_on_an_undecodable_blob previous head exit 1, this head exit 0
result-precheck: tests/unit/test_result_precheck.py::test_dispatch_acceptance_check_requires_a_result_newer_than_the_latest_revise previous head exit 1, this head exit 0
result-precheck: tests/unit/test_result_precheck.py::test_pre_push_reports_home_path_rewrites_only_under_orchestration previous head exit 1, this head exit 0
precheck=6701ae4f035dc4aec568cc37bec44028b217018c9f0825be496e2ff439c71589
exit=0
$ the record: checks, selectors and each previous-head summary
head 1ac3a1a674df895b541aff3a2fac8709b934abc9
unit-test True
render-check True
format True
shellcheck True
secrets True
local-review None
test_pre_push_scans_each_blob_on_its_own_and_keeps_json_decoding True 1 0
test_pre_push_fails_closed_on_an_undecodable_blob True 1 0
test_dispatch_acceptance_check_requires_a_result_newer_than_the_latest_revise True 1 0
test_pre_push_reports_home_path_rewrites_only_under_orchestration True 1 0
precheck-selector-1-previous.log: Ran 1 test in 1.754s FAILED (failures=1) 
precheck-selector-2-previous.log: Ran 1 test in 0.593s FAILED (failures=1) 
precheck-selector-3-previous.log: Ran 1 test in 2.799s FAILED (failures=1) 
precheck-selector-4-previous.log: Ran 1 test in 0.541s FAILED (failures=1) 
$ shasum -a 256 .orchestration/dotfiles-T133-result-precheck-a03/precheck.json
6701ae4f035dc4aec568cc37bec44028b217018c9f0825be496e2ff439c71589  .orchestration/dotfiles-T133-result-precheck-a03/precheck.json
$ cat .orchestration/dotfiles-T133-result-precheck-a03/result.txt
AGMSG-RESULT v1 task_id=dotfiles-T133-result-precheck-a03 status=ready_for_review head=1ac3a1a674df895b541aff3a2fac8709b934abc9 precheck=6701ae4f035dc4aec568cc37bec44028b217018c9f0825be496e2ff439c71589 task_copy=f416aee0dd314b3dbb33db7ef71da78f261f06bb822ed684adc685ad77034e39 report=.orchestration/dotfiles-T133-result-precheck-a03/report.md validation=.orchestration/dotfiles-T133-result-precheck-a03/validation.md sandbox=.orchestration/dotfiles-T133-result-precheck-a03/sandbox.md learning=.orchestration/dotfiles-T133-result-precheck-a03/learning.md
```

## Caps and the changed-file inventory

```
$ git diff --numstat origin/main...HEAD (outside .orchestration/)
13	0	.githooks/pre-commit
36	0	.githooks/pre-push
80	1	scripts/orchestrator/dispatch.sh
289	0	scripts/orchestrator/result-precheck.sh
520	0	tests/unit/test_result_precheck.py
outside tests/ and .orchestration/: 419 (cap 420); tests/: 520 (cap 520)
$ git diff --name-status origin/main...HEAD
A	.githooks/pre-commit
A	.githooks/pre-push
A	.orchestration/dotfiles-T133-result-precheck-a01/learning.md
A	.orchestration/dotfiles-T133-result-precheck-a01/precheck-format.log
A	.orchestration/dotfiles-T133-result-precheck-a01/precheck-render-check.log
A	.orchestration/dotfiles-T133-result-precheck-a01/precheck-secrets.log
A	.orchestration/dotfiles-T133-result-precheck-a01/precheck-selector-1-head.log
A	.orchestration/dotfiles-T133-result-precheck-a01/precheck-selector-1-previous.log
A	.orchestration/dotfiles-T133-result-precheck-a01/precheck-shellcheck.log
A	.orchestration/dotfiles-T133-result-precheck-a01/precheck-unit-test.log
A	.orchestration/dotfiles-T133-result-precheck-a01/precheck.json
A	.orchestration/dotfiles-T133-result-precheck-a01/report.md
A	.orchestration/dotfiles-T133-result-precheck-a01/result.txt
A	.orchestration/dotfiles-T133-result-precheck-a01/revise.yaml
A	.orchestration/dotfiles-T133-result-precheck-a01/sandbox.md
A	.orchestration/dotfiles-T133-result-precheck-a01/validation.md
A	.orchestration/dotfiles-T133-result-precheck-a02/learning.md
A	.orchestration/dotfiles-T133-result-precheck-a02/precheck-format.log
A	.orchestration/dotfiles-T133-result-precheck-a02/precheck-render-check.log
A	.orchestration/dotfiles-T133-result-precheck-a02/precheck-secrets.log
A	.orchestration/dotfiles-T133-result-precheck-a02/precheck-selector-1-head.log
A	.orchestration/dotfiles-T133-result-precheck-a02/precheck-selector-1-previous.log
A	.orchestration/dotfiles-T133-result-precheck-a02/precheck-selector-2-head.log
A	.orchestration/dotfiles-T133-result-precheck-a02/precheck-selector-2-previous.log
A	.orchestration/dotfiles-T133-result-precheck-a02/precheck-selector-3-head.log
A	.orchestration/dotfiles-T133-result-precheck-a02/precheck-selector-3-previous.log
A	.orchestration/dotfiles-T133-result-precheck-a02/precheck-shellcheck.log
A	.orchestration/dotfiles-T133-result-precheck-a02/precheck-unit-test.log
A	.orchestration/dotfiles-T133-result-precheck-a02/precheck.json
A	.orchestration/dotfiles-T133-result-precheck-a02/report.md
A	.orchestration/dotfiles-T133-result-precheck-a02/result.txt
A	.orchestration/dotfiles-T133-result-precheck-a02/revise.yaml
A	.orchestration/dotfiles-T133-result-precheck-a02/sandbox.md
A	.orchestration/dotfiles-T133-result-precheck-a02/validation.md
A	.orchestration/dotfiles-T133-result-precheck-a03/task.md
M	scripts/orchestrator/dispatch.sh
A	scripts/orchestrator/result-precheck.sh
A	tests/unit/test_result_precheck.py
```

## One --blob scan, timed, and pre-commit unchanged since 4ed1b27a

```
$ git diff --stat 4ed1b27a666ba939db76051243143a7d7ed2aaa5 HEAD -- .githooks/pre-commit
(empty: unchanged)
$ time bash scripts/orchestrator/result-precheck.sh --blob HEAD:scripts/orchestrator/dispatch.sh  (three runs)
secrets: 0 match(es)
exit=0 seconds=0.21
secrets: 0 match(es)
exit=0 seconds=0.21
secrets: 0 match(es)
exit=0 seconds=0.19
```

## CompactionDB memory

```
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T133 P1-5 a03 (S1 redesign of a02): result-precheck.sh scan_one feeds each blob unchanged … the task latest status=revise.'
67366379-780e-431d-8764-2b1f46cf95dc
exit=0
```
