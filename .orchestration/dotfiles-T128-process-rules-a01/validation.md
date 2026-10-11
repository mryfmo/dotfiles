# Validation: dotfiles-T128-process-rules-a01

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `docs/regime-pattern` at the content head `f7c229ff`. This file is committed with the evidence in a later commit, so it covers the previous head, as design INV-8 states.

## 0. Task file and branch

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-process-rules-a01.md | cut -d' ' -f1
65fa34940e04979f4430f07ce8bfbb29208b12f5646034fbdfa1667c5baa2e0e
$ shasum -a 256 .orchestration/dotfiles-T128-process-rules-a01/task.md | cut -d' ' -f1    # the first commit's copy
65fa34940e04979f4430f07ce8bfbb29208b12f5646034fbdfa1667c5baa2e0e
$ gh pr create --draft …   (04:19Z, 3 minutes after the TASK at 04:16:13Z)
https://github.com/mryfmo/dotfiles/pull/318
$ gh pr ready 318 --repo mryfmo/dotfiles; date -u +%FT%TZ
✓ Pull request mryfmo/dotfiles#318 is marked as "ready for review"
2026-10-11T04:21:24Z
```

## 1. Checks (task validation: prettier on the two prose files, the docs test)

```
$ git log --oneline -3; git status --porcelain | wc -l
f7c229ff docs(regime): the review and fix pattern as regime rules
1c59f1cc chore(orchestration): task file for dotfiles-T128-process-rules-a01
b896d9bc chore(orchestration): boundary commit 2026-10-11 (regime v3 design accepted) (#316)
       0
$ prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -2; echo "rc=${pipestatus[1]}"
Checking formatting...
All matched files use Prettier code style!
rc=0
$ uv run python -m unittest tests.unit.test_agmsg_orchestration_docs -v 2>&1 | grep -E "AgmsgRegimePatternTest|^Ran|^OK|^FAILED"
test_a_boundary_pr_never_gates_a_dispatch (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_boundary_pr_never_gates_a_dispatch) ... ok
test_a_revise_acceptance_names_the_previous_head_and_a_check (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_revise_acceptance_names_the_previous_head_and_a_check) ... ok
test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) ... ok
test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first) ... ok
test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestration_records_and_threat_tables) ... ok
test_counters_run_before_every_acceptance_action (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_run_before_every_acceptance_action) ... ok
test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) ... ok
test_task_file_review_is_one_round_with_a_fixed_stop_condition (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_task_file_review_is_one_round_with_a_fixed_stop_condition) ... ok
Ran 25 tests in 0.009s
OK
$ ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; echo "rc=$?"
1 file already formatted
rc=0
$ git diff --stat origin/main...HEAD
 .../dotfiles-T128-process-rules-a01/task.md        | 68 ++++++++++++++++++++
 AGENTS.md                                          |  6 ++
 .../dot_agents/skills/agmsg-orchestration/SKILL.md | 10 ++-
 tests/unit/test_agmsg_orchestration_docs.py        | 74 ++++++++++++++++++++++
 4 files changed, 157 insertions(+), 1 deletion(-)
