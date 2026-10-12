# Validation: dotfiles-T128-worker-stop-and-watch-a01

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `docs/worker-stop-and-watch`. This branch copy covers `218ac77e`; the main-checkout copy adds the PR, the final head and its CI and Bot round (design INV-8).

## 1. Task file

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-worker-stop-and-watch-a01.md .orchestration/dotfiles-T128-worker-stop-and-watch-a01/task.md | cut -c1-64
84d8acde766ff997b9f9ed6122274f4cd68dd46bcd64e69b3775d7e24d23ae2a
84d8acde766ff997b9f9ed6122274f4cd68dd46bcd64e69b3775d7e24d23ae2a
```

## 2. Checks at `218ac77e` (task validation: prettier, the docs test -v, the whole-section pin with the two fixtures)

```
$ git log --oneline -3; git show --stat --format= 218ac77e; prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime/*.md 2>&1 | tail -1; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py
218ac77e docs(regime): the worker stops itself on repeated findings; the orchestrator watches from GitHub and history
e596fd88 chore(orchestration): task file for dotfiles-T128-worker-stop-and-watch-a01
e83e923d docs(regime): the review and fix pattern as regime rules (round caps, threat tables, Bot rounds) (#318)
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  4 ++-
 tests/fixtures/regime/orchestrator-step-7.md       |  2 +-
 tests/fixtures/regime/worker-step-15.md            |  2 ++
 tests/unit/test_agmsg_orchestration_docs.py        | 31 ++++++++++++++++++++++
 4 files changed, 37 insertions(+), 2 deletions(-)
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
Ran 44 tests in 0.011s
OK
```

## 3. Removal proofs (`scratchpad/mutate_a7.py` at `218ac77e`: each of the fourteen tokens removed inside its section in a `git archive HEAD` copy of the working tree, then the whole docs module run)

```
== removed token: fixes nothing more
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: status=blocked note=S1|INV-6
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: whichever limit comes first ends the fixing
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: never a disposition
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: never for a fourth round of the same class
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: not only the current head's
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: and the review bodies whose `commit_id`, is at or after the task's first commit on the PR
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: counted toward the fix cap and the classes, never INV-6's heads
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: --history-only
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: at least every 30 minutes after a TASK
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== removed token: `…/pulls/<n>/comments`
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== removed token: never detects completion, which stays the RESULT's arrival
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== removed token: 45 minutes without a push, a PONG or a RESULT is a stall
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== removed token: `herdr-agents --remove-worker <worktree> --force`
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== restored: OK
```

## 4. Premises, re-run (the gh one outside the sandbox)

```
$ gh api --paginate repos/mryfmo/dotfiles/pulls/317/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id[0:8],.submitted_at]|@tsv'
32fe9a36	2026-10-11T02:37:13Z
56ca6c69	2026-10-11T02:52:38Z
de138f65	2026-10-11T03:03:00Z
f6528bba	2026-10-11T03:10:28Z
98f1d250	2026-10-11T03:24:14Z
2602f575	2026-10-11T03:43:58Z
e314c502	2026-10-11T04:04:13Z
$ ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conformance --limit 1000 | grep -E '2026-10-11T03:(27:02|46:22)Z' | cut -c1-120   # premise 1's read state, in place of the sqlite3 query (● unread, ○ read)
  ● [2026-10-11T03:27:02Z] claude-deep-dot → claude-standard-dot-a002: AGMSG-PING v1 task_id=dotfiles-T128-v0-main-tests
  ● [2026-10-11T03:46:22Z] claude-deep-dot → claude-standard-dot-a002: AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-v0-main
$ git show origin/docs/regime-pattern:home/dot_agents/skills/agmsg-orchestration/SKILL.md | grep -n 'Then list the Bot' | cut -c1-400
205:    - Then list the Bot's reviews of the final head with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/reviews --jq '.[]|select(.user.login=="chatgpt-codex-connector[bot]" and .commit_id=="<head-sha>")|[.commit_id,.submitted_at]|@tsv'` and the Bot's top-level review comments raised on it with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/comments --jq '.[]|select(.in_reply_to_id == nul
$ grep -n 'storage_history\|live store\|from the worktree\|--history-only' .orchestration/reports/dotfiles-T128-regime-counters-a01.md | head -4 | cut -c1-200   # in the main checkout
10:1. `scripts/regime-counters.sh` (new, 149 lines, shdoc header, shellcheck and shfmt clean). `<task id> [--team] [--pr] [--history-only] [--reset-hash <sha256>] [--history-file <tsv>] [--github-file
21:- invariant: INV-6 → scripts/regime-counters.sh:85 (history through `storage_history`, the whole team, no `--limit`; schema guard :83)
```

Premise 1: the seven Bot review heads equal the task's output. The read state of messages 407 and 408 is read through `history.sh`, not the task's `sqlite3` query, because the agmsg skill forbids constructing the store path or invoking `sqlite3` directly. Both show `●`, while messages this seat has read show `○`, which is consistent with "UNREAD". Premise 2: the claim holds; the line moved from 203 to 205, and its filter now reads `.user.login=="chatgpt-codex-connector[bot]"` (a03's revise round, `386f97ff`, now on `main`). Premise 3 equals the task's output.

## 5. A7-1: the `--history-only` count before the first push

```
$ scripts/regime-counters.sh dotfiles-T128-worker-stop-and-watch-a01 --history-only   # A7-1, before the first push
task=dotfiles-T128-worker-stop-and-watch-a01 tasks=1 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-12T01:41:55Z..none (-) source=live
detail: pr=none authors=claude-deep-dot tasks=01a12dc6-06b8-721a-8648-f2dfeaca1ad6 results=- questions=- withdrawn=- bot_heads=- source=live
rc=0
```

## 6. CompactionDB (main checkout, outside the sandbox through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-worker-stop-and-watch-a01 …'
8d4a9e78-4caa-4211-91dc-6208369b7100
```

## 7. Bot fix round 1 (Amendment 1; threads 4244128840, 4244128846, 4244128851, 4244128854, 4244128857, 4244128859)

A7-1 before the fix commit: the six threads of review 5485951311 with their priority and title (the class is the first three words, badge stripped, lower-cased; each class counts 1), and no head after a first RESULT, because none was sent:

```
4244128840 P2 Paginate every endpoint used by the watcher
4244128846 P2 Include every review finding in the S1 class count
4244128851 P1 Encode review-derived classes before dispatching the PONG
4244128854 P1 Choose one third-round handoff instead of waiting forever
4244128857 P2 Preserve the complete counter output in validation
4244128859 P2 Quarantine a forced worker worktree before reseating it
```

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-worker-stop-and-watch-a01.md .orchestration/dotfiles-T128-worker-stop-and-watch-a01/task.md | cut -c1-64
b0b8459834bf11869843ba685d795538523f1fa19adb2c30777586b11bed0b19
b0b8459834bf11869843ba685d795538523f1fa19adb2c30777586b11bed0b19
$ git diff --stat HEAD -- home tests; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime/*.md 2>&1 | tail -1; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py
 home/dot_agents/skills/agmsg-orchestration/SKILL.md | 6 +++---
 tests/fixtures/regime/orchestrator-step-7.md        | 2 +-
 tests/fixtures/regime/worker-step-15.md             | 4 ++--
 tests/unit/test_agmsg_orchestration_docs.py         | 8 ++++++++
 4 files changed, 14 insertions(+), 6 deletions(-)
Ran 44 tests in 0.009s

OK
All matched files use Prettier code style!
All checks passed!
```

Removal proofs (`scratchpad/mutate_a7_fix1.py`, the same harness with the six new tokens):

```
== removed token: from every finding the PR-feedback sweep would list (any reviewer, any priority, inline or review-body
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: a Bot title never (only its reduced class)
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: instead of a blocked PONG, and then waits for the ACCEPTANCE: one handoff
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: pastes its complete output (the count line, the `detail:` line and any `S2:` line)
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: all three with `--paginate`
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== removed token: the next seat is created in a clean worktree
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== restored: OK
```

A7-1 before the push, the complete `--history-only` output:

```
$ scripts/regime-counters.sh dotfiles-T128-worker-stop-and-watch-a01 --history-only
task=dotfiles-T128-worker-stop-and-watch-a01 tasks=2 amendments=1 questions=1 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-12T01:41:55Z..none (-) source=live
detail: pr=none authors=claude-deep-dot tasks=01a12dc6-06b8-721a-8648-f2dfeaca1ad6,01a12dd6-b440-76d3-88de-3e7987d1a1fe results=- questions=01a12dd0-fb68-7960-8708-444e1696975f withdrawn=- bot_heads=- source=live
rc=0
```

## 8. Bot fix round 2 (threads 4244175775, 4244175778)

A7-1 before the fix commit: the two threads of review 5486001543 (each a new class), and still no head after a first RESULT:

```
4244175775 P2 Count non-review feedback toward S1
4244175778 P2 Ping workers as soon as a stop threshold is crossed
$ git diff --stat HEAD -- home tests; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime/*.md 2>&1 | tail -1
 home/dot_agents/skills/agmsg-orchestration/SKILL.md | 4 ++--
 tests/fixtures/regime/orchestrator-step-7.md        | 2 +-
 tests/fixtures/regime/worker-step-15.md             | 2 +-
 tests/unit/test_agmsg_orchestration_docs.py         | 5 ++++-
 4 files changed, 8 insertions(+), 5 deletions(-)
Ran 44 tests in 0.009s

OK
All matched files use Prettier code style!
```

Removal proofs (`scratchpad/mutate_a7_fix2.py`):

```
== removed token: one per item `scripts/pr-feedback.py <pr>` lists, whatever its source or priority
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: as soon as it first sees a task past the A2 cap or an INV-6 count
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== restored: OK
```

A7-1 before the push, the complete `--history-only` output:

```
$ scripts/regime-counters.sh dotfiles-T128-worker-stop-and-watch-a01 --history-only
task=dotfiles-T128-worker-stop-and-watch-a01 tasks=2 amendments=1 questions=1 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-12T01:41:55Z..none (-) source=live
detail: pr=none authors=claude-deep-dot tasks=01a12dc6-06b8-721a-8648-f2dfeaca1ad6,01a12dd6-b440-76d3-88de-3e7987d1a1fe results=- questions=01a12dd0-fb68-7960-8708-444e1696975f withdrawn=- bot_heads=- source=live
rc=0
```

## 10. Revise round 1 (`previous_head=040b32f9`; §9 is the main-checkout copy's final head of the first RESULT)

```
$ git log --oneline -1; git diff --stat HEAD -- home tests; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/fixtures/regime/*.md 2>&1 | tail -1; grep -c "any reviewer, any priority" home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/unit/test_agmsg_orchestration_docs.py
8840f05d Merge branch 'main' into docs/worker-stop-and-watch
 home/dot_agents/skills/agmsg-orchestration/SKILL.md | 4 ++--
 tests/fixtures/regime/orchestrator-step-7.md        | 2 +-
 tests/fixtures/regime/worker-step-15.md             | 2 +-
 tests/unit/test_agmsg_orchestration_docs.py         | 8 ++++++--
 4 files changed, 10 insertions(+), 6 deletions(-)
Ran 44 tests in 0.009s

OK
All matched files use Prettier code style!
tests/unit/test_agmsg_orchestration_docs.py:0
home/dot_agents/skills/agmsg-orchestration/SKILL.md:0
```

Removal proofs (`scratchpad/mutate_a7_r1.py`):

```
== removed token: an early stop
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: never widens the worker's input beyond the Codex Bot's items
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: When a stop (heads=2 or three of a class) coincides with the third Bot round
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_worker_stops_itself_on_repeated_findings
== removed token: read or unread
   failing tests: test_regime_rule_sections_are_pinned_whole, test_the_orchestrator_watches_from_github_and_history
== restored: OK
```

A7-1 before the push, the complete `--history-only` output (this is the revise head's first push after the RESULT; no Bot head after it yet):

```
$ scripts/regime-counters.sh dotfiles-T128-worker-stop-and-watch-a01 --history-only
task=dotfiles-T128-worker-stop-and-watch-a01 tasks=2 amendments=1 questions=1 results=1 withdrawn=0 revises=0 first_result_head=040b32f9cfd88eb311f985a16ff434d6591acfbf bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-12T01:41:55Z..2026-10-12T02:21:47Z (0:39) source=live
detail: pr=323 authors=claude-deep-dot tasks=01a12dc6-06b8-721a-8648-f2dfeaca1ad6,01a12dd6-b440-76d3-88de-3e7987d1a1fe results=01a12dea-8290-783d-84fd-3c65453de786 questions=01a12dd0-fb68-7960-8708-444e1696975f withdrawn=- bot_heads=- source=live
rc=0
```
