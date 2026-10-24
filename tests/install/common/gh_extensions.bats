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
    [ "${output}" = "extension install seachicken/gh-poi" ]
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

@test "[common] gh_extensions keeps installed extensions unchanged" {
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        activate_mise() { :; }
        gh() {
            case "$1 $2" in
                "auth status") return 0 ;;
                "extension list") printf "gh poi\tseachicken/gh-poi\tv0.18.4\n" ;;
                *) printf "unexpected: %s\n" "$*"; return 99 ;;
            esac
        }
        main
    '

    [ "${status}" -eq 0 ]
    [ -z "${output}" ]
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
