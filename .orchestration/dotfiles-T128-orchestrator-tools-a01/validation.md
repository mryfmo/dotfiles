# Validation: dotfiles-T128-orchestrator-tools-a01

Seat `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `tools/orchestrator-scripts` from `origin/main` `480aabc0`. PR #328's branch `regime/playbook-rules` stays at `2276a365`, untouched (pushed before the switch). Every block is verbatim command output; `mise WARN` sandbox cache lines are filtered out.

## 1. Task copy and premises

```text
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md
aaf02188d4ea60606f07a08379ba5184582c190c79ab431ee9587be599e5a908  <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md
aaf02188d4ea60606f07a08379ba5184582c190c79ab431ee9587be599e5a908  .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md
$ cmp <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md && echo identical
identical
$ git grep -n 'class=' origin/main -- tests/unit/test_regime_counters.py
origin/main:tests/unit/test_regime_counters.py:451:            ["S1: candidate class=reject skipped contract count=3 source=fixture"],
$ git diff --stat origin/main...HEAD -- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ | tail -1; echo "(empty: the attached inputs are untouched)"
(empty: the attached inputs are untouched)
$ git ls-remote https://github.com/mryfmo/dotfiles refs/heads/regime/playbook-rules   # PR #328 untouched
2276a365cba9f104cadd7cd82f3fb0bfec7dac21	refs/heads/regime/playbook-rules
```

## 2. The new module

```text
$ uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
test_bus_read_lists_open_tasks_with_their_minutes_since_the_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_malformed_lines ... ok
test_three_repeat_prints_the_records_search_line ... ok
test_three_repeat_refuses_a_class_that_is_not_a_slug ... ok

----------------------------------------------------------------------
Ran 7 tests in 1.451s

OK
```

## 3. The counters module, and the modules that read the counters or the SKILL

```text
$ uv run --no-project python -m unittest tests/unit/test_regime_counters.py -v 2>&1 | grep -E "s1|forged|history_only|^Ran|^OK|FAIL"
test_a_forged_acceptance_record_changes_no_count ... ok
test_history_only_never_calls_gh ... ok
test_s1_candidates_are_bot_title_classes_seen_three_times ... ok
test_s1_quotes_a_title_with_shell_metacharacters ... ok
test_s1_reads_the_ledger_classes_of_the_acceptance_record ... ok
Ran 26 tests in 4.102s
OK
$ uv run --no-project python -m unittest tests/unit/test_check_regime_boundary.py tests/unit/test_agmsg_orchestration_docs.py 2>&1 | tail -n 3
Ran 51 tests in 19.502s

