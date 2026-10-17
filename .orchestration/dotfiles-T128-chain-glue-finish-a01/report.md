---
task_id: dotfiles-T128-chain-glue-finish-a01
seat: claude-standard-dot-a006
earlier_seat: claude-standard-dot-a002
branch: tools/chain-glue-finish
base: 5fd4fe0c
code_commit: af684dc2
fix_commit: 968d3439
revise_commit: 60cdac47
revise2_commit: 2171d927
fixture_commit: 14033382
revise3_commit: 4d4e3b22
pr: 378
task_sha256: 8eb760cc25b1e44050b85366ac8baadafedb863eec6dcfa98e3839a512db7272
---

# Report: dotfiles-T128-chain-glue-finish-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/chain-glue-finish` from `origin/main` `5fd4fe0c` (T7's merge). The PR #377 branch stays in the worktree, committed and pushed, until its acceptance.
- Revise round 3 seat: `claude-standard-dot-a006`, which took the task over in the same worktree from `claude-standard-dot-a002` after the operator re-seated it (ACCEPTANCE round 3 `status=revise`, bus 2026-10-17T07:34:11Z). Before the round the branch was fast-forwarded to the orchestrator's update-branch head `f20826e2`, the ACCEPTANCE's `previous_head`.
- Task file: sha256 `8eb760cc…`, copied byte-identical; the task-consistency check passes on the dispatched file (validation §1). Dispatched 2026-10-16T23:37:33Z. All five premises replay equal (§2). No question and no amendment.
- Input read from the main checkout: the glue's `finish-pr.sh` and `integrate-merge.sh`, and the headers of the scripts the chain calls. Neither glue file is copied into the branch.

## What landed

| File | What it does |
|---|---|
| `scripts/orchestrator/chain-finish.sh` (new, 166 lines) | Item 1, in its order, with T7's helpers (`say`, `refuse`, `pre`, `step`, `pick`), log form and colour setting. **Preconditions**, each exit 10: the arguments; the binaries; the main checkout on `main` and at `origin/main`; the canonical review worktree, clean, with its own `.git`; the extra TSV a file; the head, the review worktree's `HEAD`, equal to the PR's head with its audit summary present; the record; and the gate inputs (the sweep JSON with `pr` equal to the PR and, since revise round 3, `head_sha` equal to the head, the audit transcript, the receipt, the crit JSON). **Steps:** (1) the verdict and one `audit-finding: <sha7>:<n> not-applicable:<reason>; evidence=<command>` line per finding, under either verdict, with the incorrect verdict's lines as a TSV; (2) `resolve-threads.sh`, exit 3 → 11; (3) the sweep re-run as T7's, `fill_sweep.py`'s exit 1 → 13; (4) the record block, `--audit-dispositions` only when the verdict is incorrect; (5) `orch-gate.sh`; (6) `gh pr merge --squash --match-head-commit <head> <pr>`, then the merge commit from a fresh `origin/main`; (7) `ff-main.sh`; (8) `pr-cost.sh`, run as `HEAD`'s pre-merge copy (the Bot's P1, below); (9) the AGMSG-ACCEPTANCE line printed. An `EXIT` trap removes the comments JSON and both TSVs. |
| `tests/unit/test_chain_glue.py` (extended, 242 lines added, 1 changed) | T7's tests are kept. The `SCRIPTS` stubs gain `resolve-threads.sh`, `orch-gate.sh`, `ff-main.sh` and `pr-cost.sh`. Every stub also appends its name to `<calls>/order.log`. The gh stub gains `pr merge` (answering from `<calls>/merge-status`, and logging `gh pr merge` to the order log). The uv stub runs `-c` code with the system `python3 -I`. `send.sh` and `agmsg-dispatch` stubs on PATH log to `<calls>/send.log`. There are four new tests, plus a fifth for the Bot's P1 a sixth for revise round 1 three for revise round 2 and one for revise round 3, and a `finish_ready` fixture: the review worktree at the PR head, the gate's inputs, and the record lines. |

## The tests, by closed row

