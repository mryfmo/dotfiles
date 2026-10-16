---
task_id: dotfiles-T128-chain-glue-integrate-a01
seat: claude-standard-dot-a002
branch: tools/chain-glue-integrate
base: fdef3ceb
code_commit: 24f8af19
fix_commit: d8bc67d4
revise_commits: d23cb50c 4a683891 bdb96c86
pr: 372
task_sha256: 62706b88c365e1c21ef7c8b58e10647629f528b3a18b04048eb41a646a016b64
---

# Report: dotfiles-T128-chain-glue-integrate-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/chain-glue-integrate` from `origin/main` `fdef3ceb` (PR #364 merged). The PR #368 branch stays in the worktree untouched.
- Task file: sha256 `62706b88…`, copied byte-identical; the task-consistency check passes on the dispatched file (validation §1). Dispatched 05:54:58Z. All five premises replay equal (§2). No question and no amendment.
- Input read from the main checkout: the glue's `integrate-prep.sh` and `integrate-pr.sh`, `review-receipt.sh` (the receipt's fields) and `record-block.py` (the ledger regex), and the headers of the scripts the chain calls. None of them is copied into the branch.

## What landed

| File | What it does |
|---|---|
| `scripts/orchestrator/chain-integrate.sh` (new, 180 lines; the plan allows 180) | Item 1, in its order. Arguments checked first: task and owner ids by `^[A-Za-z0-9][A-Za-z0-9._-]*$`, whose leading class excludes `.` and `..`, the PR by digits, `<main>` made physical. The binaries are resolved with `mise which` under `env -i`, else `command -v`; a path not absolute or under `shims` is exit 10. Preconditions: on `main`; after `fetch origin main`, `HEAD` equals `origin/main` (else `ff-main.sh` named); the review worktree's `pwd -P` equals `$(git -C <main> rev-parse --show-toplevel)/.claude/worktrees/orchestrator-review`, with its own `.git` and clean; each called repository script tracked in the main checkout, with `scripts/` unchanged from `HEAD` there (the Bot's P1, below); the record present; `isDraft` is `false`; then `fetch origin main` in the review worktree, and an extra TSV, when given, must resolve inside the main checkout (revise round, thread `4291474891`). Steps 1 to 10 follow, each command logged by one `step` helper as `<utc> <step> rc=<n>: <command>` and echoed as `<step> rc=<n>`. The helper takes each step's accepted statuses, and any other status is `step <name> failed rc=<n>` and exit 1, so no called script's status is returned as the chain's. The chain's own refusals are 10 to 16. |
| `tests/unit/test_chain_glue.py` (new, 408 lines) | Item 2: a bare origin with `main` and `refs/pull/7/head`, a main checkout and a review worktree at the canonical path, both clones of it; STUB-template repository scripts, tracked on the origin's `main`; `gh`, `uv`, `codex` and a failing `mise` first on `PATH=<stubs>:/usr/bin:/bin`. The six tests, one per closed row; a seventh for the Bot's P1; two for revise round 1; two for revise round 2. |

## The tests, by closed row

