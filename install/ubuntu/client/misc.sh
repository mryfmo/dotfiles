#!/usr/bin/env bash

# @file install/ubuntu/client/misc.sh
# @brief Install optional Ubuntu client applications.
# @description
#   Installs or removes a small set of GUI applications used on Ubuntu client
#   machines.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly PACKAGES=(
    gparted
    # Chromium/Electron runtime libraries used by terminal-code and
    # terminal-browser; their installers only warn when these are missing.
    # libgtk-3-0 and libasound2 use their t64 package names on Ubuntu 24.04.
    libnss3
    libgtk-3-0t64
    libasound2t64
    libgbm1
)

#
# @description Install the optional Ubuntu client packages.
#
function install_misc() {
    sudo apt-get install -y "${PACKAGES[@]}"
}

#
# @description Remove the optional Ubuntu client packages.
#
function uninstall_misc() {
    sudo apt-get remove -y "${PACKAGES[@]}"
}

#
# @description Run the optional Ubuntu client package installation flow.
#
function main() {
    install_misc
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
