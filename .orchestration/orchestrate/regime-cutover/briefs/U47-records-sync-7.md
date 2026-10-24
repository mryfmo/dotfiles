# U47 Records sync 7: the coordinator store's rows since 10:30Z reach `main` — brief

GOAL
The program store under `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/` (the orchestrator seat's checkout, standing order 20) holds every row, brief and verdict written today since the last records PR, uncommitted in that checkout: `units.tsv`, `ledger.tsv`, `decisions.tsv`, `preferences.md` (standing order 24), the briefs of U36 to U47 and the verdicts of U27, U28, U36, U38b, U39. U28's `records-sync.sh` lever is not landed, so this unit publishes the store by hand as a records-only PR, the way records syncs 1 to 6 did.

SCOPE
One branch `records/program-store-7` from `origin/main` (63ff0b20 or later). May write: files under `.orchestration/orchestrate/regime-cutover/` only, copied from the orchestrator checkout's working tree: `units.tsv`, `ledger.tsv`, `decisions.tsv`, `preferences.md`, `gates.md`, `overview.md` (if it differs), `briefs/*.md`, `verdicts/*.md`, `handouts/*.md`. Nothing outside `.orchestration/`; the regime check must report `no target (records-only)`.

CHANGE
1. In your worktree on the new branch: `rsync -a --exclude '.claude/' ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/ .orchestration/orchestrate/regime-cutover/` (a copy, never a move; the source is read only); then `git status --porcelain` and `git diff --stat` pasted: every path must be under `.orchestration/orchestrate/regime-cutover/`.
2. Sanity on the TSVs: `awk -F'\t' '{print NF}' <file> | sort -u` prints one column count per file (7 for units, 7 for ledger, 6 for decisions); a row with another count is a defect to report, not to fix (the orchestrator fixes its own rows); paste the three results.
3. No content edits: the diff is the copy. One commit, `records(regime-cutover): sync 7, the store through U46 (U47)`.

ACCEPTANCE
1. `git diff --name-only origin/main..HEAD | grep -v '^\.orchestration/'` prints nothing (paste); the column-count check pasted.
2. CI: the regime check `no target (records-only)`; the test jobs skip or pass.
3. PR body `Program-Unit: regime-cutover/U47` (harmless on a records-only diff), the file count, the self-check (threat table: records only); orchestrator verdict (the diff is the orchestrator's own store).

TIMEBOX
20 minutes.

FORBIDDEN
No edit to any copied file; no path outside `.orchestration/`; no omp subagent; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 24).
