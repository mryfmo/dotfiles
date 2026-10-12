# Validation: dotfiles-T128-playbook-rules-a02

Seat `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `regime/playbook-rules`, PR #328, continued from head `9b2c02a1` (a01). `origin/main` is `4cf1d4e2` (boundary PR #330, which lands the `classes:` fields); the branch's merge-base is still `683384ea`. Every block is verbatim command output; `mise WARN` cache-write lines from the sandbox are filtered out, and `grep` is `/usr/bin/grep` wherever a result depends on it, because this seat's shell wraps `grep` in ugrep.

## 1. Task copies

```text
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-playbook-rules-a02.md .orchestration/dotfiles-T128-playbook-rules-a02/task.md .orchestration/dotfiles-T128-playbook-rules-a01/task.md
7929fe7a210a268703f93836ff3dfb55937c9477f6fa58a3f1983995ade671ff  <main checkout>/.orchestration/tasks/dotfiles-T128-playbook-rules-a02.md
7929fe7a210a268703f93836ff3dfb55937c9477f6fa58a3f1983995ade671ff  .orchestration/dotfiles-T128-playbook-rules-a02/task.md
b035ebd79add64b0cd9977e154b30746757d64782e65089541a79627b1020c0d  .orchestration/dotfiles-T128-playbook-rules-a01/task.md
$ cmp <main checkout>/.orchestration/tasks/dotfiles-T128-playbook-rules-a02.md .orchestration/dotfiles-T128-playbook-rules-a02/task.md && echo identical
identical
$ git diff --quiet 1083a8c1 HEAD -- .orchestration/dotfiles-T128-playbook-rules-a01/task.md && echo "a01 copy unchanged since 1083a8c1"
a01 copy unchanged since 1083a8c1
```

## 2. Premises (on `origin/main` `4cf1d4e2`)

```text
$ git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -n -E '^- A task-file review is one round|^- A task that touches a trust boundary|^- Before every acceptance action|^6\. Send `AGMSG-TASK v1`' | cut -c1-90
69:- A task-file review is one round with a fixed stop condition: no contradiction with th
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides
72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts
162:6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. 
$ git show origin/main:AGENTS.md | /usr/bin/grep -n 'Judge from the diff' | cut -c1-60
78:- Judge from the diff, whatever the task's metadata says,
$ git show origin/main:tests/unit/test_agmsg_orchestration_docs.py | sed -n '240,252p' | /usr/bin/grep -n -E 'PINNED_SECTIONS|fixtures/regime|declare the change'
2:        for name, path, outer, (start, end) in self.PINNED_SECTIONS:
7:                fixture = ROOT / "tests/fixtures/regime" / f"{name}.md"
11:                    f"regime rule section {name} changed: declare the change by updating "
12:                    f"tests/fixtures/regime/{name}.md in the same commit and listing it in the RESULT",
$ git diff --stat 683384ea origin/main -- home/ AGENTS.md tests/ | tail -1; echo "(empty: main moved only under .orchestration)"
(empty: main moved only under .orchestration)
```

## 3. Every quoted sentence of the task is in the prose verbatim

`verbatim.py` (session scratch) takes each double-quoted span of items 1 to 6 and looks for it in SKILL.md plus AGENTS.md; item 5's first span is the clause it replaces, so it must be absent.

```text
$ uv run --no-project python "$TMPDIR/verbatim.py" "$PWD" .orchestration/dotfiles-T128-playbook-rules-a02/task.md
item 1 quote 1: present (ok) 447 chars
item 2 quote 1: present (ok) 33 chars
item 2 quote 2: present (ok) 185 chars
item 3 quote 1: present (ok) 960 chars
item 4 quote 1: present (ok) 468 chars
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
Ran 47 tests in 0.011s

