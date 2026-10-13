# Report: dotfiles-T128-orchestrator-tools-a01

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `tools/orchestrator-scripts` from `origin/main` `480aabc0`.
- PR #328's branch `regime/playbook-rules` was committed and pushed at `2276a365` before the switch and is untouched (validation §1).
- Task file sha256 `aaf02188…` matches the TASK's `task_sha256`. It is copied byte-identical in `b0cba1a7`. The premises hold, and the attached inputs under `…-a01-input/` are untouched (§1).

## Commit `8ea05883`

New scripts under `scripts/orchestrator/` (all mode 100755, shdoc headers in English, no home-directory literal; the repository root comes from `git rev-parse --show-toplevel`, and the agmsg scripts directory from `AGMSG_SCRIPTS`, default `$HOME/.agents/skills/agmsg/scripts`):

- `dispatch.sh <team> <from> <to> <pane> <line-file>`
  - Reads exactly one line.
  - Recomputes every `<name>_sha256=` from the file its `<name>_file=` or `<name>=` sibling names: `task_file=`, `design=`, `amended_task=`, and any later pair of the same form.
  - Exits 1 naming the field on a mismatch, a missing sibling, a missing file or a non-hex value. Otherwise it `exec`s `agmsg-dispatch` with the line as one argument.
  - It accepts AGMSG-TASK, AGMSG-ACCEPTANCE and also AGMSG-PING lines. Item 1 names two kinds, but the task's Completion says the orchestrator dispatches only through this script after the merge, and a PING is a dispatch (the a04 step-6 sentence lists TASK, ACCEPTANCE, PING). A PING carries no sha field, so the check passes through.
  - It does not write a `dispatch:` line into the acceptance record; that is not in this task.
- `three-repeat.sh <class>`
  - Exits 2 unless the class is `^[a-z0-9-]+$`.
  - The records search is `/usr/bin/grep -rl '^classes:.*<class>'` over `.orchestration/learning/mistakes/`. It is anchored and substring-based because that is the gate's own match (gate-evidence-a03 item 2: "a line that begins with `classes:` contains `<class>`"), so the `search:` line equals the set the gate recomputes. Output: `search: <class> -> <basenames, LC_ALL=C sorted, ", "-joined, or none>`.
  - The CompactionDB search runs as `uv run --no-project .claude/hooks/contextdb_cli.py memory search <class>` from the root with the class as one argument, and prints `compactiondb: <class> -> <n> matches`.
