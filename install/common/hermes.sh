#!/usr/bin/env bash

# @file install/common/hermes.sh
# @brief Install Hermes Agent with the official non-interactive installer.
# @description
#   Downloads the upstream Hermes Agent installer and runs it with `--skip-setup`
#   so provider selection, OAuth, and API-key setup remain an explicit user step.

# set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly HERMES_INSTALL_SCRIPT_URL="https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh"
readonly HERMES_INSTALL_DIR="${HERMES_INSTALL_DIR:-${HOME}/.hermes/hermes-agent}"
readonly HERMES_HOME="${HERMES_HOME:-${HOME}/.hermes}"

#
# @description Print the user-facing Hermes command path used by the upstream installer.
#
function hermes_command_path() {
    if [ -n "${TERMUX_VERSION:-}" ] || [[ "${PREFIX:-}" == *"com.termux/files/usr"* ]]; then
        printf '%s\n' "${PREFIX}/bin/hermes"
    elif [ "$(id -u)" -eq 0 ] && [ "$(uname -s)" = "Linux" ]; then
        printf '%s\n' "/usr/local/bin/hermes"
    else
        printf '%s\n' "${HOME}/.local/bin/hermes"
    fi
}

#
# @description Remove legacy Hermes command symlinks before the upstream installer writes a launcher.
#   The upstream installer writes a launcher with `cat > "$command_link_dir/hermes"`.
#   If that path is an existing symlink to the venv entry point, shell redirection
#   follows it and overwrites the real entry point with a self-referential shim.
#
function prepare_hermes_command_path() {
    local command_path

    command_path="$(hermes_command_path)"
    if [ -L "${command_path}" ]; then
        unlink "${command_path}"
    fi
}

#
# @description Install Hermes Agent without running the interactive setup flow.
#
function install_hermes() {
    prepare_hermes_command_path
    curl -fsSL "${HERMES_INSTALL_SCRIPT_URL}" | bash -s -- \
        --skip-setup \
        --hermes-home "${HERMES_HOME}" \
        --dir "${HERMES_INSTALL_DIR}"
}

#
# @description Run the Hermes Agent installation flow.
#
function main() {
    install_hermes
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
