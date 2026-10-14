---
task_id: dotfiles-T128-task-checkers-a01
seat: claude-standard-dot-a002
code_commit: 612931f3
pr: 352
---

# Validation: dotfiles-T128-task-checkers-a01

Every command in sections 1 to 9 ran from the worktree `.claude/worktrees/worker-f` inside the sandbox. `MAIN` names the main checkout, and these were set: `UV_OFFLINE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`. uv cannot reach pypi from the sandbox, so `uv run --with pyyaml` resolves from the uv cache; one Check run without it failed on `pypi.org` being blocked. The global SSH signing key does not exist here. The output is verbatim, and each block ends with the command's exit status.

Sections 1 to 9 were captured at `612931f3`: the amendment-2 fix round, on top of the CI fix `1ca0d5d1` and the first head `c3b617a4`/`63433cf1`. Section 10 holds the CI runs and the Bot round.

## 1. Task file, task copy and inputs

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/dotfiles-T128-task-checkers-a01.md" .orchestration/dotfiles-T128-task-checkers-a01/task.md | sed "s#$MAIN/##"
a309b3944b2dec9be6117499a98d7cc4bd7bd0026706f99525df1221fd226efb  .orchestration/tasks/dotfiles-T128-task-checkers-a01.md
a309b3944b2dec9be6117499a98d7cc4bd7bd0026706f99525df1221fd226efb  .orchestration/dotfiles-T128-task-checkers-a01/task.md
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
612931f3 fix(orchestrator): the ledger check counts what the gate counts; C4 names an entry at a path boundary (T704 a01 amendment 2)
1ca0d5d1 fix(tests): put the stub git first inside uv run (macOS CI, T704 a01)
63433cf1 docs(orchestration): task-checkers a01 task copy and evidence (c3b617a4, PR #352)
c3b617a4 feat(orchestrator): task-consistency-check.py and ledger-check.py land with their tests (T704 a01)
28eec93c9a78e6a56d1f5f60ded675f521edb96f
28eec93c9a78e6a56d1f5f60ded675f521edb96f
[exit 0]
```

## 3. The Check command

```console
$ uv run python -m unittest tests/unit/test_task_checkers.py tests/unit/test_orchestrator_tools.py tests/unit/test_agmsg_orchestration_docs.py -v
test_ledger_check_counts_what_the_gate_counts (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_counts_what_the_gate_counts) ... ok
test_ledger_check_passes_a_complete_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_passes_a_complete_record) ... ok
test_ledger_check_reports_the_gaps_of_the_pre_fix_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_reports_the_gaps_of_the_pre_fix_record) ... ok
test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary) ... ok
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
Ran 94 tests in 30.343s

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

## 6. The port against the input, and the ten files under the amended C4

