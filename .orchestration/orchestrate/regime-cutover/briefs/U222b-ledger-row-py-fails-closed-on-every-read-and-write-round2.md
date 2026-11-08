# U222b round 2 of U222: ledger-row.py fails closed on every read and write it makes

GOAL
The round-1 audit of PR 740 (verdicts/U222-9187830e.md, correct, seven findings filed below the gate's weight) named five P2 and two P3 in `scripts/orchestrator/ledger-row.py`, each a place where the writer's own contract (one line appended, the store confinement, the gate-compatible evidence, a failed read never an absence) does not hold. (1) :434 a write that fails mid-way (a size limit, a full disk) leaves a partial line, so every reader then refuses the ledger as malformed; the write becomes atomic: the whole new text written to a temporary file in the store's directory, fsynced, renamed over `ledger.tsv`, so a failed write leaves the old file whole. (2) :254 and :280 the findings file and the verdict file are checked for a symlink at the last component alone; the resolved file (`os.path.realpath`) must lie under the resolved store and no component may be a link (`os.lstat` on each). (3) :103 the findings-file pattern accepts `;` though the sweep reader splits the evidence on `;`; the pattern allows `[A-Za-z0-9._-]` components only. (4) :118 `os.path.isfile` on the manifest reads a failed stat as absence (standing order 21); the manifest is opened and a failure other than ENOENT is a refusal naming the file and the error, ENOENT alone falls through to the checkout's manifest. (5) :95 the carried regex uses Python's `\s`, which accepts a non-breaking space the gate's C-locale class rejects; the separator class is the gate's literal set (space, tab, `;`, `,`, `.`, `)`, end) with `re.ASCII`. (6) :396 the store argument is exempt from the control-character check; it is not. (7) :80 the `ledger.py` import under `python3 -I -S` writes `__pycache__` beside the lever; `sys.dont_write_bytecode = True` before the import. Each fix carries its red test.
(8) CI at 9187830e is red in one test on all four legs, `test_lint_comparisons.test_the_changed_files_are_clean_against_the_baseline`: rule R4 (a path compared by its string form) at `ledger-row.py:155` and `:275` and the installed copy. Line 155 compares a chain of YAML keys whose constant is named `ASSET_PATH`; it is a key chain, not a path, and is renamed `ASSET_KEYS`. Line 275 compares the verdict-file argument with the text `verdicts/<unit>-<sha8>.md` on purpose (the file is named by the row's unit and the head's first 8, the 12:39:21Z lesson, and a resolved comparison would admit another name that resolves to it); it keeps the text comparison and carries the lint's allow annotation in its Python form with that reason. The worker's local `lint-comparisons --changed` passed because its tree had no baseline ref; run it as CI does (the test module itself, `python -m unittest tests.unit.test_lint_comparisons`).

SCOPE
The same branch `feat/ledger-row-writer` and PR 740 (if PR 740 has merged, a new branch `fix/ledger-row-fails-closed` from origin/main and a new pull request). May write: `scripts/orchestrator/ledger-row.py` and its copy `home/dot_local/bin/common/executable_ledger-row.py`, `tests/unit/test_ledger_row.py`, the pin through `scripts/generate-agent-configs.py` and whatever it regenerates, the README's ledger-row paragraph (the atomic write named), and the PR body. Non-goals: `ledger.py` and every other lever.

CONTEXT
`scripts/orchestrator/ledger-row.py` at 9187830e: the lines the verdict names (:80, :95, :103, :118, :254, :280, :396, :434); `verdicts/U222-9187830e.md` lines 3 to 9 (the seven findings and the auditor's probes: a size limit through `resource.setrlimit(RLIMIT_FSIZE)`, symlinked parent directories, a `;` in the findings directory name, an unreadable `~/.agents`, a non-breaking space before `carried`). `tests/unit/test_ledger_row.py`: the fixture and the refusal test (b) with its subtests. `pr-merge.sh`'s carried regex and `sweep_pin_probe`. `preferences.md` standing orders 21, 46, 49.

DATA SHAPE
One write: the whole ledger text plus the new line to `<store>/.ledger.tsv.<pid>.tmp`, fsync, `os.replace` over `ledger.tsv`, the temporary removed on any failure; one path rule for every file the lever reads under the store: physical path under the physical store, no link in any component, a regular file; one separator class for the carried digest, the gate's own; one manifest read that distinguishes ENOENT from every other error.

CHANGE
1. Tests first, red at 9187830e, in `test_ledger_row.py`: (a) a write that fails (a `RLIMIT_FSIZE` of the current size plus 8 bytes, as the auditor did) exits 1 naming the file and leaves `ledger.tsv` byte-identical, no temporary left; (b) a findings path and a verdict path through a symlinked parent directory outside the store each refuse naming the component; (c) a findings directory holding `;` refuses by the pattern; (d) an unreadable manifest directory (mode 000 under a scratch HOME) refuses naming it, and an absent one falls through to the checkout manifest (the existing path); (e) a non-breaking space before `carried` in the line refuses; (f) a store path holding a newline refuses; (g) after a run under `python3 -I -S` no `__pycache__` exists beside the lever.
2. The lever per DATA SHAPE.
3. The pin regenerated, cmp 0; the README paragraph's one sentence on the atomic write.
4. The body's Round 2 section and Verification; `Program-Unit: regime-cutover/U222` once at the end (standing order 24: the fix round writes the parent id).

ACCEPTANCE
1. Tests (a) to (g) named with red lines at 9187830e and green lines at the head; `test_lint_comparisons` red at 9187830e (R4 at :155 and :275) and green at the head. 2. `python -m unittest tests.unit.test_ledger_row tests.unit.test_ledger tests.unit.test_lever_self_check tests.unit.test_generate_agent_configs tests.unit.test_lint_comparisons` OK with counts (the lint module is CI's red at 9187830e; it must pass in the tree with origin/main fetched as its baseline). 3. `run-on-lint-files.sh` 0, `lint-comparisons --changed` 0, `make render-check` 0, `make validate-agent-assets` 0, cmp 0, the pin equal to `shasum -a 256` of the source, pasted. 4. `git diff --stat 9187830e HEAD` pasted with only the allowed paths. 5. `grep -c 'os.replace' scripts/orchestrator/ledger-row.py` 1 or more and `grep -c 'isfile' scripts/orchestrator/ledger-row.py` 0, pasted.

VERIFY
ACCEPTANCE pasted into the body and the report; the coordinator fetches the head by path, pushes, and the one audit, the sweep and CI follow.

CLOSURE
parser-module

TRUST
TRUST: the unit trusts what U222 trusts (`ledger.py` as the one grammar, the manifest's pin, the verdict file's last line, the levers' receipts) and two more things: the temporary-and-rename write as the one atomic whole-file replace the operating system offers, and the resolved-and-lstat rule for every file under the store as the rule the other levers already apply; it does not read the pull request, the network or any seat.

TIMEBOX
40 minutes.

FORBIDDEN
As U222's, with scratch under `/tmp/u222b/`.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your worker repository. Your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U222b-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U222b-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 22, 24, 35, 44, 46, 49); `verdicts/U222-9187830e.md`; the U222 brief.
