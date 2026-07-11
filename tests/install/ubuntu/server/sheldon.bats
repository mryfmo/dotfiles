#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/common/sheldon.sh"

function setup() {
    ORIGINAL_HOME="${HOME}"
    HOME="$(mktemp -d)"
    export HOME
    source "${SCRIPT_PATH}"
}

function teardown() {
    run uninstall_sheldon
    rm -rf -- "${HOME}"
    HOME="${ORIGINAL_HOME}"
    export HOME

    # reset PATH
    PATH=$(getconf PATH)
    export PATH
}

@test "[ubuntu-server] sheldon" {
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"

    export PATH="${PATH}:${HOME%/}/.local/bin"
    [ -x "$(command -v sheldon)" ]
}

@test "[ubuntu-server] failed locked cargo install leaves no Sheldon binary" {
    function cargo() {
        printf 'registry checksum mismatch\n' >&2
        return 1
    }

    run install_sheldon

    [ "${status}" -ne 0 ]
    [ ! -e "${BIN_DIR}/sheldon" ]
}