```console
$ IN="$MAIN/.orchestration/tasks/dotfiles-T128-task-checkers-a01-input/task-consistency-check.py"; d="$TMPDIR/cmp"; mkdir -p "$d"; : > "$d/all"; for f in $(/usr/bin/grep -l "^format: 2" .orchestration/tasks/*.md); do uv run --no-project --with pyyaml python -I "$IN" "$f" 2>&1 | sort > "$d/a"; uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py "$f" 2>&1 | sort > "$d/b"; diff "$d/a" "$d/b" | /usr/bin/grep "^[<>]" | sed "s#^#$(basename "$f"): #" >> "$d/all"; done; cat "$d/all"; echo "format-2 files whose output differs: $(cut -d: -f1 "$d/all" | sort -u | /usr/bin/grep -c .); differing lines: $(/usr/bin/grep -c . "$d/all"), of which added C4 lines: $(/usr/bin/grep -c ": >   C4 " "$d/all")"
dotfiles-T128-process-rules-a02.md: >   C4 allowed path has no threat_table row naming it: tests/unit/test_agmsg_orchestration_docs.py
dotfiles-T128-regime-counters-a01.md: >   C4 allowed path has no threat_table row naming it: scripts/check-regime-boundary.sh
dotfiles-T128-regime-counters-a02.md: >   C4 allowed path has no threat_table row naming it: scripts/check-regime-boundary.sh
dotfiles-T128-regime-counters-a02.md: >   C4 allowed path has no threat_table row naming it: tests/fixtures/regime-counters/**
format-2 files whose output differs: 3; differing lines: 4, of which added C4 lines: 4
[exit 0]
```
```console
$ IN="$MAIN/.orchestration/tasks/dotfiles-T128-task-checkers-a01-input/task-consistency-check.py"; same=0; differ=0; frames="^  File |^    |^ *\\^"; for f in $(/usr/bin/grep -L "^format: 2" .orchestration/tasks/*.md); do a=$(uv run --no-project --with pyyaml python -I "$IN" "$f" 2>&1 | sort | /usr/bin/grep -Ev "$frames"); b=$(uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py "$f" 2>&1 | sort | /usr/bin/grep -Ev "$frames"); if [[ $a == "$b" ]]; then same=$((same + 1)); else differ=$((differ + 1)); echo "DIFF $f"; fi; done; echo "other files (traceback frame lines dropped): same output $same, different $differ"
other files (traceback frame lines dropped): same output 309, different 0
[exit 0]
```
```console
$ d="$TMPDIR/ten"; rm -f "$d"/*.md 2> /dev/null; mkdir -p "$d"; uv run --no-project python -I -c "import pathlib, re, sys; b = re.split(r\"^# (dotfiles-T128-\\S+)\\n\", pathlib.Path(\"tests/fixtures/lessons/historical-front-matter.txt\").read_text(), flags=re.M); [pathlib.Path(sys.argv[1], t + \".md\").write_text(x) for t, x in zip(b[1::2], b[2::2])]" "$d"; uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root . "$d"/*.md | awk '/^dotfiles/ {if (n) print n, ids; n = $1; ids = ""; next} {match($0, /C[0-9]+b?/); c = substr($0, RSTART, RLENGTH); if (index(" " ids " ", " " c " ") == 0) ids = ids " " c} END {print n, ids}'
dotfiles-T128-ci-skip-orchestration-a01.md:  C2 C4 C6 C7
dotfiles-T128-ci-skip-orchestration-a02.md:  C2 C3 C4 C6 C7
dotfiles-T128-process-rules-a01.md:  C2 C6
dotfiles-T128-process-rules-a02.md:  C2 C4 C6 C7
dotfiles-T128-process-rules-a03.md:  C2 C4 C6 C7
dotfiles-T128-process-rules-a04.md:  C2 C4 C6 C7
dotfiles-T128-process-rules-a05.md:  C4 C6 C7
dotfiles-T128-process-rules-a06.md:  C4 C6 C7
dotfiles-T128-regime-counters-a01.md:  C2 C4 C6 C7
dotfiles-T128-regime-counters-a02.md:  C2 C3 C4 C6 C7
[exit 0]
```
```console
$ git show c3b617a4:scripts/orchestrator/task-consistency-check.py > "$TMPDIR/tcc-c3b617a4.py"; uv run --no-project --with pyyaml python -I "$TMPDIR/tcc-c3b617a4.py" --root . "$TMPDIR/ten"/*.md > "$TMPDIR/ten-before"; uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root . "$TMPDIR/ten"/*.md > "$TMPDIR/ten-after"; diff "$TMPDIR/ten-before" "$TMPDIR/ten-after"; echo "C4 lines before $(/usr/bin/grep -c "  C4 " "$TMPDIR/ten-before"), after $(/usr/bin/grep -c "  C4 " "$TMPDIR/ten-after")"
36a37
>   C4 allowed path has no threat_table row naming it: tests/unit/test_agmsg_orchestration_docs.py
96a98
>   C4 allowed path has no threat_table row naming it: scripts/check-regime-boundary.sh
112a115
>   C4 allowed path has no threat_table row naming it: scripts/check-regime-boundary.sh
114a118
>   C4 allowed path has no threat_table row naming it: tests/fixtures/regime-counters/**
C4 lines before 19, after 23
[exit 0]
```
```console
$ uv run --no-project --with pyyaml python -I -c "
import pathlib, re, sys, yaml
for f in sorted(pathlib.Path(sys.argv[1]).glob(\"*.md\")):
    rows = (yaml.safe_load(f.read_text().split(\"\\n---\\n\", 1)[0].lstrip(\"-\\n\")) or {}).get(\"threat_table\") or []
    fm = yaml.safe_load(f.read_text().split(\"\\n---\\n\", 1)[0].lstrip(\"-\\n\"))
    for a in fm.get(\"allowed_files\") or []:
        base = a.split(\"*\")[0].rstrip(\"/\")
        named = re.compile(re.escape(base) + r\"(?=$|[ /\\\"\\x27(),*?\\[])\")
        if any(named.search(r.get(\"control\") or \"\") for r in rows): continue
        for r in rows:
            for field in (\"control\", \"disposition\"):
                t = r.get(field) or \"\"
                if base in t: print(f\"{f.stem}: {a} appears only in a {field}: ...{t[max(0, t.find(base) - 30):t.find(base) + len(base) + 15]}...\")
" "$TMPDIR/ten"
dotfiles-T128-process-rules-a02: tests/unit/test_agmsg_orchestration_docs.py appears only in a disposition: ...ain judge every sentence, and tests/unit/test_agmsg_orchestration_docs.py pins each rule...
dotfiles-T128-regime-counters-a01: scripts/check-regime-boundary.sh appears only in a disposition: ...closed: the seams are flags, scripts/check-regime-boundary.sh never passes t...
dotfiles-T128-regime-counters-a02: scripts/check-regime-boundary.sh appears only in a disposition: ...closed: the seams are flags, scripts/check-regime-boundary.sh never passes t...
dotfiles-T128-regime-counters-a02: tests/fixtures/regime-counters/** appears only in a disposition: ...closed: tests/fixtures/regime-counters/* hold only th...
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
F1 badged review bodies not counted (thread 4266930617)	CAUGHT (unittest exit 1)
F2 bulleted audit lines not counted (thread 4266930623)	CAUGHT (unittest exit 1)
F3 C4 back to a substring match (thread 4266930635)	CAUGHT (unittest exit 1)
F4 C4 takes a dot as a boundary	CAUGHT (unittest exit 1)
A1 ledger refusal dropped	CAUGHT (unittest exit 1)
A2 default check is not the sibling	CAUGHT (unittest exit 1)
A3 override tracked check dropped	CAUGHT (unittest exit 1)
D1 SKILL line 73 reverted	CAUGHT (unittest exit 1)
D2 SKILL line 71 reverted	CAUGHT (unittest exit 1)
mutations 27 caught 27
 M .orchestration/dotfiles-T128-task-checkers-a01/sandbox.md
 M .orchestration/dotfiles-T128-task-checkers-a01/task.md
[exit 0]
```

