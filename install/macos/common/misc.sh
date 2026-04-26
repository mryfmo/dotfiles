#!/usr/bin/env bash

# @file install/macos/common/misc.sh
# @brief Install optional macOS utilities and GUI applications.
# @description
#   Installs non-essential brew packages, casks, and user-specific extras for
#   daily development use.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly BREW_PACKAGES=(
    htop
    ghostty-notifier
    watchexec
)

readonly CASK_PACKAGES=(
    cyberduck
    google-chrome
    google-drive
    google-japanese-ime
    ngrok
    slack
    rectangle
    visual-studio-code
    1password
)

# Additional brew packages installed only for user mryfmo.
readonly ADDITIONAL_BREW_PACKAGES=(
    tailscale
)

#
# @description Check whether a brew package or cask is already installed.
# @arg $1 string Package or cask name.
#
function is_brew_package_installed() {
    local package="$1"

    brew list "${package}" &> /dev/null
}

#
# @description Install every missing package from `BREW_PACKAGES`.
#
function install_brew_packages() {
    local missing_packages=()

    for package in "${BREW_PACKAGES[@]}"; do
        if ! is_brew_package_installed "${package}"; then
            missing_packages+=("${package}")
        fi
    done

    if [[ ${#missing_packages[@]} -gt 0 ]]; then
        if "${CI:-false}"; then
            brew info "${missing_packages[@]}"
        else
            brew install --force "${missing_packages[@]}"
        fi
    fi
}

#
# @description Install every missing cask from `CASK_PACKAGES`.
#
function install_brew_cask_packages() {
    local missing_packages=()

    for package in "${CASK_PACKAGES[@]}"; do
        if ! is_brew_package_installed "${package}"; then
            missing_packages+=("${package}")
        fi
    done

    if [[ ${#missing_packages[@]} -gt 0 ]]; then
        if "${CI:-false}"; then
            brew info --cask "${missing_packages[@]}"
        else
            brew install --cask --force "${missing_packages[@]}"
        fi
    fi
}

#
# @description Install additional brew packages for the primary user only.
#
function install_additional_brew_packages() {
    # Restrict personal packages to the primary user account.
    if [[ "$(whoami)" != "mryfmo" ]]; then
        return 0
    fi

    local missing_packages=()

    for package in "${ADDITIONAL_BREW_PACKAGES[@]}"; do
        if ! is_brew_package_installed "${package}"; then
            missing_packages+=("${package}")
        fi
    done

    if [[ ${#missing_packages[@]} -gt 0 ]]; then
        if "${CI:-false}"; then
            brew info "${missing_packages[@]}"
        else
            brew install --force "${missing_packages[@]}"
        fi
    fi
}

#
# @description Open Google Chrome and prompt it to become the default browser.
#
function setup_google_chrome() {
    open "/Applications/Google Chrome.app" --args --make-default-browser
}

#
# @description Install the configured optional macOS packages and casks.
#
function main() {
    install_brew_packages
    install_brew_cask_packages
    install_additional_brew_packages

    # setup_google_chrome
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
