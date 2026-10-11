# Validation: dotfiles-T128-regime-counters-a01

Verbatim output of every validation command run. Final head `72764f05ea0091b9e41203829cf9ff8e0e759924` (Amendment 1 round), PR #319. Commands that call `gh` ran outside the sandbox; everything else ran sandboxed. The first RESULT's evidence (head `324652e0`) is kept in the last section.

## Lint, live counters, the Stop-hook budget, make check-regime-boundary, PR and CI (final head)

`make check-regime-boundary` exits 1 (make prints `Error 1`, shell rc 2). Besides the Stop-list lines (untracked main-checkout evidence, seated workers), its INV-6 lines are T120's amendments, both T124 waivers and V0's Bot heads; the other historical tasks are now anchored by the orchestrator's `pr=` lines.

```text
$ git rev-parse HEAD; git status --short
72764f05ea0091b9e41203829cf9ff8e0e759924
$ git log --oneline origin/main..HEAD
72764f05 fix(regime): count only the Codex Bot's badged comments
33d8307b feat(regime): silence a PR-less task only on a pr=none record
f372d4ba chore(orchestration): recommit the dotfiles-T128-regime-counters-a01 task at Amendment 1
324652e0 fix(regime): bind a reset's hash to its redesign task file and always report waivers
e2dd97dc style(regime): format regime-counters.sh with the CI shfmt flags
ff41da6e fix(regime): count only plain task ids and keep the id list on its own stdin
9819ec3e test(regime): cover the INV-6 counters and the boundary probe
0749a556 feat(regime): count INV-6 signals from history and GitHub
f56f46a0 chore(orchestration): record the dotfiles-T128-regime-counters-a01 task
$ shellcheck -x scripts/regime-counters.sh scripts/check-regime-boundary.sh; echo "rc=$?"
rc=0
$ shfmt -i 4 -sr -d scripts/regime-counters.sh scripts/check-regime-boundary.sh; echo "rc=$?"
rc=0
$ ruff format --config ruff.toml --check tests/unit/test_regime_counters.py tests/unit/test_check_regime_boundary.py; ruff check --config ruff.toml tests/unit/test_regime_counters.py tests/unit/test_check_regime_boundary.py
2 files already formatted
All checks passed!
$ wc -l scripts/regime-counters.sh
     149 scripts/regime-counters.sh
$ shasum -a 256 .orchestration/dotfiles-T128-regime-counters-a01/task.md ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-regime-counters-a01.md
d9a44b7eece0871217fb5a7871ad3088a92fd27b3668bc1de88ccf35506151c1  .orchestration/dotfiles-T128-regime-counters-a01/task.md
d9a44b7eece0871217fb5a7871ad3088a92fd27b3668bc1de88ccf35506151c1  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-regime-counters-a01.md
$ scripts/regime-counters.sh dotfiles-T128-v0-main-tests-a01 --pr 317; echo "rc=$?"
task=dotfiles-T128-v0-main-tests-a01 tasks=1 amendments=0 questions=0 results=2 withdrawn=1 revises=1 first_result_head=adcf783b06d9081280991a3727f8a21c3c61ac85 bot_p1_heads_after_result=6 audits=unknown wall=2026-10-11T00:02:55Z..2026-10-11T02:19:04Z (2:16) source=live
S2: bot_p1_heads 6 >= 2 source=live
detail: pr=317 authors=claude-deep-dot tasks=01a12845-0798-7b75-86f8-142e23654880 results=01a128a0-3758-70c7-8817-2d2596525abc,01a128c1-adc0-7e6b-819e-de98f950d0a0 questions=- withdrawn=01a128d4-ad08-7752-83af-a7f578744d3a bot_heads=2602f5750a3c06088c9673d4c8a12595a34d4183,32fe9a36a6ca67670e54bbcb1c506ca391d9dd32,56ca6c6994a4c7199366a01c5ebc05942d01a01a,de138f65e8289da6b3d847a659d432219dd4bac9,e314c502595fadc7c5a9922978e45c5051b9c03a,f6528bbafae9881213de72ad5378968fa81316f4 source=live
rc=0
$ scripts/regime-counters.sh dotfiles-T119-rolling-release-assets-a01; echo "rc=$?"
task=dotfiles-T119-rolling-release-assets-a01 tasks=10 amendments=9 questions=8 results=6 withdrawn=0 revises=5 first_result_head=3cbcf3882d1b9e2a0a222407ce9a46c876dfd426 bot_p1_heads_after_result=4 audits=unknown wall=2026-10-09T21:26:24Z..2026-10-10T08:29:00Z (11:02) source=live
S2: revises 5 >= 2 source=live
S2: amendments 9 >= 2 source=live
S2: questions 8 >= 2 source=live
S2: bot_p1_heads 4 >= 2 source=live
detail: pr=312 authors=claude-deep-dot tasks=01a1228f-6000-723e-8740-4b7e33943470,01a12294-e9f8-76d1-8703-0e36977e674b,01a12298-35b8-7bf1-86cc-906d6e8d19b4,01a12299-d3c8-796e-830e-af65c5eb6fc1,01a1229b-8948-78c3-8caf-7b527ed9592a,01a122a3-d648-7fb9-8355-13b5fb11d9c9,01a122ae-afa0-7ecc-87f4-6bacb6975428,01a122c1-fd08-744b-8ab8-02c58c3aa0bd,01a123e3-0d08-73e6-8584-cd15466b9623,01a124af-dea0-7dd4-8104-cb237786e142 results=01a12307-f330-7ce4-8232-fce12de3a1f7,01a123ae-b698-7115-8854-7ef604245019,01a12423-1790-74a0-8070-dfece3bb6586,01a1248f-75c0-77fc-8b66-e719296beaa8,01a124e3-a870-7867-88f2-a542eee62ae8,01a124ee-00e0-7a5d-8724-1b50f9da5556 questions=01a12294-22c0-7730-8454-2615a72613db,01a12297-66b0-75b5-877f-5348432ef317,01a12299-6a50-7be2-8c28-d29376b01b68,01a1229b-1418-7608-85cd-afe1b867962f,01a122ae-51e0-77d5-86f7-5005af924d7b,01a122c1-8bc0-764e-8b6b-b6fc3a4f31d1,01a123e1-d488-7fff-8a71-b406f87f1f1f,01a124af-36a8-71a5-8bef-36c50f1abb45 withdrawn=- bot_heads=2453b1c95a5ea84e865c6584687845bd97b616b0,50759078d24b83ebbad8228717c3529be488603c,70361875685b2ba1ab110d17ffed1623a332552b,fd4ff82d5afcba9aa13da1708cf99471b46c0071 source=live
rc=0
$ time scripts/regime-counters.sh dotfiles-T119-rolling-release-assets-a01 --history-only > /dev/null
scripts/regime-counters.sh dotfiles-T119-rolling-release-assets-a01  >   0.08s user 0.11s system 51% cpu 0.375 total
$ time make check-regime-boundary; echo "rc=$?"
./scripts/check-regime-boundary.sh
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T124-design-receipt-canonical-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T124-design-review-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-process-rules-a01-design-reset.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-process-rules-a02.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-process-rules-redesign-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-task-review-contracts-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-task-review-phase-a-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-v0-main-tests-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T128-process-rules-a02.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T128-regime-counters-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T128-v0-main-tests-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T128-process-rules-a02.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T128-regime-counters-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T128-v0-main-tests-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/plan-006-s1-v0-main-tests-2026-10-11.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/plans/006-regime-v3-execution.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T128-process-rules-a02.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T128-regime-counters-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T128-v0-main-tests-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T128-process-rules-a02.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T128-regime-counters-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T128-v0-main-tests-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-contract-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-process-rules-a02.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-process-rules-redesign-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-regime-counters-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-task-review-a201-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-task-review-contracts-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-task-review-phase-a-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-v1-task-schema-contract-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-v2-audit-schema-and-runner-contract-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-process-rules-a01-pr-feedback.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-process-rules-a02-audit-27ea99b.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-process-rules-a02-audit-27ea99b.md.last.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-process-rules-a02-crit.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-process-rules-a02-pr-feedback.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-process-rules-a02-review-receipt.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-process-rules-a02.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-process-rules-redesign-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-counters-a01-pr-feedback.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-counters-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round14-codex.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round14-codex.md.transcript.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round14.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15-codex.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15-codex.md.transcript.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16-codex.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16-codex.md.transcript.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md.transcript.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-a02-a01-round2.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-a02-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-a201-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-contracts-a01-round2.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-contracts-a01-round3.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-contracts-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-phase-a-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-v0-main-tests-a01-audit-adcf783.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-v0-main-tests-a01-audit-adcf783.md.last.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-v0-main-tests-a01-crit.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-v0-main-tests-a01-pr-feedback.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-v0-main-tests-a01-review-receipt.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-v0-main-tests-a01.md
regime-boundary: worker still seated at .claude/worktrees/worker-c (herdr-agents --remove-worker .claude/worktrees/worker-c)
regime-boundary: worker still seated at .claude/worktrees/worker-d (herdr-agents --remove-worker .claude/worktrees/worker-d)
regime-boundary: worker still seated at .claude/worktrees/worker-f (herdr-agents --remove-worker .claude/worktrees/worker-f)
regime-boundary: additional worker tab still open in dotfiles: dotfiles-conformance:claude-review-dot-a001 (herdr-agents --remove-worker)
regime-boundary: additional worker tab still open in dotfiles: dotfiles-conformance:claude-standard-dot-a003 (herdr-agents --remove-worker)
regime-boundary: additional worker tab still open in dotfiles: dotfiles-conformance:claude-standard-dot-a004 (herdr-agents --remove-worker)
regime-boundary: dotfiles-T120-npm-provenance-and-claude-channel-a01 S2: amendments 7 >= 2 source=live
regime-boundary: dotfiles-T124-wave1-task-validator-a01 waiver-unanchored
regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 waiver-unanchored
regime-boundary: dotfiles-T128-v0-main-tests-a01 S2: bot_p1_heads 6 >= 2 source=live
make: *** [check-regime-boundary] Error 1
make check-regime-boundary  4.92s user 5.07s system 31% cpu 32.103 total
rc=2
$ gh pr view 319 --json number,url,isDraft,headRefOid,baseRefName
{"baseRefName":"main","headRefOid":"72764f05ea0091b9e41203829cf9ff8e0e759924","isDraft":false,"number":319,"url":"https://github.com/mryfmo/dotfiles/pull/319"}
$ gh pr checks 319
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	1s	https://dashboard.gitguardian.com	
changes	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/38117262271/job/114404531757	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/38117262212/job/114404531650	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38117262212/job/114404531639	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38117262212/job/114404531498	
public-bootstrap (macos-14, client)	pass	8m25s	https://github.com/mryfmo/dotfiles/actions/runs/38117262212/job/114404531759	
public-bootstrap (ubuntu-24.04, client)	pass	8m31s	https://github.com/mryfmo/dotfiles/actions/runs/38117262212/job/114404531624	
public-bootstrap (ubuntu-24.04, server)	pass	7m45s	https://github.com/mryfmo/dotfiles/actions/runs/38117262212/job/114404531655	
test (macos-14, client)	pass	6m13s	https://github.com/mryfmo/dotfiles/actions/runs/38117262271/job/114404559713	
test (ubuntu-24.04, client)	pass	8m20s	https://github.com/mryfmo/dotfiles/actions/runs/38117262271/job/114404559737	
test (ubuntu-24.04, server)	pass	4m44s	https://github.com/mryfmo/dotfiles/actions/runs/38117262271/job/114404559721	
test (ubuntu-26.04, client)	pass	8m35s	https://github.com/mryfmo/dotfiles/actions/runs/38117262271/job/114404559815	
validate	pass	1m14s	https://github.com/mryfmo/dotfiles/actions/runs/38117262226/job/114404531798	
```

