# T13 amendment 5 implementation validation

Previous head: 4d3d639f452e12e22c434ce62f843e0e22dc39e0
Task SHA256: 4610a9a7c064a5d93fb72b91df73c42390051a1fcb35703a6cf5aed305ef08a9
Check: tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationRuleTest::test_boundary_cadence_is_stated_between_integrations

This is the implementation snapshot committed with the revised source. New-head CI/Bot and its commit SHA can only be collected after publication; RESULT records that successor proof separately. Outputs are home-masked and trailing whitespace is normalized.

## New required cadence test red before prose edits (exit 1)

```text
test_boundary_cadence_is_stated_between_integrations (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_boundary_cadence_is_stated_between_integrations) ... FAIL

======================================================================
FAIL: test_boundary_cadence_is_stated_between_integrations (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_boundary_cadence_is_stated_between_integrations)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_agmsg_orchestration_docs.py", line 82, in test_boundary_cadence_is_stated_between_integrations
    self.assertIn("records reach `main` only between integrations (plan 020 step 3)", RULE.read_text())
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'records reach `main` only between integrations (plan 020 step 3)' not found in '## agmsg orchestration\n\nInvariants only; every procedure lives in the `agmsg-orchestration` skill, in the sections named below.\n\n- **Activation.** When the operator asks for agmsg collaboration, or the agmsg bus and a seated worker exist here, invoke the `agmsg-orchestration` skill. Only the operator opts out, for the current task. Without a seated worker, seat one (`herdr-agents --add-worker [<worktree>]`) before any repository mutation; "no worker" is never an implicit opt-out ("Regime activation and progress").\n- **Delegation.** Every repository mutation goes to a seated worker of the manifest\'s `worker_kind`. The orchestrator itself reads, judges, tasks, accepts and integrates, and acts directly only under a declared exemption: agmsg/herdr control plane, evidence-sync bookkeeping, final integration, or machine hygiene that touches no repository, or after the operator\'s explicit opt-out for the current task ("Parallel workers"). The canonical chezmoi clone is pull and apply only: no seat edits it, and nothing is applied from a dirty source tree.\n- **Acceptance.** Acceptance, adversarial RESULT review, review-profile work and `make require-crit-review` stay with the orchestrator and are never delegated. Every RESULT that changes repository code gets one task-level audit of its final head; audit findings are input, never approval (the "Task-level audit" bullet).\n- **Permissions.** A worker completes every command inside its sandbox, except the few commands Worker Playbook step 4 sends through the permission gate; any other action outside it fails and is reported as `AGMSG-PONG v1 status=blocked`. Agent-to-agent permission approval is forbidden; only the human operator answers a permission prompt (Worker Playbook step 4).\n- **`main`.** The orchestrator never pushes a repository change to `main` directly. Every change lands through a pull request the orchestrator merges on GitHub with `gh pr merge --squash --match-head-commit <audited head sha>` (Orchestrator Playbook step 10).\n- **Identity.** Each worker identity registers at its worktree path with `AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>`. Message and wake paths (`agmsg-dispatch`, `poke.sh` or `send.sh` with `--body-file`, `inbox.sh`; never retry a `poke.sh` exit 13 as `send.sh`) are in Orchestrator Playbook step 6 and "Identity, delivery, and storage".\n- **Parallelism.** Concurrent tasks need pairwise-disjoint `allowed_files`: disjoint code tasks run concurrently while overlapping code files run serially, shared prose files only in non-overlapping sections, and the later PR takes the new base with `gh pr update-branch` ("Parallel workers").\n- **Routing.** A seat never edits the source of its own execution boundary: Claude-boundary changes go to a Codex seat, Codex-boundary changes to a Claude seat, and shared sources or permgate to the operator (Orchestrator Playbook step 3).\n- **Boundaries.** At every regime or session boundary, run the Stop checklist ("Review and integration invariants"), which `make check-regime-boundary` checks; records reach `main` at most once a day (plan 020 step 3). Codify session lessons through a task, never auto-memory.\n'

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

## uv run python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v (exit 0)

```text
test_docs_no_longer_name_codex_review_commit (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_docs_no_longer_name_codex_review_commit) ... ok
test_rule_and_skill_name_worker_seats_not_codex_workers (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_rule_and_skill_name_worker_seats_not_codex_workers) ... ok
test_rule_drops_the_worker_network_escalation (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_rule_drops_the_worker_network_escalation) ... ok
test_skill_drops_the_pane_status_gate_and_raw_pane_wakes (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationForbiddenPhrasesTest.test_skill_drops_the_pane_status_gate_and_raw_pane_wakes) ... ok
test_boundary_cadence_is_stated_between_integrations (tests.unit.test_agmsg_orchestration_docs.AgmsgOrchestrationRuleTest.test_boundary_cadence_is_stated_between_integrations) ... ok
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
test_advisory_rows_are_excluded_from_the_class_counts (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_advisory_rows_are_excluded_from_the_class_counts) ... ok
test_an_incorrect_audit_is_dispositioned_in_audit_findings (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_an_incorrect_audit_is_dispositioned_in_audit_findings) ... ok
test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first) ... ok
test_boundary_merge_sentence_names_the_in_job_decision (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_boundary_merge_sentence_names_the_in_job_decision) ... ok
test_closed_selector_existence_is_checked_at_acceptance (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_closed_selector_existence_is_checked_at_acceptance) ... ok
test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestration_records_and_threat_tables) ... ok
test_counters_bullet_names_owners_not_sources (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_bullet_names_owners_not_sources) ... ok
test_counters_run_before_every_acceptance_action (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_run_before_every_acceptance_action) ... ok
test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) ... ok
test_dispatches_are_recorded_from_the_bus (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_dispatches_are_recorded_from_the_bus) ... ok
test_open_review_body_findings_have_an_identifier (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_open_review_body_findings_have_an_identifier) ... ok
test_orchestration_records_rule_binds_the_bot_review_only (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_orchestration_records_rule_binds_the_bot_review_only) ... ok
test_pattern_rules_pin_their_safeguards (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_pattern_rules_pin_their_safeguards) ... ok
test_question_pongs_are_in_the_contract (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_question_pongs_are_in_the_contract) ... ok
test_regime_rule_sections_are_pinned_whole (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_regime_rule_sections_are_pinned_whole) ... ok
test_rule_changes_travel_as_task_amendments (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_rule_changes_travel_as_task_amendments) ... ok
test_shape_is_checked_by_hand (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_is_checked_by_hand) ... ok
test_shape_rules_and_the_decision_sentence_are_pinned (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_rules_and_the_decision_sentence_are_pinned) ... ok
test_skill_names_no_unlanded_mechanism (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_skill_names_no_unlanded_mechanism) ... ok
test_skill_sandbox_text_names_both_platforms (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_skill_sandbox_text_names_both_platforms) ... ok
test_step_10_states_the_advisory_p2_policy (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_step_10_states_the_advisory_p2_policy) ... ok
test_surviving_fix_round_threads_stop_for_the_operator (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_surviving_fix_round_threads_stop_for_the_operator) ... ok
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
Ran 53 tests in 0.016s

