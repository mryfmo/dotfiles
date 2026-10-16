---
task_id: dotfiles-T128-chain-glue-finish-a01
seat: claude-standard-dot-a002
branch: tools/chain-glue-finish
base: 5fd4fe0c
code_commit: af684dc2
fix_commit: 968d3439
pr: 378
task_sha256: 8eb760cc25b1e44050b85366ac8baadafedb863eec6dcfa98e3839a512db7272
---

# Report: dotfiles-T128-chain-glue-finish-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/chain-glue-finish` from `origin/main` `5fd4fe0c` (T7's merge). The PR #377 branch stays in the worktree, committed and pushed, until its acceptance.
- Task file: sha256 `8eb760cc…`, copied byte-identical; the task-consistency check passes on the dispatched file (validation §1). Dispatched 2026-10-16T23:37:33Z. All five premises replay equal (§2). No question and no amendment.
- Input read from the main checkout: the glue's `finish-pr.sh` and `integrate-merge.sh`, and the headers of the scripts the chain calls. Neither glue file is copied into the branch.

## What landed

| File | What it does |
|---|---|
| `scripts/orchestrator/chain-finish.sh` (new, 148 lines) | Item 1, in its order, with T7's helpers (`say`, `refuse`, `pre`, `step`, `pick`), log form and colour setting. **Preconditions**, each exit 10: the arguments; the binaries; the main checkout on `main` and at `origin/main`; the canonical review worktree, clean, with its own `.git`; the extra TSV a file; the head, the review worktree's `HEAD`, equal to the PR's head with its audit summary present; the record; and the gate inputs (the sweep JSON with `pr` equal to the PR, the audit transcript, the receipt, the crit JSON). **Steps:** (1) the verdict and one `audit-finding: <sha7>:<n> not-applicable:<reason>; evidence=<command>` line per finding, under either verdict, with the incorrect verdict's lines as a TSV; (2) `resolve-threads.sh`, exit 3 → 11; (3) the sweep re-run as T7's, `fill_sweep.py`'s exit 1 → 13; (4) the record block, `--audit-dispositions` only when the verdict is incorrect; (5) `orch-gate.sh`; (6) `gh pr merge --squash --match-head-commit <head> <pr>`, then the merge commit from a fresh `origin/main`; (7) `ff-main.sh`; (8) `pr-cost.sh`, run as `HEAD`'s pre-merge copy (the Bot's P1, below); (9) the AGMSG-ACCEPTANCE line printed. An `EXIT` trap removes the comments JSON and both TSVs. |
| `tests/unit/test_chain_glue.py` (extended, 171 lines) | T7's tests are kept. The `SCRIPTS` stubs gain `resolve-threads.sh`, `orch-gate.sh`, `ff-main.sh` and `pr-cost.sh`. Every stub also appends its name to `<calls>/order.log`. The gh stub gains `pr merge` (answering from `<calls>/merge-status`, and logging `gh pr merge` to the order log). The uv stub runs `-c` code with the system `python3 -I`. `send.sh` and `agmsg-dispatch` stubs on PATH log to `<calls>/send.log`. There are four new tests, plus a fifth for the Bot's P1, and a `finish_ready` fixture: the review worktree at the PR head, the gate's inputs, and the record lines. |

## The tests, by closed row

