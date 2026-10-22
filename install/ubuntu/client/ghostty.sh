#!/usr/bin/env bash

# @file install/ubuntu/client/ghostty.sh
# @brief Install Ghostty on Ubuntu client machines.
# @description
#   Adds the community-maintained Ghostty Ubuntu PPA recommended by
#   mkasberg/ghostty-ubuntu and installs the `ghostty` package through apt.
#   A PPA that apt cannot fetch from (a Launchpad outage) skips Ghostty with
#   one retry line and never fails the apply; every other failure still fails.
#   It runs from a run_after_ script at every apply, so an installed Ghostty
#   is left as it is and a skipped one is retried by the next apply.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly GHOSTTY_PPA="ppa:mkasberg/ghostty-ubuntu"
readonly GHOSTTY_PPA_URL="ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/"
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
# @exitcode 75 apt's only errors are fetch failures from the Ghostty PPA and apt's summary of them, whatever
#   its own exit (apt-get update exits 0 when an index fails to download). The step runs under LC_ALL=C LANG=C,
#   which sudo keeps, so apt's diagnostics are the English forms on every locale.
# @exitcode * Otherwise the step's own status: any other apt error stays fatal.
#
function ppa_step() {
    local output status=0 line fetch=0
    output="$(LC_ALL=C LANG=C "$@" 2>&1)" || status=$?
    printf '%s\n' "${output}"
    while IFS= read -r line; do
        case ${line} in
        [EW]": Failed to fetch https://${GHOSTTY_PPA_URL}"* | [EW]": Failed to fetch http://${GHOSTTY_PPA_URL}"*) fetch=1 ;;
        "Err:"*" https://${GHOSTTY_PPA_URL}"* | "Err:"*" http://${GHOSTTY_PPA_URL}"*) ;;
        [EW]": Some index files failed to download"* | "E: Unable to fetch some archives"*) ;;
        "E:"* | "Err:"* | "W: Failed to fetch"*) return "${status}" ;;
        esac
    done <<< "${output}"
    [ "${fetch}" -eq 0 ] || return 75
    return "${status}"
}

#
# @description Install Ghostty from apt after the PPA has been configured; an unreachable PPA skips it.
#
function install_ghostty() {
    local status=0
    # Only a completed install is skipped: the database status, not dpkg -s's exit (dpkg-query(1): Status-Status).
    # shellcheck disable=SC2016
    if [ "$(dpkg-query -W -f '${db:Status-Status}' "${PACKAGES[@]}" 2> /dev/null || true)" = installed ]; then
        return 0
    fi
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
