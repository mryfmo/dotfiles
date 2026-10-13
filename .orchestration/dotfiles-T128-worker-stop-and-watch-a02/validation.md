# Validation: dotfiles-T128-worker-stop-and-watch-a02

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `docs/worker-stop-and-watch` (PR #323). This branch copy covers the a02 commit; the main-checkout copy adds the final head (design INV-8).

## 1. Task file

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-worker-stop-and-watch-a02.md .orchestration/dotfiles-T128-worker-stop-and-watch-a02/task.md | cut -c1-64
af519f0f6b250de6a91fceee8bc480721a8316c01be47b904d577bf0042baa8e
af519f0f6b250de6a91fceee8bc480721a8316c01be47b904d577bf0042baa8e
```

## 2. Checks (the three text changes, the three fixtures, the tokens)

```
$ git diff --stat HEAD -- home tests; prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime/*.md 2>&1 | tail -1; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py
 home/dot_agents/skills/agmsg-orchestration/SKILL.md |  8 +++++---
 tests/fixtures/regime/message-contract.md           |  4 +++-
 tests/fixtures/regime/orchestrator-step-7.md        |  2 +-
 tests/fixtures/regime/worker-step-15.md             |  2 +-
 tests/unit/test_agmsg_orchestration_docs.py         | 15 ++++++++++++---
 5 files changed, 22 insertions(+), 9 deletions(-)
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
test_question_pongs_are_in_the_contract ... ok
test_regime_rule_sections_are_pinned_whole ... ok
test_result_head_is_in_the_contract ... ok
test_shape_is_checked_by_hand_until_the_schema_lands ... ok
test_shape_rules_and_the_decision_sentence_are_pinned ... ok
test_task_file_review_is_one_round_with_a_fixed_stop_condition ... ok
test_the_bot_wait_filters_the_codex_bot ... ok
test_the_ci_watch_is_joined_before_the_result ... ok
test_the_ci_watcher_survives_the_no_checks_race ... ok
test_the_orchestrator_watches_from_github_and_history ... ok
test_the_worker_stops_itself_on_repeated_findings ... ok
test_threat_table_rule_carries_no_grammar ... ok
test_workers_commit_inside_the_sandbox ... ok
test_workers_open_the_pr_as_a_draft ... ok
Ran 45 tests in 0.012s
OK
```

## 3. Removal proofs (`scratchpad/mutate_a7_a02.py`: each new token removed inside its section in a `git archive HEAD` copy of the working tree, then the whole docs module run)

```
== removed token: counted toward the classes at any priority and toward the fix cap at P0 or P1, never INV-6's heads
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: carries a badge, P0 to P3
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: read as the counters bullet prescribes
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== removed token: head=<full sha>
   failing tests: test_regime_rule_sections_are_pinned_whole, test_result_head_is_in_the_contract
== removed token: the first RESULT's head is INV-6's baseline
   failing tests: test_regime_rule_sections_are_pinned_whole, test_result_head_is_in_the_contract
== restored: OK
```

## 4. A7-1 before the push: the complete `--history-only` output

```
$ scripts/regime-counters.sh dotfiles-T128-worker-stop-and-watch-a02 --history-only
task=dotfiles-T128-worker-stop-and-watch-a02 tasks=1 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-12T02:54:30Z..none (-) source=live
detail: pr=none authors=claude-deep-dot tasks=01a12e08-7a70-73a9-8437-bd8b05332226 results=- questions=- withdrawn=- bot_heads=- source=live
rc=0
```

## 5. CompactionDB (main checkout, outside the sandbox through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-worker-stop-and-watch-a02 …'
dccaabd2-91e1-4256-9f2c-b934222c3b19
```

## 6. Bot fix round 1 (threads 4244354410, 4244354413, 4244354417)

A7-1 after the Bot round, before the fix commit: the three threads of review 5486194208 (each a class at 1), and no head after a first RESULT:

```
4244354410 P1 Establish the PR identifier before starting the watch
4244354413 P1 Count repeated findings even when no fix commit follows
4244354417 P1 Define how the watcher derives the A2 fix-round count
$ git diff --stat HEAD -- home tests; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime/*.md 2>&1 | tail -1
 home/dot_agents/skills/agmsg-orchestration/SKILL.md | 4 ++--
 tests/fixtures/regime/orchestrator-step-7.md        | 2 +-
 tests/fixtures/regime/worker-step-15.md             | 2 +-
 tests/unit/test_agmsg_orchestration_docs.py         | 5 +++++
 4 files changed, 9 insertions(+), 4 deletions(-)
Ran 45 tests in 0.009s

OK
All matched files use Prettier code style!
```

Removal proofs (`scratchpad/mutate_a7_a02_f1.py`):

```
== removed token: After every Bot review round, before deciding whether a fix commit follows
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: `gh pr list --head <the task's branch> --json number`
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== removed token: A fix round is a push whose predecessor head carries a Codex P0/P1 finding
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== restored: OK
```

A7-1 before the push, the complete `--history-only` output:

```
$ scripts/regime-counters.sh dotfiles-T128-worker-stop-and-watch-a02 --history-only
task=dotfiles-T128-worker-stop-and-watch-a02 tasks=1 amendments=0 questions=1 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-12T02:54:30Z..none (-) source=live
detail: pr=none authors=claude-deep-dot tasks=01a12e08-7a70-73a9-8437-bd8b05332226 results=- questions=01a12e10-3ad0-7b82-8718-e18bb4590029 withdrawn=- bot_heads=- source=live
rc=0
```

## 8. Amendment 1 and revise round 1 (`previous_head=3a54d340`; §7 is the main-checkout copy's final head of the first RESULT)

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-worker-stop-and-watch-a02.md .orchestration/dotfiles-T128-worker-stop-and-watch-a02/task.md | cut -c1-64
1de19e51b9e23edff9bfc21a64e92a6755ddf247d12c3cf98456bb7629e3878e
1de19e51b9e23edff9bfc21a64e92a6755ddf247d12c3cf98456bb7629e3878e
$ git diff --stat HEAD -- home tests; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime/*.md 2>&1 | tail -1
 home/dot_agents/skills/agmsg-orchestration/SKILL.md |  4 ++--
 tests/fixtures/regime/message-contract.md           |  2 +-
 tests/fixtures/regime/orchestrator-step-7.md        |  2 +-
 tests/unit/test_agmsg_orchestration_docs.py         | 10 ++++++++--
 4 files changed, 12 insertions(+), 6 deletions(-)
Ran 45 tests in 0.011s

OK
All matched files use Prettier code style!
```

Removal proofs (`scratchpad/mutate_a7_a02_r1.py`):

```
== removed token: badged finding of any priority
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== removed token: a mismatch is answered with `status=revise`
   failing tests: test_question_pongs_are_in_the_contract, test_regime_rule_sections_are_pinned_whole
== restored: OK
```

A7-1 before the push, the complete `--history-only` output:

```
$ scripts/regime-counters.sh dotfiles-T128-worker-stop-and-watch-a02 --history-only
task=dotfiles-T128-worker-stop-and-watch-a02 tasks=2 amendments=1 questions=1 results=1 withdrawn=0 revises=0 first_result_head=3a54d340e9078ba3565237f6d73a00d8fc2d75e9 bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-12T02:54:30Z..2026-10-12T03:18:33Z (0:24) source=live
detail: pr=323 authors=claude-deep-dot tasks=01a12e08-7a70-73a9-8437-bd8b05332226,01a12e76-ad60-7ec6-858b-cae29845dddc results=01a12e1e-7f28-787a-8270-9546f18bd95c questions=01a12e10-3ad0-7b82-8718-e18bb4590029 withdrawn=- bot_heads=- source=live
rc=0
```
