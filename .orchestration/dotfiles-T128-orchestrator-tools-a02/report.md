# Report: dotfiles-T128-orchestrator-tools-a02 (PR-A)

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `tools/orchestrator-scripts-2` from `origin/main` at `a03c1daa` (the first slice's merge), as a draft PR.
- Task file sha256 `a4c929b1…` matches the TASK's `task_sha256`. It is copied byte-identical to `.orchestration/dotfiles-T128-orchestrator-tools-a02/task.md` (validation §1).

## The split

The orchestrator agreed to the split on the bus (PING of 10:01:32Z, an answer to my question; INV-6 `questions=1`). There were two reasons:

- `acceptance-front-matter.py` must import the gate module's record validator, and `orch-gate.sh` passes `ACCEPTANCE_EVIDENCE` and never `AUDIT_DISPOSITIONS`. On `origin/main` (`a03c1daa`), `scripts/require-crit-review.py` has no `read_acceptance_record`, `record_field_errors` or `mistake_records` and reads no `ACCEPTANCE_EVIDENCE`. They exist only on PR #329's branch (`regime/gate-evidence`).
- The whole scope came to about 510 added lines outside `tests/` (cap 500).

So the work lands in two PRs:

- **PR-A (this PR):** items 3, 4 and 6, plus `boundary.sh`, `ff-main.sh`, `orch-audit.sh`, `codex-review.sh`, `replay.sh`, `design-keydiff.py` and `fill_sweep.py`.
- **PR-B:** `acceptance-front-matter.py`, `orch-gate.sh` and their tests, on `tools/orchestrator-scripts-3` from `origin/main` after #329 merges, with its own RESULT. PR-B is open work.

## Items 3, 4 and 6 (`74c7d92e`)

| Row | Finding | Disposition | Closing test |
|---|---|---|---|
| 4255079204 (item 3), local:3e5cad3:1 | the counters trusted a malformed ledger block | `fixed:74c7d92e`. The block counts only when every `ledger` row is an object with a string `id` and a `[a-z0-9-]` `class`. Otherwise the title detector speaks, and its lines end `source=record-ignored:<block-not-json\|ledger-row-not-object\|id-not-string\|class-not-slug>`, the script's own slugs | `test_regime_counters.py::test_s1_ignores_a_record_whose_ledger_rows_are_not_id_class_objects` (mutants C1 to C4) |
| 4255272793 (item 4a) | the recorder split the line on single spaces, so a tab hid `task_id` from the record check | `fixed:74c7d92e`. One parse: bash hands the recorder the `task_id` it validated | `test_dispatch_record_path_tokenizes_locks_and_refuses_a_capped_history` (D1) |
| 4255272797 (item 4b) | two dispatches to one record could lose an entry | `fixed:74c7d92e`. The record's read-modify-write holds an exclusive `fcntl.flock` (see below) | the same test: both sends wait while the test holds the lock, then both are recorded (D2) |
| 4255272803 (item 4c) | a capped history could hide the new row | `fixed:74c7d92e`. Before the send, a read whose non-empty lines reach `BUS_READ_LIMIT` is refused with `dispatch: the history read is capped at <limit> rows; raise BUS_READ_LIMIT` | the same test (D3) |
| 4256541725 (item 4) | `previous_<name>_sha256=` | already fixed on main in `e2e67de8` (a04) | `test_dispatch_line_grammar_table` accepts it |
| 4256987062 (item 6) | bus-read.sh checked the limit after skipping rows | `fixed:74c7d92e`. The limit is checked against every non-empty line, before any row is skipped | `test_bus_read_refuses_a_read_that_reaches_its_limit` (B1) |
| 4256987076 (item 6) | the silence clock counted rows between other endpoints | `fixed:74c7d92e`. `last_event` is the latest counted row between the opener's two endpoints | `test_bus_read_ignores_closers_between_other_endpoints` (B2) |
| 4256987087 (item 6) | a CRLF record's prose was rewritten with LF | `fixed:74c7d92e`. The record is read and written with `newline=""`, and a block whose delimiter lines end in CRLF is found | `test_dispatch_records_the_sent_line_with_its_read_marker` (D6) |
| audit:3e5cad3:1 (item 6) | bus-read.sh split a body on single spaces | `fixed:74c7d92e`. A body is split on runs of spaces and tabs, as the stop gate's awk splits it | `test_bus_read_ignores_closers_between_other_endpoints` (B3) |

Item 4's line grammar:

- The prefix is `AGMSG-(TASK|ACCEPTANCE|PING)`, then blanks, then `v1`.
- Tokens are split on any run of spaces and tabs.
- Every token after `v1` must be `<key>=<value>`, else exit 2. This also refuses a repeated prefix, and a value a space split in two.
- `test_dispatch_line_grammar_table` refuses one line per remaining row: no `v1`, a repeated prefix, a TASK without `task_file`, a non-hex hash, a source named both ways, a repeated source key, a missing source file, and a token without `=`. It accepts `previous_design_sha256=` and a tab-separated TASK (D4, D5).

One deviation from item 4b: the task names a sibling lock file. `dispatch.sh` instead locks the record's directory fd, with the same `fcntl.flock` (exclusive, released at exit). A sibling `.<record>.lock` file would sit untracked under `.orchestration/acceptance/`, and `boundary.sh`'s `git status --untracked-files=all -- .orchestration` list would commit it (`git check-ignore` matches nothing for it). `flock` on a directory fd holds on macOS (checked) and Linux. The lock covers every record in that directory, which is a stricter guard than one per record.

## Item 1, PR-A's seven scripts (`9ee41105`)

| Script | What it does | Test |
|---|---|---|
| `boundary.sh <YYYY-MM-DD-n> <message-file>` | the input's sequence, with paths from the script's checkout:<br>1. the `git status` list;<br>2. a `--no-track` worktree of `origin/main` under `$TMPDIR`;<br>3. the masker;<br>4. `make validate-agent-assets`;<br>5. the commit;<br>6. the push to `origin` with the gh credential helper;<br>7. `gh pr create`, then `gh pr merge --squash --auto`;<br>8. `git worktree remove`.<br>A failing step stops before the commit and leaves the worktree for inspection. No `rm` | `test_boundary_stops_before_commit_when_the_validator_fails` (N1), `test_boundary_commits_pushes_and_queues_the_pr` |
| `ff-main.sh` | M-20261012-26's fourth-instance sequence:<br>1. moves the local edits and the untracked `.orchestration` copies that `origin/main` holds aside under `$TMPDIR`;<br>2. restores the tracked ones with `git checkout --`;<br>3. `git merge --ff-only`;<br>4. copies back only the files that still differ.<br>A refused fast-forward puts every file back. An ERR trap names the aside directory if a step fails before the copy-back. `rm -r` only on that directory | `test_ff_main_keeps_local_edits_across_the_fast_forward` (N2) |
| `orch-audit.sh <task> <pr-worktree> <pr> [--ledger-check <script>]` | the head from `git -C <pr-worktree> rev-parse HEAD`. Refuses:<br>- a checkout at the head;<br>- an untracked or changed validator;<br>- a review worktree that is not clean;<br>- a sweep with gaps.<br>Runs a ledger check only when the script is tracked here. Removes the earlier audit files of that head first. Runs `codex --profile audit exec` with stdin closed and branches on codex's own exit status, not a pipe's; restores the review worktree either way; masks the copies | none: its row is `residual` |
| `codex-review.sh <file> <template> <receipt> <transcript>` | the profile is fixed at `review`; the hash is rendered for `@@SHA@@`, else exit 2; `< /dev/null`; codex's status propagates | `test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash` (N5 to N8) |
| `replay.sh <command…>` | `env -i PATH=/usr/bin:/bin bash -c` in a detached worktree of `origin/main` (the ref as last fetched; the script does not fetch); prints `exit=<n>` and exits with it | `test_replay_propagates_the_command_status` (N4) |
| `design-keydiff.py <design.md>` | argparse; the hashed keys that differ from `HEAD:./<path>` | `test_design_keydiff_names_the_changed_invariant` (N9) |
| `fill_sweep.py <sweep> <comments> [extra.tsv]` | the input's rules. Every not-applicable must have the gate's grammar, one `; evidence=` between a non-empty reason and a non-empty command; one without it is a gap and nothing is written. The fixed rules carry a `jq` command that shows the item | `test_fill_sweep_refuses_a_not_applicable_without_evidence` (N10: the fails-when-removed proof) |

- The design-keydiff test runs the real `uv run --no-project --with pyyaml`, as `test_check_regime_boundary` does. CI has the network for it. In the sandbox, uv cannot reach pypi, so the module runs here with `UV_OFFLINE=1` from the uv cache (validation §2).
- `bash` on this host is 3.2. ff-main's possibly empty arrays use the `${a[@]+"${a[@]}"}` form, and the tests run every script with the host's `bash`.
- The attached inputs are untouched (validation §1).
- `three-repeat.sh` is unchanged: no item-6 row names it, so its two edit rows are no-ops in this PR (validation §1).
- Host binaries: every script resolves only the binaries the threat table's environment row lists (validation §1).
  - `boundary.sh` takes the message file's name with `${2##*/}` rather than `basename`.
  - `ff-main.sh` compares with `git diff --no-index --quiet` rather than `cmp`.
  - `orch-audit.sh` is a third user of `uv run --no-project --with pyyaml` (the masker, the SKILL's own command) beside the two the row names.
- Item 3 reading: `source=record-ignored:<reason>` appears on the S1 candidate lines, as the item says ("stated on the line"). With fewer than three equal Bot titles there is no S1 line, so nothing says the record was ignored. The orchestrator rules whether the threat row's "and says so" needs a line of its own.
- Cap headroom: 11 added lines outside `tests/` remain under the 500 cap. A revise round that adds more forces the Validation clause's second split.
- Item 5: neither checker is in this PR (T704 owns them).

## Results

- `test_orchestrator_tools.py`: 25 tests OK.
- `test_regime_counters.py`: 27 tests OK.
- shellcheck 0.11.0, shfmt 3.14.1 (`-i 4 -sr`), ruff format and ruff check: clean.
- Mutation proofs: 22 mutants, 22 failures, every file restored (validation §2, §3).
- Size: 12 files outside `.orchestration/`; added lines outside and under `tests/`: 489 and 356 (caps 500 and 1000).
- The live `bus-read.sh` read lists this task open, with its skipped rows counted (§4).

## Not done, or outside scope

- PR-B: `acceptance-front-matter.py`, `orch-gate.sh` and their tests, after #329 merges.
- `orch-audit.sh` has no test of its own; its row is residual and item 2 names none.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` in the main checkout printed `9ac653b5-177d-4119-b321-4f98b0e2a802`.

cost: n/a

## Revise round (`3544d195`)

The orchestrator's revise of 2026-10-13T15:45:08Z (head `9ad0c150`, the update-branch merge of `73f56c15` into this branch) names two P1 findings to fix and four P2 findings to leave. The branch was reset to `origin/tools/orchestrator-scripts-2` at `9ad0c150` first (validation §5).

| Row | Finding | Disposition | Closing test |
|---|---|---|---|
| Bot 4260535901, local P1 | `dispatch.sh`: the `task_file=`/`task_sha256=` check matched a literal `AGMSG-TASK ` prefix, so a tab-separated TASK without them reached `agmsg-dispatch` | `fixed:3544d195`. The kind is the first parsed token (`${tokens[0]} == AGMSG-TASK`), from the same split item 4's grammar validates | `test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields` (R1) |
| local P1 | `fill_sweep.py`: every `annotation` and `status` item got a not-applicable, warning and failure annotations and non-success statuses included | `fixed:3544d195`. `NEUTRAL = {"annotation": "notice", "status": "success"}`: only those levels get their rule; every other level is a gap, so nothing is written | `test_fill_sweep_fills_only_notice_annotations_and_success_statuses` (R2, R3) |
| Bot 4260535916, 4260535924, the local pair | `boundary.sh` and `ff-main.sh` with deleted paths (P2) | no change in this PR: advisory, owned by orchestrator-tools-followup-a01 (the revise's ruling) | none |

- Tests: `test_orchestrator_tools.py` 27 OK, `test_regime_counters.py` 27 OK; shellcheck, shfmt, ruff format and ruff check clean; mutants R1 to R3 killed by assertions (validation §5).
- Size after the round: 12 files outside `.orchestration/`; 494 added lines outside `tests/` and 387 under it (caps 500 and 1000). Six lines of headroom remain.
- No Bot wait for this round, as the revise says. This is the only round (INV-6).
