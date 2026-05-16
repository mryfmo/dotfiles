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
function hermes_command_link() {
    if [ -n "${HERMES_COMMAND_LINK:-}" ]; then
        printf '%s\n' "${HERMES_COMMAND_LINK}"
    elif [ -n "${TERMUX_VERSION:-}" ] || [[ "${PREFIX:-}" == *"com.termux/files/usr"* ]]; then
        printf '%s\n' "${PREFIX%/}/bin/hermes"
    else
        printf '%s\n' "${HOME%/}/.local/bin/hermes"
    fi
}

#
# @description Remove the user-facing Hermes command symlink before installation.
#
function prepare_hermes_command_link() {
    local command_link

    command_link="$(hermes_command_link)"
    if [ -L "${command_link}" ]; then
        rm -f "${command_link}"
    fi
}

#
# @description Install Hermes Agent without running the interactive setup flow.
#
function install_hermes() {
    prepare_hermes_command_link

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
