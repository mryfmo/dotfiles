---
task_id: dotfiles-T129-normalised-comparison-lint-followup-a02
seat: claude-standard-dot-a008
branch: tools/lint-comparisons-followup-a02
base: 51ba5801
test_commits: 883a6ab8 75c3c55c 3b59177f
fix_commits: 607d4485 5b6c5a8a
code_head: 5b6c5a8a
task_sha256: 4198ddc1b8b5e30a66c89ba01e4051a65758806f6d15d0e5dd495876902fca98
---

# Report: dotfiles-T129-normalised-comparison-lint-followup-a02 (the F2 lineage's owner task)

- **Seat and task:** `claude-standard-dot-a008` in `.claude/worktrees/worker-f`. The TASK arrived at 2026-10-19T11:36:30Z.
  - A question PONG (q1: the 200-line caps were infeasible, since main's script is already 227 lines; q2: the row count) was answered by amendment 1 at 11:39:57Z: the script-length cap is removed, at most 350 changed lines outside `tests/` excluding the baseline, at most 1000 under `tests/`, and 13 ids over 9 distinct gaps confirmed.
  - The branch copy equals the amended dispatched file (`4198ddc1…`, validation §1).
- **Branch:** `tools/lint-comparisons-followup-a02`, cut fresh from `origin/main` `51ba5801`.

## The owned rows and their fixes (validation §3; red §4 and §4b; green §5; one mutant per fix §5a)

`tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_each_owned_row_is_refused_or_accepted_by_its_fixture` holds one entry per distinct gap, keyed by its row ids. A Bot row and its local twin share the fixture.

| Row ids | Gap | Fix in `scripts/lint-comparisons.py` (re-plan: tokens, not physical-line regexes) |
|---|---|---|
| 4306643800, audit:4f5be51:4 | a `[[ … ]]` test or `case` split by `\` continuations | Continuation lines join into one statement, reported at its first line. A marker on any of its lines accepts it, and an even run of trailing backslashes continues nothing. |
| 4306643803, audit:4f5be51:9 | double-quoted jq programs never scanned | The program locator takes the first `'…'` or `"…"` word after the options and their arguments. It skips `"$expansion"` words and a stray closing quote, stops at a shell separator, and lets a `"…"` program span lines. The program is unescaped as the shell hands it to jq. |
| 4306643804, audit:4f5be51:2 | one `re.escape` accepted every fragment of a formatted value | `escaped()`: each formatted value must itself be `re.escape(…)`, a constant, or a constant separator joining `map(re.escape, …)` or an escaped comprehension. |
| 4306643808, audit:4f5be51:8 | an allow marker inside a string literal suppressed the line | A marker counts only in a comment: Python's comment tokens (`tokenize`), and for shell a quote-aware `comment()` scan. For jq, also a jq comment on the hit line or a shell comment past the program's closing quote. |
| audit:4f5be51:1 | logical operators did not bound jq operands | `and`/`or`/`then`/`elif`/`else` bound an operand, and `if…end` is one operand, like parentheses. |
| audit:4f5be51:3 | single-quoted grep patterns read as interpolation | `grep -E` and `pgrep -f` take their whole shell word, and `expands()` asks whether the shell expands a `$name` in it: outside `'…'`, after no backslash. |
| audit:4f5be51:5 | operators inside jq strings and comments | `jq_mask()`: a scanner with a context stack (string, interpolation code with its own depth, comment). It gives the code view, where strings and comments are blank, and the literal view. |
| audit:4f5be51:6 | `pgrep -f "prefix $name"` | the shell-word reading above |
| audit:4f5be51:7 | a leading variable discarded its literal path suffix | `operand()` checks both pieces: a path-named variable, or a literal path piece beside any expansion. |

The process rows are covered by the records:

- **audit:4f5be51:12:** validation §12 to §12b carry `make format` verbatim at HEAD and at the merge-base, with per-file exit statuses.
- **audit:4f5be51:14:** sandbox.md lists which Python runs used `-I`.

## The baseline follows (validation §8)

The tracked tree's `--all` output from main's lint is compared with this head's:

- **Removed row:** `home/dot_local/bin/common/executable_herdr-agents` R3 (`de8d2d7c…`, line 758). It was a false positive on main: `($processes | length) == 1` reached across `and`/`or` to a `"(^|/)…"` string. The and/or bound removes it.
- **Added rows** for hits the sharper rules newly find in files no open task names (the Goal's rule):
  - `install/common/mise.sh:45` R2 (`case "${os}/${arch}"`, a platform pair);
  - `install/macos/common/brew.sh:82` and `:91` R1 (`"${tap}/"*`, tap names).
  - Both are string comparisons of slash-joined values, consistent with how main already treats `"a/${b}"`.
- **Left as warnings, with no row:** these files are named by open tasks, so ownership is the orchestrator's. Each is a true positive (a path compared by its string form):
  - `scripts/check-regime-boundary.sh:125` (owner candidate `dotfiles-T128-seat-launch-args-followup-a01`);
  - `scripts/orchestrator/chain-integrate.sh:93` and `:106` (owner candidates `dotfiles-T128-chain-glue-integrate-followup-a01`, `dotfiles-T128-process-hardening-a01`, `dotfiles-T129-audit-inherit-replan-json-followup-a03`).
- **Unchanged:** the five `scripts/orchestrator/regime-ci.py` warnings, which predate this task and are owned by P1-11, as a03 ruled.

## Check (validation §5 to §11)

- **Unit tests:** `uv run python -m unittest tests/unit/test_lint_comparisons.py -v`: 15 of 15 (§5).
- **The lint, no mode flag:** `uv run --no-project python -I scripts/lint-comparisons.py` exits 0 (§6). Its output is not empty, unlike the Check's "no output": it prints the five `regime-ci.py` warnings and the three owner-named warnings above, all in files this PR leaves unchanged (a03's invariant).
- **`--all`** exits 0 (§7). `--list-rules` is byte-identical to main's (§9). `ruff check` and `ruff format --check` on both files are clean (§10).
- **Caps (§11), over merge-base `51ba5801`:** outside `tests/` and `.orchestration/`, without the baseline, 163 of 350; under `tests/`, 68 of 1000; the baseline (outside the count) 4.
- **`make format` exits 2 at HEAD and at `51ba5801` alike** (§12, §12a, verbatim). The same twelve files exit 1 under shfmt at both (§12b), and none of them is this PR's. Its Python files pass `ruff format`, and its Markdown passes prettier.

## Worker review

The review is recorded in `dotfiles-T129-normalised-comparison-lint-followup-a02-worker-crit.json` and its receipt. There was one pre-push round, the task's limit, covering `51ba5801..607d4485`. It returned `Verdict: incorrect`, with one P1, five P2 and P3 items.

- **Fixed in `5b6c5a8a`,** each with a fixture form red at `607d4485` (§4b) and a killed mutant (§5a):
  - the P1, the jq scanner's literal view shrinking by one slot per string character;
  - `if…end` as an operand;
  - whole-word `pgrep`/`grep`;
  - markers past a closing quote and on continued statements;
  - multi-line `"…"` programs;
  - the separator, trailing-backslash and join-separator P3s.
- **Residual P3s:** a `"…"` program that starts with an expansion is skipped, the re-plan's choice; escaped joins through `sorted()` or a set comprehension are refused, the conservative direction.

cost: n/a
