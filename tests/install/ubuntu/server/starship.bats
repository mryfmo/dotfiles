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

@test "[ubuntu-server] failed checksum preserves Starship and sibling binary" {
    local archive="${BATS_TEST_TMPDIR}/starship.tar.gz"
    local fixture="${BATS_TEST_TMPDIR}/fixture"
    mkdir -p "${BIN_DIR}"
    mkdir -p "${fixture}"
    printf 'old-starship\n' > "${BIN_DIR}/starship"
    printf 'sibling\n' > "${BIN_DIR}/must-survive"
    printf '#!/bin/sh\ntouch should-not-run\n' > "${fixture}/starship"
    tar -czf "${archive}" -C "${fixture}" starship
    function curl() {
        local output url
        url="$1"
        shift
        while [ "$#" -gt 0 ]; do
            if [ "$1" = "-o" ]; then
                output="$2"
                break
            fi
            shift
        done
        if [ -n "${output:-}" ]; then
            cp "${archive}" "${output}"
        else
            printf 'incorrect-checksum\n'
        fi
    }

    run install_starship

    [ "${status}" -ne 0 ]
    grep -qx old-starship "${BIN_DIR}/starship"
    grep -qx sibling "${BIN_DIR}/must-survive"
}
