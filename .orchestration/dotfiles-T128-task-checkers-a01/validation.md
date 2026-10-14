---
task_id: dotfiles-T128-task-checkers-a01
seat: claude-standard-dot-a002
code_commit: c3b617a4
pr: 352
---

# Validation: dotfiles-T128-task-checkers-a01

Every command below ran from the worktree `.claude/worktrees/worker-f` inside the sandbox, with `MAIN` naming the main checkout and `UV_OFFLINE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` set: uv cannot reach pypi from the sandbox, so `uv run --with pyyaml` resolves from the uv cache (a first run of the Check command without it failed on `pypi.org` being blocked), and the global SSH signing key does not exist here. The output is verbatim; each block ends with the command's exit status. Sections 1 to 9 were captured at `c3b617a4`, before the PR was marked ready; CI and the Bot round follow in section 10.

## 1. Task file, task copy and inputs

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/dotfiles-T128-task-checkers-a01.md" .orchestration/dotfiles-T128-task-checkers-a01/task.md | sed "s#$MAIN/##"
cd00812f4a3cd64d841d5a96c7720e33be904e9cabb2cf70d31ccad8580b6a2d  .orchestration/tasks/dotfiles-T128-task-checkers-a01.md
cd00812f4a3cd64d841d5a96c7720e33be904e9cabb2cf70d31ccad8580b6a2d  .orchestration/dotfiles-T128-task-checkers-a01/task.md
[exit 0]
```
```console
$ cmp "$MAIN/.orchestration/tasks/dotfiles-T128-task-checkers-a01.md" .orchestration/dotfiles-T128-task-checkers-a01/task.md && echo byte-identical
byte-identical
[exit 0]
```
```console
$ (cd "$MAIN" && shasum -a 256 .orchestration/tasks/dotfiles-T128-task-checkers-a01-input/*.py)
7f2395011075fe471929c50f86cc25eec9dadb2e8ea5174360deab540954de61  .orchestration/tasks/dotfiles-T128-task-checkers-a01-input/ledger-check.py
fdab23e0f690f280a7e889a8c38e9ae526a29d88ff590981e50e285452b94df8  .orchestration/tasks/dotfiles-T128-task-checkers-a01-input/task-consistency-check.py
[exit 0]
```

## 2. Branch

```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main; git merge-base origin/main HEAD
c3b617a4 feat(orchestrator): task-consistency-check.py and ledger-check.py land with their tests (T704 a01)
28eec93c9a78e6a56d1f5f60ded675f521edb96f
28eec93c9a78e6a56d1f5f60ded675f521edb96f
[exit 0]
```

## 3. The Check command

```console
$ uv run python -m unittest tests/unit/test_task_checkers.py tests/unit/test_orchestrator_tools.py tests/unit/test_agmsg_orchestration_docs.py -v
test_ledger_check_passes_a_complete_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_passes_a_complete_record) ... ok
test_ledger_check_reports_the_gaps_of_the_pre_fix_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_reports_the_gaps_of_the_pre_fix_record) ... ok
test_task_consistency_check_detects_the_ten_historical_files (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_detects_the_ten_historical_files) ... ok
test_task_consistency_check_passes_a_complete_task_file (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_passes_a_complete_task_file) ... ok
test_task_consistency_check_reaches_every_other_check (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_reaches_every_other_check) ... ok
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
test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap) ... ok
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
test_docs_no_longer_name_codex_review_commit (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_docs_no_longer_name_codex_review_commit) ... ok
test_rule_and_skill_name_worker_seats_not_codex_workers (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_rule_and_skill_name_worker_seats_not_codex_workers) ... ok
test_rule_drops_the_worker_network_escalation (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_rule_drops_the_worker_network_escalation) ... ok
test_skill_drops_the_pane_status_gate_and_raw_pane_wakes (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_skill_drops_the_pane_status_gate_and_raw_pane_wakes) ... ok
test_rule_pointers_name_real_skill_sections (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_rule_pointers_name_real_skill_sections) ... ok
test_rule_states_the_invariants (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_rule_states_the_invariants) ... ok
test_word_budgets (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_word_budgets) ... ok
test_audit_command_lives_only_in_the_task_level_audit_bullet (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_audit_command_lives_only_in_the_task_level_audit_bullet) ... ok
test_codex_agents_points_at_the_worklog_section (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_codex_agents_points_at_the_worklog_section) ... ok
test_contextdb_cli_is_invoked_with_uv_run (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_contextdb_cli_is_invoked_with_uv_run) ... ok
test_skill_masks_evidence_with_a_runnable_command (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSingleSourceTest.test_skill_masks_evidence_with_a_runnable_command) ... ok
test_claude_worker_merge_denials_and_prefix_limits_are_documented (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_claude_worker_merge_denials_and_prefix_limits_are_documented) ... ok
test_codex_worker_profile_defaults_to_standard (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_codex_worker_profile_defaults_to_standard) ... ok
test_skill_carries_the_audit_gate_and_bot_wait_mechanics (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_audit_gate_and_bot_wait_mechanics) ... ok
test_skill_carries_the_parallel_execution_and_routing_mechanics (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_parallel_execution_and_routing_mechanics) ... ok
test_skill_carries_the_registration_and_delivery_mechanics (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_registration_and_delivery_mechanics) ... ok
test_skill_carries_the_session_lessons (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationSkillTest.test_skill_carries_the_session_lessons) ... ok
test_a_design_lands_on_main_before_its_task (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_design_lands_on_main_before_its_task) ... ok
test_a_revise_acceptance_names_the_previous_head_and_a_check (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_revise_acceptance_names_the_previous_head_and_a_check) ... ok
test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) ... ok
test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first) ... ok
test_boundary_merge_sentence_names_the_in_job_decision (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_boundary_merge_sentence_names_the_in_job_decision) ... ok
test_closed_selector_existence_is_checked_at_acceptance (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_closed_selector_existence_is_checked_at_acceptance) ... ok
test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestration_records_and_threat_tables) ... ok
test_counters_bullet_names_owners_not_sources (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_bullet_names_owners_not_sources) ... ok
test_counters_run_before_every_acceptance_action (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_run_before_every_acceptance_action) ... ok
test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) ... ok
test_dispatches_are_recorded_from_the_bus (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_dispatches_are_recorded_from_the_bus) ... ok
test_open_review_body_findings_have_an_identifier (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_open_review_body_findings_have_an_identifier) ... ok
test_open_third_round_threads_have_an_integration_outcome (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_open_third_round_threads_have_an_integration_outcome) ... ok
test_orchestration_records_rule_binds_the_bot_review_only (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_orchestration_records_rule_binds_the_bot_review_only) ... ok
test_pattern_rules_pin_their_safeguards (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_pattern_rules_pin_their_safeguards) ... ok
test_question_pongs_are_in_the_contract (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_question_pongs_are_in_the_contract) ... ok
test_regime_rule_sections_are_pinned_whole (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_regime_rule_sections_are_pinned_whole) ... ok
test_rule_changes_travel_as_task_amendments (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_rule_changes_travel_as_task_amendments) ... ok
test_shape_is_checked_by_hand_until_the_schema_lands (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_is_checked_by_hand_until_the_schema_lands) ... ok
test_shape_rules_and_the_decision_sentence_are_pinned (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_rules_and_the_decision_sentence_are_pinned) ... ok
test_task_file_review_is_one_round_with_a_fixed_stop_condition (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_task_file_review_is_one_round_with_a_fixed_stop_condition) ... ok
test_the_bot_wait_filters_the_codex_bot (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_bot_wait_filters_the_codex_bot) ... ok
test_the_ci_watch_is_joined_before_the_result (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_ci_watch_is_joined_before_the_result) ... ok
test_the_ci_watcher_survives_the_no_checks_race (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_ci_watcher_survives_the_no_checks_race) ... ok
test_the_gate_reads_the_acceptance_record (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_the_gate_reads_the_acceptance_record) ... ok
test_threat_table_rows_have_a_fixed_unit (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_threat_table_rows_have_a_fixed_unit) ... ok
test_threat_table_rule_carries_no_grammar (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_threat_table_rule_carries_no_grammar) ... ok
test_three_repeats_start_with_a_pasted_correction_search (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_three_repeats_start_with_a_pasted_correction_search) ... ok
test_workers_commit_inside_the_sandbox (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_commit_inside_the_sandbox) ... ok
test_workers_open_the_pr_as_a_draft (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_open_the_pr_as_a_draft) ... ok

----------------------------------------------------------------------
Ran 92 tests in 29.310s

OK
[exit 0]
```

## 4. Lint and format

```console
$ shellcheck --version | sed -n 2p; shellcheck scripts/orchestrator/orch-audit.sh && echo "shellcheck: clean"
version: 0.11.0
shellcheck: clean
[exit 0]
```
```console
$ shfmt --version; shfmt --indent 4 --space-redirects --diff scripts/orchestrator/orch-audit.sh && echo "shfmt: clean"
v3.14.1
shfmt: clean
[exit 0]
```
```console
$ ruff --version; ruff format --config ruff.toml --check scripts/orchestrator/task-consistency-check.py scripts/orchestrator/ledger-check.py tests/unit/test_task_checkers.py tests/unit/test_orchestrator_tools.py tests/unit/test_agmsg_orchestration_docs.py
ruff 0.17.0
5 files already formatted
[exit 0]
```
```console
$ ruff check --config ruff.toml scripts/orchestrator/task-consistency-check.py scripts/orchestrator/ledger-check.py tests/unit/test_task_checkers.py
All checks passed!
[exit 0]
```
```console
$ prettier --version; prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime/invariants.md
3.9.10
Checking formatting...
All matched files use Prettier code style!
[exit 0]
```

## 5. Replay over the format-2 task files

```console
$ for f in $(grep -l '^format: 2' .orchestration/tasks/*.md); do uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py "$f"; done | grep -c ': OK$'
15
[exit 0]
```
```console
$ for f in $(/usr/bin/grep -l '^format: 2' .orchestration/tasks/*.md); do uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py "$f"; done | /usr/bin/grep -c ': OK$'; /usr/bin/grep -l '^format: 2' .orchestration/tasks/*.md | wc -l | tr -d " "
15
86
[exit 0]
```
```console
$ cd "$MAIN" && uv run --no-project --with pyyaml python -I .claude/worktrees/worker-f/scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T128-task-checkers-a01.md; echo "exit $?"
dotfiles-T128-task-checkers-a01.md: OK
exit 0
[exit 0]
```

## 6. The port against the input, every task file of the worktree

```console
$ IN="$MAIN/.orchestration/tasks/dotfiles-T128-task-checkers-a01-input/task-consistency-check.py"; same=0; differ=0; for f in $(/usr/bin/grep -l "^format: 2" .orchestration/tasks/*.md); do a=$(uv run --no-project --with pyyaml python -I "$IN" "$f" 2>&1 | sort); b=$(uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py "$f" 2>&1 | sort); if [[ $a == "$b" ]]; then same=$((same + 1)); else differ=$((differ + 1)); echo "DIFF $f"; fi; done; echo "format-2 files: same output $same, different $differ"
format-2 files: same output 86, different 0
[exit 0]
```
```console
$ IN="$MAIN/.orchestration/tasks/dotfiles-T128-task-checkers-a01-input/task-consistency-check.py"; same=0; differ=0; frames="^  File |^    |^ *\\^"; for f in $(/usr/bin/grep -L "^format: 2" .orchestration/tasks/*.md); do a=$(uv run --no-project --with pyyaml python -I "$IN" "$f" 2>&1 | sort | /usr/bin/grep -Ev "$frames"); b=$(uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py "$f" 2>&1 | sort | /usr/bin/grep -Ev "$frames"); if [[ $a == "$b" ]]; then same=$((same + 1)); else differ=$((differ + 1)); echo "DIFF $f"; fi; done; echo "other files (traceback frame lines dropped): same output $same, different $differ"
other files (traceback frame lines dropped): same output 309, different 0
[exit 0]
```

## 7. Fixtures

```console
$ L=tests/fixtures/lessons; git show origin/main:.orchestration/acceptance/dotfiles-T128-process-rules-a05.md | cmp - $L/dotfiles-T128-process-rules-a05.record.txt && echo "record: byte-identical"; git show origin/main:.orchestration/validation/dotfiles-T128-process-rules-a05-audit-4af8939.md.last.md | cmp - $L/dotfiles-T128-process-rules-a05-audit-4af8939.md.last.txt && echo "audit: byte-identical"; git show origin/main:.orchestration/validation/dotfiles-T128-process-rules-a05-pr-feedback.json | uv run --no-project python -I -c 'import json, sys; a = json.load(sys.stdin); b = json.load(open(sys.argv[1])); one = open(sys.argv[1]).read() == json.dumps(b, separators=(",", ":")) + "\n"; print("sweep:", "same object" if a == b else "DIFFERENT", len(b["items"]), "items; one line as json.dumps(obj, separators=(\",\", \":\")):", one)' $L/dotfiles-T128-process-rules-a05-pr-feedback.json
record: byte-identical
audit: byte-identical
sweep: same object 129 items; one line as json.dumps(obj, separators=(",", ":")): True
[exit 0]
```
```console
$ for t in process-rules-a01 process-rules-a02 process-rules-a03 process-rules-a04 process-rules-a05 process-rules-a06 regime-counters-a01 regime-counters-a02 ci-skip-orchestration-a01 ci-skip-orchestration-a02; do git show "origin/main:.orchestration/tasks/dotfiles-T128-$t.md" | awk 'NR == 1 && $0 == "---" {print; c = 1; next} c {print; if ($0 == "---") exit}' > "$TMPDIR/fm.txt"; awk -v id="# dotfiles-T128-$t" '$0 == id {c = 1; next} c && /^# dotfiles-T128-/ {exit} c {print}' tests/fixtures/lessons/historical-front-matter.txt | cmp - "$TMPDIR/fm.txt" && echo "front matter $t: byte-identical"; done
front matter process-rules-a01: byte-identical
front matter process-rules-a02: byte-identical
front matter process-rules-a03: byte-identical
front matter process-rules-a04: byte-identical
front matter process-rules-a05: byte-identical
front matter process-rules-a06: byte-identical
front matter regime-counters-a01: byte-identical
front matter regime-counters-a02: byte-identical
front matter ci-skip-orchestration-a01: byte-identical
front matter ci-skip-orchestration-a02: byte-identical
[exit 0]
```
```console
$ /usr/bin/grep -c "/Users/" tests/fixtures/lessons/*; wc -l tests/fixtures/lessons/*
tests/fixtures/lessons/dotfiles-T128-process-rules-a05-audit-4af8939.md.last.txt:0
tests/fixtures/lessons/dotfiles-T128-process-rules-a05-pr-feedback.json:0
tests/fixtures/lessons/dotfiles-T128-process-rules-a05.record.txt:0
tests/fixtures/lessons/historical-front-matter.txt:0
      22 tests/fixtures/lessons/dotfiles-T128-process-rules-a05-audit-4af8939.md.last.txt
       1 tests/fixtures/lessons/dotfiles-T128-process-rules-a05-pr-feedback.json
      31 tests/fixtures/lessons/dotfiles-T128-process-rules-a05.record.txt
     490 tests/fixtures/lessons/historical-front-matter.txt
     544 total
[exit 0]
```

## 8. Mutations

```console
$ uv run --no-project python -I "$TMPDIR/t704/mutate.py"; git status --short
M1 C1 off	CAUGHT (unittest exit 1)
M2 C2 own-dir off	CAUGHT (unittest exit 1)
M3 C2 other-dir off	CAUGHT (unittest exit 1)
M4 C3 off	CAUGHT (unittest exit 1)
M5 C4 off	CAUGHT (unittest exit 1)
M6 C6 off	CAUGHT (unittest exit 1)
M7 C6 ignores --root	CAUGHT (unittest exit 1)
M8 C5 off	CAUGHT (unittest exit 1)
M9 C7 off	CAUGHT (unittest exit 1)
M10 C7b off	CAUGHT (unittest exit 1)
M11 C8 off	CAUGHT (unittest exit 1)
M12 C10 off	CAUGHT (unittest exit 1)
M13 C9 off	CAUGHT (unittest exit 1)
M14 exit always 0	CAUGHT (unittest exit 1)
L1 no ledger rows parsed	CAUGHT (unittest exit 1)
L2 non-Bot comments counted	CAUGHT (unittest exit 1)
L3 [P3] lines not counted	CAUGHT (unittest exit 1)
L4 exit always 0	CAUGHT (unittest exit 1)
A1 ledger refusal dropped	CAUGHT (unittest exit 1)
A2 default check is not the sibling	CAUGHT (unittest exit 1)
A3 override tracked check dropped	CAUGHT (unittest exit 1)
D1 SKILL line 73 reverted	CAUGHT (unittest exit 1)
D2 SKILL line 71 reverted	CAUGHT (unittest exit 1)
mutations 23 caught 23
?? .orchestration/dotfiles-T128-task-checkers-a01/
[exit 0]
```

## 9. Caps

```console
$ git diff --numstat origin/main...HEAD -- . ':!.orchestration' | awk '{print; if ($3 ~ /^tests\//) {ta += $1; td += $2} else {xf++; xa += $1; xd += $2}} END {printf "outside tests and .orchestration: %d files, %d added + %d deleted = %d changed (cap 200)\nunder tests: %d added (cap 1000), %d deleted\n", xf, xa, xd, xa + xd, ta, td}'
2	2	home/dot_agents/skills/agmsg-orchestration/SKILL.md
33	0	scripts/orchestrator/ledger-check.py
6	8	scripts/orchestrator/orch-audit.sh
147	0	scripts/orchestrator/task-consistency-check.py
23	0	tests/fixtures/lessons/dotfiles-T128-process-rules-a05-audit-4af8939.md.last.txt
1	0	tests/fixtures/lessons/dotfiles-T128-process-rules-a05-pr-feedback.json
31	0	tests/fixtures/lessons/dotfiles-T128-process-rules-a05.record.txt
490	0	tests/fixtures/lessons/historical-front-matter.txt
2	2	tests/fixtures/regime/invariants.md
14	7	tests/unit/test_agmsg_orchestration_docs.py
27	0	tests/unit/test_orchestrator_tools.py
137	0	tests/unit/test_task_checkers.py
outside tests and .orchestration: 4 files, 188 added + 10 deleted = 198 changed (cap 200)
under tests: 725 added (cap 1000), 9 deleted
[exit 0]
```

## Scripts used above

The fixtures of item 5 were written by this script (from the worktree, at `28eec93c` = `origin/main`):

```bash
#!/usr/bin/env bash
# Copy the T704 item 5 fixtures from origin/main into tests/fixtures/lessons/.
set -euo pipefail
out=tests/fixtures/lessons
mkdir -p "$out"
: > "$out/historical-front-matter.txt"
for t in process-rules-a01 process-rules-a02 process-rules-a03 process-rules-a04 process-rules-a05 process-rules-a06 regime-counters-a01 regime-counters-a02 ci-skip-orchestration-a01 ci-skip-orchestration-a02; do
    printf '# dotfiles-T128-%s\n' "$t" >> "$out/historical-front-matter.txt"
    git show "origin/main:.orchestration/tasks/dotfiles-T128-$t.md" | awk 'NR == 1 && $0 == "---" {print; c = 1; next} c {print; if ($0 == "---") exit}' >> "$out/historical-front-matter.txt"
done
git show origin/main:.orchestration/acceptance/dotfiles-T128-process-rules-a05.md > "$out/dotfiles-T128-process-rules-a05.record.txt"
git show origin/main:.orchestration/validation/dotfiles-T128-process-rules-a05-pr-feedback.json | python3 -I -c 'import json, sys; print(json.dumps(json.load(sys.stdin), separators=(",", ":")))' > "$out/dotfiles-T128-process-rules-a05-pr-feedback.json"
git show origin/main:.orchestration/validation/dotfiles-T128-process-rules-a05-audit-4af8939.md.last.md > "$out/dotfiles-T128-process-rules-a05-audit-4af8939.md.last.txt"
```

The mutation pass of section 8 (`$TMPDIR/t704/mutate.py`): each mutation replaces one exact string, runs the named tests, and restores the file in a `finally`.

```python
"""Apply each mutation to the worktree file, run the named test module, record the exit, restore the file."""
import os, pathlib, subprocess, sys

TCC, LC, AUDIT = "scripts/orchestrator/task-consistency-check.py", "scripts/orchestrator/ledger-check.py", "scripts/orchestrator/orch-audit.sh"
SKILL = "home/dot_agents/skills/agmsg-orchestration/SKILL.md"
CHECKERS, TOOLS, DOCS = ["tests/unit/test_task_checkers.py"], ["tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap"], ["tests/unit/test_agmsg_orchestration_docs.py"]
M = [
    ("M1 C1 off", TCC, "if tid != p.stem:", "if False:", CHECKERS),
    ("M2 C2 own-dir off", TCC, "if not any(a.startswith(own_dir) for a in allowed):", "if False:", CHECKERS),
    ("M3 C2 other-dir off", TCC, "if m and m.group(1) != tid:", "if False:", CHECKERS),
    ("M4 C3 off", TCC, 'fails.append(f"C3 ', 'None and fails.append(f"C3 ', CHECKERS),
    ("M5 C4 off", TCC, 'if rows and a.split("*")[0].rstrip("/") not in rowtext:', "if False:", CHECKERS),
    ("M6 C6 off", TCC, 'if cur and cur != dr["receipt"]:', "if False:", CHECKERS),
    ("M7 C6 ignores --root", TCC, '(design := root / dr["design"])', '(design := pathlib.Path(dr["design"]))', CHECKERS),
    ("M8 C5 off", TCC, "if m and m.group(1) != suffix:", "if False:", CHECKERS),
    ("M9 C7 off", TCC, "if rows and name not in controls.lower():", "if False:", CHECKERS),
    ("M10 C7b off", TCC, "if len(hit) > 1:", "if False:", CHECKERS),
    ("M11 C8 off", TCC, "if added and rows and var not in controls:", "if False:", CHECKERS),
    ("M12 C10 off", TCC, 'if git(root, "grep", "-qF", lit,', 'if False and git(root, "grep", "-qF", lit,', CHECKERS),
    ("M13 C9 off", TCC, "            if not ok:\n", "            if False:\n", CHECKERS),
    ("M14 exit always 0", TCC, "rc |= bool(fails)", "rc |= 0", CHECKERS),
    ("L1 no ledger rows parsed", LC, r"\t(\S+)$", r"\t(\S+)x$", CHECKERS),
    ("L2 non-Bot comments counted", LC, 'item.get("bot")', "True", CHECKERS),
    ("L3 [P3] lines not counted", LC, r"^\[P[0-3]\]", r"^\[P[0-2]\]", CHECKERS),
    ("L4 exit always 0", LC, "return 1 if gaps else 0", "return 0", CHECKERS),
    ("A1 ledger refusal dropped", AUDIT, '|| refuse "the ledger is incomplete" 3', "|| true", TOOLS),
    ("A2 default check is not the sibling", AUDIT, "/ledger-check.py}", "/absent-check.py}", TOOLS),
    ("A3 override tracked check dropped", AUDIT, '(($# == 3)) || [[ -n $(git ls-files -- "${check}") ]] || refuse', 'true || refuse', TOOLS),
    ("D1 SKILL line 73 reverted", SKILL, "checked by `scripts/orchestrator/task-consistency-check.py` (C1 to C10 and C7b) before dispatch and at acceptance,", "checked by the task-consistency check C1 to C6 once plan 007 T704 lands it and by hand until then,", DOCS),
    ("D2 SKILL line 71 reverted", SKILL, "C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest.", "C4 of the task-consistency check (plan 007 T704) verifies the path half once it lands, and the task-file review checks it by hand until then.", DOCS),
]
env = {**os.environ, "UV_OFFLINE": "1", "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "commit.gpgsign", "GIT_CONFIG_VALUE_0": "false"}
caught = 0
for label, path, old, new, tests in M:
    p = pathlib.Path(path)
    original = p.read_text()
    assert original.count(old) == 1, (label, old)
    try:
        p.write_text(original.replace(old, new))
        rc = subprocess.run(["uv", "run", "python", "-m", "unittest", *tests], capture_output=True, env=env, timeout=600).returncode
    finally:
        p.write_text(original)
    caught += rc != 0
    print(f"{label}\t{'CAUGHT' if rc else 'SURVIVED'} (unittest exit {rc})")
print(f"mutations {len(M)} caught {caught}")
```
