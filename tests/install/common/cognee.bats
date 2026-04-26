#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/common/cognee.sh"
readonly TMPL_SCRIPT_PATH="./home/.chezmoiscripts/common/run_once_after_05-install-cognee.sh.tmpl"

function setup() {
    export HOME="${BATS_TEST_TMPDIR}/home"
    mkdir -p "${HOME}/.local/bin" "${HOME}/.local/share/mise/shims"

    source "${SCRIPT_PATH}"
}

function teardown() {
    PATH=$(getconf PATH)
    export PATH
}

@test "[common] cognee install template is opt-in" {
    run chezmoi execute-template --source ./home --override-data '{}' --file "${TMPL_SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [ -z "${output}" ]

    run chezmoi execute-template --source ./home --override-data '{"cognee":{"install":true}}' --file "${TMPL_SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [[ "${output}" == *'Install Cognee MCP with uv tool.'* ]]
    [[ "${output}" == *'install_cognee_mcp'* ]]
}

@test "[common] install_cognee_mcp installs cognee-mcp with uv tool" {
    cat > "${HOME}/.local/share/mise/shims/uv" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" > "${BATS_TEST_TMPDIR}/uv_args.txt"
EOF
    chmod +x "${HOME}/.local/share/mise/shims/uv"

    install_cognee_mcp

    run cat "${BATS_TEST_TMPDIR}/uv_args.txt"
    [ "${status}" -eq 0 ]
    [ "${output}" = "tool install --python ${COGNEE_MCP_PYTHON} --force ${COGNEE_MCP_PACKAGE}" ]
}
