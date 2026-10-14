---
task_id: dotfiles-T128-orchestrator-tools-a06
seat: claude-standard-dot-a003
fix_commit: dd2f3af1
---

# Validation: dotfiles-T128-orchestrator-tools-a06

## 1. Task copy and base

```text
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a06.md .orchestration/dotfiles-T128-orchestrator-tools-a06/task.md .orchestration/dotfiles-T128-orchestrator-tools-a05/task.md
b10dfb47257f00dd0ad05c11a977514b948fdebc7238af76a118a1ad80e2127c  <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a06.md
b10dfb47257f00dd0ad05c11a977514b948fdebc7238af76a118a1ad80e2127c  .orchestration/dotfiles-T128-orchestrator-tools-a06/task.md
6b238e5a958ed5124d997e129391a4e10cc2b61b7b9f57052e8b463b4f549f23  .orchestration/dotfiles-T128-orchestrator-tools-a05/task.md
$ git log --oneline -3
dd2f3af1 fix(orchestrator): orch-gate.sh builds the gate's environment with env -i and runs it with -I -P
a06c874e chore(orchestration): dotfiles-T128-orchestrator-tools-a05 PR-B revise-1 evidence and the amended task copy
ced110dd fix(orchestrator): orch-gate.sh pins the interpreter in this checkout and restores the review worktree on any failure
$ git merge-base --is-ancestor a06c874e HEAD && echo "a06c874e and its commits stay"
a06c874e and its commits stay
$ git diff --name-only a06c874e HEAD
scripts/orchestrator/orch-gate.sh
tests/unit/test_orchestrator_tools.py
```

- The TASK's `task_sha256` is `b10dfb47257f00dd0ad05c11a977514b948fdebc7238af76a118a1ad80e2127c`, and both a06 files hash to it.
- The a05 copy is unchanged at amendment 1's `6b238e5a…`.
- The `--name-only` list has no `.orchestration/dotfiles-T128-orchestrator-tools-a05/` path.

## 2. What an `env -i` child adds by itself, and gh under the allowlist

```text
$ env -i PATH=/usr/bin:/bin /bin/bash -c /usr/bin/env | cut -d= -f1
PATH
PWD
SHLVL
_
$ env -i PATH=/usr/bin:/bin A=1 <the uv python> -I -P -c "import os, sys; print(sorted(os.environ), sys.version.split()[0], sys.flags.safe_path)"
['A', 'LC_CTYPE', 'PATH', '__CF_USER_TEXT_ENCODING'] 3.15.0 True
$ env -i PATH="$PATH" HOME="$HOME" NO_COLOR=1 gh repo view --json nameWithOwner -q .nameWithOwner   # the gate's first gh call, in this worktree
mryfmo/dotfiles
rc 0
```

- **bash:** with only `PATH` given, it exports `PWD`, `SHLVL` and `_` itself. The test stub is bash, so the test allows exactly those three names beside the allowlist.
- **Python:** this Python (3.15, from mise, on macOS) adds `LC_CTYPE` (PEP 538 locale coercion) and `__CF_USER_TEXT_ENCODING` to `os.environ`. A Python stub could therefore not record the environment it was given.
- **`-P`:** `sys.flags.safe_path` is `True` under `-I -P`.
- **gh:** with only `PATH`, `HOME` and the `NO_COLOR` the gate sets, `gh` resolves the repository the way the gate's `pr_base_errors` asks.

## 3. Tests, lint, size (the Validation clause's commands)

