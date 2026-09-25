#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/docker.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

function teardown() {
    run uninstall_docker_engine
}

@test "[ubuntu-client] docker" {
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"

    run dpkg -s 'docker-ce'
    [ "${status}" -eq 0 ]
    run dpkg -s 'docker-ce-cli'
    [ "${status}" -eq 0 ]
    run dpkg -s 'containerd.io'
    [ "${status}" -eq 0 ]
    run dpkg -s 'docker-compose-plugin'
    [ "${status}" -eq 0 ]

    run getent group docker
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"$(id -un)"* ]]
}

@test "[ubuntu-client] setup_repository replaces an existing keyring non-interactively" {
    local calls_path="${BATS_TEST_TMPDIR}/docker-repository-calls.txt"

    run env CALLS_PATH="${calls_path}" bash -c '
        source "'"${SCRIPT_PATH}"'"
        curl() {
            printf "docker signing key\n"
        }
        dpkg() {
            printf "amd64\n"
        }
        lsb_release() {
            printf "noble\n"
        }
        sudo() {
            printf "%s\n" "$*" >> "${CALLS_PATH}"
            if [ "$1" = "gpg" ] || [ "$1" = "tee" ]; then
                cat > /dev/null
            fi
        }

        setup_repository
        setup_repository
    '

    [ "${status}" -eq 0 ]
    [ "$(grep -c '^gpg --batch --yes --dearmor -o /etc/apt/keyrings/docker.gpg$' "${calls_path}")" -eq 2 ]
}