| Closed row | Test |
|---|---|
| the audited head | `test_finish_refuses_a_head_that_differs_from_the_audit`. Exit 10 for each of: no audit summary for the head; a gh head that differs from the worktree's; a task id with `/`; a review worktree elsewhere; no review receipt. In every case no repository stub runs, no `pr merge` is logged, and no log is written. |
| the audit's findings | `test_finish_requires_an_audit_finding_line_per_incorrect_finding`. **Incorrect, two findings, one line:** exit 12 naming finding 2, and `resolve-threads.sh` is not run. With both lines, the record script's argv ends `--ledger <tsv> --audit-dispositions <tsv>`, and its log holds the rows `1<TAB><reason><TAB><evidence>` and `2<TAB>…`. Both TSVs and the comments JSON are gone afterwards. **Correct, three findings (`[P1]`, `- [P2]`, `+ [P3]`):** exit 12 naming finding 3. With its line, the argv holds no `--audit-dispositions`. **`Verdict: unclear`:** exit 12. |
| the order | `test_finish_runs_gate_before_merge_and_cost_after`. The order log equals the exact list: resolve-threads, pr-feedback, fill_sweep, acceptance-front-matter, orch-gate, gh pr merge, ff-main, pr-cost. There is exactly one `pr merge --squash --match-head-commit <head> 7`. Each script's arguments are as item 1 gives them, `ff-main.sh` and `pr-cost.sh` run with the main checkout as cwd, and the log's step names are in order with no path of the temporary tree. With a failing gate stub: exit 1, `step gate failed rc=3`, and the order stops at orch-gate. |
| (the Bot's P1, thread `4300324931`) | `test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward`. The `ff-main` stub's hook overwrites the main checkout's `pr-cost.sh` with a decoy, as a merged PR's change would. The decoy never runs; `HEAD`'s stub runs once with `7` and the main checkout as cwd; and no snapshot file is left. |
| the acceptance line | `test_finish_prints_the_acceptance_line_and_sends_nothing`. The last line matches `^AGMSG-ACCEPTANCE v1 task_id=<task> status=accepted reason=merged-as-<40 hex>-pr-7-head-<sha7> next_action=`, and the sha is `origin/main`'s. `send.sh` and `agmsg-dispatch` log nothing. |

Mutation check (validation §4): 13 mutants, each applied alone and each caught by its test; then the baseline of all 17 tests passes. They remove, in turn: the head check, the gate-input check, the canonical-path check, the finding-line check, the dispositions for an incorrect verdict, the verdict check, the exit trap, the gate step, the `--match-head-commit` binding and the fast-forward. One mutant adds an `agmsg-dispatch` call, one changes the acceptance line's form, and one runs the main checkout's `pr-cost.sh` again (the P1).

## Readings, declared

- **HEAD's scripts and the confined extra TSV:** both carry T7's merged checks (PR #372 threads `4291474880` and `4291474891`). The scripts this chain calls must be tracked in the main checkout and `scripts/` must match `HEAD`. The extra TSV must be a file inside the main checkout, so the log names it by a repository path. Item 1 names neither. Both are exit-10 refusals before any GitHub write.
- **The sweep JSON's `pr`** is read with `<uv> run --no-project python -I -c` (the standard library's `json`), since `jq` is not among the resolved binaries.
- **Nothing is logged before the head is known.** The log, T7's file, is appended from the verdict step on, so a refusal before it goes to stderr only.
- **The finding count** uses the gate's `AUDIT_FINDING` pattern written as an ERE: `^[[:space:]]*([-*+][[:space:]]+)?\[P[0-3]\]`.
- **The dispositions TSV** is written under either verdict and passed only for an incorrect one. The exit trap removes it.
- **A thread left open** (exit 11) and **sweep gaps** (exit 13) have no test of their own: item 2 names none, and their stops are one `refuse` line each.

## Caps

Validation §5: outside `tests/` and `.orchestration/`, 1 file, 148 added lines (cap 200); under `tests/`, 171 added lines (cap 1000).

## CI and the Bot

- **The Bot's first review** (`a8d975c6`, review `5554832605`, 23:48:52Z) left one thread, `4300324931`, P1, "Keep pr-cost on the trusted pre-merge version". It is `fixed:968d3439`, the one fix round. Before the merge, the chain takes `git show HEAD:scripts/orchestrator/pr-cost.sh` into `.orchestration/validation/<task>-pr-cost-<sha7>.sh`, runs it with `${BASH}` and the main checkout as cwd (it finds its repository from its cwd), and removes it in the exit trap. The copy lives under `.orchestration/validation/` so the log names a repository path, not a temporary one.
- **`ff-main.sh` stays in place:** it finds its repository from its own path, so a copy elsewhere would not work. It is the pre-merge script when it starts, and bash keeps reading the file it opened, since git replaces a file by unlinking and creating it.
- **The Bot's re-review** of the fix head (`bot_rounds=2`) and **CI**: in the RESULT.

## Not done, or outside scope

- T7's script and tests, the scripts the chain calls, the glue files and their retirement are unchanged.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