## Unit tests named by the task (final head)

```text
$ git rev-parse HEAD
72764f05ea0091b9e41203829cf9ff8e0e759924
$ GIT_CONFIG_GLOBAL=/dev/null uv run python -m unittest -v tests.unit.test_regime_counters tests.unit.test_check_regime_boundary; echo "rc=$?"
test_a_600_row_history_counts_fully_through_the_storage_facade (tests.unit.test_regime_counters.RegimeCountersTest.test_a_600_row_history_counts_fully_through_the_storage_facade) ... ok
test_a_forged_acceptance_record_changes_no_count (tests.unit.test_regime_counters.RegimeCountersTest.test_a_forged_acceptance_record_changes_no_count) ... ok
test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity (tests.unit.test_regime_counters.RegimeCountersTest.test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity) ... ok
test_a_store_at_another_schema_revision_is_unreadable (tests.unit.test_regime_counters.RegimeCountersTest.test_a_store_at_another_schema_revision_is_unreadable) ... ok
test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id) ... ok
test_bot_heads_are_unknown_when_gh_fails (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_when_gh_fails) ... ok
test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit) ... ok
test_bot_heads_are_unknown_without_a_first_result_head (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_without_a_first_result_head) ... ok
test_bot_heads_read_every_page_through_gh_api (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_read_every_page_through_gh_api) ... ok
test_every_line_names_its_source (tests.unit.test_regime_counters.RegimeCountersTest.test_every_line_names_its_source) ... ok
test_every_result_counts_as_a_revise_whatever_its_status (tests.unit.test_regime_counters.RegimeCountersTest.test_every_result_counts_as_a_revise_whatever_its_status) ... ok
test_history_only_never_calls_gh (tests.unit.test_regime_counters.RegimeCountersTest.test_history_only_never_calls_gh) ... ok
test_list_tasks_prints_each_task_id_once (tests.unit.test_regime_counters.RegimeCountersTest.test_list_tasks_prints_each_task_id_once) ... ok
test_only_p0_and_p1_heads_after_the_first_result_head_count (tests.unit.test_regime_counters.RegimeCountersTest.test_only_p0_and_p1_heads_after_the_first_result_head_count) ... ok
test_s1_candidates_are_bot_title_classes_seen_three_times (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_candidates_are_bot_title_classes_seen_three_times) ... ok
test_t118_fixture_counts_revises_from_results (tests.unit.test_regime_counters.RegimeCountersTest.test_t118_fixture_counts_revises_from_results) ... ok
test_t119_fixture_counts_every_task_after_the_first_as_an_amendment (tests.unit.test_regime_counters.RegimeCountersTest.test_t119_fixture_counts_every_task_after_the_first_as_an_amendment) ... ok
test_t124_wave1_fixture_counts_bot_heads_after_the_first_result_head (tests.unit.test_regime_counters.RegimeCountersTest.test_t124_wave1_fixture_counts_bot_heads_after_the_first_result_head) ... ok
test_the_boundary_check_never_passes_a_test_seam (tests.unit.test_regime_counters.RegimeCountersTest.test_the_boundary_check_never_passes_a_test_seam) ... ok
test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one (tests.unit.test_regime_counters.RegimeCountersTest.test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one) ... ok
test_thresholds_are_inv6_constants (tests.unit.test_regime_counters.RegimeCountersTest.test_thresholds_are_inv6_constants) ... ok
test_usage_errors_exit_2 (tests.unit.test_regime_counters.RegimeCountersTest.test_usage_errors_exit_2) ... ok
test_v0_fixture_counts_bot_heads_after_the_first_result_head (tests.unit.test_regime_counters.RegimeCountersTest.test_v0_fixture_counts_bot_heads_after_the_first_result_head) ... ok
test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record) ... ok
test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr) ... ok
test_a_reset_record_silences_only_when_another_identity_accepted_its_design (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_silences_only_when_another_identity_accepted_its_design) ... ok
test_a_task_over_a_count_is_reported (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_task_over_a_count_is_reported) ... ok
test_a_waiver_line_silences_nothing (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_waiver_line_silences_nothing) ... ok
test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged) ... ok
test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped) ... ok
test_the_probe_skips_without_the_counters_script_or_a_readable_store (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_the_probe_skips_without_the_counters_script_or_a_readable_store) ... ok

----------------------------------------------------------------------
Ran 31 tests in 13.272s

OK
rc=0
$ GIT_CONFIG_GLOBAL=/dev/null uv run python -m unittest tests.unit.test_herdr_agents -k regime_boundary -v; echo "rc=$?"
test_regime_boundary_check_accepts_a_clean_canonical_clone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_accepts_a_clean_canonical_clone) ... ok
test_regime_boundary_check_accepts_an_empty_manifest_worker_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_accepts_an_empty_manifest_worker_worktree) ... ok
test_regime_boundary_check_counts_names_across_runtime_types_at_the_main_seat (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_counts_names_across_runtime_types_at_the_main_seat) ... ok
test_regime_boundary_check_finds_worker_workspaces_from_a_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_finds_worker_workspaces_from_a_worktree) ... ok
test_regime_boundary_check_flags_a_seated_main_checkout_off_main (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_flags_a_seated_main_checkout_off_main) ... ok
test_regime_boundary_check_flags_empty_seats_only (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_flags_empty_seats_only) ... ok
test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout) ... ok
test_regime_boundary_check_leaves_an_unseated_detached_checkout_alone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_leaves_an_unseated_detached_checkout_alone) ... ok
test_regime_boundary_check_reports_a_canonical_clone_that_differs_from_origin_main (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_canonical_clone_that_differs_from_origin_main) ... ok
test_regime_boundary_check_reports_a_staged_only_change_in_the_canonical_clone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_staged_only_change_in_the_canonical_clone) ... ok
test_regime_boundary_check_reports_a_stale_canonical_head_whose_dirty_bytes_match_origin_main (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_stale_canonical_head_whose_dirty_bytes_match_origin_main) ... ok
test_regime_boundary_check_reports_a_stash_in_the_canonical_clone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_stash_in_the_canonical_clone) ... ok
test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace) ... ok
test_regime_boundary_check_scans_every_worktree_for_untracked_evidence (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_scans_every_worktree_for_untracked_evidence) ... ok
test_regime_boundary_check_skips_a_canonical_clone_that_is_the_working_clone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_skips_a_canonical_clone_that_is_the_working_clone) ... ok
test_regime_boundary_check_skips_the_canonical_clone_without_chezmoi (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_skips_the_canonical_clone_without_chezmoi) ... ok

----------------------------------------------------------------------
Ran 16 tests in 16.382s

OK
rc=0
```

## Mutation checks (final head): every closed threat-row rule removed in turn; each named test must fail ("killed"), and the scripts are restored from the index after each

```text
$ /tmp/claude-501/t128/mutations.sh   # each line: mutate.sh <file> <literal> <replacement> <test>
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_a_forged_acceptance_record_changes_no_count
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_silences_only_when_another_identity_accepted_its_design
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_silences_only_when_another_identity_accepted_its_design
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_waiver_line_silences_nothing
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_waiver_line_silences_nothing
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_task_over_a_count_is_reported
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_the_probe_skips_without_the_counters_script_or_a_readable_store
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_a_600_row_history_counts_fully_through_the_storage_facade
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_a_store_at_another_schema_revision_is_unreadable
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_every_result_counts_as_a_revise_whatever_its_status
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_every_result_counts_as_a_revise_whatever_its_status
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_every_result_counts_as_a_revise_whatever_its_status
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_when_gh_fails
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_without_a_first_result_head
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_only_p0_and_p1_heads_after_the_first_result_head_count
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_only_p0_and_p1_heads_after_the_first_result_head_count
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_read_every_page_through_gh_api
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_every_line_names_its_source
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_every_line_names_its_source
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_thresholds_are_inv6_constants
M  scripts/regime-counters.sh
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr
M  scripts/regime-counters.sh
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_only_p0_and_p1_heads_after_the_first_result_head_count
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_s1_candidates_are_bot_title_classes_seen_three_times
M  scripts/regime-counters.sh
```

