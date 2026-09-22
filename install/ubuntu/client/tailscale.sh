#!/usr/bin/env bash

# @file install/ubuntu/client/tailscale.sh
# @brief Install Tailscale on Ubuntu client machines from the official apt repository.
# @description
#   Configures Tailscale's official apt repository (codename-scoped signing
#   key + sources entry, mirroring docker.sh's keyring setup) and installs
#   the tailscale package. `tailscale up` (interactive login) stays manual.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly TAILSCALE_KEYRING="/usr/share/keyrings/tailscale-archive-keyring.gpg"
readonly TAILSCALE_SOURCES_LIST="/etc/apt/sources.list.d/tailscale.list"

#
# @description Configure Tailscale's official apt repository and signing key.
#
function setup_repository() {
    local codename
    codename="$(lsb_release -cs)"

    sudo mkdir -p /usr/share/keyrings
    # Tailscale publishes this key pre-dearmored (raw binary), unlike Docker's
    # ASCII-armored key, so no `gpg --dearmor` step is needed here.
    curl -fsSL "https://pkgs.tailscale.com/stable/ubuntu/${codename}.noarmor.gpg" | sudo tee "${TAILSCALE_KEYRING}" > /dev/null

    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=${TAILSCALE_KEYRING}] https://pkgs.tailscale.com/stable/ubuntu ${codename} main" |
        sudo tee "${TAILSCALE_SOURCES_LIST}" > /dev/null
}

#
# @description Install the tailscale package.
#
function install_tailscale() {
    sudo apt-get update
    sudo apt-get install -y tailscale
}

#
# @description Remove the tailscale package.
#
function uninstall_tailscale() {
    sudo apt-get remove -y tailscale
}

#
# @description Install Tailscale from its official Ubuntu apt repository.
#
function main() {
    setup_repository
    install_tailscale
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
