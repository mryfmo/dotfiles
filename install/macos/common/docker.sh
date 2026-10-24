#!/usr/bin/env bash

# @file install/macos/common/docker.sh
# @brief Install Docker Desktop on macOS.
# @description
#   Installs the Docker Desktop cask through Homebrew.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

#
# @description Validate the Docker Desktop cask in CI or install it locally.
#
function install_docker() {
    if [[ "${CI:-}" == "true" ]]; then
        brew info --cask docker
    else
        brew install --cask docker
    fi
}

#
# @description Run the Docker Desktop installation flow.
#
function main() {
    install_docker
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
