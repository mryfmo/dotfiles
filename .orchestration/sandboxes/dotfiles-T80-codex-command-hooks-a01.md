# Sandbox: dotfiles-T80-codex-command-hooks-a01

- **Sandboxed:** edits, tests, render-check, validate, ruff and the commits.
- **Unsandboxed:** the schema fetch (`curl` to developers.openai.com), the pushes, `gh pr create`, `gh pr checks` and `gh api`, CompactionDB `memory add`, and these artifact writes.
- **Not done:** nothing in the main checkout besides these artifacts; no merge, force push, push to main, thread resolution, local bats, or `make update`/`apply`/`upgrade`.
