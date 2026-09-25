#!/usr/bin/env bats

readonly SCRIPT_PATH="./home/dot_local/bin/common/executable_provision-machine-key"

function setup() {
    source "${SCRIPT_PATH}"
}

@test "[common] provision-machine-key displays an existing key without regenerating it" {
    local home_dir="${BATS_TEST_TMPDIR}/home"
    mkdir -p "${home_dir}/.ssh"
    printf 'ssh-ed25519 AAAAexisting\n' > "${home_dir}/.ssh/id_ed25519.pub"

    run env HOME="${home_dir}" bash -c "
        source '${SCRIPT_PATH}'
        function ssh-keygen() { printf 'unexpected ssh-keygen call\n'; return 99; }
        main
    "

    [ "${status}" -eq 0 ]
    [[ "${output}" == *"Machine SSH key already exists"* ]]
    [[ "${output}" == *"gh ssh-key add"*"--type authentication"* ]]
    [[ "${output}" == *"gh ssh-key add"*"--type signing"* ]]
    [[ "${output}" == *"AAAAexisting"* ]]
}

@test "[common] provision-machine-key generates a non-interactive key when missing" {
    local home_dir="${BATS_TEST_TMPDIR}/home"
    local calls_path="${BATS_TEST_TMPDIR}/calls.txt"
    mkdir -p "${home_dir}"
    : > "${calls_path}"

    run env HOME="${home_dir}" CALLS_PATH="${calls_path}" bash -c '
        source "'"${SCRIPT_PATH}"'"
        function ssh-keygen() {
            printf "%s\n" "$*" >> "${CALLS_PATH}"
            local key_path=""
            while [ "$#" -gt 0 ]; do
                if [ "$1" = "-f" ]; then
                    key_path="$2"
                    break
                fi
                shift
            done
            printf "generated\n" > "${key_path}"
            printf "ssh-ed25519 AAAAgenerated\n" > "${key_path}.pub"
        }
        main
    '

    [ "${status}" -eq 0 ]
    [[ "${output}" == *"Generating machine SSH key"* ]]
    [[ "${output}" == *"AAAAgenerated"* ]]
    run cat "${calls_path}"
    [[ "${output}" == *"-t ed25519"* ]]
    [[ "${output}" == *"-N "* ]]
}
