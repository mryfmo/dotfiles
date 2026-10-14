# Report: dotfiles-T128-chain-github-scripts-a01

- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on the fresh branch `tools/chain-github-scripts`. It was cut with `--no-track` from `origin/main` at `5ec86052`, after PR #355 merged. The earlier branch `tools/gate-wrapper-path` is left as it is.
- **Task copy.** The task file's sha256 `fe39cbc8…` matches the TASK's `task_sha256`. It is copied byte-identical to `.orchestration/dotfiles-T128-chain-github-scripts-a01/task.md` and holds no home path (validation §1).
- **The sibling task.** My files are disjoint from the sibling `dotfiles-T128-chain-review-scripts-a01`.
- **Commits.**
  - `3931db66`: items 1 to 3.
  - Then this evidence.
- cost: n/a (the runtime exposes no token or cost figures to the seat).

## Item 1: `scripts/orchestrator/resolve-threads.sh`

The script keeps the input's behaviour, and adds an shdoc header and the house style (4-space indent, `[[ ]]`, braced variables).

- **The arguments** are positional as in the input: `<pr> <extra.tsv> [--dry-run|-] [<sweep.json>]`. The script now checks them: two to four arguments, a numeric PR (it is interpolated into the GraphQL query and the API path), and a table that exists. Anything else is a usage error, exit 2. The input instead failed with exit 1 and no message when the table was missing.
- **The threads.** One GraphQL query reads the first 100 review threads. The `--jq` expression is the input's and yields one `<comment id> <thread id>` line per unresolved thread.
- **The disposition.** It is the table row whose first column is the comment id. Failing that, when a sweep JSON is given, it is the `disposition` of the first sweep item whose `url` ends with `_r<comment id>`.
- **The replies.** A `fixed:` disposition and a `not-applicable:` disposition each get the task's sentence verbatim. Any other form prints `row for <id> has an unknown form: <row>` and sets exit 3.
- **The outcomes.** No disposition prints `no disposition row for thread <id> (table or sweep); left open` and sets exit 3. `--dry-run` prints `would reply+resolve <id>: <first 90 characters>` and writes nothing. Otherwise the script posts one reply and sends one `resolveReviewThread` mutation, then prints `resolved <id> (<first 60 characters>)`. The last line is `resolved <n> thread(s); missing rows: <0|1>`.
- **`gh`** is called by name, as the input does.

### Two changes from the input

1. **The loop reads the threads on fd 3.** The input fed the loop a here-string on stdin, so every `gh` call inside it inherited that stdin. The stub `gh` reads its stdin, as item 3 requires of it. Against the input as it is (mutant R1), the first reply swallowed the second thread's line. The run then reported `missing rows: 0` and exited 0, although that thread had no disposition (validation §4). A real `gh` with `-f` fields does not read stdin today, but nothing in the loop may depend on that. `while read -r cid tid <&3; … done 3<<< "${threads}"` closes the hole. The test asserts that no logged call read anything on stdin.
2. **The sweep lookup is one `jq` call**, where the input ran a `uv run --no-project python` one-liner. The result is the same: the first matching item's `disposition`, else an empty string. No interpreter, and no uv configuration discovery, runs in the caller's checkout.

## Item 2: `scripts/orchestrator/pr-cost.sh`

The script keeps the input's behaviour, adds an shdoc header and a usage check (one numeric PR, else exit 2), and takes the repository root from `git rev-parse --show-toplevel`.

- **The ledger** is `.orchestration/metrics/pr-cost.tsv`. The header is written once, only when the file is empty or missing.
- **The line's fields, in order:** pr, branch, created, merged or `open`, wall hours with one decimal, commits, the Codex Bot's reviews, its top-level comments badged `P[01]` and `P[23]`, the local-review files whose `pr:` line names the PR, the update-branch merge commits, and the recording time. The line is appended and printed.
- **Every `--jq` expression is the input's, byte for byte** (validation §2), because the test's canned answers are keyed on them.

### Two changes from the input

1. **Per-page counts are summed.** With `--paginate`, gh applies `--jq` to each page, so a PR with more than one page of reviews, comments or commits printed one count per page into one field. That happens at 30 items, a count the Bot's threads plus the orchestrator's replies reach. The input as it is (mutant P1) breaks on the test's two pages of reviews. `count()` pipes the per-page counts through `awk` and sums them.
2. **The wall hours come from `jq` (`fromdate`) and `awk` (`%.1f`)**, where the input ran a `uv run --no-project python` one-liner. The two forms print the same on eight cases: whole hours, ties at .x5, zero and long spans (validation §5).

The threat table's environment row names `uv run --no-project python` among the scripts' binaries. After these changes, they run only `gh`, `jq`, `awk`, `git`, `/usr/bin/grep`, `wc`, `tr`, `date` and `tail`.

## Item 3: `tests/unit/test_chain_github_scripts.py` (new)