| Closed row | Test |
|---|---|
| the audited head | `test_finish_refuses_a_head_that_differs_from_the_audit`. Exit 10 for each of: no audit summary for the head; a gh head that differs from the worktree's; a task id with `/`; a review worktree elsewhere; no review receipt. In every case no repository stub runs, no `pr merge` is logged, and no log is written. |
| the audit's findings | `test_finish_requires_an_audit_finding_line_per_incorrect_finding`. **Incorrect, two findings, one line:** exit 12 naming finding 2, and `resolve-threads.sh` is not run. With both lines, the record script's argv ends `--ledger <tsv> --audit-dispositions <tsv>`, and its log holds the rows `1<TAB><reason><TAB><evidence>` and `2<TAB>…`. Both TSVs and the comments JSON are gone afterwards. **Correct, three findings (`[P1]`, `- [P2]`, `+ [P3]`):** exit 12 naming finding 3. With its line, the argv holds no `--audit-dispositions`. **`Verdict: unclear`:** exit 12. |
| (revise round 1, the Bot's P2, thread `4300359437`) | `test_finish_checks_each_audit_finding_line_in_full`. A correct verdict with one finding, and its line in five bad forms: no `; evidence=`, two of them, an empty command, a reason under 20 characters, a tab. Each is exit 12 naming the finding, and `resolve-threads.sh` is not run. With a good line, the chain proceeds. |
| (revise round 2, P1) | `test_finish_runs_pr_cost_with_a_path_of_resolved_links`. The `pr-cost` stub logs a PATH of exactly `.orchestration/validation/<task>-pr-cost-bin-<sha7>`; that directory is gone afterwards, and the log names no temporary path. With a `jq` that resolves only to a `shims` directory first on PATH: exit 10, `no jq for pr-cost.sh outside a shims directory`, before any GitHub write. The repository stubs keep their calls directory as a baked-in default, since `env -i` drops `CALLS`. |
| (revise round 2, P2) | `test_finish_reads_the_last_nonblank_line_as_the_verdict`. A summary whose verdict is `  Verdict: correct  ` followed by blank lines is read as `Verdict: correct`. |
| (revise round 2, P2) | `test_finish_counts_the_trimmed_reason`. A reason of `short` and thirty spaces is 35 characters untrimmed and 5 trimmed: exit 12, and `resolve-threads.sh` is not run. |
| (revise round 3, the local review's P1, `local:f20826e:1`) | `test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head`. The review worktree and the PR are at the head, and the sweep JSON's `head_sha` is `0`×40: exit 10, `the sweep JSON is head <stale>'s, not the audited head <head>'s`. No repository stub runs, the only gh call is the precondition read `pr view 7 --json headRefOid --jq .headRefOid`, and no log is written. With the sweep at the head, the chain proceeds and `resolve-threads.sh` runs once. The `finish_ready` fixture's sweep carries `head_sha` from this round on. |
| the order | `test_finish_runs_gate_before_merge_and_cost_after`. The order log equals the exact list: resolve-threads, pr-feedback, fill_sweep, acceptance-front-matter, orch-gate, gh pr merge, ff-main, pr-cost. There is exactly one `pr merge --squash --match-head-commit <head> 7`. Each script's arguments are as item 1 gives them, `ff-main.sh` and `pr-cost.sh` run with the main checkout as cwd, and the log's step names are in order with no path of the temporary tree. With a failing gate stub: exit 1, `step gate failed rc=3`, and the order stops at orch-gate. |
| (the Bot's P1, thread `4300324931`) | `test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward`. The `ff-main` stub's hook overwrites the main checkout's `pr-cost.sh` with a decoy, as a merged PR's change would. The decoy never runs; `HEAD`'s stub runs once with `7` and the main checkout as cwd; and no snapshot file is left. |
| the acceptance line | `test_finish_prints_the_acceptance_line_and_sends_nothing`. The last line matches `^AGMSG-ACCEPTANCE v1 task_id=<task> status=accepted reason=merged-as-<40 hex>-pr-7-head-<sha7> next_action=`, and the sha is `origin/main`'s. `send.sh` and `agmsg-dispatch` log nothing. |

Mutation check (validation §4): 22 mutants, each applied alone and each caught by its test; then the baseline of all 21 tests passes. They remove, in turn: the head check, the gate-input check, the canonical-path check, the finding-line check, the dispositions for an incorrect verdict, the verdict check, the exit trap, the gate step, the `--match-head-commit` binding and the fast-forward. One mutant adds an `agmsg-dispatch` call, one changes the acceptance line's form, one runs the main checkout's `pr-cost.sh` again (the P1), and five remove the revise round's grammar check whole or one test at a time: the 20-character reason, the command's text, the second delimiter, the tab. Revise round 2 adds four: the `env -i` tool PATH, the tools' shims check, the last-line verdict and the trimmed reason. Those nine, and the moved pr-cost mutant, are literal string replacements in Python, since the first try in `perl` changed nothing: perl interpolates `${n}` even inside `\Q…\E`. Revise round 3 adds one mutant, the new refusal line deleted, caught by its test (validation §6); §4's set was not re-run. The new test also fails on `f20826e2`'s script, before the fix (§6).

## Readings, declared

- **HEAD's scripts and the confined extra TSV:** both carry T7's merged checks (PR #372 threads `4291474880` and `4291474891`). The scripts this chain calls must be tracked in the main checkout and `scripts/` must match `HEAD`. The extra TSV must be a file inside the main checkout, so the log names it by a repository path. Item 1 names neither. Both are exit-10 refusals before any GitHub write.
- **The sweep JSON's `pr`** is read with `<uv> run --no-project python -I -c` (the standard library's `json`), since `jq` is not among the resolved binaries.
- **"No gh call" in the round-3 check** is read as no GitHub write, as its semantics line says ("before any GitHub write"). The sweep check sits beside the existing `pr` check, so nothing moved, and that is after the precondition read `gh pr view <pr> --json headRefOid`. The refusal case therefore asserts that this read is the only gh call and that no repository stub runs. The sweep's `pr` and `head_sha` are read in one `python -I -c` call; a missing `head_sha` prints `none` and refuses.
- **Nothing is logged before the head is known.** The log, T7's file, is appended from the verdict step on, so a refusal before it goes to stderr only.
- **The finding count** uses the gate's `AUDIT_FINDING` pattern written as an ERE: `^[[:space:]]*([-*+][[:space:]]+)?\[P[0-3]\]`.
- **The dispositions TSV** is written under either verdict and passed only for an incorrect one. The exit trap removes it.
- **A thread left open** (exit 11) and **sweep gaps** (exit 13) have no test of their own: item 2 names none, and their stops are one `refuse` line each.

## Caps

Validation §6, at `4d4e3b22`: outside `tests/` and `.orchestration/`, 1 file, 166 added lines (cap 200); under `tests/`, 242 added lines and 1 deleted (cap 1000 added). §5 holds the round-2 figures (164 / 227).

## CI and the Bot

- **The Bot's first review** (`a8d975c6`, review `5554832605`, 23:48:52Z) left one thread, `4300324931`, P1, "Keep pr-cost on the trusted pre-merge version". It is `fixed:968d3439`, the one fix round. Before the merge, the chain takes `git show HEAD:scripts/orchestrator/pr-cost.sh` into `.orchestration/validation/<task>-pr-cost-<sha7>.sh`, runs it with `${BASH}` and the main checkout as cwd (it finds its repository from its cwd), and removes it in the exit trap. The copy lives under `.orchestration/validation/` so the log names a repository path, not a temporary one.
- **`ff-main.sh` stays in place:** it finds its repository from its own path, so a copy elsewhere would not work. It is the pre-merge script when it starts, and bash keeps reading the file it opened, since git replaces a file by unlinking and creating it.
- **The Bot's re-review** (`bot_rounds=2`): `@codex review` at 23:53:58Z. Review `5554892210` on `72d0cd07` at 23:57:03Z had no P0 or P1 and one new P2, thread `4300359437`, "Validate the entire audit-finding disposition".
- **Revise round 1** (the orchestrator's ACCEPTANCE `status=revise`, 2026-10-17T00:05:09Z; C-50) took that P2: `fixed:60cdac47`. Each `audit-finding` line is read in the gate's grammar (`parse_disposition` in `scripts/require-crit-review.py`): exactly one `; evidence=` with a command that is not blank, and a non-empty reason. Added to that: the reason must be at least 20 characters (`FAILURE_REASON_MIN_CHARS`, the record script's minimum, which the Bot asks for), and the line must hold no tab, since the lines become a TSV. Under either verdict a bad line is exit 12 before any GitHub write. No new Bot wait.
- **Revise round 2** (ACCEPTANCE `status=revise`, 2026-10-17T02:21:35Z) took the local review of `f4d86ee5`, the orchestrator's update-branch head of `9d5b9d29`:
  - **P1, lines 147-148:** `fixed:2171d927`. The saved `pr-cost.sh` ran bare `git`, `gh`, `jq` and `date` through the post-merge checkout's mise shims. Now its tools are resolved as `orch-gate.sh` resolves gh and git (`mise which` under `env -i`, else `command -v`; a `shims` path refuses, exit 10). That happens before any GitHub write, into links under `.orchestration/validation/<task>-pr-cost-bin-<sha7>/`, which the exit trap removes. The tools are `gh`, `git`, `jq`, `awk`, `date`, `mkdir`, `tr`, `wc` and `tail`, every command `pr-cost.sh` runs by name; its `grep` is `/usr/bin/grep`. The copy then runs as `env -i PATH=<that directory> HOME=<HOME> bash <copy> <pr>`, inside a `cost_run` function, so HOME stays out of the log line.
  - **P2, lines 101-102:** `fixed:2171d927`. The verdict is the summary's last non-blank line, trimmed, as `require-crit-review.py` reads it (`lines = [line for line in text.splitlines() if line.strip()]`, then `AUDIT_VERDICT.fullmatch` with `\s*` on both sides).
  - **P2, lines 111-112:** `fixed:2171d927`. Each disposition's reason is trimmed before its 20-character minimum counts, under either verdict, before any thread step.
  - **CI on `27757afb`:** `test (macos-14, client)` failed, and two `test` jobs were cancelled with it. The macOS 14 runner has no `/usr/bin/jq`, and the tests' PATH is the stub directory, `/usr/bin` and `/bin`, so `jq` resolved to nothing and the finish tests refused with exit 10 (`no jq for pr-cost.sh outside a shims directory: none`). `14033382` links the test process's own `jq` into the stub directory, as the gh stub already uses it. The script is unchanged. The 21 tests and the 22 mutants were re-run on it.
  - No new Bot wait. CI on the final head is in the RESULT.
- **Revise round 3** (ACCEPTANCE `status=revise`, bus 2026-10-17T07:34:11Z; operator decision D-S2-378 A) took the local review of `f20826e2`, the orchestrator's update-branch head of `19f09440`:
  - **P1, lines 94-95, `local:f20826e:1` (class `sweep-head-binding`):** `fixed:4d4e3b22`. The preconditions read only the sweep's `pr`, so a sweep JSON collected for an earlier head of the same PR reached the thread step, which replied to and resolved threads with that head's dispositions, and `fill_sweep.py` then imported them as current-head evidence. Now the sweep's `head_sha` must equal the audited head, the review worktree's `HEAD` that the next precondition binds to the PR's head and its audit summary. The check is exit 10, before any GitHub write, and names the head the sweep carries: `the sweep JSON is head <sha>'s, not the audited head <head>'s: rerun scripts/pr-feedback.py`. `acceptance-front-matter.py` and the gate already compare the sweep's `head_sha`, but only at steps 4 and 5, after step 2's GitHub writes.
  - This round asks for the Bot's review of the new head; it and CI on the final head are in the RESULT.

## Not done, or outside scope

- T7's script and tests, the scripts the chain calls, the glue files and their retirement are unchanged.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- CompactionDB (revise round 3): `memory add` ran in the worktree's own database, entry `f7c752e6-7d04-48df-9cba-5eb6e9c13310`, the command and a search showing it in validation §6; the earlier rounds ran none.
- cost: n/a (the runtime exposes no session figures to the seat).
