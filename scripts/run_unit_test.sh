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
#   Instead scripts/ci/run-bats.py starts Bats in a session of its own and reads its extended stream
#   (`--formatter cat`), whose `begin <n> <name>` line names each test as it starts. It prints the TAP
#   lines; when a test has no result within the bound it prints `not ok <n> <name> # timeout after <s> s`,
#   kills every process of that session and of Bats' process tree, and fails. Time spent outside a test,
#   such as loading a file, gets the same bound. A run that plans no test fails. python3 runs it with
#   `-I`, so no PYTHON* variable or user site directory changes it.
# @arg $@ string Arguments passed to bats.
# @env BATS_PER_TEST_TIMEOUT Seconds one test may run. Default: 900 (scripts/ci/run-bats.py).
# @exitcode 124 A test, or the time between two lines outside a test, exceeded the bound.
# @exitcode 1 Bats planned no test.
# @exitcode Bats' exit status otherwise.
#
function run_bats() {
    python3 -I "$(dirname "${BASH_SOURCE[0]}")/ci/run-bats.py" "$@"
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

    if [[ "${OS}" == macos-* ]] && [ "${SYSTEM}" == "client" ]; then
        bats_args=(tests/files/macos.bats)
    elif [[ "${OS}" == ubuntu-* ]] && { [ "${SYSTEM}" == "client" ] || [ "${SYSTEM}" == "server" ]; }; then
        bats_args=(--filter-tags "common,ubuntu:${SYSTEM}" tests/files/ubuntu.bats)
    else
        echo "${OS} and ${SYSTEM} are not supported" >&2
        exit 1
    fi

    # No separate `bats --count`: it would load the files outside the bound. run_bats fails a run that plans
    # no test.
    HOME="${FILES_TEST_HOME:?FILES_TEST_HOME is required}" run_bats "${bats_args[@]}"
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
