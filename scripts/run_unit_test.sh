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
# @description Run the pinned Bats, failing by name a test that runs longer than BATS_PER_TEST_TIMEOUT.
# @description
#   The Bats on PATH must be the release home/dot_mise/config.toml pins: scripts/ci/pinned-tool-version.sh
#   runs first, and any other version, or a check that cannot run, refuses the suite with its message
#   (regime-cutover U127; CI installs the pin with scripts/ci/install-pinned-lint-tools.sh, a host with
#   `mise install http:bats`); its accepted line is printed, so every suite log names the version it ran.
#   Bats' own BATS_TEST_TIMEOUT is not used. The pinned release holds the run for the whole bound after
#   any failing test (bats-core#1206); the older Bats a host without the pin would run (refused above)
#   kills only a timed-out test's direct children, so a stalled grandchild such as `sudo snap` keeps
#   Bats' output pipe open and the run still hangs (bats-core#1020).
#   Instead scripts/ci/run-bats.py reads Bats' extended stream (`--formatter cat`): it prints
#   `running: <n> <name>` as each test starts, then the TAP lines; when a test has no result within the
#   bound it prints `not ok <n> <name> # timeout after <s> s` and fails with 124. Time spent outside a
#   test, such as loading a file, gets the same bound. A run that plans no test fails. It signals
#   nothing: the workflow step's timeout-minutes and the runner stop what a stalled test left running.
#   `--timing` is passed before the arguments (regime-cutover U128): each result line then carries its
#   duration, the wrapper prints `slowest: <n> <name> <ms> ms` after the stream, and writes the stall line
#   with its diagnosis, or a passing run's slowest line, to the file GITHUB_STEP_SUMMARY names.
#   python3 runs it with `-I -S`, so no PYTHON* variable, user site or site-packages changes it.
# @arg $@ string Arguments passed to bats.
# @env BATS_PER_TEST_TIMEOUT Seconds one test may run. Default: the wrapper's DEFAULT_BOUND (scripts/ci/run-bats.py).
# @exitcode 124 A test, or the time between two lines outside a test, exceeded the bound.
# @exitcode 1 Bats planned no test, dirname failed, or the Bats on PATH is not the pinned release (or could not be checked).
# @exitcode Bats' exit status otherwise.
#
function run_bats() {
    local here accepted
    here="$(dirname "${BASH_SOURCE[0]}")" || return 1
    # The check's status decides (standing order 21): a refusal, or a check that cannot run, ends the suite here.
    accepted="$("${here}/ci/pinned-tool-version.sh" "${here}/../home/dot_mise/config.toml" bats)" || return 1
    printf '%s\n' "${accepted}"
    python3 -I -S "${here}/ci/run-bats.py" --timing "$@"
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
