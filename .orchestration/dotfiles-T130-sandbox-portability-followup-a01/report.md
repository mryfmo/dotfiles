---
task_id: dotfiles-T130-sandbox-portability-followup-a01
seat: claude-review-dot-a005
branch: portability/followup-a01
base: 5992fac5 (PR #395's head; origin/main a8a747af; rebased onto origin/main after #395 merges)
code_commit: 0b72f4c8 (the test commit 3887df89, the fix a666ac42, the docstring commit 0b72f4c8)
pr: @PR@
task_sha256: 5141e9313d66a6fc414ef204a9afb38178aaeeef85c07bc76a2b5c1272758511
---

# Report: dotfiles-T130-sandbox-portability-followup-a01

- Seat: `claude-review-dot-a005` in `.claude/worktrees/worker-d`, on the branch `portability/followup-a01` stacked on PR #395's head `5992fac5` as the dispatch note says (the task text's "fresh branch off `origin/main` after PR #395 merges" becomes the rebase step); the branches of PR #387, PR #394, PR #395 and the README task stay in the worktree for their integrations.
- Task file: dispatched 2026-10-17T16:43:35Z at `5141e931…`, copied byte-identical to `task.md`; the task-consistency check passes (validation §1a); `premises: []`. Started after the README task's blocked PONG (17:19:39Z), as queued.

## The owned rows

The record is the source (item 1). At dispatch it carries one row under the owner heading: `4303340052`, class quoting-in-regex-predicates (validation §1b), with the orchestrator's re-plan D-S1-395 as its mechanism. Item 1's text also names the worker review's six round-1 P3 "each a row at the sweep"; no such row exists in the record yet (the sweep of PR #395 runs before its merge), so this round fixes the one row and measures the P3 candidates on the checkout for the orchestrator (validation §7): the 32 `.sh.tmpl`/`.bash.tmpl`/`.zsh.tmpl` files would add zero hits to either guard; zero lines are exempt only because a comment or quoted text names `TMPDIR`; zero `colordiff`/`sdiff`/`diff3`/`git diff`/`$DIFF` calls carry a process substitution; 28 shell files are classified by shebang only (the refused fixture is named `.sh`); no `GIT_DIR` or `GIT_WORK_TREE` is set in this seat's environment. Rows the record gains before the RESULT are fixed in the same way, one fixture per row, red before and green after.

## What changed (`tests/unit/test_sandbox_portability.py`, 63 added and 32 removed lines over the three commits)

1. **`3887df89` (red)**: the two predicates move from four per-test closures to module level, unchanged in behaviour (`diff_refused`, `tmp_refused`); `test_a_quoted_span_is_never_shell_syntax` adds one fixture of eight lines: a quoted pipe, semicolon and ampersand inside a `--label` argument before `<(sort a) <(sort b)` (lines 2 to 4), a backslash-escaped quote followed by a quoted hash (line 5), `echo 'diff <(a) <(b)'` and `diff "<(a)" b` (lines 6 and 7, quoted data the old predicate refused), and `echo "a\" # /tmp"` (line 8). Expected: the diff guard refuses exactly lines 2 to 5, the `/tmp` guard exactly line 8. Against the old predicates the test fails (§3): the old `[^|;&]*` bound stopped at the quoted operator (lines 2 to 4 accepted), the escaped quote closed the quote and the hash cut the line (lines 5 and 8 accepted), and lines 6 and 7 were refused.
2. **`a666ac42` (green)**: `code()` becomes `scan(line)`, one pass over the line that returns `(code, syntax)`: `code` is the text before the comment with quotes intact; `syntax` is the same text with every quoted span blanked to spaces (the quote characters kept) and every backslash-escaped character (outside single quotes) blanked with its backslash. A comment still starts at a `#` at the start or after whitespace outside quotes. `hits()` passes `(code, syntax, line)`; `diff_refused` reads `syntax` (operators, `<(`), `tmp_refused` reads `code` (a path inside quotes is still a path) and the raw line for the `TMPDIR` exemption as before; `logical_lines()` decides the continuation on `code` as before. The five tests are green and the checkout is still accepted by both guards (§4). ruff format re-wrapped two assertions of the earlier tests after the predicates' rename (§6).
3. **`0b72f4c8`**: the `scan()` docstring says the continuation is read from the code view (the worker review's P3; a backslash before the newline continues inside double quotes too, where the syntax view is blanked).

## The Check

Five tests green (§4). Caps (§5a): against the stack base, 0 changed lines outside `tests/` and `.orchestration/` (cap 40) and 63 added under `tests/` (cap 200); against `origin/main`, which until #395 merges carries #395's own diff, 4 and 190. After the rebase the Check reads the first pair.

## Readings, declared

- "Stacked on PR #395's head" (the dispatch note) overrides the task text's "fresh branch off `origin/main` after PR #395 merges"; the rebase happens when #395 merges, before the PR is opened, with one push of this branch under `--force-with-lease`.
- "No other change": the move of the two predicates to module level is part of the mechanism (the predicates' inputs change from one view to two) and removes duplicated closures; nothing else in the file moves.
- Inside an unclosed quote the comment cut stays suppressed to the end of the line (as the shell reads it); `$'…'` is read as a single-quoted span after a `$`; both are declared, not special-cased.

## Review, hook, cost

- Worker-side independent review: one round on `a666ac42` by a fresh read-only subagent, `Verdict: correct`, no P0 to P2, three P3 (`dotfiles-T130-sandbox-portability-followup-a01-worker-crit.json`, receipt `dotfiles-T130-sandbox-portability-followup-a01-worker-review-receipt.md`); red confirmed on `3887df89`, a 49-fixture old-versus-new harness, zero tracked lines of the newly accepted shapes. One P3 fixed in `0b72f4c8` (the docstring); two declared: ANSI-C quoting `$'a\'b'` is read as a plain single-quoted span, and a quoted command word `'diff' <(a) <(b)` is blanked and accepted; both outside D-S1-395's three quote kinds and absent from the tracked tree.
- No Understand-Anything hook prompt fired; no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
- CompactionDB: one decision added in this worktree's store before completion (validation §8).
