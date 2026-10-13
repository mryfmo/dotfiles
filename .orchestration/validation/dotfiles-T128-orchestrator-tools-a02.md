# Validation: dotfiles-T128-orchestrator-tools-a02 (PR-A)

Seat `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `tools/orchestrator-scripts-2` from `origin/main` at `a03c1daa`. Items 3, 4 and 6 are in `74c7d92e` and PR-A's seven scripts in `9ee41105`. Every block is verbatim command output, and `mise WARN` sandbox cache lines are filtered out.

## 1. Task copy and base

```text
$ shasum -a 256 <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md .orchestration/dotfiles-T128-orchestrator-tools-a02/task.md
a4c929b14f28ba5f67d007548f7e3b8e5bdcf48cf37c17eae76c4375cb363ce5  <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md
a4c929b14f28ba5f67d007548f7e3b8e5bdcf48cf37c17eae76c4375cb363ce5  .orchestration/dotfiles-T128-orchestrator-tools-a02/task.md
$ cmp <main checkout>/.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md .orchestration/dotfiles-T128-orchestrator-tools-a02/task.md && echo identical
identical
$ git log --oneline origin/main..HEAD; git merge-base HEAD origin/main
9ee41105 feat(orchestrator): boundary, ff-main, orch-audit, codex-review, replay, design-keydiff and fill_sweep
74c7d92e fix(orchestrator): a02 items 3, 4 and 6 on the first slice's scripts
a03c1daa394036d021c0b03b293a48603b923575
$ git diff --stat origin/main...HEAD -- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input scripts/orchestrator/three-repeat.sh | tail -1; echo "(empty: the attached inputs and three-repeat.sh are untouched)"
(empty: the attached inputs and three-repeat.sh are untouched)
$ for t in $(sed -n "s/.*closed: tests\/unit\/\(test_[a-z_]*\)\.py::\([a-z0-9_]*\).*/\1:\2/p" <a02 copy>); do printf "%s " "$t"; /usr/bin/grep -c "def ${t#*:}(" "tests/unit/${t%%:*}.py"; done
test_orchestrator_tools:test_boundary_stops_before_commit_when_the_validator_fails 1
test_orchestrator_tools:test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history 1
test_regime_counters:test_s1_ignores_a_record_whose_ledger_rows_are_not_id_class_objects 1
$ git diff origin/main...HEAD -- scripts/orchestrator scripts/regime-counters.sh | /usr/bin/grep -oE "^\+.*\b(basename|cmp|realpath|readlink|stat|perl|python )\b" | sort -u; echo "(empty: no host binary outside the threat row's list)"
(empty: no host binary outside the threat row's list)
```

## 2. Tests, lint and size

```text
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v 2>&1 | sed -E 's/ \(tests\.unit\.[a-z_]+\.[A-Za-z]+\.[a-z0-9_]+\)//'   # drops each test's repeated dotted id; UV_OFFLINE: the sandbox has no pypi, CI does
test_boundary_commits_pushes_and_queues_the_pr ... ok
test_boundary_stops_before_commit_when_the_validator_fails ... ok
test_bus_read_closes_a_task_on_any_non_revise_acceptance ... ok
test_bus_read_ignores_closers_between_other_endpoints ... ok
test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event ... ok
test_bus_read_refuses_a_read_that_reaches_its_limit ... ok
test_bus_read_skips_and_counts_malformed_rows ... ok
test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash ... ok
test_design_keydiff_names_the_changed_invariant ... ok
test_dispatch_line_grammar_table ... ok
test_dispatch_passes_the_line_byte_identical ... ok
test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history ... ok
test_dispatch_records_the_sent_line_with_its_read_marker ... ok
test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file ... ok
test_dispatch_refuses_a_line_without_a_task_id ... ok
test_dispatch_refuses_a_malformed_record_block_before_sending ... ok
test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line ... ok
test_dispatch_refuses_an_unwritable_record_before_sending ... ok
test_dispatch_refuses_malformed_lines ... ok
test_ff_main_keeps_local_edits_across_the_fast_forward ... ok
test_fill_sweep_refuses_a_not_applicable_without_evidence ... ok
test_replay_propagates_the_command_status ... ok
test_three_repeat_prints_body_matches_and_states_a_capped_memory_count ... ok
test_three_repeat_prints_the_records_search_line ... ok
test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout ... ok

----------------------------------------------------------------------
Ran 25 tests in 11.813s

OK
$ uv run --no-project python -m unittest tests/unit/test_regime_counters.py -v 2>&1 | sed -E 's/ \(tests\.unit\.[a-z_]+\.[A-Za-z]+\.[a-z0-9_]+\)//'
test_a_600_row_history_counts_fully_through_the_storage_facade ... ok
test_a_forged_acceptance_record_changes_no_count ... ok
test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity ... ok
test_a_status_in_free_text_counts_nothing ... ok
test_a_store_at_another_schema_revision_is_unreadable ... ok
test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id ... ok
test_bot_heads_are_unknown_when_gh_fails ... ok
test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit ... ok
test_bot_heads_are_unknown_without_a_first_result_head ... ok
test_bot_heads_read_every_page_through_gh_api ... ok
test_every_line_names_its_source ... ok
test_every_result_counts_as_a_revise_whatever_its_status ... ok
test_history_only_never_calls_gh ... ok
test_list_tasks_prints_each_task_id_once ... ok
test_only_p0_and_p1_heads_after_the_first_result_head_count ... ok
test_s1_candidates_are_bot_title_classes_seen_three_times ... ok
test_s1_ignores_a_record_whose_ledger_rows_are_not_id_class_objects ... ok
test_s1_quotes_a_title_with_shell_metacharacters ... ok
test_s1_reads_the_ledger_classes_of_the_acceptance_record ... ok
test_t118_fixture_counts_revises_from_results ... ok
test_t119_fixture_counts_every_task_after_the_first_as_an_amendment ... ok
test_t124_wave1_fixture_counts_bot_heads_after_the_first_result_head ... ok
test_the_boundary_check_never_passes_a_test_seam ... ok
test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one ... ok
test_thresholds_are_inv6_constants ... ok
test_usage_errors_exit_2 ... ok
test_v0_fixture_counts_bot_heads_after_the_first_result_head ... ok

----------------------------------------------------------------------
Ran 27 tests in 4.380s

OK
$ shellcheck --version | sed -n 2p; shellcheck -x scripts/orchestrator/*.sh scripts/regime-counters.sh && echo shellcheck-ok
version: 0.11.0
shellcheck-ok
$ (cd "$TMPDIR" && mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d <worktree>/scripts/orchestrator/*.sh <worktree>/scripts/regime-counters.sh) | /usr/bin/grep -v 'mise WARN'; echo shfmt-rc=${pipestatus[1]}
shfmt-rc=0
$ ruff --version; git diff --name-only origin/main...HEAD -- "*.py" | xargs ruff format --config ruff.toml --check; git diff --name-only origin/main...HEAD -- "*.py" | xargs ruff check
ruff 0.17.0
4 files already formatted
All checks passed!
$ git diff --numstat origin/main...HEAD
56	0	scripts/orchestrator/boundary.sh
12	8	scripts/orchestrator/bus-read.sh
39	0	scripts/orchestrator/codex-review.sh
40	0	scripts/orchestrator/design-keydiff.py
63	36	scripts/orchestrator/dispatch.sh
63	0	scripts/orchestrator/ff-main.sh
80	0	scripts/orchestrator/fill_sweep.py
84	0	scripts/orchestrator/orch-audit.sh
30	0	scripts/orchestrator/replay.sh
22	12	scripts/regime-counters.sh
308	7	tests/unit/test_orchestrator_tools.py
48	2	tests/unit/test_regime_counters.py
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^\.orchestration\// {f++} $3 !~ /^\.orchestration\// && $3 !~ /^tests\// {o+=$1} $3 ~ /^tests\// {t+=$1} END {print "files outside .orchestration/:", f, "added outside tests/:", o, "added under tests/:", t}'
files outside .orchestration/: 12 added outside tests/: 489 added under tests/: 356
```

## 3. Mutation proofs

Each mutant changes one span (D1 two), runs its named test with `UV_OFFLINE=1`, and restores the files with `git checkout --`. The script is in the seat scratchpad; lines are cut at 240 characters and the home directory is written `~`.

```text
$ uv run --no-project python <scratchpad>/mutate-a02.py 2>&1 | cut -c1-240 | sed "s|$HOME|~|g"
C1 row shape unchecked: test_s1_ignores_a_record_whose_ledger_rows_are_not_id_class_objects -> FAILED (killed) | AssertionError: 5 != 0 : jq: error (at /private/tmp/claude-501/tmpk7qjp722/repo/.orchestration/acceptance/T1.md:3): Cannot inde
C2 id type unchecked: test_s1_ignores_a_record_whose_ledger_rows_are_not_id_class_objects -> FAILED (killed) | AssertionError: Lists differ: ['S1: candidate class=unclassified count=3 title[65 chars]ing'] != ['S1: class=bookkeeping count=4 
C3 class unchecked: test_s1_ignores_a_record_whose_ledger_rows_are_not_id_class_objects -> FAILED (killed) | AssertionError: Lists differ: ['S1: candidate class=unclassified count=3 title[66 chars]lug'] != ['S1: class=bookkeeping count=3 so
C4 non-JSON block silent: test_s1_ignores_a_record_whose_ledger_rows_are_not_id_class_objects -> FAILED (killed) | AssertionError: Lists differ: ['S1:[51 chars] skipped contract tests" source=record-ignored:block-not-json'] != ['S1:[51 char
D1 recorder re-tokenizes: test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history -> FAILED (killed) | AssertionError: 0 != 1 : 
D2 no lock: test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history -> FAILED (killed) | AssertionError: Lists differ: [None, None] != [0, 0]
D3 capped read sent: test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history -> FAILED (killed) | AssertionError: 0 != 1 : 
D4 tokens without = pass: test_dispatch_line_grammar_table -> FAILED (killed) | AssertionError: 0 != 2 : 
D5 tab prefix refused: test_dispatch_line_grammar_table -> FAILED (killed) | AssertionError: 2 != 0 : dispatch: not an AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line
D6 CRLF translated: test_dispatch_records_the_sent_line_with_its_read_marker -> FAILED (killed) | AssertionError: False is not true : b'---\n{\n  "dispatch": [\n    "AGMSG-PING v1 task_id=t reason=check read_at=unread"\n  ],\n  "task": "t"\
B1 limit after the filter: test_bus_read_refuses_a_read_that_reaches_its_limit -> FAILED (killed) | AssertionError: 0 != 1 : 
B2 clock from any endpoints: test_bus_read_ignores_closers_between_other_endpoints -> FAILED (killed) | AssertionError: ' silent=yes' not found in 'open: task=T1 seat=w1 last_event=2026-10-13T10:06:31Z minutes=23 silent=no'
B3 split on one space: test_bus_read_ignores_closers_between_other_endpoints -> FAILED (killed) | AssertionError: Tuples differ: ([('T1', 'w1')], 'skipped=1') != ([('T1', 'w1'), ('T2', 'w2')], 'skipped=2')
N1 validator ignored: test_boundary_stops_before_commit_when_the_validator_fails -> FAILED (killed) | AssertionError: 0 != 2 : 
N2 no copy-back: test_ff_main_keeps_local_edits_across_the_fast_forward -> FAILED (killed) | AssertionError: Lists differ: ['restored: .orchestration/a.md', 'restored: .orchestration/c.md'] != ['ff-main: at 3695793']
N4 replay status dropped: test_replay_propagates_the_command_status -> FAILED (killed) | AssertionError: 0 != 7 : 
N5 stdin open: test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash -> FAILED (killed) | AssertionError: '' != 'open\n'
N6 profile from env: test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash -> FAILED (killed) | AssertionError: Lists differ: ['--profile', 'review', 'exec', '--sandbox', 'read-only'[222 chars]70.'] != ['--profile', 'deep', 'e
N7 hash unchecked: test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash -> FAILED (killed) | AssertionError: 3 != 2 : 
N8 codex status dropped: test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash -> FAILED (killed) | AssertionError: 0 != 3 : 
N9 sub-keys not named: test_design_keydiff_names_the_changed_invariant -> FAILED (killed) | AssertionError: "invariants ['INV-6']\n" != 'invariants changed\n'
N10 evidence not required: test_fill_sweep_refuses_a_not_applicable_without_evidence -> FAILED (killed) | AssertionError: 1 != 0 : items 2 filled 2 gaps 0
survivors: 0
$ git status --short scripts tests; echo "(empty: every mutant restored)"
(empty: every mutant restored)
```

## 4. bus-read.sh on the live team history

```text
$ bash scripts/orchestrator/bus-read.sh dotfiles-conformance
open: task=dotfiles-T128-orchestrator-tools-a02 seat=claude-standard-dot-a003 last_event=2026-10-13T10:00:24Z minutes=31 silent=yes
skipped=47
```

The full `tests/unit` discover is not rerun for this task: the change touches only `scripts/orchestrator/`, `scripts/regime-counters.sh` and their two test modules, which the runs above cover, and CI runs the discover on the pushed head.

## 5. CI and the Bot on `1287af34` (main-checkout copy only)

```text
$ gh pr checks 346 --watch --interval 30   # the final listing
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	1s	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38384234639/job/115251917615	
private-bootstrap (ubuntu-24.04, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38384234639/job/115251917693	
private-bootstrap (ubuntu-24.04, server)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/38384234639/job/115251917343	
public-bootstrap (macos-14, client)	pass	8m28s	https://github.com/mryfmo/dotfiles/actions/runs/38384234639/job/115251917700	
public-bootstrap (ubuntu-24.04, client)	pass	9m5s	https://github.com/mryfmo/dotfiles/actions/runs/38384234639/job/115251917844	
public-bootstrap (ubuntu-24.04, server)	pass	7m42s	https://github.com/mryfmo/dotfiles/actions/runs/38384234639/job/115251917612	
test (macos-14, client)	pass	6m57s	https://github.com/mryfmo/dotfiles/actions/runs/38384234576/job/115251917803	
test (ubuntu-24.04, client)	pass	7m59s	https://github.com/mryfmo/dotfiles/actions/runs/38384234576/job/115251917506	
test (ubuntu-24.04, server)	pass	5m40s	https://github.com/mryfmo/dotfiles/actions/runs/38384234576/job/115251917820	
test (ubuntu-26.04, client)	pass	8m23s	https://github.com/mryfmo/dotfiles/actions/runs/38384234576/job/115251917723	
validate	pass	1m41s	https://github.com/mryfmo/dotfiles/actions/runs/38384234956/job/115251919013	
exit=0
$ the Bot wait, 20 minutes from the push (reviews whose commit_id is the head, issue comments and review comments created after the push)
reviews on 1287af3435e4847ef819e43972b0da4bfe156e60:
issue comments after push:
6143634052 coderabbitai[bot] 2026-10-13T10:34:08Z <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
review comments created after the push:
2026-10-13T10:54:25Z
```

```text
$ the late check at the orchestrator's resume (reviews, review comments, issue comments of PR 346, and its head)
reviews:
review comments:
issue comments:
6143634052 coderabbitai[bot] 2026-10-13T10:34:08Z
head: 1287af34 UNKNOWN
2026-10-13T14:27:45Z
$ git log --oneline a03c1daa..origin/main; git diff --stat a03c1daa origin/main -- scripts tests | tail -3; git merge-tree --write-tree origin/main HEAD > /dev/null && echo "merges cleanly with origin/main"
4e7a9b3a chore(orchestration): boundary commit 2026-10-13 (12): plan 020/021 (the by-construction order), the three owner tasks, the cost ledger, plans 018 and 019 (#348)
a1d33849 chore(orchestration): boundary commit 2026-10-13 (11): T718 first slice merged (a04 records), a02 dispatched, T703 a04 amendment 1 and its owner task, M-20261012-34/35, C-33/34, plan 017 (#347)
merges cleanly with origin/main
```

## 6. Revise round (`3544d195`)

The branch reset to the orchestrator's update-branch merge, then the fix commit:

```text
$ git fetch origin && git reset --hard origin/tools/orchestrator-scripts-2
HEAD is now at 9ad0c150 Merge branch 'main' into tools/orchestrator-scripts-2
$ git log --oneline -2
3544d195 fix(orchestrator): the TASK kind from the parsed tokens; fill only neutral annotations and statuses
9ad0c150 Merge branch 'main' into tools/orchestrator-scripts-2
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -m unittest tests.unit.test_orchestrator_tools tests.unit.test_regime_counters
Ran 54 tests in 16.530s

OK
$ shellcheck scripts/orchestrator/dispatch.sh && echo sc-ok
sc-ok
$ (cd "$TMPDIR" && shfmt -i 4 -sr -d <worktree>/scripts/orchestrator/dispatch.sh) && echo shfmt-ok
shfmt-ok
$ ruff format --config ruff.toml --check scripts/orchestrator/fill_sweep.py tests/unit/test_orchestrator_tools.py; ruff check <same>
2 files already formatted
All checks passed!
$ git diff --numstat origin/main HEAD | awk <the §2 size filter>
files outside .orchestration/: 12 added outside tests/: 494 added under tests/: 387
```

Mutants: each reverts one span of `3544d195` with `sed`, runs the named test with its class in the path, and copies the saved file back.

```text
R1: AssertionError: 0 != 1 : 
R2: AssertionError: 1 != 0 : items 7 filled 7 gaps 0
R3: AssertionError: Lists differ: ['ann[28 chars]n-failure', 'status-failure', 'status-error', 'status-pending'] != ['ann[28 chars]n-failure']
$ git status --short scripts tests; echo "(empty: every mutant restored)"
(empty: every mutant restored)
```

- R1: the kind check back on the literal `"AGMSG-TASK "*` prefix. `test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields` fails on both rows.
- R2: `rule = RULES.get(source)` for every level. `test_fill_sweep_fills_only_notice_annotations_and_success_statuses` fails: all seven items are filled.
- R3: `NEUTRAL` without `status`. The same test fails: the three non-success statuses are filled.

The full discover (`python -m unittest discover -s tests/unit`, as `Makefile:185`) ran 1052 tests here and failed in eight modules this round does not touch (test_require_crit_review, test_herdr_agents, test_agent_stop_gate, test_ua_symbol_coverage, test_runtime_health, test_gh_auth, test_supply_chain_policy, test_aws_cli_acquisition). The cause is the seat sandbox: the global `commit.gpgsign=true` signs with `~/.ssh/id_ed25519.pub`, which the sandbox denies, so a test's temporary-repository commit fails (`fatal: failed to write commit object`; then `--base 'main' does not resolve to a commit`). CI runs the discover on the pushed head; §7 records that run.

## 7. CI on `7b574d32` (main-checkout copy only)

The first watch ended on `Post "https://api.github.com/graphql": … connection reset by peer` with the checks still pending; the rerun:

```text
$ gh pr checks 346 --watch --interval 30; echo "rc=$?"   # the full check table, then the exit status
private-bootstrap (macos-14, client)	pass	12s
private-bootstrap (ubuntu-24.04, client)	pass	9s
private-bootstrap (ubuntu-24.04, server)	pass	9s
public-bootstrap (macos-14, client)	pass	8m48s
public-bootstrap (ubuntu-24.04, client)	pass	10m42s
public-bootstrap (ubuntu-24.04, server)	pass	7m14s
test (macos-14, client)	pass	7m31s
test (ubuntu-24.04, client)	pass	8m46s
test (ubuntu-24.04, server)	pass	6m14s
test (ubuntu-26.04, client)	pass	9m33s
validate	pass	1m49s
CodeRabbit	pass	0
GitGuardian Security Checks	pass	17s
rc=0
```

All 13 checks pass, among them the four `test` jobs that run the `tests/unit` discover. That confirms the §6 reading: the local discover failures came from the seat sandbox, not from this round. No Bot wait for this round (the revise).
