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

## 5. CI on `1089ed24` (main-checkout copy only)

```text
$ gh pr checks 346 --watch --interval 30; echo "rc=$?"   # the final table
CodeRabbit	pass	0
GitGuardian Security Checks	pass	3s
private-bootstrap (macos-14, client)	pass	9s
private-bootstrap (ubuntu-24.04, client)	pass	9s
private-bootstrap (ubuntu-24.04, server)	pass	8s
public-bootstrap (macos-14, client)	pass	8m30s
public-bootstrap (ubuntu-24.04, client)	pass	10m21s
public-bootstrap (ubuntu-24.04, server)	pass	7m56s
test (macos-14, client)	pass	7m34s
test (ubuntu-24.04, client)	pass	9m29s
test (ubuntu-24.04, server)	pass	5m34s
test (ubuntu-26.04, client)	pass	8m30s
validate	pass	1m32s
rc=0
```

## 6. The Bot on `1089ed24` (main-checkout copy only)

One `gh api` loop polled the PR's reviews (by `chatgpt-codex-connector[bot]` with `commit_id` the head) and its issue comments (by the Bot, after the push at 17:13:11Z) once a minute for 20 minutes, then listed every Bot review comment as `<id> <commit> <original commit> <path:line> <badge> <first line>`:

```text
head=1089ed24b11d79d8855e05f16bd93add72e28603 minutes=20
reviews: none
issue_comments: none
4260535901 1089ed24 1287af34 scripts/orchestrator/dispatch.sh:80 P1 **<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Enforce TASK
4260535916 1089ed24 1287af34 scripts/orchestrator/boundary.sh:44 P2 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Preserve del
4260535924 1089ed24 1287af34 scripts/orchestrator/ff-main.sh:38 P2 **<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Handle local
```

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

## 8. CI on `046901bc` (main-checkout copy only)

`gh pr checks 346 --watch` exited 0, and `gh pr view 346 --json headRefOid` reads `046901bcdc92301fac2f81b0ea4f9ca802e1a695`. Each check's last state, 13 of 13 pass:

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	4s	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	15s	https://github.com/mryfmo/dotfiles/actions/runs/38475940395/job/115566509489	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38475940395/job/115566509574	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38475940395/job/115566509235	
public-bootstrap (macos-14, client)	pass	9m19s	https://github.com/mryfmo/dotfiles/actions/runs/38475940395/job/115566509624	
public-bootstrap (ubuntu-24.04, client)	pass	8m28s	https://github.com/mryfmo/dotfiles/actions/runs/38475940395/job/115566509391	
public-bootstrap (ubuntu-24.04, server)	pass	7m57s	https://github.com/mryfmo/dotfiles/actions/runs/38475940395/job/115566509616	
test (macos-14, client)	pass	7m38s	https://github.com/mryfmo/dotfiles/actions/runs/38475940351/job/115566509248	
test (ubuntu-24.04, client)	pass	8m2s	https://github.com/mryfmo/dotfiles/actions/runs/38475940351/job/115566509098	
test (ubuntu-24.04, server)	pass	5m36s	https://github.com/mryfmo/dotfiles/actions/runs/38475940351/job/115566508959	
test (ubuntu-26.04, client)	pass	8m31s	https://github.com/mryfmo/dotfiles/actions/runs/38475940351/job/115566509360	
validate	pass	1m49s	https://github.com/mryfmo/dotfiles/actions/runs/38475940525/job/115566509798	
```

## 9. PR-B on `tools/orchestrator-scripts-3`

```text
$ git log --oneline -4
362a9c2b test(orchestrator): assert the dispatch list and the absent key without a KeyError or an env dump
d19ed9be feat(orchestrator): acceptance-front-matter.py and orch-gate.sh (T718 a05, PR-B)
c586f20d feat(orchestrator): the second slice's scripts and the first slice's residual fixes (T718 a02, PR-A) (#346)
df044557 chore(orchestration): boundary commit 2026-10-13 (13): plan 020 step 5 (T703 #328 and T702 #329 merged, Phase 1 closed; a02 PR-A #346 stopped by the one-round rule and reset to a05), records and the cost ledger (#349)
$ git merge-base HEAD origin/main
c586f20dbc7627a16c2e900a094083f31a55f34f
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-a05/task.md
eaac8e4bd03cda154273097736944b3762581f872d5f5fbcdca67650b43236ea  .orchestration/dotfiles-T128-orchestrator-tools-a05/task.md
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v 2>&1 | tail -n 4
----------------------------------------------------------------------
Ran 35 tests in 18.486s

OK
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v 2>&1 | grep -E "front_matter|orch_gate"
test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record) ... ok
test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit) ... ok
test_orch_gate_passes_the_gate_inputs_from_the_review_worktree (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_passes_the_gate_inputs_from_the_review_worktree) ... ok
test_orch_gate_refuses_a_sweep_of_another_pr_before_the_review_worktree_moves (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_refuses_a_sweep_of_another_pr_before_the_review_worktree_moves) ... ok
test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree) ... ok
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_regime_counters.py 2>&1 | tail -n 3
Ran 28 tests in 3.855s

