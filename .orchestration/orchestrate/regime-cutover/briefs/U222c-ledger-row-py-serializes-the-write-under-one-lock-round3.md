# U222c round 3 of U222: ledger-row.py serializes read, check and replace under one lock, decodes its arguments strictly and names a failed cleanup

GOAL
The round-2 audit of PR 740 (verdicts/U222-0fc41a81.md, class lost-update) found one P1 and two P2 in `scripts/orchestrator/ledger-row.py`. (1) P1 :455: round 2 replaced the append with a whole-file temporary-and-rename write to close the partial-line risk, and that write reads the ledger, checks and writes back with no lock, so two concurrent writers lose each other's rows (the auditor's probe: 12 concurrent calls on a 4,000-row ledger kept four new rows; an interleaved push erased an incorrect audit row and left an older correct verdict as the newest). The coordinator does run two levers at once (standing order 45), so the sequence read, check, write, replace must be serial per store: one exclusive lock, `fcntl.flock(LOCK_EX)` on a lock file `<store>/.ledger.lock` opened (created 0600 when absent) before the ledger is read and held until `os.replace` has returned; the lock file itself is held to the store's file rule (no link, a regular file of this user); a lock that cannot be taken within 30 seconds (a non-blocking try in a loop) is a refusal naming the lock file (standing order 21). (2) P2 :456: an argument holding a byte that is not UTF-8 passes the cell check (Python decodes argv with surrogateescape) and raises `UnicodeEncodeError` outside the `OSError` handler, so a traceback prints and the temporary stays; every argument is encoded back to UTF-8 strictly at the start of `main` and a failure is a refusal naming the argument, before anything is read; and the write's cleanup runs under `try/finally` for every exception, not `OSError` alone. (3) P2 :460: a failed unlink of the temporary is suppressed and the diagnostic says removed; the unlink's own failure is named in the diagnostic (`the temporary <path> could not be removed: <error>`) and the exit stays 1.

SCOPE
The same branch `feat/ledger-row-writer` and PR 740; the tree `/private/tmp/dotfiles-wt-U222/U222` at 0fc41a81 (clean). May write: `scripts/orchestrator/ledger-row.py` and its copy `home/dot_local/bin/common/executable_ledger-row.py`, `tests/unit/test_ledger_row.py`, the pin through `scripts/generate-agent-configs.py` and whatever it regenerates, the README's ledger-row paragraph (the lock named in one sentence), and the PR body. Non-goals: `ledger.py` and every other lever.

CONTEXT
`scripts/orchestrator/ledger-row.py` at 0fc41a81: the write function (:440 to :465: the temporary, fsync, `os.replace`, the `OSError` handler and the unlink), `cell_check` and `main`'s argument handling, the store's file rule (`under_store` or its name there). `verdicts/U222-0fc41a81.md` lines 3 to 5 and 14 to 18 (the probes: 48 concurrent calls on an empty ledger, 12 on a 4,000-row one, a controlled interleaving, a raw non-UTF-8 argument, an injected fsync EIO then unlink EACCES). `tests/unit/test_ledger_row.py` at 0fc41a81 (17 tests; the round-2 fixture's failing-write injection, which the round-3 cleanup test extends). Python's `fcntl.flock`, `os.fsencode`, `sys.argv` surrogateescape. `preferences.md` standing orders 21, 45, 46, 49.

DATA SHAPE
One critical section per store: lock file taken exclusively, ledger read, row checked, text parsed, temporary written and fsynced, `os.replace`, lock released (by the file's close); one argument rule: every argv element must round-trip through strict UTF-8 before the first read; one cleanup rule: the temporary's removal is attempted on every exception and its own failure is named.

CHANGE
1. Tests first, red at 0fc41a81, in `test_ledger_row.py`: (a) twelve concurrent `pushed` calls (a `concurrent.futures` pool of subprocesses) against a ledger of 4,000 rows all exit 0 and the ledger holds exactly 4,012 rows afterwards, each new row present once (the auditor's probe); (b) a lock holder (a test subprocess holding `LOCK_EX` on `.ledger.lock` for the test's duration) makes the lever refuse after its wait naming the lock file, exit 2, the ledger unchanged (the wait shortened by an environment variable or a `--lock-wait` option the test alone sets, named in the docstring); (c) a `.ledger.lock` that is a symlink is refused by the file rule; (d) a raw non-UTF-8 byte in `--what` (passed as bytes through `subprocess` with `errors=surrogateescape`) is a refusal naming the argument, exit 2, one stderr line, no temporary, the ledger unchanged; (e) an injected fsync failure followed by an unlink failure (the round-2 fixture's form) exits 1 with the diagnostic naming the temporary as not removed and its error, and the ledger unchanged.
2. The lever per DATA SHAPE.
3. The pin regenerated, cmp 0; one README sentence on the lock.
4. The body's Round 3 section and Verification; `Program-Unit: regime-cutover/U222` once at the end.

ACCEPTANCE
1. Tests (a) to (e) named with red lines at 0fc41a81 and green lines at the head. 2. `python -m unittest tests.unit.test_ledger_row tests.unit.test_ledger tests.unit.test_lever_self_check tests.unit.test_generate_agent_configs tests.unit.test_lint_comparisons` OK with counts. 3. `run-on-lint-files.sh` 0, `lint-comparisons --changed` 0, `make render-check` 0, `make validate-agent-assets` 0, cmp 0, the pin equal to `shasum -a 256` of the source, pasted. 4. `git diff --stat 0fc41a81 HEAD` pasted with only the allowed paths. 5. `grep -c 'LOCK_EX' scripts/orchestrator/ledger-row.py` 1 or more, `grep -c 'except OSError' scripts/orchestrator/ledger-row.py` as the lever needs with the cleanup under `finally`, pasted with the line.

VERIFY
ACCEPTANCE pasted into the body and the report; the coordinator fetches the head by path, pushes, and the one audit, the sweep and CI follow.

CLOSURE
parser-module

TRUST
TRUST: the unit trusts what U222 and U222b trust, and `fcntl.flock` on one lock file in the store as the serialization every writer of this ledger shares (the coordinator is the only writer, running one or more levers at once); it does not read the pull request, the network or any seat.

TIMEBOX
40 minutes.

FORBIDDEN
As U222's, with scratch under `/tmp/u222c/`; no lock taken on `ledger.tsv` itself (a reader opens it without the lock); no write outside the store but the scratch directory.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your worker repository. Your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U222c-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U222c-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 35, 39, 44, 45, 46, 49); `verdicts/U222-0fc41a81.md`; the U222 and U222b briefs.
