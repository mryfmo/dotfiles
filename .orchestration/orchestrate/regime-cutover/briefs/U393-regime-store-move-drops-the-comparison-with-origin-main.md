# U393 regime-store-move drops the comparison with origin/main: the live store is ahead of main after every sync, so the equality gate can never pass

GOAL
`regime-store-move` (U221, merged 2642b6d6, deployed 12:58Z) refuses the move while the live store, masked, differs from origin/main at the published prefix (`a records sync is still due`). Measured 2026-11-08 after records sync 52 (PR 738, merged 41281b99): the sync's listing is taken when `records-sync.sh` builds its commit, and before that pull request can merge the coordinator writes its verdict row and file, its sweep row and set, and after the merge its merge row, so the live store holds nine paths main lacks or differs in (ledger.tsv, dispositions.tsv, units.tsv, decisions.tsv, the verdict file, the three files of the sweep set, the sweep brief) the moment the sync lands, and every later sync repeats it. The gate guards nothing the procedure does not already check: line 3 (`diff -r` and the count) proves the copy, line 7 (the post-move run) proves the checkout store clean against HEAD, and the next sync, listed from the derived store (U220), publishes whatever the live store held beyond main. Form `remove` (standing order 33): the fetch of origin's main, the listing of main, the masker run, the object comparison and the refusal go; the walk and its shape checks, the store root hold, the derived-store judgement, the procedure, the post-move report, the scratch directory and the read discipline stay. The pre-move verdict becomes `ready: <n> live files; the derived store is absent`.

SCOPE
A new branch `fix/regime-store-move-drops-the-sync-gate` from origin/main 41281b99; the tree is the worker repository `/private/tmp/dotfiles-wt-U393/U393` (clean, made by worker-worktree.sh). May write: `scripts/orchestrator/regime-store-move` and its copy `home/dot_local/bin/common/executable_regime-store-move`, `tests/unit/test_regime_store_move.py`, `scripts/orchestrator/README.md` (the regime-store-move paragraph and its Threat table rows), the pin through `scripts/generate-agent-configs.py` (never by hand) and whatever it regenerates, and the PR body `/tmp/dotfiles-wt/U393-pr-body.md`. Non-goals: every other lever and helper under `scripts/orchestrator/`; no move of the live store by the worker; no write to any checkout but the fixture's; no change to the procedure's seven lines but line 3's note.

CONTEXT
`scripts/orchestrator/regime-store-move` at 41281b99: lines 482 to 607 are the gate (the origin URL read and its https check, `git fetch` of `refs/heads/main` into the scratch repository, `rev-parse FETCH_HEAD`, `ls-tree -r -z` at the prefix, the `home/` entries read, the copy map, the masker under `uv run` with `UV_CACHE_DIR`, `hash-object` of every masked copy, the `differ` list, the refusal, the stderr line `equals the live store masked`, the `ready:` line and the note of line 3); the header's description, `@stdout`, `@stderr` and `@exitcode 1` name them. `tests/unit/test_regime_store_move.py`: the fixture's bare origin behind a git wrapper exists for the fetch; `self.ready`; test (b) `test_a_live_file_that_differs_from_main_masked_or_a_path_main_lacks_or_holds_alone_refuses`; the `uv` cache test; the stub matrix for `ls-tree`, `hash-object` and `cat-file`; `assert_nothing_written`. `scripts/orchestrator/README.md` lines 405 to 437. `tests/unit/test_lever_self_check.py` and `tests/unit/test_generate_agent_configs.py` hold the pin. `preferences.md` standing orders 21, 33, 46, 49.

