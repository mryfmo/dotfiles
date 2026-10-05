# Learning: dotfiles-T83-docs-diet-a01

- **Never run `git worktree prune` from a sandboxed seat.** Other worktrees' paths can look missing from inside the sandbox, so prune targets their admin dirs in the shared `.git/worktrees`. Remove your own scratch worktree with `git worktree remove <path>` and stop there.
- **Repo-wide validators also read gitignored local state.** `validate_no_removed_claude_skill` walks `ROOT.rglob("*")`, so a session ledger that logged a quoted token fails it locally. Prove the tree on a clean checkout of the commit, and keep removed tokens out of subagent prompts.
- **Check a format rule against the parser before restating it.** The PR-integration rule said `audit-finding:` lines may be bulleted, but the gate strips only whitespace and skips a line that starts with a list marker; only the audit's `[P0-P3]` lines may be bulleted.
- **A "single source" claim needs a count test.** `assertEqual(skill.count(literal), 1)`, plus `assertNotIn` for every pointer file, catches the next copy-paste; an `assertIn` cannot.
