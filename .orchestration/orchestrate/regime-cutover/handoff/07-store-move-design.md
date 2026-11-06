# The program store leaves the main checkout (gate G-30, form remove)

Written 2026-11-06 by the coordinator from a read-only trace of the lever sources at main a3ca0f2c (the `claude.levers.sha256` block of `home/dot_agents/agent-config.yaml` plus the store readers beside them under `scripts/orchestrator/`). Line numbers are the checkout's; the installed copies match byte for byte. The trace was run by a read-only subagent and every claim below was kept only where it names a `file:line`.

## Why

The live store `.orchestration/orchestrate/regime-cutover/` is written unmasked inside the main checkout's working tree while `main` holds its masked copies, so the checkout is never clean after a records sync and no ff-only pull can move it. Every procedure or lever that wrote the live checkout around that state (U192 in lever form, standing order 40 in prose form) was a list of git and filesystem states the auditor extended each round: nineteen P1 of one class over four rounds. Standing order 40 is struck; this document is the mechanism that ends the class.

## Decision: a plain directory outside the repository, not a worktree of the same repository

Two mechanisms as they stand refuse a same-repository worktree as the store:

- `scripts/orchestrator/checkout-guard.sh:450-467` and `:511-525` refuse a branch move or a commit when `.orchestration/orchestrate/*/units.tsv` exists under the worktree's toplevel or the main checkout's, so a `records/live` worktree could never commit its own records.
- `scripts/orchestrator/hcom-seat:1142-1145` and `:1033-1036` protect every other worktree of the repository from any seat write root, so the orchestrator seat could not write its ledger there.

A plain directory (the working name `~/Workspace/dotfiles-store/regime-cutover`, the final path fixed by U215) avoids both. The records still reach `main` through records pull requests, built by a sync lever from that directory.

## What binds the store to the main checkout today

| lever | binding | file:line | change |
| --- | --- | --- | --- |
| `pr-merge.sh` | `--records` by `pwd -P` must lie under the toplevel and equal `<toplevel>/.orchestration/orchestrate/<program>` | `scripts/orchestrator/pr-merge.sh:846-856` | anchor the chain walk at the store root; keep the owner, symlink and single-store checks (`:848-850, 541, 581-585, 724-743, 816-819`) |
| `pr-merge.sh` | runs in the main checkout, reads `ledger.py` and `brief-check.py` under `<toplevel>/scripts/orchestrator/` | `:874-883, 886-891` | unchanged |
| `pr-close.sh` | the table directory must start with `<toplevel>/.orchestration/orchestrate/` | `scripts/orchestrator/pr-close.sh:173-176` | the store root as the prefix |
| `records-sync.sh` | the store is a subtree of the main checkout, listed by `git ls-files` and compared with `origin/main` | `scripts/orchestrator/records-sync.sh:253-266, 277-282, 332-333, 355-356, 380` | rebuilt on the external directory: list the directory, compare with `origin/main`'s tree at the published path, build the commit in scratch as today |
| `pr-body-edit.sh` | the worker's clone must hold `<toplevel>/.orchestration/orchestrate/<program>/units.tsv` | `scripts/orchestrator/pr-body-edit.sh:167, 178-179` | the published copy on `main` keeps satisfying it as long as syncs continue; otherwise a marker file on `main` |
| `regime-init` | creates the store under the cwd toplevel | `scripts/orchestrator/regime-init:106-107, 114` | a store-root derivation shared with `regime-env` |
| `regime-start` | the store must exist under the toplevel | `scripts/orchestrator/regime-start:458, 501-502` | the same derivation |
| `regime-env` | derives the slug and the hcom store from the toplevel | `scripts/orchestrator/regime-env:72-82, 145-160` | carries the store-root derivation (an option or a `~/.local/state/...` binding file beside `origin`) |
| `checkout-guard.sh` | the trigger is the store's `units.tsv` under the checkout | `scripts/orchestrator/checkout-guard.sh:450-467, 511-525, 552-566` | with the store outside, the guard goes inert in the main checkout; a new trigger (a marker under the main checkout) keeps the protection the guard exists for |
| `hcom-seat` | `~/Workspace` is read-denied, the worker's `allowRead` re-opens only `<checkout>/.orchestration/orchestrate`, the orchestrator's write root is the checkout | `scripts/orchestrator/hcom-seat:1713, 1726-1727, 1681` | the store root enters both roles' `allowRead` and the orchestrator's write list |
| `regime-ci.py` | `git ls-tree <base> -- .orchestration/orchestrate/<program>/units.tsv` on `main` | `scripts/orchestrator/regime-ci.py:81-88` | the published copy on `main` keeps satisfying it while syncs continue |
| `.github/workflows/regime.yml` with `rounds-check.py --all` | reads both files from the head commit | `regime.yml:66`, `scripts/orchestrator/rounds-check.py:336-357` | unchanged while syncs continue to publish the files |

No change: `pr-audit.sh` (`--records` is any readable directory holding `ledger.tsv` whose last component is the program, `:826-829, 955-956`), `pr-threads-check.sh` and `pr-thread-resolve.sh` (`:325-326`, `:313-314`), `pr-update-branch.sh`, `worker-worktree.sh`, `worktree-gc.sh`, `ci-rerun.sh`, `ledger.py`, `audit-carry.py`, `filed-findings.py`, `brief-check.py`, `hcom-dispatch`, `bus-history.sh`, `omp-run.sh`, `git-isolated.sh`, `read-lib.sh`, `seat-login-preflight`, `regime-stop`, the stop gate. `pr-thread-reply.sh:140-145, 154` accepts a body under `$TMPDIR` or `<toplevel>/.orchestration`; a reply drafted inside the external store needs the store root added, or `$TMPDIR` as today.

## Units (at most two levers each, standing order 36 and brief-check's lever cap)

| unit | levers | change |
| --- | --- | --- |
| U215 | `regime-env`, `regime-init` | one shared derivation of the store root (an option or a binding file under `~/.local/state/`, the way `origin` is bound), `regime-init` creates the store there; the test of the first-run creation moves (`tests/unit/test_regime_init.py:74, 230`) |
| U216 | `pr-merge.sh`, `pr-close.sh` | the store root replaces the toplevel anchor (`test_pr_levers.py:1255, 1286, 622` change) |
| U219 | `checkout-guard.sh`, `hcom-seat` | the guard's new trigger; the store root in both roles' `allowRead` and the orchestrator's write roots (`test_checkout_guard.py:567, 657, 694, 747, 817`; a new `test_hcom_seat.py` case for the allow-read) |
| U220 | `records-sync.sh` alone | the sync rebuilt on the external directory, every listing and comparison check kept (`test_pr_levers.py:2632-2830` rewritten) |
| U221 | `regime-start` alone, then the one-time move | the store precondition; then the move itself: the live store copied to the root, the checkout's copy left to `main`'s masked content by a plain `git checkout -- .orchestration/orchestrate/regime-cutover` once the last sync from inside has merged, the checkout then clean and moved by `git pull --ff-only` |

A ledger-row writer (reserved U222, the 2026-11-06T00:18:19Z decisions row) is not part of the move and follows it.

## Order

U215 first (every later unit reads the derivation), then U216 and U219 in either order, then U220, then U221. Every unit builds on `main` after U207 (the first-token readers). The move itself is the last step of U221 and is the only moment the live store is in two places; it happens after the records sync that publishes U221's own rows.
