# Validation: dotfiles-T128-playbook-rules-a04

Seat `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `regime/playbook-rules`, PR #328. The branch was fast-forwarded from the worker's `fe34f7db` to the orchestrator's update-branch head `e12872cd` before any edit. `origin/main` is `3709a6d8`, and the merge-base is `e0e2fe62`. Every block is verbatim command output; `mise WARN` sandbox cache lines are filtered out.

## 1. Branch and task copies

```text
$ git merge-base --is-ancestor fe34f7db e12872cd && echo "fast-forward"; git log --oneline e12872cd..HEAD
fast-forward
beee078a docs(regime): state the dispatch and three-repeat obligations, and leave their commands to T718's scripts
ff2e7156 chore(orchestration): record the dotfiles-T128-playbook-rules-a04 task
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md .orchestration/dotfiles-T128-playbook-rules-a04/task.md
e64ee6912c33d98305e70b4206f4d0f55bd4236730131a080f0fd81e7227f254  <main checkout>/.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md
e64ee6912c33d98305e70b4206f4d0f55bd4236730131a080f0fd81e7227f254  .orchestration/dotfiles-T128-playbook-rules-a04/task.md
$ cmp <main checkout>/.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md .orchestration/dotfiles-T128-playbook-rules-a04/task.md && echo identical
identical
$ for t in a01:1083a8c1 a02:4486dbdd a03:196d73ca; do git diff --quiet ${t#*:} HEAD -- .orchestration/dotfiles-T128-playbook-rules-${t%%:*}/task.md && echo "${t%%:*} copy unchanged since ${t#*:}"; done
a01 copy unchanged since 1083a8c1
a02 copy unchanged since 4486dbdd
a03 copy unchanged since 196d73ca
```

## 2. Premises of the new sentences

```text
$ git diff --stat $(git merge-base HEAD origin/main) origin/main -- home/ AGENTS.md tests/ scripts/ Makefile | tail -1; echo "(empty: main moved only under .orchestration)"
(empty: main moved only under .orchestration)
$ git ls-tree -r --name-only origin/main scripts/orchestrator/ | wc -l   # T718 has not landed
       0
$ git ls-remote https://github.com/mryfmo/dotfiles 'refs/heads/regime/gate-evidence*'
4e2266aae7cddb692a9d56d8a8d2c83e48cc8303	refs/heads/regime/gate-evidence
$ history.sh dotfiles-conformance 2>/dev/null | wc -l; history.sh dotfiles-conformance --limit 1000 2>/dev/null | wc -l; history.sh dotfiles-conformance "" 1000 2>/dev/null | wc -l   # item 1 interim form
      20
     778
     778
$ sed -n "7,9p;45p" ~/.agents/skills/agmsg/scripts/history.sh; awk '/^(function )?storage_history/{p=1} p{n++; if(n>=8 && n<=12) print} n>12{exit}' ~/.agents/skills/agmsg/scripts/drivers/storage/jsonl.sh   # why --limit 1000 reads everything: history.sh passes --limit as the agent, storage_history skips a dash-led agent, then takes the second --limit as the limit value, which is non-numeric, so the limit is -1 (none)
TEAM="${1:?Usage: history.sh <team> [agent_id] [limit]}"
AGENT="${2:-}"
LIMIT="${3:-20}"
HIST_JSONL=$(storage_history "$TEAM" "$AGENT" --limit "$LIMIT")
  local team="$1"; shift
  local agent="" limit=""
  if [ $# -gt 0 ] && [ "${1#-}" = "$1" ]; then agent="$1"; shift; fi
  while [ $# -gt 0 ]; do case "$1" in --limit) limit="$2"; shift 2 ;; *) shift ;; esac; done
  case "$limit" in ''|*[!0-9]*) limit="-1" ;; esac
```

## 3. Every quoted sentence of the task is in the prose verbatim

```text
$ uv run --no-project python "$TMPDIR/verbatim.py" "$PWD" .orchestration/dotfiles-T128-playbook-rules-a04/task.md
item 1 quote 1: present (ok) 730 chars
item 2 quote 1: present (ok) 33 chars
item 2 quote 2: present (ok) 240 chars
item 3 quote 1: present (ok) 1035 chars
item 4 quote 1: present (ok) 544 chars
item 4 quote 2: present (ok) 40 chars
item 4 quote 3: present (ok) 173 chars
item 5 quote 1: absent (ok) 73 chars
item 5 quote 2: present (ok) 184 chars
```

## 4. Docs tests

```text
$ uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v
test_docs_no_longer_name_codex_review_commit ... ok
test_rule_and_skill_name_worker_seats_not_codex_workers ... ok
test_rule_drops_the_worker_network_escalation ... ok
test_skill_drops_the_pane_status_gate_and_raw_pane_wakes ... ok
test_rule_pointers_name_real_skill_sections ... ok
test_rule_states_the_invariants ... ok
test_word_budgets ... ok
test_audit_command_lives_only_in_the_task_level_audit_bullet ... ok
test_codex_agents_points_at_the_worklog_section ... ok
test_contextdb_cli_is_invoked_with_uv_run ... ok
test_skill_masks_evidence_with_a_runnable_command ... ok
test_claude_worker_merge_denials_and_prefix_limits_are_documented ... ok
test_codex_worker_profile_defaults_to_standard ... ok
test_skill_carries_the_audit_gate_and_bot_wait_mechanics ... ok
test_skill_carries_the_parallel_execution_and_routing_mechanics ... ok
test_skill_carries_the_registration_and_delivery_mechanics ... ok
test_skill_carries_the_session_lessons ... ok
test_a_design_lands_on_main_before_its_task ... ok
test_a_revise_acceptance_names_the_previous_head_and_a_check ... ok
test_a_trust_boundary_task_carries_a_threat_table ... ok
test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first ... ok
test_boundary_merge_sentence_names_the_in_job_decision ... ok
test_closed_selector_existence_is_checked_at_acceptance ... ok
test_code_review_rules_cover_orchestration_records_and_threat_tables ... ok
test_counters_bullet_names_owners_not_sources ... ok
test_counters_run_before_every_acceptance_action ... ok
test_design_review_runs_in_paired_rounds_with_a_cap ... ok
test_dispatches_are_recorded_from_the_bus ... ok
test_open_review_body_findings_have_an_identifier ... ok
test_open_third_round_threads_have_an_integration_outcome ... ok
test_orchestration_records_rule_binds_the_bot_review_only ... ok
test_pattern_rules_pin_their_safeguards ... ok
test_question_pongs_are_in_the_contract ... ok
test_regime_rule_sections_are_pinned_whole ... ok
test_rule_changes_travel_as_task_amendments ... ok
test_shape_is_checked_by_hand_until_the_schema_lands ... ok
test_shape_rules_and_the_decision_sentence_are_pinned ... ok
test_task_file_review_is_one_round_with_a_fixed_stop_condition ... ok
test_the_bot_wait_filters_the_codex_bot ... ok
test_the_ci_watch_is_joined_before_the_result ... ok
test_the_ci_watcher_survives_the_no_checks_race ... ok
test_the_gate_reads_the_acceptance_record ... ok
test_threat_table_rows_have_a_fixed_unit ... ok
test_threat_table_rule_carries_no_grammar ... ok
test_three_repeats_start_with_a_pasted_correction_search ... ok
test_workers_commit_inside_the_sandbox ... ok
test_workers_open_the_pr_as_a_draft ... ok

----------------------------------------------------------------------
Ran 47 tests in 0.009s

OK
```

## 5. The module that pins the gate command, and format

```text
$ uv run --no-project python -m unittest tests/unit/test_pr_feedback.py 2>&1 | tail -n 3
Ran 16 tests in 0.017s

OK
$ ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py
1 file already formatted
```

## 6. Each sentence fails its test when removed or put back to its previous form

`mutate.py` (session scratch) restores each file with `git checkout --` on the committed tree. a04's mutants for item 1: 1a to 1e (1c puts back a03's silence sentence, 1e a03's re-derivation clause). For item 3: 3a to 3f (3d puts back a03's whole bullet, 3f a03's "without the paste"). The output names the failing test and its FAIL-line count, not the subTest label.

```text
$ uv run --no-project python "$TMPDIR/mutate.py" "$PWD"; git status --short
mutant 1a home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=1) fail_lines=1
mutant 1b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=1) fail_lines=1
mutant 1c home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=2) fail_lines=2
mutant 1d home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=1) fail_lines=1
mutant 1e home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=1) fail_lines=1
mutant 2 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_rule_changes_travel_as_task_amendments -> rc=1 FAILED (failures=1) fail_lines=1
mutant 2b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_rule_changes_travel_as_task_amendments -> rc=1 FAILED (failures=1) fail_lines=1
mutant 3a home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
mutant 3b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
mutant 3c home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
mutant 3d home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=4) fail_lines=4
mutant 3e home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
mutant 3f home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
mutant 4a home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_threat_table_rows_have_a_fixed_unit -> rc=1 FAILED (failures=1) fail_lines=1
mutant 4c home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_threat_table_rows_have_a_fixed_unit -> rc=1 FAILED (failures=1) fail_lines=1
mutant 4b AGENTS.md: test_threat_table_rows_have_a_fixed_unit -> rc=1 FAILED (failures=1) fail_lines=1
mutant 5 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_task_file_review_is_one_round_with_a_fixed_stop_condition -> rc=1 FAILED (failures=2) fail_lines=2
mutant 5b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_task_file_review_is_one_round_with_a_fixed_stop_condition -> rc=1 FAILED (failures=1) fail_lines=1
mutant 6 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_the_gate_reads_the_acceptance_record -> rc=1 FAILED (failures=1) fail_lines=1
mutant 7 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_regime_rule_sections_are_pinned_whole -> rc=1 FAILED (failures=1) fail_lines=1
```

## 7. Fixtures and size

```text
$ git show --stat --format=%h beee078a | tail -n 5
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  4 +-
 tests/fixtures/regime/invariants.md                |  2 +-
 tests/fixtures/regime/orchestrator-step-6.md       |  2 +-
 tests/unit/test_agmsg_orchestration_docs.py        | 57 +++++++++++++---------
 4 files changed, 39 insertions(+), 26 deletions(-)
