#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/ghostty.sh"
readonly RETRY="the next make update retries"

# Fakes for sudo, dpkg-query, add-apt-repository and apt-get that answer with exit codes and recorded argv only.
# FAIL picks the failing step: ppa-add (the registration), ppa-update (the PPA-only refresh), download
# (--download-only), install (--no-download) or archive (the dependency install). SPC and STATUS are the dpkg
# status of software-properties-common (default installed; empty is absent) and of ghostty (default absent).
# Every add-apt-repository and apt-get call is logged, and an install that completes is logged as installed.
readonly APT_FAKES='
    source "'"${SCRIPT_PATH}"'"
    export APT_SOURCES_DIR="${HOME}/sources"
    mkdir -p "${APT_SOURCES_DIR}"
    sudo() { shift; "$@"; }
    dpkg-query() { local s="${STATUS-}"; [ "$4" = ghostty ] || s="${SPC-installed}"; printf "%s" "${s}"; [ -n "${s}" ]; }
    add-apt-repository() {
        printf "add-apt-repository %s\n" "$*" >> "${HOME}/calls.log"
        [ "${FAIL-}" != ppa-add ] || return 1
        printf "URIs: https://ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/ubuntu/\n" > "${APT_SOURCES_DIR}/ghostty.sources"
    }
    apt-get() {
        printf "apt-get %s\n" "$*" >> "${HOME}/calls.log"
        case "${FAIL-}:$*" in
            ppa-update:"update -o Dir::Etc::sourcelist="* | download:*--download-only* | install:*--no-download* | archive:*software-properties-common) return 100 ;;
            *:"install -y --download-only "*) ;;
            *:"install "*) printf "installed %s\n" "${*: -1}" >> "${HOME}/calls.log" ;;
        esac
    }
'

function setup() {
    source "${SCRIPT_PATH}"
}

function teardown() {
    run uninstall_ghostty
}

function retry_line() {
    printf "ghostty not installed: %s (apt's output above); %s" "$1" "${RETRY}"
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
    # The installer's own outcome is the oracle: its retry line means a stage that fetches from the PPA failed.
    run env DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    local installer="${output}" absent=0
    if [[ "${installer}" == *"ghostty not installed: "*"${RETRY}"* ]]; then
        echo "# branch: the PPA was unreachable; ghostty must be absent" >&3
        absent=1
    else
        echo "# branch: the PPA answered; ghostty must be installed" >&3
    fi
    {
        printf '%s\n' "${installer}"
        ls /etc/apt/sources.list.d || true
        apt-config dump | grep -i retries || true
        dpkg -s ghostty | grep '^Status:' || true
    } | sed 's/^/# /' >&3
    run dpkg -s ghostty
    if [ "${absent}" -eq 1 ]; then [ "${status}" -ne 0 ]; else [ "${status}" -eq 0 ]; fi
}

@test "[ubuntu-client] the dependency phase runs only when software-properties-common is absent" {
    mkdir -p "${BATS_TEST_TMPDIR}/absent"
    run env HOME="${BATS_TEST_TMPDIR}/absent" SPC= bash -c "${APT_FAKES}"'
        main
    '
    [ "$(sed -n 1,2p "${BATS_TEST_TMPDIR}/absent/calls.log")" = $'apt-get update\napt-get install -y software-properties-common' ]
    run env HOME="${BATS_TEST_TMPDIR}" bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    ! sed '/Dir::Etc::sourcelist=/,$d' "${BATS_TEST_TMPDIR}/calls.log" | grep -qx 'apt-get update'
}

@test "[ubuntu-client] an installed ghostty is left as it is" {
    run env HOME="${BATS_TEST_TMPDIR}" STATUS=installed bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [ ! -e "${BATS_TEST_TMPDIR}/calls.log" ]
}

@test "[ubuntu-client] a half-configured ghostty is installed, not skipped" {
    run env HOME="${BATS_TEST_TMPDIR}" STATUS=half-configured bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    grep -q 'installed ghostty' "${BATS_TEST_TMPDIR}/calls.log"
}

@test "[ubuntu-client] a failed PPA registration never fails the apply" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=ppa-add SPC= bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"$(retry_line "its PPA could not be registered")"* ]]
    [ "$(grep '^apt-get' "${BATS_TEST_TMPDIR}/calls.log")" = $'apt-get update\napt-get install -y software-properties-common' ]
}

@test "[ubuntu-client] an existing PPA source is not re-added" {
    mkdir -p "${BATS_TEST_TMPDIR}/sources"
    echo "deb https://ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/ubuntu noble main" > "${BATS_TEST_TMPDIR}/sources/ghostty.list"
    run env HOME="${BATS_TEST_TMPDIR}" bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    grep -q 'installed ghostty' "${BATS_TEST_TMPDIR}/calls.log"
    ! grep -q add-apt-repository "${BATS_TEST_TMPDIR}/calls.log"
}

@test "[ubuntu-client] an unreachable PPA never fails the apply" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=ppa-update bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"$(retry_line "its PPA index could not be refreshed")"* ]]
    # The PPA-only refresh is the last call, with its four options.
    [ "$(tail -n 1 "${BATS_TEST_TMPDIR}/calls.log")" = "apt-get update -o Dir::Etc::sourcelist=${BATS_TEST_TMPDIR}/sources/ghostty.sources -o Dir::Etc::sourceparts=- -o APT::Get::List-Cleanup=0 -o APT::Update::Error-Mode=any" ]
}

@test "[ubuntu-client] a failed PPA package download never fails the apply" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=download bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"$(retry_line "its package could not be downloaded")"* ]]
    ! grep -q -- --no-download "${BATS_TEST_TMPDIR}/calls.log"
}

@test "[ubuntu-client] a failed local install stays fatal" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=install bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 100 ]
    [[ "${output}" != *"${RETRY}"* ]]
}

@test "[ubuntu-client] a non-PPA apt failure still fails the apply" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=archive SPC= bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -ne 0 ]
    [[ "${output}" != *"${RETRY}"* ]]
}

@test "[ubuntu-client] the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it" {
    local template=./home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl
    [ -f "${template}" ]
    grep -qF '{{ if eq .chezmoi.os "linux" -}}' "${template}"
    grep -qF '{{   if eq .chezmoi.osRelease.idLike "debian" -}}' "${template}"
    grep -qF '{{     if eq .system "client" -}}' "${template}"
    grep -qF '{{       include "../install/ubuntu/client/ghostty.sh" }}' "${template}"
    ! grep -qF 'install/ubuntu/client/ghostty.sh' ./home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl
}
