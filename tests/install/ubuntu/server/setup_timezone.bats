#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/server/setup_timezone.sh"
readonly TMPL_PATH="./home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl"

# @description Run the script's main with sudo as a shell function that appends its argv to
#   ${BATS_TEST_TMPDIR}/sudo.log, and readlink as a shell function that runs $1 in place of the real one, so a case
#   chooses what /etc/localtime resolves to without writing it (U254). GITHUB_ACTIONS is unset first: the CI runner
#   sets it, and a case that wants the runner branch passes it again in $2.
# @arg $1 string The shell text the fake readlink runs; its stdout and exit status are the fake's.
# @arg $2 string Environment assignments (`NAME=value`) for `env`, after the unset; may be empty.
function run_main() {
    # shellcheck disable=SC2086 # $2 is a list of NAME=value words, split on purpose.
    run env -u GITHUB_ACTIONS ${2:-} /bin/bash -c '
        source "$1"
        sudo_log="$2"
        sudo() {
            echo "$*" >> "${sudo_log}"
        }
        eval "readlink() { $3; }"
        main
    ' _ "${SCRIPT_PATH}" "${BATS_TEST_TMPDIR}/sudo.log" "$1"
}

@test "[ubuntu-server] setup_timezone leaves a host already on Asia/Tokyo alone" {
    run_main 'echo /usr/share/zoneinfo/Asia/Tokyo'

    [ "${status}" -eq 0 ]
    [ "${output}" = "timezone: already Asia/Tokyo" ]
    [ ! -e "${BATS_TEST_TMPDIR}/sudo.log" ]
}

@test "[ubuntu-server] setup_timezone never replaces /etc/localtime on a GitHub runner" {
    run_main 'echo /usr/share/zoneinfo/Etc/UTC' GITHUB_ACTIONS=true

    [ "${status}" -eq 0 ]
    [ "${output}" = "timezone: unchanged on a GitHub runner (GITHUB_ACTIONS is set; replacing /etc/localtime stalls the runner, regime-cutover U254)" ]
    [ ! -e "${BATS_TEST_TMPDIR}/sudo.log" ]
}

@test "[ubuntu-server] setup_timezone configures Asia/Tokyo on a host that resolves to UTC" {
    run_main 'echo /usr/share/zoneinfo/Etc/UTC'

    [ "${status}" -eq 0 ]
    [[ "${output}" == "timezone: setting Asia/Tokyo (was /usr/share/zoneinfo/Etc/UTC)"* ]]
    [ "$(wc -l < "${BATS_TEST_TMPDIR}/sudo.log")" -eq 3 ]
    [ "$(sed -n 1p "${BATS_TEST_TMPDIR}/sudo.log")" = "ln -snf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime" ]
    [ "$(sed -n 2p "${BATS_TEST_TMPDIR}/sudo.log")" = "tee /etc/timezone" ]
    # The frontend must be an argument to sudo: env_reset drops it from the caller's environment.
    [ "$(sed -n 3p "${BATS_TEST_TMPDIR}/sudo.log")" = "DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata" ]
}

@test "[ubuntu-server] setup_timezone reads an unreadable /etc/localtime as an unknown zone and sets it" {
    run_main 'return 1'

    [ "${status}" -eq 0 ]
    [[ "${output}" == "timezone: setting Asia/Tokyo (was unknown)"* ]]
    [ "$(wc -l < "${BATS_TEST_TMPDIR}/sudo.log")" -eq 3 ]
    [ "$(sed -n 1p "${BATS_TEST_TMPDIR}/sudo.log")" = "ln -snf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime" ]
}

@test "[ubuntu-server] setup_timezone is wired for the server role only" {
    grep -Fq 'include "../install/ubuntu/server/setup_timezone.sh"' "${TMPL_PATH}"
    grep -Fq '.system "server"' "${TMPL_PATH}"
}
