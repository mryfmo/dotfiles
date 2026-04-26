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
# @description Install Hermes Agent without running the interactive setup flow.
#
function install_hermes() {
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
