# T84 Report

Status: `ready_for_review`

cost: n/a

`effects=none`

T84 resolves the three observed chezmoi drift classes without applying or overwriting the deployed state.

## Result

- Merged the deployed zsh hardening into source while retaining source behavior: `.zshenv` keeps shims-first PATH for non-interactive SSH/Mosh/Herdr, `.zprofile` keeps explicit directory ordering plus existence filtering and guarded `mise activate zsh --shims`, and `.zshrc` keeps guarded interactive mise/sheldon, filtered fpath, Herdr dispatch, and the Claude updater.
- Renamed all five runtime-written Codex profile modifiers to `modify_private_<profile>.config.toml`. Deep now has no mode drift; express, review, security, and standard correctly show pending 0644 -> 0600 mode-only source changes.
- Updated the generator, validator, runtime target mapping, and affected unit expectations to use the composed `modify_private_` naming.
- Added read-only doctor detection based on `chezmoi status`; every drift target is WARN-only, with mode-only diffs taking the permission-divergence hint, ` M` taking unapplied-source, and `MM` taking two-sided drift. WARN findings never enter the existing REPAIR map.
- Added focused tests for status classification/failure behavior and kept the full 338-test suite green.

## Project memory

[memory: decision — Resolve chezmoi drift by class: merge destination-only behavior hunk-by-hunk, represent permissions with composed source attributes, and keep doctor detection WARN-only with no automatic apply.]

Recorded as `226c1bd7-6f3a-4230-8e67-31d14221ddd4` with:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "Resolve chezmoi drift by class: merge uncommitted destination behavior into source hunk-by-hunk, encode permission drift with composed source attributes such as modify_private_, and keep doctor detection WARN-only with no automatic apply. For zsh, preserve non-interactive shims-first PATH in .zshenv and retain guarded mise/sheldon initialization."
```

## Review

Crit data review approved with resolved scope record `r_0f7b46`. Evidence: `.agents/worklog/codex/review/T84-crit-comments.json`; receipt: `.agents/worklog/codex/review/T84-review-receipt.md`.
