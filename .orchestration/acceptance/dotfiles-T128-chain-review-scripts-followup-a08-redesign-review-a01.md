# Acceptance: dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01

Review task (kind review, pr=none) sent to claude-standard-dot-a011 (Claude, worker-d) 2026-10-21T05:22Z as bus message 2966, text sha256 25e9592831145a5bc1e2f6c836337eb5a0abd1323c80d3f3cb0747443e26e7d6. It judges the a08 redesign text (`.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md`) as the INV-6 reset anchor of `dotfiles-T128-chain-review-scripts-followup-a07` (D-024-41, D-024-52).

## Round 1

- RESULT 2967 at 05:24Z: `verdict=reject design_sha256=cbc39befc4cdf5ed4d7c11e606d0ccd02c81b7bdc82bfa44e4e742f4b79d06f7`, review at `.claude/worktrees/worker-d/.orchestration/dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01/review.md` (hash recomputed and equal; reset_of, findings table, no widening and residual owners all ok).
- Finding: B:119 and B:130 make the orchestrator's Checks paste (the resolved measurement base) a precondition of the anchor review, and B:132-133 hold only the empty heading. The reviewer's fix: paste Checks, re-hash, re-run the anchor review on the new bytes.
- Orchestrator measurement for the paste (2026-10-21T05:47Z, sandboxed Bash): `git merge-base a644a7d9 origin/main` = b8213131f3818de6d14aae1ccb4b79a7ce7a99ba with origin/main a811f1334ad2e2a78d86fb63c65a69dba8e27b2e; `git diff --numstat b8213131 a644a7d9 -- scripts tests` = 27+6 scripts/orchestrator/local-review.sh, 94+8 tests/unit/test_chain_review_scripts.py, so the inherited lines are 33 outside tests/ and 102 under tests/. The dispatched text's B:117 says 26 and 69 (the author's figures, not measured, through three C-80 rounds): a figure correction decision is escalated to the operator before the amendment is sent (staged text with Checks + figures: sha256 93e4c6a41646d07dddace2ee76c9439dc2d8af4067605bbd477f3f082d1c2c5b, 138 lines, pre-send ok).

## Counters (INV-6)

amendments=0 revises=0 questions=0 (round 1 RESULT only; an amendment 1 follows the operator's decision).

## Round 2 (amendment 1, bus 2968)

- RESULT 2969 at 05:52Z: `verdict=accept design_sha256=93e4c6a41646d07dddace2ee76c9439dc2d8af4067605bbd477f3f082d1c2c5b`; accepted (status=accepted, pr=none). Counters: amendments=1 revises=0 questions=0 (S2 not reached).
