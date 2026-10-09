# Learning: dotfiles-T116-on-demand-workers-a01

Candidates only; nothing promoted.

1. Seat-label normalization rewrites a worker's self-named label to `<kind>-worker`, so a predicate that identifies a worker by its `<team>:<name>` label silently misses the manifest worker. Identify worker panes by cwd (a linked worktree) and the normalized labels, not by the raw label shape.
2. A lone positional after an optional-argument flag is ambiguous with the trailing optional DIR; deciding it by the argument's shape (`.claude/worktrees/*`) keeps both `--add-worker DIR` and the existing rejection of bad worktree paths.
3. When a large behavioural removal leaves a test file with sandbox-only failures, compare the failing-id list with an origin/main baseline run in the same sandbox, then run the new tests against the old script to show they can fail.
4. Grepping only allowed_files for a removed literal misses tests elsewhere that pin it (test_runtime_health pinned the deleted worker launch line); grep the whole tests/ tree before dispatch.
