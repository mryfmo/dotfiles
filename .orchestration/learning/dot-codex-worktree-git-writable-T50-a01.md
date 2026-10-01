# Learning: dot-codex-worktree-git-writable-T50-a01

1. **`codex sandbox` is not the worker's sandbox.** In codex-cli 0.158, `codex sandbox` runs permission profiles only. Without `-P` it is read-only, and `-P :workspace` ignores the legacy `sandbox_workspace_write.writable_roots`. To test what a worker gets, read `codex doctor --json` (the effective filesystem policy) and confirm with a disposable `codex exec --sandbox workspace-write --json` run whose `command_execution` output is harness-captured. Status: validated (probes).
2. **A linked worktree's git metadata needs four roots.** `<common>/objects`, `refs`, `logs` and `worktrees/<name>` cover commit, fetch, rebase and local push; `packed-refs` is not required. Never grant the common dir itself. Status: validated (live exec).
3. **`-c` on an array replaces it.** Rebuild it from the configured value first, or the agmsg store roots silently disappear. Status: validated (doctor).
4. **Close stdin for `codex exec` in scripts.** Otherwise it waits on stdin ("Reading additional input from stdin...") until the outer timeout. Status: observed.

## Revision 2 triage

5. **Parse config with a real parser and fail closed.** A line matcher that misses a key must not turn an array-replacing `-c` into a narrower list. When in doubt, emit nothing and keep the configured value. Status: validated (tests).
6. **A grant's edges belong in the report and on stderr.** Shallow metadata (`<common>/shallow`) is outside the grant. Say so when it applies rather than widening the grant. Status: validated (test).
