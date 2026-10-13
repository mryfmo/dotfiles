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
