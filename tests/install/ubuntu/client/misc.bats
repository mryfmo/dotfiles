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

@test "[ubuntu-client] install_misc refreshes the index before installing" {
    run bash -c 'source "'"${SCRIPT_PATH}"'"; sudo() { echo "$*" >> "'"${BATS_TEST_TMPDIR}"'/sudo.log"; }; install_misc'
    [ "${status}" -eq 0 ]
    [ "$(sed -n 1p "${BATS_TEST_TMPDIR}/sudo.log")" = "apt-get update" ]
    [[ "$(sed -n 2p "${BATS_TEST_TMPDIR}/sudo.log")" == "apt-get install -y "* ]]
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

# A fake snap first on PATH, since install_chromium runs it through `timeout`, which cannot call a shell
# function. It logs each call to SNAP_CALLS and then runs $1.
function fake_snap() {
    mkdir -p "${BATS_TEST_TMPDIR}/bin"
    {
        printf '#!/bin/bash\n'
        printf 'printf "snap %%s\\n" "$*" >> "${SNAP_CALLS}"\n'
        printf '%s\n' "$1"
    } > "${BATS_TEST_TMPDIR}/bin/snap"
    chmod +x "${BATS_TEST_TMPDIR}/bin/snap"
}

# Run install_chromium with sudo as a pass-through, the fake snap first on PATH and the given environment.
function run_install_chromium() {
    run env SNAP_CALLS="${BATS_TEST_TMPDIR}/snap_calls" PATH="${BATS_TEST_TMPDIR}/bin:${PATH}" "$@" /bin/bash -c '
        source "$1"
        sudo() {
            "$@"
        }
        install_chromium
    ' _ "${SCRIPT_PATH}"
}

@test "[ubuntu-client] install_chromium retries a failed snap install and succeeds on the third attempt" {
    fake_snap '[ "$(wc -l < "${SNAP_CALLS}")" -ge 3 ]'
    run_install_chromium SNAP_RETRY_DELAY=0
    [ "${status}" -eq 0 ]
    [ "$(grep -c '^snap install chromium$' "${BATS_TEST_TMPDIR}/snap_calls")" -eq 3 ]
}

@test "[ubuntu-client] install_chromium fails after three failed snap installs" {
    fake_snap 'exit 1'
    run_install_chromium SNAP_RETRY_DELAY=0
    [ "${status}" -ne 0 ]
    [ "$(grep -c '^snap install chromium$' "${BATS_TEST_TMPDIR}/snap_calls")" -eq 3 ]
}

@test "[ubuntu-client] install_chromium stops a stalled snap install at SNAP_INSTALL_TIMEOUT and names the step" {
    # The fake snap hangs like a snap client waiting on a stalled store download.
    fake_snap 'exec sleep 60'
    SECONDS=0
    run_install_chromium SNAP_RETRY_DELAY=0 SNAP_INSTALL_TIMEOUT=1
    [ "${status}" -eq 124 ]
    [ "${SECONDS}" -lt 30 ]
    [[ "${output}" == *"install_chromium: snap install chromium timed out after 1 s (SNAP_INSTALL_TIMEOUT)"* ]]
    # Not retried: snapd keeps the change running after its client stops.
    [ "$(grep -c '^snap install chromium$' "${BATS_TEST_TMPDIR}/snap_calls")" -eq 1 ]
}
