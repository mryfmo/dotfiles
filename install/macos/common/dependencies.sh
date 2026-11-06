#!/usr/bin/env bash

# @file install/macos/common/dependencies.sh
# @brief Install essential Homebrew packages for macOS.
# @description
#   Installs the core command-line packages required by the dotfiles.
#   Optional utilities and GUI applications live in
#   `install/macos/common/misc.sh`.

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
        echo "install/macos/common/dependencies.sh: ci-runner helper unreadable: ${ci_runner_helper}" >&2
        exit 2
    fi
    # shellcheck source=scripts/lib/ci-runner.sh
    source "${ci_runner_helper}" || {
        echo "install/macos/common/dependencies.sh: ci-runner helper failed to source: ${ci_runner_helper}" >&2
        exit 2
    }
fi

readonly BREW_PACKAGES=(
    cmake
    git
    gawk
    gpg
    mosh
    pinentry-mac
    vim
    zsh
)

#
# @description Check whether a Homebrew package is already installed.
# @arg $1 string Homebrew package name.
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
        if is_ci_runner; then
            brew info "${missing_packages[@]}"
        else
            brew install --force "${missing_packages[@]}"
        fi
    fi
}

#
# @description Install the required Homebrew dependencies.
#
function main() {
    install_brew_packages
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
