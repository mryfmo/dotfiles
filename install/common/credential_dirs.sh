#!/usr/bin/env bash

# @file install/common/credential_dirs.sh
# @brief Keep the credential directories private (mode 0700) on every apply.
# @description
#   Ubuntu's default umask 002 creates directories group-writable, so gh, age,
#   the AWS CLI and `chezmoi init` leave their credential directories at 0775 or
#   0771. This script sets each existing directory to 0700. A missing directory
#   is skipped; a symlink is warned about and not followed; a chmod that fails
#   stops the apply with a message naming the directory.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

#
# @description Print the credential directories, one per line.
# @stdout Absolute directory paths.
#
function credential_dirs() {
    local config_home="${XDG_CONFIG_HOME:-${HOME}/.config}"
    printf '%s\n' \
        "${GH_CONFIG_DIR:-${config_home}/gh}" \
        "${config_home}/age" \
        "${HOME}/.aws" \
        "${HOME}/.local/share/chezmoi-private"
}

#
# @description Set every existing credential directory to mode 0700.
# @exitcode 0 Every existing directory now has mode 0700.
# @exitcode 1 chmod failed on a directory.
#
function secure_credential_dirs() {
    local dir dirs status=0
    dirs="$(credential_dirs)" || return 1
    while IFS= read -r dir; do
        if [ -L "${dir}" ]; then
            printf 'warning: credential_dirs: %s is a symlink; its target'"'"'s mode is left unchanged\n' "${dir}" >&2
            continue
        fi
        [ -d "${dir}" ] || continue
        if ! chmod 700 "${dir}"; then
            printf 'credential_dirs: cannot set %s to mode 0700\n' "${dir}" >&2
            status=1
        fi
    done <<< "${dirs}"
    return "${status}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    secure_credential_dirs
fi
