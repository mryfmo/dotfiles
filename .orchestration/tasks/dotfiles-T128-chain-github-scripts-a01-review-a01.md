---
format: 2
task_id: dotfiles-T128-chain-github-scripts-a01-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-chain-github-scripts-a01-review-a01 — confirm the task text `dotfiles-T128-chain-github-scripts-a01` (review seat half; Codex headless runs the same check in parallel)

Drafted 2026-10-14 by the orchestrator seat (the bus time of the TASK line is the dispatch time). The reviewed file is `.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01.md` (untracked; its sha256 is the `cgs_task_sha256` of the TASK line), a step-7 short-form task (goal, files, out of scope, one check command, a hand-written threat table) for plan 021 step 6.3: the GitHub-side steps of the integration chain whose logic lives only in the orchestrator's scratchpad become repository scripts with tests (`.orchestration/plans/021-execution-detail-and-scrutiny.md`, "## Step 6.3 inventory"). Its sibling `dotfiles-T128-chain-review-scripts-a01` carries the other side; the two are meant to run concurrently on disjoint files. The attached inputs under `.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/` are the scripts as the chain runs them today (premise 1 holds their hashes); each item restates the input's behaviour and names the changes. One round, fixed stop condition.

## Stop condition

1. Nothing contradicts plan 021 step 6.3 (its inventory table and criterion) or step 7's form: two scripts (the receipt stays glue), one test module, no rule text, no glue; the one premise holds (re-run its command from any checkout and compare; it reads origin/main).
2. `allowed_files` covers every touch point the items name and nothing else; the files are pairwise-disjoint from the sibling task's (`scripts/orchestrator/local-review.sh`, `local-advisory.sh`, `sandbox-scan.sh`, `tests/unit/test_chain_review_scripts.py`, its evidence directory): confirm by listing both.
3. Each item restates its attached input faithfully (read the input script beside the item: argument form, outputs, exit codes, the written files) and names only the changes the item lists; each `closed` row's test name appears verbatim in item 4 and its described assertions close the row's risk (one reply and one resolution per thread with a row, the missing row left open with exit 3, dry-run writing nothing; the ledger header once and the fields); the Completion clause matches plan 020 step 4 (the Bot's single review, one fix round, a surviving P0/P1 to the operator, P2 advisory under the named owner, written when the first appears).
4. The file passes C1 to C10 and C7b (the orchestrator pasted `dotfiles-T128-chain-github-scripts-a01.md: OK`), the brief check (premise OK, mask clean, 14 controls, 1 claim) and `validate-agent-assets.py --mask-secrets` changes nothing in it; the caps hold by construction (two short scripts, one test module).

## Output

`.orchestration/validation/dotfiles-T128-chain-github-scripts-a01-review-a01.md`: the usual header with both sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-chain-github-scripts-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-chain-github-scripts-a01-review-a01 round=1 verdict=confirm|revise cgs_task_sha256=<sha> validation=<path>`.

## Round 2 (orchestrator, after the Codex round 1 of 08:36Z)

The Codex half's round 1: P1 item 3 added `review-receipt.sh` where plan 021's step 6.3 inventory keeps the receipt as glue (one printf): the script, its closed row, its test, its input file and every mention are removed, so the task lands two scripts (14 controls); premise 3 is counted inside the step 6.3 inventory section (M-20261014-11, C-45) and premise 1 holds the two inputs' hashes. Input checker `OK`, 14 controls, 3 claims, mask clean. Same four stop conditions on the new hash (the round-2 TASK line's token); a round-1 RESULT on the old hash is superseded.

## Round 3 (orchestrator, after the seat's round 1 of 08:43Z and the Codex round 2 of 08:41Z)

The seat's round 1 on the sibling (08:43:35Z) applies here: premises 1 and 3 read untracked files (the inputs, the plan) a worker replaying from origin/main cannot see; both removed, the inputs' hashes stated as facts in the intro, the one premise left reads origin/main. Input checker `OK`, 14 controls, 1 claim, mask clean. Same four stop conditions on the new hash (the round-3 TASK line's token); a RESULT on an older hash is superseded.

## Round 4 (orchestrator, after the seat's round 3 of 08:51Z)

The seat's round 3: P2 the stub keying (item 3 now keys on the API path plus the `--jq` expression, post-filter canned output; `graphql` for the query); P3 item 1's positional arguments, the first-100-threads query and the printed truncations; P3 on this brief: stop conditions 1 and 4 said three scripts and 3 named the receipt's assertions, all corrected. Input checker `OK`, 14 controls, 1 claim, mask clean. Same four stop conditions on the new hash (the round-4 TASK line's token); the Codex half, which confirmed round 3, reviews this hash too.
