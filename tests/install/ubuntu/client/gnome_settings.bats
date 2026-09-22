#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/ubuntu/client/gnome_settings.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

@test "[ubuntu-client] main is a no-op without gsettings on PATH" {
    run env PATH="${BATS_TEST_TMPDIR}" DISPLAY=":0" /bin/bash "${SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
}

@test "[ubuntu-client] main is a no-op headless even when gsettings exists" {
    local bin_dir="${BATS_TEST_TMPDIR}/bin"
    mkdir -p "${bin_dir}"
    printf '#!/bin/sh\necho "gsettings should not run" >&2\nexit 99\n' > "${bin_dir}/gsettings"
    chmod +x "${bin_dir}/gsettings"

    run env PATH="${bin_dir}" DISPLAY="" DBUS_SESSION_BUS_ADDRESS="" /bin/bash "${SCRIPT_PATH}"
    [ "${status}" -eq 0 ]
}

@test "[ubuntu-client] gset skips a key whose schema is not writable" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        gsettings() {
            if [ "$1" = writable ]; then
                echo false
                return 1
            fi
            echo "gsettings set should not run" >&2
            exit 99
        }
        gset org.example.nonexistent some-key value
    '
    [ "${status}" -eq 0 ]
}

@test "[ubuntu-client] gset applies a key whose schema is writable" {
    local calls_path="${BATS_TEST_TMPDIR}/gsettings-calls.txt"

    run env CALLS_PATH="${calls_path}" bash -c '
        source "'"${SCRIPT_PATH}"'"
        gsettings() {
            if [ "$1" = writable ]; then
                echo true
                return 0
            fi
            printf "%s\n" "$*" >> "${CALLS_PATH}"
        }
        gset org.gnome.desktop.peripherals.touchpad tap-to-click true
    '
    [ "${status}" -eq 0 ]
    [ "$(cat "${calls_path}")" = "set org.gnome.desktop.peripherals.touchpad tap-to-click true" ]
}

@test "[ubuntu-client] main applies every ported default when gsettings is available and writable" {
    local calls_path="${BATS_TEST_TMPDIR}/gsettings-calls.txt"

    run env CALLS_PATH="${calls_path}" DISPLAY=":0" bash -c '
        source "'"${SCRIPT_PATH}"'"
        gsettings() {
            if [ "$1" = writable ]; then
                echo true
                return 0
            fi
            printf "%s\n" "$*" >> "${CALLS_PATH}"
        }
        main
    '
    [ "${status}" -eq 0 ]
    grep -qF "set org.gnome.desktop.peripherals.keyboard repeat-interval 30" "${calls_path}"
    grep -qF "set org.gnome.desktop.peripherals.touchpad tap-to-click true" "${calls_path}"
    grep -qF "set org.gnome.desktop.input-sources sources [('xkb','us'),('ibus','mozc-jp')]" "${calls_path}"
}