OK
```

## 4. shellcheck and format

```text
$ command -v shellcheck | sed "s#$HOME#~#"; shellcheck --version | sed -n 2p; shellcheck scripts/orchestrator/*.sh scripts/regime-counters.sh; echo "shellcheck exit $?"
~/.local/share/mise/installs/shellcheck/latest/shellcheck-v0.11.0/shellcheck
version: 0.11.0
shellcheck exit 0
$ ruff format --config ruff.toml --check tests/unit/test_orchestrator_tools.py tests/unit/test_regime_counters.py
2 files already formatted
$ git ls-files -s scripts/orchestrator/ | cut -c1-6,50-
100755	scripts/orchestrator/bus-read.sh
100755	scripts/orchestrator/dispatch.sh
100755	scripts/orchestrator/three-repeat.sh
```

## 5. Each guard fails its test when broken

`mutate-tools.py` (session scratch) rewrites one span per mutant in the committed tree, runs the named test, and restores the file with `git checkout --`.

```text
$ uv run --no-project python "$TMPDIR/mutate-tools.py" "$PWD"; git status --short
mutant D1 mismatch check off: test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file -> rc=1 FAILED (failures=1)
mutant D2 line word-split: test_dispatch_passes_the_line_byte_identical -> rc=1 FAILED (failures=1)
mutant D3 multi-line check off: test_dispatch_refuses_malformed_lines -> rc=1 FAILED (failures=4)
mutant T1 slug check loosened: test_three_repeat_refuses_a_class_that_is_not_a_slug -> rc=1 FAILED (failures=2)
mutant T2 records match unanchored: test_three_repeat_prints_the_records_search_line -> rc=1 FAILED (failures=1)
mutant T3 class not one argument: test_three_repeat_prints_the_records_search_line -> rc=1 FAILED (failures=1)
mutant B1 revise does not reopen: test_bus_read_lists_open_tasks_with_their_minutes_since_the_latest_event -> rc=1 FAILED (failures=1)
mutant B2 withdrawn does not close: test_bus_read_lists_open_tasks_with_their_minutes_since_the_latest_event -> rc=1 FAILED (failures=1)
mutant B3 silence at sixty minutes: test_bus_read_lists_open_tasks_with_their_minutes_since_the_latest_event -> rc=1 FAILED (failures=1)
mutant B4 limit guard off: test_bus_read_refuses_a_read_that_reaches_its_limit -> rc=1 FAILED (failures=1)
mutant B5 the --limit flag form: test_bus_read_lists_open_tasks_with_their_minutes_since_the_latest_event -> rc=1 FAILED (failures=1)
mutant R1 record mode off: test_s1_reads_the_ledger_classes_of_the_acceptance_record -> rc=1 FAILED (failures=1)
mutant R2 title not JSON-quoted: test_s1_quotes_a_title_with_shell_metacharacters -> rc=1 FAILED (failures=1)
mutant R3 slug check off: test_s1_reads_the_ledger_classes_of_the_acceptance_record -> rc=1 FAILED (failures=1)
```

## 6. A live read-only run of bus-read.sh

```text
$ scripts/orchestrator/bus-read.sh dotfiles-conformance 2>/dev/null
open: task=dotfiles-T128-gate-evidence-a03 seat=claude-standard-dot-a002 last_event=2026-10-13T01:45:59Z minutes=5 silent=no
open: task=dotfiles-T128-orchestrator-tools-a01 seat=claude-standard-dot-a003 last_event=2026-10-13T01:35:13Z minutes=16 silent=no
open: task=dotfiles-T128-task-review-t718-a02 seat=claude-review-dot-a001 last_event=2026-10-13T01:49:21Z minutes=1 silent=no
$ grep -o -E "AGMSG-ACCEPTANCE v1 task_id=[^ ]+ status=[^ ]+" <the same history.sh read> | sed "s/.*status=//" | sort | uniq -c   # the statuses the state rule covers
  89 accepted
   1 parked
   4 reset
  56 revise
  10 superseded
  38 under_review
   6 withdrawn
$ ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conformance '' 100000 2>/dev/null | grep -c ' → '   # messages in the team history
813
```

## 7. Size (INV-2 caps)

```text
$ git diff --numstat origin/main...HEAD -- . ":!.orchestration"
57	0	scripts/orchestrator/bus-read.sh
76	0	scripts/orchestrator/dispatch.sh
42	0	scripts/orchestrator/three-repeat.sh
29	9	scripts/regime-counters.sh
187	0	tests/unit/test_orchestrator_tools.py
32	1	tests/unit/test_regime_counters.py
```

## 8. CompactionDB and commits

```text
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] dotfiles-T128-orchestrator-tools-a01 (plan 007 T718 first slice): scripts/orchestrator/dispatch.sh ..."   # main checkout, permission gate
c63b57e5-47d3-46c0-92e5-142680cda997
$ git log --oneline origin/main..HEAD
8ea05883 feat(orchestrator): add dispatch, three-repeat and bus-read scripts; read S1 classes from the acceptance record
b0cba1a7 chore(orchestration): record the dotfiles-T128-orchestrator-tools-a01 task
```

## 9. Fix round 1: CI and the Bot on `61290da8`

The first head drew a CI failure and Bot review 5497968688 (02:02:40Z, two P1s).

```text
$ gh run view --job 115091278790 --log-failed | grep -E "In scripts|SC2015|##\[error\]"   # test (ubuntu-24.04, client), Run ShellCheck
In scripts/orchestrator/three-repeat.sh line 21:
            ^-- SC2015 (info): Note that A && B || C is not if-then-else. C may run when A is true.
  https://www.shellcheck.net/wiki/SC2015 -- Note that A && B || C is not if-t...
##[error]Process completed with exit code 123.
$ gh api …/runs/38334448739/jobs --jq ".jobs[]|[.name,.conclusion]|@tsv"
test (ubuntu-24.04, client)	failure
test (macos-14, client)	cancelled
test (ubuntu-24.04, server)	cancelled
test (ubuntu-26.04, client)	cancelled
$ gh api --paginate …/pulls/336/comments --jq ".[]|select(.original_commit_id==\"61290da8…\" and .in_reply_to_id==null)|[.id,.path,.original_line]|@tsv"
4253994697	scripts/orchestrator/three-repeat.sh	38
4253994704	.orchestration/dotfiles-T128-orchestrator-tools-a01/task.md	19
$ uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
test_bus_read_lists_open_tasks_with_their_minutes_since_the_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_malformed_lines ... ok
test_scripts_read_and_run_their_own_checkout_never_the_callers ... ok
test_three_repeat_prints_the_records_search_line ... ok
test_three_repeat_refuses_a_class_that_is_not_a_slug ... ok

----------------------------------------------------------------------
Ran 8 tests in 1.544s

OK
$ uv run --no-project python -m unittest tests/unit/test_regime_counters.py 2>&1 | tail -n 3
Ran 26 tests in 3.049s

OK
$ shellcheck -x scripts/orchestrator/*.sh scripts/regime-counters.sh; echo "shellcheck exit $?"
shellcheck exit 0
$ ruff format --config ruff.toml --check tests/unit/test_orchestrator_tools.py
1 file already formatted
$ uv run --no-project python "$TMPDIR/mutate-own.py" "$PWD"   # each script put back to the caller root
mutant O1 three-repeat from the caller: test_scripts_read_and_run_their_own_checkout_never_the_callers -> rc=1 FAILED (failures=1)
mutant O2 dispatch from the caller: test_scripts_read_and_run_their_own_checkout_never_the_callers -> rc=1 FAILED (failures=1)
$ uv run --no-project python "$TMPDIR/mutate-tools.py" "$PWD"; git status --short   # the 14, T1 now on the if form
mutant D1 mismatch check off: test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file -> rc=1 FAILED (failures=1)
mutant D2 line word-split: test_dispatch_passes_the_line_byte_identical -> rc=1 FAILED (failures=1)
mutant D3 multi-line check off: test_dispatch_refuses_malformed_lines -> rc=1 FAILED (failures=4)
mutant T1 slug check loosened: test_three_repeat_refuses_a_class_that_is_not_a_slug -> rc=1 FAILED (failures=2)
mutant T2 records match unanchored: test_three_repeat_prints_the_records_search_line -> rc=1 FAILED (failures=1)
mutant T3 class not one argument: test_three_repeat_prints_the_records_search_line -> rc=1 FAILED (failures=1)
mutant B1 revise does not reopen: test_bus_read_lists_open_tasks_with_their_minutes_since_the_latest_event -> rc=1 FAILED (failures=1)
mutant B2 withdrawn does not close: test_bus_read_lists_open_tasks_with_their_minutes_since_the_latest_event -> rc=1 FAILED (failures=1)
mutant B3 silence at sixty minutes: test_bus_read_lists_open_tasks_with_their_minutes_since_the_latest_event -> rc=1 FAILED (failures=1)
mutant B4 limit guard off: test_bus_read_refuses_a_read_that_reaches_its_limit -> rc=1 FAILED (failures=1)
mutant B5 the --limit flag form: test_bus_read_lists_open_tasks_with_their_minutes_since_the_latest_event -> rc=1 FAILED (failures=1)
mutant R1 record mode off: test_s1_reads_the_ledger_classes_of_the_acceptance_record -> rc=1 FAILED (failures=1)
mutant R2 title not JSON-quoted: test_s1_quotes_a_title_with_shell_metacharacters -> rc=1 FAILED (failures=1)
mutant R3 slug check off: test_s1_reads_the_ledger_classes_of_the_acceptance_record -> rc=1 FAILED (failures=1)
$ git diff --numstat origin/main...HEAD -- . ":!.orchestration"
57	0	scripts/orchestrator/bus-read.sh
77	0	scripts/orchestrator/dispatch.sh
44	0	scripts/orchestrator/three-repeat.sh
29	9	scripts/regime-counters.sh
208	0	tests/unit/test_orchestrator_tools.py
32	1	tests/unit/test_regime_counters.py
$ git log --oneline 61290da8..HEAD
e6f2bdc0 fix(orchestrator): run the contextdb CLI of the script's own checkout, never the caller's
```

## 10. Fix round 2: CI and the Bot on `4843ccb6`

CI on `4843ccb6`: `public-bootstrap (ubuntu-24.04, client)` failed on a snap store timeout (`api.snapcraft.io` HTTP 408 while installing `gtk-common-themes`), and fail-fast cancelled the other two; `gh run rerun 38335666287 --failed` passed. The Bot posted no review in 10 minutes, so `@codex review` went out at 02:21:19Z; the wait closed at 15 minutes with none, and the Bot's review of `4843ccb6` arrived at 02:27:54Z, two minutes after the window. It is read here all the same.

```text
$ gh api repos/mryfmo/dotfiles/commits/4843ccb697fb51cc273ff48b06dcfcef8d8b4fa0/check-runs --paginate --jq '.check_runs[]|[.name,.status,.conclusion]|@tsv' | sort
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
$ gh api --paginate repos/mryfmo/dotfiles/pulls/336/reviews --jq '.[]|[.user.login,.commit_id[0:8],.submitted_at]|@tsv'
chatgpt-codex-connector[bot]	61290da8	2026-10-13T02:02:40Z
chatgpt-codex-connector[bot]	4843ccb6	2026-10-13T02:27:54Z
$ gh api repos/mryfmo/dotfiles/issues/336/comments --jq '.[]|[.user.login,.created_at,(.body|split("
")[0][0:60])]|@tsv'
coderabbitai[bot]	2026-10-13T01:55:45Z	<!-- This is an auto-generated comment: summarize by coderab
chatgpt-codex-connector[bot]	2026-10-13T01:55:56Z	<!-- codex-pull-request-review-summary -->
moriya-fumio-thd	2026-10-13T02:21:18Z	@codex review
$ gh api --paginate repos/mryfmo/dotfiles/pulls/336/comments --jq '.[]|select(.in_reply_to_id == null and .user.login=="chatgpt-codex-connector[bot]" and .original_commit_id=="4843ccb6…")|[.id,.path,.original_line]|@tsv'
4254107304	scripts/orchestrator/dispatch.sh	34
4254107312	scripts/orchestrator/dispatch.sh	77
$ uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v
test_bus_read_lists_open_tasks_with_their_minutes_since_the_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_malformed_lines ... ok
test_scripts_read_and_run_their_own_checkout_never_the_callers ... ok
test_three_repeat_prints_the_records_search_line ... ok
test_three_repeat_refuses_a_class_that_is_not_a_slug ... ok

----------------------------------------------------------------------
Ran 8 tests in 1.522s

OK
$ shellcheck -x scripts/orchestrator/*.sh scripts/regime-counters.sh; echo "shellcheck exit $?"
shellcheck exit 0
$ ruff format --config ruff.toml --check tests/unit/test_orchestrator_tools.py
1 file already formatted
$ uv run --no-project python "$TMPDIR/mutate-nl.py" "$PWD"; git status --short
mutant N1 the $( ) read put back: test_dispatch_refuses_malformed_lines -> rc=1 FAILED (failures=4)
$ git diff --numstat origin/main...HEAD -- . ":!.orchestration"
57	0	scripts/orchestrator/bus-read.sh
78	0	scripts/orchestrator/dispatch.sh
44	0	scripts/orchestrator/three-repeat.sh
29	9	scripts/regime-counters.sh
210	0	tests/unit/test_orchestrator_tools.py
32	1	tests/unit/test_regime_counters.py
$ git log --oneline 4843ccb6..HEAD
17d3735d fix(orchestrator): refuse a dispatch line file with a blank line after the message
```

## 12. Amendment 1 (TASK 03:13:58Z, sha256 `91eb1ebe…`)

```text
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md
91eb1ebe246f76e138ce8f3bf108adff844f5acf303bcfecc2b7bc62eb0130ee  <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md
91eb1ebe246f76e138ce8f3bf108adff844f5acf303bcfecc2b7bc62eb0130ee  .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md
$ cmp <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md && echo identical
identical
$ sed -n '81,82p' ~/.agents/skills/agmsg/scripts/history.sh   # the read marker is all history.sh prints of read state
# Read-state for the ●(unread)/○(read) marker (G2(c)): read-state is
# recipient-scoped and not carried on a history record, so derive it by unioning
$ /usr/bin/grep -n -E "read_at|^exit|exit 0" ~/.local/bin/common/agmsg-dispatch | head -8   # agmsg-dispatch polls read_at and prints none of it
92:        receipt=$(sqlite3 "$db" "SELECT read_at IS NOT NULL FROM messages WHERE id=$message_id;") || exit 1
109:    exit 0
116:    exit 0
118:exit 1
$ /usr/bin/grep -c 'closed: tests/unit/test_orchestrator_tools.py::' .orchestration/dotfiles-T128-orchestrator-tools-a01/task.md; for t in $(sed -n 's/.*closed: tests\/unit\/test_orchestrator_tools.py::\([a-z0-9_]*\).*/\1/p' <task copy>); do printf '%s ' "$t"; /usr/bin/grep -c "def $t(" tests/unit/test_orchestrator_tools.py; done   # each closed row names a test in this head
4
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file 1
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line 1
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout 1
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event 1
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
Ran 9 tests in 1.899s

