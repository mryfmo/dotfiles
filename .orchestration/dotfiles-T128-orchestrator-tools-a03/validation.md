# Validation: dotfiles-T128-orchestrator-tools-a03

Seat `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `tools/orchestrator-scripts`, PR #336, continued from a01 amendment 1's head `5ec05d8d` (the remote head before this task). The code is unchanged since `5ec05d8d`; a03 adds one threat row whose closing test exists there. Every block is verbatim command output; `mise WARN` sandbox cache lines are filtered out. The a01 evidence (`.orchestration/dotfiles-T128-orchestrator-tools-a01/`, §1 to §14) stays as history.

## 1. Task copies

```text
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a03.md .orchestration/dotfiles-T128-orchestrator-tools-a03/task.md .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md
b7348b8a2c08f1102eb4357249256a0790075c1a9b36de408a598daf86e19952  <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a03.md
b7348b8a2c08f1102eb4357249256a0790075c1a9b36de408a598daf86e19952  .orchestration/dotfiles-T128-orchestrator-tools-a03/task.md
91eb1ebe246f76e138ce8f3bf108adff844f5acf303bcfecc2b7bc62eb0130ee  .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md
$ cmp <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a03.md .orchestration/dotfiles-T128-orchestrator-tools-a03/task.md && echo identical
identical
$ git diff --quiet 2dddff84 HEAD -- .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md && echo "a01 copy unchanged since 2dddff84 (amendment 1)"
a01 copy unchanged since 2dddff84 (amendment 1)
$ git diff --stat 5ec05d8d HEAD -- scripts/ tests/ | tail -1; echo "(empty: no code change since 5ec05d8d)"
(empty: no code change since 5ec05d8d)
```

## 2. Every closed row of the threat table names a test in this head

```text
$ /usr/bin/grep -c 'closed: tests/unit/test_orchestrator_tools.py::' <a03 copy>; for t in $(sed -n 's/.*closed: tests\/unit\/test_orchestrator_tools.py::\([a-z0-9_]*\).*/\1/p' <a03 copy>); do printf '%s ' "$t"; /usr/bin/grep -c "def $t(" tests/unit/test_orchestrator_tools.py; done
5
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file 1
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line 1
test_dispatch_records_the_sent_line_with_its_read_marker 1
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout 1
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event 1
```

## 3. The new row's listed controls, in the code

```text
$ /usr/bin/grep -n -E "object_pairs_hook=refuse|setdefault\(\"dispatch\"|sort_keys=True, indent=2|write_text\(f|history.sh\" \"\$\{team\}\" \"\" 100000|record=\$\{6:-\}" scripts/orchestrator/dispatch.sh
51:team=$1 from=$2 to=$3 pane=$4 file=$5 record=${6:-}
154:    block = json.loads(text[4:end], object_pairs_hook=refuse, parse_constant=constant)
158:entries = block.setdefault("dispatch", [])
171:body = json.dumps(block, sort_keys=True, indent=2, ensure_ascii=False)
172:record.write_text(f"---\n{body}\n---\n{rest}")
176:bus() { "${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" 100000; }
```

## 4. Tests, format and lint

```text
$ uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_records_the_sent_line_with_its_read_marker ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line ... ok
test_dispatch_refuses_malformed_lines ... ok
test_three_repeat_prints_the_records_search_line ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout ... ok

----------------------------------------------------------------------
Ran 9 tests in 2.035s

OK
$ uv run --no-project python -m unittest tests/unit/test_regime_counters.py tests/unit/test_check_regime_boundary.py tests/unit/test_agmsg_orchestration_docs.py 2>&1 | tail -n 3
Ran 77 tests in 17.789s

