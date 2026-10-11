# Validation: dotfiles-T128-process-rules-a05

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `docs/regime-pattern` (PR #318). This branch copy covers `dfdee38b`; the main-checkout copy adds the final head (design INV-8).

## 1. Task file

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-process-rules-a05.md .orchestration/dotfiles-T128-process-rules-a05/task.md | cut -c1-64
de2897dacd0a3f47588cc7d44a8e79fd2436732d81e48977009975d989ee3237
de2897dacd0a3f47588cc7d44a8e79fd2436732d81e48977009975d989ee3237
```

## 2. Checks at `dfdee38b` (task validation: prettier on the two prose files, the docs test -v)

```
$ git log --oneline -3; git show --stat --format= dfdee38b; prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -1; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py
dfdee38b docs(regime): the counters bullet states its obligations by reference
5f2a331d chore(orchestration): task file for dotfiles-T128-process-rules-a05
7800ef92 chore(orchestration): evidence for dotfiles-T128-process-rules-a04 Amendment 1
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  2 +-
 tests/unit/test_agmsg_orchestration_docs.py        | 33 +++++++++-------------
 2 files changed, 15 insertions(+), 20 deletions(-)
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
test_counters_bullet_names_owners_not_sources ... ok
test_counters_run_before_every_acceptance_action ... ok
test_design_review_runs_in_paired_rounds_with_a_cap ... ok
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
Ran 40 tests in 0.008s
OK
$ for p in "limit 1000" "review bodies" "by hand" "grouped by \`commit_id\`" "decided from that output" "until it is on \`main\`" "gh api --paginate"; do printf "%-28s " "$p"; grep -c -- "$p" tests/unit/test_agmsg_orchestration_docs.py; done   # old-bullet literals left in the module
limit 1000                   0
review bodies                1
by hand                      2
grouped by `commit_id`       0
decided from that output     0
until it is on `main`        1
gh api --paginate            1
```

The remaining matches are the new test's own forbidden-phrase list and the threat-table bullet's pre-V1 sentence ("…checks the three shape rules by hand."), which the task keeps.

## 3. Removal proofs (`scratchpad/mutate_a05.py` at `dfdee38b`: the counters bullet edited as a plain string in a `git archive HEAD` copy, the old bullet taken from `7800ef92`; then the decision-sentence pin)

```
== broken rule: unknown-sentence-token-removed -> test_counters_bullet_names_owners_not_sources
   failing subtests: 1 (token)
   FAILED (failures=1)
== broken rule: class-table-token-removed -> test_counters_bullet_names_owners_not_sources
   failing subtests: 1 (token)
   FAILED (failures=1)
== broken rule: forbidden-phrase-pasted: review bodies -> test_counters_bullet_names_owners_not_sources
   failing subtests: 1 (phrase)
   FAILED (failures=1)
== broken rule: forbidden-phrase-pasted: by hand -> test_counters_bullet_names_owners_not_sources
   failing subtests: 1 (phrase)
   FAILED (failures=1)
== broken rule: forbidden-phrase-pasted: gh api --paginate -> test_counters_bullet_names_owners_not_sources
   failing subtests: 1 (phrase)
   FAILED (failures=1)
== broken rule: forbidden-phrase-pasted: until it is on `main` -> test_counters_bullet_names_owners_not_sources
   failing subtests: 1 (phrase)
   FAILED (failures=1)
== broken rule: old-bullet-pasted-back (from 7800ef92) -> test_counters_bullet_names_owners_not_sources
   failing subtests: 6 (phrase, token)
   FAILED (failures=6)
== restored: OK
== broken rule: decision-sentence-pin-removed -> test_shape_rules_and_the_decision_sentence_are_pinned
FAIL: test_shape_rules_and_the_decision_sentence_are_pinned (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_rules_and_the_decision_sentence_are_pinned) (<redacted:secret-pattern>s counts")
AssertionError: "S2 is decided from INV-6's counts" not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never trea
FAILED (failures=1)
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

## 5. CompactionDB (main checkout, outside the sandbox through the permission gate, in the same call as the gh premise)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-process-rules-a05 item 9 …'
546ec858-f8ac-4761-9189-3d288ba7c4e5
```
