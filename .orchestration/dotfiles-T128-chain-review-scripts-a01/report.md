---
task_id: dotfiles-T128-chain-review-scripts-a01
seat: claude-standard-dot-a002
branch: regime/chain-review-scripts
base: 5ec86052ff0f8ef0fa7dbdbbd44e1e389ba9eb6c
code_commit: 1f307a6e
pr: 357
task_sha256: db9ff03a5eb720a4778fc357fb351926e7ecbb1d5af7a5f6cf11266232ba060b
---

# Report: dotfiles-T128-chain-review-scripts-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `regime/chain-review-scripts` from `origin/main` `5ec86052` (PR #355 merged), PR #357.
- Task file: amendment 1, sha256 `db9ff03a…`, copied byte-identical to `.orchestration/dotfiles-T128-chain-review-scripts-a01/task.md` (validation §1). The attached inputs are untouched; their sha256 prefixes equal the intro's (validation §2).
- Round 1 was dispatched at 08:54:36Z. One question followed, at 09:02Z, before any commit:
  - row 11 listed a subset of the tools the inputs run;
  - a review-worktree path that exists but is not a worktree root lets `git -C` act on the enclosing checkout.

  A working PONG at 09:05Z declared the `mktemp` template. Amendment 1 (12:17:36Z, `db9ff03a`) answered all three: row 11's full tool list, item 1's `.git`-entry refusal with its test case, and item 1's `mktemp` template.

## Commits

| Commit | What |
|---|---|
| `1f307a6e` | Items 1 to 4 with amendment 1 |
| `0da6be3e` | Task copy at `db9ff03a` and the first evidence; the Bot's one review was of this head |
| this commit | The evidence update: the Bot's threads, CI and the sandbox rows |

## What landed

| Item | File | What it does |
|---|---|---|
| 1 | `scripts/orchestrator/local-review.sh` | The input, with item 1's changes, nothing else (validation §3 diffs it against the input):<br>- the root from `git rev-parse --show-toplevel`, and `cd` there;<br>- the review worktree `$ORCH_REVIEW_WORKTREE`, else `<root>/.claude/worktrees/orchestrator-review`, refused with exit 2 without its own `.git` entry, before the dirty check (amendment 1);<br>- the binary `command -v "${CODEX_BIN:-codex}"` in the root before the checkout, made absolute against the root when relative, exit 2 when none;<br>- `mktemp "${TMPDIR:-/tmp}/local-review.XXXXXX"` (amendment 1);<br>- the shdoc header. |
| 2 | `scripts/orchestrator/local-advisory.sh` | The input, shfmt-formatted, with the shdoc header. |
| 3 | `scripts/orchestrator/sandbox-scan.sh` | The input, shfmt-formatted, with the shdoc header. |
| 4 | `tests/unit/test_chain_review_scripts.py` (new) | The three tests item 4 names; see below. |

Notes on meaning:

- Item 1's binary reads as one resolution for both sources: the binary is `command -v` of `$CODEX_BIN`, else of `codex`, run in the root. An absolute `$CODEX_BIN` is used as it is. A relative one, like a relative PATH hit, is made absolute against the root, so nothing resolves inside the review worktree. A missing binary is a precondition, exit 2. The input would have run `codex` anyway and recorded exit 127.
- Every other line keeps the input's text and order. Validation §3 diffs each port against its input after running the input through CI's shfmt (`-i 4 -sr` on `scripts/**/*.sh`). Beyond item 1's changes and the headers, it shows three layout edits: `local-advisory.sh` takes its three arguments in one assignment and its two counters in another, and `sandbox-scan.sh`'s one-line `if … then … else … fi` spans five lines. None changes behaviour.

## Tests

The Check: 3 tests OK (validation §4); the whole unit suite: the four modules that exercise `scripts/orchestrator/`, 53 tests OK; the whole suite is CI's (validation intro) (validation §7). The cases:

