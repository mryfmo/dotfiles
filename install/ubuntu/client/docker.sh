#!/usr/bin/env bash

# @file install/ubuntu/client/docker.sh
# @brief Install Docker Engine on Ubuntu client machines.
# @description
#   Removes legacy Docker packages, configures Docker's apt repository, and
#   installs the current Docker Engine packages.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly PACKAGES=(
    docker-ce
    docker-ce-cli
    containerd.io
    docker-compose-plugin
)

#
# @description Remove legacy Docker packages that conflict with Docker Engine.
#
function uninstall_old_docker() {
    local packages=(
        "docker"
        "docker-engine"
        "docker.io"
        "containerd"
        "runc"
    )
    for package in "${packages[@]}"; do
        if dpkg -s "${package}" > /dev/null 2>&1; then
            sudo apt-get remove -y "${package}"
        fi
    done
}

#
# @description Configure Docker's official apt repository and signing key.
#
function setup_repository() {

    # Update the apt package index and install packages to allow apt to use a repository over HTTPS:
    sudo apt-get update
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    local arch codename
    arch="$(dpkg --print-architecture)" || {
        echo "dpkg --print-architecture failed; the Docker repository was not configured" >&2
        return 1
    }
    codename="$(lsb_release -cs)" || {
        echo "lsb_release -cs failed; the Docker repository was not configured" >&2
        return 1
    }

    # Add Docker’s official GPG key:
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --batch --yes --dearmor -o /etc/apt/keyrings/docker.gpg

    # Use the following command to set up the repository:
    echo \
        "deb [arch=${arch} signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        ${codename} stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
}

#
# @description Install Docker Engine and the configured companion packages.
#
function install_docker_engine() {
    # Update the apt package index:
    sudo apt-get update

    # Install Docker Engine, containerd, and Docker Compose.
    sudo apt-get install -y "${PACKAGES[@]}"

}

#
# @description Remove the configured Docker Engine packages.
#
function uninstall_docker_engine() {
    sudo apt-get remove -y "${PACKAGES[@]}"
}

#
# @description Add the current user to the docker group so docker can run without sudo.
#
function configure_docker_group() {
    local user
    user="$(id -un)" || {
        echo "id -un failed; no user was added to the docker group" >&2
        return 1
    }
    sudo usermod -aG docker "${user}"
}

#
# @description Install Docker Engine from Docker's official Ubuntu repository.
#
function main() {
    uninstall_old_docker
    setup_repository
    install_docker_engine
    configure_docker_group
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