## Mutation commands

```text
$ cat /tmp/claude-501/t128/mutate.sh
#!/usr/bin/env bash
# usage: mutate.sh <file> <perl-literal-from> <perl-literal-to> <test id>
f=$1 from=$2 to=$3 test=$4
FROM="$from" TO="$to" perl -0pi -e 'my $n = s/\Q$ENV{FROM}\E/$ENV{TO}/g; die "pattern not found\n" unless $n' "$f" || { echo "MUTATION-NOT-APPLIED: $test"; exit 1; }
if uv run python -m unittest "$test" > /dev/null 2>&1; then echo "SURVIVED: $test ($from -> $to)"; else echo "killed: $test"; fi
git checkout -q -- "$f"
$ cat /tmp/claude-501/t128/mutations.sh
#!/usr/bin/env bash
# Every closed threat-row rule, mutated in turn; each line must read "killed".
cd ~/Workspace/dotfiles/.claude/worktrees/worker-c || exit 1
export GIT_CONFIG_GLOBAL=/dev/null
M=/tmp/claude-501/t128/mutate.sh C=scripts/regime-counters.sh B=scripts/check-regime-boundary.sh
T=tests.unit.test_regime_counters.RegimeCountersTest K=tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest
# Row 1
$M $C "rows='def tok(" '[[ ! -f ${root}/.orchestration/acceptance/${task}.md ]] || history="$(grep -v RESULT <<< "${history}")"
'"rows='def tok(" $T.test_a_forged_acceptance_record_changes_no_count
# Row 2 (counters half and boundary)
$M $C '| .from | select(. as $f | any($authors[]; . == $f) | not)]' '| .from]' $T.test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity
$M $C '| .from | select(. as $f | any($authors[]; . == $f) | not)]' '| .from]' $K.test_a_reset_record_silences_only_when_another_identity_accepted_its_design
$M $B 'if [[ -n ${hash} && -n ${redesign} && -f ${design} ]] &&' 'if [[ -n ${hash} ]] || ' $K.test_a_reset_record_silences_only_when_another_identity_accepted_its_design
$M $B 'elif [[ -n ${pr} && -n ${merged_at} && ${record_pr} == "${pr}" ]]; then' 'elif [[ -n ${pr} && ${record_pr} == "${pr}" ]]; then' $K.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged
$M $B 'elif [[ -n ${pr} && -n ${merged_at} && ${record_pr} == "${pr}" ]]; then' 'elif [[ -n ${pr} && -n ${merged_at} && -n ${record_pr} ]]; then' $K.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged
$M $B "if [[ -f \${accepted} ]] && grep -Eiq '^(- )?\*\*decision:\*\* *accepted|^status: *accepted' \"\${accepted}\"; then" 'if [[ -f ${accepted} ]]; then' $K.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged
$M $B 'violations+=("${task} waiver-unanchored")' ':' $K.test_a_waiver_line_silences_nothing
$M $B '        if [[ ${silenced} == false ]] && grep -q' '        grep -qs DESIGN_RESET_WAIVED_BY= "${accepted}" && silenced=true
        if [[ ${silenced} == false ]] && grep -q' $K.test_a_waiver_line_silences_nothing
$M $B 'if [[ ${state} == closed && -z ${merged_at} && ${reset_anchored} == false ]]; then' 'if [[ ${state} == closed && -z ${merged_at} ]]; then' $K.test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record
$M $B '[[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ && -f' '[[ -n ${task} && -f' $K.test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped
$M $B '"${counters}" "${args[@]}" < /dev/null 2>' '"${counters}" "${args[@]}" 2>' $K.test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped
$M $B '[[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ && -f ${main}/.orchestration/tasks/${task}.md ]]' '[[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]]' $K.test_a_task_over_a_count_is_reported
$M $B 'counters="${root}/scripts/regime-counters.sh"' 'counters="~/Workspace/dotfiles/.claude/worktrees/worker-c/scripts/regime-counters.sh"' $K.test_the_probe_skips_without_the_counters_script_or_a_readable_store
# Row 4
$M $C 'storage_history "$1" |' 'storage_history "$1" --limit 20 |' $T.test_a_600_row_history_counts_fully_through_the_storage_facade
$M $C "== \"\${_AGMSG_STORAGE_SCHEMA_REV:-}\" ]] || return 1" '!= x ]] || return 1' $T.test_a_store_at_another_schema_revision_is_unreadable
# Row 5
$M $C 'kind("AGMSG-RESULT") as $results' '[kind("AGMSG-RESULT")[] | select(has("status=blocked") | not)] as $results' $T.test_every_result_counts_as_a_revise_whatever_its_status
$M $C 'select(has("status=withdrawn"))' 'select(has("status=withdrawn") or has("status=parked"))' $T.test_every_result_counts_as_a_revise_whatever_its_status
$M $C '.task = (tok("task_id") // "")' '.task = ([.toks[] | select(startswith("task_id="))][-1] // "" | .[8:])' $T.test_every_result_counts_as_a_revise_whatever_its_status
# Row 6
$M $C 'if $state != "ok" then $state elif' 'if $state == "unknown" then [] elif $state != "ok" then $state elif' $T.test_bot_heads_are_unknown_when_gh_fails
$M $C 'elif $c.head == null then "unknown"' 'elif $c.head == null then []' $T.test_bot_heads_are_unknown_without_a_first_result_head
$M $C 'any($p[]; .original_commit_id as $o | $o == null or (any($shas[]; . == $o) | not))' 'false' $T.test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id
$M $C 'if $i == null or' 'if' $T.test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit
$M $C '$shas[$i + 1:]' '$shas[$i:]' $T.test_only_p0_and_p1_heads_after_the_first_result_head_count
$M $C 'P[01] Badge' 'P[012] Badge' $T.test_only_p0_and_p1_heads_after_the_first_result_head_count
$M $C 'gh api --paginate "repos' 'gh api "repos' $T.test_bot_heads_read_every_page_through_gh_api
# Row 7
$M $C '"S2: \(.[0]) \(.[1]) >= \($limit) source=\($s)"' '"S2: \(.[0]) \(.[1]) >= \($limit)"' $T.test_every_line_names_its_source
$M $C 'source=live
[[ -z ${history_file}${github_file} ]] || source=fixture' 'source=live' $T.test_every_line_names_its_source
# Thresholds (row 9 residual, still pinned)
$M $C 'threshold=2' 'threshold=3' $T.test_thresholds_are_inv6_constants
git status --short scripts
# Amendment 1: PR-less tasks (pr=none)
$M $B 'elif [[ ${record_pr} == none && ${task_pr} == none ]]; then' 'elif [[ ${record_pr} == none ]]; then' $K.test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr
$M $C '[$results[] | tok("pr") | select(.)][0] | if . == null or test("^[0-9]+$") then . else "invalid" end end' '[$results[] | tok("pr") | select(. and test("^[0-9]+$"))][0] end' $K.test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr
$M $C '[$results[] | tok("pr") | select(.)][0] | if . == null or test("^[0-9]+$") then . else "invalid" end end' '[$results[] | tok("pr") | select(. and test("^[0-9]+$"))][0] end' $T.test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one
$M $C 'elif [[ ${pr} =~ ^[0-9]+$ ]] && comments=' 'elif [[ -n ${pr} ]] && comments=' $T.test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one
$M $B '        if [[ -f ${accepted} ]] && grep -Eiq' '        if [[ -f ${accepted} ]] || grep -Eiq' $K.test_a_pr_none_record_silences_only_a_task_whose_results_name_no_pr
git status --short scripts
# Bot round on 33d8307b: only the Codex Bot counts
$M $C 'def codex: .user.login == "chatgpt-codex-connector[bot]";' 'def codex: .user.type == "Bot";' $T.test_only_p0_and_p1_heads_after_the_first_result_head_count
$M $C 'def codex: .user.login == "chatgpt-codex-connector[bot]";' 'def codex: .user.type == "Bot";' $T.test_s1_candidates_are_bot_title_classes_seen_three_times
git status --short scripts
```

## Fixture-derived counts (final head)

