#!/usr/bin/env bash

# @file install/ubuntu/client/default_shell.sh
# @brief Set zsh as the login shell on Ubuntu client machines.

set -Eeuo pipefail

#
# @description Change the current user's login shell to zsh when needed.
#
function main() {
    local current_shell zsh_path

    zsh_path="$(command -v zsh)"
    current_shell="$(getent passwd "${USER}" | cut -d: -f7)"

    if [ "${current_shell}" = "${zsh_path}" ]; then
        printf 'Login shell is already %s.\n' "${zsh_path}"
        return
    fi

    if ! grep -Fxq "${zsh_path}" /etc/shells; then
        printf '%s\n' "${zsh_path}" | sudo tee -a /etc/shells > /dev/null
    fi

    sudo chsh -s "${zsh_path}" "${USER}"
    # shellcheck disable=SC2016 # Backticks are literal operator guidance.
    printf 'Login shell changed to %s; sign in again or run `exec zsh`.\n' "${zsh_path}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
