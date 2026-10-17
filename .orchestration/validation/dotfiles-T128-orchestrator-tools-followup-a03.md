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

## 5. CI and the Bot on `57d3577c`, the final head (main-checkout copy only)

The fix head was pushed and `@codex review` asked at 2026-10-16T21:43Z (issue comment 6225256851).

```text
$ gh pr checks 374 --repo mryfmo/dotfiles --watch --interval 30; gh pr checks 374 --repo mryfmo/dotfiles; gh pr view 374 --repo mryfmo/dotfiles --json headRefOid,mergeStateStatus
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	2s	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/38971232744/job/117209825806	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38971232744/job/117209826124	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38971232744/job/117209825845	
public-bootstrap (macos-14, client)	pass	10m38s	https://github.com/mryfmo/dotfiles/actions/runs/38971232744/job/117209825896	
public-bootstrap (ubuntu-24.04, client)	pass	10m25s	https://github.com/mryfmo/dotfiles/actions/runs/38971232744/job/117209825602	
public-bootstrap (ubuntu-24.04, server)	pass	7m17s	https://github.com/mryfmo/dotfiles/actions/runs/38971232744/job/117209825758	
test (macos-14, client)	pass	7m2s	https://github.com/mryfmo/dotfiles/actions/runs/38971232740/job/117209825693	
test (ubuntu-24.04, client)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/38971232740/job/117209825712	
test (ubuntu-24.04, server)	pass	5m31s	https://github.com/mryfmo/dotfiles/actions/runs/38971232740/job/117209825382	
test (ubuntu-26.04, client)	pass	9m11s	https://github.com/mryfmo/dotfiles/actions/runs/38971232740/job/117209825795	
validate	pass	2m0s	https://github.com/mryfmo/dotfiles/actions/runs/38971232759/job/117209825144	
ci-final rc=0
{"headRefOid":"57d3577ca780248f573fd26c4fa460e2b5e2d510","mergeStateStatus":"BLOCKED"}
```

```text
$ gh api repos/mryfmo/dotfiles/pulls/374/reviews --jq '.[]|"\(.id) \(.commit_id[0:8]) \(.state) \(.submitted_at)"'
5545290170 aeb4a0fb COMMENTED 2026-10-16T08:51:20Z
5554058212 57d3577c COMMENTED 2026-10-16T21:45:04Z
$ gh api repos/mryfmo/dotfiles/pulls/374/comments --jq '.[]|"\(.id) \(.commit_id[0:8]) \(.path):\(.line) <title>"'
4292675906 aeb4a0fb scripts/orchestrator/dispatch.sh:null Isolate uv from the caller's project
4299651928 57d3577c scripts/orchestrator/dispatch.sh:182 Run uv outside the caller-controlled directory
```

The code re-review of `57d3577c` left one P1, thread 4299651928: with `--no-project`, uv still runs an interpreter that a `.python-version` (for example `./pwn`) or a virtual environment in the caller's directory names, before the task file is validated. The PR's one fix round is spent, so it stays open for the operator's decision (`bot_rounds=2`). The fix it names is one line: run both uv forms from the trusted script root (`cd "${root}"` in a subshell, or `uv --directory "${root}"`), or pin a trusted interpreter first. The module's own uv stub already models `.python-version` execution, so a test can plant one in the caller's directory.

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

## 7. CI and the Bot on `9df6b0c7`, the final head (main-checkout copy only)

```text
$ gh pr checks 374; gh pr view 374 --json headRefOid,mergeStateStatus
CodeRabbit: pass
GitGuardian Security Checks: pass
private-bootstrap (macos-14, client): pass
private-bootstrap (ubuntu-24.04, client): pass
private-bootstrap (ubuntu-24.04, server): pass
public-bootstrap (macos-14, client): pass
public-bootstrap (ubuntu-24.04, client): pass
public-bootstrap (ubuntu-24.04, server): pass
test (macos-14, client): pass
test (ubuntu-24.04, client): pass
test (ubuntu-24.04, server): pass
test (ubuntu-26.04, client): pass
validate: pass
{"headRefOid":"9df6b0c7594cef7f42e9a43faa3e08d0f035e329","mergeStateStatus":"BLOCKED"}
```

