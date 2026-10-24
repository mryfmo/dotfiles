#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/ghostty.sh"

load "../../helpers/apt_record"

function setup() {
    source "${SCRIPT_PATH}"
}

# Only a case that installed for real removes what it installed (U41): before, every case ran
# the installer's uninstall function (removed in U46), and the array cases' teardown removed the runner image's own packages.
function teardown() {
    remove_real_packages
}

@test "[ubuntu-client] PACKAGES for ghostty" {
    num_packages="${#PACKAGES[@]}"
    [ $num_packages -eq 1 ]

    expected_packages=(
        ghostty
    )
    for ((i = 0; i < ${#expected_packages[*]}; ++i)); do
        [ "${PACKAGES[$i]}" == "${expected_packages[$i]}" ]
    done
}

@test "[ubuntu-client] DEPENDENCY_PACKAGES for ghostty" {
    num_packages="${#DEPENDENCY_PACKAGES[@]}"
    [ $num_packages -eq 1 ]

    expected_packages=(
        software-properties-common
    )
    for ((i = 0; i < ${#expected_packages[*]}; ++i)); do
        [ "${DEPENDENCY_PACKAGES[$i]}" == "${expected_packages[$i]}" ]
    done
}

@test "[ubuntu-client] ghostty" {
    install_real_packages "${PACKAGES[@]}"

    run dpkg -s ghostty
    [ "${status}" -eq 0 ]
}