- `bus-read.sh <team> [<task id>]`
  - The read: `history.sh <team> "" <limit>`, the documented positional form, with limit `BUS_READ_LIMIT` (default 100000). A read that reaches the limit exits 1.
  - Not `history.sh --limit 1000`, the form item 1 cites. That form is complete only by accident: `--limit` lands in the agent slot and `storage_history` then parses a non-numeric limit as none (PR #328 a04 report, §2 there). And 1000 is close to the live team's size: 813 messages in the §6 read.
  - The state rule, from the live statuses (§6): an AGMSG-TASK (amendments included) or an AGMSG-ACCEPTANCE `status=revise` opens a task. An AGMSG-RESULT, or an ACCEPTANCE `accepted`, `withdrawn`, `superseded`, `reset` or `parked`, closes it. `under_review` and any unknown status change nothing, so a task is never hidden. Order is the message's position in the history, not its timestamp. Without `reset` and `parked`, the first live run reported three tasks of 2026-10-10 as open, 3168 minutes silent; with them, the live run lists exactly the three tasks in flight.
  - Output per open task: `open: task=<id> seat=<to of the last opener> last_event=<the task's latest message in either direction> minutes=<n> silent=<yes at >= 30|no>`, else `open: none`. Minutes come from jq's `now` and `fromdateiso8601`, so BSD and GNU `date` never differ.

`scripts/regime-counters.sh`, the S1 line only:
- When `.orchestration/acceptance/<task>.md` starts with a `---` block that is a JSON object with a `ledger` array, jq slices and parses it (`jq -Rs`, `fromjson` inside `try`), and every class with three or more rows prints `S1: class=<slug> count=<n> source=record`. A class that is not `[a-z0-9-]` prints `class=invalid`, so it is not silently dropped.
- Without such a record (no file, or a prose record: every acceptance record on `main` today), the Bot-title grouping prints `S1: candidate class=unclassified count=<n> title=<the first title of the group as a JSON string> source=<s>`.
- The task id must match `^[A-Za-z0-9][A-Za-z0-9._-]*$` before it is used in the record path.
- Still no S1 lines under `--history-only`, as the header and `test_history_only_never_calls_gh` say. The counting logic is untouched.

## Tests

- `tests/unit/test_orchestrator_tools.py`, 7 tests, including the closed row `test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file`. `agmsg-dispatch`, `shasum` and `uv` are stubbed on PATH and `history.sh` in `AGMSG_SCRIPTS`; each stub records its argv NUL-separated. A temporary `git init` repository is the root; bus-read fixtures are timed relative to now, and minutes are asserted within ±1.
- `tests/unit/test_regime_counters.py`: line 451's expectation updated; `test_s1_reads_the_ledger_classes_of_the_acceptance_record` (a copied script in a temporary root, a JSON record with `bookkeeping` at three, `sources` at two, an invalid class at three); `test_s1_quotes_a_title_with_shell_metacharacters` (backticks and `$()`, no record).
- Results: 7 OK, 26 OK, and the boundary-checker and docs modules 51 OK (§2, §3). shellcheck 0.11.0 is clean on the four scripts, and ruff format is clean (§4).
- Each guard fails its test when broken: 14 mutants, 14 failures (§5). They include the `--limit` flag form, an unanchored records match, a word-split line, `withdrawn` not closing, and the title not JSON-quoted.

## Size (§7)

6 files outside `.orchestration/`; 204 added lines outside `tests/` (cap 500); 219 under `tests/` (cap 1000). One PR.

## Not done, or outside scope

- The two checkers (T704) and the other nine scripts (`dotfiles-T128-orchestrator-tools-a02`) are out, as item 4 says. Nothing outside `allowed_files` changed.
- The SKILL's step 10.4 sentence and the a04 rule text are PR #328's. This PR makes a04's "Once plan 007 T718 lands" clauses true for `three-repeat.sh`, `bus-read.sh` and `dispatch.sh` as scripts.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CI and the Codex Bot

They run on the head that carries this evidence. The results are in the RESULT and in the main-checkout copy of this report.

## CompactionDB

`memory add` printed `c63b57e5-47d3-46c0-92e5-142680cda997` (§8).

cost: n/a

## Fix round 1 (`e6f2bdc0`, worker fix round 1 of at most 2)

The first head `61290da8` drew a CI failure and Codex Bot review 5497968688 (two P1s) (validation §9).

| Item | Finding | Disposition |
|---|---|---|
| CI `test (ubuntu-24.04, client)`, Run ShellCheck | SC2015 (info) at `three-repeat.sh:21`, `A && B \|\| C`. Ubuntu's apt shellcheck reports it; the local 0.11.0 does not. Fail-fast cancelled the other three jobs | `fixed:e6f2bdc0`: the guard is an `if` |
| 4253994697 (P1, `three-repeat.sh:38`) | the root came from the caller's directory, so run from a PR worktree the script executed that PR's `.claude/hooks/contextdb_cli.py` on the orchestrator host | `fixed:e6f2bdc0`: `three-repeat.sh`, and `dispatch.sh` for the same reason (it hashes task files by relative path), take the root of the checkout they live in, `git -C <script dir> rev-parse --show-toplevel`. Running the main checkout's script runs the main checkout's CLI whatever the cwd; running a PR's copy of the script is already running PR code, so no new boundary is crossed. `test_scripts_read_and_run_their_own_checkout_never_the_callers` runs both scripts from a foreign git checkout and asserts the records, the CLI's cwd and the hashed file are the script's own; each script put back to the caller root fails it (mutants O1, O2) |
| 4253994704 (P1, task.md:19) | the first threat row (`scripts/orchestrator/*`, three scripts) closes on one test that covers only `dispatch.sh` | not fixable by the worker: the row is in the task file, whose copy must stay byte-identical (threat row 5), and changing it is an amendment (the T703 amendment rule). Proposed split, one `closed` row per script: `dispatch.sh` → `tests/unit/test_orchestrator_tools.py::test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file`; `three-repeat.sh` → `…::test_scripts_read_and_run_their_own_checkout_never_the_callers` (with `…::test_three_repeat_refuses_a_class_that_is_not_a_slug` for the slug); `bus-read.sh` → `…::test_bus_read_refuses_a_read_that_reaches_its_limit`. Every selector exists in this head |

After the round, the new module runs 8 tests, OK; the counters module 26, OK; shellcheck is clean; all 16 mutants fail (§9). Size: 6 files outside `.orchestration/`; 207 added lines outside `tests/`; 240 under `tests/`.

## Fix round 2 (`17d3735d`, worker fix round 2 of 2)

On head `4843ccb6` (validation §10):
- **CI:** all 12 check runs succeeded after `gh run rerun --failed` of a snap store timeout (`api.snapcraft.io` HTTP 408 in `public-bootstrap (ubuntu-24.04, client)`).
- **Bot:** the review arrived at 02:27:54Z, two minutes after the 15-minute window, which had closed as `bot: none` even though `@codex review` went out at 02:21:19Z. It is dispositioned all the same:

| Thread | Finding | Disposition |
|---|---|---|
| 4254107304 (P2, `dispatch.sh:34`) | `$( )` dropped every trailing newline, so the message followed by a blank line passed as one line | `fixed:17d3735d`: the read keeps a sentinel and strips exactly one final newline; a new `test_dispatch_refuses_malformed_lines` case; the old read put back fails it (mutant N1) |
| 4254107312 (P1, `dispatch.sh:77`) | once PR #328's a04 rule text lands, every dispatch is recorded under the acceptance record's `dispatch:` key, but `dispatch.sh` takes no record path and only calls `agmsg-dispatch` | not fixed, the orchestrator's call: this task's item 1 specifies `dispatch.sh` as check-and-send, and nothing defines where a `dispatch:` key lives. The gate-evidence-a03 JSON block lists `format`, `task`, `head`, `pr`, `ledger`, `searches` and `audit_findings` and validates field by field, so an extra key written by a worker's guess could break the gate. The rule text and this script disagree (a04 item 1, "dispatch.sh writes the line"), which the first report section already notes. Options: an amendment that adds a record-path argument and a defined place for `dispatch:` (prose line or JSON field), or moving it to `dotfiles-T128-orchestrator-tools-a02` |

Unchanged in this round: 8 tests OK, shellcheck clean (§10).

A slip without effect: while checking a file without a final newline, I ran the real `scripts/orchestrator/dispatch.sh a b c d <file>` once, with the host's `agmsg-dispatch` on PATH instead of the stub. `agmsg-dispatch` resolves the pane before it sends anything, so it exited at "pane not found or unavailable: d". `team-list.sh` still lists only `dotfiles-conformance`: no message was sent and no team was created.

## Amendment 1 (TASK 03:13:58Z, sha256 `91eb1ebe…`; commits `2dddff84`, `0a5ae302`)

The amendment answers threads 4253994704, 4254107312 and 4254163604 and confirms `e6f2bdc0` for 4253994697. The task copy was recommitted byte-identical (validation §12).

- **`dispatch.sh`**
  - An AGMSG-TASK line without `task_file=` or `task_sha256=` exits 1 naming the missing field, and nothing is sent (thread 4254163604).
  - It takes an optional sixth argument, the acceptance record (thread 4254107312). The record's JSON block is parsed before the send, so a malformed record means no send. After `agmsg-dispatch`, the script finds the sent line in `history.sh <team> <to> 200` and appends `<line> read_at=read` (marker `○`) or `read_at=unread` (marker `●`) to the block's `dispatch` list. It writes with Python's standard json (duplicate keys and NaN refused, `sort_keys`, `indent=2`, non-ASCII kept) and keeps the prose byte for byte. A prose-only or missing record gets a block holding only `dispatch`.
  - The read state is the marker. `history.sh` prints no read_at time, and `agmsg-dispatch` polls `read_at` without printing it; the orchestrator chose that option (A) in its PONG of 03:16Z, and messages.db is never read.
  - When `agmsg-dispatch` exits non-zero (unread at its timeout), the line is still recorded as unread and the script exits with that status. If the line is not on the bus at all, the record is left unchanged and the script exits 1.
  - New host binary: `python3 -I` (standard library only), which the amendment's "standard library's json" implies.
- **`three-repeat.sh`**: it already resolved its root from its own checkout (`e6f2bdc0`). It now also passes the CLI to `uv` by its absolute path there, which the new closed-row test asserts.
- **Tests** carry the four closed-row names. Two-line and blank-line files move into the new TASK test, and the ACCEPTANCE case for a missing `amended_task=` remains. The new record test loads the block as the gate's contract says (standard json, duplicate keys and NaN refused, since the gate's loader is not on `main`) and covers both markers, a prose-only record and a duplicate key.
- **Results** (§12): 9 tests OK; 26 + 51 neighbouring tests OK; shellcheck clean; 23 mutants, 23 failures. The new mutants put back the unbound TASK, skip the pre-send check, invert the marker, drop the prose, accept duplicate keys, use the caller root, or pass a relative CLI path.
