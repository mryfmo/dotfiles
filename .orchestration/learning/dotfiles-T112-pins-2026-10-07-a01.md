# Learning: dotfiles-T112-pins-2026-10-07-a01

- **CI derives `DOTFILES_MISE_VERSION` from the manifest pin** (`.github/workflows/{test,macos,docs}.y*ml` echo `${pin}` into `GITHUB_ENV`), so a mise pin bump needs no workflow edit. A `git grep` for each old version string outside `mise.lock` and `.orchestration` is a quick way to show that no other copy of a pin exists.
- **zsh's `echo` interprets `\b` as a backspace,** so a command line logged with `echo` into a validation file loses its regex escapes. Log command lines with `printf '%s\n'` or a quoted heredoc.
- No rule candidate is promoted.