OK
```

## make render-check (exit 0)

```text
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
generated agent configs are up to date
```

## git numstat, D6/retired name counts, words, caps, task hashes, diff-check and Crit status

```text
15	0	.orchestration/dotfiles-T128-rules-step8-a01/dotfiles-T128-rules-step8-a01-worker-crit.json
6	0	.orchestration/dotfiles-T128-rules-step8-a01/dotfiles-T128-rules-step8-a01-worker-review-receipt.md
4	0	.orchestration/dotfiles-T128-rules-step8-a01/revise.yaml
157	0	.orchestration/dotfiles-T128-rules-step8-a01/task.md
2	2	AGENTS.md
20	17	home/dot_agents/skills/agmsg-orchestration/SKILL.md
1	1	home/dot_config/claude/rules/agmsg-orchestration.md
2	2	home/dot_config/claude/rules/pr-integration.md
1	1	tests/fixtures/regime/code-review-orchestration.md
6	6	tests/fixtures/regime/invariants.md
1	1	tests/fixtures/regime/message-contract.md
3	3	tests/fixtures/regime/worker-step-15.md
56	25	tests/unit/test_agmsg_orchestration_docs.py
home/dot_agents/skills/agmsg-orchestration/SKILL.md D6= 0 AUDIT_DISPOSITIONS= 0
AGENTS.md D6= 0 AUDIT_DISPOSITIONS= 0
rule words: 447
source changed lines: 47 <=200; test additions: 67 <=1000
4610a9a7c064a5d93fb72b91df73c42390051a1fcb35703a6cf5aed305ef08a9  .orchestration/dotfiles-T128-rules-step8-a01/task.md
4610a9a7c064a5d93fb72b91df73c42390051a1fcb35703a6cf5aed305ef08a9  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-rules-step8-a01.md
{
  "branch": "fix/regime-rules-step8",
  "daemon": {
    "running": false
  },
  "review_file": "~/.crit/reviews/aa925ad8a1cc/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}
```
