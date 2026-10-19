---
task_id: dotfiles-T128-chain-review-scripts-followup-a06
seat: claude-standard-dot-a011
branch: tools/chain-review-scripts-followup-a06
base: 1eac64a8 (origin/main, PR #402's squash merge)
task_sha256: e21ef5bef826e9d5c195d8145c26810c2fa438cf1c4a86b16ba7477d23d14749
---

# Report: dotfiles-T128-chain-review-scripts-followup-a06

- Seat: `claude-standard-dot-a011` in `.claude/worktrees/worker-d`. The branch `tools/chain-review-scripts-followup-a06` was created with `--no-track` from `origin/main` `1eac64a8`, after a single-command `git fetch origin main`. PR #375's branch, the previous task, was clean and pushed before the switch.
- Task file: `e21ef5be…`, copied byte-identical to `.orchestration/dotfiles-T128-chain-review-scripts-followup-a06/task.md` (`67b66f68`). The task-consistency check passes (validation §1).
- The owned rows are those under `## Owned by dotfiles-T128-chain-review-scripts-followup-a06` in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a05.md`, read at dispatch (validation §2). There is one: `audit:c646472:1`.

## Row audit:c646472:1 (evidence-reconciliation)

The finding, from the task-level audit of PR #402's head `c6464729`: a05's `sandbox.md` lists planned gh commands with placeholders and conditional execution rather than completed calls. The a05 report says the seat stopped before PR creation, while the acceptance record says the orchestrator created PR #402.

**What this task does.** `.orchestration/dotfiles-T128-chain-review-scripts-followup-a06/a05-gh-calls.md` records the calls that ran, one row per call, with the seat, the UTC time, the outcome and the evidence:

- a007's push and blocked PONG (2026-10-17T16:46:39Z);
- the orchestrator's draft PR creation (23:39:20Z);
- this seat's `gh pr ready 402` (2026-10-18T04:37:04Z, item 0 of `dotfiles-T133-ci-efficiency-a01`);
- no `@codex review` at all;
- the chain's two update-branches (2026-10-19T12:02:36Z and 13:03:44Z) and its reads;
- the orchestrator's squash merge (20:05:25Z, `1eac64a8`).

**The evidence behind it.**

- GitHub's own data for PR #402 (validation §4): `createdAt`, the timeline events, the comments, the reviews, `mergedAt` and `mergeCommit`. GitHub shows one shared account for every action.
- The seat for each action comes from the regime records (validation §5): the a05 acceptance record (lines 7, 128, 129, 153, 159 and 160), and this seat's own ci-efficiency-a01 sandbox record (lines 10 and 19) and acceptance record (line 32).
- The record also states that the a05 report and the acceptance record do not contradict each other: the worker stopped, and the orchestrator created the PR.

**Where it is written.** The a05 `sandbox.md` itself is unchanged. Checker C2 keeps another task's `.orchestration/<id>/` directory out of a worker's `allowed_files`, so an amendment could not add it. The correction is therefore this task's own record, which names the lines of the a05 record it supersedes: lines 19 to 21, the planned gh command rows 2 to 4 of its ledger (validation §7, a pasted `grep -n` of that file; line 18 is the row of the blocked PONG, an `agmsg-dispatch` call that did run). The regime-ci follow-up a01 settled the same case the same way.

**No code, no test.** The owned row names no test and no code. Its subject is a record, so its red-then-green is the record it names.
- The red side is the a05 ledger's planned rows: placeholders and conditional execution, quoted in validation §3 and §7.
- The green side is `a05-gh-calls.md`: one row per call that ran, each checked against pasted command output in validation §2 to §5.

The task text's item 1 sentence ("its fix and one red-then-green test in `tests/unit/test_chain_review_scripts.py`") applies to rows that name a test. So `scripts/orchestrator/local-advisory.sh` and `tests/unit/test_chain_review_scripts.py` are unchanged.

**Not read.** The team-wide bus history. A whole-bus `history.sh` read started for this record had not finished when the record was committed (C-53: such reads take close to an hour). The seat of the PR creation therefore rests on the orchestrator's own acceptance record, which is the authority on the orchestrator's actions.

## The Check

The Check of `.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a05.md`, as written (validation §6):

- `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v`: 18 tests OK.
- `shellcheck scripts/orchestrator/local-advisory.sh`: clean.
- Caps: 0 changed lines outside `tests/` and `.orchestration/` (cap 200), and 0 added under `tests/` (cap 1000).
- No local Bats ran.

## Changed files

Only `.orchestration/dotfiles-T128-chain-review-scripts-followup-a06/**`: `task.md`, `a05-gh-calls.md`, this report, `validation.md`, `sandbox.md` and `learning.md`.

## Evidence, review, cost

- Evidence in `.orchestration/dotfiles-T128-chain-review-scripts-followup-a06/`.
- No worker review ran. The change is one record, and every claim in it is a pasted command output in validation §2 to §5.
- precheck: pending-411 (`scripts/orchestrator/result-precheck.sh` is not on main).
- No Understand-Anything hook prompt fired, and no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