```text
$ the code_review state of the Bot's summary; gh api …/pulls/374/reviews; …/pulls/374/comments; …/issues/374/reactions
"code_review":{"commit_sha":"9df6b0c7594cef7f42e9a43faa3e08d0f035e329","has_any_findings":false,"has_unresolved_findings":false,"status":"completed"}
5545290170 aeb4a0fb COMMENTED 2026-10-16T08:51:20Z
5554058212 57d3577c COMMENTED 2026-10-16T21:45:04Z
4292675906 aeb4a0fb scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate uv from the caller's project**
4299651928 57d3577c scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Run uv outside the caller-controlled directory**
chatgpt-codex-connector[bot] +1
```

The Bot's code re-review of `9df6b0c7`, asked with `@codex review`, completed with no finding and a 👍 reaction: no new review and no new thread. Threads 4292675906 and 4299651928 are on earlier heads (their `line` is now null).

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

## 9. CI and the Bot on `6ae8cf75`, the final head (main-checkout copy only)

```text
$ gh pr checks 374; gh pr view 374 --json headRefOid,mergeStateStatus
CodeRabbit: pass
GitGuardian Security Checks: pass
private-bootstrap (macos-14, client): pass
private-bootstrap (ubuntu-24.04, client): pass
private-bootstrap (ubuntu-24.04, server): pass
public-bootstrap (macos-14, client): pass
public-bootstrap (ubuntu-24.04, client): pass
public-bootstrap (ubuntu-24.04, server): pass
test (macos-14, client): pass
test (ubuntu-24.04, client): pass
test (ubuntu-24.04, server): pass
test (ubuntu-26.04, client): pass
validate: pass
{"headRefOid":"6ae8cf75df74bb54eb3b724ea7c94e16b70759ef","mergeStateStatus":"UNKNOWN"}
```

```text
$ the code_review state of the Bot's summary; gh api …/pulls/374/reviews; …/pulls/374/comments; …/issues/374/reactions
"code_review":{"commit_sha":"6ae8cf75df74bb54eb3b724ea7c94e16b70759ef","has_any_findings":true,"has_unresolved_findings":true,"status":"completed"}
5545290170 aeb4a0fb COMMENTED 2026-10-16T08:51:20Z
5554058212 57d3577c COMMENTED 2026-10-16T21:45:04Z
5554562648 6ae8cf75 COMMENTED 2026-10-16T23:04:34Z
4292675906 aeb4a0fb scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate uv from the caller's project**
4299651928 57d3577c scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Run uv outside the caller-controlled directory**
4300102967 6ae8cf75 scripts/orchestrator/dispatch.sh:197 **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate the PyYAML probe from inherited Python paths**
```

The Bot's code re-review of `6ae8cf75` (review 5554562648) left one P1, thread 4300102967 at `dispatch.sh:197`, "Isolate the PyYAML probe from inherited Python paths": the probe `uvr python -c 'import yaml'` runs without `-I`, so an inherited `PYTHONPATH` naming a caller-writable directory holding `yaml.py` executes that module before the task is validated; the later `python -I` calls do not cover the probe. The fix it names is one flag (`python -I -c 'import yaml'`), or stripping `PYTHONPATH` and the other `PYTHON*` overrides with the `env -u` list. This round's scope said nothing else, so it stays open for the orchestrator's decision.

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

## 11. CI and the Bot on `9cf65c02`, the final head (main-checkout copy only)

```text
$ gh pr checks 374; gh pr view 374 --json headRefOid,mergeStateStatus
CodeRabbit: pass
GitGuardian Security Checks: pass
private-bootstrap (macos-14, client): pass
private-bootstrap (ubuntu-24.04, client): pass
private-bootstrap (ubuntu-24.04, server): pass
public-bootstrap (macos-14, client): pass
public-bootstrap (ubuntu-24.04, client): pass
public-bootstrap (ubuntu-24.04, server): pass
test (macos-14, client): pass
test (ubuntu-24.04, client): pass
test (ubuntu-24.04, server): pass
test (ubuntu-26.04, client): pass
validate: pass
{"headRefOid":"9cf65c0299645e30e54419668ba523eff9c4897e","mergeStateStatus":"BEHIND"}
```

