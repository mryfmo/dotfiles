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

## 7. CI and the Bot on `5b99a744` (main-checkout copy only)

The push of `5b99a744` was at 2026-10-13T08:38:53Z. Bot review 5500993250 came at 08:46:05Z, inside the 15-minute window of Worker Playbook step 15.

```text
$ gh pr checks 336 --watch --interval 30   # the final listing
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	5s	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/38370693171/job/115206654717	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38370693171/job/115206654648	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38370693171/job/115206654785	
public-bootstrap (macos-14, client)	pass	8m15s	https://github.com/mryfmo/dotfiles/actions/runs/38370693171/job/115206654711	
public-bootstrap (ubuntu-24.04, client)	pass	9m36s	https://github.com/mryfmo/dotfiles/actions/runs/38370693171/job/115206654372	
public-bootstrap (ubuntu-24.04, server)	pass	7m46s	https://github.com/mryfmo/dotfiles/actions/runs/38370693171/job/115206654957	
test (macos-14, client)	pass	6m11s	https://github.com/mryfmo/dotfiles/actions/runs/38370693125/job/115206654481	
test (ubuntu-24.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/38370693125/job/115206653992	
test (ubuntu-24.04, server)	pass	5m33s	https://github.com/mryfmo/dotfiles/actions/runs/38370693125/job/115206654524	
test (ubuntu-26.04, client)	pass	8m42s	https://github.com/mryfmo/dotfiles/actions/runs/38370693125/job/115206654232	
validate	pass	55s	https://github.com/mryfmo/dotfiles/actions/runs/38370693102/job/115206654880	
exit=0
$ the Bot wait (reviews whose commit_id is the head, issue comments after the push, review comments the API lists on the head)
reviews on 5b99a7443b255426569724f15822dfb3e248411c:
5500993250 chatgpt-codex-connector[bot] 2026-10-13T08:46:05Z COMMENTED
issue comments after push:
review comments on 5b99a7443b255426569724f15822dfb3e248411c:
4253994704 .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md:19 chatgpt-codex-connector[bot] **P1  Close the threat row for all three scripts**
4254163604 scripts/orchestrator/dispatch.sh:104 chatgpt-codex-connector[bot] **P1  Require the TASK hash before dispatching**
4254399800 scripts/orchestrator/dispatch.sh:124 chatgpt-codex-connector[bot] **P1  Reject conflicting hash source fields**
4254494989 scripts/orchestrator/dispatch.sh:78 chatgpt-codex-connector[bot] **P1  Reject duplicate file tokens before hashing**
4254494999 .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md:21 chatgpt-codex-connector[bot] **P1  Add a threat row for acceptance-record mutation**
4254893065 scripts/orchestrator/dispatch.sh:65 chatgpt-codex-connector[bot] **P2  Require a task ID on every dispatched message**
4255079204 scripts/regime-counters.sh:132 chatgpt-codex-connector[bot] **P2  Validate ledger rows before trusting the record**
4255272793 scripts/orchestrator/dispatch.sh:179 chatgpt-codex-connector[bot] **P2  Use consistent tokenization for record association**
4255272803 scripts/orchestrator/dispatch.sh:212 chatgpt-codex-connector[bot] **P2  Refuse a capped history before dispatching**
4256541708 tests/unit/test_orchestrator_tools.py:234 chatgpt-codex-connector[bot] **P2  Make the unwritable-directory test independent of root privileges**
4256541716 scripts/orchestrator/dispatch.sh:60 chatgpt-codex-connector[bot] **P2  Reject NUL bytes instead of silently deleting them**
4256541723 scripts/orchestrator/bus-read.sh:52 chatgpt-codex-connector[bot] **P2  Restrict bus history rows to documented read markers**
4256541725 scripts/orchestrator/dispatch.sh:126 chatgpt-codex-connector[bot] **P2  Treat previous hashes as references rather than local artifacts**
2026-10-13T08:47:15Z
```

The API lists every thread still on a line of the head; the six from 4253994704 to 4254893065 and 4255079204 are a01 and a03 threads, dispositioned in their reports and the a03 acceptance record. 4255272793 and 4255272803 (review 5499448264 on `e16c5219`) belong to `dotfiles-T128-orchestrator-tools-a02` item 4 (`.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:121` on main). Review 5500993250's four new threads are all P2:

