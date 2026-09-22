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
    [ $num_packages -eq 9 ]

    expected_packages=(
        gparted
        language-pack-ja
        fonts-noto-cjk
        fonts-noto-color-emoji
        ibus-mozc
        libnss3
        libgtk-3-0t64
        libasound2t64
        libgbm1
    )
    for ((i = 0; i < ${#expected_packages[*]}; ++i)); do
        [ "${PACKAGES[$i]}" == "${expected_packages[$i]}" ]
    done
}

@test "[ubuntu-client] misc" {
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"

    for package in gparted language-pack-ja fonts-noto-cjk fonts-noto-color-emoji ibus-mozc libnss3 libgtk-3-0t64 libasound2t64 libgbm1; do
        run dpkg -s "${package}"
        [ "${status}" -eq 0 ]
    done

    if command -v snap > /dev/null 2>&1; then
        run snap list chromium
        [ "${status}" -eq 0 ]
    fi
}

@test "[ubuntu-client] install_chromium is a no-op when snap is unavailable" {
    run env PATH="${BATS_TEST_TMPDIR}" /bin/bash -c '
        source "'"${SCRIPT_PATH}"'"
        install_chromium
    '
    [ "${status}" -eq 0 ]
}
