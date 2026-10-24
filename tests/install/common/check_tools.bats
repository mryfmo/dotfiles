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

@test "[common] check_omp reports its pin and warns when absent" {
    local bin="${BATS_TEST_TMPDIR}/.local/bin"
    source ./scripts/lib/installer-pins.sh
    mkdir -p "${bin}"
    printf '#!/usr/bin/env bash\nprintf "omp %s\\n"\n' "${OMP_PIN_VERSION}" > "${bin}/omp"
    chmod +x "${bin}/omp"
    run env HOME="${BATS_TEST_TMPDIR}" bash -c "source '${SCRIPT_PATH}'; check_omp"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   omp ->"*"(pin ${OMP_PIN_VERSION})"* ]]
    [[ "${output}" == *"omp ${OMP_PIN_VERSION}"* ]]

    run env HOME="${BATS_TEST_TMPDIR}/empty" bash -c 'source "$1"; check_omp; [ "$required_failures" -eq 0 ]' bash "${SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"optional warning: omp not installed"* ]]
}

@test "[common] check_hcom reports its pin and warns when absent" {
    local bin="${BATS_TEST_TMPDIR}/.local/bin"
    source ./scripts/lib/installer-pins.sh
    mkdir -p "${bin}"
    printf '#!/usr/bin/env bash\nprintf "hcom %s\\n"\n' "${HCOM_PIN_VERSION}" > "${bin}/hcom"
    chmod +x "${bin}/hcom"
    run env HOME="${BATS_TEST_TMPDIR}" bash -c "source '${SCRIPT_PATH}'; check_hcom"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   hcom ->"*"(pin ${HCOM_PIN_VERSION})"* ]]
    [[ "${output}" == *"hcom ${HCOM_PIN_VERSION}"* ]]

    run env HOME="${BATS_TEST_TMPDIR}/empty" bash -c 'source "$1"; check_hcom; [ "$required_failures" -eq 0 ]' bash "${SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"optional warning: hcom not installed"* ]]
}

@test "[common] check_zed is not applicable outside an Ubuntu client" {
    run env HOME="${BATS_TEST_TMPDIR}/empty" bash -c "source '${SCRIPT_PATH}'; uname() { printf 'Darwin\\n'; }; chezmoi() { printf client; }; check_zed"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"not applicable: Zed (installed on Ubuntu clients only)"* ]]
}

@test "[common] check_zed warns with the gh-auth hint when Zed is missing on a client" {
    run env HOME="${BATS_TEST_TMPDIR}/empty" bash -c "source '${SCRIPT_PATH}'; uname() { printf 'Linux\\n'; }; chezmoi() { printf client; }; check_zed"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"optional warning: zed not installed: run make gh-auth, then make update"* ]]
}

@test "[common] check_zed reports the installed Zed on a client" {
    local zed_path="${BATS_TEST_TMPDIR}/.local/bin/zed"
    mkdir -p "$(dirname "${zed_path}")"
    printf '#!/usr/bin/env bash\nprintf "Zed 1.22.0 deadbeef\\n"\n' > "${zed_path}"
    chmod +x "${zed_path}"

    run env HOME="${BATS_TEST_TMPDIR}" bash -c "source '${SCRIPT_PATH}'; uname() { printf 'Linux\\n'; }; chezmoi() { printf client; }; check_zed"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   zed -> ${zed_path}"* ]]
    [[ "${output}" == *"Zed 1.22.0"* ]]
}

@test "[common] check_crit_cli is not applicable and not a failure when absent" {
    run env HOME="${BATS_TEST_TMPDIR}/empty" bash -c "source '${SCRIPT_PATH}'; check_crit_cli"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"not applicable: Crit CLI (not installed)"* ]]
}

@test "[common] check_crit_cli warns instead of aborting when --version fails" {
    local crit_path="${BATS_TEST_TMPDIR}/.local/bin/crit"
    mkdir -p "$(dirname "${crit_path}")"
    printf '#!/usr/bin/env bash\nexit 1\n' > "${crit_path}"
    chmod +x "${crit_path}"

    run env HOME="${BATS_TEST_TMPDIR}" bash -c "source '${SCRIPT_PATH}'; check_crit_cli"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   crit ->"* ]]
    [[ "${output}" == *"optional warning: crit --version failed"* ]]
}
