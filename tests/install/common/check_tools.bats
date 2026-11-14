#!/usr/bin/env bats

readonly SCRIPT_PATH="./scripts/check-tools.sh"

function setup() {
    source "${SCRIPT_PATH}"
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

# check_srt (U141) resolves srt as hcom-seat does (`mise which srt`, else PATH), so each case gives it a `mise` that
# finds nothing and a PATH of its own; the pin is read from the checkout's home/dot_mise/config.toml, the fallback
# when the scratch HOME holds no applied mise config.
@test "[common] check_srt reports the installed srt beside its mise pin" {
    local bin="${BATS_TEST_TMPDIR}/bin" pin
    pin="$(awk -F'"' '/^"npm:@anthropic-ai\/sandbox-runtime" = "/ { print $4; exit }' home/dot_mise/config.toml)"
    [[ "${pin}" =~ ^[0-9]+(\.[0-9]+)+$ ]]
    mkdir -p "${bin}"
    printf '#!/usr/bin/env bash\nprintf "%s\\n"\n' "${pin}" > "${bin}/srt"
    chmod +x "${bin}/srt"
    run env HOME="${BATS_TEST_TMPDIR}" PATH="${bin}:${PATH}" bash -c "source '${SCRIPT_PATH}'; mise() { return 1; }; check_srt; echo \"req=\${required_failures}\""
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   srt -> ${bin}/srt (pin ${pin})"* ]]
    [[ "${output}" == *"${pin}"*"req=0"* ]]
    [[ "${output}" != *"required failed"* ]]
}

@test "[common] check_srt counts a required failure naming both when the installed version differs from the pin" {
    local bin="${BATS_TEST_TMPDIR}/bin" pin
    pin="$(awk -F'"' '/^"npm:@anthropic-ai\/sandbox-runtime" = "/ { print $4; exit }' home/dot_mise/config.toml)"
    mkdir -p "${bin}"
    printf '#!/usr/bin/env bash\nprintf "9.9.9\\n"\n' > "${bin}/srt"
    chmod +x "${bin}/srt"
    run env HOME="${BATS_TEST_TMPDIR}" PATH="${bin}:${PATH}" bash -c "source '${SCRIPT_PATH}'; mise() { return 1; }; check_srt; echo \"req=\${required_failures}\""
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   srt -> ${bin}/srt (pin ${pin})"* ]]
    [[ "${output}" == *"required failed: srt 9.9.9 differs from the pin ${pin}; run make update"*"req=1"* ]]

    # A --version that fails or prints nothing is the same failure, never a pass.
    printf '#!/usr/bin/env bash\nexit 1\n' > "${bin}/srt"
    run env HOME="${BATS_TEST_TMPDIR}" PATH="${bin}:${PATH}" bash -c "source '${SCRIPT_PATH}'; mise() { return 1; }; check_srt; echo \"req=\${required_failures}\""
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"required failed: srt --version printed no version (pin ${pin})"*"req=1"* ]]
}

@test "[common] check_srt warns without failing when srt is absent" {
    run env HOME="${BATS_TEST_TMPDIR}/empty" PATH="/usr/bin:/bin" bash -c "source '${SCRIPT_PATH}'; mise() { return 1; }; check_srt; echo \"req=\${required_failures}\""
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"optional warning: srt not installed; run make update"*"req=0"* ]]
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

# check_seat_logins (regime-cutover U37, U318, U498): a fake HOME with two seat profiles and a seats root whose login
# group directory `.state/claude-orchestrator` (the orchestrator profile's group) the pre-flight judges through a fake
# `claude auth status` (exit `${FAKE_CLAUDE_AUTH_STATUS:-0}`, method `${FAKE_CLAUDE_AUTH_METHOD:-claude.ai}`), so the
# host's Claude Code never runs.
function seat_login_home() {
    local home="${BATS_TEST_TMPDIR}/seat"
    mkdir -p "${home}/.agents/omp/profiles" "${BATS_TEST_TMPDIR}/fakebin"
    printf 'modelRoles:\n  default: openai-siwc/gpt-6-astra\n' > "${home}/.agents/omp/profiles/audit.yml"
    printf 'modelRoles:\n  default: claude-bridge/claude-fable-5-2\n' > "${home}/.agents/omp/profiles/orchestrator.yml"
    printf '#!/bin/sh\nprintf '"'"'{"configDirectory": "%%s", "authMethod": "%%s"}\\n'"'"' "${CLAUDE_CONFIG_DIR-}" "${FAKE_CLAUDE_AUTH_METHOD:-claude.ai}"\nexit "${FAKE_CLAUDE_AUTH_STATUS:-0}"\n' \
        > "${BATS_TEST_TMPDIR}/fakebin/claude"
    chmod +x "${BATS_TEST_TMPDIR}/fakebin/claude"
    printf '%s\n' "${home}"
}

