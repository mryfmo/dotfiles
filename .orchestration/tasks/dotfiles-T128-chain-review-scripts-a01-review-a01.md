---
format: 2
task_id: dotfiles-T128-chain-review-scripts-a01-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-a01-review-a01 — confirm the task text `dotfiles-T128-chain-review-scripts-a01` (review seat half; Codex headless runs the same check in parallel)

Drafted 2026-10-14 by the orchestrator seat (the bus time of the TASK line is the dispatch time). The reviewed file is `.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md` (untracked; its sha256 is the `crs_task_sha256` of the TASK line), a step-7 short-form task (goal, files, out of scope, one check command, a hand-written threat table) for plan 021 step 6.3: the review-side steps of the integration chain whose logic lives only in the orchestrator's scratchpad become repository scripts with tests (`.orchestration/plans/021-execution-detail-and-scrutiny.md`, "## Step 6.3 inventory"). Its sibling `dotfiles-T128-chain-github-scripts-a01` carries the other side; the two are meant to run concurrently on disjoint files. The attached inputs under `.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/` are the scripts as the chain runs them today (premise 1 holds their hashes); each item restates the input's behaviour and names the changes. One round, fixed stop condition.

## Stop condition

1. Nothing contradicts plan 021 step 6.3 (its inventory table and criterion) or step 7's form: three scripts, one test module, no rule text, no glue; the one premise holds (re-run its command from any checkout and compare; it reads origin/main).
2. `allowed_files` covers every touch point the items name and nothing else; the files are pairwise-disjoint from the sibling task's (`scripts/orchestrator/resolve-threads.sh`, `pr-cost.sh`, `review-receipt.sh`, `tests/unit/test_chain_github_scripts.py`, its evidence directory): confirm by listing both.
3. Each item restates its attached input faithfully (read the input script beside the item: argument form, outputs, exit codes, the written files) and names only the changes the item lists; each `closed` row's test name appears verbatim in item 4 and its described assertions close the row's risk (the review binary resolved before the checkout and run read-only in the worktree at the head, one file written, the dirty-worktree refusal; the rows and lines appended once and the stop on P0/P1; the scan lines); the Completion clause matches plan 020 step 4 (the Bot's single review, one fix round, a surviving P0/P1 to the operator, P2 advisory under the named owner, written when the first appears).
4. The file passes C1 to C10 and C7b (the orchestrator pasted `dotfiles-T128-chain-review-scripts-a01.md: OK`), the brief check (premise OK, mask clean, 15 controls, 1 claim) and `validate-agent-assets.py --mask-secrets` changes nothing in it; the caps hold by construction (three short scripts, one test module).

## Output

`.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-review-a01.md`: the usual header with both sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-chain-review-scripts-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-chain-review-scripts-a01-review-a01 round=1 verdict=confirm|revise crs_task_sha256=<sha> validation=<path>`.

## Round 2 (orchestrator, after the Codex round 1 of 08:36Z)

The Codex half's round 1: P1 premise 3 counted a phrase over the whole plan file, which the orchestrator's 08:45Z status line changed from 8 to 9 (now counted inside the step 6.3 inventory section; M-20261014-11, C-45); P1 item 3 said `<task>.md` where the input reads `${task%-fixtures}.md` (now stated). The sibling dropped `review-receipt.sh`, so the Completion's sibling list names two scripts. Input checker `OK`, 15 controls, 3 claims, mask clean. Same four stop conditions on the new hash (the round-2 TASK line's token); a round-1 RESULT on the old hash is superseded.

## Round 3 (orchestrator, after the seat's round 1 of 08:43Z and the Codex round 2 of 08:41Z)

The seat's round 1 (08:43:35Z, on the round-1 hash): P2 premise 3 read an uncommitted plan file (0 on origin/main) so a worker's replay would block; P2 the row-1 test could not close the resolve-before-checkout claim with CODEX_BIN set in every case; P3 item 3's dropped behaviours (suffix strip, case-insensitive match), P3 item 1's non-zero-exit continuation, P3 the only-path assertion against the default worktree under the repository and the reused file, P3 row 11's tool list. Applied: premises 1 and 3 removed (the inputs and the plan are untracked until the boundary; the inputs' hashes are stated as facts in the intro), the one premise left reads origin/main; the first test gains the CODEX_BIN-unset case with a relative ./bin decoy present only in the head commit, the worktree outside the repository root (ORCH_REVIEW_WORKTREE) and the no-new-path assertion on the main working tree, a second task name for the no-finding run; items 1 and 3 and row 11 state what the seat named. Input checker `OK`, 15 controls, 1 claim, mask clean. Same four stop conditions on the new hash (the round-3 TASK line's token); a RESULT on an older hash is superseded.
