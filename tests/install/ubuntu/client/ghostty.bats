#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/ghostty.sh"
readonly RETRY_LINE="ghostty not installed: ppa:mkasberg/ghostty-ubuntu is unreachable; the next make update retries"

# Fakes for sudo and apt: FAIL picks the PPA step that answers 503 as apt does (update or pool), or a non-PPA
# failure (archive); every apt call is logged, and an install that succeeds is logged as installed.
readonly APT_FAKES='
    source "'"${SCRIPT_PATH}"'"
    sudo() { shift; "$@"; }
    add-apt-repository() { printf "add-apt-repository %s\n" "$*" >> "${HOME}/calls.log"; touch "${HOME}/ppa-added"; }
    apt-get() {
        printf "apt-get %s\n" "$*" >> "${HOME}/calls.log"
        local ppa=https://ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/ubuntu
        case "${FAIL:-}:$1 ${3-}" in
            update:"update "*) [ ! -e "${HOME}/ppa-added" ] || { printf "E: Failed to fetch %s/dists/noble/InRelease  503  Service Unavailable [IP: 185.125.190.80 443]\n" "${ppa}"; return 100; } ;;
            pool:"install ghostty") printf "E: Failed to fetch %s/pool/main/g/ghostty/ghostty_1.2.0_amd64.deb  503  Service Unavailable [IP: 185.125.190.80 443]\n" "${ppa}"; return 100 ;;
            archive:"install software-properties-common") printf "E: Failed to fetch http://archive.ubuntu.com/ubuntu/pool/main/s/x.deb  503  Service Unavailable\n"; return 100 ;;
            *:"install "*) printf "installed %s\n" "$3" >> "${HOME}/calls.log" ;;
        esac
    }
'

function setup() {
    source "${SCRIPT_PATH}"
}

function teardown() {
    run uninstall_ghostty
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
    # The installer's own outcome is the oracle: its retry line means the PPA was unreachable at some step.
    run env DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    if [[ "${output}" == *"${RETRY_LINE}"* ]]; then
        echo "# branch: the PPA was unreachable; ghostty must be absent" >&3
        run dpkg -s ghostty
        [ "${status}" -ne 0 ]
    else
        echo "# branch: the PPA answered; ghostty must be installed" >&3
        run dpkg -s ghostty
        [ "${status}" -eq 0 ]
    fi
}

@test "[ubuntu-client] an unreachable PPA never fails the apply" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=update bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"${RETRY_LINE}"* ]]
    grep -q 'installed software-properties-common' "${BATS_TEST_TMPDIR}/calls.log"
    ! grep -q 'installed ghostty' "${BATS_TEST_TMPDIR}/calls.log"
}

@test "[ubuntu-client] a failed PPA package download never fails the apply" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=pool bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"${RETRY_LINE}"* ]]
    ! grep -q 'installed ghostty' "${BATS_TEST_TMPDIR}/calls.log"
}

@test "[ubuntu-client] a non-PPA apt failure still fails the apply" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=archive bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -ne 0 ]
    [[ "${output}" != *"${RETRY_LINE}"* ]]
}
