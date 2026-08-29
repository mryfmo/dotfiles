#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/misc.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

function teardown() {
    run uninstall_misc
}

@test "[ubuntu-client] PACKAGES for misc" {
    num_packages="${#PACKAGES[@]}"
    [ $num_packages -eq 5 ]

    expected_packages=(
        gparted
        libnss3
        libgtk-3-0
        libasound2t64
        libgbm1
    )
    for ((i = 0; i < ${#expected_packages[*]}; ++i)); do
        [ "${PACKAGES[$i]}" == "${expected_packages[$i]}" ]
    done
}

@test "[ubuntu-client] misc" {
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"

    for package in gparted libnss3 libgtk-3-0 libasound2t64 libgbm1; do
        run dpkg -s "${package}"
        [ "${status}" -eq 0 ]
    done
}
