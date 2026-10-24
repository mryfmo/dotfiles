#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/tailscale.sh"

load "../../helpers/apt_record"

function setup() {
    source "${SCRIPT_PATH}"
}

# Only a case that installed for real removes what it installed (U41): before, every case ran
# the installer's uninstall function (removed in U46), and the array cases' teardown removed the runner image's own packages.
function teardown() {
    remove_real_packages
}

@test "[ubuntu-client] tailscale" {
    # install/ubuntu/client/tailscale.sh has no PACKAGES array; it installs this one package.
    install_real_packages tailscale

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