```text
$ scripts/regime-counters.sh dotfiles-T118-rolling-tools-single-update-a01 --history-file tests/fixtures/regime-counters/dotfiles-T118-rolling-tools-single-update-a01.tsv --history-only
task=dotfiles-T118-rolling-tools-single-update-a01 tasks=2 amendments=1 questions=0 results=10 withdrawn=0 revises=9 first_result_head=0d21899066569c6d32879f2f4691c4a462e2dcb9 bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-09T10:37:19Z..2026-10-09T20:59:47Z (10:22) source=fixture
S2: revises 9 >= 2 source=fixture
detail: pr=310 authors=claude-deep-dot tasks=01a1203d-1f18-70c6-8a9e-2f3bc926596b,01a12262-9b10-7a3e-8b41-db7936f54014 results=01a120ac-a9c8-7ddd-8ba9-0586ec10f7d2,01a120dd-a0f0-7198-8227-7487e7d62568,01a12111-0148-7c9c-8c4e-7dec5c02688f,01a12179-11e8-7577-8086-6d3574b8c3ce,01a1218f-d9f0-78a6-8612-59590ee7619c,01a121ae-e340-7065-80d5-5cbacaf9d77f,01a121e7-15f8-72c0-84be-255539993d8c,01a1221d-d980-7ca8-830f-fee5d38b6248,01a12255-e140-72a9-88f1-dc5af8c84780,01a12277-01b8-7a95-8573-5becf2400f61 questions=- withdrawn=- bot_heads=- source=fixture
$ scripts/regime-counters.sh dotfiles-T119-rolling-release-assets-a01 --history-file tests/fixtures/regime-counters/dotfiles-T119-rolling-release-assets-a01.tsv --history-only
task=dotfiles-T119-rolling-release-assets-a01 tasks=10 amendments=9 questions=8 results=6 withdrawn=0 revises=5 first_result_head=3cbcf3882d1b9e2a0a222407ce9a46c876dfd426 bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-09T21:26:24Z..2026-10-10T08:29:00Z (11:02) source=fixture
S2: revises 5 >= 2 source=fixture
S2: amendments 9 >= 2 source=fixture
S2: questions 8 >= 2 source=fixture
detail: pr=312 authors=claude-deep-dot tasks=01a1228f-6000-723e-8740-4b7e33943470,01a12294-e9f8-76d1-8703-0e36977e674b,01a12298-35b8-7bf1-86cc-906d6e8d19b4,01a12299-d3c8-796e-830e-af65c5eb6fc1,01a1229b-8948-78c3-8caf-7b527ed9592a,01a122a3-d648-7fb9-8355-13b5fb11d9c9,01a122ae-afa0-7ecc-87f4-6bacb6975428,01a122c1-fd08-744b-8ab8-02c58c3aa0bd,01a123e3-0d08-73e6-8584-cd15466b9623,01a124af-dea0-7dd4-8104-cb237786e142 results=01a12307-f330-7ce4-8232-fce12de3a1f7,01a123ae-b698-7115-8854-7ef604245019,01a12423-1790-74a0-8070-dfece3bb6586,01a1248f-75c0-77fc-8b66-e719296beaa8,01a124e3-a870-7867-88f2-a542eee62ae8,01a124ee-00e0-7a5d-8724-1b50f9da5556 questions=01a12294-22c0-7730-8454-2615a72613db,01a12297-66b0-75b5-877f-5348432ef317,01a12299-6a50-7be2-8c28-d29376b01b68,01a1229b-1418-7608-85cd-afe1b867962f,01a122ae-51e0-77d5-86f7-5005af924d7b,01a122c1-8bc0-764e-8b6b-b6fc3a4f31d1,01a123e1-d488-7fff-8a71-b406f87f1f1f,01a124af-36a8-71a5-8bef-36c50f1abb45 withdrawn=- bot_heads=- source=fixture
$ scripts/regime-counters.sh dotfiles-T124-wave1-task-validator-a01 --history-file tests/fixtures/regime-counters/dotfiles-T124-wave1-task-validator-a01.tsv --github-file tests/fixtures/regime-counters/pr-313.json
task=dotfiles-T124-wave1-task-validator-a01 tasks=10 amendments=9 questions=6 results=2 withdrawn=0 revises=1 first_result_head=a11e36176f7021df4160efb553a170bd680a5f30 bot_p1_heads_after_result=2 audits=unknown wall=2026-10-10T09:00:29Z..2026-10-10T12:37:16Z (3:36) source=fixture
S2: amendments 9 >= 2 source=fixture
S2: questions 6 >= 2 source=fixture
S2: bot_p1_heads 2 >= 2 source=fixture
detail: pr=313 authors=claude-deep-dot tasks=01a1250a-d3c8-7c32-8c91-c3a3147ae281,01a1250b-8778-7f9c-8efb-71cafba4c54d,01a1250d-bde0-7dd2-8b9b-7fc0f18ef85c,01a12523-1e88-7a7c-86f7-cf67b49e0f39,01a12549-2100-79cd-8f86-a31a9339e1a1,01a12556-6770-7bcb-8f41-eda54eab405f,01a12559-e9e0-78bc-863f-3c8ebd132f60,01a12572-34a0-7a3e-8bda-c958615615ed,01a12590-6b00-7309-8a26-8d151a6ddc99,01a12592-ff28-770c-8522-341cad5f919a results=01a125ab-5988-7913-810e-aeec384ef8b6,01a125d1-4c60-7814-8783-701525ca35d3 questions=01a1250c-6620-7965-8752-db98042724e0,01a12548-03d8-7554-8bad-35b599798ea2,01a12558-e040-795d-89b6-9b65a97844c7,01a12571-7538-72e7-8d1f-c525e8f732a3,01a1258f-da78-7202-8068-4ae0c4971620,01a12592-a550-7038-8e7e-3fd4b6a0a653 withdrawn=- bot_heads=52bb69fc0f2085e290f242e9145f74ba84f2a25c,e6b30e9670569604666730bf1de042b51cf4f2b7 source=fixture
$ scripts/regime-counters.sh dotfiles-T128-v0-main-tests-a01 --history-file tests/fixtures/regime-counters/dotfiles-T128-v0-main-tests-a01.tsv --github-file tests/fixtures/regime-counters/pr-317.json
task=dotfiles-T128-v0-main-tests-a01 tasks=1 amendments=0 questions=0 results=2 withdrawn=1 revises=1 first_result_head=adcf783b06d9081280991a3727f8a21c3c61ac85 bot_p1_heads_after_result=6 audits=unknown wall=2026-10-11T00:02:55Z..2026-10-11T02:19:04Z (2:16) source=fixture
S2: bot_p1_heads 6 >= 2 source=fixture
detail: pr=317 authors=claude-deep-dot tasks=01a12845-0798-7b75-86f8-142e23654880 results=01a128a0-3758-70c7-8817-2d2596525abc,01a128c1-adc0-7e6b-819e-de98f950d0a0 questions=- withdrawn=01a128d4-ad08-7752-83af-a7f578744d3a bot_heads=2602f5750a3c06088c9673d4c8a12595a34d4183,32fe9a36a6ca67670e54bbcb1c506ca391d9dd32,56ca6c6994a4c7199366a01c5ebc05942d01a01a,de138f65e8289da6b3d847a659d432219dd4bac9,e314c502595fadc7c5a9922978e45c5051b9c03a,f6528bbafae9881213de72ad5378968fa81316f4 source=fixture
```

## CompactionDB memory add for the Amendment 1 round (main checkout, outside the sandbox)

```text
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T128 A3 Amendment 1 (PR 319 head 72764f05, 2026-10-11): check-regime-boundary.sh silences a PR-less task (review, design, redesign) only on an accepted acceptance record with a pr=none line and only when none of the task's RESULTs carries a pr= token; regime-counters.sh prints detail: pr=<digits>, pr=none (no RESULT carries pr=) or pr=invalid (any other value, so a RESULT saying pr=none makes the record a forgery) and fetches GitHub only for digits. Bot heads and S1 classes count only the Codex Bot login chatgpt-codex-connector[bot], not any GitHub App." 2>&1 | tail -2
6dda48a5-20ce-47b1-abef-01b8cabe5bf8
```

## Bot wait and threads, Amendment 1 round (Worker Playbook step 15)

```text
$ /tmp/claude-501/t128/wait.sh 319 33d8307bea3bcb486711d8a6ade31f9394e9d5fa
checks_rc=0
bot_review:
5482116532	33d8307bea3bcb486711d8a6ade31f9394e9d5fa	2026-10-11T06:03:56Z	COMMENTED
bot_comments:
4240473132	33d8307bea3bcb486711d8a6ade31f9394e9d5fa	scripts/regime-counters.sh	**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Restrict counted reviews to the Codex bot**
2026-10-11T06:08:45Z

$ /tmp/claude-501/t128/wait.sh 319 72764f05ea0091b9e41203829cf9ff8e0e759924
checks_rc=0
bot: none (15 min)
2026-10-11T06:36:14Z

$ gh api --paginate repos/{owner}/{repo}/pulls/319/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at,.state]|@tsv'
ff41da6eb87e416bbd128f14797740339bfcf87b	2026-10-11T05:07:46Z	COMMENTED
33d8307bea3bcb486711d8a6ade31f9394e9d5fa	2026-10-11T06:03:56Z	COMMENTED
$ gh api --paginate repos/{owner}/{repo}/pulls/319/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.user.login,.original_commit_id,.path,(.line|tostring),(.body|split("
")[0])]|@tsv'
4240344209	chatgpt-codex-connector[bot]	ff41da6eb87e416bbd128f14797740339bfcf87b	scripts/regime-counters.sh	118	**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Bind reset approval to the named redesign task**
4240344212	chatgpt-codex-connector[bot]	ff41da6eb87e416bbd128f14797740339bfcf87b	scripts/check-regime-boundary.sh	null	**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Report unanchored waivers outside the S2 branch**
4240344214	chatgpt-codex-connector[bot]	ff41da6eb87e416bbd128f14797740339bfcf87b	.orchestration/dotfiles-T128-regime-counters-a01/task.md	null	**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Correct the T119 amendment baseline**
4240344216	chatgpt-codex-connector[bot]	ff41da6eb87e416bbd128f14797740339bfcf87b	.orchestration/dotfiles-T128-regime-counters-a01/task.md	17	**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Persist the commit ID required by the invariant**
4240473132	chatgpt-codex-connector[bot]	33d8307bea3bcb486711d8a6ade31f9394e9d5fa	scripts/regime-counters.sh	null	**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Restrict counted reviews to the Codex bot**
$ gh api repos/{owner}/{repo}/issues/319/reactions --jq '.[]|[.user.login,.content,.created_at]|@tsv'
chatgpt-codex-connector[bot]	+1	2026-10-11T06:14:11Z
$ git log --format="%h %cI %s" origin/main..HEAD
72764f05 2026-10-11T15:11:34+09:00 fix(regime): count only the Codex Bot's badged comments
33d8307b 2026-10-11T14:58:31+09:00 feat(regime): silence a PR-less task only on a pr=none record
f372d4ba 2026-10-11T14:58:31+09:00 chore(orchestration): recommit the dotfiles-T128-regime-counters-a01 task at Amendment 1
324652e0 2026-10-11T14:10:17+09:00 fix(regime): bind a reset's hash to its redesign task file and always report waivers
e2dd97dc 2026-10-11T14:07:12+09:00 style(regime): format regime-counters.sh with the CI shfmt flags
ff41da6e 2026-10-11T13:58:44+09:00 fix(regime): count only plain task ids and keep the id list on its own stdin
9819ec3e 2026-10-11T13:57:04+09:00 test(regime): cover the INV-6 counters and the boundary probe
0749a556 2026-10-11T13:34:12+09:00 feat(regime): count INV-6 signals from history and GitHub
f56f46a0 2026-10-11T13:25:59+09:00 chore(orchestration): record the dotfiles-T128-regime-counters-a01 task
```

