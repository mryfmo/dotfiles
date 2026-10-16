---
task_id: dotfiles-T128-chain-glue-integrate-a01
seat: claude-standard-dot-a002
branch: tools/chain-glue-integrate
base: fdef3ceb
code_commit: 24f8af19
task_sha256: 62706b88c365e1c21ef7c8b58e10647629f528b3a18b04048eb41a646a016b64
---

# Report: dotfiles-T128-chain-glue-integrate-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/chain-glue-integrate` from `origin/main` `fdef3ceb` (PR #364 merged). The PR #368 branch stays in the worktree untouched.
- Task file: sha256 `62706b88…`, copied byte-identical; the task-consistency check passes on the dispatched file (validation §1). Dispatched 05:54:58Z. All five premises replay equal (§2). No question and no amendment.
- Input read from the main checkout: the glue's `integrate-prep.sh` and `integrate-pr.sh`, `review-receipt.sh` (the receipt's fields) and `record-block.py` (the ledger regex), and the headers of the scripts the chain calls. None of them is copied into the branch.

## What landed

| File | What it does |
|---|---|
| `scripts/orchestrator/chain-integrate.sh` (new, 180 lines, the plan's allowance) | Item 1, in its order. Arguments checked first: task and owner ids by `^[A-Za-z0-9][A-Za-z0-9._-]*$`, whose leading class excludes `.` and `..`, the PR by digits, `<main>` made physical. The binaries are resolved with `mise which` under `env -i`, else `command -v`; a path not absolute or under `shims` is exit 10. Preconditions: on `main`; after `fetch origin main`, `HEAD` equals `origin/main` (else `ff-main.sh` named); the review worktree's `pwd -P` equals `$(git -C <main> rev-parse --show-toplevel)/.claude/worktrees/orchestrator-review`, with its own `.git` and clean; the record present; `isDraft` is `false`; then `fetch origin main` in the review worktree. Steps 1 to 10 follow, each command logged by one `step` helper as `<utc> <step> rc=<n>: <command>` and echoed as `<step> rc=<n>`. The helper takes each step's accepted statuses, and any other status is `step <name> failed rc=<n>` and exit 1, so no called script's status is returned as the chain's. The chain's own refusals are 10 to 16. |
| `tests/unit/test_chain_glue.py` (new, 317 lines) | Item 2: a bare origin with `main` and `refs/pull/7/head`, a main checkout and a review worktree at the canonical path, both clones of it; STUB-template repository scripts in the main checkout; `gh`, `uv`, `codex` and a failing `mise` first on `PATH=<stubs>:/usr/bin:/bin`. The six tests, one per closed row. |

## The six tests, by closed row

| Closed row | Test |
|---|---|
| main checkout on `main` | `test_integrate_refuses_when_main_is_not_on_main`. Exit 10 for each of: a task id with `/`, `..` or a leading `.`; a non-digit PR; a review worktree elsewhere; a draft PR (no log, no stub run, no `refs/remotes/pr/7`); a main checkout on `x` (likewise); a head already audited (only `fetch` in the log, no stub run); a main checkout one commit behind (`ff-main.sh` on stderr). |
| steps in order, each logged | `test_integrate_runs_the_steps_in_order_and_logs_each`. The log's step names equal the twelve-name list exactly. Each stub ran once with item 1's arguments and with the main checkout as its cwd, and `ORCH_REVIEW_WORKTREE` is the review worktree. The log holds no path of the temporary tree. The ledger TSV keeps the ten-digit and `audit:` rows and drops `local:` and a nine-digit id. The comments are one JSON array, and they and the TSV are deleted afterwards. The crit record and the receipt carry the fields of item 1 (8). |
| restart after update-branch | `test_integrate_restarts_after_update_branch`. Origin `main` has advanced, the main checkout is at it, and only the review worktree lags. `pr update-branch 7` runs once, followed by a `pr view` poll. The merged head's log holds two pull fetches for each checkout, while the first head's log holds one. The merged head is in both object databases, is checked out in the review worktree, and is named on the last line. |
| binaries resolved before the checkout | `test_integrate_resolves_binaries_before_the_checkout`. The head commits a decoy `gh` at the review worktree's root and a decoy `scripts/orchestrator/local-review.sh`, with `.` first on PATH. Neither decoy runs, and the main checkout's local-review stub does. The Bot wait ends `absent`. |
| owner task absent | `test_integrate_refuses_an_absent_owner_task_before_the_advisory_step`. With local review exit 3 and no owner file: exit 15, `write the owner task <owner> first`, and no `local-advisory.sh` or later step. |
| sandbox-scan hit | `test_integrate_stops_on_a_sandbox_scan_hit`. A hit is exit 16 naming `CHAIN_SCAN_JUDGED=<sha7>`, and no later stub runs. The re-run with it proceeds and logs `sandbox scan: judged by the orchestrator`. |

Mutation check (validation §4): 11 mutants, each applied alone, all 11 caught, then a baseline run of the six tests, OK. They remove, in turn: the off-main refusal, the draft refusal, the already-audited refusal, the checks step, the ten-digit ledger bound, the comment join, the restart, the log reset, the main-checkout script path, the owner check and the scan stop.

## Readings, declared

- **Comments across pages:** item 1 says `gh api …/comments --paginate` into the file. Paginated `gh api` writes one JSON array per page back to back, which `fill_sweep.py`'s `json.loads` refuses beyond one page (30 comments). The chain reads `--paginate --jq '.[]'`, one compact object per line, and writes them joined as one array. The test's two comments, one of them with a comma and a newline in its body, come back as one array.
- **Logged commands:** each logs the binary's basename, with the main checkout's prefix replaced by a relative path or `.`, so the log names repository paths only (D7). The `<utc>` stamps are from the resolved `date`.
- **The log across a restart:** lines before the head is known are kept in memory and written when the log is opened. After `update-branch` the first head's log ends, and the merged head's log takes every line of the run.
- **`shasum`** is resolved and checked as item 1 lists it, but no step hashes, so it is not called.
- **The local review's exit 4** (the review binary failed), like its exit 2, is a failed step, exit 1: only 0 and 3 are accepted.
- **The verdict** on the last line is `orch-audit.sh`'s last output line (its header: the verdict line is printed).
- **`fill_sweep.py`'s exit 1** is exit 14 with the `gaps <n>` its summary line prints.
- **The receipt** has two `printf`s writing the two files. The log records them as `receipt rc=0: printf > <file>`.
- **The record step's `grep`** is `/usr/bin/grep` by absolute path (coreutils, as in the other repository scripts); exit 1, no row, is accepted.

## Caps

Validation §5: outside `tests/` and `.orchestration/`, 1 file, 180 added lines (cap 200; the plan's 180 for the script); under `tests/`, 317 added lines (cap 1000).

## CI and the Bot

In the RESULT (the post-ready calls are planned in sandbox.md).

## Not done, or outside scope

- T8's steps, the scripts the chain calls, and the glue files are unchanged.
- The first mutation run printed `(sed changed nothing)` for its top-level-line mutants: the diff filter matched only indented lines. The filter was fixed and the run repeated; §4 is the second run.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
