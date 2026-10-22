#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/ghostty.sh"
readonly RETRY_LINE="ghostty not installed: ppa:mkasberg/ghostty-ubuntu is unreachable; the next make update retries"

# Fakes for sudo, dpkg and apt: FAIL picks the PPA step that answers 503 as apt does (update or pool), an update
# that exits 0 with failed-index warnings (warn), a PPA failure beside another source's (mixed: the archive;
# otherppa: another PPA on the same host), a PPA warning beside a failing apt hook (hook), a pool failure with apt's
# summary lines (summary), a PPA failure that apt reports translated unless LC_ALL=C (locale), or a non-PPA failure
# (archive). STATUS is ghostty's dpkg status (installed, half-configured, ...): as with dpkg, `dpkg -s` succeeds for
# any status record, and dpkg-query prints the status and exits 1 for a never-installed package.
# Every apt call is logged, and an install that succeeds is logged as installed.
readonly APT_FAKES='
    source "'"${SCRIPT_PATH}"'"
    sudo() { shift; "$@"; }
    dpkg() { [ "$1" = -s ] && [ -n "${STATUS:-}" ]; }
    dpkg-query() { printf "%s" "${STATUS:-}"; [ -n "${STATUS:-}" ]; }
    add-apt-repository() { printf "add-apt-repository %s\n" "$*" >> "${HOME}/calls.log"; touch "${HOME}/ppa-added"; }
    apt-get() {
        printf "apt-get %s\n" "$*" >> "${HOME}/calls.log"
        local ppa=https://ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/ubuntu
        case "${FAIL:-}:$1 ${3-}" in
            update:"update "*) [ ! -e "${HOME}/ppa-added" ] || { printf "E: Failed to fetch %s/dists/noble/InRelease  503  Service Unavailable [IP: 185.125.190.80 443]\n" "${ppa}"; return 100; } ;;
            warn:"update "*) [ ! -e "${HOME}/ppa-added" ] || printf "W: Failed to fetch %s/dists/noble/InRelease  503  Service Unavailable [IP: 185.125.190.80 443]\nW: Some index files failed to download. They have been ignored, or old ones used instead.\n" "${ppa}" ;;
            hook:"update "*)
                [ -e "${HOME}/ppa-added" ] || return 0
                printf "W: Failed to fetch %s/dists/noble/InRelease  503  Service Unavailable\nE: Problem executing scripts APT::Update::Post-Invoke-Success 'false'\nE: Sub-process returned an error code\n" "${ppa}"
                return 100 ;;
            summary:"install ghostty")
                printf "Err:3 %s noble/main amd64 ghostty amd64 1.2.0\n  503  Service Unavailable\nE: Failed to fetch %s/pool/main/g/ghostty/ghostty_1.2.0_amd64.deb  503  Service Unavailable\nE: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?\n" "${ppa}" "${ppa}"
                return 100 ;;
            locale:"update "*)
                [ -e "${HOME}/ppa-added" ] || return 0
                printf "apt-get locale LC_ALL=%s LANG=%s\n" "${LC_ALL:-}" "${LANG:-}" >> "${HOME}/calls.log"
                local line="E: Failed to fetch %s/dists/noble/InRelease  503  Service Unavailable\n"
                [ "${LC_ALL:-}" = C ] || line="E: %s/dists/noble/InRelease の取得に失敗しました  503  Service Unavailable\n"
                printf "${line}" "${ppa}"
                return 100 ;;
            warn:"install ghostty") printf "E: Unable to locate package ghostty\n"; return 100 ;;
            mixed:"update "* | otherppa:"update "*)
                [ -e "${HOME}/ppa-added" ] || return 0
                local other=http://archive.ubuntu.com/ubuntu
                [ "${FAIL}" = mixed ] || other=https://ppa.launchpadcontent.net/someone/else/ubuntu
                printf "E: Failed to fetch %s/dists/noble/InRelease  503  Service Unavailable\n" "${ppa}" "${other}"
                return 100 ;;
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

@test "[ubuntu-client] an apt-get update that reports a failed PPA index without a non-zero exit is an outage" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=warn bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"${RETRY_LINE}"* ]]
    ! grep -q 'apt-get install -y ghostty' "${BATS_TEST_TMPDIR}/calls.log"
}

@test "[ubuntu-client] a fetch failure from another host stays fatal even when the PPA also failed" {
    for fail in mixed otherppa; do
        mkdir -p "${BATS_TEST_TMPDIR}/${fail}"
        run env HOME="${BATS_TEST_TMPDIR}/${fail}" FAIL="${fail}" bash -c "${APT_FAKES}"'
            main
        '
        [ "${status}" -eq 100 ]
        [[ "${output}" != *"${RETRY_LINE}"* ]]
    done
}

@test "[ubuntu-client] an installed ghostty is left as it is" {
    run env HOME="${BATS_TEST_TMPDIR}" STATUS=installed bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [ ! -e "${BATS_TEST_TMPDIR}/calls.log" ]
}

@test "[ubuntu-client] a non-fetch apt error after a PPA warning stays fatal" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=hook bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 100 ]
    [[ "${output}" != *"${RETRY_LINE}"* ]]
}

@test "[ubuntu-client] a half-configured ghostty is installed, not skipped" {
    run env HOME="${BATS_TEST_TMPDIR}" STATUS=half-configured bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    grep -q 'installed ghostty' "${BATS_TEST_TMPDIR}/calls.log"
}

@test "[ubuntu-client] apt's download-failure summary counts as a PPA outage" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=summary bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"${RETRY_LINE}"* ]]
    ! grep -q 'installed ghostty' "${BATS_TEST_TMPDIR}/calls.log"
}

@test "[ubuntu-client] apt diagnostics are classified under a stable locale" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=locale LANG=ja_JP.UTF-8 LC_ALL=ja_JP.UTF-8 bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"${RETRY_LINE}"* ]]
    grep -q 'apt-get locale LC_ALL=C LANG=C' "${BATS_TEST_TMPDIR}/calls.log"
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

@test "[ubuntu-client] a non-PPA apt failure still fails the apply" {
    run env HOME="${BATS_TEST_TMPDIR}" FAIL=archive bash -c "${APT_FAKES}"'
        main
    '
    [ "${status}" -ne 0 ]
    [[ "${output}" != *"${RETRY_LINE}"* ]]
}
