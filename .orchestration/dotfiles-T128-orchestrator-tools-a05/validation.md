---
task_id: dotfiles-T128-orchestrator-tools-a05
seat: claude-standard-dot-a003
fix_commit: 608b38a28bd53249caf167e20a29b759010d2eed
---

# Validation: dotfiles-T128-orchestrator-tools-a05

## 1. Task copy and base

```text
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md .orchestration/dotfiles-T128-orchestrator-tools-a05/task.md
eaac8e4bd03cda154273097736944b3762581f872d5f5fbcdca67650b43236ea  <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a05.md
eaac8e4bd03cda154273097736944b3762581f872d5f5fbcdca67650b43236ea  .orchestration/dotfiles-T128-orchestrator-tools-a05/task.md
$ git log --oneline -3
608b38a2 fix(orchestrator): a05 items 7 to 9 (reply trust, badged bodies, fresh audit receipts)
7b574d32 chore(orchestration): dotfiles-T128-orchestrator-tools-a02 PR-A revise-round evidence
3544d195 fix(orchestrator): the TASK kind from the parsed tokens; fill only neutral annotations and statuses
$ git merge-base --is-ancestor 7b574d32 HEAD && echo "7b574d32 and its commits stay"
7b574d32 and its commits stay
$ git diff --name-only 7b574d32 HEAD
scripts/orchestrator/fill_sweep.py
scripts/orchestrator/orch-audit.sh
tests/unit/test_orchestrator_tools.py
```

The TASK's `task_sha256` is `eaac8e4bd03cda154273097736944b3762581f872d5f5fbcdca67650b43236ea`; both files hash to it. The a02 directory and its task copy are untouched (the `--name-only` list has no `.orchestration/dotfiles-T128-orchestrator-tools-a02/` path).

## 2. Tests, lint and size (the Validation clause's commands)

`UV_OFFLINE=1` is set because the seat sandbox cannot reach pypi; the design-keydiff test runs `uv run --with pyyaml` from the uv cache. CI runs online.

```text
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
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
test_replay_propagates_the_command_status (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_replay_propagates_the_command_status) ... ok
test_three_repeat_prints_body_matches_and_states_a_capped_memory_count (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_three_repeat_prints_body_matches_and_states_a_capped_memory_count) ... ok
test_three_repeat_prints_the_records_search_line (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_three_repeat_prints_the_records_search_line) ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout) ... ok

----------------------------------------------------------------------
Ran 30 tests in 14.971s

OK
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_regime_counters.py -v
test_a_600_row_history_counts_fully_through_the_storage_facade (tests.unit.test_regime_counters.RegimeCountersTest.test_a_600_row_history_counts_fully_through_the_storage_facade) ... ok
test_a_forged_acceptance_record_changes_no_count (tests.unit.test_regime_counters.RegimeCountersTest.test_a_forged_acceptance_record_changes_no_count) ... ok
test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity (tests.unit.test_regime_counters.RegimeCountersTest.test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity) ... ok
test_a_status_in_free_text_counts_nothing (tests.unit.test_regime_counters.RegimeCountersTest.test_a_status_in_free_text_counts_nothing) ... ok
test_a_store_at_another_schema_revision_is_unreadable (tests.unit.test_regime_counters.RegimeCountersTest.test_a_store_at_another_schema_revision_is_unreadable) ... ok
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
Ran 27 tests in 3.976s

OK
$ shellcheck --version | sed -n 2p; shellcheck scripts/orchestrator/*.sh && echo "shellcheck: no findings"
version: 0.11.0
shellcheck: no findings
$ (cd "$TMPDIR" && shfmt -i 4 -sr -d <worktree>/scripts/orchestrator/*.sh) && echo shfmt-ok
shfmt-ok
$ ruff format --config ruff.toml --check scripts/orchestrator/*.py tests/unit/test_orchestrator_tools.py; ruff check <same>
3 files already formatted
All checks passed!
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-orchestrator-tools-a02/autoskill.md
11	0	.orchestration/dotfiles-T128-orchestrator-tools-a02/learning.md
98	0	.orchestration/dotfiles-T128-orchestrator-tools-a02/report.md
34	0	.orchestration/dotfiles-T128-orchestrator-tools-a02/sandbox.md
146	0	.orchestration/dotfiles-T128-orchestrator-tools-a02/task.md
202	0	.orchestration/dotfiles-T128-orchestrator-tools-a02/validation.md
56	0	scripts/orchestrator/boundary.sh
12	8	scripts/orchestrator/bus-read.sh
39	0	scripts/orchestrator/codex-review.sh
40	0	scripts/orchestrator/design-keydiff.py
66	38	scripts/orchestrator/dispatch.sh
63	0	scripts/orchestrator/ff-main.sh
87	0	scripts/orchestrator/fill_sweep.py
82	0	scripts/orchestrator/orch-audit.sh
30	0	scripts/orchestrator/replay.sh
22	12	scripts/regime-counters.sh
445	7	tests/unit/test_orchestrator_tools.py
48	2	tests/unit/test_regime_counters.py
$ git diff --numstat origin/main...HEAD | awk <files outside .orchestration/, added outside and under tests/>
files outside .orchestration/: 12 added outside tests/: 497 added under tests/: 493
```

