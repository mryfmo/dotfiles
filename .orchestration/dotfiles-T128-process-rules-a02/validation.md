# Validation: dotfiles-T128-process-rules-a02

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `docs/regime-pattern` (PR #318). This branch copy covers heads through `3ff0cade`; the main-checkout copy adds the final head (design INV-8).

## 1. Checks at `3ff0cade` (task validation: prettier on the two prose files, the docs test -v)

```
$ git log --oneline -4; git status --porcelain | wc -l
3ff0cade docs(regime): the manual counters read Bot review bodies too
c31b8327 docs(regime): threat-table rule without a payload grammar; open threads have an outcome
7382fb01 chore(orchestration): task file for dotfiles-T128-process-rules-a02
aeb6c5ad chore(orchestration): T128 Phase A evidence after the revise round's second Bot round
       0
$ prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -2; echo "rc=${pipestatus[1]}"
Checking formatting...
All matched files use Prettier code style!
rc=0
$ uv run python -m unittest tests.unit.test_agmsg_orchestration_docs -v 2>&1 | grep -E "AgmsgRegimePatternTest|^Ran|^OK|^FAILED" | sed -E "s/ \(tests[^)]*\)//"
test_a_boundary_pr_never_gates_a_dispatch ... ok
test_a_revise_acceptance_names_the_previous_head_and_a_check ... ok
test_a_trust_boundary_task_carries_a_threat_table ... ok
test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first ... ok
test_code_review_rules_cover_orchestration_records_and_threat_tables ... ok
test_counters_run_before_every_acceptance_action ... ok
test_design_review_runs_in_paired_rounds_with_a_cap ... ok
test_manual_counts_read_the_whole_history ... ok
test_open_review_body_findings_have_an_identifier ... ok
test_open_third_round_threads_have_an_integration_outcome ... ok
test_task_file_review_is_one_round_with_a_fixed_stop_condition ... ok
test_the_ci_watch_is_joined_before_the_result ... ok
test_threat_table_rule_carries_no_grammar ... ok
Ran 30 tests in 0.007s
OK
$ ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; echo "rc=$?"
1 file already formatted
rc=0
$ shasum -a 256 .orchestration/dotfiles-T128-process-rules-a02/task.md
0a31acb474089c3c1ef74480b4a7f03512165e68132d5863171c81263428f079  .orchestration/dotfiles-T128-process-rules-a02/task.md
```

## 2. Verbatim replacement check (items 1, 2, 4, 5 against the task file; `scratchpad/a02_verify.py` at `c31b8327`)

```
item1 bullet verbatim in SKILL: True
item2 bullet verbatim in AGENTS.md: True
item4 new text present: True
item5 sentence ends step 10.1: True
old grammar gone: True
```

Item 4 was extended in `3ff0cade` (§5); that check ran before. The old AGENTS.md test tokens of the replaced bullet moved to the new bullet's sentences, in `test_code_review_rules_cover_orchestration_records_and_threat_tables`.

## 3. Removal proofs (`scratchpad/mutate-a02.sh` at `3ff0cade`: each new token removed, and the old grammar pasted back, in a `git archive HEAD` copy)

```
== removed rule: item1-closed-form (SKILL, diff lines: 2) -> test_a_trust_boundary_task_carries_a_threat_table
FAIL: test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) (<redacted:secret-pattern>`closed: tests/<file>::<name>`' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to re
FAILED (failures=1)
== removed rule: item1-residual-form (SKILL, diff lines: 2) -> test_a_trust_boundary_task_carries_a_threat_table
FAIL: test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) (<redacted:secret-pattern>`residual: <sentence>`' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it,
FAILED (failures=1)
== removed rule: item1-out-of-scope-form (SKILL, diff lines: 2) -> test_a_trust_boundary_task_carries_a_threat_table
FAIL: test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) (<redacted:secret-pattern>`out-of-scope: <task id>`' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute 
FAILED (failures=1)
== removed rule: item1-shape-is-the-schema (SKILL, diff lines: 2) -> test_a_trust_boundary_task_carries_a_threat_table
FAIL: test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) (<redacted:secret-pattern>Shape is `schemas/task.json`'s" not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to re
FAILED (failures=1)
== removed rule: item1-substance-is-the-reviewers (SKILL, diff lines: 2) -> test_a_trust_boundary_task_carries_a_threat_table
FAIL: test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) (<redacted:secret-pattern>Substance is the reviewers'" not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refut
FAILED (failures=1)
== removed rule: item1-completion-condition (SKILL, diff lines: 2) -> test_a_trust_boundary_task_carries_a_threat_table
FAIL: test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) (<redacted:secret-pattern>The table is the task's completion condition" not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissi
FAIL: test_a_trust_boundary_task_carries_a_threat_table (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_a_trust_boundary_task_carries_a_threat_table) (<redacted:secret-pattern>^(closed|residual|out-of-scope)' unexpectedly found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions:
FAILED (failures=1)
== removed rule: item1-old-none-pasted-back (SKILL, diff lines: 2) -> test_threat_table_rule_carries_no_grammar
FAIL: test_threat_table_rule_carries_no_grammar (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_threat_table_rule_carries_no_grammar)
AssertionError: '`none`' unexpectedly found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, indepe
FAILED (failures=1)
== removed rule: item2-missing-table-or-row (AGENTS, diff lines: 2) -> test_code_review_rules_cover_orchestration_records_and_threat_tables
FAIL: test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestrati
AssertionError: 'report a missing table or a missing row' not found in "\n\n- Files under `.orchestration/**` are the regime's records and task specifications, which the regime's o
FAILED (failures=1)
== removed rule: item2-substance-per-form (AGENTS, diff lines: 2) -> test_code_review_rules_cover_orchestration_records_and_threat_tables
FAIL: test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestrati
AssertionError: 'a `residual` row whose control does not mitigate the risk' not found in "\n\n- Files under `.orchestration/**` are the regime's records and task specifications, wh
FAIL: test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestrati
== removed rule: item2-residual-not-reraised (AGENTS, diff lines: 2) -> test_code_review_rules_cover_orchestration_records_and_threat_tables
FAIL: test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestrati
AssertionError: 'Do not re-raise a `residual` row whose control mitigates the risk' not found in "\n\n- Files under `.orchestration/**` are the regime's records and task specificat
FAILED (failures=1)
== removed rule: item2-shape-is-the-schema (AGENTS, diff lines: 2) -> test_code_review_rules_cover_orchestration_records_and_threat_tables
FAIL: test_code_review_rules_cover_orchestration_records_and_threat_tables (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_code_review_rules_cover_orchestrati
AssertionError: "Shape (the test selector, the sentence, the owning task id) is the schema's to check, not the review's" not found in "\n\n- Files under `.orchestration/**` are the
FAILED (failures=1)
== removed rule: item4-history-limit (SKILL, diff lines: 2) -> test_manual_counts_read_the_whole_history
FAIL: test_manual_counts_read_the_whole_history (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_manual_counts_read_the_whole_history)
AssertionError: 'with an explicit `--limit 1000`' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to r
FAILED (failures=1)
== removed rule: fix1-review-bodies (SKILL, diff lines: 2) -> test_counters_run_before_every_acceptance_action
FAIL: test_counters_run_before_every_acceptance_action (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_run_before_every_acceptance_action)
AssertionError: 'P0/P1-badged Bot review bodies grouped by `commit_id`' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporti
FAILED (failures=1)
== removed rule: item5-open-is-a-sweep-item (SKILL, diff lines: 2) -> test_open_third_round_threads_have_an_integration_outcome
FAIL: test_open_third_round_threads_have_an_integration_outcome (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_open_third_round_threads_have_an_integration_o
AssertionError: 'is a sweep item like any other' not found in '\n\n1. Join or confirm the agmsg team and identities with the `agmsg` scripts.\n2. Create the `.orchestration` direct
FAIL: test_open_third_round_threads_have_an_integration_outcome (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_open_third_round_threads_have_an_integration_o
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
$ (in the main checkout) sha256sum .orchestration/validation/dotfiles-T128-process-rules-redesign-a01.md
b95b4eacb3b7ef3f8cc8f0da438062e4a794a1e96139268b9cecc6b4df0b40e4  .orchestration/validation/dotfiles-T128-process-rules-redesign-a01.md
```

## 5. Bot round 1 on `c31b8327` (pushed 05:22:13Z; review 5482021584 at 05:25:42Z, so no `@codex review`)

```
poll 8 05:26:13Z head c31b8327e026ec6604a1b0846d217ef456788cd1 asked=no
reviews: 5482021584	c31b8327e026ec6604a1b0846d217ef456788cd1	2026-10-11T05:25:42Z	chatgpt-codex-connector[bot]
comments: 4240382519	c31b8327e026ec6604a1b0846d217ef456788cd1	home/dot_agents/skills/agmsg-orchestration/SKILL.md	chatgpt-codex-connector[bot]
code-review-completed: | 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T05:25:44.527064Z">2026-10-11T05:25:44.527064Z</relative-time> | `c31b832` | New commits |
```

- 4240382519 (P1, SKILL.md:72, the counters bullet, not the threat-table payload wording): the by-hand counts read only inline comments, while a Bot finding can live only in a review body. Fixed in `3ff0cade`: P0/P1-badged Bot review bodies (`pulls/<n>/reviews`, by `commit_id`) are counted too. Test: `test_counters_run_before_every_acceptance_action`. Fix round 1 of the two A2 allows.

## 6. CompactionDB `memory add` (main checkout, outside the sandbox through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128 process-rules a02 (reset of a01 after INV-6 and plan 006 S1 on the disposition-grammar class; …) …'
05618498-52b4-4708-8262-8b762c5ce8e0
```

## 7. Revise round 1 (the revise commit; `previous_head=27ea99b2`)

```
$ UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py; prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -1
Ran 34 tests in 0.008s

OK
1 file already formatted
All checks passed!
All matched files use Prettier code style!
$ git diff --stat -- AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md tests/unit/test_agmsg_orchestration_docs.py
 AGENTS.md                                          |  4 +-
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |  4 +-
 tests/unit/test_agmsg_orchestration_docs.py        | 48 ++++++++++++++++++++++
 3 files changed, 52 insertions(+), 4 deletions(-)
```

Removal proofs (`scratchpad/mutate-a02-r1.sh`: the working tree's three files in a `git archive HEAD` copy, each sentence removed alone, the old first bullet pasted back; output cut to three lines of at most 400 characters per rule, and the masker replaces each `subTest` label, which it reads as a secret pattern):

```
== removed rule: bot-review-scope (AGENTS, diff lines: 2) -> test_orchestration_records_rule_binds_the_bot_review_only
FAIL: test_orchestration_records_rule_binds_the_bot_review_only (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_orchestration_records_rule_binds_the_bot_review_only) (<redacted:secret-pattern>)
AssertionError: 'in the pull-request review by the Codex Bot, review them for secrets and home-directory paths only' not found in "Files under `.orchestration/**` are the regime's records and task specifications, which the regime's own reviewers review; review them for secrets and home-directory paths only. The task-level audit keeps the full scope of the Audit section."
FAILED (failures=1)
== removed rule: audit-keeps-full-scope (AGENTS, diff lines: 2) -> test_orchestration_records_rule_binds_the_bot_review_only
FAIL: test_orchestration_records_rule_binds_the_bot_review_only (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_orchestration_records_rule_binds_the_bot_review_only) (<redacted:secret-pattern>)
AssertionError: 'The task-level audit keeps the full scope of the Audit section.' not found in "Files under `.orchestration/**` are the regime's records and task specifications, which the regime's own reviewers review; in the pull-request review by the Codex Bot, review them for secrets and home-directory paths only."
FAILED (failures=1)
== removed rule: old-first-bullet-pasted-back (AGENTS, diff lines: 2) -> test_orchestration_records_rule_binds_the_bot_review_only
FAIL: test_orchestration_records_rule_binds_the_bot_review_only (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_orchestration_records_rule_binds_the_bot_review_only) (<redacted:secret-pattern>)
AssertionError: 'in the pull-request review by the Codex Bot, review them for secrets and home-directory paths only' not found in "Files under `.orchestration/**` are the regime's records and task specifications, which the regime's own reviewers review; review them for secrets and home-directory paths only."
FAIL: test_orchestration_records_rule_binds_the_bot_review_only (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_orchestration_records_rule_binds_the_bot_review_only) (<redacted:secret-pattern>)
== removed rule: shape-by-hand-skill (SKILL, diff lines: 2) -> test_shape_is_checked_by_hand_until_the_schema_lands
FAIL: test_shape_is_checked_by_hand_until_the_schema_lands (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_is_checked_by_hand_until_the_schema_lands) (section='SKILL invariants')
AssertionError: 'Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand.' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review
FAILED (failures=1)
== removed rule: shape-by-hand-agents (AGENTS, diff lines: 2) -> test_shape_is_checked_by_hand_until_the_schema_lands
FAIL: test_shape_is_checked_by_hand_until_the_schema_lands (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_shape_is_checked_by_hand_until_the_schema_lands) (section='AGENTS.md')
AssertionError: 'Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand.' not found in "\n\n- Files under `.orchestration/**` are the regime's records and task specifications, which the regime's own reviewers review; in the pull-request review by the Codex Bot, review them for secrets and home-directory paths only. The task-level audit keeps the full 
FAILED (failures=1)
== removed rule: closed-row-verification (AGENTS, diff lines: 2) -> test_pattern_rules_pin_their_safeguards
FAIL: test_pattern_rules_pin_their_safeguards (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_pattern_rules_pin_their_safeguards)
AssertionError: 'report a `closed` row whose test does not close it' not found in "\n\n- Files under `.orchestration/**` are the regime's records and task specifications, which the regime's own reviewers review; in the pull-request review by the Codex Bot, review them for secrets and home-directory paths only. The task-level audit keeps the full scope of the Audit section.\n- Judge from the diff, 
FAILED (failures=1)
== removed rule: threat-control-enumeration (SKILL, diff lines: 2) -> test_pattern_rules_pin_their_safeguards
FAIL: test_pattern_rules_pin_their_safeguards (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_pattern_rules_pin_their_safeguards) (<redacted:secret-pattern>)
AssertionError: '(the tree and its tests, task.md, workflow files,' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; n
FAILED (failures=1)
== removed rule: reviewer-independence (SKILL, diff lines: 2) -> test_pattern_rules_pin_their_safeguards
FAIL: test_pattern_rules_pin_their_safeguards (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_pattern_rules_pin_their_safeguards) (<redacted:secret-pattern>)
AssertionError: 'a fresh Claude context on the `review` profile and a Codex read-only run' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work rema
FAILED (failures=1)
== removed rule: design-on-main-precondition (SKILL, diff lines: 2) -> test_pattern_rules_pin_their_safeguards
FAIL: test_pattern_rules_pin_their_safeguards (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_pattern_rules_pin_their_safeguards) (<redacted:secret-pattern>)
AssertionError: 'meets the design-on-main precondition' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; never delegat
FAILED (failures=1)
== removed rule: commit-inside-the-sandbox (SKILL, diff lines: 2) -> test_workers_commit_inside_the_sandbox
FAIL: test_workers_commit_inside_the_sandbox (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_commit_inside_the_sandbox) (<redacted:secret-pattern>)
AssertionError: 'Commit inside the sandbox, with `git -c commit.gpgsign=false` when the signing key is unreadable there' not found in " and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push o
FAIL: test_workers_commit_inside_the_sandbox (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_commit_inside_the_sandbox) (<redacted:secret-pattern>)
== restored: OK
```

CompactionDB (main checkout, outside the sandbox through the permission gate):

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-process-rules-a02 revise round 1 …'
aae4a1c4-c1c0-4bbb-bd54-71223252c0f4
```

## 8. The fifth item and Bot fix round 1 of the revise (`21c160c8`, `e8d20aae`, `052eea4c`)

```
$ gh pr checks 318 --repo mryfmo/dotfiles --watch --interval 30   # on 108b43bd, final table; exit 0
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	1s	https://dashboard.gitguardian.com	
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38118717869/job/114408828732	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/38118717854/job/114408829009	
private-bootstrap (ubuntu-24.04, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38118717854/job/114408828924	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38118717854/job/114408828870	
public-bootstrap (macos-14, client)	pass	8m31s	https://github.com/mryfmo/dotfiles/actions/runs/38118717854/job/114408828850	
public-bootstrap (ubuntu-24.04, client)	pass	9m59s	https://github.com/mryfmo/dotfiles/actions/runs/38118717854/job/114408828757	
public-bootstrap (ubuntu-24.04, server)	pass	7m27s	https://github.com/mryfmo/dotfiles/actions/runs/38118717854/job/114408828888	
test (macos-14, client)	pass	5m51s	https://github.com/mryfmo/dotfiles/actions/runs/38118717869/job/114408854505	
test (ubuntu-24.04, client)	pass	8m3s	https://github.com/mryfmo/dotfiles/actions/runs/38118717869/job/114408854570	
test (ubuntu-24.04, server)	pass	5m7s	https://github.com/mryfmo/dotfiles/actions/runs/38118717869/job/114408854509	
test (ubuntu-26.04, client)	pass	9m28s	https://github.com/mryfmo/dotfiles/actions/runs/38118717869/job/114408854446	
validate	pass	1m35s	https://github.com/mryfmo/dotfiles/actions/runs/38118717865/job/114408828753	
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-process-rules-a02.md .orchestration/dotfiles-T128-process-rules-a02/task.md | cut -c1-64
b6500dbfbd86d40ffc9227ef9533317060da4cdf9536a8517d96a8ef7ee6d421
b6500dbfbd86d40ffc9227ef9533317060da4cdf9536a8517d96a8ef7ee6d421
$ git log --oneline -4; UV_OFFLINE=1 uv run python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_agmsg_orchestration_docs.py; ruff check --config ruff.toml tests/unit/test_agmsg_orchestration_docs.py; prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -1
052eea4c docs(regime): the boundary-merge sentence names the in-job decision
e8d20aae chore(orchestration): task file for dotfiles-T128-process-rules-a02, Amendment 1
21c160c8 docs(regime): open the worker PR as a draft; pin the paired-round and counter-record clauses
108b43bd docs(regime): bind the records-only rule to the Bot, shape by hand until the schema, commit inside the sandbox
Ran 36 tests in 0.007s

OK
1 file already formatted
All checks passed!
All matched files use Prettier code style!
```

Removal proofs (`scratchpad/mutate-a02-r1b.sh`, the same harness with the four new rules; output cut to three lines of at most 400 characters per rule):

```
== removed rule: draft-flag (SKILL, diff lines: 2) -> test_workers_open_the_pr_as_a_draft
FAIL: test_workers_open_the_pr_as_a_draft (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_workers_open_the_pr_as_a_draft)
AssertionError: '`gh pr create --draft --head <branch>`' not found in " and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push origin <branch>` (no `-u`), and open the PR as a draft with `gh p
FAILED (failures=1)
== removed rule: revises-once-per-pair (SKILL, diff lines: 2) -> test_design_review_runs_in_paired_rounds_with_a_cap
FAIL: test_design_review_runs_in_paired_rounds_with_a_cap (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_design_review_runs_in_paired_rounds_with_a_cap) (<redacted:secret-pattern>)
AssertionError: 'The orchestrator revises once per pair of results' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; n
FAILED (failures=1)
== removed rule: counter-output-recorded (SKILL, diff lines: 2) -> test_counters_run_before_every_acceptance_action
FAIL: test_counters_run_before_every_acceptance_action (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_counters_run_before_every_acceptance_action)
AssertionError: 'and pastes its output into the acceptance record' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.\n- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; ne
FAILED (failures=1)
== removed rule: old-boundary-clause-pasted-back (SKILL, diff lines: 2) -> test_boundary_merge_sentence_names_the_in_job_decision
FAIL: test_boundary_merge_sentence_names_the_in_job_decision (tests.unit.test_agmsg_orchestration_docs.AgmsgRegimePatternTest.test_boundary_merge_sentence_names_the_in_job_decision)
AssertionError: 'each required job decides inside itself and reports success on an `.orchestration`-only diff; a skipped required job would report Success (fail-open), so no required job carries a job-level `if` or a `needs`.' not found in '\n\n- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings,
FAILED (failures=1)
== restored: OK
```
