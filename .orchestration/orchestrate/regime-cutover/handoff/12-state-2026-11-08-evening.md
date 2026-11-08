# State at 2026-11-08 15:0xZ (coordinator handoff; follows 11-state-2026-11-08-morning.md)

## Landed today (each through pr-audit.sh, a sweep row and pr-merge.sh, then `make deploy-kit`)

| PR | unit | what | rounds |
| --- | --- | --- | --- |
| 737 | U221 (store move 5 of 5) | `regime-start` resolves the store by the two-form rule; `regime-store-move <program>` is the read-only judge of the move and prints the operator's seven-line procedure. Rounds 1 to 3 (class move-race) had the lever copy the store under observation, mode and identity controls, each defeated by a same-user writer; the mechanism-change row of 10:26:46Z (form remove) made it read-only; round 4 (class read-rigor) fixed the printed copy line's mode and the listing reads; round 5 correct. Two CI reruns lost to a GitHub download outage (the merge of main 78432b2b, the empty commit 61cba044, both carried from 89a533f0 by the digest lever) | 5 |
| 738 | U20 | records sync 52 (40 files: the U221 rounds, sweeps U387 to U391, the merge). The body's Threat table was rewritten in place with one row per changed path after the audit filed the grouped form a third time (dispositions.tsv:194, residual in the sync-51 form) | 1 |
| 739 | U393 | `regime-store-move` drops the comparison with origin/main: every sync's own verdict, sweep and merge rows are written after the sync's listing, so the live store is ahead of main after every merge and the equality gate could never pass (nine paths after sync 52); line 3's `diff -r` and count and line 7's post-move check are the controls that remain (design amendment at the end of 07-store-move-design.md) | 1 |

Deployed on this laptop: `regime-start`, `regime-store-move` (the U393 version, pin 592ed0a7), the manifest. The store root `~/.local/state/regime-store/dotfiles` exists (0700), made by the launch of the idle seat sweep-4-zilu at 13:23Z (the two older sweep seats predate U219c's hcom-seat).

## The move: handed to the operator

`regime-store-move regime-cutover` printed `ready: 1825 live files; the derived store is absent` and the seven lines at 15:01Z (1827 at 15:03Z; the count grows with every record). The handout is `handouts/store-move-procedure.md`: step 0 reprints the procedure for the current count, then lines 1 to 7 by hand after this session is closed. The gate is G-31 in `gates.md`. Every record written since sync 52's listing is in the live store and will be in the copy.

## First things for the next session (after the operator's line 7)

1. Confirm the form: any lever's stderr says `store: derived ~/.local/state/regime-store/dotfiles/regime-cutover`; `git -C ~/Workspace/dotfiles status --porcelain` is empty and HEAD is origin/main.
2. Records sync 53 from the derived store (`records-sync.sh --program regime-cutover --unit U20`): the delta since sync 52's listing is the sync 52 verdict, sweep set and merge row, U392 to U394 (briefs, verdict U393-195ce731, sweeps), the U393 design and goal-check rows, the CI outage rows, this note and the handout. The body's Threat table goes per path (the form that ended the class at sync 52).
3. The pre-move cleanup is three sequenced units, briefed and reserved under G-31 (dispatched only after the `moved` receipt row, in order, since they share `test_pr_levers.py` and the README): U395 (`pr-merge.sh`, `pr-close.sh`), U396 (`records-sync.sh`, `regime-start`), U397 (`checkout-guard.sh`'s marker-only trigger, `hcom-seat`'s checkout-subtree read grant). `pr-body-edit.sh` and `regime-ci.py` keep reading the published copy on main. After U397 deploys: `checkout-guard.sh install` on the coordinator's checkout and a seat relaunch.
4. U222 (the ledger-row writer, `ledger-row.py`) merged as PR 740 at 17:38Z after four rounds (round 2 lost-update, round 3 store-shape, the mechanism-change row of 16:50:19Z: no file but the ledger, its own descriptor the advisory lock, one append, truncate on a failed write). Deployed by `make deploy-kit`; the installed copy needs `ledger.py` beside it, so run it from the chezmoi clone: `python3 -I -S ~/.local/share/chezmoi/scripts/orchestrator/ledger-row.py <store> <kind> ...` (its own merge row was the first written through it). U222e (the tests wave: injection tests for lseek, fsync, ftruncate and close; the held-lock helper's stdout; the option name in the one-line refusal) is reserved and unbriefed, after the move. Every coordinator row from now on goes through the lever.

If the operator reports a refusal at step 0 or a failure at any line, the live store is untouched until line 4 and the derived copy is removable; read the message before anything else.

## Still waiting on the operator (unchanged since the morning note)

1. Codex hardware-key login (PR 720, U343e). After the login: `pr-audit.sh 720`.
2. Seat login: the shared seats token is revoked; `seat-login-preflight --check` reads the method, not the validity. After the login: the g6 rerun.
3. The Router's agent account (handouts/m25-agent-github-account.md).

## Residual rows worth a tests wave

The morning note's list stands, plus: `regime-store-move`'s `read_file` suppresses a producer's stderr warning (the U221 round-5 P2 at weight 4 and the U393 P2 at weight 3, the same class, both filed); the audit route cannot run `producer-status-check.sh` inside its sandbox (here-document temporaries denied), so that lint's evidence is the worker's and CI's.

## Lessons recorded today (decisions.tsv)

- A delegate that goes silent after a tool call returned (13:22Z to 14:17Z, no edit) is stopped and replaced; the replacement finished in 9 minutes. Watchers now return after 20 minutes so the stall check is not missed.
- The standing order 19 `pushInsteadOf` override does not match an https origin whose global rule is `url.git@github.com:.pushInsteadOf=https://github.com/`; the explicit-URL form with gh's credential helper is the push that works on this host.
- A body-only P2 is fixed in the body in place (order 35) and the gate is satisfied by the disposition row, never by a re-audit round.