```text
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record) ... ok
test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit) ... ok
test_boundary_commits_pushes_and_queues_the_pr (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_boundary_commits_pushes_and_queues_the_pr) ... ok
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
test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history) ... ok
test_dispatch_records_the_sent_line_with_its_read_marker (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_records_the_sent_line_with_its_read_marker) ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file) ... ok
test_dispatch_refuses_a_line_without_a_task_id (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_line_without_a_task_id) ... ok
test_dispatch_refuses_a_malformed_record_block_before_sending (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_malformed_record_block_before_sending) ... ok
test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields) ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line) ... ok
test_dispatch_refuses_an_unwritable_record_before_sending (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_an_unwritable_record_before_sending) ... ok
test_dispatch_refuses_malformed_lines (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_refuses_malformed_lines) ... ok
test_ff_main_keeps_local_edits_across_the_fast_forward (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_ff_main_keeps_local_edits_across_the_fast_forward) ... ok
test_fill_sweep_fills_only_notice_annotations_and_success_statuses (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_fills_only_notice_annotations_and_success_statuses) ... ok
test_fill_sweep_ignores_a_disposition_reply_from_another_login (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_ignores_a_disposition_reply_from_another_login) ... ok
test_fill_sweep_leaves_a_badged_review_body_a_gap (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_leaves_a_badged_review_body_a_gap) ... ok
test_fill_sweep_refuses_a_not_applicable_without_evidence (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_fill_sweep_refuses_a_not_applicable_without_evidence) ... ok
test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt) ... ok
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
Ran 39 tests in 16.350s

OK
tools rc 0
```

```text
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_regime_counters.py -v
test_a_600_row_history_counts_fully_through_the_storage_facade (tests.unit.test_regime_counters.RegimeCountersTest.test_a_600_row_history_counts_fully_through_the_storage_facade) ... ok
test_a_forged_acceptance_record_changes_no_count (tests.unit.test_regime_counters.RegimeCountersTest.test_a_forged_acceptance_record_changes_no_count) ... ok
test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity (tests.unit.test_regime_counters.RegimeCountersTest.test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity) ... ok
test_a_status_in_free_text_counts_nothing (tests.unit.test_regime_counters.RegimeCountersTest.test_a_status_in_free_text_counts_nothing) ... ok
test_a_store_at_another_schema_revision_is_unreadable (tests.unit.test_regime_counters.RegimeCountersTest.test_a_store_at_another_schema_revision_is_unreadable) ... ok
test_a_tab_separated_task_counts_as_an_amendment (tests.unit.test_regime_counters.RegimeCountersTest.test_a_tab_separated_task_counts_as_an_amendment) ... ok
test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id) ... ok
test_bot_heads_are_unknown_when_gh_fails (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_when_gh_fails) ... ok
test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit) ... ok
test_bot_heads_are_unknown_without_a_first_result_head (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_without_a_first_result_head) ... ok
test_bot_heads_read_every_page_through_gh_api (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_read_every_page_through_gh_api) ... ok
test_every_line_names_its_source (tests.unit.test_regime_counters.RegimeCountersTest.test_every_line_names_its_source) ... ok
test_every_result_counts_as_a_revise_whatever_its_status (tests.unit.test_regime_counters.RegimeCountersTest.test_every_result_counts_as_a_revise_whatever_its_status) ... ok
test_history_only_never_calls_gh (tests.unit.test_regime_counters.RegimeCountersTest.test_history_only_never_calls_gh) ... ok
test_list_tasks_prints_each_task_id_once (tests.unit.test_regime_counters.RegimeCountersTest.test_list_tasks_prints_each_task_id_once) ... ok
test_only_p0_and_p1_heads_after_the_first_result_head_count (tests.unit.test_regime_counters.RegimeCountersTest.test_only_p0_and_p1_heads_after_the_first_result_head_count) ... ok
test_s1_candidates_are_bot_title_classes_seen_three_times (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_candidates_are_bot_title_classes_seen_three_times) ... ok
test_s1_ignores_a_record_whose_ledger_rows_are_not_id_class_objects (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_ignores_a_record_whose_ledger_rows_are_not_id_class_objects) ... ok
test_s1_quotes_a_title_with_shell_metacharacters (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_quotes_a_title_with_shell_metacharacters) ... ok
test_s1_reads_the_ledger_classes_of_the_acceptance_record (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_reads_the_ledger_classes_of_the_acceptance_record) ... ok
test_t118_fixture_counts_revises_from_results (tests.unit.test_regime_counters.RegimeCountersTest.test_t118_fixture_counts_revises_from_results) ... ok
test_t119_fixture_counts_every_task_after_the_first_as_an_amendment (tests.unit.test_regime_counters.RegimeCountersTest.test_t119_fixture_counts_every_task_after_the_first_as_an_amendment) ... ok
test_t124_wave1_fixture_counts_bot_heads_after_the_first_result_head (tests.unit.test_regime_counters.RegimeCountersTest.test_t124_wave1_fixture_counts_bot_heads_after_the_first_result_head) ... ok
test_the_boundary_check_never_passes_a_test_seam (tests.unit.test_regime_counters.RegimeCountersTest.test_the_boundary_check_never_passes_a_test_seam) ... ok
test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one (tests.unit.test_regime_counters.RegimeCountersTest.test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one) ... ok
test_thresholds_are_inv6_constants (tests.unit.test_regime_counters.RegimeCountersTest.test_thresholds_are_inv6_constants) ... ok
test_usage_errors_exit_2 (tests.unit.test_regime_counters.RegimeCountersTest.test_usage_errors_exit_2) ... ok
test_v0_fixture_counts_bot_heads_after_the_first_result_head (tests.unit.test_regime_counters.RegimeCountersTest.test_v0_fixture_counts_bot_heads_after_the_first_result_head) ... ok

----------------------------------------------------------------------
Ran 28 tests in 4.298s

OK
counters rc 0
```

