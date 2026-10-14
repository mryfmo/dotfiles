# Learning triage: dotfiles-T128-chain-review-scripts-a01

These are candidates only; nothing is promoted.

1. [memory:failure] macOS `mktemp` with no template, or with only `-t`, ignores `TMPDIR`. It takes `_CS_DARWIN_USER_TEMP_DIR` (`/var/folders/…/T/`) first, as `man mktemp` says, and the Claude sandbox denies writes there. The input's bare `mktemp` therefore worked outside the sandbox, where the chain runs it, and failed inside the sandbox, where the tests run. On Linux, `mktemp` follows `TMPDIR`.
   - Detected by the first test run: `mktemp: mkstemp failed on /var/folders/…: Operation not permitted`.
   - Mechanism candidate: a repository script takes its temporary file from an explicit template, `mktemp "${TMPDIR:-/tmp}/<name>.XXXXXX"`, as `orch-gate.sh` already does. A shellcheck-style grep in the test suite for a bare `$(mktemp)` under `scripts/` would catch the next one.
2. [memory:decision] A port that freezes an input's behaviour can still need a guard the input lacks. `git -C <dir>` falls through to the enclosing repository when `<dir>` exists but is not a worktree root. So a review-worktree path that names a plain directory inside a clean checkout would move that checkout to the PR head. I asked before the PR opened (09:02Z); the orchestrator answered with amendment 1 rather than a PONG answer. Ask about a guard beyond the frozen text before the first push, together with every other discrepancy found by reading the task's rows against the input (here, row 11's tool list).
3. [memory:failure] Two kinds of mutation-pass gap had nothing to do with the code under test:
   - A fixture line meant to exercise one filter was dropped earlier by another filter. `tee:` does not match the `tee ` pattern, so the `lists` exclusion never ran (mutation S8).
   - A mutation's pattern also matched the shdoc header, so the runner skipped it (R12, R13).

   Mechanism candidate: the mutation runner refuses a pattern that does not occur exactly once, which it already does, and the report lists every skip. A fixture line for a filter carries every token that the earlier filters require.