$ git diff --numstat origin/main...HEAD -- . ":!.orchestration"
1	1	AGENTS.md
6	4	home/dot_agents/skills/agmsg-orchestration/SKILL.md
1	1	tests/fixtures/regime/code-review-orchestration.md
4	2	tests/fixtures/regime/invariants.md
1	0	tests/fixtures/regime/orchestrator-step-6.md
107	1	tests/unit/test_agmsg_orchestration_docs.py
```

## 8. CompactionDB

```text
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] dotfiles-T128-playbook-rules-a04 (plan 010 option D): SKILL Orchestrator Playbook step 6 and the three-repeat bullet state the obligation ..."   # main checkout, permission gate
a3ae0494-87a7-437c-b39a-2a08ecfcd170
```

## 9. Revise round 1, amendment 1 (ACCEPTANCE `status=revise` of 2026-10-13T13:57:09Z on `2276a365`)

The branch fast-forwarded to the remote head `7771082f` and merged `origin/main` (`4e7a9b3a`) in `87bce51e`. The amended sentences are in `e6602ca1`.

```text
$ git show origin/main:.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md | shasum -a 256; shasum -a 256 .orchestration/dotfiles-T128-playbook-rules-a04/task.md
c5dbc2c3d3514707870c2146ac4acfd6e96279d50f0f6bf04bd8921cd242a6fa  -
c5dbc2c3d3514707870c2146ac4acfd6e96279d50f0f6bf04bd8921cd242a6fa  .orchestration/dotfiles-T128-playbook-rules-a04/task.md
$ git log --oneline -4
e6602ca1 docs(agmsg-orchestration): playbook-rules a04 amendment 1 sentences
87bce51e Merge remote-tracking branch 'origin/main' into regime/playbook-rules
4e7a9b3a chore(orchestration): boundary commit 2026-10-13 (12): plan 020/021 (the by-construction order), the three owner tasks, the cost ledger, plans 018 and 019 (#348)
a1d33849 chore(orchestration): boundary commit 2026-10-13 (11): T718 first slice merged (a04 records), a02 dispatched, T703 a04 amendment 1 and its owner task, M-20261012-34/35, C-33/34, plan 017 (#347)
$ uv run --no-project python -I <the check below>   # each quoted sentence of the amended items 1, 4 and 5, as the task file quotes it, is in the SKILL verbatim
item 1: 1161 characters, in the SKILL: True
item 4: 789 characters, in the SKILL: True
item 5: 334 characters, in the SKILL: True
$ uv run --no-project python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v 2>&1 | sed -E 's/ \(tests\.unit\.[a-z_]+\.[A-Za-z]+\.[a-z0-9_]+\)//'   # drops each test's repeated dotted id
test_docs_no_longer_name_codex_review_commit ... ok
test_rule_and_skill_name_worker_seats_not_codex_workers ... ok
test_rule_drops_the_worker_network_escalation ... ok
test_skill_drops_the_pane_status_gate_and_raw_pane_wakes ... ok
test_rule_pointers_name_real_skill_sections ... ok
test_rule_states_the_invariants ... ok
test_word_budgets ... ok
test_audit_command_lives_only_in_the_task_level_audit_bullet ... ok
test_codex_agents_points_at_the_worklog_section ... ok
test_contextdb_cli_is_invoked_with_uv_run ... ok
test_skill_masks_evidence_with_a_runnable_command ... ok
test_claude_worker_merge_denials_and_prefix_limits_are_documented ... ok
test_codex_worker_profile_defaults_to_standard ... ok
test_skill_carries_the_audit_gate_and_bot_wait_mechanics ... ok
test_skill_carries_the_parallel_execution_and_routing_mechanics ... ok
test_skill_carries_the_registration_and_delivery_mechanics ... ok
test_skill_carries_the_session_lessons ... ok
test_a_design_lands_on_main_before_its_task ... ok
test_a_revise_acceptance_names_the_previous_head_and_a_check ... ok
test_a_trust_boundary_task_carries_a_threat_table ... ok
test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first ... ok
test_boundary_merge_sentence_names_the_in_job_decision ... ok
test_closed_selector_existence_is_checked_at_acceptance ... ok
test_code_review_rules_cover_orchestration_records_and_threat_tables ... ok
test_counters_bullet_names_owners_not_sources ... ok
test_counters_run_before_every_acceptance_action ... ok
test_design_review_runs_in_paired_rounds_with_a_cap ... ok
test_dispatches_are_recorded_from_the_bus ... ok
test_open_review_body_findings_have_an_identifier ... ok
test_open_third_round_threads_have_an_integration_outcome ... ok
test_orchestration_records_rule_binds_the_bot_review_only ... ok
test_pattern_rules_pin_their_safeguards ... ok
test_question_pongs_are_in_the_contract ... ok
test_regime_rule_sections_are_pinned_whole ... ok
test_rule_changes_travel_as_task_amendments ... ok
test_shape_is_checked_by_hand_until_the_schema_lands ... ok
test_shape_rules_and_the_decision_sentence_are_pinned ... ok
test_task_file_review_is_one_round_with_a_fixed_stop_condition ... ok
test_the_bot_wait_filters_the_codex_bot ... ok
test_the_ci_watch_is_joined_before_the_result ... ok
test_the_ci_watcher_survives_the_no_checks_race ... ok
test_the_gate_reads_the_acceptance_record ... ok
test_threat_table_rows_have_a_fixed_unit ... ok
test_threat_table_rule_carries_no_grammar ... ok
test_three_repeats_start_with_a_pasted_correction_search ... ok
test_workers_commit_inside_the_sandbox ... ok
test_workers_open_the_pr_as_a_draft ... ok

----------------------------------------------------------------------
Ran 47 tests in 0.009s

OK
$ prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime/*.md; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py
Checking formatting...
All matched files use Prettier code style!
1 file already formatted
$ git diff --stat 87bce51e HEAD -- home tests AGENTS.md   # the fixture changes of this round: invariants.md and orchestrator-step-6.md
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  6 ++--
 tests/fixtures/regime/invariants.md                |  4 +--
 tests/fixtures/regime/orchestrator-step-6.md       |  2 +-
 tests/unit/test_agmsg_orchestration_docs.py        | 38 +++++++++++++++-------
 4 files changed, 32 insertions(+), 18 deletions(-)
$ uv run --no-project python <scratchpad>/mutate-pr328.py   # each amended sentence put back to its previous form, in the SKILL and its fixture
P1 step 6: complete bus read: test_dispatches_are_recorded_from_the_bus -> FAILED (killed) | AssertionError: 'Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read mark
P2 step 6: thirty minutes: test_dispatches_are_recorded_from_the_bus -> FAILED (killed) | AssertionError: "A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minu
P3 row unit: no wildcard rule: test_threat_table_rows_have_a_fixed_unit -> FAILED (killed) | AssertionError: "metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow
P4 invariant check: ids only: test_task_file_review_is_one_round_with_a_fixed_stop_condition -> FAILED (killed) | AssertionError: "one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry, the invariant ids match, 
P5 fixture only (pinning): test_regime_rule_sections_are_pinned_whole -> FAILED (killed) | AssertionError: '6. S[2911 chars] for 20 minutes since its latest bus event for[568 chars]ge).' != '6. S[2911 chars] for 30 minutes since its latest bus event f
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-playbook-rules-a01/autoskill.md
7	0	.orchestration/dotfiles-T128-playbook-rules-a01/learning.md
49	0	.orchestration/dotfiles-T128-playbook-rules-a01/report.md
26	0	.orchestration/dotfiles-T128-playbook-rules-a01/sandbox.md
84	0	.orchestration/dotfiles-T128-playbook-rules-a01/task.md
220	0	.orchestration/dotfiles-T128-playbook-rules-a01/validation.md
3	0	.orchestration/dotfiles-T128-playbook-rules-a02/autoskill.md
7	0	.orchestration/dotfiles-T128-playbook-rules-a02/learning.md
71	0	.orchestration/dotfiles-T128-playbook-rules-a02/report.md
26	0	.orchestration/dotfiles-T128-playbook-rules-a02/sandbox.md
90	0	.orchestration/dotfiles-T128-playbook-rules-a02/task.md
362	0	.orchestration/dotfiles-T128-playbook-rules-a02/validation.md
3	0	.orchestration/dotfiles-T128-playbook-rules-a03/autoskill.md
6	0	.orchestration/dotfiles-T128-playbook-rules-a03/learning.md
53	0	.orchestration/dotfiles-T128-playbook-rules-a03/report.md
21	0	.orchestration/dotfiles-T128-playbook-rules-a03/sandbox.md
92	0	.orchestration/dotfiles-T128-playbook-rules-a03/task.md
183	0	.orchestration/dotfiles-T128-playbook-rules-a03/validation.md
3	0	.orchestration/dotfiles-T128-playbook-rules-a04/autoskill.md
6	0	.orchestration/dotfiles-T128-playbook-rules-a04/learning.md
55	0	.orchestration/dotfiles-T128-playbook-rules-a04/report.md
21	0	.orchestration/dotfiles-T128-playbook-rules-a04/sandbox.md
94	0	.orchestration/dotfiles-T128-playbook-rules-a04/task.md
183	0	.orchestration/dotfiles-T128-playbook-rules-a04/validation.md
1	1	AGENTS.md
6	4	home/dot_agents/skills/agmsg-orchestration/SKILL.md
1	1	tests/fixtures/regime/code-review-orchestration.md
4	2	tests/fixtures/regime/invariants.md
1	0	tests/fixtures/regime/orchestrator-step-6.md
121	1	tests/unit/test_agmsg_orchestration_docs.py
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^\.orchestration\// {f++} $3 !~ /^\.orchestration\// && $3 !~ /^tests\// {o+=$1} $3 ~ /^tests\// {t+=$1} END {print "files outside .orchestration/:", f, "added outside tests/:", o, "added under tests/:", t}'
files outside .orchestration/: 6 added outside tests/: 7 added under tests/: 127
```
