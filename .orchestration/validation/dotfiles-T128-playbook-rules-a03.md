# Validation: dotfiles-T128-playbook-rules-a03

Seat `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `regime/playbook-rules`, PR #328, continued from a02's head `c4e0bb72`. `origin/main` is `e0e2fe62`; the branch's merge-base is still `683384ea`. Every block is verbatim command output; `mise WARN` sandbox cache lines are filtered out, and `grep` is `/usr/bin/grep` wherever a result depends on it.

## 1. Task copies

```text
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-playbook-rules-a03.md .orchestration/dotfiles-T128-playbook-rules-a03/task.md
ee6385184e3db246df45970bf71862525d5fd990aa41f92b2b9d03654d45adb2  <main checkout>/.orchestration/tasks/dotfiles-T128-playbook-rules-a03.md
ee6385184e3db246df45970bf71862525d5fd990aa41f92b2b9d03654d45adb2  .orchestration/dotfiles-T128-playbook-rules-a03/task.md
$ cmp <main checkout>/.orchestration/tasks/dotfiles-T128-playbook-rules-a03.md .orchestration/dotfiles-T128-playbook-rules-a03/task.md && echo identical
identical
$ git diff --quiet 1083a8c1 HEAD -- .orchestration/dotfiles-T128-playbook-rules-a01/task.md && echo "a01 copy unchanged since 1083a8c1"; git diff --quiet 4486dbdd HEAD -- .orchestration/dotfiles-T128-playbook-rules-a02/task.md && echo "a02 copy unchanged since 4486dbdd"
a01 copy unchanged since 1083a8c1
a02 copy unchanged since 4486dbdd
$ shasum -a 256 .orchestration/dotfiles-T128-playbook-rules-a02/task.md; /usr/bin/grep -n -o -E "(7929fe7a|07b78f64)[0-9a-f]*" <main checkout>/.orchestration/acceptance/dotfiles-T128-playbook-rules-a02.md
07b78f643bc5a488614bca59d195d45da93defb7d7c0acf5fc8a4820e00f4f33  .orchestration/dotfiles-T128-playbook-rules-a02/task.md
3:7929fe7a210a268703f93836ff3dfb55937c9477f6fa58a3f1983995ade671ff
24:07b78f64
25:07b78f64
```

## 2. Premises of the landing conditions

```text
$ git diff --stat 683384ea origin/main -- home/ AGENTS.md tests/ scripts/ Makefile | tail -1; echo "(empty: main moved only under .orchestration)"
(empty: main moved only under .orchestration)
$ git grep -c ACCEPTANCE_EVIDENCE origin/main -- scripts/ Makefile | wc -l   # the gate does not read it on main
       0
$ git ls-tree -r --name-only origin/main | /usr/bin/grep -ci task-consistency   # no checker on main
0
$ git ls-remote https://github.com/mryfmo/dotfiles 'refs/heads/regime/gate-evidence*'   # the task the gate sentence names is in flight
d5d6c9b1b22c32e483f76ed2d313571a487aa16a	refs/heads/regime/gate-evidence
```

## 3. Every quoted sentence of the task is in the prose verbatim

```text
$ uv run --no-project python "$TMPDIR/verbatim.py" "$PWD" .orchestration/dotfiles-T128-playbook-rules-a03/task.md
item 1 quote 1: present (ok) 580 chars
item 2 quote 1: present (ok) 33 chars
item 2 quote 2: present (ok) 240 chars
item 3 quote 1: present (ok) 1014 chars
item 4 quote 1: present (ok) 544 chars
item 4 quote 2: present (ok) 40 chars
item 4 quote 3: present (ok) 173 chars
item 5 quote 1: absent (ok) 73 chars
item 5 quote 2: present (ok) 184 chars
$ /usr/bin/grep -c "ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main" home/dot_agents/skills/agmsg-orchestration/SKILL.md   # item 6: the command token only
1
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
Ran 47 tests in 0.010s

OK
```

## 5. The module that pins the gate command, and format

```text
$ uv run --no-project python -m unittest tests/unit/test_pr_feedback.py 2>&1 | tail -n 3
Ran 16 tests in 0.019s

