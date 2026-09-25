#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/server/setup_timezone.sh"
readonly TMPL_PATH="./home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl"

@test "[ubuntu-server] setup_timezone configures Asia/Tokyo" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        sudo() {
            printf "%s\n" "$*"
        }
        main
    '

    [ "${status}" -eq 0 ]
    [[ "${output}" == *"ln -snf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime"* ]]
    [[ "${output}" == *"tee /etc/timezone"* ]]
    [[ "${output}" == *"apt-get install -y tzdata"* ]]
}

@test "[ubuntu-server] setup_timezone is wired for the server role only" {
    grep -Fq 'include "../install/ubuntu/server/setup_timezone.sh"' "${TMPL_PATH}"
    grep -Fq '.system "server"' "${TMPL_PATH}"
}
