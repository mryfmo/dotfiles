#!/usr/bin/env bash

# @file install/ubuntu/server/ssh_server.sh
# @brief Install and configure an Ubuntu SSH server.
# @description
#   Installs `openssh-server`, configures it for the repository's Docker test
#   container, and starts the SSH service. The script is container-only: it
#   refuses to run (exit 1) unless `/.dockerenv` exists, so a server-role apply
#   on a real host never reconfigures that host's sshd. Root login keeps the
#   distribution default `prohibit-password` and sshd keeps its default listen
#   addresses.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

declare -r SSH_PORT="${DOTFILES_SERVER_SSH_PORT:-22}"

#
# @description Install the Ubuntu OpenSSH server package and its prerequisites.
#
function install_openssh_server() {
    # install openssh-server and vim
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install --no-install-recommends -y \
        vim \
        openssh-server
}

#
# @description Merge proxy-related variables into `AcceptEnv` in `sshd_config`.
#
function configure_accept_env() {
    local current add merged

    # Get existing AcceptEnv values (empty if not set)
    current=$(grep '^AcceptEnv' /etc/ssh/sshd_config | sed 's/^AcceptEnv //')

    # Variables to append
    add="HTTP_PROXY HTTPS_PROXY NO_PROXY http_proxy https_proxy no_proxy"

    # Merge and remove duplicates
    merged=$(echo "$current $add" | tr ' ' '\n' | sort -u | tr '\n' ' ')

    # Remove existing entries and keep a single AcceptEnv line
    sudo sed -i '/^AcceptEnv/d' /etc/ssh/sshd_config
    echo "AcceptEnv $merged" | sudo tee -a /etc/ssh/sshd_config
}

#
# @description Configure `sshd` for the repository's container-oriented setup.
#
function setup_sshd() {
    sudo mkdir -p /var/run/sshd
    mkdir -p "${HOME}/.ssh"

    sudo sed -i "s/^#\?Port .*/Port ${SSH_PORT}/" /etc/ssh/sshd_config &&
        sudo sed -i 's/^#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config &&
        sudo sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

    configure_accept_env

    # check the /etc/ssh/sshd_config
    sudo /usr/sbin/sshd -t

    # create .ssh/authorized_keys if not exists
    touch "${HOME}/.ssh/authorized_keys"
}

#
# @description Start the SSH service after configuration has been validated.
#
function run_sshd() {
    # run sshd
    sudo /usr/sbin/service ssh start
}

#
# @description Install, configure, and start the Ubuntu SSH server.
#
function main() {
    install_openssh_server
    setup_sshd
    run_sshd
}

#
# @description Return success when the script runs inside a Docker container.
#
function in_container() {
    [ -f "/.dockerenv" ]
}

#
# @description Run `main` only inside a container; fail closed anywhere else.
# @exitcode 1 When `/.dockerenv` is absent (not a Docker container).
#
function run_in_container_only() {
    if ! in_container; then
        echo "ssh_server.sh: refusing to configure sshd outside a Docker container (/.dockerenv not found)" >&2
        return 1
    fi
    main
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_in_container_only
fi
