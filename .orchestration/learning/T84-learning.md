# T84 Learning

## Validated learning

1. A two-column `chezmoi status` code is insufficient to identify permission-only drift: an `MM` or ` M` entry can still have a diff containing only old/new mode lines. Inspecting the per-target diff and giving mode-only classification precedence produces the actionable class.
2. Chezmoi attributes compose after modifier semantics: `modify_private_<name>` keeps the source executable as a modifier while making the computed target private.
3. Zsh `(N-/)` directory filtering can be preserved with `[[ -d ]]` and array append, which retains symlink-following directory semantics while remaining parseable by repository shfmt/static gates.
4. Non-interactive SSH commands do not read `.zprofile` or `.zshrc`; shims-first PATH therefore belongs in `.zshenv`, not only in login/interactive startup.

## Apply to

- Future doctor drift triage and chezmoi permission fixes.
- Future zsh startup merges where deployed behavior predates source history.
- Generator/validator/runtime consumers whenever a chezmoi source attribute changes a generated filename.

The reusable decision was recorded in project memory; no separate Codex learn-index entry was added because the T84 allowed-file contract makes this orchestration learning artifact the authoritative record.

