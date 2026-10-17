---
task_id: dotfiles-T130-sandbox-portability-a01
seat: claude-review-dot-a005
branch: portability/sandbox-a01
base: e9bc99d2
code_commit: 005e6c91
pr: 395
task_sha256: 53eb1abbaa839795a41abd9540a5e08bd312e95a4b9274bbdf272721f3a967bc
---

# Report: dotfiles-T130-sandbox-portability-a01

- Seat: `claude-review-dot-a005` in `.claude/worktrees/worker-d`, on a fresh branch `portability/sandbox-a01` from `origin/main` `e9bc99d2`; the branches of PR #387 and PR #394 stay in the worktree, committed and pushed, for their integrations.
- Task file: dispatched 2026-10-17T14:00:00Z at `3c8cb121…`; Amendment 1 (14:39:41Z) at `d5f403d0…`; Amendment 2 (14:43:25Z) at `53eb1abb…`, copied byte-identical to `task.md`; the task-consistency check passes on it (validation §1a); the three premises replay as recorded (§2a to §2c). One question (PONG 14:38:09Z, answered by Amendment 1) and one blocked note (PONG 14:40:45Z, answered by Amendment 2).

## What changed

- **`tests/unit/test_sandbox_portability.py`** (new, 102 lines, stdlib only; `git ls-files` over `scripts`, `home` and `install`, a file read by name or shebang): `test_no_process_substitution_in_tracked_scripts` refuses a `diff` invocation with a `<(` or `>(` argument outside a comment in a tracked shell file (a temporary repository with `diff <(sort a) <(sort b)` refused by that line, one with `done < <(…)` and `comm <(…) <(…)` accepted, the checkout accepted); `test_no_hard_coded_tmp_in_tracked_scripts` refuses a line outside a comment that names `/tmp/` or a bare `/tmp` without reading `TMPDIR`, over the shell and Python files (the same fixture shape; the checkout accepted).
- **`scripts/check-statusline-tools.py`** (two literals): the probe's payload `current_dir` and `transcript_path` move from `/private/tmp` and `/private/tmp/nonexistent.jsonl` to `/nonexistent/statusline` and `/nonexistent/statusline/transcript.jsonl`; the probe only sends them as JSON to the statusline binaries, and no consumer in the repository reads them (validation §4a).

## The question, the blocked note and the two amendments

1. Both guards as first worded refused the checkout: item 1 (no `<(` or `>(` outside a comment) 31 lines in 11 tracked files, 30 of them `done < <(…)` loops and one `comm -23 <(…) <(…)`; item 2 the two probe literals in a script outside `allowed_files`. Measured inside the sandbox (validation §3): `done < <(…)`, `comm <(…) <(…)` and `cat <(…)` work and only `diff <(…) <(…)` fails (`diff: /dev/fd/63: Operation not permitted`), so premise 1's own predicate is the hazard. Amendment 1 made item 1's guard that predicate and added the probe script to `allowed_files` for the two literals.
2. Item 3 (the CompactionDB store out of `.claude/`) needed edits outside the task and across a trust boundary: `home/dot_local/bin/common/executable_contextdb-codex-notify` resolves the project by the `.claude/contextdb` directory, refuses symlinks under it and requires its storage children before running the trusted CLI from the home directory; `tests/unit/test_contextdb_codex_notify.py` asserts that boundary; the trusted CLI's `paths.py` is byte-identical to the repository's copy (synced from `vendor/compactiondb`, never edited), so moving only the repository's package base would split the ledger; `compactiondb-install` rewrites the package copy and the ignore entries; upstream has no store-base option. Amendment 2 withdrew item 3 (D-portability-store); a relocation is an upstream design task of its own.
3. The `ps` guard (item 2 (d)): none on `origin/main` (premise 2) and PR #387's lint carries rule R5 for it, so no second guard, as the task says.

## The Check

The two tests green (§4); caps 4 changed lines outside `tests/` and `.orchestration/` (cap 20) and 102 added under `tests/` (cap 200) (§5a). `ruff format --check` is clean on both files; `ruff check` reports three pre-existing findings on `scripts/check-statusline-tools.py` (EXE001, I001, PLW1510) that are on `origin/main`'s copy unchanged and outside the two literals.

## Readings, declared

- "Outside a comment" is read as: a line whose first non-space character is `#` is skipped, and a trailing ` #…` is cut before the match.
- A trailing ` #…` is cut whether or not the `#` sits inside a quoted string, and the `TMPDIR` exemption reads the whole line, comment included.
- Item 1's guard is line- and word-scoped: the word `diff` and a `<(` or `>(` on the same line; a backslash continuation or a variable holding the program name is outside it.
- A shell file is one whose name ends `.sh`, `.bash` or `.zsh` or whose first line is a `sh`, `bash` or `zsh` shebang; a Python file one whose name ends `.py` or whose first line is a python shebang; `.tmpl` files and executables under `env -S uv run` are outside both sets, as the task's own filter has it.

## Review, hook, cost

- Worker-side independent review: one round on `005e6c91` by a fresh read-only subagent, `Verdict: correct`, no P0 to P2, six P3 notes (`dotfiles-T130-sandbox-portability-a01-worker-crit.json`, receipt `dotfiles-T130-sandbox-portability-a01-worker-review-receipt.md`). The notes, all spec-shaped or test-robustness, are declared below and are the orchestrator's follow-up input (C-61): `.sh.tmpl` scripts with a template directive on line 1 (25 tracked, 21 with inline shell) are outside both guards; the `TMPDIR` exemption reads the whole line, comment included (`export TMPDIR=/tmp` passes); the trailing-comment cut also cuts inside a quoted string and no fixture exercises that branch; the `diff` guard is line- and word-scoped (a backslash continuation, `$DIFF`, `colordiff` pass); the refused fixture is named `.sh`, so shebang-only classification is exercised only as accepted; `tracked()` inherits the environment, so an exported `GIT_DIR` makes the fixture tests error loudly.
- No Understand-Anything hook prompt fired; no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
- CompactionDB: one decision added in this worktree's store before completion (validation §6); the orchestrator consolidates adopted decisions into the main checkout's store at acceptance.
