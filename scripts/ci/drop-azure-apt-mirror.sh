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
#   this before its first apt use (tests/unit/test_apt_mirror.py checks the order). A list that would be left with no
#   mirror is refused, so apt never runs against an empty list.
# @arg $1 path Optional: the mirror list. Default: /etc/apt/apt-mirrors.txt.
# @stdout The list before and after.
# @exitcode 0 The Azure line is gone (or was never there), or the list is absent (not such a runner).
# @exitcode 1 A read or write failed, or no mirror would be left.
# @example
#   scripts/ci/drop-azure-apt-mirror.sh
set -euo pipefail

mirrors=${1:-/etc/apt/apt-mirrors.txt}

if [[ ! -e ${mirrors} ]]; then
    printf '%s is absent; no apt mirror list to change\n' "${mirrors}"
    exit 0
fi
if ! before="$(cat -- "${mirrors}")"; then
    printf 'drop-azure-apt-mirror: cannot read %s\n' "${mirrors}" >&2
    exit 1
fi
printf '%s before:\n%s\n' "${mirrors}" "${before}"

# awk prints the kept lines and fails only when it cannot run; grep -v would also exit 1 when no line is kept.
if ! after="$(awk '!/azure\.archive\.ubuntu\.com/' <<< "${before}")"; then
    printf 'drop-azure-apt-mirror: awk could not filter %s\n' "${mirrors}" >&2
    exit 1
fi
if [[ ${after} == "${before}" ]]; then
    printf 'no azure.archive.ubuntu.com entry in %s; nothing to change\n' "${mirrors}"
    exit 0
fi
if ! grep -q 'priority:' <<< "${after}"; then
    printf 'drop-azure-apt-mirror: no apt mirror would be left in %s; it is unchanged\n' "${mirrors}" >&2
    exit 1
fi

# The runner's list is root's; a list this user may write (the tests' copy) is written without sudo.
if [[ -w ${mirrors} ]]; then
    writer=(tee -- "${mirrors}")
else
    writer=(sudo -n tee -- "${mirrors}")
fi
if ! printf '%s\n' "${after}" | "${writer[@]}" > /dev/null; then
    printf 'drop-azure-apt-mirror: could not write %s\n' "${mirrors}" >&2
    exit 1
fi
printf '%s after:\n%s\n' "${mirrors}" "${after}"
