#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/macos/common/docker.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

@test "[macos] docker validates the cask without installing it on a GitHub Actions runner" {
    function brew() {
        printf '%s\n' "$*" > "${BATS_TEST_TMPDIR}/brew-args"
    }

    GITHUB_ACTIONS=true RUNNER_TEMP="${BATS_TEST_TMPDIR}" install_docker

    run cat "${BATS_TEST_TMPDIR}/brew-args"
    [ "${output}" = "info --cask docker" ]
}

@test "[macos] docker installs the cask off the runner, an agent shell's CI=true included" {
    function brew() {
        printf '%s\n' "$*" > "${BATS_TEST_TMPDIR}/brew-args"
    }

    local runner_env

    for runner_env in "CI=true" "CI=true GITHUB_ACTIONS=true" "GITHUB_ACTIONS=false RUNNER_TEMP=${BATS_TEST_TMPDIR}"; do
        rm -f "${BATS_TEST_TMPDIR}/brew-args"
        # shellcheck disable=SC2086 # One VAR=value word per assignment.
        (
            unset GITHUB_ACTIONS RUNNER_TEMP
            export ${runner_env}
            install_docker
        )

        run cat "${BATS_TEST_TMPDIR}/brew-args"
        [ "${output}" = "install --cask docker" ]
    done
}