DATA SHAPE
One lever with one mode and one argument and two verdicts: before the move `ready: <n> live files; the derived store is absent` then the seven lines (line 3's comment reads `expect no line from diff and the count <n>`), after it `moved: ...` as today. One stderr line before the move: `regime-store-move: live store <dir> (<n> files); derived store <dir> absent`. No git against anything but the checkout's `rev-parse` and `status`; no network; no scratch repository, no masker, no uv.

CHANGE
1. Tests first, red at 41281b99, in `test_regime_store_move.py`: (a) a live store ahead of origin/main (one row appended to the fixture's live `ledger.tsv` and one new file `verdicts/x.md` in the live store, main unchanged) prints the new `ready:` line and the seven lines byte-exact, the fixture's git wrapper logs no `fetch`, the scratch directory held no `main-listing` and no `copy-map` (the run's `TMPDIR` listing is read before removal through the fixture's `rm` stub, or the stub matrix's form), nothing is written, and the scratch directory is removed; (b) the pre-move run with the fixture's bare origin removed (no fetch source at all) prints the same `ready:` line and procedure; (c) the removed behaviour's tests go with it: test (b) of U221d, the uv-cache assertion of test (c), and the `ls-tree`, `hash-object` and `cat-file` rows of the stub matrix; every other injection (find, tr, wc, /usr/bin/stat, cat, git rev-parse, git status, rm) stays and keeps passing; (d) the post-move test is unchanged and green.
2. The lever: remove lines 482 to 607's gate as CONTEXT lists it, the `uv` and masker words, the https origin check and every variable only they read; print the new stderr line and the new verdict; pass the live count to `print_procedure` and make line 3's note `the count <n>`; update the header (description, `@stdout`, `@stderr`, `@exitcode 1` and `2`) so no sentence names the fetch, the masker, `ls-tree`, `hash-object` or the sync. Keep `read_listing` and `read_line` for every producer that remains.
3. `scripts/orchestrator/README.md`: the regime-store-move paragraph says the live store may be ahead of main and why (this GOAL's measurement, two sentences), the row `the reads of the checkout and the comparison with origin/main` becomes `the reads of the checkout` naming the tests that remain, and the procedure block's line 3 comment follows the lever.
4. `scripts/generate-agent-configs.py` regenerates the pin; `cmp scripts/orchestrator/regime-store-move home/dot_local/bin/common/executable_regime-store-move` exits 0.
5. Body at `/tmp/dotfiles-wt/U393-pr-body.md`: Summary, Contract, Threat table (one row per changed path: the lever, its copy, the test module, the README, the manifest and the generated outputs; one effect row: the move loses nothing, with the three controls that remain named), Verification (ACCEPTANCE pasted), `Program-Unit: regime-cutover/U393` once at the end.

ACCEPTANCE
1. Tests (a) to (d) named with their red lines at 41281b99 (`/tmp/u393/red.txt`) and green lines at the head; the removed tests named. 2. `python -m unittest tests.unit.test_regime_store_move tests.unit.test_lever_self_check tests.unit.test_generate_agent_configs tests.unit.test_scratch_git` OK with counts. 3. The producer-status lint `scripts/ci/producer-status-check.sh scripts/orchestrator/regime-store-move` exits 0 with no output, pasted; `run-on-lint-files.sh`, `lint-comparisons --changed`, `make render-check` and `make validate-agent-assets` 0; cmp 0; the pin equals `shasum -a 256` of the source. 4. `git diff --stat 41281b99 HEAD` pasted; only the lever, its copy, the test module, the README, the manifest and the generated outputs in it. 5. `grep -c -E 'still due|fetch|mask|hash-object|ls-tree|uv run' scripts/orchestrator/regime-store-move` prints 0 and `grep -c 'the derived store is absent' scripts/orchestrator/regime-store-move` prints 2 or more, pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator fetches the head by path, pushes the branch, opens the pull request with the body, and the one audit, the sweep and CI follow.

CLOSURE
remove

TRUST
TRUST: the unit trusts the printed procedure's own checks (line 3's `diff -r` and count, line 7's post-move judgement) as the integrity controls of the move, the next records sync from the derived store (U220) as the publication of what the live store holds beyond origin/main, and the fixture's stubs on PATH as the injection points; it does not read origin/main, the masker or any network, and it changes no procedure line but line 3's note.

TIMEBOX
45 minutes.

FORBIDDEN
No copy, rename, mode change, directory creation or removal by the lever anywhere but its scratch directory; no change to any lever but regime-store-move; no write to any checkout but the fixture's; no move of the live store; no `# producer-status: allow` comment; no network; no push; no pin edited by hand; no rebase; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u393/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/private/tmp/dotfiles-wt-U393/U393`. The repository is yours alone; your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U393-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U393-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 33, 34, 36, 44, 46, 49); the U221e brief; `verdicts/U221-89a533f0.md`; `handoff/07-store-move-design.md`; the decisions row of this unit's reservation.
