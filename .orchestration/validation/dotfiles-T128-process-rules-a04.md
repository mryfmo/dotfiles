# Validation: dotfiles-T128-process-rules-a04

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `docs/regime-pattern` (PR #318). This main-checkout copy covers `28d728c5`, §6 the final head `cc9fc785` (design INV-8).

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

## 6. Final head `cc9fc785` (main-checkout copy)

```
$ gh pr checks 318 --repo mryfmo/dotfiles --watch --interval 30   # started once a check run was listed; final table; exit 0
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	1s	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38181632658/job/114595250527	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/38181632658/job/114595250542	
private-bootstrap (ubuntu-24.04, server)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/38181632658/job/114595250606	
public-bootstrap (macos-14, client)	pass	9m24s	https://github.com/mryfmo/dotfiles/actions/runs/38181632658/job/114595250567	
public-bootstrap (ubuntu-24.04, client)	pass	10m39s	https://github.com/mryfmo/dotfiles/actions/runs/38181632658/job/114595250619	
public-bootstrap (ubuntu-24.04, server)	pass	7m50s	https://github.com/mryfmo/dotfiles/actions/runs/38181632658/job/114595250348	
test (macos-14, client)	pass	5m59s	https://github.com/mryfmo/dotfiles/actions/runs/38181632591/job/114595250262	
test (ubuntu-24.04, client)	pass	8m27s	https://github.com/mryfmo/dotfiles/actions/runs/38181632591/job/114595250105	
test (ubuntu-24.04, server)	pass	5m19s	https://github.com/mryfmo/dotfiles/actions/runs/38181632591/job/114595250225	
test (ubuntu-26.04, client)	pass	7m43s	https://github.com/mryfmo/dotfiles/actions/runs/38181632591/job/114595250216	
validate	pass	1m20s	https://github.com/mryfmo/dotfiles/actions/runs/38181632586/job/114595250153	
$ bash scratchpad/bot-wait.sh 318 cc9fc785035b8d7c41ad9b12223093a8c3f27b93 2026-10-11T22:44:40Z   # last poll (Codex login filter)
poll 4 22:46:25Z head cc9fc785035b8d7c41ad9b12223093a8c3f27b93 asked=no
reviews: 
comments: 
code-review-completed: | 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T22:46:20.271557Z">2026-10-11T22:46:20.271557Z</relative-time> | `cc9fc78` | New commits |
DONE
$ # final recheck right before the RESULT
2026-10-11T22:55:48Z
$ gh pr view 318 --json headRefOid,state,isDraft
cc9fc785035b8d7c41ad9b12223093a8c3f27b93	OPEN	false
$ gh api --paginate repos/mryfmo/dotfiles/pulls/318/reviews --jq '.[]|select(.user.login=="chatgpt-codex-connector[bot]" and .submitted_at > "2026-10-11T22:00:00Z")|[.id,.commit_id[0:8],.submitted_at]|@tsv'
5485303545	386f97ff	2026-10-11T22:28:07Z
5485324335	781e6ef8	2026-10-11T22:34:55Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/318/comments --jq '.[]|select(.in_reply_to_id == null and .user.login=="chatgpt-codex-connector[bot]" and .created_at > "2026-10-11T22:00:00Z")|[.id,.original_commit_id[0:8],.path,(.original_line|tostring)]|@tsv'
4243516879	386f97ff	home/dot_agents/skills/agmsg-orchestration/SKILL.md	72
4243516880	386f97ff	home/dot_agents/skills/agmsg-orchestration/SKILL.md	202
4243537278	781e6ef8	home/dot_agents/skills/agmsg-orchestration/SKILL.md	72
4243537279	781e6ef8	home/dot_agents/skills/agmsg-orchestration/SKILL.md	68
4243537281	781e6ef8	home/dot_agents/skills/agmsg-orchestration/SKILL.md	70
$ gh api --paginate repos/mryfmo/dotfiles/issues/318/comments --jq '.[]|select(.user.login=="chatgpt-codex-connector[bot]")|.body' | grep -E 'Code Review|Security Review'
| 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T22:46:20.271557Z">2026-10-11T22:46:20.271557Z</relative-time> | `cc9fc78` | New commits |
| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime="2026-10-11T04:24:27.529578Z">2026-10-11T04:24:27.529578Z</relative-time> | `f7c229f` | Draft marked ready |
$ gh api repos/mryfmo/dotfiles/issues/318/reactions --jq '.[]|[.user.login,.content,.created_at]|@tsv'
chatgpt-codex-connector[bot]	+1	2026-10-11T22:46:23Z
$ git show origin/main:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sed -n 55p | grep -o "Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py"
Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py
```