- **`test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file`:** item 4's cases, in this order:
  - the plain-directory case (amendment 1), run first, while the main working tree is still clean, since otherwise the dirty check alone would refuse it;
  - case one (`CODEX_BIN` unset, `./bin` decoy in the head);
  - case two (`CODEX_BIN` set);
  - the reuse;
  - the no-finding run under a new task name;
  - the dirty worktree.
- **`test_local_advisory_records_p2_rows_and_stops_on_p0_p1`:** item 4's four cases.
- **`test_sandbox_scan_prints_the_unsandboxed_mutation_calls`:** item 4's three cases.

Cases beyond item 4's text, each added to close a mutation the listed cases left alive (validation §8):

- local-review:
  - The stub records its stdin, and the caller gives it some, so `< /dev/null` is checked.
  - The transcript holds an earlier `codex` marker with a `[P1]` line, so only the final message counts, and one finding twice, so the unique count is checked.
  - Every finding carries the worktree prefix, so the stripping is checked.
  - No `local-review.*` temporary file is left under `TMPDIR`.
  - Case two passes `CODEX_BIN` as a path relative to the root and runs from a subdirectory, so both the `cd` and the absolute path are checked.
  - The no-finding run's binary exits 5: `codex exited 5` is printed, the file is still written, and the exit is 0.
  - A missing `CODEX_BIN` and an unknown head each exit 2, and nothing runs.
- local-advisory:
  - The two P2 lines are written out of sort order, so the numbering follows `sort -u`.
  - One P2 line is longer than 120 characters and holds backticks, so the cut and the removal are checked.
  - A review with one `[P0]` line prints STOP and exits 3.
- sandbox-scan:
  - A `-fixtures` task id reads the stripped record, and its line is matched in other letter case.
  - The `counts` line is written `Counts`.
  - The reads-only record holds a `> ` line excluded by `reads` and a `tee ` line excluded by `lists`.

Mutation pass: 57 mutations, 57 caught, across every refusal and exit, each item-1 change, the front matter, the advisory row and line text, and each scan filter (validation §8).

## Caps

Validation §6:

- outside `tests/` and `.orchestration/`: 3 files, 148 added + 0 deleted = 148 changed lines (cap 200);
- under `tests/`: 230 added lines (cap 1000);
- 4 files outside `.orchestration/`.

## CI and the Bot

- **The Bot:** PR #357 was opened as a draft and marked ready (12:42:37Z) after the evidence commit, so the Bot's one review saw the whole PR. That review, 5518077170 at 12:45:21Z of `0da6be3e`, raised two inline threads, both P2, and its body holds no badge (validation §9). No P0 or P1, so there is no fix round. Each P2 is advisory, proposed for `dotfiles-T128-chain-review-scripts-followup-a01`:

  | Thread | Where | Finding | Proposed disposition |
  |---|---|---|---|
  | 4270918132 | `local-review.sh:61` | A non-zero review-binary exit still writes the file, with `findings: 0` when no finding came back, and the next run on that head reuses it as a review. | advisory P2: the input's continuation, which item 1 states (`the file is still written from whatever transcript came back`) |
  | 4270918140 | `local-review.sh:28` | The reuse is keyed by the head's first seven characters; the file's full `head:` is never compared, so a second head with the same prefix is not reviewed. | advisory P2: the input's file name and reuse, which item 1 states (`<task>-local-review-<sha7>.md` is reused) |

  The worker resolves no thread.
- **CI on `0da6be3e`:** 13 of 13 checks pass, the four `test` jobs (`make unit-test` and the bats suites) among them (validation §9). The suite's failures under the Claude sandbox (validation intro) are therefore environmental.
- **CI on the final head (this commit):** in the RESULT.

## Not done, or outside scope

- `cut -c1-2000` of the transcript is checked only through mutation R26 (`cut -c1-20`); no case holds a line over 2000 characters.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
