# U20 Records sync: the program store carried to main

GOAL
The coordinator writes the program's records (units, ledger, decisions, dispositions, gates, briefs, verdicts, handoff) in the main checkout's store. A records sync carries the store to `main` as one pull request so the repository holds the same records the coordinator reads. Each sync is one pull request named `records/sync-<n>`, opened by the records lever, audited like any program pull request and merged by the merge lever.

SCOPE
One branch `records/sync-<n>` from `origin/main`, made by `records-sync.sh`. May write: files under `.orchestration/orchestrate/regime-cutover/` only, as the lever copies them (the copy set is the store on disk compared with `origin/main` by content; `redact-words.txt` is never carried; every copy is masked by the asset validator and scanned for secret patterns, home paths and redact words before the push).

CHANGE
1. Run `~/.local/bin/common/records-sync.sh --program regime-cutover --unit U20` in the main checkout; it prints `synced branch=records/sync-<n> files=<n> pr=<url>`.
2. The audit of the head judges records only: every changed file lies under the store, the TSV files keep their header's column count on every row, and the copies equal the local store but for masked words.
3. Merge with `pr-merge.sh` on the correct row for the head.

ACCEPTANCE
1. The receipt line of the lever. 2. The audit verdict `correct` for the head. 3. `rounds-check.py --all` over the store exits 0 before the sync.

TIMEBOX
30 minutes per sync.

FORBIDDEN
No file outside the store; no hand edit of a copy after the lever made it; no `codex` or `gh` write other than the lever's own.

REPORT
The receipt line, the verdict, the merge receipt.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; the U101 and U28 decisions rows on the records lever.
