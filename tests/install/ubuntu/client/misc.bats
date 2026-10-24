#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/misc.sh"

load "../../helpers/apt_record"

function setup() {
    source "${SCRIPT_PATH}"
}

# Only a case that installed for real removes what it installed (U41): before, every case ran
# the installer's uninstall function (removed in U46), and the array cases' teardown removed the runner image's own packages.
function teardown() {
    remove_real_packages
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
    install_real_packages "${PACKAGES[@]}"

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

@test "[ubuntu-client] install_misc asks apt-get for every package in PACKAGES at once" {
    run record_apt_calls "${SCRIPT_PATH}" install_misc
    [ "${status}" -eq 0 ]
    [ "$(grep -c '^apt-get install ' <<< "${output}")" -eq 1 ]
    grep -qxF "apt-get install -y ${PACKAGES[*]}" <<< "${output}"
}

@test "[ubuntu-client] the recorded install_misc call catches an installer that drops a package" {
    local mutant="${BATS_TEST_TMPDIR}/misc.sh" calls
    sed 's/apt-get install -y "${PACKAGES\[@\]}"/apt-get install -y "${PACKAGES[@]:1}"/' "${SCRIPT_PATH}" > "${mutant}"
    if cmp -s "${SCRIPT_PATH}" "${mutant}"; then
        false
    fi
    run record_apt_calls "${mutant}" install_misc
    [ "${status}" -eq 0 ]
    calls="${output}"
    # The recorder saw the mutant's call, and the check above would refuse it.
    grep -qxF "apt-get install -y ${PACKAGES[*]:1}" <<< "${calls}"
    if grep -qxF "apt-get install -y ${PACKAGES[*]}" <<< "${calls}"; then
        false
    fi
}
