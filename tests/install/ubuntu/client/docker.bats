#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/docker.sh"

load "../../helpers/apt_record"

function setup() {
    source "${SCRIPT_PATH}"
}

# Only a case that installed for real removes what it installed (U41): before, every case ran
# the installer's uninstall function (removed in U46), and the array cases' teardown removed the runner image's own packages.
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
    run dpkg -s 'docker-buildx-plugin'
    [ "${status}" -eq 0 ]
    run dpkg -s 'docker-compose-plugin'
    [ "${status}" -eq 0 ]

    run getent group docker
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"$(id -un)"* ]]
}

@test "[ubuntu-client] setup_repository writes docker.asc and a deb822 docker.sources and drops the legacy files" {
    local calls_path="${BATS_TEST_TMPDIR}/docker-repository-calls.txt"
    local sources_path="${BATS_TEST_TMPDIR}/docker.sources"

    run env CALLS_PATH="${calls_path}" SOURCES_PATH="${sources_path}" bash -c '
        source "'"${SCRIPT_PATH}"'"
        dpkg() {
            printf "amd64\n"
        }
        lsb_release() {
            printf "noble\n"
        }
        sudo() {
            printf "%s\n" "$*" >> "${CALLS_PATH}"
            if [ "$1" = "tee" ]; then
                cat > "${SOURCES_PATH}"
            fi
        }

        setup_repository
    '

    [ "${status}" -eq 0 ]
    grep -qxF 'rm -f /etc/apt/sources.list.d/docker.list /etc/apt/keyrings/docker.gpg' "${calls_path}"
    grep -qxF 'curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc' "${calls_path}"
    grep -qxF 'tee /etc/apt/sources.list.d/docker.sources' "${calls_path}"
    grep -qxF 'Types: deb' "${sources_path}"
    grep -qxF 'URIs: https://download.docker.com/linux/ubuntu' "${sources_path}"
    grep -qxF 'Suites: noble' "${sources_path}"
    grep -qxF 'Components: stable' "${sources_path}"
    grep -qxF 'Architectures: amd64' "${sources_path}"
    grep -qxF 'Signed-By: /etc/apt/keyrings/docker.asc' "${sources_path}"
    if grep -qE '(gpg --dearmor|sources.list.d/docker.list$)' <(grep -v '^rm -f ' "${calls_path}"); then
        false
    fi
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
            dpkg() { [ "${FAILING}" != dpkg ] && printf "amd64\n"; }
            lsb_release() { [ "${FAILING}" != lsb_release ] && printf "noble\n"; }
            sudo() {
                printf "%s\n" "$*" >> "${CALLS_PATH}"
                if [ "$1" = "tee" ]; then
                    cat > /dev/null
                fi
            }

            setup_repository
        '

        [ "${status}" -eq 1 ]
        grep -qE -- "^${producer} .* failed; the Docker repository was not configured$" <<< "${output}"
        if grep -qE '^(tee /etc/apt/sources.list.d/docker.sources|curl )' "${calls_path}"; then
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

# uninstall_old_docker has no install_* counterpart: main calls it first, to remove the distribution's Docker
# packages that conflict with Docker's own (docs.docker.com/engine/install/ubuntu, "Uninstall old versions").
# The list below is that set; the cases check it is removed whole, one package per call, and never a package
# install_docker_engine installs.
@test "[ubuntu-client] uninstall_old_docker removes each installed legacy package and none of PACKAGES" {
    local removed installed

    run record_apt_calls "${SCRIPT_PATH}" uninstall_old_docker installed
    [ "${status}" -eq 0 ]
    [ "$(grep -c '^apt-get remove -y [^ ]*$' <<< "${output}")" -eq 8 ]
    removed="$(apt_call_packages remove <<< "${output}")"
    [ "${removed}" = "$(printf '%s\n' docker.io docker-compose docker-compose-v2 docker-doc docker-buildx podman-docker containerd runc)" ]

    run record_apt_calls "${SCRIPT_PATH}" install_docker_engine
    [ "${status}" -eq 0 ]
    installed="$(apt_call_packages install <<< "${output}")"
    [ -n "${installed}" ]
    run grep -xF -f <(printf '%s\n' "${installed}") <<< "${removed}"
    [ "${status}" -eq 1 ]

    run record_apt_calls "${SCRIPT_PATH}" uninstall_old_docker missing
    [ "${status}" -eq 0 ]
    [ -z "${output}" ]
}

@test "[ubuntu-client] the recorded uninstall_old_docker call catches an uninstaller that drops a package" {
    local mutant="${BATS_TEST_TMPDIR}/docker-old.sh" removed
    sed '/^        "runc"$/d' "${SCRIPT_PATH}" > "${mutant}"
    if cmp -s "${SCRIPT_PATH}" "${mutant}"; then
        false
    fi

    run record_apt_calls "${mutant}" uninstall_old_docker installed
    [ "${status}" -eq 0 ]
    removed="$(apt_call_packages remove <<< "${output}")"

    # The recorder saw the mutant's calls, and the comparison above would refuse them.
    [ "${removed}" = "$(printf '%s\n' docker.io docker-compose docker-compose-v2 docker-doc docker-buildx podman-docker containerd)" ]
    [ "${removed}" != "$(printf '%s\n' docker.io docker-compose docker-compose-v2 docker-doc docker-buildx podman-docker containerd runc)" ]
}