## 3. Mutation proofs

Each mutant changes one span of `608b38a2` (A2 two), runs its named test with the class in the path and `UV_OFFLINE=1`, and restores both files with `git checkout --`. The script is `mutate-a05.py` in the seat scratchpad. A mutant counts as killed only on an `AssertionError`, never on a load error.

```text
$ uv run --no-project python <scratchpad>/mutate-a05.py
F1 any login's reply counts: test_fill_sweep_ignores_a_disposition_reply_from_another_login -> killed | AssertionError: 'ignored-reply 21 mallory\n' not found in "items 3 filled 2 gaps 1\nGAP discussion_r22 review_comment None - Disposition
F2 ignored reply not printed: test_fill_sweep_ignores_a_disposition_reply_from_another_login -> killed | AssertionError: 'ignored-reply 21 mallory\n' not found in "items 3 filled 1 gaps 2\nGAP discussion_r11 review_comment P1 - P1\nGAP disc
F3 own-reply rule for any non-bot: test_fill_sweep_ignores_a_disposition_reply_from_another_login -> killed | AssertionError: Lists differ: ['discussion_r11', 'discussion_r22'] != ['discussion_r11']
F4 login grammar unchecked: test_fill_sweep_ignores_a_disposition_reply_from_another_login -> killed | AssertionError: 2 != 1 : ignored-reply 21 orch
F5 repeated option accepted: test_fill_sweep_ignores_a_disposition_reply_from_another_login -> killed | AssertionError: 2 != 1 : Traceback (most recent call last):
F6 badge ignored: test_fill_sweep_leaves_a_badged_review_body_a_gap -> killed | AssertionError: 1 != 0 : items 4 filled 4 gaps 0
F7 bare P0 is a badge: test_fill_sweep_leaves_a_badged_review_body_a_gap -> killed | AssertionError: Lists differ: ['pullrequestreview-31', 'annotation-34'] != ['pullrequestreview-31', 'issuecomment-33', 'annotation-34']
A1 no freshness check: test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt -> killed | AssertionError: 0 != 3 : 
A2 review copy kept, no freshness check: test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt -> killed | AssertionError: 0 != 3 : 
A3 review copy kept: test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt -> SURVIVED | OK
A4 lineage copies this head's files: test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt -> SURVIVED | OK
survivors: 2
$ git status --short scripts tests; echo "(empty: every mutant restored)"
(empty: every mutant restored)
```

