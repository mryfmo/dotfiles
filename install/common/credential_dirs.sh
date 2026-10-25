#!/usr/bin/env bash

# @file install/common/credential_dirs.sh
# @brief Keep the credential directories private (mode 0700) on every apply.
# @description
#   Ubuntu's default umask 002 creates directories group-writable, so gh, age,
#   the AWS CLI and `chezmoi init` leave their credential directories at 0775 or
#   0771. This script sets each existing directory to 0700. A missing directory
#   is skipped. A directory that is a symlink, or that is reached through a
#   symlinked component below `$HOME` (or below `/` for a directory outside
#   `$HOME`), is warned about and left unchanged; trailing slashes are stripped
#   first, so `dir/` cannot hide a symlink. On macOS and the BSDs chmod runs with
#   `-h` (never follows a link). A chmod that fails stops the apply with a
#   message naming the directory.
#   shortcut: GNU chmod has no no-follow flag, so a symlink swapped in between
#   the check and the chmod is followed; that needs write access to `$HOME`.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

#
# @description Strip trailing slashes from a path (a bare `/` stays `/`).
# @arg $1 string Path.
# @stdout The path without trailing slashes.
#
function strip_trailing_slashes() {
    local path="$1"
    while [[ ${#path} -gt 1 && ${path: -1} == / ]]; do # lint-comparisons: allow the last character, not a path identity
        path="${path%/}"
    done
    printf '%s\n' "${path}"
}

#
# @description Return success when no component of a path is a symlink, checked below `$HOME`
#   for a path inside it and below `/` otherwise; `.` and `..` components count as unsafe.
# @arg $1 string Absolute path without trailing slashes.
# @arg $2 string `$HOME` without trailing slashes.
# @exitcode 1 A component is a symlink, `.` or `..`, or the path is relative.
#
function path_has_no_symlink() {
    local path="$1" home="$2" current rest component
    [[ ${path:0:1} == / ]] || return 1                  # lint-comparisons: allow the first character, not a path identity
    if [[ -n ${home} && ${path} == "${home}"/* ]]; then # lint-comparisons: allow a lexical prefix split, never an identity check
        current="${home}"
        rest="${path#"${home}"/}"
    else
        current=""
        rest="${path#/}"
    fi
    while [ -n "${rest}" ]; do
        component="${rest%%/*}"
        if [[ ${rest} == */* ]]; then # lint-comparisons: allow a separator test, not a path identity
            rest="${rest#*/}"
        else
            rest=""
        fi
        [ -n "${component}" ] || continue
        case "${component}" in
        . | ..) return 1 ;;
        esac
        current="${current}/${component}"
        [ ! -L "${current}" ] || return 1
    done
}

#
# @description Set one directory to mode 0700, never following a link when the chmod supports it.
# @arg $1 string Directory.
# @arg $2 string Non-empty when chmod takes `-h` (macOS, BSD).
#
function chmod_private() {
    if [ -n "$2" ]; then
        chmod -h 700 "$1"
    else
        chmod 700 "$1"
    fi
}

#
# @description Set every existing credential directory to mode 0700.
# @exitcode 0 Every existing directory now has mode 0700.
# @exitcode 1 chmod failed on a directory, or uname failed.
#
function secure_credential_dirs() {
    local config_home="${XDG_CONFIG_HOME:-${HOME}/.config}" dir home kernel no_follow="" status=0
    # An array, not a here-string: bash 3.2 writes a here-string to a temporary file, and a failed
    # write there would skip every chmod while the loop still returned success.
    local -a dirs=(
        "${GH_CONFIG_DIR:-${config_home}/gh}"
        "${config_home}/age"
        "${HOME}/.aws"
        "${HOME}/.local/share/chezmoi-private"
    )
    home="$(strip_trailing_slashes "${HOME}")" || return 1
    kernel="$(uname -s)" || {
        printf 'credential_dirs: uname -s failed; no directory mode was changed\n' >&2
        return 1
    }
    case "${kernel}" in
    Darwin | *BSD) no_follow=1 ;;
    esac
    for dir in "${dirs[@]}"; do
        dir="$(strip_trailing_slashes "${dir}")" || return 1
        if [ -L "${dir}" ] || ! path_has_no_symlink "${dir}" "${home}"; then
            printf 'warning: credential_dirs: %s is a symlink or is reached through one; its mode is left unchanged\n' "${dir}" >&2
            continue
        fi
        [ -d "${dir}" ] || continue
        if ! chmod_private "${dir}" "${no_follow}"; then
            printf 'credential_dirs: cannot set %s to mode 0700\n' "${dir}" >&2
            status=1
        fi
    done
    return "${status}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    secure_credential_dirs
fi
