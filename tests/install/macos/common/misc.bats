#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/macos/common/misc.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

@test "[macos] misc" {
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"

    #
    # brew packages
    #
    run brew info gpg
    [ "${status}" -eq 0 ]
    run brew info htop
    [ "${status}" -eq 0 ]
    run brew info pinentry-mac
    [ "${status}" -eq 0 ]
    run brew info tailscale
    [ "${status}" -eq 0 ]
    run brew info vim
    [ "${status}" -eq 0 ]
    run brew info watchexec
    [ "${status}" -eq 0 ]
    run brew info zsh
    [ "${status}" -eq 0 ]

    #
    # Cask packages
    #

    # Currently, we do not run this test on CI
    # because of the time it takes to install the cask packages.
}

@test "[macos] misc leaves Herdr to mise, excludes VS Code, and includes Zed cask" {
    [[ " ${BREW_PACKAGES[*]} " != *" herdr "* ]]
    [[ " ${CASK_PACKAGES[*]} " != *" visual-studio-code "* ]]
    [[ " ${CASK_PACKAGES[*]} " == *" zed "* ]]
}

@test "[macos] tailscale is a regular brew package installed for every user" {
    [[ " ${BREW_PACKAGES[*]} " == *" tailscale "* ]]
    ! declare -F install_additional_brew_packages > /dev/null
    ! declare -p ADDITIONAL_BREW_PACKAGES > /dev/null 2>&1

    local calls_path="${BATS_TEST_TMPDIR}/brew_calls.txt"
    : > "${calls_path}"

    run env CALLS_PATH="${calls_path}" CI=false bash -c '
        source "'"${SCRIPT_PATH}"'"

        whoami() {
            echo "s.kitada"
        }

        is_brew_package_installed() {
            [ "$1" != "tailscale" ]
        }

        brew() {
            echo "$*" >> "${CALLS_PATH}"
        }

        install_brew_packages
    '

    [ "${status}" -eq 0 ]

    run cat "${calls_path}"
    [ "${status}" -eq 0 ]
    [ "${output}" = "install --force tailscale" ]
}