## Round 1 evidence (first RESULT, head 324652e0), kept verbatim

### Round 1 validation: dotfiles-T128-regime-counters-a01

Verbatim output of every validation command run. Final head `324652e0f8181248982fb0e88a2cd329e73e5144`, PR #319. Commands that call `gh` ran outside the sandbox; everything else ran sandboxed.

### Lint, live counters, the Stop-hook budget, make check-regime-boundary, PR and CI (final head)

`make check-regime-boundary` exits 1 (make prints `Error 1`, shell rc 2): besides the pre-existing Stop-list lines (untracked main-checkout evidence, seated workers), it lists the historical tasks over an INV-6 count, since no existing record carries an anchor yet (report, "Consequences").

```text
$ git rev-parse HEAD; git status --short
324652e0f8181248982fb0e88a2cd329e73e5144
$ git log --oneline origin/main..HEAD
324652e0 fix(regime): bind a reset's hash to its redesign task file and always report waivers
e2dd97dc style(regime): format regime-counters.sh with the CI shfmt flags
ff41da6e fix(regime): count only plain task ids and keep the id list on its own stdin
9819ec3e test(regime): cover the INV-6 counters and the boundary probe
0749a556 feat(regime): count INV-6 signals from history and GitHub
f56f46a0 chore(orchestration): record the dotfiles-T128-regime-counters-a01 task
$ shellcheck -x scripts/regime-counters.sh scripts/check-regime-boundary.sh; echo "rc=$?"
rc=0
$ shfmt -i 4 -sr -d scripts/regime-counters.sh scripts/check-regime-boundary.sh; echo "rc=$?"
rc=0
$ ruff format --config ruff.toml --check tests/unit/test_regime_counters.py tests/unit/test_check_regime_boundary.py; ruff check --config ruff.toml tests/unit/test_regime_counters.py tests/unit/test_check_regime_boundary.py
2 files already formatted
All checks passed!
$ wc -l scripts/regime-counters.sh
     148 scripts/regime-counters.sh
$ shasum -a 256 .orchestration/dotfiles-T128-regime-counters-a01/task.md ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-regime-counters-a01.md
69fee4958ce69f2940870f1a684f131c39391dda1316e42f610e6dd5ec0dad1c  .orchestration/dotfiles-T128-regime-counters-a01/task.md
69fee4958ce69f2940870f1a684f131c39391dda1316e42f610e6dd5ec0dad1c  ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-regime-counters-a01.md
$ scripts/regime-counters.sh dotfiles-T128-v0-main-tests-a01 --pr 317; echo "rc=$?"
task=dotfiles-T128-v0-main-tests-a01 tasks=1 amendments=0 questions=0 results=2 withdrawn=1 revises=1 first_result_head=adcf783b06d9081280991a3727f8a21c3c61ac85 bot_p1_heads_after_result=6 audits=unknown wall=2026-10-11T00:02:55Z..2026-10-11T02:19:04Z (2:16) source=live
S2: bot_p1_heads 6 >= 2 source=live
detail: pr=317 authors=claude-deep-dot tasks=01a12845-0798-7b75-86f8-142e23654880 results=01a128a0-3758-70c7-8817-2d2596525abc,01a128c1-adc0-7e6b-819e-de98f950d0a0 questions=- withdrawn=01a128d4-ad08-7752-83af-a7f578744d3a bot_heads=2602f5750a3c06088c9673d4c8a12595a34d4183,32fe9a36a6ca67670e54bbcb1c506ca391d9dd32,56ca6c6994a4c7199366a01c5ebc05942d01a01a,de138f65e8289da6b3d847a659d432219dd4bac9,e314c502595fadc7c5a9922978e45c5051b9c03a,f6528bbafae9881213de72ad5378968fa81316f4 source=live
rc=0
$ scripts/regime-counters.sh dotfiles-T119-rolling-release-assets-a01; echo "rc=$?"
task=dotfiles-T119-rolling-release-assets-a01 tasks=10 amendments=9 questions=8 results=6 withdrawn=0 revises=5 first_result_head=3cbcf3882d1b9e2a0a222407ce9a46c876dfd426 bot_p1_heads_after_result=4 audits=unknown wall=2026-10-09T21:26:24Z..2026-10-10T08:29:00Z (11:02) source=live
S2: revises 5 >= 2 source=live
S2: amendments 9 >= 2 source=live
S2: questions 8 >= 2 source=live
S2: bot_p1_heads 4 >= 2 source=live
detail: pr=312 authors=claude-deep-dot tasks=01a1228f-6000-723e-8740-4b7e33943470,01a12294-e9f8-76d1-8703-0e36977e674b,01a12298-35b8-7bf1-86cc-906d6e8d19b4,01a12299-d3c8-796e-830e-af65c5eb6fc1,01a1229b-8948-78c3-8caf-7b527ed9592a,01a122a3-d648-7fb9-8355-13b5fb11d9c9,01a122ae-afa0-7ecc-87f4-6bacb6975428,01a122c1-fd08-744b-8ab8-02c58c3aa0bd,01a123e3-0d08-73e6-8584-cd15466b9623,01a124af-dea0-7dd4-8104-cb237786e142 results=01a12307-f330-7ce4-8232-fce12de3a1f7,01a123ae-b698-7115-8854-7ef604245019,01a12423-1790-74a0-8070-dfece3bb6586,01a1248f-75c0-77fc-8b66-e719296beaa8,01a124e3-a870-7867-88f2-a542eee62ae8,01a124ee-00e0-7a5d-8724-1b50f9da5556 questions=01a12294-22c0-7730-8454-2615a72613db,01a12297-66b0-75b5-877f-5348432ef317,01a12299-6a50-7be2-8c28-d29376b01b68,01a1229b-1418-7608-85cd-afe1b867962f,01a122ae-51e0-77d5-86f7-5005af924d7b,01a122c1-8bc0-764e-8b6b-b6fc3a4f31d1,01a123e1-d488-7fff-8a71-b406f87f1f1f,01a124af-36a8-71a5-8bef-36c50f1abb45 withdrawn=- bot_heads=2453b1c95a5ea84e865c6584687845bd97b616b0,50759078d24b83ebbad8228717c3529be488603c,70361875685b2ba1ab110d17ffed1623a332552b,fd4ff82d5afcba9aa13da1708cf99471b46c0071 source=live
rc=0
$ time scripts/regime-counters.sh dotfiles-T119-rolling-release-assets-a01 --history-only > /dev/null
scripts/regime-counters.sh dotfiles-T119-rolling-release-assets-a01  >   0.08s user 0.12s system 47% cpu 0.406 total
$ time make check-regime-boundary; echo "rc=$?"
./scripts/check-regime-boundary.sh
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-process-rules-a01-design-reset.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-process-rules-redesign-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-task-review-contracts-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-task-review-phase-a-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T128-v0-main-tests-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T128-v0-main-tests-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T128-v0-main-tests-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/plan-006-s1-v0-main-tests-2026-10-11.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/plans/006-regime-v3-execution.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T128-v0-main-tests-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T128-v0-main-tests-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-contract-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-process-rules-a02.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-process-rules-redesign-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-regime-counters-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-task-review-a201-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-task-review-contracts-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-task-review-phase-a-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-v1-task-schema-contract-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T128-v2-audit-schema-and-runner-contract-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-process-rules-a01-pr-feedback.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-process-rules-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-process-rules-redesign-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round14-codex.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round14-codex.md.transcript.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round14.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15-codex.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15-codex.md.transcript.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16-codex.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16-codex.md.transcript.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md.transcript.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-a02-a01-round2.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-a02-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-a201-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-contracts-a01-round2.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-contracts-a01-round3.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-contracts-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-task-review-phase-a-a01.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-v0-main-tests-a01-audit-adcf783.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-v0-main-tests-a01-audit-adcf783.md.last.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-v0-main-tests-a01-crit.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-v0-main-tests-a01-pr-feedback.json
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-v0-main-tests-a01-review-receipt.md
regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T128-v0-main-tests-a01.md
regime-boundary: worker still seated at .claude/worktrees/worker-c (herdr-agents --remove-worker .claude/worktrees/worker-c)
regime-boundary: worker still seated at .claude/worktrees/worker-d (herdr-agents --remove-worker .claude/worktrees/worker-d)
regime-boundary: worker still seated at .claude/worktrees/worker-f (herdr-agents --remove-worker .claude/worktrees/worker-f)
regime-boundary: additional worker tab still open in dotfiles: dotfiles-conformance:claude-review-dot-a001 (herdr-agents --remove-worker)
regime-boundary: additional worker tab still open in dotfiles: dotfiles-conformance:claude-standard-dot-a003 (herdr-agents --remove-worker)
regime-boundary: additional worker tab still open in dotfiles: dotfiles-conformance:claude-standard-dot-a004 (herdr-agents --remove-worker)
regime-boundary: dotfiles-T114-canonical-clone-reconcile-a01 S2: revises 4 >= 2 source=live
regime-boundary: dotfiles-T118-rolling-tools-single-update-a01 S2: revises 9 >= 2 source=live
regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: revises 5 >= 2 source=live
regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: amendments 9 >= 2 source=live
regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: questions 8 >= 2 source=live
regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: bot_p1_heads 4 >= 2 source=live
regime-boundary: dotfiles-T120-npm-provenance-and-claude-channel-a01 S2: amendments 7 >= 2 source=live
regime-boundary: dotfiles-T124-design-receipt-canonical-a01 S2: revises 3 >= 2 source=live
regime-boundary: dotfiles-T124-design-receipt-canonical-a01 S2: amendments 2 >= 2 source=live
regime-boundary: dotfiles-T124-design-review-a01 S2: revises 2 >= 2 source=live
regime-boundary: dotfiles-T124-design-review-a01 S2: amendments 2 >= 2 source=live
regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: amendments 9 >= 2 source=live
regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: questions 6 >= 2 source=live
regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: bot_p1_heads 2 >= 2 source=live
regime-boundary: dotfiles-T124-wave1-task-validator-a01 waiver-unanchored
regime-boundary: dotfiles-T124-wave1-task-validator-a01 PR #313 closed unmerged without an anchored reset record
regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 S2: amendments 9 >= 2 source=live
regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 S2: bot_p1_heads 2 >= 2 source=live
regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 waiver-unanchored
regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 PR #314 closed unmerged without an anchored reset record
regime-boundary: dotfiles-T128-design-review-a01 S2: revises 26 >= 2 source=live
regime-boundary: dotfiles-T128-design-review-a01 S2: amendments 15 >= 2 source=live
regime-boundary: dotfiles-T128-process-rules-a01 S2: bot_p1_heads 3 >= 2 source=live
regime-boundary: dotfiles-T128-task-review-contracts-a01 S2: revises 2 >= 2 source=live
regime-boundary: dotfiles-T128-task-review-contracts-a01 S2: amendments 3 >= 2 source=live
regime-boundary: dotfiles-T128-task-review-v1-v2-a01 S2: revises 17 >= 2 source=live
regime-boundary: dotfiles-T128-task-review-v1-v2-a01 S2: amendments 20 >= 2 source=live
regime-boundary: dotfiles-T128-v0-main-tests-a01 S2: bot_p1_heads 6 >= 2 source=live
make: *** [check-regime-boundary] Error 1
make check-regime-boundary  4.29s user 4.71s system 29% cpu 30.971 total
rc=2
$ gh pr view 319 --json number,url,isDraft,headRefOid,baseRefName
{"baseRefName":"main","headRefOid":"324652e0f8181248982fb0e88a2cd329e73e5144","isDraft":false,"number":319,"url":"https://github.com/mryfmo/dotfiles/pull/319"}
$ gh pr checks 319
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	1s	https://dashboard.gitguardian.com	
changes	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38113932075/job/114394945566	
private-bootstrap (macos-14, client)	pass	12s	https://github.com/mryfmo/dotfiles/actions/runs/38113931931/job/114394945062	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38113931931/job/114394945133	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38113931931/job/114394945117	
public-bootstrap (macos-14, client)	pass	9m38s	https://github.com/mryfmo/dotfiles/actions/runs/38113931931/job/114394945146	
public-bootstrap (ubuntu-24.04, client)	pass	10m6s	https://github.com/mryfmo/dotfiles/actions/runs/38113931931/job/114394945018	
public-bootstrap (ubuntu-24.04, server)	pass	7m29s	https://github.com/mryfmo/dotfiles/actions/runs/38113931931/job/114394945115	
test (macos-14, client)	pass	5m29s	https://github.com/mryfmo/dotfiles/actions/runs/38113932075/job/114394972866	
test (ubuntu-24.04, client)	pass	8m23s	https://github.com/mryfmo/dotfiles/actions/runs/38113932075/job/114394972913	
test (ubuntu-24.04, server)	pass	4m58s	https://github.com/mryfmo/dotfiles/actions/runs/38113932075/job/114394972846	
test (ubuntu-26.04, client)	pass	7m26s	https://github.com/mryfmo/dotfiles/actions/runs/38113932075/job/114394972871	
validate	pass	1m33s	https://github.com/mryfmo/dotfiles/actions/runs/38113931977/job/114394945210	
```

