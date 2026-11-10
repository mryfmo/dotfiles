# U395 pr-merge.sh and pr-close.sh read the derived store alone: the pre-move form leaves (cleanup 1 of 3)

GOAL
Since U216 the two levers choose a program's store by a two-form rule: the derived store `${REGIME_STORE_ROOT}/<program>` when that directory exists, else the checkout's own `.orchestration/orchestrate/<program>` (the pre-move form, "removed by U221" in their text). The move (U221, handouts/store-move-procedure.md) puts the live store under the root, after which the checkout subtree holds main's masked copies and is no store. The second form is then dead code that a reader must still understand and an auditor must still probe (a checkout form with the derived store absent reads the published copies as if they were records). Form `remove` (standing order 33): `store_resolve` in both levers takes the derived form alone, and a program whose derived store is absent is refused naming `regime-init <program>` as the route; the `--records` rule becomes one comparison (`pwd -P` equality with the derived store); the "pre-move form" sentences of both headers, the README rows and the regime README section go.

GATE
This unit is dispatched only after the ledger holds the operator's `moved` receipt for regime-cutover (handouts/store-move-procedure.md line 7; the decisions row that records it). Merged before the move, the levers would refuse every merge and close on this host (no derived store exists until the move). The coordinator checks the row before the TASK.

SCOPE
A new branch `chore/levers-derived-store-alone-1` from origin/main; the tree a worker repository made by worker-worktree.sh. May write: `scripts/orchestrator/pr-merge.sh` and `scripts/orchestrator/pr-close.sh` with their copies under `home/dot_local/bin/common/`, `tests/unit/test_pr_levers.py` (the `store_resolve` tests of the two levers), `scripts/orchestrator/README.md` (the two levers' table cells and Threat table rows), the pins through `scripts/generate-agent-configs.py` and whatever it regenerates, and the PR body `/tmp/dotfiles-wt/U395-pr-body.md`. Non-goals: every other file under `scripts/orchestrator/`; the regime-store-move lever reads the checkout subtree by design (it judges the move) and does not change here.

CONTEXT
`pr-merge.sh` at main: the header's description (lines 8 to 18), `store_resolve` (around line 731 to 776, with `store_checkout`, `store_form`, the `checkout` branch and its stderr line), `require_records`'s two-form refusals (around lines 803 to 817). `pr-close.sh` at main: the header (lines 8 to 15), `store_resolve` (around 155 to 203), the handouts-table location check (around 255 to 270, both forms). `tests/unit/test_pr_levers.py`: `test_the_checkout_store_stands_as_the_pre_move_form_while_the_derived_store_is_absent` for each lever and the tests of the derived form. `scripts/orchestrator/README.md`: the two levers' rows in the seat-levers table (lines 290 and 293 region) and the Threat table rows (304 and 308 region). `preferences.md` standing orders 21, 33, 36, 46, 49.

DATA SHAPE
One store per program: `${REGIME_STORE_ROOT}/<program>`, a directory of this user and no symlink, held as today; one stderr line `store: derived <dir>`; one refusal when it is absent: `no program store at <dir>; run regime-init <program> (the live store of a program that moved is there; the checkout subtree holds main's published copies and is no store)`.

CHANGE
1. Tests first, red at the base, in `test_pr_levers.py`: (a) for each lever, the derived store absent is a refusal naming `regime-init <program>` and the derived path, exit 2, nothing merged or closed, nothing written; (b) the derived form's tests unchanged and green; (c) the two pre-move-form tests removed; (d) a `--records` (pr-merge.sh) or a table path (pr-close.sh) under the checkout subtree while the derived store exists is refused naming the derived store alone (no "both forms" sentence).
2. Both levers: `store_resolve` with the derived form alone; the refusal of DATA SHAPE; `store_form` and `store_checkout` removed with every read of them; the headers' "pre-move form" and "until U221" sentences removed; the one stderr line kept.
3. README: the two table cells and the two Threat table rows say the derived store alone, naming the tests of change 1.
4. Pins regenerated; `cmp` of each source and copy 0.
5. Body with Summary, Contract, Threat table (one row per changed path and one effect row: a host whose program has not moved refuses with the route), Verification, `Program-Unit: regime-cutover/U395` once at the end.

ACCEPTANCE
1. Tests (a) to (d) named with red lines at the base and green lines at the head. 2. `python -m unittest tests.unit.test_pr_levers tests.unit.test_lever_self_check tests.unit.test_generate_agent_configs` OK with counts. 3. `scripts/ci/producer-status-check.sh` over both levers 0 with no output, `run-on-lint-files.sh` 0, `lint-comparisons --changed` 0, `make render-check` 0, `make validate-agent-assets` 0, `make shellcheck` 0, cmp 0 twice, pasted. 4. `git diff --stat <base> HEAD` pasted with only the allowed paths. 5. `grep -c -E 'pre-move|until U221|store_checkout|store_form' scripts/orchestrator/pr-merge.sh scripts/orchestrator/pr-close.sh` prints 0 for each, pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator fetches the head by path, pushes the branch, opens the pull request, and the one audit, the sweep and CI follow; `make deploy-kit` after the merge, then `pr-merge.sh` prints `store: derived` on its next run.

CLOSURE
remove

TRUST
TRUST: the unit trusts regime-env's derivation of the root and the per-component holds already in both levers as the store's identity, and the operator's completed move (the `moved` receipt row) as the precondition of its merge; it reads nothing new and removes a form.

TIMEBOX
45 minutes.

FORBIDDEN
No change to any lever but the two named; no new form, option or environment read; no write to any checkout but the fixture's; no `# producer-status: allow` comment; no network; no push; no pin edited by hand; no rebase; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u395/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your worker repository. Your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U395-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U395-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 33, 36, 44, 46, 49); `handoff/07-store-move-design.md` and its U393 amendment; the U216 and U216c briefs; the decisions row that records the operator's move.