- F1 to F5 (item 7): the reply login, the ignored-reply line, the own-reply login, the login grammar and the single-option rule each fail the item 7 test alone. F5 survived the first run of the table, whose repeated-option row also gave both positionals, so the positional count refused it. The row that repeats the option where the comments path belongs was added; the run above is the second.
- F6 and F7 (item 8): the badge gate and its grammar (the image form, not a bare `P0`) each fail the item 8 test.
- A1 to A4 (item 9): the freshness check alone (A1) fails the item 9 test, through the `codex-stale` mode. Two guards survive alone because the others cover them:
  - A3, the review-checkout `rm`: the freshness check refuses the tracked earlier receipt (its mtime is the worktree checkout's, before the run). A2 removes both and is killed, so the `rm` holds whenever the freshness check does not.
  - A4, the lineage skip: the `rm` in both checkouts runs after the lineage copy and removes whatever the copy brought in. The skip is still what item 9 names. It also keeps the copy from carrying this head's files in if the two steps ever change order.

## 4. The item 9 test against the audited script

```text
$ git show 7b574d32:scripts/orchestrator/orch-audit.sh > scripts/orchestrator/orch-audit.sh
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -m unittest tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt; echo "rc=$?"
FAIL: test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt) (mode='codex-silent')
AssertionError: 0 != 3 : 
FAIL: test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt) (mode='codex-stale')
AssertionError: 0 != 3 : 
Ran 1 test in 2.392s
FAILED (failures=2)
rc=1
$ git checkout -- scripts/orchestrator/orch-audit.sh
```

At `7b574d32` both modes exit 0 and print the earlier verdict: the audit's P1 at `orch-audit.sh:62` to 72.

The full `tests/unit` discover is not rerun here. The seat sandbox fails eight untouched modules on commit signing (a02's validation, its revise-round section), and CI runs the discover on the pushed head.

## 7. Revise round on `8576645c` (`5582fa3c`)

Sections 5 and 6 are in the main-checkout copy only. The task copy still hashes to `eaac8e4b…`.

```text
$ git log --oneline -3
5582fa3c fix(regime-counters): tokenize history bodies on whitespace runs as dispatch.sh does
8576645c Merge branch 'main' into tools/orchestrator-scripts-2
1089ed24 chore(orchestration): dotfiles-T128-orchestrator-tools-a05 task copy and evidence
$ git merge-base --is-ancestor 8576645c HEAD && echo "8576645c (the update-branch merge) is the base"
8576645c (the update-branch merge) is the base
$ git diff --stat 8576645c HEAD
 scripts/regime-counters.sh         |  4 ++--
 tests/unit/test_regime_counters.py | 14 ++++++++++++++
 2 files changed, 16 insertions(+), 2 deletions(-)
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-a05/task.md
eaac8e4bd03cda154273097736944b3762581f872d5f5fbcdca67650b43236ea  .orchestration/dotfiles-T128-orchestrator-tools-a05/task.md
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests.unit.test_regime_counters tests.unit.test_orchestrator_tools tests.unit.test_check_regime_boundary tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3
Ran 114 tests in 31.988s

OK
$ shellcheck scripts/regime-counters.sh && echo shellcheck-clean
shellcheck-clean
$ (cd "$TMPDIR" && shfmt --indent 4 --space-redirects --diff <worktree>/scripts/regime-counters.sh) && echo shfmt-clean
shfmt-clean
$ ruff format --check tests/unit/test_regime_counters.py && ruff check tests/unit/test_regime_counters.py
1 file already formatted
All checks passed!
$ git diff --numstat origin/main...HEAD | awk (files and added lines outside .orchestration)
files 12 added-non-test 499 added-test 507
```

Mutation proofs. `mutate-a05r.py` (scratchpad) edits `scripts/regime-counters.sh`, runs `tests.unit.test_regime_counters.RegimeCountersTest.test_a_tab_separated_task_counts_as_an_amendment`, counts a kill only on an AssertionError, and restores the file with `git checkout --`. R1 is the code at `8576645c`, so it also shows the test fails against the audited head.

```text
R1 single-space split: KILLED rc=1 ["AssertionError: Tuples differ: ('3', '2', '1', '1') != ('1', '0', '0', '0')"]
R2 no @tsv unescape: KILLED rc=1 ["AssertionError: Tuples differ: ('3', '2', '1', '1') != ('1', '0', '0', '0')"]
R3 empty tokens kept: KILLED rc=1 ["AssertionError: Tuples differ: ('3', '2', '1', '1') != ('3', '2', '0', '1')"]
R4 naive tab unescape: KILLED rc=1 ["AssertionError: Tuples differ: ('3', '2', '1', '1') != ('3', '2', '1', '2')"]
restored: 0 OK
```
