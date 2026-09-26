#!/usr/bin/env bash

# @file install/ubuntu/common/bwrap_apparmor.sh
# @brief Allow bubblewrap to create user namespaces on Ubuntu 24.04 and later.
# @description
#   The Claude Code Bash sandbox runs commands through `bwrap`. When
#   `kernel.apparmor_restrict_unprivileged_userns` is `1`, the default AppArmor
#   policy blocks the user namespaces bwrap needs, so this installs the profile
#   from the Claude Code sandboxing documentation and reloads AppArmor. It is a
#   no-op when the sysctl is absent or `0`, or when the profile already matches.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly USERNS_SYSCTL="${BWRAP_APPARMOR_SYSCTL:-/proc/sys/kernel/apparmor_restrict_unprivileged_userns}"
readonly PROFILE_PATH="${BWRAP_APPARMOR_PROFILE:-/etc/apparmor.d/bwrap}"
readonly PROFILE_CONTENT='abi <abi/4.0>,
include <tunables/global>

profile bwrap /usr/bin/bwrap flags=(unconfined) {
  userns,
  include if exists <local/bwrap>
}'

#
# @description Install the bwrap AppArmor profile when user namespaces are restricted.
#
function main() {
    if [ ! -r "${USERNS_SYSCTL}" ] || [ "$(< "${USERNS_SYSCTL}")" != "1" ]; then
        printf 'Unprivileged user namespaces are not restricted; skipping the bwrap AppArmor profile.\n'
        return 0
    fi

    if [ -f "${PROFILE_PATH}" ] && [ "$(< "${PROFILE_PATH}")" = "${PROFILE_CONTENT}" ]; then
        printf 'The bwrap AppArmor profile is already installed.\n'
        return 0
    fi

    printf '%s\n' "${PROFILE_CONTENT}" | sudo tee "${PROFILE_PATH}" > /dev/null
    if systemctl is-active --quiet apparmor; then
        sudo systemctl reload apparmor
    else
        printf 'AppArmor is not active; %s takes effect when AppArmor starts.\n' "${PROFILE_PATH}"
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
