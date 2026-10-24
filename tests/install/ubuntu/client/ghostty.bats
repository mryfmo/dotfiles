#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/ghostty.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

function teardown() {
    u41_mark teardown-start
    run uninstall_ghostty
    u41_teardown_summary
    u41_mark teardown-end
}

# U41 MEASUREMENT (temporary, removed before review): fd-3 markers GitHub timestamps.
function u41_mark() { printf '# U41 %s | %s\n' "$1" "${BATS_TEST_DESCRIPTION}" >&3; }
function u41_teardown_summary() {
    printf '# U41 teardown-status %s removed %s: %s | %s\n' "${status}" "$(grep -c '^Removing ' <<< "${output}")" \
        "$(grep '^Removing ' <<< "${output}" | awk '{print $2}' | tr '\n' ' ')" "${BATS_TEST_DESCRIPTION}" >&3
}
function u41_install() {
    local log="${BATS_TEST_TMPDIR}/u41-install.log"
    u41_mark body-install-start
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}" > "${log}" 2>&1 || { sed 's/^/# /' "${log}" >&3; return 1; }
    u41_mark body-install-end
    grep -E '^(Need to get|Fetched|After this operation|[0-9]+ upgraded)' "${log}" | sed 's/^/# U41 apt: /' >&3 || true
}

@test "[ubuntu-client] PACKAGES for ghostty" {
    num_packages="${#PACKAGES[@]}"
    [ $num_packages -eq 1 ]

    expected_packages=(
        ghostty
    )
    for ((i = 0; i < ${#expected_packages[*]}; ++i)); do
        [ "${PACKAGES[$i]}" == "${expected_packages[$i]}" ]
    done
}

@test "[ubuntu-client] DEPENDENCY_PACKAGES for ghostty" {
    num_packages="${#DEPENDENCY_PACKAGES[@]}"
    [ $num_packages -eq 1 ]

    expected_packages=(
        software-properties-common
    )
    for ((i = 0; i < ${#expected_packages[*]}; ++i)); do
        [ "${DEPENDENCY_PACKAGES[$i]}" == "${expected_packages[$i]}" ]
    done
}

@test "[ubuntu-client] ghostty" {
    u41_install

    run dpkg -s ghostty
    [ "${status}" -eq 0 ]
}
