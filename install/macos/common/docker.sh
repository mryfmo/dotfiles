#!/usr/bin/env bash

# @file install/macos/common/docker.sh
# @brief Install Docker Desktop on macOS.
# @description
#   Installs the Docker Desktop cask through Homebrew.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

# The chezmoi script includes scripts/lib/ci-runner.sh before this file, so the rendered run_once already defines
# is_ci_runner; a direct run (a test, an operator's shell) sources it from the tree. The helper's directory is a
# parameter expansion, never a command substitution: the Ubuntu client's snap-unavailable test runs its installer
# with an empty PATH, and a producer's status would be lost in the source line (standing order 21, regime-cutover
# U297c, U301). A helper that cannot be read or sourced refuses here, naming its path: no is_ci_runner decision below
# may run without it. One block in the five installers, pinned by tests/unit/test_ci_runner.py; copy it whole.
if ! declare -F is_ci_runner > /dev/null; then
    case ${BASH_SOURCE[0]} in
    */*) ci_runner_helper="${BASH_SOURCE[0]%/*}/../../../scripts/lib/ci-runner.sh" ;;
    *) ci_runner_helper="../../../scripts/lib/ci-runner.sh" ;;
    esac
    if [ ! -r "${ci_runner_helper}" ]; then
        echo "install/macos/common/docker.sh: ci-runner helper unreadable: ${ci_runner_helper}" >&2
        exit 2
    fi
    # shellcheck source=scripts/lib/ci-runner.sh
    source "${ci_runner_helper}" || {
        echo "install/macos/common/docker.sh: ci-runner helper failed to source: ${ci_runner_helper}" >&2
        exit 2
    }
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