OK
$ shfmt -i 4 -sr -d scripts/orchestrator/*.sh scripts/regime-counters.sh; echo "shfmt exit $?"
shfmt exit 0
$ shellcheck -x scripts/orchestrator/*.sh scripts/regime-counters.sh; echo "shellcheck exit $?"
shellcheck exit 0
$ ruff format --config ruff.toml --check tests/unit/test_orchestrator_tools.py tests/unit/test_regime_counters.py
2 files already formatted
```

## 5. Each guard fails its test when broken

`mutate-am1.py` (session scratch) rewrites one span per mutant, runs the named test, and restores the file with `git checkout --`. D6 to D9, D12 and D13 break the record path the new row closes.

```text
$ uv run --no-project python "$TMPDIR/mutate-am1.py" "$PWD"; git status --short
mutant D1 mismatch check off: test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file -> rc=1 FAILED (failures=1)
mutant D2 line word-split: test_dispatch_passes_the_line_byte_identical -> rc=1 FAILED (failures=1)
mutant D3 multi-line check off: test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line -> rc=1 FAILED (failures=2)
mutant D4 the $( ) read put back: test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line -> rc=1 FAILED (failures=1)
mutant D5 TASK binding check off: test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line -> rc=1 FAILED (failures=4)
mutant D6 record not checked before the send: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D7 read marker inverted: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D8 prose dropped: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D9 duplicate keys accepted: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D10 caller root: test_dispatch_passes_the_line_byte_identical -> rc=1 FAILED (failures=1)
mutant D11 doubly named file accepted: test_dispatch_refuses_malformed_lines -> rc=1 FAILED (failures=1)
mutant D12 history read with the agent: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D13 no before-count: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D14 repeated keys accepted: test_dispatch_refuses_malformed_lines -> rc=1 FAILED (failures=1)
mutant T1 slug check loosened: test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout -> rc=1 FAILED (failures=2)
mutant T2 records match unanchored: test_three_repeat_prints_the_records_search_line -> rc=1 FAILED (failures=1)
mutant T3 class not one argument: test_three_repeat_prints_the_records_search_line -> rc=1 FAILED (failures=1)
mutant T4 caller root: test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout -> rc=1 FAILED (failures=1)
mutant T5 relative CLI path: test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout -> rc=1 FAILED (failures=1)
mutant B1 revise does not reopen: test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event -> rc=1 FAILED (failures=1)
mutant B2 withdrawn does not close: test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event -> rc=1 FAILED (failures=1)
mutant B3 silence at sixty minutes: test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event -> rc=1 FAILED (failures=1)
mutant B4 limit guard off: test_bus_read_refuses_a_read_that_reaches_its_limit -> rc=1 FAILED (failures=1)
mutant B5 the --limit flag form: test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event -> rc=1 FAILED (failures=1)
mutant R1 record mode off: test_s1_reads_the_ledger_classes_of_the_acceptance_record -> rc=1 FAILED (failures=1)
mutant R2 title not JSON-quoted: test_s1_quotes_a_title_with_shell_metacharacters -> rc=1 FAILED (failures=1)
mutant R3 slug check off: test_s1_reads_the_ledger_classes_of_the_acceptance_record -> rc=1 FAILED (failures=1)
```

## 6. Size, CompactionDB, commits

```text
$ git diff --numstat origin/main...HEAD -- . ":!.orchestration"
57	0	scripts/orchestrator/bus-read.sh
181	0	scripts/orchestrator/dispatch.sh
44	0	scripts/orchestrator/three-repeat.sh
29	9	scripts/regime-counters.sh
284	0	tests/unit/test_orchestrator_tools.py
32	1	tests/unit/test_regime_counters.py
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] dotfiles-T128-orchestrator-tools-a03 (INV-6 reset of a01 after thread 4254494999): ..."   # main checkout, permission gate
7a16273b-e91b-450e-abcd-de070e344d08
$ git log --oneline 5ec05d8d..HEAD
a3b71527 chore(orchestration): record the dotfiles-T128-orchestrator-tools-a03 task
```

## 7. Fix round 1: the Bot on `58ecd753`

Bot review 5498865497 of `58ecd753` (04:36:01Z): one P1 and two P2s.

```text
$ gh api --paginate …/pulls/336/comments --jq '.[]|select(.in_reply_to_id == null and .original_commit_id=="58ecd753…")|[.id,.path,(.original_line|tostring),<badge>]|@tsv'
4254771284	scripts/orchestrator/three-repeat.sh	40	P2
4254771296	scripts/regime-counters.sh	132	P2
4254771302	scripts/orchestrator/dispatch.sh	94	P1
$ gh api …/commits/58ecd753…/check-runs --jq '.check_runs[]|[.name,.status,(.conclusion//"-")]|@tsv' | sort   # the previous head, superseded by this push
GitGuardian Security Checks	completed	success
private-bootstrap (macos-14, client)	completed	success
private-bootstrap (ubuntu-24.04, client)	completed	success
private-bootstrap (ubuntu-24.04, server)	completed	success
public-bootstrap (macos-14, client)	in_progress	-
public-bootstrap (ubuntu-24.04, client)	in_progress	-
public-bootstrap (ubuntu-24.04, server)	completed	success
test (macos-14, client)	completed	success
test (ubuntu-24.04, client)	completed	success
test (ubuntu-24.04, server)	in_progress	-
test (ubuntu-26.04, client)	completed	success
validate	completed	success
$ cd <main checkout> && uv run --no-project .claude/hooks/contextdb_cli.py memory search -- --help; echo rc=$?   # -- makes an option-shaped slug a query
No matches.
rc=0
$ uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_records_the_sent_line_with_its_read_marker ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line ... ok
test_dispatch_refuses_malformed_lines ... ok
test_three_repeat_prints_the_records_search_line ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout ... ok

----------------------------------------------------------------------
Ran 9 tests in 2.387s

OK
$ uv run --no-project python -m unittest tests/unit/test_regime_counters.py tests/unit/test_check_regime_boundary.py tests/unit/test_agmsg_orchestration_docs.py 2>&1 | tail -n 3
Ran 77 tests in 17.475s

OK
$ shfmt -i 4 -sr -d scripts/orchestrator/*.sh scripts/regime-counters.sh; echo "shfmt exit $?"
shfmt exit 0
$ shellcheck -x scripts/orchestrator/*.sh scripts/regime-counters.sh; echo "shellcheck exit $?"
shellcheck exit 0
$ ruff format --config ruff.toml --check tests/unit/test_orchestrator_tools.py tests/unit/test_regime_counters.py
2 files already formatted
$ uv run --no-project python "$TMPDIR/mutate-am1.py" "$PWD"; git status --short
mutant D1 mismatch check off: test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file -> rc=1 FAILED (failures=1)
mutant D2 line word-split: test_dispatch_passes_the_line_byte_identical -> rc=1 FAILED (failures=1)
mutant D3 multi-line check off: test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line -> rc=1 FAILED (failures=2)
mutant D4 the $( ) read put back: test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line -> rc=1 FAILED (failures=1)
mutant D5 TASK binding check off: test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line -> rc=1 FAILED (failures=4)
mutant D6 record not checked before the send: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D7 read marker inverted: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D8 prose dropped: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D9 duplicate keys accepted: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D10 caller root: test_dispatch_passes_the_line_byte_identical -> rc=1 FAILED (failures=1)
mutant D11 doubly named file accepted: test_dispatch_refuses_malformed_lines -> rc=1 FAILED (failures=1)
mutant D12 history read with the agent: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D13 no before-count: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D14 repeated keys accepted: test_dispatch_refuses_malformed_lines -> rc=1 FAILED (failures=1)
mutant T1 slug check loosened: test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout -> rc=1 FAILED (failures=2)
mutant T2 records match unanchored: test_three_repeat_prints_the_records_search_line -> rc=1 FAILED (failures=1)
mutant T3 class not one argument: test_three_repeat_prints_the_records_search_line -> rc=1 FAILED (failures=1)
mutant T4 caller root: test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout -> rc=1 FAILED (failures=1)
mutant T5 relative CLI path: test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout -> rc=1 FAILED (failures=1)
mutant D15 digit names skipped: test_dispatch_refuses_malformed_lines -> rc=1 FAILED (failures=3)
mutant T6 no option terminator: test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout -> rc=1 FAILED (failures=1)
mutant R4 record of another task accepted: test_s1_reads_the_ledger_classes_of_the_acceptance_record -> rc=1 FAILED (failures=1)
mutant B1 revise does not reopen: test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event -> rc=1 FAILED (failures=1)
mutant B2 withdrawn does not close: test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event -> rc=1 FAILED (failures=1)
mutant B3 silence at sixty minutes: test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event -> rc=1 FAILED (failures=1)
mutant B4 limit guard off: test_bus_read_refuses_a_read_that_reaches_its_limit -> rc=1 FAILED (failures=1)
mutant B5 the --limit flag form: test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event -> rc=1 FAILED (failures=1)
mutant R1 record mode off: test_s1_reads_the_ledger_classes_of_the_acceptance_record -> rc=1 FAILED (failures=1)
mutant R2 title not JSON-quoted: test_s1_quotes_a_title_with_shell_metacharacters -> rc=1 FAILED (failures=1)
mutant R3 slug check off: test_s1_reads_the_ledger_classes_of_the_acceptance_record -> rc=1 FAILED (failures=1)
$ git diff --numstat origin/main...HEAD -- . ":!.orchestration"
57	0	scripts/orchestrator/bus-read.sh
182	0	scripts/orchestrator/dispatch.sh
45	0	scripts/orchestrator/three-repeat.sh
29	9	scripts/regime-counters.sh
295	0	tests/unit/test_orchestrator_tools.py
41	1	tests/unit/test_regime_counters.py
$ git log --oneline 58ecd753..HEAD
9496c734 fix(orchestrator): check digit-bearing hash fields, end CLI options before the class, bind a record to its task
```

## 8. Fix round 2: CI and the Bot on `4fc6040f`

Bot review 5498947497 of `4fc6040f` (04:50:43Z): two P2s. Both are fixed: the atomic write guards gate evidence against loss.

```text
$ gh api --paginate …/pulls/336/comments --jq '.[]|select(.in_reply_to_id == null and .original_commit_id=="4fc6040f…")|[.id,.path,(.original_line|tostring),<badge>]|@tsv'
4254844587	scripts/orchestrator/dispatch.sh	159	P2
4254844595	scripts/orchestrator/dispatch.sh	173	P2
$ gh api …/commits/4fc6040f…/check-runs --jq '.check_runs[]|[.name,.status,(.conclusion//"-")]|@tsv' | sort   # the previous head
GitGuardian Security Checks	completed	success
private-bootstrap (macos-14, client)	completed	success
private-bootstrap (ubuntu-24.04, client)	completed	success
private-bootstrap (ubuntu-24.04, server)	completed	success
public-bootstrap (macos-14, client)	completed	success
public-bootstrap (ubuntu-24.04, client)	completed	success
public-bootstrap (ubuntu-24.04, server)	completed	success
test (macos-14, client)	completed	success
test (ubuntu-24.04, client)	completed	success
test (ubuntu-24.04, server)	completed	success
test (ubuntu-26.04, client)	completed	success
validate	completed	success
$ uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_records_the_sent_line_with_its_read_marker ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line ... ok
test_dispatch_refuses_malformed_lines ... ok
test_three_repeat_prints_the_records_search_line ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout ... ok

----------------------------------------------------------------------
Ran 9 tests in 2.481s

OK
$ uv run --no-project python -m unittest tests/unit/test_regime_counters.py tests/unit/test_check_regime_boundary.py tests/unit/test_agmsg_orchestration_docs.py 2>&1 | tail -n 3
Ran 77 tests in 17.698s

OK
$ shfmt -i 4 -sr -d scripts/orchestrator/*.sh scripts/regime-counters.sh; echo "shfmt exit $?"
shfmt exit 0
$ shellcheck -x scripts/orchestrator/*.sh scripts/regime-counters.sh; echo "shellcheck exit $?"
shellcheck exit 0
$ ruff format --config ruff.toml --check tests/unit/test_orchestrator_tools.py tests/unit/test_regime_counters.py
2 files already formatted
$ uv run --no-project python "$TMPDIR/mutate-am1.py" "$PWD"; git status --short
mutant D1 mismatch check off: test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file -> rc=1 FAILED (failures=1)
mutant D2 line word-split: test_dispatch_passes_the_line_byte_identical -> rc=1 FAILED (failures=1)
mutant D3 multi-line check off: test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line -> rc=1 FAILED (failures=2)
mutant D4 the $( ) read put back: test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line -> rc=1 FAILED (failures=1)
mutant D5 TASK binding check off: test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line -> rc=1 FAILED (failures=4)
mutant D6 record not checked before the send: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D7 read marker inverted: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D8 prose dropped: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D9 duplicate keys accepted: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D10 caller root: test_dispatch_passes_the_line_byte_identical -> rc=1 FAILED (failures=1)
mutant D11 doubly named file accepted: test_dispatch_refuses_malformed_lines -> rc=1 FAILED (failures=1)
mutant D12 history read with the agent: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D13 no before-count: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D14 repeated keys accepted: test_dispatch_refuses_malformed_lines -> rc=1 FAILED (failures=1)
mutant D16 another task's record accepted: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant D17 record rewritten in place: test_dispatch_records_the_sent_line_with_its_read_marker -> rc=1 FAILED (failures=1)
mutant T1 slug check loosened: test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout -> rc=1 FAILED (failures=2)
mutant T2 records match unanchored: test_three_repeat_prints_the_records_search_line -> rc=1 FAILED (failures=1)
mutant T3 class not one argument: test_three_repeat_prints_the_records_search_line -> rc=1 FAILED (failures=1)
mutant T4 caller root: test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout -> rc=1 FAILED (failures=1)
mutant T5 relative CLI path: test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout -> rc=1 FAILED (failures=1)
mutant D15 digit names skipped: test_dispatch_refuses_malformed_lines -> rc=1 FAILED (failures=3)
mutant T6 no option terminator: test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout -> rc=1 FAILED (failures=1)
mutant R4 record of another task accepted: test_s1_reads_the_ledger_classes_of_the_acceptance_record -> rc=1 FAILED (failures=1)
mutant B1 revise does not reopen: test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event -> rc=1 FAILED (failures=1)
mutant B2 withdrawn does not close: test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event -> rc=1 FAILED (failures=1)
mutant B3 silence at sixty minutes: test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event -> rc=1 FAILED (failures=1)
mutant B4 limit guard off: test_bus_read_refuses_a_read_that_reaches_its_limit -> rc=1 FAILED (failures=1)
mutant B5 the --limit flag form: test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event -> rc=1 FAILED (failures=1)
mutant R1 record mode off: test_s1_reads_the_ledger_classes_of_the_acceptance_record -> rc=1 FAILED (failures=1)
mutant R2 title not JSON-quoted: test_s1_quotes_a_title_with_shell_metacharacters -> rc=1 FAILED (failures=1)
mutant R3 slug check off: test_s1_reads_the_ledger_classes_of_the_acceptance_record -> rc=1 FAILED (failures=1)
$ git diff --numstat origin/main...HEAD -- . ":!.orchestration"
57	0	scripts/orchestrator/bus-read.sh
203	0	scripts/orchestrator/dispatch.sh
45	0	scripts/orchestrator/three-repeat.sh
29	9	scripts/regime-counters.sh
305	0	tests/unit/test_orchestrator_tools.py
41	1	tests/unit/test_regime_counters.py
$ git log --oneline 4fc6040f..HEAD
6cd491f5 fix(orchestrator): refuse another task's record and replace the record atomically
```
