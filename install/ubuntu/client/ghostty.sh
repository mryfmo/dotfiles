#!/usr/bin/env bash

# @file install/ubuntu/client/ghostty.sh
# @brief Install Ghostty on Ubuntu client machines.
# @description
#   Adds the community-maintained Ghostty Ubuntu PPA recommended by
#   mkasberg/ghostty-ubuntu and installs the `ghostty` package through apt.
#   When a Launchpad host the remaining steps need gives no answer, Ghostty is
#   skipped with a retry line before any apt call; once the hosts answer, every
#   failure stays fatal.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly GHOSTTY_PPA="ppa:mkasberg/ghostty-ubuntu"
# The URIs host and path of the PPA's apt source stanza.
readonly GHOSTTY_PPA_URL="ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/"
# Probed before any PPA step: the archive serves the index and the package, and
# add-apt-repository reads the PPA's record and signing key from the Launchpad API.
readonly GHOSTTY_ARCHIVE_PROBE="https://${GHOSTTY_PPA_URL}ubuntu/"
readonly GHOSTTY_API_PROBE="https://api.launchpad.net/devel/~mkasberg/+archive/ubuntu/ghostty-ubuntu"
readonly PACKAGES=(
    ghostty
)
readonly DEPENDENCY_PACKAGES=(
    software-properties-common
)

#
# @description Succeed when dpkg's database records a package as fully installed.
# @arg $1 string The package name.
# @exitcode 0 The package's status is installed.
# @exitcode 1 Any other status (half-configured, config-files, ...) or no record.
#
function installed() {
    local status
    # shellcheck disable=SC2016
    status="$(dpkg-query -W -f '${db:Status-Status}' "$1" 2> /dev/null)" || return 1
    [ "${status}" = installed ]
}

#
# @description Install packages required before adding the Ghostty PPA, only when they are missing,
#   so an existing machine refreshes the apt index once, after the PPA is registered.
#
function install_ghostty_dependencies() {
    installed software-properties-common && return 0
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get update
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install -y "${DEPENDENCY_PACKAGES[@]}"
}

#
# @description Print the apt source file that names the Ghostty PPA.
# @stdout The first .sources or .list file under APT_SOURCES_DIR (default /etc/apt/sources.list.d)
#   naming GHOSTTY_PPA_URL, or nothing when none does.
#
function ghostty_source_file() {
    local dir="${APT_SOURCES_DIR:-/etc/apt/sources.list.d}"
    grep -lsF "${GHOSTTY_PPA_URL}" "${dir}"/*.sources "${dir}"/*.list | head -n 1 || true
}

#
# @description Add the community-maintained Ghostty Ubuntu PPA without updating the package cache.
#
function add_ghostty_ppa() {
    sudo --preserve-env=http_proxy,https_proxy,no_proxy add-apt-repository -y -n "${GHOSTTY_PPA}"
}

#
# @description Print the first URL that gives no answer, so the PPA counts as unreachable.
# @arg $@ string The URLs to probe, in order.
# @stdout `<url> (<reason>)` for the first URL that fails to connect, resolve, finish TLS or
#   answer within the timeout (curl exit 5, 6, 7, 28, 35, 52 or 56), or answers HTTP 5xx;
#   nothing when every URL answers.
# @exitcode 0 Each URL answered or was found unreachable.
# @exitcode * Any other curl failure (a local error, not evidence of the network), unchanged.
#
function ghostty_unreachable_url() {
    local url code status
    for url in "$@"; do
        status=0
        code="$(curl --silent --show-error --output /dev/null --write-out '%{http_code}' \
            --connect-timeout 5 --max-time 15 "${url}")" || status=$?
        case "${status}" in
        0)
            if [[ ${code} == 5?? ]]; then
                printf '%s (HTTP %s)\n' "${url}" "${code}"
                return 0
            fi
            ;;
        5 | 6 | 7 | 28 | 35 | 52 | 56)
            printf '%s (curl exit %s)\n' "${url}" "${status}"
            return 0
            ;;
        *) return "${status}" ;;
        esac
    done
}

#
# @description Install Ghostty from apt, registering the PPA when no source names it.
# @exitcode 0 Ghostty is installed, or a Launchpad host it needs gave no answer and Ghostty was skipped.
# @exitcode 1 add-apt-repository succeeded but no apt source names the PPA.
# @exitcode * Otherwise the status of the failed probe, dependency, registration, refresh or install command.
#
function install_ghostty() {
    local sources_file unreachable
    local -a probes=("${GHOSTTY_ARCHIVE_PROBE}")
    installed ghostty && return 0
    sources_file="$(ghostty_source_file)"
    [ -n "${sources_file}" ] || probes+=("${GHOSTTY_API_PROBE}")
    unreachable="$(ghostty_unreachable_url "${probes[@]}")"
    if [ -n "${unreachable}" ]; then
        printf 'ghostty not installed: its PPA is unreachable: %s; the next make update retries\n' "${unreachable}"
        return 0
    fi
    install_ghostty_dependencies
    if [ -z "${sources_file}" ]; then
        add_ghostty_ppa
        sources_file="$(ghostty_source_file)"
        if [ -z "${sources_file}" ]; then
            echo "ghostty: add-apt-repository succeeded but no apt source names ${GHOSTTY_PPA_URL}" >&2
            return 1
        fi
    fi
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get update
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install -y "${PACKAGES[@]}"
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
