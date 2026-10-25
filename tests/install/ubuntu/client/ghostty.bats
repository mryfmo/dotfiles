#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/ghostty.sh"
readonly RETRY="the next make update retries"
readonly SKIPPED="ghostty not installed: its PPA is unreachable: "

# Fakes for sudo, curl, dpkg-query, add-apt-repository and apt-get that answer with exit codes and recorded argv only.
# PROBE picks curl's answer for every URL, as its `%{http_connect} %{http_code}` write-out and exit status: dns (exit 6),
# timeout (exit 28), http503, proxy503 (the proxy's CONNECT answered 503, exit 56), proxy407 (the proxy refused the
# credentials, exit 56), or local (exit 2, a usage error, not evidence of the network); an api- prefix applies it to the
# Launchpad API URL only. Default: HTTP 200. A ${HOME}/.curlrc with `fail` makes an HTTP 4xx/5xx exit 22, unless
# curl's first argument is -q, as with the real curl.
# FAIL picks the failing step once the probe answered: ppa-add (registration), ppa-permission (registration cannot
# write the source), lock (apt-get update cannot take its lock), index (apt-get update cannot fetch the PPA index),
# resolve or download (the ghostty install), or archive
# (the dependency install). SPC and STATUS are the dpkg status of software-properties-common (default installed;
# empty is absent) and of ghostty (default absent). Every curl, add-apt-repository and apt-get call is logged, an
# install that completes is logged as installed, and the ERR trap logs ERR when it fires in the script's own shell
# (a fake that returns non-zero inside a command substitution is not a script failure).
readonly APT_FAKES='
    source "'"${SCRIPT_PATH}"'"
    export APT_SOURCES_DIR="${HOME}/sources"
    mkdir -p "${APT_SOURCES_DIR}"
    trap "[ \${BASH_SUBSHELL} -gt 0 ] || echo ERR >> \"${HOME}/calls.log\"" ERR
    sudo() { shift; "$@"; }
    dpkg-query() { local s="${STATUS-}"; [ "$4" = ghostty ] || s="${SPC-installed}"; printf "%s" "${s}"; [ -n "${s}" ]; }
    curl() {
        local url="${*: -1}" mode="${PROBE-}" code=200
        printf "curl %s\n" "${url}" >> "${HOME}/calls.log"
        if [[ ${mode} == api-* ]]; then
            mode="${mode#api-}"
            [[ ${url} == https://api.launchpad.net/* ]] || mode=
        fi
        case "${mode}" in
            dns) echo "curl: (6) Could not resolve host" >&2; printf "000 000"; return 6 ;;
            timeout) echo "curl: (28) Connection timed out" >&2; printf "000 000"; return 28 ;;
            proxy503) echo "curl: (56) CONNECT tunnel failed, response 503" >&2; printf "503 000"; return 56 ;;
            proxy407) echo "curl: (56) CONNECT tunnel failed, response 407" >&2; printf "407 000"; return 56 ;;
            local) echo "curl: (2) option unknown" >&2; return 2 ;;
            http503) code=503 ;;
        esac
        if [ "$1" != -q ] && grep -qx fail "${HOME}/.curlrc" 2> /dev/null && [ "${code}" -ge 400 ]; then
            echo "curl: (22) The requested URL returned error: ${code}" >&2
            printf "000 %s" "${code}"
            return 22
        fi
        printf "000 %s" "${code}"
    }
    add-apt-repository() {
        printf "add-apt-repository %s\n" "$*" >> "${HOME}/calls.log"
        case "${FAIL-}" in
            ppa-add) return 1 ;;
            ppa-permission) echo "PermissionError: [Errno 13] Permission denied" >&2; return 1 ;;
        esac
        printf "URIs: https://ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/ubuntu/\n" > "${APT_SOURCES_DIR}/ghostty.sources"
    }
    apt-get() {
        printf "apt-get %s\n" "$*" >> "${HOME}/calls.log"
        case "${FAIL-}:$*" in
            lock:update) echo "E: Could not get lock /var/lib/apt/lists/lock" >&2; return 100 ;;
            index:update) echo "E: Failed to fetch https://ppa.launchpadcontent.net/.../InRelease  503  Service Unavailable" >&2; return 100 ;;
            resolve:"install -y ghostty") echo "E: Unable to correct problems, you have held broken packages." >&2; return 100 ;;
            download:"install -y ghostty") echo "E: Failed to fetch ghostty.deb" >&2; return 100 ;;
            archive:*software-properties-common) return 100 ;;
            *:"install "*) printf "installed %s\n" "${*: -1}" >> "${HOME}/calls.log" ;;
        esac
    }
'

load "../../helpers/apt_record"

function setup() {
    source "${SCRIPT_PATH}"
}

# Only a case that installed for real removes what it installed (U41): before, every case ran
# the installer's uninstall function (removed in U46), and the array cases' teardown removed the runner image's own packages.
function teardown() {
    remove_real_packages
}

