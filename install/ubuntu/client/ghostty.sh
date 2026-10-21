#!/usr/bin/env bash

# @file install/ubuntu/client/ghostty.sh
# @brief Install Ghostty on Ubuntu client machines.
# @description
#   Adds the community-maintained Ghostty Ubuntu PPA recommended by
#   mkasberg/ghostty-ubuntu and installs the `ghostty` package through apt.
#   A PPA that apt cannot fetch from (a Launchpad outage) skips Ghostty with
#   one retry line and never fails the apply; every other failure still fails.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly GHOSTTY_PPA="ppa:mkasberg/ghostty-ubuntu"
readonly GHOSTTY_PPA_HOST="ppa.launchpadcontent.net"
readonly PACKAGES=(
    ghostty
)
readonly DEPENDENCY_PACKAGES=(
    software-properties-common
)

#
# @description Install packages required before adding the Ghostty PPA.
#
function install_ghostty_dependencies() {
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get update
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install -y "${DEPENDENCY_PACKAGES[@]}"
}

#
# @description Add the community-maintained Ghostty Ubuntu PPA.
#
function add_ghostty_ppa() {
    sudo --preserve-env=http_proxy,https_proxy,no_proxy add-apt-repository -y "${GHOSTTY_PPA}"
}

#
# @description Run one step that fetches from the Ghostty PPA, passing its output through.
# @arg $@ string The command to run.
# @exitcode 0 The step succeeded.
# @exitcode 75 The step failed because apt could not fetch from the PPA host.
# @exitcode 1 The step failed for any other reason (its own status is not kept).
#
function ppa_step() {
    local output status=0
    output="$("$@" 2>&1)" || status=$?
    printf '%s\n' "${output}"
    [ "${status}" -eq 0 ] && return 0
    grep -qF -e "Failed to fetch https://${GHOSTTY_PPA_HOST}/" -e "Failed to fetch http://${GHOSTTY_PPA_HOST}/" <<< "${output}" && return 75
    return 1
}

#
# @description Install Ghostty from apt after the PPA has been configured; an unreachable PPA skips it.
#
function install_ghostty() {
    local status=0
    install_ghostty_dependencies
    {
        ppa_step add_ghostty_ppa &&
            ppa_step sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get update &&
            ppa_step sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install -y "${PACKAGES[@]}"
    } || status=$?
    if [ "${status}" -eq 75 ]; then
        echo "ghostty not installed: ${GHOSTTY_PPA} is unreachable; the next make update retries"
        return 0
    fi
    return "${status}"
}

#
# @description Remove Ghostty without removing the configured PPA.
#
function uninstall_ghostty() {
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get remove -y "${PACKAGES[@]}"
}

#
# @description Run the Ghostty installation flow.
#
function main() {
    install_ghostty
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