OK
$ uv run --no-project python -m unittest tests/unit/test_regime_counters.py tests/unit/test_check_regime_boundary.py tests/unit/test_agmsg_orchestration_docs.py 2>&1 | tail -n 3
Ran 77 tests in 17.397s

OK
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
$ git diff --numstat origin/main...HEAD -- . ":!.orchestration"
57	0	scripts/orchestrator/bus-read.sh
153	0	scripts/orchestrator/dispatch.sh
44	0	scripts/orchestrator/three-repeat.sh
29	9	scripts/regime-counters.sh
258	0	tests/unit/test_orchestrator_tools.py
32	1	tests/unit/test_regime_counters.py
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] dotfiles-T128-orchestrator-tools-a01 amendment 1: ..."   # main checkout, permission gate
63c8d8c4-4ff9-42d1-b95f-d5429f80dbc6
$ git log --oneline 5b6d5f24..HEAD
0a5ae302 feat(orchestrator): record dispatches in the acceptance record and refuse an unbound TASK
2dddff84 chore(orchestration): recommit the dotfiles-T128-orchestrator-tools-a01 task at amendment 1
```

## 13. Amendment 1, fix round 1: CI and the Bot on `374fc171`

Bot review 5498425049 of `374fc171` (03:28:16Z): two P1s and one P2 on `dispatch.sh`. CI: `Run shfmt` failed on a backslash-continued pipe that this round removes.

```text
$ gh api …/commits/374fc171…/check-runs --jq '.check_runs[]|.conclusion' | sort | uniq -c
   2 
   2 cancelled
   2 failure
   6 success