| Closed row | Test |
|---|---|
| main checkout on `main` | `test_integrate_refuses_when_main_is_not_on_main`. Exit 10 for each of: a task id with `/`, `..` or a leading `.`; a non-digit PR; a review worktree elsewhere; a draft PR (no log, no stub run, no `refs/remotes/pr/7`); a main checkout on `x` (likewise); a head already audited (only `fetch` in the log, no stub run); a main checkout one commit behind (`ff-main.sh` on stderr). |
| steps in order, each logged | `test_integrate_runs_the_steps_in_order_and_logs_each`. The log's step names equal the twelve-name list exactly. Each stub ran once with item 1's arguments and with the main checkout as its cwd, and `ORCH_REVIEW_WORKTREE` is the review worktree. The log holds no path of the temporary tree. The ledger TSV keeps the ten-digit and `audit:` rows and drops `local:` and a nine-digit id. The comments are one JSON array, and they and the TSV are deleted afterwards. The crit record and the receipt carry the fields of item 1 (8). |
| restart after update-branch | `test_integrate_restarts_after_update_branch`. Origin `main` has advanced, the main checkout is at it, and only the review worktree lags. `pr update-branch 7` runs once, followed by a `pr view` poll. The merged head's log holds two pull fetches for each checkout, while the first head's log holds one. The merged head is in both object databases, is checked out in the review worktree, and is named on the last line. |
| binaries resolved before the checkout | `test_integrate_resolves_binaries_before_the_checkout`. The head commits a decoy `gh` at the review worktree's root and a decoy `scripts/orchestrator/local-review.sh`, with `.` first on PATH. Neither decoy runs, and the main checkout's local-review stub does. The Bot wait ends `absent`. |
| owner task absent | `test_integrate_refuses_an_absent_owner_task_before_the_advisory_step`. With local review exit 3 and no owner file: exit 15, `write the owner task <owner> first`, and no `local-advisory.sh` or later step. |
| (the Bot's P1, thread `4291474880`: no closed row yet) | `test_integrate_refuses_a_main_checkout_script_that_is_not_heads`. A called stub changed in the main checkout: exit 10, `scripts/ in the main checkout differs from HEAD`. A stub removed from the index: exit 10, `<path> is not tracked in the main checkout`. In both, no stub runs and no log is written. |
| (revise round, thread `4291474885`) | `test_integrate_restarts_when_the_base_moves_during_the_waits`. A hook in the `gh` stub pushes a commit to origin `main` during `pr checks`. The first head's log runs checks, bot, and then three `base` lines (the re-fetch, the failed ancestry test, the update-branch), with no sandbox scan. `pr update-branch 7` runs once. The merged head's log has its own `checks` line, local review runs once on the merged head, and the last line names it. |
| (revise round, thread `4291474891`) | `test_integrate_refuses_an_extra_tsv_outside_the_main_checkout`. An extra TSV in the temporary tree, outside the main checkout: exit 10, with no stub run and no log. An extra TSV under `<main>/.orchestration/` runs; `fill_sweep.py` gets the absolute path, and the log names `.orchestration/extra.tsv` and no path of the temporary tree. |
| (revise round 2, the local review of `2fe135c5`, P2) | `test_integrate_refuses_a_stale_main_checkout_after_the_restart`. The PR is behind, and a hook in the `gh` stub's `update-branch` pushes origin `main` again. After the restart the main checkout is behind, which `local-review.sh` would diff against: exit 10 with the `ff-main.sh` guidance. `update-branch` runs once, and no sandbox scan, local review or audit runs. The during-waits test's hook now also fast-forwards the main checkout, as the orchestrator's `ff-main.sh` would, so that test keeps covering the success path. |
| (revise round 2, P1) | `test_integrate_restores_the_review_worktree_after_the_audit`. A hook in the audit stub checks the review worktree out at `origin/main`, as `orch-audit.sh` leaves it. After the chain the review worktree is at the audited head, and the log's last step line is `audit rc=0: git -C .claude/worktrees/orchestrator-review checkout -q --detach <head>`. |
| sandbox-scan hit | `test_integrate_stops_on_a_sandbox_scan_hit`. A hit is exit 16 naming `CHAIN_SCAN_JUDGED=<sha7>`, and no later stub runs. The re-run with it proceeds and logs `sandbox scan: judged by the orchestrator`. |

Mutation check (validation §4): 17 mutants, each applied alone, all 17 caught, then a baseline run of the six tests, OK. They remove, in turn: the off-main refusal, the draft refusal, the already-audited refusal, the checks step, the ten-digit ledger bound, the comment join, the restart, the log reset, the main-checkout script path, the owner check, the scan stop, the P1 fix's two checks (the `HEAD` diff and the tracked-file check), revise round 1's two (the re-check after the waits and the extra-TSV check), and revise round 2's two (the freshness re-check after a restart and the restore after the audit). The no-restart mutant now makes the first ancestry test always pass. The restart test catches it, because it asserts that a head behind the base waits for no CI (`4a683891`).

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

Validation §5: outside `tests/` and `.orchestration/`, 1 file, 180 added lines (cap 200; the plan's 180 for the script); under `tests/`, 408 added lines (cap 1000).

## CI and the Bot

- **The Bot's first review** (`9f1cee1c`, review `5543747032`, 06:14:19Z) left three threads:
  - `4291474880`, P1, "Refuse modified main-checkout scripts": fixed in `d8bc67d4` (the one fix round). Each called script must be tracked in the main checkout, and `scripts/` there must not differ from `HEAD`; otherwise exit 10 before any fetch. The tests' stubs are now tracked on the origin's `main`, so the other six tests run against `HEAD`'s copies. The Bot also asks for a main-worktree-content row in the threat table. The task file is the orchestrator's, so the row is proposed in the RESULT, not added here.
  - `4291474885`, P2, "Recheck origin/main after the waits": `origin/main` can advance during the checks or Bot wait, after the ancestry test. The proposed disposition is a C-50 revise round: re-run the review worktree's `fetch origin main` and the ancestry test before the local review, restarting at the fetch. That is a few lines plus one test.
  - `4291474891`, P2, "Redact external disposition paths from the log": an extra TSV outside the main checkout is logged by its absolute path. The proposed disposition is a C-50 revise round: refuse an extra TSV outside `<main>`, or log only its basename. One line plus one test.
- **The Bot's re-review** (`bot_rounds=2`): `@codex review` at 06:18:43Z. The answer was issue comment `6209443752` at 06:21:43Z, "Didn't find any major issues", Reviewed commit `5ed27e9212`.
- **Revise round 1** (the orchestrator's ACCEPTANCE `status=revise`, 08:27:28Z; C-50) had both P2s:
  - `4291474885`: `fixed:d23cb50c`. After the checks and the Bot wait, the chain fetches `origin main` into the review worktree again and re-runs the ancestry test. A base that moved goes to the same update-branch path, which restarts at the fetch (bounded as before: at most two update-branches, and a third ancestry failure is exit 13).
  - `4291474891`: `fixed:d23cb50c`. An extra TSV must resolve inside the main checkout, else exit 10 before any fetch, so the log names it by a repository path.
  - The orchestrator added the main-worktree-content threat row to the task file as a Change note (validation §1).
  - No new Bot wait, per the revise message.
- **Revise round 2** (ACCEPTANCE `status=revise`, 2026-10-16T21:49:05Z; operator decision D-S2-372-A, INV-6 S2 waived for this PR) had the local review's two findings on `2fe135c5`, the orchestrator's update-branch head of `a6d6c1c9`:
  - P1, line 177: `fixed:bdb96c86`. `orch-audit.sh` checks the shared review worktree out at `origin/main` and does not restore it, so the gate would read the wrong head. The chain keeps the verdict line, checks the audited head out again as the last `audit` step, and only then prints the verdict.
  - P2, lines 121 to 126: `fixed:bdb96c86`. The main checkout's freshness check is now a function, `fresh` (the fetch, then `HEAD` against `origin/main`, else exit 10 naming `ff-main.sh`). It runs at the preconditions and again after every update-branch, before the restart. The chain does not fast-forward the main checkout itself; that stays the orchestrator's step, as item 1 says.
  - No new Bot wait. CI is in the RESULT.

## Not done, or outside scope

- T8's steps, the scripts the chain calls, and the glue files are unchanged.
- The first mutation run printed `(sed changed nothing)` for its top-level-line mutants: the diff filter matched only indented lines. The filter was fixed and the run repeated; §4 is the second run.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