```

## 2. Premises, re-run (task front matter)

The local commands ran in the sandbox, the `gh` commands outside it. The design-review RESULT count is 27 now; the task file stamped 26 at 04:13:28Z and says the count grows with every round.

```
$ date -u +%FT%TZ; ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conformance --limit 1000 | grep -c 'AGMSG-RESULT v1 task_id=dotfiles-T128-design-review-a01'
2026-10-11T04:21:54Z
agmsg: did not name or record this pane: this seat resolved herdr:~/.config/herdr/herdr.sock:w5:p4, and that pane is already recorded as 01a0fa8d-c088-7bf0-8eb7-1f9171449a35__01a12527-be20-7c17-8f0d-fae79ae95475's. Keeping that seat's name and record. If that seat is gone, drop or despawn it and act again. (#1114 placement guard, kept alongside #1112's label-first resolution.)
27
$ grep -n 'Code Review Rules' AGENTS.md
67:## Code Review Rules
$ wc -w home/dot_config/claude/rules/agmsg-orchestration.md
     447 home/dot_config/claude/rules/agmsg-orchestration.md
$ gh api --paginate repos/mryfmo/dotfiles/pulls/317/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id[0:8],.submitted_at]|@tsv'
32fe9a36	2026-10-11T02:37:13Z
56ca6c69	2026-10-11T02:52:38Z
de138f65	2026-10-11T03:03:00Z
f6528bba	2026-10-11T03:10:28Z
98f1d250	2026-10-11T03:24:14Z
2602f575	2026-10-11T03:43:58Z
e314c502	2026-10-11T04:04:13Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/317/reviews --jq '.[0].submitted_at'
2026-10-11T02:37:13Z
```

## 3. Each rule fails its test when its sentence is removed (`scratchpad/mutate-t128.sh` at `e9ae8b65`: one sentence or bullet deleted at a time in a `git archive HEAD` copy, then the named test)

```
== removed rule: paired-design-review (SKILL, diff lines: 1) -> test_design_review_runs_in_paired_rounds_with_a_cap
FAIL: test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) (tok
AssertionError: 'get the same design hash at the same time' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions
FAIL: test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) (tok
== removed rule: round-cap (SKILL, diff lines: 2) -> test_design_review_runs_in_paired_rounds_with_a_cap
FAIL: test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) (tok
AssertionError: 'After at most three revision rounds the design is frozen' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and repo
FAIL: test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) (tok
== removed rule: one-round-task-review (SKILL, diff lines: 1) -> test_task_file_review_is_one_round_with_a_fixed_stop_condition
FAIL: test_task_file_review_is_one_round_with_a_fixed_stop_condition (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_task_file_review_is_one_round_with_a_fixe
AssertionError: 'A task-file review is one round with a fixed stop condition' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and r
FAILED (failures=1)
== removed rule: boundary-pr (SKILL, diff lines: 1) -> test_a_boundary_pr_never_gates_a_dispatch
FAIL: test_a_boundary_pr_never_gates_a_dispatch (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_boundary_pr_never_gates_a_dispatch)
AssertionError: 'is never a prerequisite of a dispatch' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: tr
FAILED (failures=1)
== removed rule: threat-table (SKILL, diff lines: 1) -> test_a_trust_boundary_task_carries_a_threat_table
FAIL: test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) (<redacted:secret-pattern>carries a `threat_table` in its front matter' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissi
FAIL: test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) (<redacted:secret-pattern>Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>`' not found in '\n\n- Review every RESULT advers
FAILED (failures=1)
== removed rule: pr-ready-first (SKILL, diff lines: 1) -> test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first
FAIL: test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_f
AssertionError: 'Mark the PR ready for review with `gh pr ready <n>` before the wait' not found in ', wait for CI and the Codex Bot before sending RESULT.\n    - Run `gh pr checks 
FAIL: test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_f
== removed rule: bot-round-cap (SKILL, diff lines: 2) -> test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first
FAIL: test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_f
AssertionError: 'at most twice. The third Bot round is not fixed' not found in ', wait for CI and the Codex Bot before sending RESULT.\n    - Mark the PR ready for review with `gh 
FAIL: test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_f
== removed rule: revise-contract (SKILL, diff lines: 1) -> test_a_revise_acceptance_names_the_previous_head_and_a_check
FAIL: test_a_revise_acceptance_names_the_previous_head_and_a_check (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_revise_acceptance_names_the_previous_head
AssertionError: 'carries `previous_head=<the RESULT head being revised>`' not found in '\n\nSend messages as single-line records so inbox/history output stays parseable.\n\n`AGMSG-
FAILED (failures=1)
== removed rule: counters-by-hand-until-a3 (SKILL, diff lines: 2) -> test_counters_run_before_every_acceptance_action
FAIL: test_counters_run_before_every_acceptance_action (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_run_before_every_acceptance_action)
AssertionError: 'until it is on `main`, the orchestrator counts the same things by hand' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, secu
FAILED (failures=1)
== removed rule: bot-wait-alongside-ci (SKILL, diff lines: 2) -> test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first
FAIL: test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_f
AssertionError: 'in the background and the Bot wait below at the same time' not found in ', wait for CI and the Codex Bot before sending RESULT.\n    - Mark the PR ready for review
FAIL: test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_bot_fix_rounds_are_capped_and_the_pr_is_ready_f
== removed rule: code-review-subsection (AGENTS, diff lines: 6) -> test_code_review_rules_cover_orchestration_records_and_threat_tables
ERROR: test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestrat
FAILED (errors=1)
== removed rule: residual-not-reraised (AGENTS, diff lines: 2) -> test_code_review_rules_cover_orchestration_records_and_threat_tables
FAIL: test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestrati
AssertionError: 'Do not re-raise a `residual` row' not found in "\n\n- Files under `.orchestration/**` are the regime's records and task specifications, which the regime's own revi
FAILED (failures=1)
== restored: OK
```

## 1b. The same checks at the Bot-fix commit `e9ae8b65`

```
$ git log --oneline -1; git status --porcelain | wc -l
e9ae8b65 docs(regime): counters by hand until A3 lands; Bot window runs alongside CI
       0
$ prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -2; echo "rc=${pipestatus[1]}"
Checking formatting...
All matched files use Prettier code style!
rc=0
$ uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3
Ran 25 tests in 0.006s

OK
$ ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; echo "rc=$?"
1 file already formatted
rc=0
```

## 4. Bot round 1 on `f7c229ff` (A2: ready at 04:21:24Z, Bot wait alongside CI)

```
$ (Bot wait loop: reviews and top-level comments of the head, the connector summary's Code Review row, the 👍 reaction; @codex review after 10 minutes from ready)
poll 3 04:26:27Z head f7c229fff279e6f98e2025ebb3b2be42912ed722 asked=no
reviews: 5481888792	f7c229fff279e6f98e2025ebb3b2be42912ed722	2026-10-11T04:26:14Z	chatgpt-codex-connector[bot]
comments: 4240250137	f7c229fff279e6f98e2025ebb3b2be42912ed722	home/dot_agents/skills/agmsg-orchestration/SKILL.md	chatgpt-codex-connector[bot]
4240250141	f7c229fff279e6f98e2025ebb3b2be42912ed722	home/dot_agents/skills/agmsg-orchestration/SKILL.md	chatgpt-codex-connector[bot]
code-review-completed: | 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T04:26:18.074875Z">2026-10-11T04:26:18.074875Z</relative-time> | `f7c229f` | Draft marked ready |
+1: 
```

The review arrived 5 minutes after ready, so no `@codex review` was posted. The first loop stopped at 04:24:54Z on the summary's `"status":"completed"`, which the security review set while the code review was still running (learning item 2); the second loop waited for the Code Review row.

- 4240250137 (P1, SKILL.md:72): `scripts/regime-counters.sh` does not exist before plan 006 A3, so the rule would block every acceptance. Fixed in `e9ae8b65`: counts by hand from `history.sh` and the task's `.orchestration` files, commands and output pasted, until the script is on `main`. Test: `test_counters_run_before_every_acceptance_action`.
- 4240250141 (P2, SKILL.md:202): `gh pr checks --watch` ran before the Bot timer. Fixed in `e9ae8b65`: CI watch in the background alongside the Bot wait, the marks counted from `gh pr ready` (from the push for a later head). Test: `test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first`.

This is Bot fix round 1 of the two A2 allows.

## 5. CompactionDB `memory add` (main checkout, outside the sandbox through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128 plan 006 Phase A (worker claude-standard-dot-a003, 2026-10-11, PR 318): the regime review and fix pattern lives in the agmsg-orchestration SKILL. … AGENTS.md Code Review Rules: .orchestration reviewed for secrets and home paths only, trust-boundary code against its threat_table.'
70b799fb-e5e6-41be-b4d4-f82208c715d9
```
