# Validation: dotfiles-T128-process-rules-a04

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `docs/regime-pattern` (PR #318). This branch copy covers `28d728c5`; the main-checkout copy adds the final head (design INV-8).

## 1. Task file

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-process-rules-a04.md .orchestration/dotfiles-T128-process-rules-a04/task.md | cut -c1-64
842deee29dab4594ba077b56fc5d7769936617fcaa50fb2b4ebc947361626950
842deee29dab4594ba077b56fc5d7769936617fcaa50fb2b4ebc947361626950
```

## 2. Checks at `28d728c5` (task validation: prettier on the two prose files, the docs test -v)

```
$ git log --oneline -3; prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -1; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py
28d728c5 docs(regime): freeze the design at the last accepted hash; a design lands on main before its task
379fa107 chore(orchestration): task file for dotfiles-T128-process-rules-a04
781e6ef8 chore(orchestration): evidence for the a03 revise's Bot fix round 1
All matched files use Prettier code style!
1 file already formatted
All checks passed!
$ UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs -v 2>&1 | grep -E "AgmsgRegimePatternTest|^Ran|^OK|^FAILED" | sed -E "s/ \(tests[^)]*\)//"
test_a_design_lands_on_main_before_its_task ... ok
test_a_revise_acceptance_names_the_previous_head_and_a_check ... ok
test_a_trust_boundary_task_carries_a_threat_table ... ok
test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first ... ok
test_boundary_merge_sentence_names_the_in_job_decision ... ok
test_closed_selector_existence_is_checked_at_acceptance ... ok
test_code_review_rules_cover_orchestration_records_and_threat_tables ... ok
test_counters_add_review_body_findings ... ok
test_counters_run_before_every_acceptance_action ... ok
test_design_review_runs_in_paired_rounds_with_a_cap ... ok
test_manual_counts_read_the_whole_history ... ok
test_open_review_body_findings_have_an_identifier ... ok
test_open_third_round_threads_have_an_integration_outcome ... ok
test_orchestration_records_rule_binds_the_bot_review_only ... ok
test_pattern_rules_pin_their_safeguards ... ok
test_shape_is_checked_by_hand_until_the_schema_lands ... ok
test_shape_rules_and_the_decision_sentence_are_pinned ... ok
test_task_file_review_is_one_round_with_a_fixed_stop_condition ... ok
test_the_bot_wait_filters_the_codex_bot ... ok
test_the_ci_watch_is_joined_before_the_result ... ok
test_the_ci_watcher_survives_the_no_checks_race ... ok
test_threat_table_rule_carries_no_grammar ... ok
test_workers_commit_inside_the_sandbox ... ok
test_workers_open_the_pr_as_a_draft ... ok
Ran 41 tests in 0.008s
OK
```

## 3. Removal proofs (`scratchpad/mutate-a04.sh` at `28d728c5`: the task's new and old sentences taken from the task file, each new token removed or each old sentence pasted back in a `git archive HEAD` copy; output cut to three lines of at most 400 characters per rule)

```
== removed rule: item6-old-sentence-pasted-back (SKILL, diff lines: 2) -> test_design_review_runs_in_paired_rounds_with_a_cap
FAIL: test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) (<redacted:secret-pattern>)
AssertionError: 'frozen at the hash the pair last accepted' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; never del
FAIL: test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) (<redacted:secret-pattern>)
== removed rule: item6-hashed-key-is-a-new-pair (SKILL, diff lines: 2) -> test_design_review_runs_in_paired_rounds_with_a_cap
FAIL: test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) (<redacted:secret-pattern>)
AssertionError: 'any later change to a hashed key is a new pair (INV-7)' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-si
FAILED (failures=1)
== removed rule: item7-old-sentence-pasted-back (SKILL, diff lines: 2) -> test_a_design_lands_on_main_before_its_task
FAIL: test_a_design_lands_on_main_before_its_task (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_design_lands_on_main_before_its_task) (<redacted:secret-pattern>)
AssertionError: 'before its implementing TASK is dispatched (INV-2)' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; 
FAIL: test_a_design_lands_on_main_before_its_task (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_design_lands_on_main_before_its_task)
== removed rule: item7-design-lands-before-dispatch (SKILL, diff lines: 2) -> test_a_design_lands_on_main_before_its_task
FAIL: test_a_design_lands_on_main_before_its_task (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_design_lands_on_main_before_its_task) (<redacted:secret-pattern>)
AssertionError: 'before its implementing TASK is dispatched (INV-2)' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; 
FAILED (failures=1)
== removed rule: item7-safeguard-clause (SKILL, diff lines: 2) -> test_pattern_rules_pin_their_safeguards
FAIL: test_pattern_rules_pin_their_safeguards (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_pattern_rules_pin_their_safeguards) (<redacted:secret-pattern>)
AssertionError: 'any merged boundary that carries the design meets that precondition' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work remain or
FAILED (failures=1)
== restored: OK
```

## 4. Premises, re-run (the gh one outside the sandbox)

```
$ gh api --paginate repos/mryfmo/dotfiles/pulls/318/comments --jq '.[]|select(.in_reply_to_id==null and (.original_commit_id[0:8]|IN("9a46c3c4","ac3794f9","6635030f")) and (.body|test("P0 Badge|P1 Badge|P2 Badge")))|[.id,.original_commit_id[0:8]]|@tsv'
4240290382	9a46c3c4
4240290387	9a46c3c4
4240290391	9a46c3c4
4240321113	ac3794f9
4240334094	6635030f
4240334098	6635030f
$ ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conformance --limit 1000 | grep 'AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a01' | cut -c1-140
  ○ [2026-10-11T05:10:11Z] claude-review-dot-a001 → claude-deep-dot: AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a01 status
