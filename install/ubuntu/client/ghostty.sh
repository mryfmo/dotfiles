#!/usr/bin/env bash

# @file install/ubuntu/client/ghostty.sh
# @brief Install Ghostty on Ubuntu client machines.
# @description
#   Adds the community-maintained Ghostty Ubuntu PPA recommended by
#   mkasberg/ghostty-ubuntu and installs the `ghostty` package through apt.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly GHOSTTY_PPA="ppa:mkasberg/ghostty-ubuntu"
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
# @description Install Ghostty from apt after the PPA has been configured.
#
function install_ghostty() {
    install_ghostty_dependencies
    add_ghostty_ppa
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get update
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install -y "${PACKAGES[@]}"
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