```text
$ the code_review state of the Bot's summary; gh api …/pulls/374/reviews; …/pulls/374/comments; …/issues/374/reactions; the body of any thread on the head
"code_review":{"commit_sha":"9cf65c0299645e30e54419668ba523eff9c4897e","has_any_findings":false,"has_unresolved_findings":false,"status":"completed"}
5545290170 aeb4a0fb COMMENTED 2026-10-16T08:51:20Z
5554058212 57d3577c COMMENTED 2026-10-16T21:45:04Z
5554562648 6ae8cf75 COMMENTED 2026-10-16T23:04:34Z
4292675906 aeb4a0fb scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate uv from the caller's project**
4299651928 57d3577c scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Run uv outside the caller-controlled directory**
4300102967 6ae8cf75 scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate the PyYAML probe from inherited Python paths**
chatgpt-codex-connector[bot] +1
```

The Bot's code re-review of `9cf65c02`, asked with `@codex review`, completed with no finding and a 👍 reaction: no new review and no new thread. `mergeStateStatus` is `BEHIND` because `main` moved after the branch was cut (`1d418126`); the orchestrator's update-branch takes the new base.

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

## 13. CI and the Bot on `9f6c5ceb`, the final head (main-checkout copy only)

```text
$ gh pr checks 374; gh pr view 374 --json headRefOid,mergeStateStatus
CodeRabbit: pass
GitGuardian Security Checks: pass
private-bootstrap (macos-14, client): pass
private-bootstrap (ubuntu-24.04, client): pass
private-bootstrap (ubuntu-24.04, server): pass
public-bootstrap (macos-14, client): pass
public-bootstrap (ubuntu-24.04, client): pass
public-bootstrap (ubuntu-24.04, server): pass
test (macos-14, client): pass
test (ubuntu-24.04, client): pass
test (ubuntu-24.04, server): pass
test (ubuntu-26.04, client): pass
validate: pass
{"headRefOid":"9f6c5cebd23592793f3ad5247a20753aff26f388","mergeStateStatus":"BLOCKED"}
```

```text
$ the code_review state of the Bot's summary; gh api …/pulls/374/reviews; …/pulls/374/comments; …/issues/374/reactions; the body of the thread on the head
"code_review":{"commit_sha":"9f6c5cebd23592793f3ad5247a20753aff26f388","has_any_findings":true,"has_unresolved_findings":true,"status":"completed"}
5545290170 aeb4a0fb COMMENTED 2026-10-16T08:51:20Z
5554058212 57d3577c COMMENTED 2026-10-16T21:45:04Z
5554562648 6ae8cf75 COMMENTED 2026-10-16T23:04:34Z
5555371628 9f6c5ceb COMMENTED 2026-10-17T01:32:04Z
4292675906 aeb4a0fb scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate uv from the caller's project**
4299651928 57d3577c scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Run uv outside the caller-controlled directory**
4300102967 6ae8cf75 scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate the PyYAML probe from inherited Python paths**
4300738707 9f6c5ceb scripts/orchestrator/dispatch.sh:199 **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Ignore caller-controlled uv configuration**
--- 4300738707
**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Ignore caller-controlled uv configuration**

When the caller can set `HOME` to a writable directory, both uv invocations discover `$HOME/.config/uv/uv.toml` because the clean environment preserves that value and neither command uses `--no-config`. I confirmed with uv 0.7.22 that a user config containing an `index-url` redirects the `pyyaml` fetch; a malicious index can therefore supply code that executes at the subsequent `import yaml` before the task is validated. `uv help run` documents that `--no-config` avoids configuration files normally discovered in user configuration directories, so add it to both command forms or pin a trusted HOME. This leaves the task's environment-input residual ineffective.

AGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/9f6c5cebd23592793f3ad5247a20753aff26f388/AGENTS.md#L78-L78)

Useful? React with 👍 / 👎.

<!-- codex-code-review-finding:v1 -->
```

The Bot's code re-review of `9f6c5ceb` (review 5555371628) left one P1, thread 4300738707 at `dispatch.sh:199`, "Ignore caller-controlled uv configuration": the allowlist keeps `HOME`, and neither uv form passes `--no-config`, so a `HOME` the caller controls supplies `$HOME/.config/uv/uv.toml`, whose `index-url` can redirect the `pyyaml` fetch to code that runs at `import yaml` before the task is validated. The fix it names is `--no-config` on both uv forms, or a pinned trusted `HOME`. This round's scope said nothing else, so it stays open for the orchestrator's decision.

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

