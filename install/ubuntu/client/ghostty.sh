#!/usr/bin/env bash

# @file install/ubuntu/client/ghostty.sh
# @brief Install Ghostty on Ubuntu client machines.
# @description
#   Adds the community-maintained Ghostty Ubuntu PPA recommended by
#   mkasberg/ghostty-ubuntu and installs the `ghostty` package through apt.
#   A failure is attributed by the scope of the command that failed: a command
#   that touches only the PPA failing skips Ghostty with a retry line, and any
#   other failure stays fatal.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly GHOSTTY_PPA="ppa:mkasberg/ghostty-ubuntu"
# The URIs host and path of the PPA's apt source stanza.
readonly GHOSTTY_PPA_URL="ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/"
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
    # shellcheck disable=SC2016
    [ "$(dpkg-query -W -f '${db:Status-Status}' "$1" 2> /dev/null)" = installed ]
}

#
# @description Install packages required before adding the Ghostty PPA, only when they are missing,
#   so an existing machine reaches the PPA-only refresh without a system-wide one.
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
# @description Print that Ghostty was skipped because a step that fetches from its PPA failed.
# @arg $1 string The step that failed.
#
function skip_ghostty() {
    printf "ghostty not installed: %s (apt's output above); the next make update retries\n" "$1"
}

#
# @description Install Ghostty from apt, registering the PPA when no source names it.
# @exitcode 0 Ghostty is installed, or registering the PPA, refreshing its index or downloading
#   its package failed and Ghostty was skipped.
# @exitcode 1 add-apt-repository succeeded but no apt source names the PPA.
# @exitcode * Otherwise the status of the failed dependency, refresh or install command.
#
function install_ghostty() {
    local sources_file
    installed ghostty && return 0
    install_ghostty_dependencies
    sources_file="$(ghostty_source_file)"
    if [ -z "${sources_file}" ]; then
        if ! add_ghostty_ppa; then
            skip_ghostty "its PPA could not be registered"
            return 0
        fi
        sources_file="$(ghostty_source_file)"
        if [ -z "${sources_file}" ]; then
            echo "ghostty: add-apt-repository succeeded but no apt source names ${GHOSTTY_PPA_URL}" >&2
            return 1
        fi
    fi
    # Only the PPA's source is read, so a non-zero exit means its index could not be refreshed.
    if ! sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get update -o Dir::Etc::sourcelist="${sources_file}" \
        -o Dir::Etc::sourceparts=- -o APT::Get::List-Cleanup=0 -o APT::Update::Error-Mode=any; then
        skip_ghostty "its PPA index could not be refreshed"
        return 0
    fi
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get update
    if ! sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install -y --download-only "${PACKAGES[@]}"; then
        skip_ghostty "its package could not be downloaded"
        return 0
    fi
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install -y --no-download "${PACKAGES[@]}"
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
