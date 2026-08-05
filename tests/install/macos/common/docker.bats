#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/macos/common/docker.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

@test "[macos] docker validates the cask without installing it in CI" {
    function brew() {
        printf '%s\n' "$*" > "${BATS_TEST_TMPDIR}/brew-args"
    }

    CI=true install_docker

    run cat "${BATS_TEST_TMPDIR}/brew-args"
    [ "${output}" = "info --cask docker" ]
}

@test "[macos] docker installs the cask outside CI" {
    function brew() {
        printf '%s\n' "$*" > "${BATS_TEST_TMPDIR}/brew-args"
    }

    CI=false install_docker

    run cat "${BATS_TEST_TMPDIR}/brew-args"
    [ "${output}" = "install --cask docker" ]
}
