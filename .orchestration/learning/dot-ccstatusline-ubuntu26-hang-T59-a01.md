# Learning triage: dot-ccstatusline-ubuntu26-hang-T59-a01

Candidates only; nothing is promoted.

1. **A "hang" can be a cold page cache on a lazily hydrated runner image.**
   - Lesson: the first exec of a large preinstalled binary that nothing has touched yet, here a 126 MB `/usr/local/bin/node`, can take seconds on a fresh image. It shows up as page faults, not syscalls.
   - Diagnose it with `fincore` before and after the run, plus cold-order timing in which no earlier step warms the binary.
   - Check the step order: a warm-up call in the diagnostics hides the very effect being measured. Diagnostics 1 did exactly that.
2. **mise shims fall back to SYSTEM outside their config.**
   - Lesson: a smoke that overrides `HOME` and runs outside the mise config directory makes `#!/usr/bin/env node` resolve to the system runtime, not the pinned one. Smokes of "exact" npm tools should put `$(mise where node)/bin` first on `PATH` and assert where `node` resolves.
3. **Dangling symlinks break `Path.exists()` guards.**
   - Lesson: when building a symlink farm from `/usr/bin` and `/bin` (the same directory on usr-merged images), the existence guard needs `exists() or is_symlink()` (or `os.path.lexists`). Otherwise a dangling link is re-created and raises `FileExistsError`.
4. **The formatter hook rewrites Python files too.** An Edit-tool change to a test file triggered the PostToolUse formatter (+21/−7 unrelated). Restore and apply the change with a script for scoped edits; the same lesson as T57's README.
