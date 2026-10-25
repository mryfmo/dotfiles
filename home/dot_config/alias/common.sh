#!/usr/bin/env bash

# @file home/dot_config/alias/common.sh
# @brief Shared shell aliases used across machines.
# @description
#   These aliases wrap common repository and local workflow commands.

# Use eza for ls command. In eza 0.23.5 `--icons` takes an optional WHEN value,
# so the bare flag swallows the first path argument and `ls dir` fails.
alias ls="eza --long --group --header --binary --time-style=long-iso --icons=auto"

# Alias for private chezmoi configuration
# ref. https://www.chezmoi.io/user-guide/frequently-asked-questions/design/#can-chezmoi-support-multiple-sources-or-multiple-source-states
alias chezmoi-private="chezmoi --source ~/.local/share/chezmoi-private --config ~/.config/chezmoi-private/chezmoi.yaml"

# Alias to checkout the default branch in git
alias gm='git checkout $(git symbolic-ref refs/remotes/origin/HEAD | sed "s@^refs/remotes/origin/@@")'