## 9. Caps (amendment 2: the 200-line practice cap yields within INV-2's 500)

```console
$ git diff --numstat origin/main...HEAD -- . ':!.orchestration' | awk '{print; if ($3 ~ /^tests\//) {ta += $1; td += $2} else {xf++; xa += $1; xd += $2}} END {printf "outside tests and .orchestration: %d files, %d added + %d deleted = %d changed\nunder tests: %d added (cap 1000), %d deleted\n", xf, xa, xd, xa + xd, ta, td}'
2	2	home/dot_agents/skills/agmsg-orchestration/SKILL.md
37	0	scripts/orchestrator/ledger-check.py
6	8	scripts/orchestrator/orch-audit.sh
149	0	scripts/orchestrator/task-consistency-check.py
23	0	tests/fixtures/lessons/dotfiles-T128-process-rules-a05-audit-4af8939.md.last.txt
1	0	tests/fixtures/lessons/dotfiles-T128-process-rules-a05-pr-feedback.json
31	0	tests/fixtures/lessons/dotfiles-T128-process-rules-a05.record.txt
490	0	tests/fixtures/lessons/historical-front-matter.txt
2	2	tests/fixtures/regime/invariants.md
14	7	tests/unit/test_agmsg_orchestration_docs.py
27	0	tests/unit/test_orchestrator_tools.py
164	0	tests/unit/test_task_checkers.py
outside tests and .orchestration: 4 files, 194 added + 10 deleted = 204 changed
under tests: 752 added (cap 1000), 9 deleted
[exit 0]
```

## 10. CI and the Bot round on PR #352

These commands ran outside the sandbox, because gh fails TLS inside it.

