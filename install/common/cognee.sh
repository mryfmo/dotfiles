#!/usr/bin/env bash

# @file install/common/cognee.sh
# @brief Install Cognee MCP with uv tool.
# @description
#   Installs the `cognee-mcp` command used by the optional shared Cognee MCP
#   memory server. Runtime secrets, model provider settings, and database URLs
#   must be supplied by the target machine environment or private chezmoi source.

# set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly COGNEE_MCP_PACKAGE="${COGNEE_MCP_PACKAGE:-cognee-mcp}"
readonly COGNEE_MCP_PYTHON="${COGNEE_MCP_PYTHON:-3.11}"

#
# @description Resolve the uv executable installed by mise or already available on PATH.
# @stdout Absolute or shell-resolved path to uv.
#
function resolve_uv() {
    local mise_shims="${HOME}/.local/share/mise/shims"
    local mise_uv="${mise_shims}/uv"
    if [ -x "${mise_uv}" ]; then
        printf '%s\n' "${mise_uv}"
        return 0
    fi

    if command -v uv > /dev/null 2>&1; then
        command -v uv
        return 0
    fi

    printf 'uv is required before installing Cognee MCP. Run the mise installer first.\n' >&2
    return 1
}

#
# @description Install or refresh the Cognee MCP command with uv tool.
#
function install_cognee_mcp() {
    local uv_bin
    uv_bin="$(resolve_uv)"
    export PATH="${HOME}/.local/share/mise/shims:${PATH}"
    "${uv_bin}" tool install --python "${COGNEE_MCP_PYTHON}" --force "${COGNEE_MCP_PACKAGE}"
}

#
# @description Run the Cognee MCP installation flow.
#
function main() {
    install_cognee_mcp
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