```text
$ shellcheck --version | head -2; shellcheck scripts/orchestrator/*.sh; ruff check / ruff format --check tests/unit/test_orchestrator_tools.py; shfmt --indent 4 --space-redirects -d scripts/orchestrator/orch-gate.sh
ShellCheck - shell script analysis tool
version: 0.11.0
shellcheck rc 0
All checks passed!
1 file already formatted
shfmt rc 0
$ git diff --numstat origin/main...HEAD   (outside .orchestration)
124	0	scripts/orchestrator/acceptance-front-matter.py
77	0	scripts/orchestrator/orch-gate.sh
222	2	tests/unit/test_orchestrator_tools.py
files 3 added_non_test 201 added_test 222
```

INV-2 holds: 3 of 15 files, 201 of 500 added lines outside tests, 222 of 1000 under tests. The merge base with `origin/main` is `7d58d6cd`, so the three-dot diff shows PR #350 only. The tests ran with `UV_OFFLINE=1` from the uv cache, because the sandbox has no pypi; CI runs them online.

## 4. Mutation proofs (`scratchpad/mutate-a06.py`)

The method:

- edit one span of `orch-gate.sh` at `dd2f3af1`;
- run `test_orch_gate_runs_the_gate_under_an_explicit_environment` by its full dotted name;
- count a kill only on an AssertionError;
- restore with `git checkout --`.

```text
KILLED E1 the a05 code (inherit the shell, unset three names) :: AssertionError: Lists differ: ['ACC[34 chars]', 'AUDIT_EVIDENCE', 'HOME', 'PATH', 'PR_FEEDB[67 chars] '_'] != ['ACC[34 chars]', 'AGMSG_SCRIPTS', 'AGMSG_SPAWNED', 'AI_AGENT[2255 chars]oxy']
KILLED E2 no PYTHONSAFEPATH=1 :: AssertionError: Lists differ: ['ACC[89 chars]NCE', 'PWD', 'PYTHONSAFEPATH', 'REVIEW_EVIDENCE', 'SHLVL', '_'] != ['ACC[89 chars]NCE', 'PWD', 'REVIEW_EVIDENCE', 'SHLVL', '_']
KILLED E3 no -P :: AssertionError: Lists differ: ['-I', '-P'] != ['-I', '/private/tmp/claude-501/tmphxrvipv_/repo/[27 chars].py']
KILLED E4 no HOME :: AssertionError: Lists differ: ['ACC[51 chars]E', 'HOME', 'PATH', 'PR_FEEDBACK_EVIDENCE', 'P[50 chars] '_'] != ['ACC[51 chars]E', 'PATH', 'PR_FEEDBACK_EVIDENCE', 'PWD', 'PY[42 chars] '_']
KILLED E5 one inherited name passed through (PYTHONPATH) :: AssertionError: Lists differ: ['ACC[103 chars]PYTHONSAFEPATH', 'REVIEW_EVIDENCE', 'SHLVL', '_'] != ['ACC[103 chars]PYTHONPATH', 'PYTHONSAFEPATH', 'REVIEW_EVIDENCE', 'SHLVL', '_']
kills 5/5
clean
```

- E1 is the a05 code at `a06c874e`: it inherits this shell and unsets three names.
- The failure messages list variable names only, never values. E1's list shows the test environment's own names; the values do not appear.
