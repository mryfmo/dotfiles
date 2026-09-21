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
