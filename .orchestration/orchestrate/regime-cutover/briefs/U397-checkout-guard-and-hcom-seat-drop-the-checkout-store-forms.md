# U397 checkout-guard.sh and hcom-seat drop the checkout-store forms: the marker alone triggers the guard, and no seat reads the checkout subtree (cleanup 3 of 3)

GOAL
Two pre-move forms remain after U395 and U396. `checkout-guard.sh`'s reference-transaction hook and its pre-commit hook trigger while the marker `regime-coordinator` lies beside them or a program store `.orchestration/orchestrate/<program>/units.tsv` exists under the worktree's toplevel or the main checkout's (the pre-move trigger "which U221 removes"); after the move the published copies on main carry a `units.tsv` at that path in every checkout of this repository, so the store trigger would fire for every clone and every linked worktree, on and off the coordinator's host, and the marker is the one trigger that means what it says. `hcom-seat` grants both omp roles read of `<checkout>/.orchestration/orchestrate` ("the records until U221 moves them"); after the move the records are under the store root, which both roles already read, and the grant re-opens a slice of the main checkout the worker role otherwise denies. Form `remove` (standing order 33): the guard's two hooks trigger on the marker alone, and the `.orchestration/orchestrate` entry leaves both `allow_read` lists and the README's worker-reads paragraph.

GATE
Dispatched only after the ledger holds the operator's `moved` receipt for regime-cutover and after U396 has merged (sequence, not parallel: the README is shared). Deployed by `make deploy-kit`, then `checkout-guard.sh install` is re-run on the coordinator's checkout (it upgrades its own earlier hook, U219) and the seats are relaunched at a quiet moment so the settings render without the grant.

SCOPE
A new branch `chore/levers-derived-store-alone-3` from origin/main after U396; the tree a worker repository made by worker-worktree.sh. May write: `scripts/orchestrator/checkout-guard.sh` and `scripts/orchestrator/hcom-seat` with their copies under `home/dot_local/bin/common/`, the test module of each (`tests/unit/test_checkout_guard.py` and the hcom-seat settings-render tests, by their names at the base), `scripts/orchestrator/README.md` (the guard's table cell, the worker-reads paragraph at line 175, the Threat table rows), the pins through `scripts/generate-agent-configs.py` and whatever it regenerates, and the PR body `/tmp/dotfiles-wt/U397-pr-body.md`. Non-goals: every other file under `scripts/orchestrator/`; the orchestrator's write root of the store root, the deny rows and `store_root_judge` (U219c) do not change.

CONTEXT
`checkout-guard.sh` at main: the header (lines 20 to 25), the reference-transaction hook's description and its store walk (lines 295 to 310 and the Python `store_exists` function around 420 to 440), the two pre-commit hook bodies (lines 545 to 584 and 586 to 626: the `for top in toplevel main` store walk), the `check` form's byte comparison of the installed hooks. `hcom-seat` at main: the read-grant comment (lines 2542 to 2551), the `allow_read` arrays of the orchestrator (2563 to 2564) and the worker (2580 to 2581), `tag_row store` and `store_root_judge` (unchanged). `scripts/orchestrator/README.md` line 175 (worker reads), line 223 (the guard's cell). The tests of the guard's triggers and of the rendered read grants, by name at the base. `preferences.md` standing orders 21, 29, 33, 36, 46, 49.

DATA SHAPE
One trigger for the guard's two hooks: the marker file beside them, read by `os.lstat` as today; one read-grant list per omp role without the checkout subtree, every other row as rendered today.

CHANGE
1. Tests first, red at the base: (a) a checkout with a program store under `.orchestration/orchestrate/` and no marker lets a local commit and a branch move through both hooks (the pre-move trigger gone); (b) the marker alone refuses both, unchanged; (c) the rendered settings of the orchestrator and the worker hold no `allowRead` row ending in `/.orchestration/orchestrate` and every other row of each list as before, byte for byte; (d) the guard's `check` form compares the new hook bytes and an installed old hook reads as a drift to upgrade (U219's upgrade path, re-asserted); (e) the tests of the store trigger removed.
2. The levers: the store walk removed from the reference-transaction hook and from both pre-commit hook bodies with every helper only it used; the `.orchestration/orchestrate` entry removed from both `allow_read` arrays and the comment reworded; the headers' pre-move sentences removed.
3. README: line 175 and the guard's cell say the marker alone and the store root alone; the Threat table rows name the tests.
4. Pins regenerated; `cmp` 0 twice.
5. Body as in U395 with an effect row for the coordinator's checkout (the installed hooks upgraded by `checkout-guard.sh install` after the deploy) and `Program-Unit: regime-cutover/U397` once at the end.

ACCEPTANCE
1. Tests (a) to (e) named with red and green lines. 2. `python -m unittest` over the guard's test module, the hcom-seat test modules the change touches, `tests.unit.test_lever_self_check` and `tests.unit.test_generate_agent_configs`, OK with counts. 3. `scripts/ci/producer-status-check.sh` over both levers 0 with no output, `run-on-lint-files.sh` 0, `lint-comparisons --changed` 0, `make render-check` 0, `make validate-agent-assets` 0, `make shellcheck` 0, cmp 0 twice, pasted. 4. `git diff --stat <base> HEAD` pasted with only the allowed paths. 5. `grep -c -E 'pre-move|until U221|orchestration/orchestrate' scripts/orchestrator/checkout-guard.sh scripts/orchestrator/hcom-seat` prints 0 for each, pasted.

VERIFY
As in U395; after the merge, `make deploy-kit`, then `checkout-guard.sh install` in the coordinator's checkout prints the upgrade rows and `check` exits 0; a seat dry run (`hcom-seat worker --name probe --dry-run`) renders no checkout-subtree read row.

CLOSURE
remove

TRUST
TRUST: the unit trusts the marker as the guard's one trigger (written by the coordinator's own `install`, under a hooks directory every seat is write-denied) and the store root's read grant as the seats' route to the records; it removes two forms and adds none.

TIMEBOX
60 minutes.

FORBIDDEN
As in U395, with scratch under `/tmp/u397/`; no change to any deny row, write root or the store root's judgement in hcom-seat.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your worker repository. Your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U397-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U397-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 29, 33, 36, 44, 46, 49); `handoff/07-store-move-design.md`; the U219, U219b and U219c briefs and verdicts; the U396 brief and its merge row.
