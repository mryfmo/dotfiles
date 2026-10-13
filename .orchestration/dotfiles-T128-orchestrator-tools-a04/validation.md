# Validation: dotfiles-T128-orchestrator-tools-a04

Seat `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `tools/orchestrator-scripts`, PR #336. Work continues from the second update-branch head `0d199475`, with `origin/main` (`d25c3df8`) merged in `3d131215`. The fixes and tests are in `05e3292f`. Every block is verbatim command output, and `mise WARN` sandbox cache lines are filtered out. The a01 and a03 evidence stays as history.

## 1. Task copies and the base

```text
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a04.md .orchestration/dotfiles-T128-orchestrator-tools-a0{4,3,1}/task.md
d0a26050132a32ddc8d3b397b31f3a815bdaed1a55867daa4d81551f15e14fd7  <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a04.md
d0a26050132a32ddc8d3b397b31f3a815bdaed1a55867daa4d81551f15e14fd7  .orchestration/dotfiles-T128-orchestrator-tools-a04/task.md
ef3b264693a4d8a91b688b06f46d3fb44ec2e90578ad3a18258b69c29b1fcb34  .orchestration/dotfiles-T128-orchestrator-tools-a03/task.md
91eb1ebe246f76e138ce8f3bf108adff844f5acf303bcfecc2b7bc62eb0130ee  .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md
$ cmp <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a04.md .orchestration/dotfiles-T128-orchestrator-tools-a04/task.md && echo identical
identical
$ git diff --quiet ba4d4762 HEAD -- .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md .orchestration/dotfiles-T128-orchestrator-tools-a03/task.md && echo "a01 and a03 copies unchanged since ba4d4762"
a01 and a03 copies unchanged since ba4d4762
$ git diff --stat ba4d4762 0d199475 -- scripts/orchestrator scripts/regime-counters.sh tests/unit | tail -1; echo "(empty: the update-branch heads carry the accepted code)"
(empty: the update-branch heads carry the accepted code)
$ git log --oneline -3 HEAD
36bd7d31 fix(orchestrator): the a04 fixes for PR #336 threads 4255494133, 4255494139, 4255494137 and the local review
3d131215 Merge remote-tracking branch 'origin/main' into tools/orchestrator-scripts
d25c3df8 chore(orchestration): boundary commit 2026-10-13 (10): plan 016 G′ (T718 a03 → a04 reset, the local-review guard), a02 item 6, M-20261012-33/C-32, records (#345)
$ git merge-base --is-ancestor origin/main HEAD && echo "origin/main ($(git rev-parse --short origin/main)) is merged"
origin/main (d25c3df8) is merged
$ git diff --stat 0d199475 HEAD -- scripts/regime-counters.sh tests/unit/test_regime_counters.py | tail -1; echo "(empty: no counters change under a04)"
(empty: no counters change under a04)
```

## 2. Every closed row of the threat table names a test in this head

```text
$ /usr/bin/grep -c "closed: tests/unit/test_orchestrator_tools.py::" <a04 copy>; for t in $(sed -n "s/.*closed: tests\/unit\/test_orchestrator_tools.py::\([a-z0-9_]*\).*/\1/p" <a04 copy>); do printf "%s " "$t"; /usr/bin/grep -c "def $t(" tests/unit/test_orchestrator_tools.py; done
11
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file 1
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line 1
test_dispatch_refuses_a_line_without_a_task_id 1
test_dispatch_records_the_sent_line_with_its_read_marker 1
test_dispatch_refuses_an_unwritable_record_before_sending 1
test_dispatch_refuses_a_malformed_record_block_before_sending 1
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout 1
test_three_repeat_prints_body_matches_and_states_a_capped_memory_count 1
test_bus_read_ignores_closers_between_other_endpoints 1
test_bus_read_closes_a_task_on_any_non_revise_acceptance 1
test_bus_read_skips_and_counts_malformed_rows 1
```

## 3. Tests, lint and size

```text
$ uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v 2>&1 | sed -E 's/ \(tests\.unit\.test_orchestrator_tools\.OrchestratorToolsTest\.[a-z0-9_]+\)//'   # drops each test's repeated dotted id
test_bus_read_closes_a_task_on_any_non_revise_acceptance ... ok
test_bus_read_ignores_closers_between_other_endpoints ... ok
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_bus_read_skips_and_counts_malformed_rows ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_records_the_sent_line_with_its_read_marker ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_a_line_without_a_task_id ... ok
test_dispatch_refuses_a_malformed_record_block_before_sending ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line ... ok
test_dispatch_refuses_an_unwritable_record_before_sending ... ok
test_dispatch_refuses_malformed_lines ... ok
test_three_repeat_prints_body_matches_and_states_a_capped_memory_count ... ok
test_three_repeat_prints_the_records_search_line ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout ... ok

----------------------------------------------------------------------
Ran 16 tests in 3.711s

OK
$ uv run --no-project python -m unittest tests.unit.test_regime_counters 2>&1 | tail -3
Ran 26 tests in 3.193s

OK
$ shellcheck --version | sed -n 2p; shellcheck -x scripts/orchestrator/*.sh && echo shellcheck-ok
version: 0.11.0
shellcheck-ok
$ (cd "$TMPDIR" && mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d <worktree>/scripts/orchestrator/*.sh) | /usr/bin/grep -v 'mise WARN'; echo shfmt-rc=${pipestatus[1]}
shfmt-rc=0
$ ruff --version; ruff format --check tests/unit/test_orchestrator_tools.py; ruff check tests/unit/test_orchestrator_tools.py
ruff 0.17.0
1 file already formatted
All checks passed!
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-orchestrator-tools-a01/autoskill.md
8	0	.orchestration/dotfiles-T128-orchestrator-tools-a01/learning.md
122	0	.orchestration/dotfiles-T128-orchestrator-tools-a01/report.md
23	0	.orchestration/dotfiles-T128-orchestrator-tools-a01/sandbox.md
104	0	.orchestration/dotfiles-T128-orchestrator-tools-a01/task.md
523	0	.orchestration/dotfiles-T128-orchestrator-tools-a01/validation.md
3	0	.orchestration/dotfiles-T128-orchestrator-tools-a03/autoskill.md
5	0	.orchestration/dotfiles-T128-orchestrator-tools-a03/learning.md
68	0	.orchestration/dotfiles-T128-orchestrator-tools-a03/report.md
4	0	.orchestration/dotfiles-T128-orchestrator-tools-a03/revise.yaml
21	0	.orchestration/dotfiles-T128-orchestrator-tools-a03/sandbox.md
116	0	.orchestration/dotfiles-T128-orchestrator-tools-a03/task.md
400	0	.orchestration/dotfiles-T128-orchestrator-tools-a03/validation.md
3	0	.orchestration/dotfiles-T128-orchestrator-tools-a04/autoskill.md
8	0	.orchestration/dotfiles-T128-orchestrator-tools-a04/learning.md
53	0	.orchestration/dotfiles-T128-orchestrator-tools-a04/report.md
26	0	.orchestration/dotfiles-T128-orchestrator-tools-a04/sandbox.md
130	0	.orchestration/dotfiles-T128-orchestrator-tools-a04/task.md
155	0	.orchestration/dotfiles-T128-orchestrator-tools-a04/validation.md
68	0	scripts/orchestrator/bus-read.sh
216	0	scripts/orchestrator/dispatch.sh
65	0	scripts/orchestrator/three-repeat.sh
29	9	scripts/regime-counters.sh
427	0	tests/unit/test_orchestrator_tools.py
41	1	tests/unit/test_regime_counters.py
$ git diff --numstat origin/main...HEAD -- . ":!.orchestration"
68	0	scripts/orchestrator/bus-read.sh
216	0	scripts/orchestrator/dispatch.sh
65	0	scripts/orchestrator/three-repeat.sh
29	9	scripts/regime-counters.sh
427	0	tests/unit/test_orchestrator_tools.py
41	1	tests/unit/test_regime_counters.py
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^\.orchestration\// {f++} $3 !~ /^\.orchestration\// && $3 !~ /^tests\// {o+=$1} $3 ~ /^tests\// {t+=$1} END {print "files outside .orchestration/:", f, "added outside tests/:", o, "added under tests/:", t}'
files outside .orchestration/: 6 added outside tests/: 378 added under tests/: 468
```

## 4. The full unit discover (in the sandbox)

CI runs `uv run python -m unittest discover -s tests/unit -v`. The same discover in the seat sandbox fails only in modules this task does not touch, each where a test needs what the sandbox denies (the SSH signing key, `mktemp` under `/var/folders`, the herdr socket). CI is the authority for those modules.

```text
$ uv run python -m unittest discover -s tests/unit > "$TMPDIR/discover.txt" 2>&1; tail -3 "$TMPDIR/discover.txt"
Ran 1014 tests in 422.207s

FAILED (failures=114, errors=103, skipped=2)
$ /usr/bin/grep -E "^(FAIL|ERROR): " "$TMPDIR/discover.txt" | sed -E "s/^(FAIL|ERROR): [^ ]+ \(([^.]+\.[^.]+)\..*/\2/" | /usr/bin/grep -v "^ERROR: " | sort | uniq -c | sort -rn
  78 test_herdr_agents.HerdrAgentsTest
  73 test_require_crit_review.ReviewGuardTest
  28 test_agent_stop_gate.AgentStopGateTest
  19 test_ua_symbol_coverage.UaSymbolCoverageTest
   8 test_runtime_health.RuntimeHealthTest
   5 test_gh_auth.GhAuthTest
   4 test_supply_chain_policy.SupplyChainPolicyTest
   2 test_aws_cli_acquisition.AwsCliAcquisitionTest
$ /usr/bin/grep -E "^(FAIL|ERROR): " "$TMPDIR/discover.txt" | /usr/bin/grep -cE "test_orchestrator_tools|test_regime_counters"
0
$ /usr/bin/grep -c "Couldn't load public key" "$TMPDIR/discover.txt"; /usr/bin/grep -c "Operation not permitted" "$TMPDIR/discover.txt"
41
39
```

## 5. Mutation proofs

Each mutant changes one span of the fix, runs the named test, and restores the file with `git checkout --`. The script is in the seat scratchpad; the lines are cut at 260 characters, and the home directory is written `~`.

```text
$ uv run --no-project python <scratchpad>/mutate-a04.py 2>&1 | cut -c1-260 | sed "s|$HOME|~|g"
M1 no writability check: test_dispatch_refuses_an_unwritable_record_before_sending -> FAILED (killed) | AssertionError: 'the record /private/tmp/claude-501/tmp4xoa2zy_/repo/locked/t.md cannot be written' not found in 'dispatch: this send added no bus row; /pri
M2 malformed JSON unnamed: test_dispatch_refuses_a_malformed_record_block_before_sending -> FAILED (killed) | AssertionError: 'the block is not valid JSON' not found in 'Traceback (most recent call last):\n  File "<string>", line 24, in <module>\n    block = j
M3a RESULT/PONG from any endpoints: test_bus_read_ignores_closers_between_other_endpoints -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=1') != ([], 'skipped=1')
M3b ACCEPTANCE from any endpoints: test_bus_read_ignores_closers_between_other_endpoints -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=1') != ([], 'skipped=1')
M4 the old status whitelist: test_bus_read_closes_a_task_on_any_non_revise_acceptance -> FAILED (killed) | AssertionError: Tuples differ: ([('T4', 'w4')], 'skipped=1') != ([('T1', 'w1'), ('T2', 'w2'), ('T3', 'w3'), ('T4', 'w4')], 'skipped=1')
M5a any kind counts: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=8') != ([('T1', 'w1')], 'skipped=7')
M5b no v1 needed: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=8') != ([], 'skipped=7')
M5c repeated task_id counts: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=8') != ([], 'skipped=7')
M5d empty task_id counts: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=8') != ([('T1', 'w1')], 'skipped=7')
M5e repeated status counts: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=8') != ([], 'skipped=7')
M5f unparsable at counts: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=8') != ([], 'skipped=7')
M5g empty lines count: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Lists differ: ['open: none', 'skipped=0'] != ['open: none', 'skipped=1']
M6 no body search: test_three_repeat_prints_body_matches_and_states_a_capped_memory_count -> FAILED (killed) | AssertionError: Lists differ: ['sea[59 chars]-1.md, M-2.md', 'compactiondb: bookkeeping -> [20 chars]ed)'] != ['sea[59 chars]-1.md', 'compactiondb: b
M7 cap never stated: test_three_repeat_prints_body_matches_and_states_a_capped_memory_count -> FAILED (killed) | AssertionError: Lists differ: ['sea[67 chars]-2.md', 'compactiondb: bookkeeping -> >=1000 matches (capped)'] != ['sea[67 chars]-2.md', 'compactiond
M8 no --limit: test_three_repeat_prints_body_matches_and_states_a_capped_memory_count -> FAILED (killed) | AssertionError: Lists differ: ['memory', 'search', '--limit', '1000', '--', 'bookkeeping'] != ['memory', 'search', '--', 'bookkeeping']
survivors: 0
$ git status --short scripts tests; echo "(empty: every mutant restored)"
(empty: every mutant restored)
```

## 6. bus-read.sh on the live team history

```text
$ bash scripts/orchestrator/bus-read.sh dotfiles-conformance
open: task=dotfiles-T128-orchestrator-tools-a04 seat=claude-standard-dot-a003 last_event=2026-10-13T07:59:15Z minutes=32 silent=yes
skipped=45
```

The discover in §4 ran on the tree committed as `77203547`. The two amends that followed (`36bd7d31`, `05e3292f`) change only `tests/unit/test_orchestrator_tools.py`, which §3 runs on the final head.
