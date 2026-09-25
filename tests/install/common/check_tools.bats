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

@test "[common] check_crit_cli reports the pinned version and origin when installed" {
    local crit_path="${BATS_TEST_TMPDIR}/.local/bin/crit"
    mkdir -p "$(dirname "${crit_path}")"
    printf '#!/usr/bin/env bash\nprintf "crit 0.20.3\\n"\n' > "${crit_path}"
    chmod +x "${crit_path}"

    run env HOME="${BATS_TEST_TMPDIR}" bash -c "source '${SCRIPT_PATH}'; check_crit_cli"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   crit ->"*"(pinned release)"* ]]
    [[ "${output}" == *"crit 0.20.3"* ]]
}

@test "[common] check_crit_cli is not applicable and not a failure when absent" {
    run env HOME="${BATS_TEST_TMPDIR}/empty" bash -c "source '${SCRIPT_PATH}'; check_crit_cli"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"not applicable: Crit CLI (not installed)"* ]]
}
