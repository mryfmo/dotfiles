#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/server/ssh_server.sh"

@test "[ubuntu-server] ssh_server refuses to run outside a container and never reaches main" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        in_container() { return 1; }
        main() { echo "MAIN-RAN"; }
        run_in_container_only
    '

    [ "${status}" -eq 1 ]
    [[ "${output}" != *"MAIN-RAN"* ]]
    [[ "${output}" == *"/.dockerenv"* ]]
}

@test "[ubuntu-server] ssh_server runs main inside a container" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        in_container() { return 0; }
        main() { echo "MAIN-RAN"; }
        run_in_container_only
    '

    [ "${status}" -eq 0 ]
    [[ "${output}" == *"MAIN-RAN"* ]]
}

@test "[ubuntu-server] ssh_server keeps root login and listen addresses at the sshd defaults" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        sudo() { printf "%s\n" "$*"; }
        mkdir() { :; }
        touch() { :; }
        configure_accept_env() { :; }
        setup_sshd
    '

    [ "${status}" -eq 0 ]
    [[ "${output}" != *"PermitRootLogin yes"* ]]
    [[ "${output}" != *"ListenAddress"* ]]
}