The module imports only the standard library. Each test copies both scripts into a temporary git repository, their root, and runs them there with stdin closed, under a stub `gh` first on PATH.

- **The stub `gh`.**
  - It is a Python script whose shebang is the test's own interpreter.
  - It appends each call's argv and stdin to a log.
  - It answers from a canned map, keyed on the API path plus the `--jq` expression for REST, and on `graphql` plus the operation (`query` or `mutation`) for GraphQL.
  - A call with no answer exits non-zero and names its key.
- **The test-side jq.** The test computes each filtered answer by running the real `jq` with that expression over the fixture the case describes, one page at a time. The stub itself records and answers, nothing else.
- **`test_resolve_threads_replies_with_the_table_row_and_resolves_only_threads_with_rows`.** Two unresolved threads, 101 and 202. The table has a `fixed:` row for 101. The sweep has a `not-applicable:` item for neither.
  - **First run, with placeholder `-` and the sweep:** exactly one reply, for 101, with the `fixed:` sentence (argv compared whole), and one mutation naming `T_one`. Thread 202 is reported left open, the last line is `resolved 1 thread(s); missing rows: 1`, and the exit is 3.
  - **Second run, with the sweep now holding 202's `not-applicable:` disposition:** both replies, in order, with their two sentences, mutations for `T_one` and `T_two`, and exit 0.
  - **`--dry-run`:** the only call is the threads query, and both `would reply+resolve` lines are printed.
- **`test_pr_cost_appends_one_ledger_line_from_the_api`.** The PR is merged three hours after creation, with 4 commits.
  - **The fixtures.** Reviews come in two pages, with two of the Bot's reviews in all. The comments are one Bot `P1 Badge` top-level comment, one Bot `P2 Badge` reply that does not count, and one other user's comment that mentions `P2 Badge`. The commits are one update-branch merge and one fix. There are two local-review files, one with `pr: 9` and one with `pr: 90`.
  - **The first line:** the header, then `9, tools/x, created, merged, 3.0, 4, 2, 1, 0, 1, 1` and a UTC timestamp. The script's stdout is that line.
  - **A second run, with the PR now open:** it appends a third line with `open` and a one-decimal wall, and writes no second header.

## Proofs and size

- **Tests.** Both tests are green, and shellcheck, shfmt and ruff are clean (validation §3).
- **Mutation proofs.** 13 mutants, all killed, including both inputs as they are (validation §4).
- **Caps.** 124 changed lines outside `tests/` and `.orchestration/` (of 200), 193 added under `tests/` (of 1000), and 3 files outside `.orchestration` (validation §6).

## Threat table

| Row | Where it is closed or bounded |
|---|---|
| resolve-threads.sh | `test_resolve_threads_replies_with_the_table_row_and_resolves_only_threads_with_rows`; R1 to R7 die there |
| pr-cost.sh | `test_pr_cost_appends_one_ledger_line_from_the_api`; P1 to P6 die there |
| the test module's stub | it records and answers, nothing else. The filtered answers are computed in the test, by the real jq, from the described fixtures |
| the GitHub writes | the reply body is built only from the table row or the sweep's `disposition`, in the two fixed sentences. `--dry-run` writes nothing (R4). A thread without a row stays open and gives exit 3 (R5) |
| the task copy | byte-identical, sha256 `fe39cbc8…` (validation §1) |
| environment inputs | the scripts run `gh`, `jq`, `awk`, `git` and coreutils on the orchestrator's PATH, with `mryfmo/dotfiles` literal. They no longer run `uv run --no-project python` |
| new scripts | exactly the two named in `allowed_files`, both mode 755 |

## Notes for the orchestrator

- **A wider argument check.** resolve-threads.sh and pr-cost.sh refuse a non-numeric PR with exit 2. The input interpolated it into the GraphQL query unchecked.
- **pr-cost.sh writes to the repository of the current directory,** as the input does. Run it from the main checkout.
- **The Understand-Anything stale-graph hook** did not fire in this task.

## CompactionDB

The main-checkout `memory add` runs after CI, with the masked main-checkout copy. Its exact command and output go into the main-checkout copy of this report.

- [memory:decision] The integration chain's thread resolution and PR cost line are repository scripts: `scripts/orchestrator/resolve-threads.sh <pr> <extra.tsv> [--dry-run|-] [<sweep.json>]` and `scripts/orchestrator/pr-cost.sh <pr>`. The tests are in `tests/unit/test_chain_github_scripts.py`, with a stub gh keyed on the API path and the `--jq` expression.
- [memory:failure] A `while read … done <<< "${list}"` loop gives its stdin to every command in its body. A command that reads stdin swallows the rest of the list, and the loop then reports success over items it never saw. Feed such loops on fd 3.
- [memory:failure] `gh api --paginate --jq` applies the filter to each page and prints one result per page. A count needs a sum over the pages.

## Bot and CI

The PR opens after this evidence commit. The CI result and the Bot's review of the final head go into the main-checkout copy and the RESULT.
