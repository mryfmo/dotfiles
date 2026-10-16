# T13 amendment6 implementation validation

Previous head: 61dbd68e6bb72b1bc0420f3e1b93b7c064fdbce3
Task SHA256: 03544af5abdfc292683383f0548109254e3928b92528dd3cb927126bb9f65c66
Corrected ACCEPTANCE check: tests/unit/test_agmsg_orchestration_docs.py::AgmsgRegimePatternTest::test_step_10_states_the_advisory_p2_policy
regression_check: tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationRuleTest::test_boundary_cadence_is_stated_between_integrations

The initial ACCEPTANCE used the unchanged cadence selector; the worker reported this and the 03:47:05Z corrected ACCEPTANCE names the actual review-count test as check and cadence as regression_check. revise.yaml matches the corrected message. The count test below failed before prose changes and passes after; both selectors pass in the full53-test run. This snapshot is committed with source; publication commit/CI/Bot are necessarily collected afterward and reported separately by RESULT. Output home paths and trailing whitespace are normalized.

## Actual review-count regression red on61dbd68e before prose (exit1)

```text
test_step_10_states_the_advisory_p2_policy (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_step_10_states_the_advisory_p2_policy) ... FAIL

======================================================================
FAIL: test_step_10_states_the_advisory_p2_policy (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_step_10_states_the_advisory_p2_policy)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_agmsg_orchestration_docs.py", line 281, in test_step_10_states_the_advisory_p2_policy
    self.assertIn("bot_rounds=2", self.section(skill, "\n15. After the final push"))
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'bot_rounds=2' not found in ', wait for CI and the Codex Bot before sending RESULT. The Bot reviews at PR open and, after the one P0/P1 fix round, once more on `@codex review`; the review count is 1 + the fix rounds (plan 020 step 2).\n    - Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a draft (`gh pr ready` exits non-zero on a PR that is already ready, so a later head\'s wait skips it): the Codex Bot reviews non-draft PRs, and a draft only on an explicit `@codex review` comment. When no Bot review of the final head arrives within 10 minutes, post `@codex review` on the PR and wait out the rest of the window.\n    - Run `gh pr checks <pr> --watch` in the background and the Bot wait below at the same time: the 10-minute and 15-minute marks count from `gh pr ready` (from the push, for a later head), never from the end of CI. Right after a push GitHub can report no checks yet, and the watcher then exits 1 with `no checks reported`: start it once a check is listed, and restart it on that message instead of reading it as a CI failure. Wait for that watcher\'s exit status before the RESULT: a non-zero exit means no RESULT until CI passes.\n    - Then list the Bot\'s reviews of the final head with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/reviews --jq \'.[]|select(.user.login=="chatgpt-codex-connector[bot]" and .commit_id=="<head-sha>")|[.commit_id,.submitted_at]|@tsv\'` and the Bot\'s top-level review comments raised on it with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/comments --jq \'.[]|select(.in_reply_to_id == null and .user.login=="chatgpt-codex-connector[bot]" and .original_commit_id=="<head-sha>")|[.id,.original_commit_id,.path]|@tsv\'`. A human comment, a CodeRabbit review or an earlier head\'s review never ends the wait. A comment\'s `commit_id` moves to the newest head, so findings are matched by `original_commit_id`. Repeat until a review of the final head appears or 15 minutes pass; the report records the latter as `bot: none`. The final head here is the diff head, the last commit that changes the PR\'s content: a head that only merges the new base with `gh pr update-branch` needs green CI but no new Bot wait. Both endpoints return 30 items per page by default, so keep `--paginate`.\n    - This bounded wait is the permitted exception to the no-polling rule in "Regime activation and progress", which governs detecting worker completion and pane status, not a worker\'s wait on CI and the Bot. List at most every 30 seconds, stop at 15 minutes, and run the loop as a background command or a foreground command with a timeout. Never use bare foreground `sleep`.\n    - A 👍 reaction alone is not evidence of a review.\n    - Read each listed review\'s body too: the Codex Bot sometimes places a finding (a `P0`–`P3` badge with a blob link) in the review body instead of an inline thread. Such a review-body finding is listed alongside the top-level inline comments and fixed or dispositioned the same way.\n    - Fix P0/P1 findings, inline or review-body, in at most one worker-side fix round before RESULT, then request `@codex review` and restart the wait from the push. A P0/P1 surviving that round is not fixed again: send `AGMSG-RESULT … bot_rounds=1` with each listed as `open:<thread id>` (`open:review-<review id>` for a review-body finding); this stops the PR for the operator\'s decision, and the next bullet\'s `fixed:`/`not-applicable:` rule does not override it.\n    - Apart from those surviving P0/P1 items, the RESULT names every unresolved thread id with `fixed:<sha>` or a proposed `not-applicable:<reason>` under Orchestrator Playbook step 10. The worker resolves no thread.\n'

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

## uv run python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v (exit0)

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
Ran 53 tests in 0.010s

OK
```

## make render-check and native format/diff checks (exit0)

```text
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
generated agent configs are up to date
1 file already formatted
```

## Numstat/caps/D6/count/word/task-hash/Crit checks

```text
21	0	.orchestration/dotfiles-T128-rules-step8-a01/dotfiles-T128-rules-step8-a01-worker-crit.json
6	0	.orchestration/dotfiles-T128-rules-step8-a01/dotfiles-T128-rules-step8-a01-worker-review-receipt.md
5	0	.orchestration/dotfiles-T128-rules-step8-a01/learning.md
19	0	.orchestration/dotfiles-T128-rules-step8-a01/report.md
6	0	.orchestration/dotfiles-T128-rules-step8-a01/revise.yaml
3	0	.orchestration/dotfiles-T128-rules-step8-a01/sandbox.md
161	0	.orchestration/dotfiles-T128-rules-step8-a01/task.md
132	0	.orchestration/dotfiles-T128-rules-step8-a01/validation.md
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
home/dot_agents/skills/agmsg-orchestration/SKILL.md bot_rounds1= 0 bot_rounds2= 2
tests/fixtures/regime/worker-step-15.md bot_rounds1= 0 bot_rounds2= 1
tests/fixtures/regime/message-contract.md bot_rounds1= 0 bot_rounds2= 1
tests/unit/test_agmsg_orchestration_docs.py bot_rounds1= 0 bot_rounds2= 2
03544af5abdfc292683383f0548109254e3928b92528dd3cb927126bb9f65c66  .orchestration/dotfiles-T128-rules-step8-a01/task.md
03544af5abdfc292683383f0548109254e3928b92528dd3cb927126bb9f65c66  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-rules-step8-a01.md
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