## 15. Round 6 supplement (`e2b7d2cc`): offline only, and the test asserts identity

The orchestrator's supplement of 2026-10-17T01:53:21Z, the operator's correction (six single-source patches were not the re-plan S1 requires), replaced §14's specification before its Bot wait; that wait was stopped. Two changes, nothing else:

1. **Offline only.** Both uv forms are `uv run --no-config --no-project --offline --python <pinned> --with pyyaml`; the non-offline fallback is gone. PyYAML comes from the pinned `UV_CACHE_DIR` that the validator recipes warm, and when the probe cannot import it, the script prints `dispatch: PyYAML is not in the uv cache <home>/.cache/uv; run make validate-agent-assets to warm it` and exits 2, never fetching. The checker test's new cold-cache case (the fake fails the probe while `uv-cold` exists) asserts exit 2, the message, one uv call and nothing sent. M18 (the fallback put back) is killed by it.
2. **Positive identity.** The fake uv is now a Python script, which adds no variable of its own, recording each call's argv, directory and full environment as JSON. `test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state` keeps every planted source in its one case and asserts, for both calls, the exact environment `{PATH, HOME, UV_CACHE_DIR}` plus `LANG`/`LC_ALL` when set and the `AGMSG_*` variables given, with their values. It also asserts the directory (the root) and the exact argv: the probe is `run --no-config --no-project --offline --python <python> --with pyyaml python -I -c "import yaml"`; the brief parse has the same head, `-c`, the brief and the task path. `<python>` is resolved as the script resolves it (`mise which python3` under `env -i` at the root, else `python3` on PATH). The one key dropped before the comparison is `__CF_USER_TEXT_ENCODING`, which macOS adds to every process after `env -i` too; it is no input the script passes. Any other variable, flag or value now fails the test by construction.

```text
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
b291ba85f89d46877f74969d4e33ce994ff875f83454df58dbd8037a7d745da7  .orchestration/dotfiles-T128-orchestrator-tools-followup-a03/task.md
$ git log --oneline -1; git merge-base HEAD origin/main
e2b7d2cc fix(orchestrator): dispatch.sh runs uv offline only and the test asserts each uv 
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
Ran 56 tests in 43.550s
OK

$ shellcheck scripts/orchestrator/dispatch.sh; shfmt --indent 4 --space-redirects -d scripts/orchestrator/dispatch.sh
(rc=0)
$ ruff check tests/unit/test_orchestrator_tools.py; ruff format --check tests/unit/test_orchestrator_tools.py
All checks passed!
1 file already formatted
(rc=0)

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
123	26	scripts/orchestrator/dispatch.sh
235	10	tests/unit/test_orchestrator_tools.py
files: 2; changed lines outside tests/ and .orchestration/: 149; added under tests/: 235
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
M11 the probe without -I (the Bot's P1 4300102967) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M12 no pinned --python -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M13 PYTHONPATH let through the allowlist -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M14 the root found under the inherited environment (audit:ef74eae:1) -> killed by test_dispatch_resolves_its_root_without_inherited_git_variables, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M15 no --no-config (the Bot's P1 4300738707) -> killed by test_dispatch_refuses_a_task_file_failing_the_checker, test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M16 the inherited HOME kept -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M17 the uv cache not pinned -> killed by test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state
M18 the network fallback kept for a cold cache -> killed by test_dispatch_refuses_a_task_file_failing_the_checker
file restored (git diff --quiet HEAD): True
```

## 16. CI and the Bot on `5ef0ef3b`, the final head (main-checkout copy only)

```text
$ gh pr checks 374; gh pr view 374 --json headRefOid,mergeStateStatus
CodeRabbit: pass
GitGuardian Security Checks: pass
private-bootstrap (macos-14, client): pass
private-bootstrap (ubuntu-24.04, client): pass
private-bootstrap (ubuntu-24.04, server): pass
public-bootstrap (macos-14, client): pass
public-bootstrap (ubuntu-24.04, client): pass
public-bootstrap (ubuntu-24.04, server): pass
test (macos-14, client): pass
test (ubuntu-24.04, client): pass
test (ubuntu-24.04, server): pass
test (ubuntu-26.04, client): pass
validate: pass
{"headRefOid":"5ef0ef3bb7d9d89d51bfa2056029fde54fc825d9","mergeStateStatus":"BLOCKED"}
```

