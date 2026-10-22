#!/usr/bin/env bash
# @file smoke.sh
# @brief Run tests/install/ubuntu/client/ghostty.bats's APT_FAKES in plain bash (not Bats) against one installer.
# @description
#   Evidence helper for validation.md: Bats is never run locally, so each fake mode is run once in plain bash and
#   its exit, apt calls and retry line are printed, one line per mode.
# @arg $1 string The installer to source, relative to the repository root.
# @exitcode 0 Always; each mode's own exit is printed.
set -u
installer=$1
fakes=$(sed -n "/^readonly APT_FAKES='\$/,/^'\$/p" tests/install/ubuntu/client/ghostty.bats | sed '1d;$d')
fakes=$(sed "s|\"'\"\${SCRIPT_PATH}\"'\"|${installer}|" <<< "${fakes}")
count() { if [ -e "$2" ]; then grep -c -- "$1" "$2" || true; else echo 0; fi; }
for mode in update pool archive none warn mixed otherppa hook summary locale status=installed status=half-configured; do
    home=$(mktemp -d "${TMPDIR:-/tmp}/ghostty-smoke.XXXXXX")
    case ${mode} in status=*) setting=STATUS=${mode#status=} ;; *) setting=FAIL=${mode} ;; esac
    out=$(env HOME="${home}" LANG=ja_JP.UTF-8 LC_ALL=ja_JP.UTF-8 "${setting}" bash -c "${fakes}
main" 2>&1)
    rc=$?
    printf '%s exit=%s install-attempted=%s installed=%s retry-line=%s\n' "${mode}" "${rc}" \
        "$(count 'apt-get install -y ghostty' "${home}/calls.log")" "$(count 'installed ghostty' "${home}/calls.log")" \
        "$(grep -c 'is unreachable; the next make update retries' <<< "${out}" || true)"
done
