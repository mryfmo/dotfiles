# Learning triage: dotfiles-T128-settings-hook-dedupe-followup-a01

These are candidates only; nothing is promoted.

1. [memory:decision] A predicate that matches a rendered command against known renderings compares the command string itself (stripped), not a shell tokenisation of it: `shlex` removes quotes and escapes that change the shell's meaning, so `'~/x'` and `\~/x` would match `~/x`.
