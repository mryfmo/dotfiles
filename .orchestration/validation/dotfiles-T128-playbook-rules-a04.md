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

## 9. CI and the Bot on `2276a365`

```text
$ scratchpad/ci-watch.sh
ci-watch exit status: 0
GitGuardian Security Checks	completed	success
private-bootstrap (macos-14, client)	completed	success
private-bootstrap (ubuntu-24.04, client)	completed	success
private-bootstrap (ubuntu-24.04, server)	completed	success
public-bootstrap (macos-14, client)	completed	success
public-bootstrap (ubuntu-24.04, client)	completed	success
public-bootstrap (ubuntu-24.04, server)	completed	success
test (macos-14, client)	completed	success
test (ubuntu-24.04, client)	completed	success
test (ubuntu-24.04, server)	completed	success
test (ubuntu-26.04, client)	completed	success
validate	completed	success
$ scratchpad/bot-wait.sh   # from the push, 15:49:28Z
https://github.com/mryfmo/dotfiles/pull/328#issuecomment-6127877830
posted @codex review at 2026-10-12T15:59:59Z
elapsed=845s reviews:
5493270947	2276a365cba9f104cadd7cd82f3fb0bfec7dac21	2026-10-12T16:03:26Z
top-level comments:
4250028600	2276a365cba9f104cadd7cd82f3fb0bfec7dac21	home/dot_agents/skills/agmsg-orchestration/SKILL.md

[exited with code 0]
$ git grep -n 'candidate class=' origin/main -- scripts/regime-counters.sh tests/ | cut -c1-170   # thread 4250028600
origin/main:scripts/regime-counters.sh:147:      | group_by(.)[] | select(length >= 3) | "S1: candidate class=\(.[0]) count=\(length) source=\($s)" else empty end),
origin/main:tests/unit/test_regime_counters.py:451:            ["S1: candidate class=reject skipped contract count=3 source=fixture"],
```
