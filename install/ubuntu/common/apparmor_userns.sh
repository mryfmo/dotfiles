#!/usr/bin/env bash

# @file install/ubuntu/common/apparmor_userns.sh
# @brief Install the AppArmor profile that lets bwrap create user namespaces.
# @description
#   Copies install/ubuntu/common/apparmor/bwrap-userns to /etc/apparmor.d and
#   loads it with apparmor_parser, so sandboxed Codex runs keep working under
#   kernel.apparmor_restrict_unprivileged_userns=1. It is a no-op when the
#   restriction is off or absent, or when apparmor_parser or /usr/bin/bwrap is
#   missing. The global sysctl is never changed.
#   Remove with: sudo apparmor_parser -R /etc/apparmor.d/bwrap-userns &&
#   sudo rm /etc/apparmor.d/bwrap-userns

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly RESTRICT_SYSCTL="${APPARMOR_USERNS_SYSCTL:-/proc/sys/kernel/apparmor_restrict_unprivileged_userns}"
readonly BWRAP_PATH="${APPARMOR_USERNS_BWRAP:-/usr/bin/bwrap}"
readonly PROFILE_TARGET="${APPARMOR_USERNS_PROFILE_TARGET:-/etc/apparmor.d/bwrap-userns}"

#
# @description Print the profile source path from the chezmoi source tree or this script's directory.
# @stdout Absolute or relative path to the bwrap-userns profile source.
#
function profile_source() {
    if [ -n "${APPARMOR_USERNS_PROFILE_SOURCE:-}" ]; then
        printf '%s\n' "${APPARMOR_USERNS_PROFILE_SOURCE}"
    elif [ -n "${CHEZMOI_SOURCE_DIR:-}" ]; then
        printf '%s\n' "${CHEZMOI_SOURCE_DIR}/../install/ubuntu/common/apparmor/bwrap-userns"
    else
        printf '%s\n' "$(dirname "${BASH_SOURCE[0]}")/apparmor/bwrap-userns"
    fi
}

#
# @description Print why the profile is not needed, or nothing when it is.
# @stdout One skip reason line, or nothing.
#
function skip_reason() {
    if [ "$(cat "${RESTRICT_SYSCTL}" 2> /dev/null)" != "1" ]; then
        printf 'AppArmor unprivileged userns restriction is not enabled\n'
    elif ! command -v apparmor_parser > /dev/null 2>&1; then
        printf 'apparmor_parser is not installed\n'
    elif [ ! -x "${BWRAP_PATH}" ]; then
        printf '%s is not installed\n' "${BWRAP_PATH}"
    fi
}

#
# @description Copy the profile into place and (re)load it; both steps are idempotent.
#
function install_profile() {
    local source
    source="$(profile_source)"
    sudo install -m 0644 "${source}" "${PROFILE_TARGET}"
    sudo apparmor_parser -r "${PROFILE_TARGET}"
}

#
# @description Install the bwrap user-namespace profile when the host needs it.
#
function main() {
    local reason
    reason="$(skip_reason)"
    if [ -n "${reason}" ]; then
        printf 'Skipping bwrap AppArmor userns profile: %s.\n' "${reason}"
        return 0
    fi
    install_profile
    printf 'Loaded AppArmor profile bwrap-userns from %s.\n' "${PROFILE_TARGET}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
