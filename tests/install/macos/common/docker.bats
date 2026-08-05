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

@test "[macos] docker installs the cask unless CI is exactly true" {
    function brew() {
        printf '%s\n' "$*" > "${BATS_TEST_TMPDIR}/brew-args"
    }

    local ci_value

    for ci_value in false yes no 1 0; do
        CI="${ci_value}" install_docker

        run cat "${BATS_TEST_TMPDIR}/brew-args"
        [ "${output}" = "install --cask docker" ]
    done
}