$ sha256sum .orchestration/validation/dotfiles-T128-process-rules-redesign-a01.md   # in the main checkout
b95b4eacb3b7ef3f8cc8f0da438062e4a794a1e96139268b9cecc6b4df0b40e4  .orchestration/validation/dotfiles-T128-process-rules-redesign-a01.md
```

All three equal the task's recorded output.

## 5. CompactionDB (main checkout, outside the sandbox through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-process-rules-a04 …'
172a34d7-e9a7-4556-9874-cf55f2c7314d
```

## 7. Amendment 1: item 8 at `2a3f52e9` (thread 4243537278; §6 is the main-checkout copy's final head of the first RESULT)

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-process-rules-a04.md .orchestration/dotfiles-T128-process-rules-a04/task.md | cut -c1-64
6ef9ae9572ecd90876ed7b706c4d2d739b082d39adec4b531ccef0789e410fa6
6ef9ae9572ecd90876ed7b706c4d2d739b082d39adec4b531ccef0789e410fa6
$ git log --oneline -2; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py; prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -1
2a3f52e9 docs(regime): review-body findings feed S1 and the fix-round cap, never INV-6's head count
16c2e3d4 chore(orchestration): task file for dotfiles-T128-process-rules-a04, Amendment 1
Ran 41 tests in 0.011s

OK
1 file already formatted
All checks passed!
All matched files use Prettier code style!
```

Removal proofs (`scratchpad/mutate_a04_am1.py`: the task's old and new sentences taken from the task file, replaced as plain strings in a `git archive HEAD` copy):

```
== removed rule: item8-new-sentence-removed (SKILL) -> test_counters_add_review_body_findings
FAIL: test_counters_add_review_body_findings (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_add_review_body_findings)
AssertionError: "The script reads inline review comments only, and that is INV-6's whole head count (`original_commit_id` on `review_comment` items); the orchestrator also lists the P0/P1-badged Bot review bodies of `…/pulls/<n>/reviews`, grouped by `commit_id`, by hand and pastes that command and its output beside the script's, for S1's finding classes and the worker's fix-round cap only, never a
FAILED (failures=1)
== removed rule: item8-old-sentence-pasted-back (SKILL) -> test_counters_add_review_body_findings
FAIL: test_counters_add_review_body_findings (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_add_review_body_findings)
AssertionError: "The script reads inline review comments only, and that is INV-6's whole head count (`original_commit_id` on `review_comment` items); the orchestrator also lists the P0/P1-badged Bot review bodies of `…/pulls/<n>/reviews`, grouped by `commit_id`, by hand and pastes that command and its output beside the script's, for S1's finding classes and the worker's fix-round cap only, never a
FAILED (failures=1)
== removed rule: item8-old-inv6-clause-pasted-back (SKILL) -> test_counters_add_review_body_findings
FAIL: test_counters_add_review_body_findings (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_add_review_body_findings)
AssertionError: 'which INV-6 and S1 count' unexpectedly found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; never delegate th
FAILED (failures=1)
== restored: OK
```

CompactionDB (main checkout, outside the sandbox through the permission gate):

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-process-rules-a04 Amendment 1 item 8 …'
f38272e9-e7e8-480f-bdca-f9a6c6dc5205
```
