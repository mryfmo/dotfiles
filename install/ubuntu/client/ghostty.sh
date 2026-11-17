#!/usr/bin/env bash

# @file install/ubuntu/client/ghostty.sh
# @brief Install Ghostty on Ubuntu client machines.
# @description
#   Adds the community-maintained Ghostty Ubuntu PPA recommended by
#   mkasberg/ghostty-ubuntu and installs the `ghostty` package through apt.
#   When a Launchpad host the remaining steps need gives no answer, Ghostty is
#   skipped with a retry line before any apt call. The network evidence is the
#   probe and apt's own report of the PPA: a 5xx that apt's output attributes
#   to the PPA's URL (a failed index or package fetch, such as a 503 between
#   the probe and apt) is the same outage one step later and is skipped with
#   the same retry line. Every other failure after the probe is fatal, so a
#   local, permission, lock or resolution fault is never masked as an outage,
#   and the next make update retries.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly GHOSTTY_PPA="ppa:mkasberg/ghostty-ubuntu"
# The URIs host and path of the PPA's apt source stanza.
readonly GHOSTTY_PPA_URL="ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/"
# Probed before any PPA step: the archive serves the index and the package, and
# add-apt-repository reads the PPA's record and signing key from the Launchpad API.
readonly GHOSTTY_ARCHIVE_PROBE="https://${GHOSTTY_PPA_URL}ubuntu/"
readonly GHOSTTY_API_PROBE="https://api.launchpad.net/devel/~mkasberg/+archive/ubuntu/ghostty-ubuntu"
readonly PACKAGES=(
    ghostty
)
readonly DEPENDENCY_PACKAGES=(
    software-properties-common
)

#
# @description Succeed when dpkg's database records a package as fully installed.
# @arg $1 string The package name.
# @exitcode 0 The package's status is installed.
# @exitcode 1 Any other status (half-configured, config-files, ...) or no record.
#
function installed() {
    local status
    # shellcheck disable=SC2016
    status="$(dpkg-query -W -f '${db:Status-Status}' "$1" 2> /dev/null)" || return 1
    [ "${status}" = installed ]
}

#
# @description Install packages required before adding the Ghostty PPA, only when they are missing,
#   so an existing machine refreshes the apt index once, after the PPA is registered.
#
function install_ghostty_dependencies() {
    installed software-properties-common && return 0
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get update
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install -y "${DEPENDENCY_PACKAGES[@]}"
}