### Unit tests named by the task (final head)

```text
$ git rev-parse HEAD
324652e0f8181248982fb0e88a2cd329e73e5144
$ GIT_CONFIG_GLOBAL=/dev/null uv run python -m unittest -v tests.unit.test_regime_counters tests.unit.test_check_regime_boundary; echo "rc=$?"
test_a_600_row_history_counts_fully_through_the_storage_facade (tests.unit.test_regime_counters.RegimeCountersTest.test_a_600_row_history_counts_fully_through_the_storage_facade) ... ok
test_a_forged_acceptance_record_changes_no_count (tests.unit.test_regime_counters.RegimeCountersTest.test_a_forged_acceptance_record_changes_no_count) ... ok
test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity (tests.unit.test_regime_counters.RegimeCountersTest.test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity) ... ok
test_a_store_at_another_schema_revision_is_unreadable (tests.unit.test_regime_counters.RegimeCountersTest.test_a_store_at_another_schema_revision_is_unreadable) ... ok
test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id) ... ok
test_bot_heads_are_unknown_when_gh_fails (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_when_gh_fails) ... ok
test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit) ... ok
test_bot_heads_are_unknown_without_a_first_result_head (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_without_a_first_result_head) ... ok
test_bot_heads_read_every_page_through_gh_api (tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_read_every_page_through_gh_api) ... ok
test_every_line_names_its_source (tests.unit.test_regime_counters.RegimeCountersTest.test_every_line_names_its_source) ... ok
test_every_result_counts_as_a_revise_whatever_its_status (tests.unit.test_regime_counters.RegimeCountersTest.test_every_result_counts_as_a_revise_whatever_its_status) ... ok
test_history_only_never_calls_gh (tests.unit.test_regime_counters.RegimeCountersTest.test_history_only_never_calls_gh) ... ok
test_list_tasks_prints_each_task_id_once (tests.unit.test_regime_counters.RegimeCountersTest.test_list_tasks_prints_each_task_id_once) ... ok
test_only_p0_and_p1_heads_after_the_first_result_head_count (tests.unit.test_regime_counters.RegimeCountersTest.test_only_p0_and_p1_heads_after_the_first_result_head_count) ... ok
test_s1_candidates_are_bot_title_classes_seen_three_times (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_candidates_are_bot_title_classes_seen_three_times) ... ok
test_t118_fixture_counts_revises_from_results (tests.unit.test_regime_counters.RegimeCountersTest.test_t118_fixture_counts_revises_from_results) ... ok
test_t119_fixture_counts_every_task_after_the_first_as_an_amendment (tests.unit.test_regime_counters.RegimeCountersTest.test_t119_fixture_counts_every_task_after_the_first_as_an_amendment) ... ok
test_t124_wave1_fixture_counts_bot_heads_after_the_first_result_head (tests.unit.test_regime_counters.RegimeCountersTest.test_t124_wave1_fixture_counts_bot_heads_after_the_first_result_head) ... ok
test_the_boundary_check_never_passes_a_test_seam (tests.unit.test_regime_counters.RegimeCountersTest.test_the_boundary_check_never_passes_a_test_seam) ... ok
test_thresholds_are_inv6_constants (tests.unit.test_regime_counters.RegimeCountersTest.test_thresholds_are_inv6_constants) ... ok
test_usage_errors_exit_2 (tests.unit.test_regime_counters.RegimeCountersTest.test_usage_errors_exit_2) ... ok
test_v0_fixture_counts_bot_heads_after_the_first_result_head (tests.unit.test_regime_counters.RegimeCountersTest.test_v0_fixture_counts_bot_heads_after_the_first_result_head) ... ok
test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record) ... ok
test_a_reset_record_silences_only_when_another_identity_accepted_its_design (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_silences_only_when_another_identity_accepted_its_design) ... ok
test_a_task_over_a_count_is_reported (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_task_over_a_count_is_reported) ... ok
test_a_waiver_line_silences_nothing (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_waiver_line_silences_nothing) ... ok
test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged) ... ok
test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped) ... ok
test_the_probe_skips_without_the_counters_script_or_a_readable_store (tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_the_probe_skips_without_the_counters_script_or_a_readable_store) ... ok

----------------------------------------------------------------------
Ran 29 tests in 11.097s

OK
rc=0
$ GIT_CONFIG_GLOBAL=/dev/null uv run python -m unittest tests.unit.test_herdr_agents -k regime_boundary -v; echo "rc=$?"
test_regime_boundary_check_accepts_a_clean_canonical_clone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_accepts_a_clean_canonical_clone) ... ok
test_regime_boundary_check_accepts_an_empty_manifest_worker_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_accepts_an_empty_manifest_worker_worktree) ... ok
test_regime_boundary_check_counts_names_across_runtime_types_at_the_main_seat (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_counts_names_across_runtime_types_at_the_main_seat) ... ok
test_regime_boundary_check_finds_worker_workspaces_from_a_worktree (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_finds_worker_workspaces_from_a_worktree) ... ok
test_regime_boundary_check_flags_a_seated_main_checkout_off_main (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_flags_a_seated_main_checkout_off_main) ... ok
test_regime_boundary_check_flags_empty_seats_only (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_flags_empty_seats_only) ... ok
test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_gives_the_seat_lock_check_the_main_checkout) ... ok
test_regime_boundary_check_leaves_an_unseated_detached_checkout_alone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_leaves_an_unseated_detached_checkout_alone) ... ok
test_regime_boundary_check_reports_a_canonical_clone_that_differs_from_origin_main (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_canonical_clone_that_differs_from_origin_main) ... ok
test_regime_boundary_check_reports_a_staged_only_change_in_the_canonical_clone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_staged_only_change_in_the_canonical_clone) ... ok
test_regime_boundary_check_reports_a_stale_canonical_head_whose_dirty_bytes_match_origin_main (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_stale_canonical_head_whose_dirty_bytes_match_origin_main) ... ok
test_regime_boundary_check_reports_a_stash_in_the_canonical_clone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_a_stash_in_the_canonical_clone) ... ok
test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_reports_an_added_worker_tab_in_the_pair_workspace) ... ok
test_regime_boundary_check_scans_every_worktree_for_untracked_evidence (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_scans_every_worktree_for_untracked_evidence) ... ok
test_regime_boundary_check_skips_a_canonical_clone_that_is_the_working_clone (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_skips_a_canonical_clone_that_is_the_working_clone) ... ok
test_regime_boundary_check_skips_the_canonical_clone_without_chezmoi (tests.unit.test_herdr_agents.HerdrAgentsTest.test_regime_boundary_check_skips_the_canonical_clone_without_chezmoi) ... ok

----------------------------------------------------------------------
Ran 16 tests in 16.778s

OK
rc=0
```

