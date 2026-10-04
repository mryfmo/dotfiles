# Learning triage: dotfiles-T74-bootstrap-dead-code-a01

Candidates only; nothing is promoted.

1. **A branch can be dead code and a guard at once.** An `else fail` beside empty includes is still a platform check. When deleting dead branches, keep the guard semantics, or state that the change removes them.
2. **`chezmoi execute-template` uses the configured source dir.** Point it at a worktree with `--source <dir>`, and isolate config and state with `--config` and `--persistent-state` temp paths.
3. **Diff rendered output.** Before and after a template simplification, the rendered output (blank lines ignored) is a cheap behaviour-equivalence check.
