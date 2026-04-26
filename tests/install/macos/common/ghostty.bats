#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/macos/common/ghostty.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

function teardown() {
    run uninstall_ghostty
}

@test "[macos] ghostty" {
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"

    [ -e "/Applications/Ghostty.app" ]
}
