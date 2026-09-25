#!/usr/bin/env bats

readonly SCRIPT_PATH="./scripts/check-tools.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

@test "[common] check_machine_ssh_key reports found when the public key exists" {
    local key_path="${BATS_TEST_TMPDIR}/.ssh/id_ed25519.pub"
    mkdir -p "$(dirname "${key_path}")"
    touch "${key_path}"

    run env HOME="${BATS_TEST_TMPDIR}" bash -c "source '${SCRIPT_PATH}'; check_machine_ssh_key"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   machine SSH key"* ]]
}

@test "[common] check_machine_ssh_key warns and suggests provision-machine-key when missing" {
    run env HOME="${BATS_TEST_TMPDIR}/empty" bash -c "source '${SCRIPT_PATH}'; check_machine_ssh_key"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"optional warning: machine SSH key is missing"* ]]
    [[ "${output}" == *"provision-machine-key"* ]]
}
