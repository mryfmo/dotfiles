#!/usr/bin/env bash

# @file install/macos/common/brew.sh
# @brief Install Homebrew and apply repository defaults.
# @description
#   Ensures Homebrew is installed on macOS and disables analytics for the local
#   user.

set -Eeuo pipefail

readonly HOMEBREW_INSTALL_COMMIT="c7952e40b7957268f61643152f4db725379b292e"
readonly HOMEBREW_INSTALL_SHA256="99287f194a8b3c9e6b0203a11a5fa54518be57209343e6bb954dec4635796d9d"

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

#
# @description Check whether Homebrew is already available on `PATH`.
#
function is_homebrew_exists() {
    command -v brew &> /dev/null
}

#
# @description Install Homebrew when it is not present.
#
function install_homebrew() {
    if ! is_homebrew_exists; then
        (
            local actual installer
            installer="$(mktemp)"
            trap 'rm -f "${installer}"' EXIT
            curl -fsSL "https://raw.githubusercontent.com/Homebrew/install/${HOMEBREW_INSTALL_COMMIT}/install.sh" -o "${installer}"
            actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
            [ "${actual}" = "${HOMEBREW_INSTALL_SHA256}" ] || {
                printf 'Homebrew installer checksum mismatch\n' >&2
                return 1
            }
            NONINTERACTIVE=1 /bin/bash "${installer}"
        )
    fi
}

#
# @description Disable Homebrew analytics for the current user.
#
function opt_out_of_analytics() {
    brew analytics off
}

#
# @description Install Homebrew and apply repository defaults.
#
function main() {
    install_homebrew
    opt_out_of_analytics
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
