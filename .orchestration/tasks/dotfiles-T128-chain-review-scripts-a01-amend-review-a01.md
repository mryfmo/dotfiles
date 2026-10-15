---
format: 2
task_id: dotfiles-T128-chain-review-scripts-a01-amend-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-a01-amend-review-a01 — confirm amendment 1 of `dotfiles-T128-chain-review-scripts-a01` (review seat half; Codex headless runs the same check)

Drafted 2026-10-14 by the orchestrator seat. The worker's question (bus 1149, 09:02:17Z): row 11 listed a subset of the tools the attached inputs run, and a review worktree path that exists but is not a worktree root lets `git -C` act on the enclosing checkout, so a clean main checkout would pass the dirty check and be checked out detached at the PR head; the worker asked for one refusal line, a change beyond item 1, and the answer travels as this amendment. Amended file: `.orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md`, sha256 `b875d2472d2a85c26ad6a225bf5052d0493679faf5ecbdfec03a134885c0e0e5`; the pre-amendment copy is `.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-pre-amend1.md (the pair-confirmed round-3 text, sha256 af6556ba591a742f155fea5a649be9c579b95210dee56104babf4256018fcdd7; the task is not on main)`.

## What changed (amendment 1)

- Row 11 (workflow and interpreter or environment inputs) lists the tools each input runs: local-review.sh adds grep, sort, head and rm; local-advisory.sh adds head and sort.
- Item 1: before the dirty check, the review worktree path must hold a `.git` entry of its own (a worktree root), exit 2 otherwise.
- Item 1 (round 2): the transcript's temporary file comes from `mktemp` with the template `${TMPDIR:-/tmp}/local-review.XXXXXX` (macOS `mktemp` without a template ignores `TMPDIR`; the Bash sandbox denies the per-user directory; the form `orch-gate.sh` uses).
- Item 4, first test: a new case, `ORCH_REVIEW_WORKTREE` naming a plain directory created inside the repository's main working tree: exit 2, the stub not run, the main working tree's HEAD unmoved.
- Row 5 (the review worktree, residual) names both refusals and that amendment 1 adds the non-worktree case to the first closed row's coverage.
- A `## Change (amendment 1 …)` section with the why (bus 1149) and the list above. Nothing else: allowed_files, the other rows, the premise, items 2 and 3, Out of scope, Check and Completion are unchanged.

## Stop condition

1. The diff of the task file against the pre-amendment copy named above contains only what the list above says.
2. For each behaviour the amendment adds or changes in a script or a procedure, name the threat row that covers it; a new effect on a gate input (an acceptance record, a sweep JSON, an audit receipt), on the bus or on the host has its own row with a closing test, added by this amendment (C-28, M-20261012-29). An amendment that adds behaviour without its row is `revise`.
3. Each closed row's named test closes its risk and the test names appear verbatim in the task's test item; the wording agrees with the rule sentences and the sibling tasks it cites.
4. The file passes C1 to C10 and C7b (the orchestrator pasted OK) (no superseded term: the amendment adds; `amend-sweep.sh` has nothing to sweep); the copy rows and the evidence directory are unchanged (the task has no `reset_of`).

## Output

`.orchestration/validation/dotfiles-T128-chain-review-scripts-a01-amend-review-a01.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-chain-review-scripts-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-chain-review-scripts-a01-amend-review-a01 verdict=confirm|revise amended_task_sha256=b875d2472d2a85c26ad6a225bf5052d0493679faf5ecbdfec03a134885c0e0e5 validation=<path>`.

## Round 2 (orchestrator, 09:08Z, after the worker's PONG of 09:05Z)

One more change joins the amendment: item 1 names the `mktemp` template (the list above, second bullet). The task's Change section records it as round 2. Input checker `OK`, 15 controls, 1 claim, mask clean. Same four stop conditions on the new hash (`amended_task_sha256` of the round-2 TASK line); a round-1 RESULT on the old hash is superseded.