OK
$ ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py
1 file already formatted
```

## 6. Each sentence fails its test when removed or put back to its previous form

`mutate.py` (session scratch) restores each file with `git checkout --` on the committed tree. a03's mutants: 2 drops the new parenthesis and 2b puts back a02's; 3c drops the not-applicable sentence and 3e puts back a02's gate sentence; 4a drops the new C4 clause and 4c puts back a02's. The output names the failing test and its FAIL-line count, not the subTest label.

```text
$ uv run --no-project python "$TMPDIR/mutate.py" "$PWD"; git status --short
mutant 1a home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=1) fail_lines=1
mutant 1b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=1) fail_lines=1
mutant 1c home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=2) fail_lines=2
mutant 2 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_rule_changes_travel_as_task_amendments -> rc=1 FAILED (failures=1) fail_lines=1
mutant 2b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_rule_changes_travel_as_task_amendments -> rc=1 FAILED (failures=1) fail_lines=1
mutant 3a home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=2) fail_lines=2
mutant 3d home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=2) fail_lines=2
mutant 3b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
mutant 3c home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
mutant 3e home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=3) fail_lines=3
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
$ git show --stat --format=%h f40e530a | tail -n 4
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  6 +++---
 tests/fixtures/regime/invariants.md                |  6 +++---
 tests/unit/test_agmsg_orchestration_docs.py        | 25 ++++++++++++++++------
 3 files changed, 24 insertions(+), 13 deletions(-)
$ git diff --numstat origin/main...HEAD -- . ":!.orchestration"
1	1	AGENTS.md
6	4	home/dot_agents/skills/agmsg-orchestration/SKILL.md
1	1	tests/fixtures/regime/code-review-orchestration.md
4	2	tests/fixtures/regime/invariants.md
1	0	tests/fixtures/regime/orchestrator-step-6.md
94	1	tests/unit/test_agmsg_orchestration_docs.py
$ git diff -U0 origin/main...HEAD -- home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep "^@@" | cut -c1-30
@@ -69 +69 @@ Use this skill f
@@ -71 +71 @@ Use this skill f
@@ -72,0 +73,2 @@ Use this ski
@@ -162 +164 @@ AGMSG-PONG v1 
@@ -170 +172 @@ AGMSG-PONG v1 
```

## 8. CompactionDB

```text
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] dotfiles-T128-playbook-rules-a03 (plan 009 option A): a SKILL rule that cites a mechanism not yet on main names its landing condition ..."   # main checkout, permission gate
651f5fce-7002-4db5-9d48-b9af40a34601
```

## 9. Commits since a02's head

```text
$ git log --oneline c4e0bb72..HEAD
f40e530a docs(regime): name the landing condition of the checker and gate the rules cite
196d73ca chore(orchestration): record the dotfiles-T128-playbook-rules-a03 task
```

## 10. CI and the Bot on `fe34f7db`

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
$ scratchpad/bot-wait.sh   # from the push, 14:40:23Z
elapsed=350s reviews:
5492353166	fe34f7db0311fd5503104abe1a4b8ddec509c547	2026-10-12T14:45:52Z
top-level comments:
4249303398	fe34f7db0311fd5503104abe1a4b8ddec509c547	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4249303413	fe34f7db0311fd5503104abe1a4b8ddec509c547	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4249303426	fe34f7db0311fd5503104abe1a4b8ddec509c547	home/dot_agents/skills/agmsg-orchestration/SKILL.md
4249303433	fe34f7db0311fd5503104abe1a4b8ddec509c547	home/dot_agents/skills/agmsg-orchestration/SKILL.md

[exited with code 0]
$ /usr/bin/grep -n -E 'LIMIT=' ~/.agents/skills/agmsg/scripts/history.sh   # thread 4249303413
9:LIMIT="${3:-20}"
14:case "$LIMIT" in ''|*[!0-9]*) LIMIT=20 ;; esac
$ git show origin/main:scripts/regime-counters.sh | sed -n '146,147p' | cut -c1-150   # thread 4249303433: the S1 class is the first three words of a title, lowercased, unfiltered
        | gsub("!\\[[^\\]]*\\]\\([^)]*\\)|</?sub>|\\*\\*"; "") | ascii_downcase | [splits("\\s+") | select(. != "")][0:3] | join(" ") | select(. != ""
      | group_by(.)[] | select(length >= 3) | "S1: candidate class=\(.[0]) count=\(length) source=\($s)" else empty end),
$ git show origin/main:.orchestration/learning/corrections/C-2.md | sed -n '13p'   # thread 4249303398
status: "landed for fixtures and the bullet; pending for C4 and T703 (dotfiles-T128-playbook-rules-a02 carries the AGENTS.md sentence)"
```
