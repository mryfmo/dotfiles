#!/usr/bin/env bash

# @file install/ubuntu/common/apparmor_userns.sh
# @brief Install the AppArmor profile that lets bwrap create user namespaces.
# @description
#   Loads install/ubuntu/common/apparmor/bwrap-userns with apparmor_parser and
#   copies it to /etc/apparmor.d, so sandboxed Codex runs keep working under
#   kernel.apparmor_restrict_unprivileged_userns=1. It is a no-op when the
#   restriction is off or absent, when apparmor_parser or /usr/bin/bwrap is
#   missing, or when the installed copy equals the source and bwrap can already
#   create a user namespace (the profile is loaded). The global sysctl is never
#   changed.
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
# @description Print why the profile is not needed, or nothing when it is. A host without the
#   sysctl has no restriction; a sysctl that exists but cannot be read decides nothing.
# @stdout One skip reason line, or nothing.
# @exitcode 1 The restriction sysctl exists but cannot be read.
#
function skip_reason() {
    local restrict=""
    if [ -e "${RESTRICT_SYSCTL}" ]; then
        restrict="$(cat "${RESTRICT_SYSCTL}")" || {
            printf 'cannot read %s; the bwrap AppArmor userns profile was not changed.\n' "${RESTRICT_SYSCTL}" >&2
            return 1
        }
    fi
    if [ "${restrict}" != "1" ]; then
        printf 'AppArmor unprivileged userns restriction is not enabled\n'
    elif ! command -v apparmor_parser > /dev/null 2>&1; then
        printf 'apparmor_parser is not installed\n'
    elif [ ! -x "${BWRAP_PATH}" ]; then
        printf '%s is not installed\n' "${BWRAP_PATH}"
    fi
}

#
# @description Load the profile, then copy it into place; both steps are idempotent.
#   Never prompts: without cached sudo credentials it leaves the profile pending.
# @exitcode 0 Profile loaded, or left pending without cached sudo credentials.
# @stderr Pending notice with the manual remedy when sudo would prompt.
#
function install_profile() {
    local source="$1"
    sudo -n true 2> /dev/null || {
        echo "apparmor bwrap-userns profile pending: run 'sudo -v && bash install/ubuntu/common/apparmor_userns.sh', or cache sudo before the next chezmoi apply, which retries" >&2
        return 0
    }
    sudo -n apparmor_parser -r "${source}"
    sudo -n install -m 0644 "${source}" "${PROFILE_TARGET}"
    printf 'Loaded AppArmor profile bwrap-userns from %s.\n' "${PROFILE_TARGET}"
}

#
# @description Succeed when bwrap can create a user namespace, the effect the loaded profile
#   grants; the same unprivileged probe `make doctor` runs. A profile file in /etc/apparmor.d
#   proves nothing: a copy whose load failed sits there unloaded.
#
function profile_is_effective() {
    "${BWRAP_PATH}" --ro-bind / / true > /dev/null 2>&1
}

#
# @description Install the bwrap user-namespace profile when the host needs it, unless the
#   installed copy equals the source and bwrap already works under it. chezmoi runs this on every
#   apply (run_after_), so a pending or failed install is retried without the operator
#   remembering it; a working host costs one cmp and one bwrap probe.
#
function main() {
    local reason source
    reason="$(skip_reason)" || return 1
    if [ -n "${reason}" ]; then
        printf 'Skipping bwrap AppArmor userns profile: %s.\n' "${reason}"
        return 0
    fi
    source="$(profile_source)"
    if cmp -s "${source}" "${PROFILE_TARGET}" && profile_is_effective; then
        return 0
    fi
    install_profile "${source}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
