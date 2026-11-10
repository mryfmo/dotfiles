# U222d round 4 of U222: ledger-row.py makes no file but the ledger, locks the ledger's own descriptor and appends one line under it

GOAL
The round-3 audit of PR 740 (verdicts/U222-238f0f55.md, class store-shape) found that the lock file `.ledger.lock` round 3 introduced stays in the store after every write, and the store's own walks (records-sync.sh's derived listing, regime-store-move's walk) refuse a name beginning with `.`, so the first write after the move would stop every records sync. Rounds 2 and 3 each fixed the write by a whole-file replace with helper files in the store, and each helper file was the next round's P1 (the mechanism-change row of the decisions, 2026-11-08, form remove). Round 4 removes the premise: the writer makes no file but the ledger. (1) The lock is the ledger's own descriptor: `os.open(ledger, O_RDWR | O_APPEND)` then `fcntl.flock(LOCK_EX | LOCK_NB)` tried every 0.1 s for `--lock-wait` seconds (default 30), a refusal naming the ledger on expiry; advisory, so the readers (`ledger.py`, `pr-merge.sh`), which open the file without a lock, are unaffected. (2) Under the lock: `os.fstat` for the length `n0`, the whole text read through the same descriptor (`os.pread(fd, n0, 0)`, looped until `n0` bytes), the row composed and checked, the text plus the line parsed through `ledger.parse_ledger`, then one `os.write(fd, line)` (O_APPEND puts it at the end), its count compared with the line's length, `os.fsync`, close (which releases the lock). (3) A write that fails or returns short truncates the file back to `n0` (`os.ftruncate(fd, n0)`) and exits 1 naming the ledger and the error; a truncate that fails is named too (`the ledger <path> may hold a partial last line: <error>`), exit 1. (4) Every `OSError` of the sequence (open, flock, fstat, pread, write, fsync, ftruncate, close) is one stderr line and exit 2 before the write (a read refusal, standing order 21) or exit 1 from the write on, never a traceback. (5) Every element of `sys.argv` passes the control-character check before argparse runs (the P3: `--lock-wait` escaped it). (6) The temporary, the lock file, `os.replace`, the mode copy and the lock-file rule go, with their tests; the round-2 and round-3 guarantees that remain (strict UTF-8 arguments, the store's file rule for the ledger, the verdict file and the findings file, no bytecode, the concurrency property) keep their tests.

SCOPE
The same branch `feat/ledger-row-writer` and PR 740; the tree `/private/tmp/dotfiles-wt-U222/U222` at 238f0f55 (clean). May write: `scripts/orchestrator/ledger-row.py` and its copy `home/dot_local/bin/common/executable_ledger-row.py`, `tests/unit/test_ledger_row.py`, the pin through `scripts/generate-agent-configs.py` and whatever it regenerates, the README's ledger-row paragraph (the write form in two sentences), and the PR body. Non-goals: `ledger.py` and every other lever; no change to the readers.

CONTEXT
`scripts/orchestrator/ledger-row.py` at 238f0f55: the lock function (`.ledger.lock`, `LOCK_NAME`, `LOCK_WAIT`, `--lock-wait`), the write function (the temporary, fsync, `os.replace`, the `finally` cleanup and its diagnostic), `cell_check` and `main`. `verdicts/U222-238f0f55.md` (the four findings and the probes: the offline records-sync.sh listing after one write; the 0644 temporary under umask 022; an injected fstat EIO; tab, newline and carriage return inside `--lock-wait`). `verdicts/U222-0fc41a81.md` line 3 (the concurrency probe round 4 must still pass: twelve concurrent calls on a 4,000-row ledger keep all twelve rows). `tests/unit/test_ledger_row.py` at 238f0f55 (27 tests; the round-2 and round-3 ones named `test_r2*` and `test_r3*`). `records-sync.sh`'s derived listing rule (a name beginning with `.` refused) and `regime-store-move`'s `check_entry`. `preferences.md` standing orders 21, 33, 45, 46, 49.

DATA SHAPE
One file, the ledger; one descriptor, opened O_RDWR | O_APPEND, the lock and the read and the write all through it; one write call; one recovery, truncate to the recorded length; one argument rule applied to every argv element before parsing.

CHANGE
1. Tests first, red at 238f0f55, in `test_ledger_row.py`: (a) after a successful write the store holds exactly the entries it held before plus nothing (no `.ledger.lock`, no temporary): the store listing before and after differ in no name, and the ledger's mode and owner are unchanged; (b) the round-3 concurrency test (twelve concurrent calls, 4,012 rows, each once) kept and green; (c) a held advisory lock on the ledger (a test subprocess holding `LOCK_EX` on `ledger.tsv`) makes the lever refuse after its wait naming the ledger, the ledger unchanged, and `ledger.py <store> verdict ...` run by the test during the hold still reads the ledger (the readers are unaffected); (d) an injected short or failing write (a `RLIMIT_FSIZE` of `n0` plus a few bytes, the round-2 fixture's form) exits 1 naming the ledger, and the ledger is byte-identical to before (the truncate ran); (e) an injected failure of fstat or pread (through `runpy` with the function replaced, the round-3 form) is one stderr line, exit 2, the ledger unchanged; (f) a tab, a newline and a carriage return inside `--lock-wait` each refuse by the argument rule, exit 2, nothing written; (g) the round-2 and round-3 tests of the temporary, the lock file and the mode copy removed; every other test green.
2. The lever per DATA SHAPE and GOAL 1 to 6.
3. The pin regenerated, cmp 0; the README paragraph's write sentences.
4. The body's Round 4 section and Verification; `Program-Unit: regime-cutover/U222` once at the end.

ACCEPTANCE
1. Tests (a) to (g) named with red lines at 238f0f55 and green lines at the head; the removed tests named. 2. `python -m unittest tests.unit.test_ledger_row tests.unit.test_ledger tests.unit.test_lever_self_check tests.unit.test_generate_agent_configs tests.unit.test_lint_comparisons` OK with counts. 3. `run-on-lint-files.sh` 0, `lint-comparisons --changed` 0, `make render-check` 0, `make validate-agent-assets` 0, cmp 0, the pin equal to `shasum -a 256` of the source, pasted. 4. `git diff --stat 238f0f55 HEAD` pasted with only the allowed paths. 5. `grep -c -E 'ledger\.lock|os\.replace|\.tmp' scripts/orchestrator/ledger-row.py` prints 0 and `grep -c 'ftruncate' scripts/orchestrator/ledger-row.py` 1 or more, pasted.

VERIFY
ACCEPTANCE pasted into the body and the report; the coordinator fetches the head by path, pushes, and the one audit, the sweep and CI follow.

CLOSURE
remove

TRUST
TRUST: the unit trusts what U222 trusts (`ledger.py` as the one grammar, the manifest's pin, the verdict file's last line, the levers' receipts), the advisory flock on the ledger's descriptor as the serialization every writer shares and no reader needs, and the kernel's append and truncate on one descriptor as the write and its recovery; it makes no file but the ledger and does not read the pull request, the network or any seat.

TIMEBOX
40 minutes.

FORBIDDEN
As U222's, with scratch under `/tmp/u222d/`; no file created anywhere under the store but the ledger itself; no mode change of any file; no change to the readers.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your worker repository. Your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U222d-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U222d-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 33, 35, 39, 44, 45, 46, 49); `verdicts/U222-238f0f55.md`; `verdicts/U222-0fc41a81.md`; the mechanism-change row of U222 in decisions.tsv; the U222, U222b and U222c briefs.