| Thread | Finding | Worker's reading |
|---|---|---|
| 4256541708 (`test_orchestrator_tools.py:234`) | as UID 0, `chmod 0o555` does not deny the write, so the unwritable-record test fails under root | Valid. CI runs unprivileged and passed. A deterministic denial, or a skip of the locked case under UID 0, would make the test root-independent. |
| 4256541716 (`dispatch.sh:60`) | bash command substitution drops a NUL byte with a warning, so the sent line differs from the file | Valid. The fix: refuse a file holding a NUL before reading it (for example, compare `tr -d '\0' < file` with the file). |
| 4256541723 (`bus-read.sh:52`) | the row regex takes any first token, though the grammar allows only `●` or `○` | Valid against item 1's grammar table. The fix: match `[●○]` (the same in `dispatch.sh`'s recorder regex). |
| 4256541725 (`dispatch.sh:126`) | a `previous_design_sha256=` reference names no file and is refused | Valid. Seven design-review TASK lines on the bus carry `previous_design_sha256=` (`history.sh dotfiles-conformance "" 100000 \| grep 'previous_[a-z_]*sha256='`). The fix: check `previous_*_sha256` as 64 hex and do not recompute it. |

None is P0 or P1. Under the task's Completion the orchestrator returns its local review with the Bot's findings in a04's one revise round, so no fix is pushed before that round.

## 8. Revise round 1 (ACCEPTANCE `status=revise` of 2026-10-13T08:56:02Z on `5b99a744`)

The fixes are in `e2e67de8`. Mutants M1 to M8 are rerun on the new head; M1r, R1 to R5 are new. M1r removes the record check and skips the read-only directory case as a root run would.

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
Ran 16 tests in 4.365s

