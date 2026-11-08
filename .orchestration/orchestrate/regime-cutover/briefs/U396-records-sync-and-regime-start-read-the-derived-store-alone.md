# U396 records-sync.sh and regime-start read the derived store alone: the pre-move form leaves (cleanup 2 of 3)

GOAL
`records-sync.sh` (U220) and `regime-start` (U221) choose a program's store by the two-form rule: the derived store `${REGIME_STORE_ROOT}/<program>` when that directory exists, else the checkout subtree `.orchestration/orchestrate/<program>` (the pre-move form). After the move (handouts/store-move-procedure.md) the checkout subtree holds main's published copies and is no store, and the checkout form of the sync would publish the published copies to themselves. Form `remove` (standing order 33): both levers take the derived form alone, a program whose derived store is absent is refused naming `regime-init <program>`, and the sync's checkout-form listing (the git-tracked walk, the `.orchestration` holds) goes with it, leaving the `find` walk of U220 as the one listing.

GATE
Dispatched only after the ledger holds the operator's `moved` receipt for regime-cutover and after U395 has merged (the three cleanup units share `tests/unit/test_pr_levers.py` and the README, so they run in sequence, not in parallel; Separate Before Serializing Shared State).

SCOPE
A new branch `chore/levers-derived-store-alone-2` from origin/main after U395; the tree a worker repository made by worker-worktree.sh. May write: `scripts/orchestrator/records-sync.sh` and `scripts/orchestrator/regime-start` with their copies under `home/dot_local/bin/common/`, `tests/unit/test_pr_levers.py` (the records-sync tests) and `tests/unit/test_regime_start.py`, `scripts/orchestrator/README.md` (the two levers' cells and Threat table rows, the regime-start paragraph), the pins through `scripts/generate-agent-configs.py` and whatever it regenerates, and the PR body `/tmp/dotfiles-wt/U396-pr-body.md`. Non-goals: every other file under `scripts/orchestrator/`.

CONTEXT
`records-sync.sh` at main: the header (lines 10 to 20), `store_resolve` (around 280 to 323: the `.orchestration` holds, `store_checkout`, `store_form`), the two listings (the `find` walk of the derived form and the git-tracked listing of the checkout form; which `collect_path` and `check_path` branches serve the checkout form alone), the stderr line. `regime-start` at main: the header (lines 13 to 18, 42), `store_resolve` (around 465 to 495). `tests/unit/test_pr_levers.py`: `test_the_checkout_subtree_stands_as_the_pre_move_form_while_the_derived_directory_is_absent` and the records-sync tests around lines 2632 to 2830; `tests/unit/test_regime_start.py`: the pre-move-form test and the derived-form tests. The README's `regime-start` paragraph (line 405 region) and the sync's row. `preferences.md` standing orders 21, 33, 36, 46, 49.

DATA SHAPE
One store per program (`${REGIME_STORE_ROOT}/<program>`, held as today), one listing (the `find` walk under the per-path holds), one stderr line `store: derived <dir>`, one refusal naming `regime-init <program>` when the store is absent.

CHANGE
1. Tests first, red at the base: (a) each lever refuses an absent derived store naming `regime-init <program>`, exit 2, nothing started or synced, nothing written; (b) the derived-form tests unchanged and green; (c) the two pre-move-form tests and every test of the checkout-form listing removed; (d) for records-sync.sh, a checkout subtree with stray files beside an existing derived store changes nothing in the copy set (kept from U220, re-asserted).
2. Both levers: `store_resolve` with the derived form alone and the refusal; the checkout-form listing and its holds removed from records-sync.sh with every variable only it read; the headers' "pre-move form" sentences removed.
3. README per the pattern of U395.
4. Pins regenerated; `cmp` 0 twice.
5. Body as in U395 with `Program-Unit: regime-cutover/U396` once at the end.

ACCEPTANCE
1. Tests (a) to (d) named with red and green lines. 2. `python -m unittest tests.unit.test_pr_levers tests.unit.test_regime_start tests.unit.test_lever_self_check tests.unit.test_generate_agent_configs` OK with counts. 3. `scripts/ci/producer-status-check.sh` over both levers 0 with no output, `run-on-lint-files.sh` 0, `lint-comparisons --changed` 0, `make render-check` 0, `make validate-agent-assets` 0, `make shellcheck` 0, cmp 0 twice, pasted. 4. `git diff --stat <base> HEAD` pasted with only the allowed paths. 5. `grep -c -E 'pre-move|until U221|store_checkout|store_form' scripts/orchestrator/records-sync.sh scripts/orchestrator/regime-start` prints 0 for each, pasted.

VERIFY
As in U395; after the merge and `make deploy-kit`, the next records sync prints `store: derived`.

CLOSURE
remove

TRUST
TRUST: as in U395; the `find` walk of U220 and its per-path holds are the listing the sync trusts.

TIMEBOX
45 minutes.

FORBIDDEN
As in U395, with scratch under `/tmp/u396/`.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your worker repository. Your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U396-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U396-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 33, 36, 44, 46, 49); `handoff/07-store-move-design.md`; the U220 and U221 briefs; the U395 brief and its merge row.