@test "[common] check_seat_logins reports registered and present logins from presence, mtimes and the group directory" {
    local home
    home="$(seat_login_home)"
    mkdir -p "${home}/.omp/profiles/audit/agent/openai-siwc" "${home}/seats/.state/claude-orchestrator"
    printf '{"hostId":"urn:uuid:11111111-1111-4111-8111-111111111111","clientId":"oaiapp_fake"}\n' \
        > "${home}/.omp/profiles/audit/agent/openai-siwc/registration.json"
    printf 'not a database\n' > "${home}/.omp/profiles/audit/agent/agent.db"

    run env -u CLAUDE_CODE_OAUTH_TOKEN -u CLAUDE_CONFIG_DIR HOME="${home}" REGIME_SEATS_ROOT="${home}/seats" PATH="${BATS_TEST_TMPDIR}/fakebin:${PATH}" \
        bash -c "source '${SCRIPT_PATH}'; check_seat_logins; echo \"failures=\${required_failures} warnings=\${optional_warnings}\""
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   seat login audit openai-siwc: registered (host urn:uuid:11111111-1111-4111-8111-111111111111, client oaiapp_fake), agent.db mtime 20"* ]]
    [[ "${output}" == *"found:   seat login orchestrator claude-bridge: login present (claude.ai, ${home}/seats/.state/claude-orchestrator)"* ]]
    [[ "${output}" == *"failures=0 warnings=0"* ]]
}

@test "[common] check_seat_logins warns for an absent login without failing" {
    local home
    home="$(seat_login_home)"

    run env -u CLAUDE_CODE_OAUTH_TOKEN -u CLAUDE_CONFIG_DIR HOME="${home}" REGIME_SEATS_ROOT="${home}/seats" PATH="${BATS_TEST_TMPDIR}/fakebin:${PATH}" \
        bash -c "source '${SCRIPT_PATH}'; check_seat_logins; echo \"failures=\${required_failures} warnings=\${optional_warnings}\""
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"optional warning: seat login audit openai-siwc: absent (no ${home}/.omp/profiles/audit/agent/openai-siwc/registration.json)"* ]]
    [[ "${output}" == *"optional warning: seat login orchestrator claude-bridge: absent (no ${home}/seats/.state/claude-orchestrator)"* ]]
    [[ "${output}" == *"failures=0 warnings=2"* ]]
}

@test "[common] check_seat_logins counts the group directory's claude.ai login alone and never prints a token" {
    local home
    home="$(seat_login_home)"
    mkdir -p "${home}/seats/.state/claude-orchestrator" "${home}/.claude"
    printf '{}\n' > "${home}/.claude/.credentials.json"
    chmod 600 "${home}/.claude/.credentials.json"

    # U312, U318, U498: a token variable in the environment and the operator's own ~/.claude are no input; the group
    # directory's method decides, and a token or key login there is absent.
    run env -u CLAUDE_CONFIG_DIR CLAUDE_CODE_OAUTH_TOKEN=unused-variable-value HOME="${home}" REGIME_SEATS_ROOT="${home}/seats" PATH="${BATS_TEST_TMPDIR}/fakebin:${PATH}" \
        bash -c "source '${SCRIPT_PATH}'; check_seat_logins"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"found:   seat login orchestrator claude-bridge: login present (claude.ai, ${home}/seats/.state/claude-orchestrator)"* ]]
    [[ "${output}" != *"unused-variable-value"* ]]

    run env -u CLAUDE_CODE_OAUTH_TOKEN -u CLAUDE_CONFIG_DIR FAKE_CLAUDE_AUTH_METHOD=oauth_token HOME="${home}" REGIME_SEATS_ROOT="${home}/seats" PATH="${BATS_TEST_TMPDIR}/fakebin:${PATH}" \
        bash -c "source '${SCRIPT_PATH}'; check_seat_logins"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"optional warning: seat login orchestrator claude-bridge: absent (authMethod oauth_token under ${home}/seats/.state/claude-orchestrator, not claude.ai)"* ]]
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

@test "[common] a platform check counts a required failure when uname fails, never not-applicable" {
    local check
    for check in check_homebrew check_zed check_claude_sandbox; do
        run env HOME="${BATS_TEST_TMPDIR}/empty" bash -c "source '${SCRIPT_PATH}'; uname() { return 1; }; chezmoi() { printf client; }; ${check}; echo \"req=\${required_failures}\""
        [ "${status}" -eq 0 ]
        grep -qF -- "required failed: uname" <<< "${output}"
        if grep -qF -- "not applicable" <<< "${output}"; then
            false
        fi
        grep -qF -- "req=1" <<< "${output}"
    done
}
