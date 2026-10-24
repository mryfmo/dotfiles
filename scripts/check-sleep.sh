#!/usr/bin/env bash

# @file check-sleep.sh
# @brief Fail when this Mac may sleep: `pmset -g` must report `SleepDisabled 1`.
# @description
#   An orchestrator Mac that sleeps overnight stalls every seat, so `make doctor`
#   runs this check after the tools check. On macOS it reads `pmset -g` and
#   requires the `SleepDisabled` line to hold `1`; on any other OS it only says
#   the check is skipped. It runs nothing else and changes no setting: the
#   operator's `sudo pmset -a disablesleep 1` does that.
# @exitcode 0 SleepDisabled is 1, or the OS is not macOS.
# @exitcode 1 SleepDisabled is not 1, its line is missing, pmset -g failed, or uname -s failed.

set -Eeuo pipefail

if ! kernel="$(uname -s)"; then
    echo "sleep check: uname -s failed; cannot tell whether this host is macOS" >&2
    exit 1
fi
if [[ "${kernel}" != Darwin ]]; then
    echo "sleep check: skipped (not macOS)"
    exit 0
fi

if ! output="$(pmset -g 2>&1)"; then
    echo "sleep check: pmset -g failed: ${output}" >&2
    exit 1
fi

value="$(printf '%s\n' "${output}" | awk '$1 == "SleepDisabled" { print $2; exit }')"
if [[ -z ${value} ]]; then
    echo "sleep check: pmset -g reports no SleepDisabled line; run: sudo pmset -a disablesleep 1" >&2
    exit 1
fi
if [[ ${value} != 1 ]]; then
    echo "sleep check: SleepDisabled is ${value}; run: sudo pmset -a disablesleep 1" >&2
    exit 1
fi
echo "sleep check: SleepDisabled is 1"
