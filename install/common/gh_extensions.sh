#!/usr/bin/env bash

# @file install/common/gh_extensions.sh
# @brief Install GitHub CLI extensions used by the dotfiles.
# @description
#   Activates `mise` when available and installs the configured `gh`
#   extensions only when GitHub CLI is already authenticated.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly MISE_BIN="${HOME}/.local/bin/mise"

readonly GH_EXTENSIONS=(
    seachicken/gh-poi
)

#
# @description Activate `mise` so `gh` can resolve the expected toolchain.
#
function activate_mise() {
    if [ -x "${MISE_BIN}" ]; then
        eval "$("${MISE_BIN}" activate bash)"
    fi
}

#
# @description Install every configured extension, or skip when unauthenticated.
#
function install_gh_extensions() {
    if ! gh auth status &> /dev/null; then
        printf '%s\n' 'Warning: GitHub CLI is not authenticated. Run setup-gh, then rerun chezmoi apply to install extensions.' >&2
        return 0
    fi

    for extension in "${GH_EXTENSIONS[@]}"; do
        gh extension install "${extension}"
    done
}

#
# @description Run the `gh` extension installation workflow.
#
function main() {
    activate_mise
    install_gh_extensions
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