### Full suite and the origin/main baseline (local; CI ran `make unit-test` green on the final head, listed above)

```text
# full suite at 9819ec3e (before ff41da6e, e2dd97dc, 324652e0; CI ran make unit-test green on 324652e0)
$ make unit-test   (sandboxed, global git config)
Ran 953 tests in 399.495s

FAILED (failures=114, errors=103, skipped=2)
make: *** [unit-test] Error 1
$ GIT_CONFIG_GLOBAL=/dev/null make unit-test
Ran 953 tests in 510.916s

FAILED (failures=68, errors=10, skipped=2)
make: *** [unit-test] Error 1
$ grep -E "^(FAIL|ERROR): test" unit2.log | sed -E "s/.*\(([a-z_]+)\..*/\1/" | sort | uniq -c | sort -rn
  31 test_herdr_agents
  28 test_agent_stop_gate
   8 test_runtime_health
   5 test_gh_auth
   4 test_supply_chain_policy
   2 test_aws_cli_acquisition
$ (git worktree add -q --detach $TMPDIR/base-main origin/main; cd $TMPDIR/base-main) GIT_CONFIG_GLOBAL=/dev/null uv run python -m unittest tests.unit.test_herdr_agents tests.unit.test_agent_stop_gate tests.unit.test_runtime_health tests.unit.test_gh_auth tests.unit.test_supply_chain_policy tests.unit.test_aws_cli_acquisition   (origin/main b896d9bc)
Ran 335 tests in 326.050s

FAILED (failures=68, errors=10, skipped=1)
rc=1
$ comm -3 <(failing test names on origin/main) <(failing test names on the branch)   # empty: the same 78
base=78 branch=78
$ grep -E "^(FAIL|ERROR): test" unit2.log | grep -ci "regime\|boundary\|counters"
0
$ grep -m1 -A6 "^ERROR: test_regime_boundary_check_flags_empty_seats_only" unit.log   (first run: setup fails on git commit signing)
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['git', '-c', 'user.name=t', '-c', 'user.email=t@t', '-C', '/tmp/claude-501/herdr-agents-test-q8c5ghyb/dotfiles', 'commit', '-q', '--allow-empty', '-m', 'c']' returned non-zero exit status 128.
test_attach_in_a_linked_worker_worktree_exits_quietly (test_herdr_agents.HerdrAgentsTest.test_attach_in_a_linked_worker_worktree_exits_quietly) ... error: Couldn't load public key ~/.ssh/id_ed25519.pub: No such file or directory?
```

### Mutation checks (final head): every closed threat-row rule removed in turn; each named test must fail ("killed"), and the scripts are restored from the index after each

```text
$ /tmp/claude-501/t128/mutations.sh   # each line: mutate.sh <file> <literal> <replacement> <test>
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_a_forged_acceptance_record_changes_no_count
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_silences_only_when_another_identity_accepted_its_design
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_reset_record_silences_only_when_another_identity_accepted_its_design
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_waiver_line_silences_nothing
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_waiver_line_silences_nothing
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_a_task_over_a_count_is_reported
killed: tests.unit.test_check_regime_boundary.RegimeBoundaryCountsTest.test_the_probe_skips_without_the_counters_script_or_a_readable_store
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_a_600_row_history_counts_fully_through_the_storage_facade
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_a_store_at_another_schema_revision_is_unreadable
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_every_result_counts_as_a_revise_whatever_its_status
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_every_result_counts_as_a_revise_whatever_its_status
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_every_result_counts_as_a_revise_whatever_its_status
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_when_gh_fails
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_without_a_first_result_head
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_only_p0_and_p1_heads_after_the_first_result_head_count
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_only_p0_and_p1_heads_after_the_first_result_head_count
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_bot_heads_read_every_page_through_gh_api
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_every_line_names_its_source
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_every_line_names_its_source
killed: tests.unit.test_regime_counters.RegimeCountersTest.test_thresholds_are_inv6_constants
```

### Fixture-derived counts (the values the fixture tests assert)

```text
$ scripts/regime-counters.sh dotfiles-T118-rolling-tools-single-update-a01 --history-file tests/fixtures/regime-counters/dotfiles-T118-rolling-tools-single-update-a01.tsv --history-only
task=dotfiles-T118-rolling-tools-single-update-a01 tasks=2 amendments=1 questions=0 results=10 withdrawn=0 revises=9 first_result_head=0d21899066569c6d32879f2f4691c4a462e2dcb9 bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-09T10:37:19Z..2026-10-09T20:59:47Z (10:22) source=fixture
S2: revises 9 >= 2 source=fixture
detail: pr=310 authors=claude-deep-dot tasks=01a1203d-1f18-70c6-8a9e-2f3bc926596b,01a12262-9b10-7a3e-8b41-db7936f54014 results=01a120ac-a9c8-7ddd-8ba9-0586ec10f7d2,01a120dd-a0f0-7198-8227-7487e7d62568,01a12111-0148-7c9c-8c4e-7dec5c02688f,01a12179-11e8-7577-8086-6d3574b8c3ce,01a1218f-d9f0-78a6-8612-59590ee7619c,01a121ae-e340-7065-80d5-5cbacaf9d77f,01a121e7-15f8-72c0-84be-255539993d8c,01a1221d-d980-7ca8-830f-fee5d38b6248,01a12255-e140-72a9-88f1-dc5af8c84780,01a12277-01b8-7a95-8573-5becf2400f61 questions=- withdrawn=- bot_heads=- source=fixture
$ scripts/regime-counters.sh dotfiles-T119-rolling-release-assets-a01 --history-file tests/fixtures/regime-counters/dotfiles-T119-rolling-release-assets-a01.tsv --history-only
task=dotfiles-T119-rolling-release-assets-a01 tasks=10 amendments=9 questions=8 results=6 withdrawn=0 revises=5 first_result_head=3cbcf3882d1b9e2a0a222407ce9a46c876dfd426 bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-09T21:26:24Z..2026-10-10T08:29:00Z (11:02) source=fixture
S2: revises 5 >= 2 source=fixture
S2: amendments 9 >= 2 source=fixture
S2: questions 8 >= 2 source=fixture
detail: pr=312 authors=claude-deep-dot tasks=01a1228f-6000-723e-8740-4b7e33943470,01a12294-e9f8-76d1-8703-0e36977e674b,01a12298-35b8-7bf1-86cc-906d6e8d19b4,01a12299-d3c8-796e-830e-af65c5eb6fc1,01a1229b-8948-78c3-8caf-7b527ed9592a,01a122a3-d648-7fb9-8355-13b5fb11d9c9,01a122ae-afa0-7ecc-87f4-6bacb6975428,01a122c1-fd08-744b-8ab8-02c58c3aa0bd,01a123e3-0d08-73e6-8584-cd15466b9623,01a124af-dea0-7dd4-8104-cb237786e142 results=01a12307-f330-7ce4-8232-fce12de3a1f7,01a123ae-b698-7115-8854-7ef604245019,01a12423-1790-74a0-8070-dfece3bb6586,01a1248f-75c0-77fc-8b66-e719296beaa8,01a124e3-a870-7867-88f2-a542eee62ae8,01a124ee-00e0-7a5d-8724-1b50f9da5556 questions=01a12294-22c0-7730-8454-2615a72613db,01a12297-66b0-75b5-877f-5348432ef317,01a12299-6a50-7be2-8c28-d29376b01b68,01a1229b-1418-7608-85cd-afe1b867962f,01a122ae-51e0-77d5-86f7-5005af924d7b,01a122c1-8bc0-764e-8b6b-b6fc3a4f31d1,01a123e1-d488-7fff-8a71-b406f87f1f1f,01a124af-36a8-71a5-8bef-36c50f1abb45 withdrawn=- bot_heads=- source=fixture
$ scripts/regime-counters.sh dotfiles-T124-wave1-task-validator-a01 --history-file tests/fixtures/regime-counters/dotfiles-T124-wave1-task-validator-a01.tsv --github-file tests/fixtures/regime-counters/pr-313.json
task=dotfiles-T124-wave1-task-validator-a01 tasks=10 amendments=9 questions=6 results=2 withdrawn=0 revises=1 first_result_head=a11e36176f7021df4160efb553a170bd680a5f30 bot_p1_heads_after_result=2 audits=unknown wall=2026-10-10T09:00:29Z..2026-10-10T12:37:16Z (3:36) source=fixture
S2: amendments 9 >= 2 source=fixture
S2: questions 6 >= 2 source=fixture
S2: bot_p1_heads 2 >= 2 source=fixture
detail: pr=313 authors=claude-deep-dot tasks=01a1250a-d3c8-7c32-8c91-c3a3147ae281,01a1250b-8778-7f9c-8efb-71cafba4c54d,01a1250d-bde0-7dd2-8b9b-7fc0f18ef85c,01a12523-1e88-7a7c-86f7-cf67b49e0f39,01a12549-2100-79cd-8f86-a31a9339e1a1,01a12556-6770-7bcb-8f41-eda54eab405f,01a12559-e9e0-78bc-863f-3c8ebd132f60,01a12572-34a0-7a3e-8bda-c958615615ed,01a12590-6b00-7309-8a26-8d151a6ddc99,01a12592-ff28-770c-8522-341cad5f919a results=01a125ab-5988-7913-810e-aeec384ef8b6,01a125d1-4c60-7814-8783-701525ca35d3 questions=01a1250c-6620-7965-8752-db98042724e0,01a12548-03d8-7554-8bad-35b599798ea2,01a12558-e040-795d-89b6-9b65a97844c7,01a12571-7538-72e7-8d1f-c525e8f732a3,01a1258f-da78-7202-8068-4ae0c4971620,01a12592-a550-7038-8e7e-3fd4b6a0a653 withdrawn=- bot_heads=52bb69fc0f2085e290f242e9145f74ba84f2a25c,e6b30e9670569604666730bf1de042b51cf4f2b7 source=fixture
$ scripts/regime-counters.sh dotfiles-T128-v0-main-tests-a01 --history-file tests/fixtures/regime-counters/dotfiles-T128-v0-main-tests-a01.tsv --github-file tests/fixtures/regime-counters/pr-317.json
task=dotfiles-T128-v0-main-tests-a01 tasks=1 amendments=0 questions=0 results=2 withdrawn=1 revises=1 first_result_head=adcf783b06d9081280991a3727f8a21c3c61ac85 bot_p1_heads_after_result=6 audits=unknown wall=2026-10-11T00:02:55Z..2026-10-11T02:19:04Z (2:16) source=fixture
S2: bot_p1_heads 6 >= 2 source=fixture
detail: pr=317 authors=claude-deep-dot tasks=01a12845-0798-7b75-86f8-142e23654880 results=01a128a0-3758-70c7-8817-2d2596525abc,01a128c1-adc0-7e6b-819e-de98f950d0a0 questions=- withdrawn=01a128d4-ad08-7752-83af-a7f578744d3a bot_heads=2602f5750a3c06088c9673d4c8a12595a34d4183,32fe9a36a6ca67670e54bbcb1c506ca391d9dd32,56ca6c6994a4c7199366a01c5ebc05942d01a01a,de138f65e8289da6b3d847a659d432219dd4bac9,e314c502595fadc7c5a9922978e45c5051b9c03a,f6528bbafae9881213de72ad5378968fa81316f4 source=fixture
$ wc -l tests/fixtures/regime-counters/*
      42 tests/fixtures/regime-counters/dotfiles-T118-rolling-tools-single-update-a01.tsv
      35 tests/fixtures/regime-counters/dotfiles-T119-rolling-release-assets-a01.tsv
      25 tests/fixtures/regime-counters/dotfiles-T124-wave1-task-validator-a01.tsv
       9 tests/fixtures/regime-counters/dotfiles-T128-v0-main-tests-a01.tsv
     678 tests/fixtures/regime-counters/pr-313.json
     249 tests/fixtures/regime-counters/pr-317.json
    1038 total
```

