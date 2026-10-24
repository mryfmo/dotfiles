#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/docker.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

function teardown() {
    u41_mark teardown-start
    run uninstall_docker_engine
    u41_teardown_summary
    u41_mark teardown-end
}

# U41 MEASUREMENT (temporary, removed before review): fd-3 markers GitHub timestamps.
function u41_mark() { printf '# U41 %s | %s\n' "$1" "${BATS_TEST_DESCRIPTION}" >&3; }
function u41_teardown_summary() {
    printf '# U41 teardown-status %s removed %s: %s | %s\n' "${status}" "$(grep -c '^Removing ' <<< "${output}")" \
        "$(grep '^Removing ' <<< "${output}" | awk '{print $2}' | tr '\n' ' ')" "${BATS_TEST_DESCRIPTION}" >&3
}
function u41_install() {
    local log="${BATS_TEST_TMPDIR}/u41-install.log"
    u41_mark body-install-start
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}" > "${log}" 2>&1 || { sed 's/^/# /' "${log}" >&3; return 1; }
    u41_mark body-install-end
    grep -E '^(Need to get|Fetched|After this operation|[0-9]+ upgraded)' "${log}" | sed 's/^/# U41 apt: /' >&3 || true
}

@test "[ubuntu-client] docker" {
    u41_install

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
