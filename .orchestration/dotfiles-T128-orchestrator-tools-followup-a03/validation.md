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

## 4. The Bot's fix round (`c8e813ea`): `--no-project`

The Bot's code review of `aeb4a0fb` (review 5545290170) left one P1, thread 4292675906 at `scripts/orchestrator/dispatch.sh:181`: without `--no-project`, both `uv run` forms discover and sync a `pyproject.toml` in the caller's directory before the task file is checked, so a build backend there could run. Its security review of the same head completed with no finding. `c8e813ea` adds `--no-project` to both forms. The checker test now sends the review brief from a directory whose `pyproject.toml` depends on a package that does not exist, and pins the probe as `run --no-project --offline --with pyyaml python -c import yaml`. Mutant M8 drops `--no-project`; the send is then refused because the brief parse cannot run, so the test fails on the exit code, not only on the probe string.

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
c8e813ea fix(orchestrator): dispatch.sh runs uv with --no-project (the Bot's P1 4292675906
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
Ran 54 tests in 41.307s
OK

$ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
(rc=0)
$ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
All checks passed!
1 file already formatted
(rc=0)

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
82	23	scripts/orchestrator/dispatch.sh
114	11	tests/unit/test_orchestrator_tools.py
files: 2; changed lines outside tests/ and .orchestration/: 105; added under tests/: 114
```

```text
M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker
M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
M8 uv without --no-project (the Bot's P1) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
file restored (git diff --quiet HEAD): True
```

## 6. Revise round 2 (`8adf74bb`): uv runs from the trusted root

(§5 is the main-checkout copy's: CI and the Bot on `57d3577c`.) The Bot's re-review of `57d3577c` left P1 4299651928: with `--no-project`, uv still lets a `.python-version` or a virtual environment in the caller's directory choose the interpreter. The operator's decision D-P1-374 A gave this PR one more fix round. `8adf74bb` runs both uv forms through `uvr`, a subshell that changes to the script's checkout root, and names the checker by the script directory's absolute path (`here`), since a relative `BASH_SOURCE` would no longer resolve from the root.

The check `test_dispatch_refuses_a_task_file_failing_the_checker` sends the review brief from a caller directory whose `.python-version` names an executable that touches a marker and exits 1. The marker never appears, and the fake uv records the repository root as the directory of every call. Mutant M9 drops the `cd`; the planted interpreter then runs, the brief parse fails, and the send is refused, so the test fails on the exit code.

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
8adf74bb fix(orchestrator): dispatch.sh runs uv from the trusted root (the Bot's P1 429965
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
Ran 54 tests in 39.296s
OK

$ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
(rc=0)
$ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
All checks passed!
1 file already formatted
(rc=0)

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
85	23	scripts/orchestrator/dispatch.sh
122	11	tests/unit/test_orchestrator_tools.py
files: 2; changed lines outside tests/ and .orchestration/: 108; added under tests/: 122
```

```text
M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker
M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
M8 uv without --no-project (the Bot's P1) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M9 uv run from the caller's directory (the Bot's P1 4299651928) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
file restored (git diff --quiet HEAD): True
```

## 8. Revise round 3 (`411c7d68`): a pinned interpreter, no inherited environment

(§7 is the main-checkout copy's: CI and the Bot on `9df6b0c7`.) The local review of `9df6b0c7` found a P1, `local:9df6b0c:1` at `dispatch.sh:183-185`: after the `cd` to the root, an inherited `VIRTUAL_ENV` still chose uv's interpreter, so a PR checkout's `.venv` could run during the probe. It is the third finding of one class, the interpreter chosen from caller state (`pyproject.toml`, `.python-version`, `VIRTUAL_ENV`), and the operator's decision D-S2-374-2 A gave one round that closes the class (C-57).

`411c7d68` names the interpreter on both uv forms with `--python`: `python3` as `mise which` answers it under `env -i` at the root, else `python3` on PATH, and a non-absolute answer refuses. Both forms run under `env -u VIRTUAL_ENV -u VIRTUAL_ENV_PROMPT -u CONDA_PREFIX` plus `-u` for every inherited `UV_*` variable, keeping `--no-project` and the `cd` to the root.

The checker test's setup moved into a helper, `checker_dispatch`, which the new test `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state` shares. That test sets, all at once, a caller `pyproject.toml` with an unresolvable dependency, a caller `.python-version` naming an executable, `VIRTUAL_ENV` and `CONDA_PREFIX` naming a caller `.venv` whose `python` is that executable, and `UV_PYTHON` naming it. It asserts that the executable never runs, that every uv call runs at the root and inherits no `VIRTUAL_ENV`, `CONDA_PREFIX` or `UV_*` variable (the fake uv records them), that both calls name one `--python` path other than the planted one, and that the send is recorded. The probe assertion in the checker test now expects `--python /<path>`. M10 to M12 are this round's mutants: the environment kept, only the non-`UV_*` variables stripped, and no `--python`.

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
411c7d68 fix(orchestrator): dispatch.sh runs uv on a pinned interpreter without the caller
1d418126
$ the three premises (origin/main)
1
0
52
$ the same counts on HEAD
0
2
55

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
test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state ... ok
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
Ran 55 tests in 40.016s
OK

$ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
(rc=0)
$ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
All checks passed!
1 file already formatted
(rc=0)

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
97	23	scripts/orchestrator/dispatch.sh
145	11	tests/unit/test_orchestrator_tools.py
files: 2; changed lines outside tests/ and .orchestration/: 120; added under tests/: 145
```

```text
M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
M8 uv without --no-project (the Bot's P1) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M9 uv run from the caller's directory (the Bot's P1 4299651928) -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M10 the inherited environment kept (local:9df6b0c:1) -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M11 only VIRTUAL_ENV stripped, the UV_* overrides kept -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M12 no pinned --python -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
file restored (git diff --quiet HEAD): True
```

## 10. Revise round 4 (`b18698d5`): an env -i allowlist and the probe with -I

(§9 is the main-checkout copy's: CI and the Bot on `6ae8cf75`.) The Bot's re-review of `6ae8cf75` left P1 4300102967 at `dispatch.sh:197`: the PyYAML probe ran `python -c 'import yaml'` without `-I`, so an inherited `PYTHONPATH` naming a caller-writable directory with a `yaml.py` would run that module before the task is validated. It is the fourth finding of the class, and the operator's decision D-S2-374-3 A gave one round that ends the class by an allowlist instead of a denylist.

`b18698d5` replaces round 3's `env -u` denylist with `env -i PATH=… HOME=…`, plus `LANG` and `LC_ALL` when set and every `AGMSG_*` variable, nothing else, for both uv forms; the probe runs `python -I -c 'import yaml'`. The pinned `--python`, `--no-project` and the `cd` to the root stay.

The test `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state` now plants every source at once: a caller `pyproject.toml`, a caller `.python-version`, `VIRTUAL_ENV` and `CONDA_PREFIX` naming a caller `.venv`, `UV_PYTHON`, and a `yaml.py` on `PYTHONPATH` that writes the marker file, plus `AGMSG_STORAGE_PATH`. The fake uv, which has the calls directory written into it since `env -i` drops `CALLS`, records the name of every variable it inherits. The test asserts that the marker never appears, that apart from the `AGMSG_*` names the fake sees only `PATH`, `HOME`, `LANG`, `LC_ALL` and what bash sets itself (`PWD`, `SHLVL`, `_`, `OLDPWD`), and that `PATH`, `HOME` and `AGMSG_STORAGE_PATH` arrive. The checker test's probe form now expects `-I`.

M10 (no `env -i`) and M13 (`PYTHONPATH` let through) are killed by the new assertions. M11 (the probe without `-I`) is killed only by the checker test's probe-form assertion, since under `env -i` no `PYTHONPATH` reaches the probe; `-I` is the second layer.

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
b18698d5 fix(orchestrator): dispatch.sh runs uv under an env -i allowlist and the PyYAML p
1d418126
$ the three premises (origin/main)
1
0
52
$ the same counts on HEAD
0
2
55

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
test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state ... ok
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
Ran 55 tests in 40.461s
OK

$ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
(rc=0)
$ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
All checks passed!
1 file already formatted
(rc=0)

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
101	23	scripts/orchestrator/dispatch.sh
153	11	tests/unit/test_orchestrator_tools.py
files: 2; changed lines outside tests/ and .orchestration/: 124; added under tests/: 153
```

```text
M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
M8 uv without --no-project (the Bot's P1) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M9 uv run from the caller's directory (the Bot's P1 4299651928) -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M10 the inherited environment kept (no env -i) -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M11 the probe without -I (the Bot's P1 4300102967) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M12 no pinned --python -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M13 PYTHONPATH let through the allowlist -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
file restored (git diff --quiet HEAD): True
```

## 12. Revise round 5 (`f77185dd`): the root found under the allowlisted environment

(§11 is the main-checkout copy's: CI and the Bot on `9cf65c02`.) The audit of `ef74eaea`, round 4's head after the orchestrator's update-branch, found `audit:ef74eae:1` (P1, `dispatch.sh:219`): `git -C <script dir> rev-parse --show-toplevel` ran under the inherited environment, so `GIT_DIR` or `GIT_WORK_TREE` redirected the root the checker then trusted. With an absolute task path, C6 found no design file under the redirected root and accepted a stale receipt. It is the fifth finding of the caller-state class, and the operator's decision D-S2-374-4 A gave one round. Its two P2s on the history window stay advisory (owner a04), with no change here.

`f77185dd` builds the `env -i` allowlist (`PATH`, `HOME`, `LANG` and `LC_ALL` when set, the `AGMSG_*` variables) first and runs the root discovery, the one `git` call the script makes, under it. The uv calls use the same array as before, and the header says so.

The new test `test_dispatch_resolves_its_root_without_inherited_git_variables` replaces the stub checker with one that emulates C6 and prints the root it is given: a task file whose design receipt `r1` is stale against `d.md` (`r2`) under the real root, and absent under another tree. It sends that task file by an absolute path with `GIT_DIR` and `GIT_WORK_TREE` naming a freshly initialised other repository, and asserts that the send is refused with the C6 line, that the root the checker prints and the `--root` in the uv log are the script's checkout, that the checker path is the one beside the script, and that nothing is sent and the record is unchanged. M14 (the root found under the inherited environment) lets the stale receipt pass and the line be sent, so the test fails on the exit code.

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
f77185dd fix(orchestrator): dispatch.sh finds its root under the allowlisted environment (
f7847616
$ the three premises (origin/main)
1
0
52
$ the same counts on HEAD
0
2
56

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
test_dispatch_resolves_its_root_without_inherited_git_variables ... ok
test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state ... ok
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
Ran 56 tests in 39.177s
OK

$ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
(rc=0)
$ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
All checks passed!
1 file already formatted
(rc=0)

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
105	25	scripts/orchestrator/dispatch.sh
187	10	tests/unit/test_orchestrator_tools.py
files: 2; changed lines outside tests/ and .orchestration/: 130; added under tests/: 187
```

```text
M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_resolves_its_root_without_inherited_git_variables, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
M8 uv without --no-project (the Bot's P1) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M9 uv run from the caller's directory (the Bot's P1 4299651928) -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M10 the inherited environment kept (no env -i) -> killed by test_dispatch_resolves_its_root_without_inherited_git_variables, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M11 the probe without -I (the Bot's P1 4300102967) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M12 no pinned --python -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M13 PYTHONPATH let through the allowlist -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M14 the root found under the inherited environment (audit:ef74eae:1) -> killed by test_dispatch_resolves_its_root_without_inherited_git_variables
file restored (git diff --quiet HEAD): True
```

## 14. Revise round 6 (`e09f14ca`): every input of the uv invocation named

(§13 is the main-checkout copy's: CI and the Bot on `9f6c5ceb`.) The Bot's re-review of `9f6c5ceb` left P1 4300738707 at `dispatch.sh:199`: the allowlist kept the inherited `HOME`, and neither uv form passed `--no-config`, so a caller-controlled `HOME` supplied `$HOME/.config/uv/uv.toml`, whose `index-url` could redirect the `pyyaml` fetch. It is the sixth finding of the class in six rounds, and the operator's decision D-S2-374-5 A made this the final round, naming every input of the invocation at once; a further finding of the class is advisory under a04.

`e09f14ca`:

- `HOME` is the passwd home of the script's owner: `stat -c %U` (GNU), else `stat -f %Su` (BSD), for the owner; the name is checked against `^[A-Za-z0-9._][A-Za-z0-9._-]*$`, then `~name` gives its passwd home, which must be absolute. An inherited `HOME` is never used.
- `UV_CACHE_DIR` is `<that home>/.cache/uv`.
- The `env -i` allowlist is `PATH`, `HOME`, `UV_CACHE_DIR`, `LANG` and `LC_ALL` when set, and the `AGMSG_*` variables. It is built before the root discovery, which runs under it, as do both uv forms; mise's interpreter lookup takes the same `HOME`.
- Both uv forms are `uv run --no-config --no-project [--offline] --python <pinned> --with pyyaml`, from the root; the probe runs `python -I`.

The test `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state` now plants every source at once: a caller `pyproject.toml`, a `.python-version`, `VIRTUAL_ENV` and `CONDA_PREFIX`, `UV_PYTHON`, a `yaml.py` on `PYTHONPATH`, `GIT_DIR` and `GIT_WORK_TREE` naming another tree, and a `HOME` holding a `uv.toml` whose `index-url` names a planted index, plus `AGMSG_STORAGE_PATH`. The fake uv records its argv, directory, variable names and its `HOME` and `UV_CACHE_DIR` values. The test asserts that nothing planted runs, that every uv call starts `run --no-config --no-project`, runs at the root and pins one `--python`, that the fake sees only the named variables, and that it sees `HOME` as the script owner's passwd home and `UV_CACHE_DIR` under it.

The mutation script now refuses a mutant that changes nothing: round 6 moved `--no-project` after `--no-config`, which had turned M8's old anchor into a no-op. M15 to M17 are this round's mutants: no `--no-config`, the inherited `HOME`, the cache not pinned.

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
e09f14ca fix(orchestrator): dispatch.sh names every input of its uv invocation (the Bot's 
f7847616
$ the three premises (origin/main)
1
0
52
$ the same counts on HEAD
0
2
56

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
test_dispatch_resolves_its_root_without_inherited_git_variables ... ok
test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state ... ok
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
Ran 56 tests in 42.655s
OK

$ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
(rc=0)
$ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
All checks passed!
1 file already formatted
(rc=0)

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
118	25	scripts/orchestrator/dispatch.sh
201	10	tests/unit/test_orchestrator_tools.py
files: 2; changed lines outside tests/ and .orchestration/: 143; added under tests/: 201
```

```text
M1 the dispatch.sh of origin/main -> killed by test_dispatch_reads_a_bounded_history_window, test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_resolves_its_root_without_inherited_git_variables, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M2 the brief found by a literal kind: review line -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M3 no duplicate-key refusal -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M4 the first fitting shift, not a unique one -> killed by test_dispatch_reads_a_bounded_history_window
M5 the newest new row taken as the send -> killed by test_dispatch_reads_a_bounded_history_window
M6 the whole bus read again -> killed by test_dispatch_reads_a_bounded_history_window
M7 no EXIT trap -> killed by test_dispatch_reads_a_bounded_history_window
M8 uv without --no-project (the Bot's P1) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M9 uv run from the caller's directory (the Bot's P1 4299651928) -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M10 the inherited environment kept (no env -i) -> killed by test_dispatch_resolves_its_root_without_inherited_git_variables, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M11 the probe without -I (the Bot's P1 4300102967) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
M12 no pinned --python -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M13 PYTHONPATH let through the allowlist -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M14 the root found under the inherited environment (audit:ef74eae:1) -> killed by test_dispatch_resolves_its_root_without_inherited_git_variables, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M15 no --no-config (the Bot's P1 4300738707) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M16 the inherited HOME kept -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M17 the uv cache not pinned -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
file restored (git diff --quiet HEAD): True
```
