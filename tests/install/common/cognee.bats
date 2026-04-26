#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/common/cognee.sh"
readonly TMPL_SCRIPT_PATH="./home/.chezmoiscripts/common/run_once_after_05-install-cognee.sh.tmpl"

function setup() {
    export HOME="${BATS_TEST_TMPDIR}/home"
    mkdir -p "${HOME}/.local/bin" "${HOME}/.local/share/mise/shims"
}

function teardown() {
    PATH=$(getconf PATH)
    export PATH
}

@test "[common] cognee install template renders only when opted in" {
    run chezmoi execute-template --source ./home --override-data '{}' --file "${TMPL_SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
    [ -z "${output}" ]

    run chezmoi execute-template --source ./home --override-data '{"cognee":{"install":false}}' --file "${TMPL_SCRIPT_PATH}"
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

    run bash -c 'source "$1"; install_cognee_mcp' _ "${SCRIPT_PATH}"
    [ "${status}" -eq 0 ]

    run cat "${BATS_TEST_TMPDIR}/uv_args.txt"
    [ "${status}" -eq 0 ]
    [ "${output}" = "tool install --python 3.11 --force cognee-mcp" ]
}
