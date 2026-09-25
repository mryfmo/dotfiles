# Learning

[memory:failure] Setting MISE_CONFIG_DIR alone does not prevent ancestor config discovery of the live ~/.config/mise symlink. Bound discovery with MISE_CEILING_PATHS at the checkout and export the configuration scope for every lifecycle call. Confirmed with native config ls and spill fixtures.
[memory:decision] Chezmoi regular-file include templates with trailing whitespace trim preserve source bytes; real temporary apply replaces symlinks and breaks the runtime-to-source write path.
No automatic skill/rule promotion.

## PR172 revision
Applied copies require explicit refresh after canonical upgrade. Compare physical checkout paths using source-path git toplevel, preserve worktree isolation, and propagate targeted apply failure. Four fixture outcomes and the full suite validate this decision.