#
# @description Print the apt source file that names the Ghostty PPA.
# @stdout The first .sources or .list file under APT_SOURCES_DIR (default /etc/apt/sources.list.d)
#   naming GHOSTTY_PPA_URL, or nothing when none does.
#
function ghostty_source_file() {
    local dir="${APT_SOURCES_DIR:-/etc/apt/sources.list.d}"
    grep -lsF "${GHOSTTY_PPA_URL}" "${dir}"/*.sources "${dir}"/*.list | head -n 1 || true
}

#
# @description Add the community-maintained Ghostty Ubuntu PPA without updating the package cache.
#
function add_ghostty_ppa() {
    sudo --preserve-env=http_proxy,https_proxy,no_proxy add-apt-repository -y -n "${GHOSTTY_PPA}"
}

#
# @description Print the first URL that gives no answer, so the PPA counts as unreachable.
# @arg $@ string The URLs to probe, in order.
# @stdout `<url> (<reason>)` for the first URL that fails to connect, resolve, finish TLS or
#   answer within the timeout (curl exit 5, 6, 7, 28, 35, 52 or 56), or answers HTTP 5xx;
#   nothing when every URL answers.
# @exitcode 0 Each URL answered or was found unreachable.
# @exitcode * A proxy that answered CONNECT with 4xx (such as 407, a local credential fault), or any
#   other curl failure (a local error, not evidence of the network): curl's status, unchanged.
#
function ghostty_unreachable_url() {
    local url out connect code status
    for url in "$@"; do
        status=0
        # -q must come first so no curlrc can change the options this decision relies on (e.g. `fail`).
        out="$(curl -q --silent --show-error --output /dev/null --write-out '%{http_connect} %{http_code}' \
            --connect-timeout 5 --max-time 15 "${url}")" || status=$?
        read -r connect code <<< "${out}" || true
        if [[ ${connect-} == 4?? ]]; then
            printf 'ghostty: the proxy answered CONNECT %s for %s\n' "${connect}" "${url}" >&2
            return "$((status == 0 ? 1 : status))"
        fi
        case "${status}" in
        0)
            if [[ ${code-} == 5?? ]]; then
                printf '%s (HTTP %s)\n' "${url}" "${code}"
                return 0
            fi
            ;;
        5 | 6 | 7 | 28 | 35 | 52 | 56)
            printf '%s (curl exit %s)\n' "${url}" "${status}"
            return 0
            ;;
        *) return "${status}" ;;
        esac
    done
}

#
# @description Print the 5xx code a line of apt's output attributes to the Ghostty PPA.
# @arg $1 string apt-get's output, stdout and stderr.
# @stdout The code of the first line naming GHOSTTY_PPA_URL with a 5xx code between blanks, as apt writes
#   `W: Failed to fetch https://ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/ubuntu/dists/noble/InRelease  503
#   Service Unavailable [IP: ...]` (an index, exit 0) or the same `E:` line for a .deb under pool/ (exit 100);
#   nothing when no line does. Another PPA on the same host is not this PPA's outage, so the host alone never matches.
# @exitcode 0 The output was read to its end: the code is printed, or nothing when no line qualifies.
# @exitcode * grep's status when it could not read the output (2, or 128 plus a signal): no judgement was made. The
#   output reaches grep over a pipe and grep says how its read ended (0 a line names the PPA, 1 none does, 2 a read
#   error); a `read` loop over a here-string returns 1 at the end of the input and on a read error alike, and bash
#   stages a here-string in a temporary file whose failure the loop never reports, so that form's failure was unseen.
#
function ghostty_ppa_outage_code() {
    local lines line code='[[:space:]](5[0-9][0-9])([[:space:]]|$)' status=0
    lines="$(printf '%s\n' "$1" | grep -F -- "${GHOSTTY_PPA_URL}")" || status=$?
    case "${status}" in
    0) ;;
    1) return 0 ;;
    *) return "${status}" ;;
    esac
    # The PPA's lines are walked by parameter expansion: no second read whose failure could go unseen.
    lines+=$'\n'
    while [ -n "${lines}" ]; do
        line="${lines%%$'\n'*}"
        lines="${lines#*$'\n'}"
        if [[ ${line} =~ ${code} ]]; then
            printf '%s\n' "${BASH_REMATCH[1]}"
            return 0
        fi
    done
    return 0
}

#
# @description Run one apt-get step under sudo with its output kept, and judge the output for the PPA's outage.
# @arg $@ string apt-get's arguments.
# @stderr apt-get's stdout and stderr, line by line as it writes them, so the operator keeps apt's lines. tee writes
#   to a file and copies to the inherited stderr: `tee /dev/stderr` would reopen a stderr that is a file and
#   truncate it. One line naming the step (and the file, for tee and cat) when the output could not be kept, read
#   or judged.
# @stdout The 5xx code of ghostty_ppa_outage_code over the step's output, or nothing.
# @exitcode 0 apt-get exited 0, or its output attributed a 5xx to the PPA (the code is printed, whatever apt's status).
# @exitcode 1 The output could not be kept (tee failed, whatever the file holds), read (cat failed) or judged
#   (ghostty_ppa_outage_code failed), so no judgement was made and neither apt's status nor the output is read as a
#   pass or as the outage (standing order 21). The file is removed after the message names it.
# @exitcode * apt-get's own status otherwise.
#
function ghostty_apt() {
    local log output code status
    local -a statuses=(0 0)
    log="$(mktemp)" || return 1
    # apt's status and tee's are read apart, from PIPESTATUS right after the pipeline: the pipeline's one status under
    # pipefail is the rightmost failure, so apt's 100 would hide a failed tee, and a failed tee would pass for apt's.
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get "$@" 2>&1 | tee "${log}" >&2 || statuses=("${PIPESTATUS[@]}")
    status="${statuses[0]}"
    if [ "${statuses[1]}" -ne 0 ]; then
        printf "ghostty: cannot keep apt-get %s's output in %s; the outage judgement needs it\n" "$*" "${log}" >&2
        rm -f "${log}"
        return 1
    fi
    if ! output="$(cat "${log}")"; then
        printf "ghostty: cannot read apt-get %s's output from %s\n" "$*" "${log}" >&2
        rm -f "${log}"
        return 1
    fi
    rm -f "${log}"
    code="$(ghostty_ppa_outage_code "${output}")" || {
        printf "ghostty: cannot judge apt-get %s's output for the PPA's outage: its reader exited %s\n" "$*" "$?" >&2
        return 1
    }
    if [ -n "${code}" ]; then
        printf '%s\n' "${code}"
        return 0
    fi
    return "${status}"
}

#
# @description Print the retry line for a 5xx the PPA answered to apt after it answered the probe.
# @arg $1 string The HTTP code.
#
function ghostty_skipped_after_probe() {
    printf 'ghostty not installed: its PPA answered %s after the probe; the next make update retries\n' "$1"
}

#
# @description Install Ghostty from apt, registering the PPA when no source names it.
# @exitcode 0 Ghostty is installed, or it was skipped: a Launchpad host it needs gave no answer to the probe, or the
#   PPA answered a 5xx to apt's index or package fetch after the probe.
# @exitcode 1 add-apt-repository succeeded but no apt source names the PPA; or an apt step's output could not be kept,
#   read or judged, so no outage judgement was made.
# @exitcode * Otherwise the status of the failed probe, dependency, registration, refresh or install command.
#
function install_ghostty() {
    local sources_file unreachable code status
    local -a probes=("${GHOSTTY_ARCHIVE_PROBE}")
    installed ghostty && return 0
    sources_file="$(ghostty_source_file)"
    [ -n "${sources_file}" ] || probes+=("${GHOSTTY_API_PROBE}")
    unreachable="$(ghostty_unreachable_url "${probes[@]}")"
    if [ -n "${unreachable}" ]; then
        printf 'ghostty not installed: its PPA is unreachable: %s; the next make update retries\n' "${unreachable}"
        return 0
    fi
    install_ghostty_dependencies
    if [ -z "${sources_file}" ]; then
        add_ghostty_ppa
        sources_file="$(ghostty_source_file)"
        if [ -z "${sources_file}" ]; then
            echo "ghostty: add-apt-repository succeeded but no apt source names ${GHOSTTY_PPA_URL}" >&2
            return 1
        fi
    fi
    # An index 5xx is a warning to apt (exit 0, old lists kept), so the output decides, not the status alone.
    status=0
    code="$(ghostty_apt update)" || status=$?
    if [ -n "${code}" ]; then
        ghostty_skipped_after_probe "${code}"
        return 0
    fi
    [ "${status}" -eq 0 ] || return "${status}"
    status=0
    code="$(ghostty_apt install -y "${PACKAGES[@]}")" || status=$?
    if [ -n "${code}" ]; then
        ghostty_skipped_after_probe "${code}"
        return 0
    fi
    return "${status}"
}

#
# @description Run the Ghostty installation flow.
#
function main() {
    install_ghostty
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