# @description Run main under the fakes with a fresh HOME.
# @arg $1 string The directory name under BATS_TEST_TMPDIR.
# @arg $@ string Environment assignments for the fakes (PROBE, FAIL, SPC, STATUS).
function run_fakes() {
    local home="${BATS_TEST_TMPDIR}/$1"
    shift
    mkdir -p "${home}"
    run env HOME="${home}" "$@" bash -c "${APT_FAKES}"'
        main
    '
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
    # The installer's own outcome is the oracle: its retry line means the probe found the PPA unreachable.
    # Not under `run`: its subshell would drop REAL_PACKAGES_NEW, and the teardown would leave ghostty installed.
    local installer_status=0 installer absent=0
    install_real_packages "${PACKAGES[@]}" > "${BATS_TEST_TMPDIR}/installer.log" 2>&1 || installer_status=$?
    installer="$(cat "${BATS_TEST_TMPDIR}/installer.log")"
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
    [ "${installer_status}" -eq 0 ]
    run dpkg -s ghostty
    if [ "${absent}" -eq 1 ]; then [ "${status}" -ne 0 ]; else [ "${status}" -eq 0 ]; fi
}

@test "[ubuntu-client] the dependency phase runs only when software-properties-common is absent" {
    run_fakes absent SPC=
    [ "${status}" -eq 0 ]
    [ "$(grep '^apt-get' "${BATS_TEST_TMPDIR}/absent/calls.log" | sed -n 1,2p)" = $'apt-get update\napt-get install -y software-properties-common' ]
    run_fakes present
    [ "${status}" -eq 0 ]
    [ -z "$(sed '/^add-apt-repository/,$d' "${BATS_TEST_TMPDIR}/present/calls.log" | grep '^apt-get')" ]
}

@test "[ubuntu-client] an installed ghostty is left as it is" {
    run_fakes home STATUS=installed
    [ "${status}" -eq 0 ]
    [ ! -e "${BATS_TEST_TMPDIR}/home/calls.log" ]
}

@test "[ubuntu-client] a half-configured ghostty is installed, not skipped" {
    run_fakes home STATUS=half-configured
    [ "${status}" -eq 0 ]
    grep -qx 'installed ghostty' "${BATS_TEST_TMPDIR}/home/calls.log"
}

@test "[ubuntu-client] a reachable PPA probes the archive and the API, then registers and installs" {
    run_fakes home
    [ "${status}" -eq 0 ]
    [ "$(grep '^curl' "${BATS_TEST_TMPDIR}/home/calls.log")" = $'curl https://ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/ubuntu/\ncurl https://api.launchpad.net/devel/~mkasberg/+archive/ubuntu/ghostty-ubuntu' ]
    grep -qx 'add-apt-repository -y -n ppa:mkasberg/ghostty-ubuntu' "${BATS_TEST_TMPDIR}/home/calls.log"
    [ "$(tail -n 2 "${BATS_TEST_TMPDIR}/home/calls.log")" = $'apt-get install -y ghostty\ninstalled ghostty' ]
    ! grep -qx ERR "${BATS_TEST_TMPDIR}/home/calls.log"
}

@test "[ubuntu-client] an existing PPA source is not re-added and the API is not probed" {
    mkdir -p "${BATS_TEST_TMPDIR}/home/sources"
    echo "deb https://ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/ubuntu noble main" > "${BATS_TEST_TMPDIR}/home/sources/ghostty.list"
    run_fakes home PROBE=api-dns
    [ "${status}" -eq 0 ]
    grep -qx 'installed ghostty' "${BATS_TEST_TMPDIR}/home/calls.log"
    ! grep -q -e add-apt-repository -e api.launchpad.net "${BATS_TEST_TMPDIR}/home/calls.log"
}

@test "[ubuntu-client] an unreachable PPA skips Ghostty before any apt call" {
    local probe
    for probe in dns timeout http503 proxy503 api-dns; do
        run_fakes "${probe}" PROBE="${probe}"
        [ "${status}" -eq 0 ]
        [[ "${output}" == *"${SKIPPED}"*"${RETRY}"* ]]
        run ! grep -q -e '^apt-get' -e '^add-apt-repository' -e '^ERR' "${BATS_TEST_TMPDIR}/${probe}/calls.log"
    done
}

@test "[ubuntu-client] a curlrc with fail does not turn an HTTP 503 probe into a fatal exit" {
    mkdir -p "${BATS_TEST_TMPDIR}/home"
    echo fail > "${BATS_TEST_TMPDIR}/home/.curlrc"
    run_fakes home PROBE=http503
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"${SKIPPED}"*"(HTTP 503)"*"${RETRY}"* ]]
}

@test "[ubuntu-client] a probe that fails locally (a curl usage error or a proxy CONNECT 407) is fatal, not a skip" {
    local probe
    for probe in local proxy407; do
        run_fakes "${probe}" PROBE="${probe}"
        [ "${status}" -ne 0 ]
        [[ "${output}" != *"${RETRY}"* ]]
        grep -qx ERR "${BATS_TEST_TMPDIR}/${probe}/calls.log"
        run ! grep -q -e '^apt-get' -e '^add-apt-repository' "${BATS_TEST_TMPDIR}/${probe}/calls.log"
    done
}

@test "[ubuntu-client] once the PPA answers the probe, every later failure is fatal, a failed index or package fetch included (by design)" {
    local fail spc
    for fail in ppa-add ppa-permission lock index resolve download archive; do
        spc=installed
        [ "${fail}" != archive ] || spc=
        run_fakes "${fail}" FAIL="${fail}" SPC="${spc}"
        [ "${status}" -ne 0 ]
        [[ "${output}" != *"${RETRY}"* ]]
        grep -qx ERR "${BATS_TEST_TMPDIR}/${fail}/calls.log"
        run ! grep -qx 'installed ghostty' "${BATS_TEST_TMPDIR}/${fail}/calls.log"
    done
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
