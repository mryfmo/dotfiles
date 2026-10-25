#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/common/gh_extensions.sh"

@test "[common] gh_extensions installs extensions when authenticated" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        activate_mise() { :; }
        gh() {
            if [ "$1 $2" = "auth status" ]; then
                return 0
            fi
            printf "%s\n" "$*"
        }
        main
    '

    [ "${status}" -eq 0 ]
    [ "${output}" = "extension install seachicken/gh-poi --pin $(sed -n 's/^GH_POI_PIN_VERSION="\(.*\)"$/\1/p' "${SCRIPT_PATH}")" ]
}

@test "[common] gh_extensions skips login and extensions when unauthenticated" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        activate_mise() { :; }
        gh() {
            if [ "$1 $2" = "auth status" ]; then
                return 1
            fi
            printf "unexpected: %s\n" "$*"
            return 99
        }
        main
    '

    [ "${status}" -eq 0 ]
    [[ "${output}" == *"Run setup-gh, then make update"* ]]
    [[ "${output}" != *"unexpected:"* ]]
}

@test "[common] gh_extensions keeps an extension at its pinned tag unchanged" {
    export XDG_DATA_HOME="${BATS_TEST_TMPDIR}/data"
    mkdir -p "${XDG_DATA_HOME}/gh/extensions/gh-poi"
    printf 'tag: %s\nispinned: true\n' "$(sed -n 's/^GH_POI_PIN_VERSION="\(.*\)"$/\1/p' "${SCRIPT_PATH}")" \
        > "${XDG_DATA_HOME}/gh/extensions/gh-poi/manifest.yml"
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        activate_mise() { :; }
        gh() {
            case "$1 $2" in
                "auth status") return 0 ;;
                "extension list") printf "gh poi\tseachicken/gh-poi\t%s\n" "${GH_POI_PIN_VERSION}" ;;
                *) printf "unexpected: %s\n" "$*"; return 99 ;;
            esac
        }
        main
    '

    [ "${status}" -eq 0 ]
    [ -z "${output}" ]
}

@test "[common] gh_extensions reinstalls an unpinned extension at its tag with --pin" {
    export XDG_DATA_HOME="${BATS_TEST_TMPDIR}/data"
    mkdir -p "${XDG_DATA_HOME}/gh/extensions/gh-poi"
    printf 'ispinned: false\n' > "${XDG_DATA_HOME}/gh/extensions/gh-poi/manifest.yml"
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        activate_mise() { :; }
        gh() {
            case "$1 $2" in
                "auth status") return 0 ;;
                "extension list") printf "gh poi\tseachicken/gh-poi\t%s\n" "${GH_POI_PIN_VERSION}" ;;
                *) printf "%s\n" "$*" ;;
            esac
        }
        main
    '

    [ "${status}" -eq 0 ]
    [ "${lines[1]}" = "extension remove gh-poi" ]
    [[ "${lines[2]}" == "extension install seachicken/gh-poi --pin "* ]]
}

@test "[common] gh_extensions reinstalls an extension at another tag at its pin" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        activate_mise() { :; }
        gh() {
            case "$1 $2" in
                "auth status") return 0 ;;
                "extension list") printf "gh poi\tseachicken/gh-poi\tv0.0.1\n" ;;
                *) printf "%s\n" "$*" ;;
            esac
        }
        main
        printf "pin=%s\n" "${GH_POI_PIN_VERSION}"
    '

    [ "${status}" -eq 0 ]
    pin="${lines[3]#pin=}"
    [ "${lines[1]}" = "extension remove gh-poi" ]
    [ "${lines[2]}" = "extension install seachicken/gh-poi --pin ${pin}" ]
}

@test "[common] gh_extensions changes nothing when the extension list cannot be read" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        activate_mise() { :; }
        gh() {
            case "$1 $2" in
                "auth status") return 0 ;;
                "extension list") return 1 ;;
                *) printf "unexpected: %s\n" "$*"; return 99 ;;
            esac
        }
        main
    '

    [ "${status}" -ne 0 ]
    [[ "${output}" == *"gh extension list failed"* ]]
    [[ "${output}" != *"unexpected:"* ]]
}

@test "[common] gh_extensions refuses when mise activate fails, before any gh call" {
    export HOME="${BATS_TEST_TMPDIR}/home"
    mkdir -p "${HOME}/.local/bin"
    printf '#!/bin/sh\necho "mise: broken" >&2\nexit 3\n' > "${HOME}/.local/bin/mise"
    chmod +x "${HOME}/.local/bin/mise"

    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        gh() { printf "unexpected: %s\n" "$*"; }
        main
    '

    [ "${status}" -ne 0 ]
    grep -qF -- "${HOME}/.local/bin/mise activate bash failed; gh extensions were not installed." <<< "${output}"
    if grep -qF -- "unexpected:" <<< "${output}"; then
        false
    fi
}
