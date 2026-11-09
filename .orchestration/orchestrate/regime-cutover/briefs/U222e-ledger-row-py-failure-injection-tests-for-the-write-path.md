# U222e tests wave for U222: the write path's failure injections are committed, the held-lock helper closes its pipe, and an option name is escaped in the one-line refusal

GOAL
The round-4 audit of PR 740 (verdicts/U222-60415f10.md, correct) filed one P2 and two P3 that the merge left as residual rows (dispositions 2026-11-08T17:19:09Z, unit U222e). (1) P2 `tests/unit/test_ledger_row.py:1207` (weight 20): the writer's `append_line` has four failure paths the auditor injected by hand and found right (an `lseek` failure and a `fsync` failure each exit 1 with the ledger byte-identical; a `close` failure exits 1 naming the appended row; a short write followed by a failing `ftruncate` exits 1 naming the ledger as possibly holding a partial last line), and none of the four has a committed test, against standing order 21's rule that every safety decision carries its injection test. (2) P3 `:1126`: the held-lock helper kills and waits for its subprocess without closing the pipe it opened, so every run prints a `ResourceWarning`. (3) P3 `scripts/orchestrator/ledger-row.py:482`: the refusal that names an offending option interpolates the option's text unescaped, so an option spelled with a newline prints two stderr lines against the one-line contract; the name is written in `repr` form (the escapes visible, one line). The lever's behaviour changes in that one message alone.

SCOPE
A new branch `chore/ledger-row-failure-injection-tests` from origin/main 1f9f31f9; the tree is the worker repository `/private/tmp/dotfiles-wt-U222e/U222e` (clean, made by worker-worktree.sh). May write: `tests/unit/test_ledger_row.py`, `scripts/orchestrator/ledger-row.py` and its copy `home/dot_local/bin/common/executable_ledger-row.py` (the one message at :482 only), the pin through `scripts/generate-agent-configs.py` (never by hand) and whatever it regenerates, and the PR body `/tmp/dotfiles-wt/U222e-pr-body.md`. Non-goals: every other line of the lever; `ledger.py`; every other lever and test module.

CONTEXT
`scripts/orchestrator/ledger-row.py` at 1f9f31f9: `append_line` (the `os.lseek`, `os.write`, `os.fsync`, `os.ftruncate`, `os.close` calls and the two failure texts), the refusal at :482. `tests/unit/test_ledger_row.py` at 1f9f31f9: the round-3 and round-4 injection tests that replace an `os` function in the interpreter and run the lever through `runpy` under `-I -S` (`test_r4e_an_injected_fstat_or_pread_failure_...`, the form to copy), the size-limit fixture (`test_r4d_...`), the held-lock helper around :1126 (`holder` and its `stdout`). `verdicts/U222-60415f10.md` lines 3 to 5 and 14 to 15 (the auditor's injections and their observed results). `preferences.md` standing orders 21, 46, 49.

DATA SHAPE
One injection form (the round-4 `runpy` form) applied to four more `os` functions; one subprocess helper that closes what it opens; one refusal text whose variable part is `repr`-escaped.

CHANGE
1. Tests first, in `test_ledger_row.py`: (a) an injected `os.lseek` failure exits 1, one stderr line naming the ledger, the ledger byte-identical; (b) an injected `os.fsync` failure the same; (c) an injected `os.close` failure after a successful write exits 1 with the diagnostic naming the appended row, and the row is in the ledger; (d) a short write (the size-limit fixture) followed by an injected `os.ftruncate` failure exits 1 with the text naming the ledger as possibly holding a partial last line; (e) the held-lock helper runs under `warnings.catch_warnings(record=True)` with `ResourceWarning` turned into an error, and passes; (f) an option spelled `--what` followed by a newline refuses with exactly one stderr line that holds the escaped name. Tests (a) to (d) and (f) assert behaviour the lever has at 1f9f31f9 except (f), which is red there (two lines); (e) is red there (the warning).
2. The helper closes its pipe; the refusal at :482 writes the option name in `repr` form.
3. The pin regenerated; `cmp` of the source and the copy 0.
4. Body at `/tmp/dotfiles-wt/U222e-pr-body.md`: Summary, Contract, Threat table (one row per changed path and one effect row: the lever's messages), Verification (ACCEPTANCE pasted), `Program-Unit: regime-cutover/U222` once at the end (standing order 24: the fix unit writes the parent id).

ACCEPTANCE
1. Tests (a) to (f) named; (e) and (f) red at 1f9f31f9 (`/tmp/u222e/red.txt`) and all six green at the head; the run under `python3 -W error::ResourceWarning -m unittest tests.unit.test_ledger_row` OK. 2. `python -m unittest tests.unit.test_ledger_row tests.unit.test_ledger tests.unit.test_lever_self_check tests.unit.test_generate_agent_configs tests.unit.test_lint_comparisons` OK with counts. 3. `run-on-lint-files.sh` 0, `lint-comparisons --changed` 0, `make render-check` 0, `make validate-agent-assets` 0, cmp 0, the pin equal to `shasum -a 256` of the source, pasted. 4. `git diff --stat 1f9f31f9 HEAD` pasted with only the allowed paths; the lever's diff is one message. 5. `grep -c 'ResourceWarning' tests/unit/test_ledger_row.py` 1 or more, pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator fetches the head by path, pushes the branch, opens the pull request, and the one audit, the sweep and CI follow.

CLOSURE
parser-module

TRUST
TRUST: the unit trusts the round-4 injection form (a replaced `os` function under `runpy`) as the way a kernel-level failure is made in a test, and the lever's four failure texts at 1f9f31f9 as the behaviour to pin; it changes the lever in one message and nothing else, and reads no pull request, network or seat.

TIMEBOX
35 minutes.

FORBIDDEN
No change to the lever beyond the one refusal text; no change to `ledger.py` or any other lever; no write to any checkout but the fixture's; no `# producer-status: allow` comment; no network; no push; no pin edited by hand; no rebase; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u222e/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/private/tmp/dotfiles-wt-U222e/U222e`. Your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U222e-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U222e-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 22, 24, 44, 46, 49); `verdicts/U222-60415f10.md`; the dispositions rows of 2026-11-08T17:19:09Z; the U222 and U222d briefs.