OK
```

## 5. The module that pins the gate command (outside allowed_files, unchanged)

```text
$ uv run --no-project python -m unittest tests/unit/test_pr_feedback.py -v 2>&1 | grep -E "PrIntegrationRuleParity|^Ran|^OK|FAIL"
test_gate_command_appears_once_in_skill_step_10 ... ok
test_rule_mirrors_and_skills_carry_the_same_requirements ... ok
test_rule_symlink_points_at_the_rule ... ok
Ran 16 tests in 0.018s
OK
$ /usr/bin/grep -c "BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review" home/dot_agents/skills/agmsg-orchestration/SKILL.md
1
```

## 6. Format

```text
$ ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py
1 file already formatted
```

## 7. Each new sentence fails its test when removed

`mutate.py` (session scratch) rewrites one span per mutant, runs the named test, and restores the file with `git checkout --` on the committed tree. 3a puts back a01 amendment 1's `grep -l` on a directory; 3d puts back a01's corrections grep; 5 puts back the `-contract-a01` clause and 5b a01's unqualified clause; 7 changes one word of step 6 against the `orchestrator-step-6` fixture. A count of 2 means a token test and a stale-phrase test both fired. The output names the failing test and its FAIL-line count, not the subTest label, which the repository masker reads as a secret.

```text
$ uv run --no-project python "$TMPDIR/mutate.py" "$PWD"; git status --short
mutant 1a home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=1) fail_lines=1
mutant 1b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_dispatches_are_recorded_from_the_bus -> rc=1 FAILED (failures=1) fail_lines=1
mutant 2 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_rule_changes_travel_as_task_amendments -> rc=1 FAILED (failures=1) fail_lines=1
mutant 3a home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=2) fail_lines=2
mutant 3d home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=2) fail_lines=2
mutant 3b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
mutant 3c home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_three_repeats_start_with_a_pasted_correction_search -> rc=1 FAILED (failures=1) fail_lines=1
mutant 4a home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_threat_table_rows_have_a_fixed_unit -> rc=1 FAILED (failures=1) fail_lines=1
mutant 4b AGENTS.md: test_threat_table_rows_have_a_fixed_unit -> rc=1 FAILED (failures=1) fail_lines=1
mutant 5 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_task_file_review_is_one_round_with_a_fixed_stop_condition -> rc=1 FAILED (failures=2) fail_lines=2
mutant 5b home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_task_file_review_is_one_round_with_a_fixed_stop_condition -> rc=1 FAILED (failures=1) fail_lines=1
mutant 6 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_the_gate_reads_the_acceptance_record -> rc=1 FAILED (failures=1) fail_lines=1
mutant 7 home/dot_agents/skills/agmsg-orchestration/SKILL.md: test_regime_rule_sections_are_pinned_whole -> rc=1 FAILED (failures=1) fail_lines=1
?? .orchestration/dotfiles-T128-playbook-rules-a02/validation.md
```

## 8. Item 3's search, run from `main`

On an export of `origin/main` `4cf1d4e2`'s `.orchestration/learning` (`git archive origin/main .orchestration/learning | tar -x`), with the two classes Bot thread 4247933574 named:

```text
$ /usr/bin/grep -rl 'classes:.*bookkeeping' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-4.md
rc=0
$ /usr/bin/grep -rl 'classes:.*sources' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-2.md
.orchestration/learning/mistakes/M-20261012-1.md
rc=0
$ /usr/bin/grep -l 'classes:.*bookkeeping' .orchestration/learning/mistakes/   # a01 amendment 1's form
grep: .orchestration/learning/mistakes/: Is a directory
rc=2
$ /usr/bin/grep -n -E '^classes|^corrections' .orchestration/learning/mistakes/M-20261012-4.md
4:classes: [bookkeeping]
8:corrections: [C-3, C-6]
$ /usr/bin/grep -n -A1 'id: M-20261012-4' .orchestration/learning/index.yaml
14:  - id: M-20261012-4
15-    corrections: [C-3, C-6]
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search bookkeeping   # main checkout, permission gate (a01 round)
No matches.
```

## 9. The a01 Bot round on `9b2c02a1` (review 5490674624)

```text
$ /usr/bin/grep -n 'control: orchestrator effect' .orchestration/dotfiles-T128-playbook-rules-a02/task.md   # thread 4247933544: one row each
42:  - control: orchestrator effect merge
44:  - control: orchestrator effect update-branch
46:  - control: orchestrator effect forced worker removal
$ /usr/bin/grep -c 'playbook-rules' .orchestration/tasks/dotfiles-T128-regime-v3-a01.md; /usr/bin/grep -c '^invariants:' .orchestration/dotfiles-T128-playbook-rules-a02/task.md   # thread 4247933561: not listed, no invariants key
0
0
```

## 10. Size (INV-2 caps)

```text
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-playbook-rules-a01/autoskill.md
7	0	.orchestration/dotfiles-T128-playbook-rules-a01/learning.md
49	0	.orchestration/dotfiles-T128-playbook-rules-a01/report.md
26	0	.orchestration/dotfiles-T128-playbook-rules-a01/sandbox.md
84	0	.orchestration/dotfiles-T128-playbook-rules-a01/task.md
220	0	.orchestration/dotfiles-T128-playbook-rules-a01/validation.md
90	0	.orchestration/dotfiles-T128-playbook-rules-a02/task.md
1	1	AGENTS.md
6	4	home/dot_agents/skills/agmsg-orchestration/SKILL.md
1	1	tests/fixtures/regime/code-review-orchestration.md
4	2	tests/fixtures/regime/invariants.md
1	0	tests/fixtures/regime/orchestrator-step-6.md
80	1	tests/unit/test_agmsg_orchestration_docs.py
```

## 11. Nothing else changes (item 8)

```text
$ git diff -U0 origin/main...HEAD -- home/dot_agents/skills/agmsg-orchestration/SKILL.md | grep "^@@" | cut -c1-40
@@ -69 +69 @@ Use this skill for structu
@@ -71 +71 @@ Use this skill for structu
@@ -72,0 +73,2 @@ Use this skill for str
@@ -162 +164 @@ AGMSG-PONG v1 task_id=<i
@@ -170 +172 @@ AGMSG-PONG v1 task_id=<i
$ for n in 69 71 73 74 164 172; do printf "%s " $n; awk -v n=$n 'NR<=n && /^## /{h=$0} NR==n{print h; exit}' home/dot_agents/skills/agmsg-orchestration/SKILL.md; done
69 ## Review and integration invariants
71 ## Review and integration invariants
73 ## Review and integration invariants
74 ## Review and integration invariants
164 ## Orchestrator Playbook
172 ## Orchestrator Playbook
$ git diff --stat origin/main...HEAD -- tests/fixtures/regime/worker-step-15.md tests/fixtures/regime/message-contract.md tests/fixtures/regime/orchestrator-step-7.md | tail -1; echo "(empty: unchanged)"
(empty: unchanged)
$ sed -n 72p home/dot_agents/skills/agmsg-orchestration/SKILL.md | shasum -a 256; git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | sed -n 72p | shasum -a 256
dee39b7af7713062e6fec3f5c8f8a6df5556d3679fd87c3cb4951de2c5d562d6  -
dee39b7af7713062e6fec3f5c8f8a6df5556d3679fd87c3cb4951de2c5d562d6  -
```

## 12. CompactionDB

```text
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] dotfiles-T128-playbook-rules-a02 (plan 007 T703, INV-6 reset of a01): the SKILL three-repeat search greps the mistake records classes field with grep -rl ..."   # main checkout, permission gate
8bbacd66-762a-4abb-9ae7-7944c4aceb2c
$ (a01) ... memory add ... "[memory:decision] dotfiles-T128-playbook-rules-a01 (plan 007 T703): SKILL Orchestrator Playbook step 10.4 places ACCEPTANCE_EVIDENCE ..."
e187a179-a202-4697-b671-71df72581733
```

## 13. Commits

```text
$ git log --oneline origin/main..HEAD
8b1dbefc docs(regime): key the three-repeat search on the mistake records, qualify the invariant check
95ba4e4c chore(orchestration): record the dotfiles-T128-playbook-rules-a02 task
9b2c02a1 chore(orchestration): dotfiles-T128-playbook-rules-a01 evidence
0158b866 docs(regime): record dispatches from the bus, send rule changes as amendments, fix the threat-row unit
1083a8c1 chore(orchestration): record the dotfiles-T128-playbook-rules-a01 task
```
