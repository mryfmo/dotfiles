# Review receipt: dotfiles-T128-seat-liveness-followup-review-a01 (round 3)

- reviewer: claude-review-dot-a001 (review seat half; the Codex half runs in parallel)
- previous_receipt: round 2 sha256 `84c5ea8ea71370de6832f885c71f8ab866882c3861cf0789c48d8b7510ffb316` (confirm on `4dd72bbd`, one P3; round 1 `2c5e6f66…`, revise on `75129cde`; overwritten by this file)
- brief: `.orchestration/tasks/dotfiles-T128-seat-liveness-followup-review-a01.md` sha256 `36a765cbd34a4f7a071b3e18e714c669946005806c0d46595fdc2574f73ba4ab` (the round-2 brief with the round-3 note in its intro, stop condition 1 reworded for the dropped record-less sentence and stop condition 2 for three cases; `diff` against the round-2 copy shows nothing else)
- reviewed file: `.orchestration/tasks/dotfiles-T128-seat-liveness-followup-a01.md` sha256 `1b64dca61343642c260cec3fbaa48b8b7850b2b8ffab849895c9f106ed63ba5a` (copied from the main checkout and hashed before reading)
- sources: as in rounds 1 and 2, on origin/main `8b25f9ca` (unchanged)

## What changed since round 2 (`diff` of the two copies: lines 20, 58, 59, and a new "Change (round 3)" section)

- The Codex half's first P2 applied: the record-less sentence is gone; item 1(b) says instead that every seat reaching the destination check has a placement record, because `seat_pane_state` answers `unknown` without a readable one and the state loop already refused. Verified on origin/main: `seat_pane_state` (957 to 970) exits its inner script when `agmsg_spawn_path` fails or the record is not readable (962) and prints `unknown` for anything but `present` or `gone` (966 to 969); the state loop (1930 to 1938) refuses any state other than `gone` with exit 2 before the per-row block. The claim holds.
- The Codex half's second P2 applied: a third test case, the run directory made read-only (`chmod 0500`, restored by the test's cleanup) with `run/stale` absent: exit 1, the stderr line, none of the four calls, the record byte-identical, the workspace still listed, no `stale/` created; row 3's disposition names the three cases.

## Checks (stop condition 1 to 4)

1. As in round 2 against the block at 1908 to 1977: refusal (a) before the state loop with exit 2; refusal (b) after the state loop and before the first `delivery.sh` with exit 1, checking without creating; `mkdir -p` left at the move; both before `delivery.sh`, `leave.sh`, the move and any `herdr` mutation; the despawn path untouched; fail closed. The record-less question is answered by the state loop itself.
2. The test name is verbatim in the closed row (16) and item 2 (59); the three cases are constructible with the module's helpers (`write_worktree_seat` with empty `worktree_identities`; `write_pane_state_fakes` for a readable record; the call filter by prefix, the record comparison and the fake herdr's `workspace close`, 3205 and 3333 to 3337); the lineage's tests stay, which the check-not-create form keeps true.
3. 13 controls, the seven generic rows byte-identical to the template after id substitution (compared by script), the new-scripts row saying no new script, the side-effects row naming the three cases; the Completion clause unchanged; the two files named by no in-flight task.
4. `task-consistency-check.py` (origin/main copy, sha256 prefix `ba27c4da`, `--root` the main checkout): `dotfiles-T128-seat-liveness-followup-a01.md: OK`; `validate-agent-assets.py --mask-secrets` on a second copy: `masked 0 match(es)`, `cmp` equal; the two premises extracted with PyYAML and replayed with `bash -c` from the main checkout after `git fetch`: `0`, `7`, equal.

## Findings

None. Two notes for the worker, no change needed: cases one and three fake the pane state `gone` (as `write_pane_state_fakes(record, "gone")` does in the lineage's tests), since the destination check sits after the state loop; case three's `chmod 0500` blocks writes for a non-root user only, which the CI runners and this host are. The round-2 P3 (an existing `stale/` directory that is not writable) stays worker input under item 1(b)'s "check the archive destination".

Task-file verdict: dotfiles-T128-seat-liveness-followup-a01: confirm
