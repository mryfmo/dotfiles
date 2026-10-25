#!/usr/bin/env bash

# @file install/macos/common/docker.sh
# @brief Install Docker Desktop on macOS.
# @description
#   Installs the Docker Desktop cask through Homebrew.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

# The chezmoi script includes scripts/lib/ci-runner.sh before this file; a direct run sources it.
if ! declare -F is_ci_runner > /dev/null; then
    # shellcheck source=scripts/lib/ci-runner.sh
    source "$(dirname "${BASH_SOURCE[0]}")/../../../scripts/lib/ci-runner.sh"
fi

#
# @description Validate the Docker Desktop cask on a CI runner or install it locally.
#
function install_docker() {
    if is_ci_runner; then
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
