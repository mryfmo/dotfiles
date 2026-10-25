#!/usr/bin/env bash

# @file install/ubuntu/client/docker.sh
# @brief Install Docker Engine on Ubuntu client machines.
# @description
#   Follows https://docs.docker.com/engine/install/ubuntu/: removes the
#   distribution packages that conflict with Docker Engine, configures Docker's
#   apt repository (docker.asc key, deb822 docker.sources), and installs Docker
#   Engine with the buildx and compose plugins.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly PACKAGES=(
    docker-ce
    docker-ce-cli
    containerd.io
    docker-buildx-plugin
    docker-compose-plugin
)

#
# @description Remove legacy Docker packages that conflict with Docker Engine.
#
function uninstall_old_docker() {
    local packages=(
        "docker.io"
        "docker-compose"
        "docker-compose-v2"
        "docker-doc"
        "docker-buildx"
        "podman-docker"
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

    # Docker's ASCII-armored key and a deb822 source. The one-line docker.list and the dearmored docker.gpg
    # an earlier version of this script wrote are removed first: two sources for one URI with different
    # Signed-By keys make apt refuse to update.
    sudo rm -f /etc/apt/sources.list.d/docker.list /etc/apt/keyrings/docker.gpg
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    printf '%s\n' \
        "Types: deb" \
        "URIs: https://download.docker.com/linux/ubuntu" \
        "Suites: ${codename}" \
        "Components: stable" \
        "Architectures: ${arch}" \
        "Signed-By: /etc/apt/keyrings/docker.asc" | sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null
}

#
# @description Install Docker Engine and the configured companion packages.
#
function install_docker_engine() {
    # Update the apt package index:
    sudo apt-get update

    # Install Docker Engine, containerd, and the buildx and compose plugins.
    sudo apt-get install -y "${PACKAGES[@]}"

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
