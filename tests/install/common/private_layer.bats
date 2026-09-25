#!/usr/bin/env bats

readonly SCRIPT_PATH="./scripts/check-tools.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

@test "[common] private_layer_enabled defaults to true when usePrivate is absent" {
    function chezmoi() { printf '{"system":"client"}\n'; }
    function jq() { command jq "$@"; }

    run private_layer_enabled
    [ "${status}" -eq 0 ]
}

@test "[common] private_layer_enabled honors an explicit usePrivate=false" {
    function chezmoi() { printf '{"usePrivate":false}\n'; }
    function jq() { command jq "$@"; }

    run private_layer_enabled
    [ "${status}" -eq 1 ]
}

@test "[common] private_layer_enabled honors an explicit usePrivate=true" {
    function chezmoi() { printf '{"usePrivate":true}\n'; }
    function jq() { command jq "$@"; }

    run private_layer_enabled
    [ "${status}" -eq 0 ]
}

@test "[common] private_layer_enabled defaults to true when chezmoi is unavailable" {
    function command() {
        if [ "$1" = "-v" ] && [ "$2" = "chezmoi" ]; then
            return 1
        fi
        builtin command "$@"
    }

    run private_layer_enabled
    [ "${status}" -eq 0 ]
}

@test "[common] check_private_chezmoi reports not applicable when usePrivate is false" {
    function private_layer_enabled() { return 1; }

    run check_private_chezmoi
    [ "${status}" -eq 0 ]
    [[ "${output}" == *"not applicable: private layer (usePrivate=false)"* ]]
}
