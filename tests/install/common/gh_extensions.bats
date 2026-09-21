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
    [[ "${output}" == *"Run setup-gh, then rerun chezmoi apply"* ]]
    [[ "${output}" != *"unexpected:"* ]]
}
