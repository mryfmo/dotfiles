#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/server/starship.sh"

function setup() {
    ORIGINAL_HOME="${HOME}"
    TEST_HOME="$(mktemp -d)"
    HOME="${TEST_HOME}"
    export HOME
    source "${SCRIPT_PATH}"
}

function teardown() {
    run uninstall_starship
    rm -rf -- "${TEST_HOME}"
    HOME="${ORIGINAL_HOME}"
    export HOME

    # reset PATH
    PATH=$(getconf PATH)
    export PATH
}

@test "[ubuntu-server] starship" {
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"

    export PATH="${PATH}:${HOME%/}/.local/bin"
    [ -x "$(command -v starship)" ]
}

@test "[ubuntu-server] uninstall_starship preserves sibling binaries" {
    mkdir -p "${HOME}/.local/bin"
    touch "${HOME}/.local/bin/starship" "${HOME}/.local/bin/must-survive"

    run uninstall_starship

    [ "${status}" -eq 0 ]
    [ ! -e "${HOME}/.local/bin/starship" ]
    [ -e "${HOME}/.local/bin/must-survive" ]
    [ -d "${HOME}/.local/bin" ]
}