- The Bot reviewed once, at `gh pr ready` (04:52:25Z), on head `63433cf1`. Its review raised four P1 threads; the Security Review finished with no comment.
- By the task's once-at-open rule, the fix heads `1ca0d5d1` and `612931f3` get no new Bot wait.
- `Unit test` failed on `c3b617a4` and `63433cf1` in `test (macos-14, client)` alone. The two Ubuntu client jobs were cancelled by fail-fast, and `test (ubuntu-24.04, server)` passed all five checker tests.

The cause: `uv run` puts its environment's and its base interpreter's `bin` directories before the caller's PATH (the listing below is local). So the stub `git` on the test's PATH loses to any `git` beside the interpreter. On the macOS runner that is evidently Homebrew's directory: the C8 to C10 probes got a real git's non-zero answers in a non-repository root. This is inferred from the listing and from the failure pattern; it was not reproduced, since the reproduction command was denied (sandbox record).

`1ca0d5d1` sets PATH inside `uv run`, right before python starts. Its CI is 13 of 13 green, `test (macos-14, client)` included.

```console
$ PATH="/stubdir:$PATH" uv run --no-project --with pyyaml python -I -c 'import os; print("\n".join(os.environ["PATH"].split(":")[:4]))' | sed "s#$HOME#~#g"
~/.cache/uv/builds-v0/.tmpgmZ3cx/bin
~/.cache/uv/archive-v0/jSialj41YAM_22Nh/bin
~/.local/share/mise/installs/python/latest/bin
/stubdir
[exit 0]
```
```console
$ gh run list --repo mryfmo/dotfiles --branch regime/task-checkers --workflow "Unit test" --json headSha,conclusion,databaseId --jq ...
1ca0d5d1	success	38515532822
63433cf1	failure	38513653854
c3b617a4	failure	38513225179
[exit 0]
```
```console
$ gh run view 38513653854 --repo mryfmo/dotfiles --json jobs --jq ...
test (ubuntu-26.04, client)	cancelled
test (ubuntu-24.04, server)	success
test (ubuntu-24.04, client)	cancelled
test (macos-14, client)	failure
[exit 0]
```
```console
$ gh run view 38513653854 --repo mryfmo/dotfiles --log-failed | grep -E "FAIL: |AssertionError|  C8 the task|Ran [0-9]+ tests" | cut -f3- | cut -c1-200
2026-10-14T04:58:10.9576910Z FAIL: test_task_consistency_check_passes_a_complete_task_file (test_task_checkers.TaskCheckersTest.test_task_consistency_check_passes_a_complete_task_file)
2026-10-14T04:58:10.9594260Z AssertionError: 0 != 1 : t-a01.md: FAIL
2026-10-14T04:58:10.9594620Z   C8 the task adds input REVIEW_EVIDENCE but no threat row controls it
2026-10-14T04:58:10.9595750Z FAIL: test_task_consistency_check_reaches_every_other_check (test_task_checkers.TaskCheckersTest.test_task_consistency_check_reaches_every_other_check) (check='C10')
2026-10-14T04:58:10.9599800Z AssertionError: 'C10' not found in {'C9'}
2026-10-14T04:58:10.9600460Z Ran 1071 tests in 282.524s
[exit 0]
```
```console
$ gh pr checks 352 --repo mryfmo/dotfiles | cut -f1,2 | sort
CodeRabbit	pass
GitGuardian Security Checks	pass
private-bootstrap (macos-14, client)	pass
private-bootstrap (ubuntu-24.04, client)	pass
private-bootstrap (ubuntu-24.04, server)	pass
public-bootstrap (macos-14, client)	pass
public-bootstrap (ubuntu-24.04, client)	pass
public-bootstrap (ubuntu-24.04, server)	pass
test (macos-14, client)	pass
test (ubuntu-24.04, client)	pass
test (ubuntu-24.04, server)	pass
test (ubuntu-26.04, client)	pass
validate	pass
[exit 0]
```
```console
$ gh api --paginate repos/mryfmo/dotfiles/pulls/352/reviews --jq (the Codex Bot reviews: id, commit, time, state)
5513241585	63433cf11438647e519f5382f4667182bcd70572	2026-10-14T04:55:40Z	COMMENTED
[exit 0]
```
```console
$ gh api --paginate repos/mryfmo/dotfiles/pulls/352/comments --jq (the Codex Bot top-level comments: id, commit, path, badge, title)
4266930617	63433cf1	scripts/orchestrator/ledger-check.py	P1	Include badged review findings in the ledger**
4266930623	63433cf1	scripts/orchestrator/ledger-check.py	P1	Count Markdown-bulleted audit findings**
4266930635	63433cf1	scripts/orchestrator/task-consistency-check.py	P1	Require exact allowed-path coverage in C4**
4266930643	63433cf1	.orchestration/dotfiles-T128-task-checkers-a01/task.md	P1	Bind the checker row to tests that close the whole control**
[exit 0]
```
```console
$ gh api --paginate repos/mryfmo/dotfiles/issues/352/comments --jq (the Codex Bot issue comments: id, time, review lines)
6161179355	2026-10-14T04:52:54Z	| 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-14T04:55:44.230617Z">2026-10-14T04:55:44.230617Z</relative-time> | `63433cf` | Draft marked ready | / | 🔒 **Security Review** | ✅ **Completed** <relative-time datetime="2026-10-14T04:58:58.476544Z">2026-10-14T04:58:58.476544Z</relative-time> | `63433cf` | Draft marked ready |
[exit 0]
```