OK
$ shellcheck --version | sed -n 2p; shellcheck scripts/orchestrator/*.sh && echo shellcheck-clean
version: 0.11.0
shellcheck-clean
$ (cd "$TMPDIR" && shfmt --indent 4 --space-redirects --diff <worktree>/scripts/orchestrator/orch-gate.sh) && echo shfmt-clean
shfmt-clean
$ ruff format --check scripts/orchestrator/acceptance-front-matter.py tests/unit/test_orchestrator_tools.py && ruff check scripts/orchestrator tests/unit/test_orchestrator_tools.py
2 files already formatted
All checks passed!
$ git diff --numstat origin/main...HEAD
124	0	scripts/orchestrator/acceptance-front-matter.py
63	0	scripts/orchestrator/orch-gate.sh
151	1	tests/unit/test_orchestrator_tools.py
$ (the INV-2 sums outside .orchestration)
files 3 added-non-test 187 added-test 151
```

Mutation proofs. `mutate-prb.py` (scratchpad) edits one span, runs the named test of `tests.unit.test_orchestrator_tools.OrchestratorToolsTest`, counts a kill only on an AssertionError, and restores the file with `git checkout --`.

```text
AF1 no head check: KILLED rc=1 AssertionError: 1 != 0 : written .orchestration/acceptance/t-a01.md head 2126e5d pr 9 ledger 4
AF2 duplicate keys read: KILLED rc=1 AssertionError: 1 != 0 : written .orchestration/acceptance/t-a01.md head 694e94f pr 9 ledger 0
AF3 present ids re-added: KILLED rc=1 AssertionError: 'kept-ledger-row 4250000001' not found in 'written .orchestration/acceptance/t-a01.md head e35186d pr 9 ledger 5\n'
AF4 searches for every class: KILLED rc=1 AssertionError: Lists differ: [{'class': 'stale-path', 'records': ['M-1.md']}] != [{'class': 'other', 'records': ['M-1.md', 'M-2.md']},[43 chars]d']}]
AF5 text after the block dropped: KILLED rc=1 AssertionError: Tuples differ: ('t-a01', '4d473acc281f02941f7be4ed5ce74992965c9f95', 9, 1, '\n# Record\n') != ('t-a01', '4d473acc281f02941f7be4ed5ce74
AF6 dispatch list dropped: KILLED rc=1 AssertionError: ['AGMSG-TASK v1 task_id=t-a01'] != None
AF7 field checks skipped: KILLED rc=1 AssertionError: 1 != 0 : written .orchestration/acceptance/t-a01.md head f52b1bc pr 9 ledger 5
AF8 dispositions not required: KILLED rc=1 AssertionError: '--audit-dispositions is required' not found in "acceptance-front-matter: AUDIT_EVIDENCE verdict is incorrect: the acceptance record's
AF9 completeness skipped: KILLED rc=1 AssertionError: 1 != 0 : written .orchestration/acceptance/t-a01.md head b73c5ec pr 9 ledger 0
G1 AUDIT_DISPOSITIONS kept: KILLED rc=1 AssertionError: 'AUDIT_DISPOSITIONS' unexpectedly found in ['ACCEPTANCE_EVIDENCE', 'AGENT_REVIEWED', 'AGMSG_SCRIPTS', 'AGMSG_SPAWNED', 'AI_AGENT', 'AL
G2 no ACCEPTANCE_EVIDENCE: KILLED rc=1 AssertionError: {'ACC[14 chars]CE': '.orchestration/acceptance/t-a01.md', 'AU[255 chars]ain'} != {'ACC[14 chars]CE': None, 'AUDIT_EVIDENCE': '.orchest
G3 make in the main checkout: KILLED rc=1 AssertionError: '/private/tmp/claude-501/tmptralagwa/repo/.claude/worktrees/orchestrator-review' != '/private/tmp/claude-501/tmptralagwa/repo'
G4 gate status dropped: KILLED rc=1 AssertionError: 0 != 2 : 
G5 review worktree left at the head: KILLED rc=1 AssertionError: '8ba1a18e7249f2eaeb3ffbd7a1b330ab3858133f' != 'f485bdd5723eac97d8b38e3207f95e2b8c0ba55f'
G6 no PR binding: KILLED rc=1 AssertionError: 0 != 2 : 
restored: 0 OK
```
## 10. PR-B fix round (`e30cbed0`)

```text
$ git log --oneline -3
e30cbed0 fix(orchestrator): orch-gate.sh runs the trusted gate, refuses tracked symlinks, clears overrides
0749e931 chore(orchestration): dotfiles-T128-orchestrator-tools-a05 PR-B evidence
362a9c2b test(orchestrator): assert the dispatch list and the absent key without a KeyError or an env dump
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v 2>&1 | grep -E "orch_gate|front_matter|ERROR|FAIL|^Ran|^OK"
test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record) ... ok
test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit) ... ok
test_design_keydiff_names_the_changed_invariant (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_design_keydiff_names_the_changed_invariant) ... ERROR
test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration) ... ok
test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves) ... ok
test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree) ... ok
test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs) ... ok
Ran 36 tests in 20.715s
FAILED (errors=1)
$ (cd "$TMPDIR" && UV_OFFLINE=1 uv run --no-project --with pyyaml python -I -c 'import yaml' 2>&1 | tail -2)
error: Failed to download and build `pyyaml==6.0.3`
  cause: Network connectivity is disabled, but the requested data wasn't found in the cache: https://files.pythonhosted.org/packages/05/8e/961c0007c59b8dd7729d542c61a4d537767a59645b82a0b521206e1e25c2/pyyaml-6.0.3.tar.gz
$ shellcheck scripts/orchestrator/*.sh && echo shellcheck-clean
shellcheck-clean
$ (cd "$TMPDIR" && shfmt --indent 4 --space-redirects --diff <worktree>/scripts/orchestrator/orch-gate.sh) && echo shfmt-clean
shfmt-clean
$ ruff format --check tests/unit/test_orchestrator_tools.py && ruff check tests/unit/test_orchestrator_tools.py
1 file already formatted
All checks passed!
$ git diff --numstat origin/main...HEAD | awk (files and added lines outside .orchestration)
files 3 added-non-test 196 added-test 174
```

After `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets …` fetched PyYAML into the cache (the masker of these records, run with pypi.org and files.pythonhosted.org allowed), the module passes offline:

```text
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py 2>&1 | tail -3
Ran 36 tests in 21.011s

OK
```

Mutation proofs. `mutate-prb2.py` (scratchpad) uses the same rules as §9.

```text
F1 the head's gate runs: KILLED rc=1 AssertionError: Lists differ: ['run[31 chars]I', '/private/tmp/claude-501/tmpnso2ai87/repo/[52 chars]ain'] != ['run[31 chars]I', 'scripts/re
F2 no gate equality check: KILLED rc=1 AssertionError: 0 != 2 : 
F3 tracked symlinks allowed: KILLED rc=1 AssertionError: 0 != 2 : 
F4 CRIT_REVIEW inherited: KILLED rc=1 AssertionError: Lists differ: [] != ['CRIT_REVIEW']
F5 CRIT_REVIEWED inherited: KILLED rc=1 AssertionError: Lists differ: [] != ['CRIT_REVIEWED']
G1 AUDIT_DISPOSITIONS inherited: KILLED rc=1 AssertionError: Lists differ: [] != ['AUDIT_DISPOSITIONS']
G2 no ACCEPTANCE_EVIDENCE: KILLED rc=1 AssertionError: {'ACC[14 chars]CE': '.orchestration/acceptance/t-a01.md', 'AU[232 chars] '1'} != {'ACC[14 chars]CE': None, 'AUDIT_EVIDENCE':
G3 the gate in the main checkout: KILLED rc=1 AssertionError: '/private/tmp/claude-501/tmp5juebzi8/repo/.claude/worktrees/orchestrator-review' != '/private/tmp/claude-501/tmp5juebzi8/rep
G4 gate status dropped: KILLED rc=1 AssertionError: 0 != 2 : 
G5 review worktree left at the head: KILLED rc=1 AssertionError: '7525355595ba59d72065367ba38d83ec85a83874' != '15456cf2590c836208cf7a6f47c9dc2bae69f3ca'
G6 no PR binding: KILLED rc=1 AssertionError: 0 != 2 : 
restored: 0 OK
```

## 11. PR #350 CI and Bot (main-checkout copy only)

CI on `0749e931` (`gh pr checks 350 --watch` exited 0). Each check's last state, 13 of 13 pass:

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	2s	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38484720257/job/115595479203	
private-bootstrap (ubuntu-24.04, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/38484720257/job/115595478731	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38484720257/job/115595479096	
public-bootstrap (macos-14, client)	pass	6m32s	https://github.com/mryfmo/dotfiles/actions/runs/38484720257/job/115595478978	
public-bootstrap (ubuntu-24.04, client)	pass	8m1s	https://github.com/mryfmo/dotfiles/actions/runs/38484720257/job/115595479179	
public-bootstrap (ubuntu-24.04, server)	pass	6m6s	https://github.com/mryfmo/dotfiles/actions/runs/38484720257/job/115595479086	
test (macos-14, client)	pass	6m1s	https://github.com/mryfmo/dotfiles/actions/runs/38484720225/job/115595478780	
test (ubuntu-24.04, client)	pass	8m1s	https://github.com/mryfmo/dotfiles/actions/runs/38484720225/job/115595479655	
test (ubuntu-24.04, server)	pass	5m2s	https://github.com/mryfmo/dotfiles/actions/runs/38484720225/job/115595479206	
test (ubuntu-26.04, client)	pass	8m10s	https://github.com/mryfmo/dotfiles/actions/runs/38484720225/job/115595479156	
validate	pass	57s	https://github.com/mryfmo/dotfiles/actions/runs/38484720246/job/115595478646	
```

CI on `1f3abb55`, the fix-round head (`gh pr checks 350 --watch` exited 0; `gh pr view 350 --json headRefOid` reads `1f3abb555949dc62b2a90cfb66e6a5554e4891e0`). Each check's last state, 13 of 13 pass:

```text
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	1s	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	13s	https://github.com/mryfmo/dotfiles/actions/runs/38486634489/job/115601746791	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/38486634489/job/115601747060	
private-bootstrap (ubuntu-24.04, server)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/38486634489/job/115601747035	
public-bootstrap (macos-14, client)	pass	9m17s	https://github.com/mryfmo/dotfiles/actions/runs/38486634489/job/115601747043	
public-bootstrap (ubuntu-24.04, client)	pass	9m39s	https://github.com/mryfmo/dotfiles/actions/runs/38486634489/job/115601747206	
public-bootstrap (ubuntu-24.04, server)	pass	8m1s	https://github.com/mryfmo/dotfiles/actions/runs/38486634489/job/115601747115	
test (macos-14, client)	pass	7m16s	https://github.com/mryfmo/dotfiles/actions/runs/38486634497/job/115601747332	
test (ubuntu-24.04, client)	pass	8m3s	https://github.com/mryfmo/dotfiles/actions/runs/38486634497/job/115601747261	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/38486634497/job/115601746944	
test (ubuntu-26.04, client)	pass	8m26s	https://github.com/mryfmo/dotfiles/actions/runs/38486634497/job/115601747278	
validate	pass	1m45s	https://github.com/mryfmo/dotfiles/actions/runs/38486634561/job/115601747485	
```

The Bot reviewed once, on `0749e931`: review 5511311071 at 23:33:44Z, and its summary comment reached `"status":"completed"` by 23:40:52Z. It left three P1 threads (4265190252, 4265190259 and 4265190267, all `fixed:e30cbed0`, report). After the fix-round push, the reviews list still holds that one Codex review and the comments list those three threads, with no reply.

## 12. PR-B revise 1 (`ced110dd`, amendment 1)

### The probe (`scratchpad/pv-probe.sh`; the scratch directory is a fresh `mktemp -d` under `$TMPDIR`, its `.python-version` is `./pwn`, and `pwn` touches `ran-$$` and exits 1; the last argument is this worktree)

```text
$ bash pv-probe.sh <worker-c>
find:
error: Failed to inspect Python interpreter from provided path at `./pwn`
  cause: Querying Python at `./pwn` failed with exit status exit status: 1
ran after find:        1
run:
error: Failed to inspect Python interpreter from provided path at `./pwn`
  cause: Querying Python at `./pwn` failed with exit status exit status: 1
ran after run:        2
root files:
none
root find: ~/.local/share/mise/installs/python/latest/bin/python rc=0
trap 1:
restore
rc=1
trap 2:
rc=1
trap 3:
sub rc=3
trap-ran
rc=0
```

- "trap 1": an EXIT trap runs when `set -e` stops the script.
- "trap 2": a failing command in the trap makes the exit non-zero after an `exit 0`.
- "trap 3": a `( … ) || rc=$?` subshell does not fire the parent's trap.

### Tests, lint, size

```text
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests.unit.test_orchestrator_tools
Ran 38 tests in 25.265s

OK
rc 0
$ ruff check / ruff format --check tests/unit/test_orchestrator_tools.py; shellcheck and shfmt --indent 4 --space-redirects -d on scripts/orchestrator/orch-gate.sh
All checks passed!
1 file already formatted
shellcheck rc 0
shfmt rc 0
$ git diff --numstat origin/main...HEAD (outside .orchestration)
files 3 added_non_test 198 added_test 205
$ UV_OFFLINE=1 make validate-agent-assets
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: amendments 11 >= 2 source=live
agent asset validation ok
$ shasum -a 256 .orchestration/dotfiles-T128-orchestrator-tools-a05/task.md
6b238e5a958ed5124d997e129391a4e10cc2b61b7b9f57052e8b463b4f549f23  .orchestration/dotfiles-T128-orchestrator-tools-a05/task.md
```

The two WARN lines are another task's counters. The validator's run also tried `cafe.github.com:443`, which the sandbox refused; the validation still ended ok.

### Mutation proofs (`scratchpad/mutate-fix.py`)

The method is the one used before:

- edit one span of `orch-gate.sh` at `ced110dd`;
- run the full dotted test;
- count a kill only on an AssertionError;
- restore with `git checkout --`.

```text
KILLED P1 the pre-fix gate run (uv run in the review worktree) :: test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree :: AssertionError: True is not false : the head's .python-version executable ran
KILLED P2 the interpreter resolved in the review worktree :: test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree :: AssertionError: 127 != 0 : /private/tmp/claude-501/tmpg6zqiq5h/repo/scripts/orchestrator/orch-gate.sh: line 70: : command not found
KILLED P3 the gate run by name from PATH, not the resolved path :: test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs :: NameError: name 'gate' is not defined
KILLED R1 no trap (the pre-fix code) :: test_orch_gate_restores_the_review_worktree_when_setup_fails :: AssertionError: '' != '?? .orchestration/'
KILLED R2 the trap set after the evidence copy :: test_orch_gate_restores_the_review_worktree_when_setup_fails :: AssertionError: '' != '?? .orchestration/'
kills 5/5
clean
```

- P3's last error line comes from the stub gate file (`gate`) run under the real `python3`. The assertion that failed is the exit status (`AssertionError: 1 != 0`, rerun of P3 alone).
- R1 is the pre-fix code without the trap. P1 is the pre-fix gate line.

## 13. PR #350 CI on `a06c874e` (main-checkout copy only)

The push moved PR #350 from `f48593d6` to `a06c874e`: `ced110dd` is the fix and `a06c874e` the evidence. The Bot reviews on PR open only, so this round has no Bot wait.

### Attempt 1: one test job failed on a GitHub API HTTP 500, three cancelled

```text
$ gh pr checks 350 --watch --interval 30; gh pr view 350 --json headRefOid,mergeStateStatus
CodeRabbit	pass	0
GitGuardian Security Checks	pass	9s
private-bootstrap (macos-14, client)	pass	12s
private-bootstrap (ubuntu-24.04, client)	pass	7s
private-bootstrap (ubuntu-24.04, server)	pass	6s
public-bootstrap (macos-14, client)	pass	8m41s
public-bootstrap (ubuntu-24.04, client)	pass	9m43s
public-bootstrap (ubuntu-24.04, server)	pass	8m2s
test (macos-14, client)	fail	5m17s
test (ubuntu-24.04, client)	fail	5m15s
test (ubuntu-24.04, server)	fail	4m42s
test (ubuntu-26.04, client)	fail	5m17s
validate	pass	1m46s
checks rc 1
a06c874ed37d01c6effaaae59eeec1a15510d80b BLOCKED
```

`gh run view 38497634877 --log-failed` returned one job's log, `test (ubuntu-24.04, server)`:

- The only `not ok` is case 59, `tests/install/common/mise.bats` line 26. GitHub's API answered HTTP 500 for the mise tag ref during the release-attestation check. The excerpt follows.
- The run's job list shows that job as `failure` and the other three test jobs as `cancelled` by fail-fast. `--log-failed` for each of them shows no `not ok` line.
- This round changes nothing that `mise.bats` exercises. The same check passed on `1f3abb55` (§11).

The failed jobs were re-run with `gh run rerun 38497634877 --failed`.

```text
2026-10-14T01:52:26.7438024Z ok 57 [common] README documents agent permission asset lifecycle
2026-10-14T01:52:26.7957209Z ok 58 [common] chezmoi source-path handoff resolves the repository root
2026-10-14T01:52:30.5770355Z not ok 59 [common] mise
2026-10-14T01:52:30.5782251Z # (in test file tests/install/common/mise.bats, line 26)
2026-10-14T01:52:30.5815647Z #   `DOTFILES_DEBUG=1 bash -c 'source "$1"; install_mise' _ "${SCRIPT_PATH}"' failed
2026-10-14T01:52:30.5818371Z # gpg: keybox '/tmp/tmp.ANEwtf0ZaP/gnupg/pubring.kbx' created
2026-10-14T01:52:30.5819177Z # gpg: /tmp/tmp.ANEwtf0ZaP/gnupg/trustdb.gpg: trustdb created
2026-10-14T01:52:30.5819824Z # gpgv: Signature made Fri Oct  9 23:35:47 2026 UTC
2026-10-14T01:52:30.5820482Z # gpgv:                using RSA key 24853EC9F655CE80B48E6C3A8B81C9D17413A06D
2026-10-14T01:52:30.5821172Z # gpgv: Good signature from "mise releases <release@mise.jdx.dev>"
2026-10-14T01:52:30.5822023Z # HTTP 500: 500 Internal Server Error (https://api.github.com/repos/jdx/mise/git/ref/tags%2Fv2026.10.7)
2026-10-14T01:52:30.5822959Z # GitHub release attestation failed for mise-v2026.10.7-linux-x64.tar.gz; nothing was installed.
2026-10-14T01:52:30.6419461Z ok 60 [common] mise bootstrap resolves the newest cooled-down jdx/mise release
```

### Attempt 2: the re-run

```text
$ gh pr checks 350 --watch --interval 30; gh pr view 350 --json headRefOid,mergeStateStatus; gh run view 38497634877 --json jobs,attempt
CodeRabbit	pass	0
GitGuardian Security Checks	pass	9s
private-bootstrap (macos-14, client)	pass	12s
private-bootstrap (ubuntu-24.04, client)	pass	7s
private-bootstrap (ubuntu-24.04, server)	pass	6s
public-bootstrap (macos-14, client)	pass	8m41s
public-bootstrap (ubuntu-24.04, client)	pass	9m43s
public-bootstrap (ubuntu-24.04, server)	pass	8m2s
test (macos-14, client)	pass	6m37s
test (ubuntu-24.04, client)	pass	8m47s
test (ubuntu-24.04, server)	pass	5m18s
test (ubuntu-26.04, client)	pass	8m9s
validate	pass	1m46s
checks rc 0
a06c874ed37d01c6effaaae59eeec1a15510d80b BLOCKED
attempt 2
test (ubuntu-26.04, client) success
test (ubuntu-24.04, client) success
test (ubuntu-24.04, server) success
test (macos-14, client) success
```
