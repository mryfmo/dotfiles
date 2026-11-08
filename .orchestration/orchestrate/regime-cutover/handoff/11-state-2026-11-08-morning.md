# State at 2026-11-08 04:0xZ (coordinator handoff; follows 10-state-2026-11-07-evening.md)

## Landed overnight (each through pr-audit.sh, a sweep row and pr-merge.sh, then `make deploy-kit`)

| PR | unit | what | rounds |
| --- | --- | --- | --- |
| 731 | U20 | records sync 49 | 1 |
| 732 | U216 (store move 2 of 5) | `pr-merge.sh` and `pr-close.sh` source `regime-env` and anchor the store at `${REGIME_STORE_ROOT}/<program>` when it exists, else the checkout store (the pre-move form, removed by U221); round 2 made the producer-status lint take `regime-env` as a library and accept `return` as a refusal block's terminator inside a function; round 3 fixed the lint's contract table and confined the terminator to brace blocks | 3 |
| 733 | U219 (store move 3 of 5) | `checkout-guard.sh` triggers on a marker `regime-coordinator` beside its hook and `install` upgrades its own earlier hook; `hcom-seat` grants the store root to both roles for read and to the orchestrator for write, makes the root at launch, denies it for write to every other row, judges every rendered grant against it by identity, and refuses an hcom store overlapping it; `~/.local/state/regime-store` is a protected root | 3 |
| 734 | U220 (store move 4 of 5) | `records-sync.sh` syncs the derived store directory when it exists (a `find` walk under the per-path holds, compared with `origin/main` at the published prefix), else the checkout subtree | 1 |
| 736 | U20 | records sync 51 (sync 50, PR 735, closed after its audit: a decisions row split by quoted guard receipts) | 1 |

The guard is installed on the coordinator's checkout (23:35Z: `check` said both absent, `install` wrote the hook and the marker). It refused the coordinator's own fetch of a records branch into a local branch an hour later, as designed; records branches are now fetched into `refs/remotes/origin/<branch>` and the body lever runs from a detached worktree switched to a tracking branch.

## In flight

- **U221 (store move 5 of 5), worker dispatched 03:58Z** on `/tmp/dotfiles-wt/U221`: `regime-start` takes the two-form rule; a new lever `regime-store-move <program>` copies the live store to the derived root, refuses when a records sync is still due (the masked form of a live file against `origin/main`'s blob), verifies the copy and prints the operator's one step. After it merges and deploys: `regime-store-move regime-cutover --check`, the last sync from inside, the move, then the operator's step (`git checkout -- <store>`, `git clean -fd -- <store>`, `git pull --ff-only` in `~/Workspace/dotfiles`). That step is the last write to the coordinator's live checkout by anyone.
- After the move, a cleanup unit removes the pre-move forms (the checkout fallback in the four levers, the guard's store trigger, the worker's read grant of the checkout records) and `pr-body-edit.sh:178` and `regime-ci.py:82` keep reading the published copy on `main`.

## Still waiting on the operator (unchanged since the evening note)

1. Codex hardware-key login (PR 720, U343e): three audits ended on the Daybreak Blue message; the content gate, not the size. After the login: `pr-audit.sh 720`.
2. Seat login: the shared seats token is revoked (`expiresAt 0`); `seat-login-preflight --check` says `login present` because it reads the method, not the validity (a preflight gap worth a unit). After the login: the g6 rerun.
3. The Router's agent account (handouts/m25-agent-github-account.md): step 1 and the credential-root login; step 2's form needs a role, team or app as the bypass actor (a user-owned repository cannot name a single user).

## Residual rows worth a tests wave

router-gh's `/usr/bin/stat` producer (U353 round 4); regime-init's copy-then-fail and stat window (U215 round 3); run-host-rows.py's default discovery containment (sync 48); the lint's nested-subshell and exit-in-subshell gaps (U216 round 3, the U216c worker's note); regime-env's own four producer-status findings (U216b's deviation: `set -euo pipefail` absent in a sourced helper, three `|| name=''` reads); the m25 bypass-actor form; the records sync body's Threat table form (re-raised at every sync as a P2 at weight 20: the auditor wants per-path rows and the regime workflow's actual selectors; the coordinator's grouped table with selectors in the control column did not satisfy it at sync 51).