Dispositions of the four Bot threads, fixed in the one round that amendment 2 allows (`612931f3`; each fix's mutation, F1 to F3, is caught in section 8):

| Thread | Finding | Disposition |
|---|---|---|
| 4266930617 | `ledger-check.py` ignored badged Codex Bot `review` bodies, which the gate's `swept_finding_ids()` counts | `fixed:612931f3`: a Codex Bot `review` item whose body holds a `![P<n> Badge]` token counts, keyed by its `pullrequestreview-<id>`. Test: `test_ledger_check_counts_what_the_gate_counts`. |
| 4266930623 | `ledger-check.py` counted no bulleted `- [P1]` audit line, which the gate's `AUDIT_FINDING` accepts | `fixed:612931f3`: the gate's regex, verbatim. Same test. |
| 4266930635 | C4's substring match let `scripts/foo.py.bak` cover `scripts/foo.py` | `fixed:612931f3`: a row's control names the entry only where the prefix is followed by the end of the control, a space, `/`, `"`, `'`, `(`, `)`, `,` or a glob character. Test: `test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary`. On the ten files the sets of premise 1 stay (section 6); four C4 lines are added in three files whose sets already held C4, each for an entry named only in a disposition. |
| 4266930643 | The checker's closed row cited one test for C1 to C10 | `fixed:612931f3`: amendment 2 splits the row into four closed rows plus the ledger alignments' row. Their selectors are the tests this commit carries; the task copy is refreshed to `a309b394`. |

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

The mutation pass of section 8 (`$TMPDIR/t704/mutate.py`): each mutation replaces one exact string, runs the named tests, and restores the file in a `finally`. F1 to F3 put back the pre-fix forms of the three amendment-2 alignments.

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
    ("M5 C4 off", TCC, "if rows and not any(named.search(r.get(\"control\") or \"\") for r in rows):", "if False:", CHECKERS),
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
    ("L3 [P3] lines not counted", LC, r"(?:[-*+]\s+)?\[P[0-3]\]", r"(?:[-*+]\s+)?\[P[0-2]\]", CHECKERS),
    ("L4 exit always 0", LC, "return 1 if gaps else 0", "return 0", CHECKERS),
    ("F1 badged review bodies not counted (thread 4266930617)", LC, 'elif item["source"] == "review" and', 'elif False and item["source"] == "review" and', CHECKERS),
    ("F2 bulleted audit lines not counted (thread 4266930623)", LC, r"^\s*(?:[-*+]\s+)?\[P[0-3]\]", r"^\[P[0-3]\]", CHECKERS),
    ("F3 C4 back to a substring match (thread 4266930635)", TCC, "if rows and not any(named.search(r.get(\"control\") or \"\") for r in rows):", "if rows and a.split(\"*\")[0].rstrip(\"/\") not in rowtext:", CHECKERS),
    ("F4 C4 takes a dot as a boundary", TCC, r"""(?=$|[ /\"'(),*?\[])""", r"""(?=$|[ ./\"'(),*?\[])""", CHECKERS),
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
