# Learning triage: dot-formatter-hook-root-fix-T61-a01

Candidates only; nothing is promoted.

1. **ruff's per-file config bypasses root exclusions.**
   - Lesson: ruff resolves configuration per file, so a nested `pyproject.toml` with `[tool.ruff]` (here `vendor/compactiondb`) is outside the root `extend-exclude`, even with `force-exclude`. Repository-wide checks need `--config <root ruff.toml>`.
2. **prettier reads `.prettierignore` from its working directory.**
   - Lesson: a hook that runs in the session's cwd ignores the edited repository's ignore file whenever the session sits in another tree (worktree sessions editing main-checkout records). Run formatters from the file's git root.
3. **prettier corrupts tables whose code spans contain `|`.**
   - Lesson: the pipe is read as a cell separator, padded and split, and `*` globs become `_` emphasis, so the commands change. prettier is also not idempotent on some wrapped inline code in list items.
   - Before adopting prettier on prose that holds commands, scan for pipe-in-code table rows. A whitespace-normalized content check that discards `|` cannot see this class; that is how I missed plans/001 and 003 at first.
4. **Adding a formatter pin is not enough.** `make update` installs only selected mise tools. A new hook dependency needs an install step on existing machines, as a follow-up outside this task's files.
5. **The Codex bot reviews each push and keeps finding real issues.** Here it found five valid findings over four pushes. A worker should batch-fix and then stop at a defined point, listing the open threads for the orchestrator.
