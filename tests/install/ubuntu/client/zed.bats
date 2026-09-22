#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/zed.sh"
readonly PINS_PATH="./scripts/lib/installer-pins.sh"

function setup() {
    source "${PINS_PATH}"
    source "${SCRIPT_PATH}"
}

@test "[ubuntu-client] zed_artifact selects the pinned checksum for the current architecture" {
    run bash -c '
        source "'"${PINS_PATH}"'"
        source "'"${SCRIPT_PATH}"'"
        uname() { [ "$1" = -m ] && printf x86_64 || command uname "$1"; }
        zed_artifact
    '
    [ "${status}" -eq 0 ]
    [ "${lines[0]}" = "zed-linux-x86_64.tar.gz" ]
    [ "${lines[1]}" = "${ZED_LINUX_AMD64_SHA256}" ]
}

@test "[ubuntu-client] zed_artifact rejects an unsupported architecture" {
    run bash -c '
        source "'"${PINS_PATH}"'"
        source "'"${SCRIPT_PATH}"'"
        uname() { [ "$1" = -m ] && printf riscv64 || command uname "$1"; }
        zed_artifact
    '
    [ "${status}" -ne 0 ]
}

@test "[ubuntu-client] main downloads, verifies, and links zed when not already installed" {
    run env HOME="${BATS_TEST_TMPDIR}" bash -c '
        source "'"${PINS_PATH}"'"
        source "'"${SCRIPT_PATH}"'"
        curl() {
            local output
            while [ "$#" -gt 0 ]; do
                if [ "$1" = -o ]; then output="$2"; shift 2; else shift; fi
            done
            mkdir -p "${BATS_TEST_TMPDIR}/tar-src/zed.app/bin"
            printf "#!/bin/sh\necho Zed %s deadbeef\n" "${ZED_PIN_VERSION#v}" > "${BATS_TEST_TMPDIR}/tar-src/zed.app/bin/zed"
            chmod +x "${BATS_TEST_TMPDIR}/tar-src/zed.app/bin/zed"
            tar -czf "${output}" -C "${BATS_TEST_TMPDIR}/tar-src" zed.app
        }
        main
        [ -L "${HOME}/.local/bin/zed" ]
        [ -x "${HOME}/.local/bin/zed" ]
    '
    [ "${status}" -eq 0 ]
}

@test "[ubuntu-client] main is a no-op when the pinned version is already installed" {
    local app_dir="${BATS_TEST_TMPDIR}/.local/share/zed.app"
    mkdir -p "${app_dir}/bin" "${BATS_TEST_TMPDIR}/.local/bin"
    printf '#!/bin/sh\necho "Zed %s deadbeef"\n' "${ZED_PIN_VERSION#v}" > "${app_dir}/bin/zed"
    chmod +x "${app_dir}/bin/zed"
    ln -s "${app_dir}/bin/zed" "${BATS_TEST_TMPDIR}/.local/bin/zed"

    run env HOME="${BATS_TEST_TMPDIR}" bash -c '
        source "'"${PINS_PATH}"'"
        source "'"${SCRIPT_PATH}"'"
        curl() { echo "curl should not run" >&2; exit 99; }
        main
    '
    [ "${status}" -eq 0 ]
}
