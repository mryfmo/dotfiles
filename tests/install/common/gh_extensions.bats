#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/common/gh_extensions.sh"

#
# @description Point every directory agent_home and gh resolve into this test's scratch tree. GH_DATA_DIR beats
#   XDG_DATA_HOME, so an inherited one would let a fake install move or delete the operator's real extensions.
#
setup() {
    export HOME="${BATS_TEST_TMPDIR}/home"
    export XDG_DATA_HOME="${BATS_TEST_TMPDIR}/data"
    export GH_DATA_DIR="${XDG_DATA_HOME}/gh"
    export GH_CONFIG_DIR="${HOME}/.config/gh"
    export CLAUDE_CONFIG_DIR="${HOME}/.claude"
    export CODEX_HOME="${HOME}/.codex"
    mkdir -p "${HOME}"
}

@test "[common] gh_extensions installs extensions when authenticated" {
    # No installed copy: setup points GH_DATA_DIR into the scratch tree.
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
    printf 'owner: seachicken\nname: gh-poi\nhost: github.com\ntag: %s\nispinned: true\npath: %s\n' \
        "$(sed -n 's/^GH_POI_PIN_VERSION="\(.*\)"$/\1/p' "${SCRIPT_PATH}")" "${XDG_DATA_HOME}/gh/extensions/gh-poi/gh-poi" \
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
    printf 'owner: seachicken\nname: gh-poi\nhost: github.com\ntag: %s\nispinned: false\npath: %s\n' \
        "$(sed -n 's/^GH_POI_PIN_VERSION="\(.*\)"$/\1/p' "${SCRIPT_PATH}")" "${XDG_DATA_HOME}/gh/extensions/gh-poi/gh-poi" \
        > "${XDG_DATA_HOME}/gh/extensions/gh-poi/manifest.yml"
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
    [[ "${lines[1]}" == "extension install seachicken/gh-poi --pin "* ]]
    [[ "${output}" != *"extension remove"* ]]
}

@test "[common] gh_extensions reinstalls an extension at another tag at its pin" {
    export XDG_DATA_HOME="${BATS_TEST_TMPDIR}/data"
    # gh's record of the installed copy: pinned, but at another tag than the pin.
    mkdir -p "${XDG_DATA_HOME}/gh/extensions/gh-poi"
    printf 'owner: seachicken\nname: gh-poi\nhost: github.com\ntag: v0.0.1\nispinned: true\npath: %s\n' \
        "${XDG_DATA_HOME}/gh/extensions/gh-poi/gh-poi" > "${XDG_DATA_HOME}/gh/extensions/gh-poi/manifest.yml"
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
    [ "${#lines[@]}" -eq 3 ]
    pin="${lines[2]#pin=}"
    [ "${lines[0]}" = "seachicken/gh-poi is v0.0.1 true (listed at v0.0.1); reinstalling it pinned at ${pin}." ]
    [ "${lines[1]}" = "extension install seachicken/gh-poi --pin ${pin}" ]
}

@test "[common] gh_extensions restores the previous copy when the pinned install fails" {
    export XDG_DATA_HOME="${BATS_TEST_TMPDIR}/data"
    mkdir -p "${XDG_DATA_HOME}/gh/extensions/gh-poi"
    printf 'old\n' > "${XDG_DATA_HOME}/gh/extensions/gh-poi/gh-poi"
    run bash -c '
        source "'"${SCRIPT_PATH}"'"
        activate_mise() { :; }
        gh() {
            case "$1 $2" in
                "auth status") return 0 ;;
                "extension list") printf "gh poi\tseachicken/gh-poi\tv0.0.1\n" ;;
                "extension install") mkdir -p "${XDG_DATA_HOME}/gh/extensions/gh-poi"; return 1 ;;
                *) printf "unexpected: %s\n" "$*" ;;
            esac
        }
        main
    '

    [ "${status}" -ne 0 ]
    [ "$(cat "${XDG_DATA_HOME}/gh/extensions/gh-poi/gh-poi")" = "old" ]
    [ ! -e "${XDG_DATA_HOME}/gh/extensions/.gh-poi.previous" ]
    [[ "${output}" != *"unexpected:"* ]]
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
