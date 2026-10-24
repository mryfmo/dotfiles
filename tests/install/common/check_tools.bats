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

@test "[common] check_agmsg reports the installed version against the pin" {
    local skill_dir="${BATS_TEST_TMPDIR}/.agents/skills/agmsg"
    mkdir -p "${skill_dir}"
    local pin
    pin="$(awk -F'"' '/^AGMSG_PIN_VERSION=/ { print $2; exit }' scripts/update-agent-assets.sh)"
    printf '%s\n' "${pin}" > "${skill_dir}/VERSION"

    run env HOME="${BATS_TEST_TMPDIR}" bash -c "source '${SCRIPT_PATH}'; check_agmsg"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   agmsg ->"*"matches pin"* ]]
}

@test "[common] check_agmsg warns when the installed version does not match the pin" {
    local skill_dir="${BATS_TEST_TMPDIR}/.agents/skills/agmsg"
    mkdir -p "${skill_dir}"
    printf '0.0.0\n' > "${skill_dir}/VERSION"

    run env HOME="${BATS_TEST_TMPDIR}" bash -c "source '${SCRIPT_PATH}'; check_agmsg"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"optional warning: agmsg version 0.0.0 does not match the pinned"* ]]
}

@test "[common] check_agmsg is not applicable and not a failure when absent" {
    run env HOME="${BATS_TEST_TMPDIR}/empty" bash -c "source '${SCRIPT_PATH}'; check_agmsg"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"not applicable: agmsg (not installed)"* ]]
}

# check_seat_logins (regime-cutover U37): a fake HOME with two seat profiles; `security` is faked so the
# macOS Keychain branch never sees the real login of the host running the test.
function seat_login_home() {
    local home="${BATS_TEST_TMPDIR}/seat"
    mkdir -p "${home}/.agents/omp/profiles" "${BATS_TEST_TMPDIR}/fakebin"
    printf 'modelRoles:\n  default: openai-siwc/gpt-6-astra\n' > "${home}/.agents/omp/profiles/audit.yml"
    printf 'modelRoles:\n  default: claude-bridge/claude-fable-5-1\n' > "${home}/.agents/omp/profiles/orchestrator.yml"
    printf '#!/bin/sh\nexit %s\n' "${1:-44}" > "${BATS_TEST_TMPDIR}/fakebin/security"
    chmod +x "${BATS_TEST_TMPDIR}/fakebin/security"
    printf '%s\n' "${home}"
}

@test "[common] check_seat_logins reports registered and present logins from presence and mtimes" {
    local home
    home="$(seat_login_home)"
    mkdir -p "${home}/.omp/profiles/audit/agent/openai-siwc" "${home}/.claude"
    printf '{"hostId":"urn:uuid:11111111-1111-4111-8111-111111111111","clientId":"oaiapp_fake"}\n' \
        > "${home}/.omp/profiles/audit/agent/openai-siwc/registration.json"
    printf 'not a database\n' > "${home}/.omp/profiles/audit/agent/agent.db"
    printf '{}\n' > "${home}/.claude/.credentials.json"
    chmod 600 "${home}/.claude/.credentials.json"

    run env -u CLAUDE_CODE_OAUTH_TOKEN -u CLAUDE_CONFIG_DIR HOME="${home}" PATH="${BATS_TEST_TMPDIR}/fakebin:${PATH}" \
        bash -c "source '${SCRIPT_PATH}'; check_seat_logins; echo \"failures=\${required_failures} warnings=\${optional_warnings}\""
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   seat login audit openai-siwc: registered (host urn:uuid:11111111-1111-4111-8111-111111111111, client oaiapp_fake), agent.db mtime 20"* ]]
    [[ "${output}" == *"found:   seat login orchestrator claude-bridge: login present (credentials file 600, mtime 20"* ]]
    [[ "${output}" == *"failures=0 warnings=0"* ]]
}

@test "[common] check_seat_logins warns for an absent login without failing" {
    local home
    home="$(seat_login_home)"

    run env -u CLAUDE_CODE_OAUTH_TOKEN -u CLAUDE_CONFIG_DIR HOME="${home}" PATH="${BATS_TEST_TMPDIR}/fakebin:${PATH}" \
        bash -c "source '${SCRIPT_PATH}'; check_seat_logins; echo \"failures=\${required_failures} warnings=\${optional_warnings}\""
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"optional warning: seat login audit openai-siwc: absent (no ${home}/.omp/profiles/audit/agent/openai-siwc/registration.json)"* ]]
    [[ "${output}" == *"optional warning: seat login orchestrator claude-bridge: absent"* ]]
    [[ "${output}" == *"failures=0 warnings=2"* ]]
}

@test "[common] check_seat_logins counts an exported token as the Claude login and never prints it" {
    local home
    home="$(seat_login_home)"

    run env -u CLAUDE_CONFIG_DIR CLAUDE_CODE_OAUTH_TOKEN=fake-token-value HOME="${home}" PATH="${BATS_TEST_TMPDIR}/fakebin:${PATH}" \
        bash -c "source '${SCRIPT_PATH}'; check_seat_logins"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   seat login orchestrator claude-bridge: login present (env token)"* ]]
    [[ "${output}" != *"fake-token-value"* ]]
}

@test "[common] check_seat_logins fails on an unreadable SIWC record instead of calling it absent" {
    local home
    home="$(seat_login_home)"
    mkdir -p "${home}/.omp/profiles/audit/agent/openai-siwc"
    printf '{ not json\n' > "${home}/.omp/profiles/audit/agent/openai-siwc/registration.json"

    run env -u CLAUDE_CODE_OAUTH_TOKEN HOME="${home}" PATH="${BATS_TEST_TMPDIR}/fakebin:${PATH}" \
        bash -c "source '${SCRIPT_PATH}'; check_seat_logins; [ \"\${required_failures}\" -eq 1 ]"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"required failed: seat login audit openai-siwc: unreadable (${home}/.omp/profiles/audit/agent/openai-siwc/registration.json)"* ]]
    [[ "${output}" != *"audit openai-siwc: absent"* ]]
}

@test "[common] check_seat_logins reports the pre-flight's own failure as a failure, never as found" {
    local home
    home="$(seat_login_home)"
    printf '#!/bin/sh\nexit 1\n' > "${BATS_TEST_TMPDIR}/fakebin/uname"
    chmod +x "${BATS_TEST_TMPDIR}/fakebin/uname"

    run env -u CLAUDE_CODE_OAUTH_TOKEN HOME="${home}" PATH="${BATS_TEST_TMPDIR}/fakebin:${PATH}" \
        bash -c "source '${SCRIPT_PATH}'; check_seat_logins; [ \"\${required_failures}\" -eq 1 ]"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"required failed: seat-login-preflight: cannot read the system name: uname -s failed"* ]]
    [[ "${output}" != *"found:"* ]]
}

@test "[common] check_seat_logins is not applicable without seat profiles" {
    run env HOME="${BATS_TEST_TMPDIR}/empty" bash -c "source '${SCRIPT_PATH}'; check_seat_logins; [ \"\${optional_warnings}\" -eq 0 ]"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"not applicable: no omp seat profiles under ${BATS_TEST_TMPDIR}/empty/.agents/omp/profiles"* ]]
}
