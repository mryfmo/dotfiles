# U221e round 5 of U221: the printed procedure completes against the lever's own post-move check, and every read of the move lever is whole

GOAL
The round-4 audit of PR 737 (verdicts/U221-af547232.md, class read-rigor; the move-race class of rounds 1 to 3 was not re-raised) found one P1 and five P2 in `regime-store-move`'s read-only form. (1) P1 :221: the printed `cp -a` preserves the checkout store's 0755, and the lever's post-move check requires 0700, so the procedure as printed cannot complete (the test fixture hid it with an extra `chmod`); the procedure's copy line becomes `cp -a <checkout store> <root>/<program> && chmod -R go-rwx <root>/<program>` (one line, the mode the kit gives every store it makes) and the post-move check keeps 0700. (2) P2 :308: `read` trims trailing IFS whitespace before `check_entry` sees the path, so `units.tsv ` (a trailing space) beside `units.tsv`, as a file or a dangling link, passes; every listing is read with `IFS= read -r -d ''` from a NUL-delimited walk, the way U220's derived walk reads. (3) P2 :478: `uv run` writes its cache under `$HOME/.cache/uv`, outside the lever's scratch directory; the masker runs with `UV_CACHE_DIR=<scratch>/uv-cache` (and `--no-cache` if the kit's other levers use it: read records-sync.sh's form and take it). (4) P2 :203: the count pipeline reads the status alone; a `wc` that warns on stderr while printing a count passes; every producer's stderr is captured to a scratch file and a non-empty one refuses naming the producer (read-lib.sh's `read_listing` shape). (5) P2 :184: a failed scratch removal prints a warning after `ready` and exits 0; the removal's status is read and a failure exits 1 naming the directory left behind (the verdict line already printed stands; the exit status says the run did not end clean). (6) P2 tests:396: the injection matrix omits `tr`, `stat`, `ls-tree`, `rev-parse` and `hash-object`; each gets a committed injection.

SCOPE
The same branch `feat/regime-start-store-resolve-and-regime-store-move` and PR 737; the tree is the worker repository `/tmp/dotfiles-wt-U221/U221` at af547232 (clean). May write: `scripts/orchestrator/regime-store-move` and its copy `home/dot_local/bin/common/executable_regime-store-move`, `tests/unit/test_regime_store_move.py`, `scripts/orchestrator/README.md` (the procedure's copy line where the README quotes it), the pin through `scripts/generate-agent-configs.py` (never by hand) and whatever it regenerates, and the PR body `/tmp/dotfiles-wt/U221-pr-body.md`. Non-goals: `regime-start` and every other file under `scripts/orchestrator/`; no move of the live store by the worker; no write to any checkout but the fixture's.

CONTEXT
`regime-store-move` at af547232: the procedure's printf (:221), the listing reads (:308 region), the masker's `uv run` (:478), the count pipeline (:203), the scratch removal (:184), the post-move 0700 check; `tests/unit/test_regime_store_move.py` (six tests; the fixture's extra `chmod` the auditor named, to remove); `records-sync.sh` at origin/main (how it runs the masker under `uv run` and where its cache goes; how it reads NUL-delimited listings through `read_listing`); `read-lib.sh` (`read_listing`: status and stderr both read); `verdicts/U221-af547232.md` lines 15 to 19 (the auditor's five probes, the shapes of the new tests); `preferences.md` standing orders 21, 46. CI at af547232: read the failed legs' logs before assuming the head; the earlier head's red was GitHub's 504 on tool downloads (decisions 2026-11-08T10:29:52Z).

DATA SHAPE
One procedure whose copy line leaves the destination 0700 (`cp -a ... && chmod -R go-rwx ...`); one listing grammar (NUL-delimited, `IFS= read -r -d ''`, every byte of the name kept, a name with a trailing or leading space or any control character refused by name); one scratch directory that holds every write of the run, uv's cache included; one stderr rule (every producer's stderr captured, a non-empty one refuses naming the producer); one exit rule (a failed removal of the scratch directory exits 1 naming it, after the verdict line).

