# Report: dotfiles-T128-chain-review-scripts-followup-a02

- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on the fresh branch `tools/local-review-env-s-quoting`, cut with `--no-track` from `origin/main` at `1d418126`. The earlier branches are left as they are.
- **Task copy.** Byte-identical to the dispatched main-checkout file, sha256 `2cc46db3…`, the TASK's `task_sha256` (validation §1).
- **Commits.** `fbc1d4ac`: the change, its test and the task copy; then this evidence.
- cost: n/a (the runtime exposes no token or cost figures to the seat).

## The owned rows: `audit:2e3ff49:1` and `local:2e3ff49:1` (class `env-s-quoting`)

- **The defect.** PR #364's round 3 split an `env -S` remainder with `read -r -a`, which does not follow `env -S`'s quoting, escapes, variable expansion or comments: `--require "/opt/review modules/init.js"` became three words with literal quotes.
- **The fix.** In the shebang branch, when the `-S` form is used and the whole `-S` string (the interpreter token and the remainder) holds a double quote, a single quote, a backslash, a dollar sign or a word starting with `#`, `local-review.sh` prints `local-review: the review binary's env -S shebang holds a quote, an escape, an expansion or a comment the script does not split; refused` on stdout and exits 2, before the interpreter is resolved and before the checkout. A string of plain words is split as before; a faithful `env -S` parser stays out of scope, as the task says. The header and the `@exitcode 2` line say so.
- **The test.** `test_local_review_refuses_a_quoted_env_S_shebang`: five stub binaries whose first lines are `#!/usr/bin/env -S fakeinterp` followed by `--require "/opt/a b/x.js"`, `'x'`, `a\ b`, `${HOMEX}/lib` and `one # two`. Each exits 2 with the stdout line, the review worktree stays at `main`, no review file is written, and neither the stub interpreter nor the stub codex runs. The round-3 test's plain-word case is unchanged and passes.
- **Checks.** 14 tests pass; six mutants, all killed, each feature's mutant by its own case (validation §2).
- **Size.** 18 changed lines outside `tests/` and `.orchestration/` (of 200), 28 added under `tests/` (of 1000), 2 files.

## Bot and CI (main-checkout copy only)

- **CI.** All 13 checks pass on `b20a0141`, the final head; `mergeStateStatus` is `CLEAN` (validation §3).
- **The Bot.** Its code and security reviews of `b20a0141` completed with no finding and a 👍 reaction: no thread, no fix round.
- **The memory add:**

```text
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T128-chain-review-scripts-followup-a02 (PR #376, head b20a0141): local-review.sh refuses, with exit 2 before the checkout, an env -S shebang string holding a double or single quote, a backslash, a dollar sign or a word starting with # (the four env -S features read -r -a splits differently), closing audit:2e3ff49:1 and local:2e3ff49:1 (class env-s-quoting); plain words are split as before; one test, one case per feature, each feature mutant killed by its own case after a per-case reset of the reused review file. Bot: code and security reviews clean, no thread.'
dad7ad40-e5fa-4a1c-ac71-f2ffca25964e
rc=0
```
