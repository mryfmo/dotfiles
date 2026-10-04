# Learning triage: dotfiles-T67-audit-task-level-a01

Candidates only; nothing is promoted.

1. **Artifact names have history.** A path convention that tasks define (`<id>.md`) was not always followed: T24 used `.txt`. Code that discovers artifacts should accept the established variants, or read the task's `expected_*` fields.
2. **Track whether a flag was given, not just its value.** A flag whose empty value means "not given" lets `--flag ""` silently change the mode.
3. **The sandbox's phantom `.git/config.lock`.** The Claude sandbox's deny-mask mount point leaves an empty read-only lock file in the shared git dir. While it exists, every unsandboxed git config write in that repository fails, for example `push -u` and `branch --set-upstream`. Branch creation already works around it with `git symbolic-ref`.
