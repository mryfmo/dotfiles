#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/common/hermes.sh"
readonly TMPL_SCRIPT_PATH="./home/.chezmoiscripts/common/run_once_after_04-install-hermes.sh.tmpl"

function setup() {
    ORIGINAL_PATH="${PATH}"
    export HOME="${BATS_TEST_TMPDIR}/home"
    export CHEZMOI_TEST_CONFIG="${BATS_TEST_TMPDIR}/chezmoi.yaml"
    mkdir -p "${HOME}/.local/bin" "${HOME}/.hermes"
    printf '{}\n' > "${CHEZMOI_TEST_CONFIG}"
}

function teardown() {
    export PATH="${ORIGINAL_PATH}"
}

@test "[common] hermes install template renders by default unless explicitly disabled" {
    run chezmoi --config "${CHEZMOI_TEST_CONFIG}" --config-format yaml execute-template --source ./home --override-data '{}' --file "${TMPL_SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *'Install Hermes Agent with the official non-interactive installer.'* ]]
    [[ "${output}" == *'install_hermes'* ]]

    run chezmoi --config "${CHEZMOI_TEST_CONFIG}" --config-format yaml execute-template --source ./home --override-data '{"hermes":{"install":true}}' --file "${TMPL_SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *'Install Hermes Agent with the official non-interactive installer.'* ]]
    [[ "${output}" == *'install_hermes'* ]]

    run chezmoi --config "${CHEZMOI_TEST_CONFIG}" --config-format yaml execute-template --source ./home --override-data '{"hermes":{}}' --file "${TMPL_SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *'Install Hermes Agent with the official non-interactive installer.'* ]]
    [[ "${output}" == *'install_hermes'* ]]

    run chezmoi --config "${CHEZMOI_TEST_CONFIG}" --config-format yaml execute-template --source ./home --override-data '{"hermes":{"install":false}}' --file "${TMPL_SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [ -z "${output}" ]
}

@test "[common] install_hermes passes non-interactive install options to upstream installer" {
    mkdir -p "${BATS_TEST_TMPDIR}/bin"
    cat > "${BATS_TEST_TMPDIR}/bin/curl" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" > "${BATS_TEST_TMPDIR}/curl_args.txt"
printf '%s\n' '#!/usr/bin/env bash'
printf '%s\n' 'printf "%s\n" "$*" > "${BATS_TEST_TMPDIR}/installer_args.txt"'
EOF
    chmod +x "${BATS_TEST_TMPDIR}/bin/curl"
    export PATH="${BATS_TEST_TMPDIR}/bin:${PATH}"

    run bash -c 'source "$1"; install_hermes' _ "${SCRIPT_PATH}"
    [ "${status}" -eq 0 ]

    run cat "${BATS_TEST_TMPDIR}/curl_args.txt"
    [ "${status}" -eq 0 ]
    [ "${output}" = "-fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh" ]

    run cat "${BATS_TEST_TMPDIR}/installer_args.txt"
    [ "${status}" -eq 0 ]
    [ "${output}" = "--skip-setup --hermes-home ${HOME}/.hermes --dir ${HOME}/.hermes/hermes-agent" ]
}

@test "[common] install_hermes removes legacy hermes command symlink before upstream writes launcher" {
    mkdir -p "${BATS_TEST_TMPDIR}/bin" "${HOME}/.hermes/hermes-agent/venv/bin"
    touch "${HOME}/.hermes/hermes-agent/venv/bin/hermes"
    ln -s "${HOME}/.hermes/hermes-agent/venv/bin/hermes" "${HOME}/.local/bin/hermes"
    cat > "${BATS_TEST_TMPDIR}/bin/curl" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' '#!/usr/bin/env bash'
printf '%s\n' 'if [ -L "${HOME}/.local/bin/hermes" ]; then exit 42; fi'
EOF
    chmod +x "${BATS_TEST_TMPDIR}/bin/curl"
    export PATH="${BATS_TEST_TMPDIR}/bin:${PATH}"

    run bash -c 'source "$1"; install_hermes' _ "${SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [ ! -e "${HOME}/.local/bin/hermes" ]
    [ -e "${HOME}/.hermes/hermes-agent/venv/bin/hermes" ]
}

@test "[common] hermes_command_path matches upstream command link locations" {
    run bash -c 'source "$1"; hermes_command_path' _ "${SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [ "${output}" = "${HOME}/.local/bin/hermes" ]

    run env TERMUX_VERSION=1 PREFIX="${BATS_TEST_TMPDIR}/termux" \
        bash -c 'source "$1"; hermes_command_path' _ "${SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [ "${output}" = "${BATS_TEST_TMPDIR}/termux/bin/hermes" ]

    mkdir -p "${BATS_TEST_TMPDIR}/root-bin"
    cat > "${BATS_TEST_TMPDIR}/root-bin/id" <<'EOF'
#!/usr/bin/env bash
printf '0\n'
EOF
    cat > "${BATS_TEST_TMPDIR}/root-bin/uname" <<'EOF'
#!/usr/bin/env bash
printf 'Linux\n'
EOF
    chmod +x "${BATS_TEST_TMPDIR}/root-bin/id" "${BATS_TEST_TMPDIR}/root-bin/uname"

    run env PATH="${BATS_TEST_TMPDIR}/root-bin:${PATH}" \
        bash -c 'source "$1"; hermes_command_path' _ "${SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [ "${output}" = "/usr/local/bin/hermes" ]
}
