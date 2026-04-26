#!/usr/bin/env bash

# @file install/macos/common/ghostty.sh
# @brief Install Ghostty on macOS.
# @description
#   Installs the Ghostty Homebrew cask and provides helpers for launching or
#   removing the application.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

#
# @description Install the Ghostty Homebrew cask.
#
function install_ghostty() {
    brew install --cask ghostty
}

#
# @description Uninstall the Ghostty Homebrew cask.
#
function uninstall_ghostty() {
    brew uninstall --cask ghostty
}

#
# @description Open Ghostty until the application can be launched.
#
function initialize_ghostty() {
    while ! open -g "/Applications/Ghostty.app"; do
        sleep 2
    done
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
