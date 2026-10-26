#!/usr/bin/env bash

# @file scripts/run_unit_test.sh
# @brief Run the repository's shell unit tests.
# @description
#   Dispatches the common Bats suite and the OS/system-specific Bats suite
#   selected by the `OS` and `SYSTEM` environment variables. Every Bats run
#   goes through run_bats, which fails a test by name when it outlives
#   BATS_PER_TEST_TIMEOUT.

# Keep this wrapper minimal: CI invokes this script through `bashcov`.
# `-u` is intentionally omitted because strict nounset can propagate through
# bashcov's SHELLOPTS/xtrace path and break third-party scripts under test.
set -Eeo pipefail

#
# @description Run Bats, failing by name a test that runs longer than BATS_PER_TEST_TIMEOUT.
# @description
#   Bats' own BATS_TEST_TIMEOUT is not used. Bats 1.10.0 (the ubuntu-24.04 apt package) kills only a
#   timed-out test's direct children, so a stalled grandchild such as `sudo snap` keeps Bats' output pipe
#   open and the run still hangs (bats-core#1020). Bats 1.13.0 (ubuntu-26.04) and 1.14.0 (Homebrew) hold
#   the run for the whole bound after any failing test (bats-core#1206).
#   Instead Bats writes its extended stream (`--formatter cat`), whose `begin <n> <name>` line names each
#   test as it starts. This function prints the TAP lines from that stream. When a test has no result
#   within the bound, it prints `not ok <n> <name> # timeout after <s> s`, stops Bats' whole process group
#   (SIGTERM, then SIGKILL after 10 s) and fails. Time spent outside a test, such as loading a file, gets
#   the same bound, counted from the last line.
# @arg $@ string Arguments passed to bats.
# @env BATS_PER_TEST_TIMEOUT Seconds one test may run. Default: 900, ten times the slowest passing test
#   measured on main (`[ubuntu-client] misc`, 89 s on ubuntu-24.04, October 2026) and four times the
#   slowest test of a passing run on a slow mirror (`[ubuntu-client] ghostty`, 214 s).
# @exitcode 124 A test, or the time between two lines outside a test, exceeded the bound.
# @exitcode 1 The stream FIFO could not be created.
# @exitcode Bats' exit status otherwise.
#
function run_bats() {
    local limit="${BATS_PER_TEST_TIMEOUT:-900}" dir pid line left running="" deadline timed_out="" status=0 i
    dir="$(mktemp -d "${TMPDIR:-/tmp}/run-bats.XXXXXX")" || return 1
    if ! mkfifo "${dir}/stream"; then
        rm -rf "${dir}"
        return 1
    fi
    # Job control gives Bats its own process group, so a stalled test's whole tree can be stopped. A
    # background job that reads the terminal is stopped, so Bats reads /dev/null.
    set -m
    bats --formatter cat "$@" < /dev/null > "${dir}/stream" &
    pid=$!
    set +m
    deadline=$((SECONDS + limit))
    while true; do
        left=$((deadline - SECONDS))
        if [ "${left}" -le 0 ]; then
            timed_out=1
            break
        fi
        if IFS= read -r -t "${left}" line; then
            case "${line}" in
            'begin '*)
                running="${line#begin }"
                deadline=$((SECONDS + limit))
                continue
                ;;
            'suite '*) continue ;;
            'ok '* | 'not ok '*) running="" ;;
            esac
            # A test's own output lines do not extend its bound.
            [ -n "${running}" ] || deadline=$((SECONDS + limit))
            printf '%s\n' "${line}"
        else
            # A timed-out read returns over 128 on bash 4 and later, and 1, as at end of input, on bash 3.2.
            [ "$?" -le 128 ] && [ "${SECONDS}" -lt "${deadline}" ] || timed_out=1
            break
        fi
    done < "${dir}/stream"
    if [ -n "${timed_out}" ]; then
        if [ -n "${running}" ]; then
            printf 'not ok %s # timeout after %d s (BATS_PER_TEST_TIMEOUT); stopping Bats\n' "${running}" "${limit}"
        else
            printf 'not ok - Bats printed nothing for %d s outside a test (BATS_PER_TEST_TIMEOUT); stopping Bats\n' \
                "${limit}"
        fi
        kill -TERM -- "-${pid}" 2> /dev/null || true
        for ((i = 0; i < 10; i++)); do
            kill -0 -- "-${pid}" 2> /dev/null || break
            sleep 1
        done
        kill -KILL -- "-${pid}" 2> /dev/null || true
        wait "${pid}" 2> /dev/null || true
        rm -rf "${dir}"
        return 124
    fi
    wait "${pid}" || status=$?
    rm -rf "${dir}"
    return "${status}"
}

#
# @description Run the install tests shared across all CI targets.
#
function run_common_test() {
    # Common install tests executed on every matrix target.
    run_bats -r "tests/install/common/"
}

#
# @description Run the OS-specific Bats suite for the active CI target.
#
function run_os_specific_test() {
    if [[ "${OS}" == macos-* ]]; then
        # macOS-only install tests.
        run_bats -r "tests/install/macos/common/"

    elif [[ "${OS}" == ubuntu-* ]]; then
        # Ubuntu install tests shared by client and server targets.
        run_bats -r "tests/install/ubuntu/common/"

        if [ "${SYSTEM}" == "client" ] || [ "${SYSTEM}" == "server" ]; then
            # Ubuntu install tests for the selected system target.
            run_bats -r "tests/install/ubuntu/${SYSTEM}/"
        else
            echo "${OS} and ${SYSTEM} are not supported" >&2
            exit 1
        fi
    else
        echo "${OS} and ${SYSTEM} are not supported" >&2
        exit 1
    fi
}

#
# @description Run the rendered public-dotfiles manifest tests for the active CI target.
#
function run_files_test() {
    local -a bats_args
    local test_count

    if [[ "${OS}" == macos-* ]] && [ "${SYSTEM}" == "client" ]; then
        bats_args=(tests/files/macos.bats)
    elif [[ "${OS}" == ubuntu-* ]] && { [ "${SYSTEM}" == "client" ] || [ "${SYSTEM}" == "server" ]; }; then
        bats_args=(--filter-tags "common,ubuntu:${SYSTEM}" tests/files/ubuntu.bats)
    else
        echo "${OS} and ${SYSTEM} are not supported" >&2
        exit 1
    fi

    test_count="$(HOME="${FILES_TEST_HOME:?FILES_TEST_HOME is required}" bats --count "${bats_args[@]}")"
    if [[ ! ${test_count} =~ ^[1-9][0-9]*$ ]]; then
        echo "Expected at least one files test; got ${test_count:-no count}" >&2
        exit 1
    fi
    HOME="${FILES_TEST_HOME}" run_bats "${bats_args[@]}"
}

#
# @description Run the full unit test flow used by CI.
#
function main() {
    run_files_test
    run_common_test
    run_os_specific_test
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