### Premises re-run as written

All three hold: 10 TASKs and 52 top-level comments; the stop gate reads history through `storage_history`; PR 317's seven Bot-reviewed heads are unchanged. `history.sh` printed a placement-guard notice on stderr (it did not record the pane).

```text
$ ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conformance --limit 1000 | grep -c 'AGMSG-TASK v1 task_id=dotfiles-T119-rolling-release-assets-a01'; gh api --paginate repos/mryfmo/dotfiles/pulls/313/comments --jq '[.[]|select(.in_reply_to_id==null)]|length'
agmsg: did not name or record this pane: this seat resolved herdr:~/.config/herdr/herdr.sock:w5:p5, and that pane is already recorded as 01a0fa8d-c088-7bf0-8eb7-1f9171449a35__01a1292b-9708-74e9-8332-8506dc5443ed's. Keeping that seat's name and record. If that seat is gone, drop or despawn it and act again. (#1114 placement guard, kept alongside #1112's label-first resolution.)
10
52
$ grep -n 'storage_history\|read_history\|lib/storage' scripts/agent-stop-gate.sh | head -6   (main checkout)
51:# shortens each wait on a contended store. storage_history runs storage_init, which writes unless
56:# SQLITE_BUSY; only a non-initializing storage_history upstream would close that.
57:read_history() {
60:    source "${scripts}/lib/storage.sh" && agmsg_storage_load || return 1
65:    storage_history "$1" | jq -r '[.from, .to, .body] | @tsv'
71:    read_history "$2"
$ gh api --paginate repos/mryfmo/dotfiles/pulls/317/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id[0:8],.submitted_at]|@tsv'
32fe9a36	2026-10-11T02:37:13Z
56ca6c69	2026-10-11T02:52:38Z
de138f65	2026-10-11T03:03:00Z
f6528bba	2026-10-11T03:10:28Z
98f1d250	2026-10-11T03:24:14Z
2602f575	2026-10-11T03:43:58Z
e314c502	2026-10-11T04:04:13Z
```

### CompactionDB memory add (main checkout, outside the sandbox)

```text
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T128 A3 (PR 319, dotfiles-T128-regime-counters-a01, 2026-10-11): scripts/regime-counters.sh counts INV-6 literally: amendments = AGMSG-TASKs - 1 (a note= re-dispatch counts too: T119 = 9, not 8), revises = AGMSG-RESULTs - 1 whatever the status, Bot heads = distinct original_commit_id of Bot P0/P1 review comments after the FIRST RESULT's head= in PR commit order (V0: after adcf783b = 6), unknown never 0. check-regime-boundary.sh anchors: an accepted acceptance record silences only with a pr=<n> line naming the task's PR merged on GitHub; a reset record only when its design_sha256: equals the sha256 of its redesign_task file and a verdict=accept RESULT for that hash came from an identity other than the task's TASK senders; DESIGN_RESET_WAIVED_BY= is always reported waiver-unanchored. No record on main carried these anchors on 2026-10-11, so make check-regime-boundary lists historical tasks until records are amended." 2>&1 | tail -5
1a2cbd75-7d8b-45dd-ab7a-21710a305caa
```

### Bot wait and threads (Worker Playbook step 15)

```text
$ /tmp/claude-501/t128/wait.sh 319 ff41da6eb87e416bbd128f14797740339bfcf87b   # CI watch, then the step-15 Bot wait
checks_rc=1
bot_review:
5481983748	ff41da6eb87e416bbd128f14797740339bfcf87b	2026-10-11T05:07:46Z	COMMENTED
bot_comments:
4240344209	ff41da6eb87e416bbd128f14797740339bfcf87b	scripts/regime-counters.sh	**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Bind reset approval to the named redesign task**
4240344212	ff41da6eb87e416bbd128f14797740339bfcf87b	scripts/check-regime-boundary.sh	**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Report unanchored waivers outside the S2 branch**
4240344214	ff41da6eb87e416bbd128f14797740339bfcf87b	.orchestration/dotfiles-T128-regime-counters-a01/task.md	**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Correct the T119 amendment baseline**
4240344216	ff41da6eb87e416bbd128f14797740339bfcf87b	.orchestration/dotfiles-T128-regime-counters-a01/task.md	**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Persist the commit ID required by the invariant**
2026-10-11T05:07:50Z

$ /tmp/claude-501/t128/wait.sh 319 324652e0f8181248982fb0e88a2cd329e73e5144
checks_rc=0
bot: none (15 min)
2026-10-11T05:38:20Z

$ gh api --paginate repos/{owner}/{repo}/pulls/319/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at,.state]|@tsv'
ff41da6eb87e416bbd128f14797740339bfcf87b	2026-10-11T05:07:46Z	COMMENTED
$ gh api --paginate repos/{owner}/{repo}/pulls/319/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.original_commit_id,.path,(.line|tostring),(.body|split("
")[0])]|@tsv'
4240344209	ff41da6eb87e416bbd128f14797740339bfcf87b	scripts/regime-counters.sh	117	**<sub><sub>![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)</sub></sub>  Bind reset approval to the named redesign task**
4240344212	ff41da6eb87e416bbd128f14797740339bfcf87b	scripts/check-regime-boundary.sh	null	**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Report unanchored waivers outside the S2 branch**
4240344214	ff41da6eb87e416bbd128f14797740339bfcf87b	.orchestration/dotfiles-T128-regime-counters-a01/task.md	24	**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Correct the T119 amendment baseline**
4240344216	ff41da6eb87e416bbd128f14797740339bfcf87b	.orchestration/dotfiles-T128-regime-counters-a01/task.md	17	**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Persist the commit ID required by the invariant**
$ gh api repos/{owner}/{repo}/issues/319/reactions --jq '.[]|[.user.login,.content,.created_at]|@tsv'
chatgpt-codex-connector[bot]	+1	2026-10-11T05:13:06Z
$ git log --format="%h %cI %s" origin/main..HEAD
324652e0 2026-10-11T14:10:17+09:00 fix(regime): bind a reset's hash to its redesign task file and always report waivers
e2dd97dc 2026-10-11T14:07:12+09:00 style(regime): format regime-counters.sh with the CI shfmt flags
ff41da6e 2026-10-11T13:58:44+09:00 fix(regime): count only plain task ids and keep the id list on its own stdin
9819ec3e 2026-10-11T13:57:04+09:00 test(regime): cover the INV-6 counters and the boundary probe
0749a556 2026-10-11T13:34:12+09:00 feat(regime): count INV-6 signals from history and GitHub
f56f46a0 2026-10-11T13:25:59+09:00 chore(orchestration): record the dotfiles-T128-regime-counters-a01 task
```
