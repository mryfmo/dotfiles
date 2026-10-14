---
task_id: dotfiles-T128-playbook-rules-followup-a01
seat: claude-standard-dot-a002
rule_commit: 7a282f3b
---

# Validation: dotfiles-T128-playbook-rules-followup-a01

Every command ran from the worktree `.claude/worktrees/worker-f` inside the sandbox, with `MAIN` naming the main checkout and `UV_OFFLINE=1` set (uv cannot reach pypi from the sandbox). The output is verbatim; each block ends with the command's exit status. Captured at `7a282f3b`, before the PR was opened.

Changed tests: `test_dispatches_are_recorded_from_the_bus` (step 6's sentence), `test_the_gate_reads_the_acceptance_record` (step 10.3 and 10.4) and `test_an_incorrect_audit_is_dispositioned_in_audit_findings` (new: the task-level audit bullet and AGENTS.md's gate sentence). Changed fixtures (`test_regime_rule_sections_are_pinned_whole`): `tests/fixtures/regime/orchestrator-step-6.md` and `tests/fixtures/regime/invariants.md`, each in the one changed sentence.

## 1. Task file and task copy

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md" .orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md | sed "s#$MAIN/##"; cmp "$MAIN/.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md" .orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md && echo byte-identical
ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b  .orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md
ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b  .orchestration/dotfiles-T128-playbook-rules-followup-a01/task.md
byte-identical
[exit 0]
```

## 2. Branch and the owned section (item 1's definition)

```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
7a282f3b docs(agmsg-orchestration): the record before the first dispatch; audit_findings replaces AUDIT_DISPOSITIONS (T703 a04 owner rows)
c15ba668da20dc2956220077cb0f20054ab352c7
[exit 0]
```
```console
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md | shasum -a 256; git show origin/main:.orchestration/acceptance/dotfiles-T128-playbook-rules-a04.md | awk '/^## Owned by dotfiles-T128-playbook-rules-followup-a01/ {p = 1} p && /^(local|audit):[0-9a-f]{7}:[0-9]+\t/'
3bfd13d7c9e2b381e3de118b6f717d9025ce2b67f5b2bc08b844d0486613e5ec  -
local:65a3d71:1	rule-gap
audit:71eb920:1	procedure-migration (the SKILL step 10.4 gate command still names AUDIT_DISPOSITIONS; from the audit of PR #329's head)
audit:65a3d71:1	disposition-range
audit:65a3d71:2	rule-gap
[exit 0]
```

## 3. The retired gate input before and after

```console
$ for f in home/dot_agents/skills/agmsg-orchestration/SKILL.md AGENTS.md tests/fixtures/regime/invariants.md; do echo "== origin/main:$f"; git show "origin/main:$f" | /usr/bin/grep -n "AUDIT_DISPOSITIONS\|audit-finding" | cut -c1-140; echo "== HEAD:$f"; /usr/bin/grep -n "AUDIT_DISPOSITIONS\|audit-finding" "$f" | cut -c1-140; done
== origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md
90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n>
171:    3. Write the acceptance record, summarising the dispositions, with an `audit-finding:` line for every audit finding whatever the ver
172:    4. Run the gate: `AUDIT_EVIDENCE=<audit> [AUDIT_DISPOSITIONS=<acceptance record>] AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTA
178:       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedb
== HEAD:home/dot_agents/skills/agmsg-orchestration/SKILL.md
90:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's or
171:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet 
== origin/main:AGENTS.md
44:- Before merging a pull request, follow the integration order in the agmsg-orchestration SKILL's Orchestrator Playbook step 10 and `home/
== HEAD:AGENTS.md
== origin/main:tests/fixtures/regime/invariants.md
27:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict: exactly one `audit-finding: <n>
== HEAD:tests/fixtures/regime/invariants.md
27:  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's or
[exit 0]
```
```console
$ git grep -n "RETIRED_AUDIT_DISPOSITIONS_ENV =\|^FAILURE_REASON_MIN_CHARS\|def audit_findings_errors" -- scripts/require-crit-review.py; /usr/bin/grep -n "audit-dispositions" scripts/orchestrator/acceptance-front-matter.py | head -3; /usr/bin/grep -n "is not an existing regular file\|whose .task. is not" scripts/orchestrator/dispatch.sh
scripts/require-crit-review.py:26:RETIRED_AUDIT_DISPOSITIONS_ENV = "AUDIT_DISPOSITIONS"
scripts/require-crit-review.py:33:FAILURE_REASON_MIN_CHARS = 20
scripts/require-crit-review.py:705:def audit_findings_errors(record: dict | None, findings: int) -> list[str]:
1:"""acceptance-front-matter.py <task> <sweep-json> <pr-worktree> [--ledger <tsv>] [--audit-dispositions <tsv>]
9:`--audit-dispositions` (`n<TAB>reason<TAB>evidence`), required when the audit summary orch-audit.sh writes beside
51:    parser.add_argument("--audit-dispositions")
34:#   (thread 4255272797). A record that is not an existing regular file writable in a
35:#   writable directory, or whose `task` is not the line's `task_id`, is refused
[exit 0]
```

## 4. The Validation command

```console
$ uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v
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
Ran 48 tests in 0.012s

OK
[exit 0]
```

## 5. Formatting

```console
$ prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md AGENTS.md tests/fixtures/regime/*.md; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py
Checking formatting...
All matched files use Prettier code style!
1 file already formatted
[exit 0]
```

## 6. The changed tests and fixtures

```console
$ git diff origin/main...HEAD --stat -- tests; git diff origin/main...HEAD -- tests/unit/test_agmsg_orchestration_docs.py | /usr/bin/grep "^@@\|^+    def \|^ *def test" | cut -c1-140
 tests/fixtures/regime/invariants.md          |  2 +-
 tests/fixtures/regime/orchestrator-step-6.md |  2 +-
 tests/unit/test_agmsg_orchestration_docs.py  | 52 +++++++++++++++++++++++++---
 3 files changed, 50 insertions(+), 6 deletions(-)
@@ -522,7 +522,12 @@ class AgmsgRegimePatternTest(unittest.TestCase):
@@ -629,11 +634,50 @@ class AgmsgRegimePatternTest(unittest.TestCase):
     def test_the_gate_reads_the_acceptance_record(self) -> None:
+    def test_an_incorrect_audit_is_dispositioned_in_audit_findings(self) -> None:
[exit 0]
```

## 7. Caps (INV-2)

```console
$ git diff --numstat origin/main...HEAD -- . ':!.orchestration' | awk '{print; f++; if ($3 ~ /^tests\//) t += $1; else x += $1} END {printf "files outside .orchestration: %d (cap 15); added outside tests: %d (cap 500); added under tests: %d (cap 1000)\n", f, x, t}'
1	1	AGENTS.md
5	5	home/dot_agents/skills/agmsg-orchestration/SKILL.md
1	1	tests/fixtures/regime/invariants.md
1	1	tests/fixtures/regime/orchestrator-step-6.md
48	4	tests/unit/test_agmsg_orchestration_docs.py
files outside .orchestration: 5 (cap 15); added outside tests: 6 (cap 500); added under tests: 50 (cap 1000)
[exit 0]
```