```text
$ the code_review state of the Bot's summary; gh api …/pulls/374/reviews; …/pulls/374/comments; …/issues/374/reactions; the body of the thread on the head
"code_review":{"commit_sha":"5ef0ef3bb7d9d89d51bfa2056029fde54fc825d9","has_any_findings":true,"has_unresolved_findings":true,"status":"completed"}
5545290170 aeb4a0fb COMMENTED 2026-10-16T08:51:20Z
5554058212 57d3577c COMMENTED 2026-10-16T21:45:04Z
5554562648 6ae8cf75 COMMENTED 2026-10-16T23:04:34Z
5555371628 9f6c5ceb COMMENTED 2026-10-17T01:32:04Z
5555541928 5ef0ef3b COMMENTED 2026-10-17T02:21:25Z
4292675906 aeb4a0fb scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate uv from the caller's project**
4299651928 57d3577c scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Run uv outside the caller-controlled directory**
4300102967 6ae8cf75 scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Isolate the PyYAML probe from inherited Python paths**
4300738707 9f6c5ceb scripts/orchestrator/dispatch.sh:null **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Ignore caller-controlled uv configuration**
4300891366 5ef0ef3b tests/unit/test_orchestrator_tools.py:8 **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Warm PyYAML before exercising the real uv wrapper**
--- 4300891366
**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Warm PyYAML before exercising the real uv wrapper**

On a clean unit-test runner, this case cannot use the stated “reachable index”: `dispatch.sh` now always invokes `uv run --offline --with pyyaml`, and `uv help run` defines `--offline` as “Disable network access.” The required Unit test workflow disables uv cache restoration and proceeds directly to `make unit-test`, which does not warm PyYAML, so the new cases exit 2 at the probe rather than reaching their assertions; this is reproducible with an empty cache. Warm the cache in the unit-test setup or make the fixture provision PyYAML independently.

Useful? React with 👍 / 👎.

<!-- codex-code-review-finding:v1 -->
```

The Bot's code re-review of `5ef0ef3b` (review 5555541928) left one P1, thread 4300891366 at `tests/unit/test_orchestrator_tools.py:8`, "Warm PyYAML before exercising the real uv wrapper": `dispatch.sh` now always runs `uv run --offline`, the Unit test workflow restores no uv cache, and `make unit-test` warms no PyYAML, so on a clean runner the new cases would exit 2 at the probe. The Unit test run of `5ef0ef3b` shows otherwise for CI as it stands:

```text
$ gh run list --repo mryfmo/dotfiles --commit 5ef0ef3bb7d9d89d51bfa2056029fde54fc825d9 --json databaseId,name,conclusion
38994408082 Agent assets success
38994408067 Unit test success
38994408075 Snippet install success
$ gh run view 38994408067 --repo mryfmo/dotfiles --log | grep -E 'test_dispatch_(runs_uv|refuses_a_task_file|resolves_its_root)[a-z_]* .*\.\.\. ' | sort | uniq -c
   4 test_dispatch_refuses_a_task_file_failing_the_checker) ... ok
   4 test_dispatch_resolves_its_root_without_inherited_git_variables) ... ok
   4 test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state) ... ok
$ … | grep -E 'Ran [0-9]+ tests' ; … | grep -E 'enable-cache'
Ran 1147 tests in 207.860s
Ran 1147 tests in 215.078s
  enable-cache: false
```

All three tests ran and passed in all four matrix jobs, with no uv cache restored: PyYAML reaches the cache earlier in the same job, through a module that runs `uv run --with pyyaml` before `test_orchestrator_tools` in unittest's order. The finding is therefore a real order dependency, not a failure today: run alone on a fresh runner, the cases would exit 2. The proposed fix, within the test module, is a warm step in `checker_dispatch` (`uv run --with pyyaml python -c "import yaml"` with `HOME` and `UV_CACHE_DIR` as the script pins them), or a skip with the reason when the cache cannot be warmed. It stays open for the orchestrator's decision.
