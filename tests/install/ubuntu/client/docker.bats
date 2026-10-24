#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/docker.sh"

load "../../helpers/apt_record"

function setup() {
    source "${SCRIPT_PATH}"
}

# Only a case that installed for real removes what it installed (U41): before, every case ran
# uninstall_docker_engine, and the array cases' teardown removed the runner image's own packages.
function teardown() {
    remove_real_packages
}

@test "[ubuntu-client] docker" {
    install_real_packages "${PACKAGES[@]}"

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

@test "[ubuntu-client] install_docker_engine asks apt-get for every package in PACKAGES at once" {
    run record_apt_calls "${SCRIPT_PATH}" install_docker_engine
    [ "${status}" -eq 0 ]
    [ "$(grep -c '^apt-get install ' <<< "${output}")" -eq 1 ]
    grep -qxF "apt-get install -y ${PACKAGES[*]}" <<< "${output}"
}

@test "[ubuntu-client] the recorded install_docker_engine call catches an installer that drops a package" {
    local mutant="${BATS_TEST_TMPDIR}/docker.sh" calls
    sed 's/apt-get install -y "${PACKAGES\[@\]}"/apt-get install -y "${PACKAGES[@]:1}"/' "${SCRIPT_PATH}" > "${mutant}"
    if cmp -s "${SCRIPT_PATH}" "${mutant}"; then
        false
    fi
    run record_apt_calls "${mutant}" install_docker_engine
    [ "${status}" -eq 0 ]
    calls="${output}"
    # The recorder saw the mutant's call, and the check above would refuse it.
    grep -qxF "apt-get install -y ${PACKAGES[*]:1}" <<< "${calls}"
    if grep -qxF "apt-get install -y ${PACKAGES[*]}" <<< "${calls}"; then
        false
    fi
}

@test "[ubuntu-client] setup_repository writes no repository when dpkg or lsb_release cannot be read" {
    local producer
    for producer in dpkg lsb_release; do
        local calls_path="${BATS_TEST_TMPDIR}/docker-${producer}-calls.txt"

        run env CALLS_PATH="${calls_path}" FAILING="${producer}" bash -c '
            source "'"${SCRIPT_PATH}"'"
            curl() { printf "docker signing key\n"; }
            dpkg() { [ "${FAILING}" != dpkg ] && printf "amd64\n"; }
            lsb_release() { [ "${FAILING}" != lsb_release ] && printf "noble\n"; }
            sudo() {
                printf "%s\n" "$*" >> "${CALLS_PATH}"
                if [ "$1" = "gpg" ] || [ "$1" = "tee" ]; then
                    cat > /dev/null
                fi
            }

            setup_repository
        '

        [ "${status}" -eq 1 ]
        grep -qE -- "^${producer} .* failed; the Docker repository was not configured$" <<< "${output}"
        if grep -qE '^(tee /etc/apt/sources.list.d/docker.list|gpg )' "${calls_path}"; then
            false
        fi
    done
}

@test "[ubuntu-client] configure_docker_group adds no user when id cannot name the user" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        id() { return 1; }
        sudo() { printf "unexpected: sudo %s\n" "$*"; }

        configure_docker_group
    '

    [ "${status}" -eq 1 ]
    [ "${output}" = "id -un failed; no user was added to the docker group" ]
}
