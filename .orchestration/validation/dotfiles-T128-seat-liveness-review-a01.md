# Review receipt: dotfiles-T128-seat-liveness-review-a01 (round 2)

- reviewer: claude-review-dot-a001 (review seat half; the Codex half runs in parallel)
- previous_receipt: round 1 sha256 `55e0c32b2739c6ccae4d7e10f135c28bbcc0d5c5866e1e7c6c5051876a45896d` (revise on `8efb4299`, one P2 and seven P3; overwritten by this file)
- brief: `.orchestration/tasks/dotfiles-T128-seat-liveness-review-a01.md` sha256 `cf7ca897b16011ca39147d5cf8f46e41dfd5d5d70802b7fb4a64e0d21da706c2` (round 1 brief with the round-2 note in its intro and stop conditions 1 and 2 reworded for the applied clauses; `diff` against the round-1 copy shows nothing else)
- reviewed file: `.orchestration/tasks/dotfiles-T128-seat-liveness-a01.md` sha256 `eb50e54f2427d9acc5fd9f0f1fb1e6f934828cf5c47c8530e5cca1da065ae9c9` (copied from the main checkout and hashed before reading)
- origin/main at review: `59599783` (unchanged since round 1)

## What changed since round 1 (`diff` of the two copies: lines 26, 38, 72, 77, 78, 79, and a new "Change (round 2)" section)

- P2 applied: the retired record is moved to `<run directory>/stale/<record basename>.<UTC timestamp>` instead of renamed in place (row 26, Goal, item 2(b)); item 4's assertion is "exactly one file `stale/<record basename>.<timestamp>` under the run directory". Checked against the installed upstream: every iteration over the run directory is a prefix glob (`spawn.*` in terminal-registry.sh:898, `role-session.*`, `cc-instance.*`, `proj.*.project`, `actas.*.session`), none walks `"$dir"/*`, so a `stale/` subdirectory is outside every scan and the evidence stays on disk.
- P3 clauses applied: `--stale` reads every identity row's state before anything changes and retires only when every row is `gone` (item 2(b)); the dirty-worktree refusal and the orchestrator-identity check (`leader`) stay before both paths; `seat_stale=` lines print only when the claim was not skipped (item 2(c)); item 3's temporary repository gains a linked worktree under `.claude/worktrees/` (`git worktree add`); row 38 names sqlite3 (either binary absent yields `unknown`); item 2(a) points at the `env SKILL_DIR=… bash -c` form `check_worker_linkage` already uses.
- The Change section records the round. The front matter is otherwise the round-1 one.

## Checks (stop condition 1 to 4)

1. Upstream and the two scripts on origin/main are unchanged since round 1 (the lookup chain, `terminal_pane_state`'s three answers, `despawn.sh`'s precedent, the loop at crb.sh:91-108, the remove block at 1839-1866 with the dirty-worktree refusal at 1841 and the `leader` check at 1845-1852, `claim_seat_and_print_directive` at 701-711); the round-1 live replay stands (`present` for this seat's `wA:p2`, `gone` for `wA:p77`). The behaviours and failure modes now read as the brief's stop condition 1 states them: `unknown` and `present` never retire and keep the despawn path; `gone` retires only on `--stale`, after every row's state is read; the record moves under `stale/`; both refusals precede both paths; `seat_stale=` only on an unskipped claim.
2. The three test names are verbatim; the cases distinguish the three states, the `--stale` test asserts the call order and the moved record against `present` with nothing changed, the boundary test now has the linked worktree the loop needs, and the fakes answer from files the case writes.
3. Rows as in round 1 (one per path, the record-and-agent-list row, the seven generic rows byte-identical to the template, the new-scripts row saying no new script); the Completion clause and the cap sentence unchanged; the four files are named by no in-flight task. 15 controls, 4 claims.
4. `task-consistency-check.py` (origin/main copy, sha256 prefix `ba27c4da`, `--root` the main checkout): `dotfiles-T128-seat-liveness-a01.md: OK`; `validate-agent-assets.py --mask-secrets` on a second copy: `masked 0 match(es)`, `cmp` equal; the four premises replayed from the main checkout after `git fetch`: `1`, `0`, `189`, `9`, equal.

## Findings

None. The round-1 P3s that needed no change (the shared child-bash form, now named in item 2(a); the C-49 learning line following the final test name at the next boundary) stand as noted.

Task-file verdict: dotfiles-T128-seat-liveness-a01: confirm
