#!/usr/bin/env bash

# @file install/ubuntu/common/ssh.sh
# @brief Install the OpenSSH client on Ubuntu.
# @description
#   Installs or removes the Ubuntu OpenSSH client package while preserving
#   proxy-related environment variables.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly PACKAGES=(
    openssh-client
)

# GitHub-published key fingerprint: SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU
readonly GITHUB_HOST_KEY='github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl'

#
# @description Install the OpenSSH client package.
#
function install_openssh() {
    sudo --preserve-env=http_proxy,https_proxy,no_proxy apt-get install -y "${PACKAGES[@]}"
}

#
# @description Add GitHub's published SSH host key to the current user's known hosts.
#
function install_github_host_key() {
    local ssh_dir="${HOME}/.ssh"
    local known_hosts="${ssh_dir}/known_hosts"

    install -d -m 700 "${ssh_dir}"
    touch "${known_hosts}"
    chmod 600 "${known_hosts}"
    grep -Fqx "${GITHUB_HOST_KEY}" "${known_hosts}" || printf '%s\n' "${GITHUB_HOST_KEY}" >> "${known_hosts}"
}

#
# @description Remove the OpenSSH client package.
#
function uninstall_openssh() {
    sudo apt-get remove -y "${PACKAGES[@]}"
}

#
# @description Run the OpenSSH client installation flow.
#
function main() {
    install_openssh
    install_github_host_key
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
