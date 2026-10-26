#!/usr/bin/env bash
# @file drop-azure-apt-mirror.sh
# @brief Remove azure.archive.ubuntu.com from a GitHub-hosted Ubuntu runner's apt mirror list.
# @description
#   actions/runner-images#14823 (open since 2026-09-30, ubuntu-24.04 and ubuntu-26.04): the runner image lists
#   azure.archive.ubuntu.com first in /etc/apt/apt-mirrors.txt and sets `Acquire::http::Timeout "15"` and
#   `Acquire::Retries "1"` (runner-images#14594). That timeout fires only when no data arrives for 15 s, so a node that
#   keeps sending archives slowly (61.5 kB/s for 20 minutes in the issue's run) never trips it, and apt never moves on
#   to the next entry; apt has no minimum-throughput setting. The issue's workaround is this script's: delete the Azure
#   line, so apt fetches from the next mirror in the list (archive.ubuntu.com).
#   Every workflow job that runs apt on a Ubuntu runner, directly or through setup.sh and the install tests, calls
#   this before its first apt use (tests/unit/test_apt_mirror.py checks the order).
#   The list is read, filtered and counted with bash builtins only; the one external command is the write (`tee`, or
#   `sudo -n tee` for root's list), whose status is checked, and the list is read back and compared with what was
#   written. A list that would be left with no mirror is refused, so apt never runs against an empty list.
# @arg $1 path Optional: the mirror list. Default: /etc/apt/apt-mirrors.txt.
# @stdout The list before and after.
# @exitcode 0 The Azure line is gone (or was never there), or the list is absent (not such a runner).
# @exitcode 1 The list cannot be read, no mirror would be left, the write failed, or the list read back differs.
# @example
#   scripts/ci/drop-azure-apt-mirror.sh
set -euo pipefail

mirrors=${1:-/etc/apt/apt-mirrors.txt}

#
# @description Print the list's lines, each ending in a newline, with bash's read only.
# @arg $1 path The list.
# @stdout Its lines.
# @exitcode 1 The file could not be opened.
#
function read_list() {
    local line
    # The loop's body ends in a command that succeeds, so the loop fails only when the redirection does.
    { while IFS= read -r line || [[ -n ${line} ]]; do
        printf '%s\n' "${line}"
        line=""
    done; } < "$1"
}

if [[ ! -e ${mirrors} ]]; then
    printf '%s is absent; no apt mirror list to change\n' "${mirrors}"
    exit 0
fi
if ! before="$(read_list "${mirrors}")"; then
    printf 'drop-azure-apt-mirror: cannot read %s\n' "${mirrors}" >&2
    exit 1
fi
printf '%s before:\n%s\n' "${mirrors}" "${before}"

kept="" dropped=0 left=0
while IFS= read -r line || [[ -n ${line} ]]; do
    if [[ ${line} == *azure.archive.ubuntu.com* ]]; then
        dropped=$((dropped + 1))
    else
        kept+="${line}"$'\n'
        [[ ${line} != *priority:* ]] || left=$((left + 1))
    fi
    line=""
done <<< "${before}"

if ((dropped == 0)); then
    printf 'no azure.archive.ubuntu.com entry in %s; nothing to change\n' "${mirrors}"
    exit 0
fi
if ((left == 0)); then
    printf 'drop-azure-apt-mirror: no apt mirror would be left in %s; it is unchanged\n' "${mirrors}" >&2
    exit 1
fi

# The runner's list is root's; a list this user may write (the tests' copy) is written without sudo.
if [[ -w ${mirrors} ]]; then
    writer=(tee -- "${mirrors}")
else
    writer=(sudo -n tee -- "${mirrors}")
fi
if ! printf '%s' "${kept}" | "${writer[@]}" > /dev/null; then
    printf 'drop-azure-apt-mirror: could not write %s\n' "${mirrors}" >&2
    exit 1
fi
if ! after="$(read_list "${mirrors}")"; then
    printf 'drop-azure-apt-mirror: cannot read %s back after the write\n' "${mirrors}" >&2
    exit 1
fi
# Command substitution drops the trailing newlines of both sides alike.
if [[ ${after} != "$(printf '%s' "${kept}")" ]]; then
    printf 'drop-azure-apt-mirror: %s read back differs from what was written:\n%s\n' "${mirrors}" "${after}" >&2
    exit 1
fi
printf '%s after:\n%s\n' "${mirrors}" "${after}"