OK
$ uv run --no-project python -m unittest tests.unit.test_regime_counters 2>&1 | tail -3
Ran 26 tests in 3.187s

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
$ uv run --no-project python <scratchpad>/mutate-a04.py 2>&1 | cut -c1-260 | sed "s|$HOME|~|g"
M1 no writability check: test_dispatch_refuses_an_unwritable_record_before_sending -> FAILED (killed) | AssertionError: 'the record /private/tmp/claude-501/tmp2zh7ocka/repo/.orchestration/acceptance/absent.md cannot be written' not found in 'Traceback (most re
M2 malformed JSON unnamed: test_dispatch_refuses_a_malformed_record_block_before_sending -> FAILED (killed) | AssertionError: 'the block is not valid JSON' not found in 'Traceback (most recent call last):\n  File "<string>", line 24, in <module>\n    block = j
M3a RESULT/PONG from any endpoints: test_bus_read_ignores_closers_between_other_endpoints -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=1') != ([], 'skipped=1')
M3b ACCEPTANCE from any endpoints: test_bus_read_ignores_closers_between_other_endpoints -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=1') != ([], 'skipped=1')
M4 the old status whitelist: test_bus_read_closes_a_task_on_any_non_revise_acceptance -> FAILED (killed) | AssertionError: Tuples differ: ([('T4', 'w4')], 'skipped=1') != ([('T1', 'w1'), ('T2', 'w2'), ('T3', 'w3'), ('T4', 'w4')], 'skipped=1')
M5a any kind counts: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=9') != ([('T1', 'w1')], 'skipped=8')
M5b no v1 needed: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=9') != ([], 'skipped=8')
M5c repeated task_id counts: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=9') != ([], 'skipped=8')
M5d empty task_id counts: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=9') != ([('T1', 'w1')], 'skipped=8')
M5e repeated status counts: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=9') != ([], 'skipped=8')
M5f unparsable at counts: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=9') != ([], 'skipped=8')
M5g empty lines count: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Lists differ: ['open: none', 'skipped=0'] != ['open: none', 'skipped=1']
M6 no body search: test_three_repeat_prints_body_matches_and_states_a_capped_memory_count -> FAILED (killed) | AssertionError: Lists differ: ['sea[59 chars]-1.md, M-2.md', 'compactiondb: bookkeeping -> [20 chars]ed)'] != ['sea[59 chars]-1.md', 'compactiondb: b
M7 cap never stated: test_three_repeat_prints_body_matches_and_states_a_capped_memory_count -> FAILED (killed) | AssertionError: Lists differ: ['sea[67 chars]-2.md', 'compactiondb: bookkeeping -> >=1000 matches (capped)'] != ['sea[67 chars]-2.md', 'compactiond
M8 no --limit: test_three_repeat_prints_body_matches_and_states_a_capped_memory_count -> FAILED (killed) | AssertionError: Lists differ: ['memory', 'search', '--limit', '1000', '--', 'bookkeeping'] != ['memory', 'search', '--', 'bookkeeping']
M1r no writability check, run as root: test_dispatch_refuses_an_unwritable_record_before_sending -> FAILED (killed) | AssertionError: 'the record /private/tmp/claude-501/tmp0h_4pk9k/repo/.orchestration/acceptance/absent.md cannot be written' not found in 'Trac
R1 revise opens between any endpoints: test_bus_read_ignores_closers_between_other_endpoints -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=1') != ([('T1', 'w1'), ('T3', 'w3')], 'skipped=1')
R2 no NUL check: test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line -> FAILED (killed) | AssertionError: 0 != 2 : 
R3 any marker: test_bus_read_skips_and_counts_malformed_rows -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=9') != ([], 'skipped=8')
R4 previous_ recomputed: test_dispatch_passes_the_line_byte_identical -> FAILED (killed) | AssertionError: 1 != 0 : dispatch: previous_design_sha256 has no previous_design_file= or previous_design= field naming its file
R5 previous_ hex unchecked: test_dispatch_refuses_malformed_lines -> FAILED (killed) | AssertionError: 0 != 1 : 
survivors: 0
$ git status --short scripts tests; echo "(empty: every mutant restored)"
(empty: every mutant restored)
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
181	0	.orchestration/dotfiles-T128-orchestrator-tools-a04/validation.md
72	0	scripts/orchestrator/bus-read.sh
227	0	scripts/orchestrator/dispatch.sh
65	0	scripts/orchestrator/three-repeat.sh
29	9	scripts/regime-counters.sh
444	0	tests/unit/test_orchestrator_tools.py
41	1	tests/unit/test_regime_counters.py
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^\.orchestration\// {f++} $3 !~ /^\.orchestration\// && $3 !~ /^tests\// {o+=$1} $3 ~ /^tests\// {t+=$1} END {print "files outside .orchestration/:", f, "added outside tests/:", o, "added under tests/:", t}'
files outside .orchestration/: 6 added outside tests/: 393 added under tests/: 485
$ bash scripts/orchestrator/bus-read.sh dotfiles-conformance
open: task=dotfiles-T128-orchestrator-tools-a04 seat=claude-standard-dot-a003 last_event=2026-10-13T08:56:02Z minutes=7 silent=no
skipped=45
```

The full `tests/unit` discover is not rerun in this round: the fix commit changes only `scripts/orchestrator/` and `tests/unit/test_orchestrator_tools.py`, which the runs above cover, and CI runs the discover on the pushed head.

## 9. CI and the Bot on `3e5cad37` (main-checkout copy only)

The revise push of `3e5cad37` was at 2026-10-13T09:25:33Z. Bot review 5501536934 came at 09:32:57Z, inside the 15-minute window.

```text
$ gh pr checks 336 --watch --interval 30   # the final listing
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	2s	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38376219066/job/115225138927	
private-bootstrap (ubuntu-24.04, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38376219066/job/115225138716	
private-bootstrap (ubuntu-24.04, server)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38376219066/job/115225139139	
public-bootstrap (macos-14, client)	pass	9m31s	https://github.com/mryfmo/dotfiles/actions/runs/38376219066/job/115225138900	
public-bootstrap (ubuntu-24.04, client)	pass	8m14s	https://github.com/mryfmo/dotfiles/actions/runs/38376219066/job/115225138863	
public-bootstrap (ubuntu-24.04, server)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/38376219066/job/115225138843	
test (macos-14, client)	pass	6m57s	https://github.com/mryfmo/dotfiles/actions/runs/38376218983/job/115225138378	
test (ubuntu-24.04, client)	pass	8m33s	https://github.com/mryfmo/dotfiles/actions/runs/38376218983/job/115225138615	
test (ubuntu-24.04, server)	pass	5m22s	https://github.com/mryfmo/dotfiles/actions/runs/38376218983/job/115225138676	
test (ubuntu-26.04, client)	pass	8m54s	https://github.com/mryfmo/dotfiles/actions/runs/38376218983/job/115225138506	
validate	pass	1m41s	https://github.com/mryfmo/dotfiles/actions/runs/38376219048/job/115225138752	
exit=0
$ the Bot wait (reviews whose commit_id is the head, issue comments and review comments created after the push)
reviews on 3e5cad37118dfed6836eb3b1e52541198b43b7d7:
5501536934 chatgpt-codex-connector[bot] 2026-10-13T09:32:57Z COMMENTED
issue comments after push:
review comments created after the push:
=== 4256987062 review=5501536934 scripts/orchestrator/bus-read.sh:55 2026-10-13T09:32:57Z
**P2  Count capped history rows before filtering malformed entries**

When `history.sh` returns `BUS_READ_LIMIT` bus entries but one entry fails the outer row-shape regex, `$all` excludes that entry before this check, so the script accepts a truncated newest-only window as complete. An older opener or closer can consequently be omitted while `bus-read.sh` reports an incorrect task state; determine whether the history reached its limit before filtering malformed rows. The a04 threat table has no control covering this interaction between the skip path and the completeness check.

AGENTS.md reference: [AGENTS.md:L77-L78](<head>/AGENTS.md#L77-L78)


=== 4256987076 review=5501536934 scripts/orchestrator/bus-read.sh:69 2026-10-13T09:32:57Z
**P2  Base the silence clock on events from the assigned seat**

When a syntactically valid row for the same `task_id` is later sent between unrelated endpoints, this unfiltered `max_by(.i)` treats it as the task's latest event even though the preceding state machine correctly ignores those endpoints for opening and closing. For example, a recent `w9 → w8` PONG makes an hour-silent `w1` task report `silent=no`, suppressing the required PING; select the latest relevant event from the assigned seat rather than every row sharing the task ID. The peer-bound threat-table test checks only open/closed state and does not exercise the silence timestamp.

AGENTS.md reference: [AGENTS.md:L77-L78](<head>/AGENTS.md#L77-L78)


=== 4256987087 review=5501536934 scripts/orchestrator/dispatch.sh:171 2026-10-13T09:32:57Z
**P2  Preserve record line endings during atomic rewrite**

When an acceptance record uses CRLF line endings, `Path.read_text()` performs universal-newline translation, so `rest` no longer contains the original bytes and the subsequent replacement rewrites all prose with LF endings. This contradicts the byte-for-byte preservation guarantee and can create unrelated acceptance-record changes after every dispatch; read and write the record with newline translation disabled (or preserve the prose as bytes). The closed acceptance-record threat row's test uses only LF input, so it does not verify its claimed prose-preservation control.

AGENTS.md reference: [AGENTS.md:L77-L78](<head>/AGENTS.md#L77-L78)


2026-10-13T09:33:53Z
```

All three threads are P2, none P0 or P1:

| Thread | Finding | Worker's reading |
|---|---|---|
| 4256987062 (`bus-read.sh:55`) | the limit check counts rows after the shape filter, so a full read with one malformed row passes as complete | Valid. The check has counted shape-matching rows since a01. The fix: compare the limit with history.sh's own line count, or all non-empty lines, before the filter. |
| 4256987076 (`bus-read.sh:69`) | `last_event` is the task's latest row between any endpoints, so a third member's row resets the silence clock | Valid. The fix: take `last_event` from the rows between the opener's two endpoints. |
| 4256987087 (`dispatch.sh:171`) | `read_text()` translates CRLF, so a CRLF record's prose is rewritten with LF | Valid. The fix: read and write the record with `newline=""`, or as bytes. |

The revise ACCEPTANCE made this the only revise round (INV-6) and gave residual P2s of the new head to a02 item 6. So each is `not-applicable: owned by dotfiles-T128-orchestrator-tools-a02 item 6`, a row of a04's acceptance ledger.
