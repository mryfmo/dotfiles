#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/tailscale.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

function teardown() {
    u41_mark teardown-start
    run uninstall_tailscale
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

@test "[ubuntu-client] tailscale" {
    u41_install

    run dpkg -s 'tailscale'
    [ "${status}" -eq 0 ]
}

@test "[ubuntu-client] setup_repository writes a codename-scoped keyring and sources entry" {
    local calls_path="${BATS_TEST_TMPDIR}/tailscale-repository-calls.txt"

    run env CALLS_PATH="${calls_path}" bash -c '
        source "'"${SCRIPT_PATH}"'"
        curl() {
            printf "tailscale signing material\n"
        }
        dpkg() {
            printf "arm64\n"
        }
        lsb_release() {
            printf "noble\n"
        }
        sudo() {
            printf "%s\n" "$*" >> "${CALLS_PATH}"
            if [ "$1" = "tee" ]; then
                cat > /dev/null
            fi
        }

        setup_repository
        setup_repository
    '

    [ "${status}" -eq 0 ]
    [ "$(grep -c '^mkdir -p /usr/share/keyrings$' "${calls_path}")" -eq 2 ]
    [ "$(grep -c '^tee /usr/share/keyrings/tailscale-archive-keyring.gpg$' "${calls_path}")" -eq 2 ]
    [ "$(grep -c '^tee /etc/apt/sources.list.d/tailscale.list$' "${calls_path}")" -eq 2 ]
}
