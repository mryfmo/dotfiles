---
task_id: dotfiles-T128-orchestrator-tools-followup-a03
seat: claude-standard-dot-a003
commit: 766c1491
---

# Validation: dotfiles-T128-orchestrator-tools-followup-a03

## 1. Task copy, premises, tests, linters and size

The task copy hashes to the TASK line's `task_sha256`. The task file on `origin/main` (`1d418126`) hashes to `5a741e63…`, the pair-confirmed text before the `bot_rounds` change the task's last section records; the dispatched file is the main checkout's, which the Worker Playbook says to copy. The three premises replay with the task's outputs (1, 0, 52); on HEAD the same counts are 0, 2 and 54.

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
766c1491 fix(orchestrator): dispatch.sh refuses a task file that fails the checker and rea
1d418126
$ the three premises (origin/main)
1
0
52
$ the same counts on HEAD
0
2
54

$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
(rc=0)
test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record ... ok
test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit ... ok
test_boundary_commits_pushes_and_queues_the_pr ... ok
test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path ... ok
test_boundary_deletes_a_name_with_glob_characters_literally ... ok
test_boundary_keeps_a_name_with_a_newline_one_path ... ok
test_boundary_stops_before_commit_when_the_validator_fails ... ok
test_bus_read_closes_a_task_on_any_non_revise_acceptance ... ok
test_bus_read_ignores_closers_between_other_endpoints ... ok
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_bus_read_skips_and_counts_malformed_rows ... ok
test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash ... ok
test_design_keydiff_names_the_changed_invariant ... ok
test_dispatch_line_grammar_table ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_reads_a_bounded_history_window ... ok
test_dispatch_record_path_tokenizes_and_locks ... ok
test_dispatch_records_the_sent_line_with_its_read_marker ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_a_line_without_a_task_id ... ok
test_dispatch_refuses_a_malformed_record_block_before_sending ... ok
test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields ... ok
test_dispatch_refuses_a_task_file_failing_the_checker ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line ... ok
test_dispatch_refuses_an_unwritable_record_before_sending ... ok
test_dispatch_refuses_malformed_lines ... ok
test_ff_main_keeps_a_local_deletion_across_the_fast_forward ... ok
test_ff_main_keeps_local_edits_across_the_fast_forward ... ok
test_fill_sweep_fills_only_a_commented_review ... ok
test_fill_sweep_fills_only_notice_annotations_and_success_statuses ... ok
test_fill_sweep_ignores_a_disposition_reply_from_another_login ... ok
test_fill_sweep_leaves_a_badged_review_body_a_gap ... ok
test_fill_sweep_quotes_the_url_form_evidence ... ok
test_fill_sweep_refuses_a_not_applicable_without_evidence ... ok
test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id ... ok
test_fill_sweep_sees_a_collision_after_the_discussion_r_strip ... ok
test_fill_sweep_selects_a_null_url_status_by_source_and_check ... ok
test_orch_audit_refuses_a_ledger_check_that_differs_from_head ... ok
test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt ... ok
test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap ... ok
test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules ... ok
test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout ... ok
test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree ... ok
test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration ... ok
test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves ... ok
test_orch_gate_restores_the_review_worktree_when_setup_fails ... ok
test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree ... ok
test_orch_gate_runs_the_gate_under_an_explicit_environment ... ok
test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs ... ok
test_replay_propagates_the_command_status ... ok
test_three_repeat_prints_body_matches_and_states_a_capped_memory_count ... ok
test_three_repeat_prints_the_records_search_line ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout ... ok
Ran 54 tests in 46.271s
OK

$ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
(rc=0)
$ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
All checks passed!
1 file already formatted
(rc=0)

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
81	23	scripts/orchestrator/dispatch.sh
107	11	tests/unit/test_orchestrator_tools.py
files: 2; changed lines outside tests/ and .orchestration/: 104; added under tests/: 107
```

## 2. Mutation proofs

Each mutant of `scripts/orchestrator/dispatch.sh` runs against the two new tests, and the file is restored after each (`a03-mutate.py`, a scratch script outside the repository).

```text
M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker
M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
file restored (git diff --quiet HEAD): True
```

## 3. The two existing tests the change touches

The task keeps the 52 tests, and item 1b removes the cap refusal and `BUS_READ_LIMIT`. Two of the 52 asserted exactly those, so each changes as little as the removal needs:

- `test_dispatch_records_the_sent_line_with_its_read_marker`: the history limit it asserts is `200`, the new default, instead of `100000`.
- `test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history`: its last case (a read that reaches `BUS_READ_LIMIT` is refused) is removed with the refusal, and the test is renamed `test_dispatch_record_path_tokenizes_and_locks`, since it no longer refuses a capped history. Its other cases stay as they were.

Neither change weakens a check that still exists; the bounded window is covered by the new `test_dispatch_reads_a_bounded_history_window`.
