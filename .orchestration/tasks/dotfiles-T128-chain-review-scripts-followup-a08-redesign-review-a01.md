---
format: 2
task_id: dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01
kind: review
security: false
allowed_files:
  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01/**
after: []
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01 — INV-6 reset anchor review of dotfiles-T128-chain-review-scripts-followup-a07 by its redesign a08

Drafted 2026-10-21T05:22Z by the orchestrator seat (plan 006 A3 / V3a: a reached INV-6 threshold is silenced only by a design-reset record whose redesign the review of another context accepted). `dotfiles-T128-chain-review-scripts-followup-a07` (PR #439, head a644a7d9) reached S2 (two amendments, one the orchestrator's erroneous resend 2710, M-20261020-03) and its audit found a P1 (review content read from the worker-writable shared object store, design 5.14 item 8); D-024-41 resets the lineage to a08. The a08 text was authored by author-loop (design 1 one round, design 2 two rounds, round 3 under the re-plan line `integration-trust-chain` after the operator's decision D-024-52: a08 keeps only the private-bare-clone local review, the chain's audit-reuse and shared-worktree hardening is owned by `dotfiles-T128-chain-review-scripts-followup-a09` as a release prerequisite, and the two former `closed` claims are residual naming that owner); C-80 of these bytes: `…-text-security-cbc39be.md` Verdict correct.

## What to review

Amendment 1 (2026-10-21T05:51Z, D-024-53): your round 1 finding (RESULT 2967, the empty Checks block) is answered. The a08 text now carries the orchestrator's Checks paste (merge-base b8213131, main a811f133, inherited 27+6 and 94+8 lines, the uv/python host facts) and its B:117 inherited figures are corrected from the recalled 26/69 to the measured 33/102; nothing else changed (138 lines). Judge the new bytes under the same three items; the hash below is the new one.

1. `.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md` at sha256 `93e4c6a41646d07dddace2ee76c9439dc2d8af4067605bbd477f3f082d1c2c5b` is the file you judge; compute the hash yourself (`shasum -a 256`) and stop with `verdict=reject` if it differs.
2. Its front matter names `reset_of: [dotfiles-T128-chain-review-scripts-followup-a07]` and `retained_predecessor_directories`; its items and threat table answer the findings that forced the reset, as `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md` (D-024-41, the audit P1) and `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a08.md` (the three C-80 rounds, the re-plan line) record them; nothing in a08 widens permissions or trust boundaries beyond a07; every residual row names an existing owner file (`dotfiles-T128-chain-review-scripts-followup-a09`, present under `.orchestration/tasks/` with the two obligations added 2026-10-21).
3. The redesign is not dispatched yet (a013 after your accept); your review changes no file and dispatches nothing. Read only.

## Output

`.orchestration/dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01/review.md`: the hash you computed, one line per item above (ok, or the finding with file:line), and the verdict. Then exactly one RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01 status=ready_for_review verdict=accept design_sha256=93e4c6a41646d07dddace2ee76c9439dc2d8af4067605bbd477f3f082d1c2c5b review=.orchestration/dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01/review.md` when every item holds, or `... verdict=reject design_sha256=93e4c6a41646d07dddace2ee76c9439dc2d8af4067605bbd477f3f082d1c2c5b review=...` with the findings in the file. No PR, no commit, no push; the orchestrator writes the reset record from your RESULT.