CHANGE
1. Tests first, red at af547232, in `test_regime_store_move.py`: (a) the fixture's extra `chmod` removed; the printed procedure's lines executed against the fixture (the stop line skipped as text) end with the lever's post-move run reporting `moved: ...` (the destination 0700 by the printed line alone); (b) a live file named `units.tsv ` (trailing space) and a dangling link of that name each refuse by name before any comparison; (c) after a `ready` run, nothing exists under `<HOME>/.cache` (the fixture's HOME clean of uv's cache) and the scratch directory is gone; (d) a `wc` stub that prints a valid count and a warning on stderr refuses naming `wc`; (e) an `rm` stub exiting 7 on the scratch removal makes the run exit 1 naming the directory after the `ready` line; (f) stubs for `tr`, `stat`, `git ls-tree`, `git rev-parse` and `git hash-object` (through the scratch git's PATH or a wrapper the fixture already uses) each refuse naming the producer. 2. The lever: the six changes; the header says the listing grammar and the cache. 3. The copy and the pin through the generator. 4. README: the quoted copy line. 5. Green: `uv run --offline --with pyyaml python -m unittest tests.unit.test_regime_store_move tests.unit.test_regime_start tests.unit.test_lever_self_check tests.unit.test_generate_agent_configs -v` to `/tmp/u221e/full.txt`; `scripts/ci/producer-status-check.sh scripts/orchestrator/regime-store-move` exits 0 with no output; the lints through `run-on-lint-files.sh` (shellcheck, shfmt, ruff, prettier), `lint-comparisons --changed`, `make render-check`, `validate-agent-assets`; cmp of the pair; the pin equal to `shasum -a 256` of the source. 6. One commit on af547232; the body gains `## Round 5 (U221e)` (the six findings in the body's own words) and a `### Round 5, U221e, head <sha>` subsection under the existing `## Verification` heading (kept once) with ACCEPTANCE pasted; the operator-step row's copy line updated; `Program-Unit: regime-cutover/U221` once at the end; the body under 50000 bytes.

ACCEPTANCE
1. Tests (a) to (f) named with their red lines at af547232 (`/tmp/u221e/red.txt`) and green lines at the head. 2. The four modules OK with counts under `python -m unittest`. 3. The producer-status lint over the lever exits 0 with no output, pasted; every other lint 0 (`run-on-lint-files.sh`, `lint-comparisons --changed`, `make render-check`); cmp 0; the pin equals `shasum -a 256` of the source. 4. `git diff --stat af547232 HEAD` pasted; `regime-start` not in it. 5. `grep -c 'chmod -R go-rwx' scripts/orchestrator/regime-store-move` is 1 (the procedure's line), `grep -c "read -r -d ''" scripts/orchestrator/regime-store-move` is 1 or more, `grep -c UV_CACHE_DIR scripts/orchestrator/regime-store-move` is 1 or more, pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator fetches the head by path, pushes to PR 737's branch, and the one audit, the sweep and CI follow.

CLOSURE
remove

TRUST
TRUST: the unit trusts the printed procedure as the operator's contract (so the fixture runs it as written and the lever's own post-move check judges it), read-lib.sh's listing shape as the reading rule, and the fixture's stubs on PATH as the injection points.

TIMEBOX
50 minutes.

FORBIDDEN
No copy, rename, mode change, directory creation or removal by the lever anywhere but its scratch directory; no change to any lever but regime-store-move; no write to any checkout but the fixture's; no move of the live store; no `# producer-status: allow` comment; no network beyond the fixture's bare origin; no push; no pin edited by hand; no rebase; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u221e/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt-U221/U221`. The repository is yours alone; your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U221e-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U221e-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 36, 44, 46, 49); `verdicts/U221-af547232.md`; the U221d brief; the two mechanism-change rows of U221.