$ gh api …/actions/jobs/<id> --jq '[.conclusion, (.steps[]|select(.conclusion=="failure")|.name)]|@tsv'   # test (ubuntu-24.04, client) and test (ubuntu-26.04, client)
failure	Run `shfmt`
failure	Run `shfmt`
$ gh run view --job 115112766434 --log-failed | grep -A9 "^diff scripts/orchestrator"
diff scripts/orchestrator/dispatch.sh.orig scripts/orchestrator/dispatch.sh
--- scripts/orchestrator/dispatch.sh.orig
+++ scripts/orchestrator/dispatch.sh
@@ -148,6 +148,6 @@
 python3 -I -c "${recorder}" check "${record}" "${line}" "${from}" "${to}" < /dev/null
 rc=0
 agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" || rc=$?
-"${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "${to}" 200 \
-    | python3 -I -c "${recorder}" append "${record}" "${line}" "${from}" "${to}"
+"${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "${to}" 200 |
$ gh api --paginate …/pulls/336/comments --jq '.[]|select(.in_reply_to_id == null and .original_commit_id=="374fc171…")|[.id,.path,(.original_line|tostring),(.body|split("
")[0]|capture("!\[(?<p>P[0-3])").p)]|@tsv'
4254399800	scripts/orchestrator/dispatch.sh	87	P1
4254399805	scripts/orchestrator/dispatch.sh	152	P1
4254399807	scripts/orchestrator/dispatch.sh	152	P2
$ sed -n '30p' ~/.agents/skills/agmsg/scripts/history.sh; awk '/agmsg_self_rename_on_action\(\)/{p=1} p{n++; if(n<=3) print}' ~/.agents/skills/agmsg/scripts/lib/self-rename.sh   # an agent argument renames the caller; an empty one returns at once
  agmsg_self_rename_on_action "$TEAM" "$AGENT"
agmsg_self_rename_on_action() {
  local team="${1:-}" agent="${2:-}" type="${3:-}"
  [ -n "$team" ] && [ -n "$agent" ] || return 0
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
Ran 9 tests in 2.318s

OK
$ uv run --no-project python -m unittest tests/unit/test_regime_counters.py tests/unit/test_check_regime_boundary.py tests/unit/test_agmsg_orchestration_docs.py 2>&1 | tail -n 3
Ran 77 tests in 19.035s

OK
$ shfmt --version; shfmt -i 4 -sr -d scripts/orchestrator/*.sh scripts/regime-counters.sh; echo "shfmt exit $?"   # the CI command
v3.14.1
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
$ git diff --numstat origin/main...HEAD -- . ":!.orchestration"
57	0	scripts/orchestrator/bus-read.sh
165	0	scripts/orchestrator/dispatch.sh
44	0	scripts/orchestrator/three-repeat.sh
29	9	scripts/regime-counters.sh
278	0	tests/unit/test_orchestrator_tools.py
32	1	tests/unit/test_regime_counters.py
$ git log --oneline 374fc171..HEAD
b80b03ee fix(orchestrator): read the dispatch marker team-wide, record only this send's row, refuse a doubly named file
```
