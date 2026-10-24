#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/macos/common/ghostty.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

# Only the case that installs the cask removes it (U45): the recorded-call cases below install nothing, and a
# real `brew uninstall` after them would only cost time.
function teardown() {
    if [ -n "${GHOSTTY_CASK_INSTALLED:-}" ]; then
        run uninstall_ghostty
    fi
}

#
# @description Call an installer function with brew replaced, printing each brew call.
# @arg $1 path The installer script to source.
# @arg $2 string The function to call.
# @stdout One line per brew call: `brew` and its arguments, space-separated.
#
function record_brew_calls() {
    bash -c '
        source "$1"
        brew() {
            printf "brew %s\n" "$*"
        }
        "$2"
    ' _ "$1" "$2"
}

@test "[macos] ghostty" {
    GHOSTTY_CASK_INSTALLED=1
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"

    [ -e "/Applications/Ghostty.app" ]
}

@test "[macos] uninstall_ghostty removes exactly the cask install_ghostty installs" {
    local installed

    run record_brew_calls "${SCRIPT_PATH}" install_ghostty
    [ "${status}" -eq 0 ]
    [ "${#lines[@]}" -eq 1 ]
    [[ "${output}" == "brew install "* ]]
    installed="${output#brew install }"

    run record_brew_calls "${SCRIPT_PATH}" uninstall_ghostty
    [ "${status}" -eq 0 ]
    [ "${#lines[@]}" -eq 1 ]
    [[ "${output}" == "brew uninstall "* ]]
    [ "${output#brew uninstall }" = "${installed}" ]
}

@test "[macos] the recorded uninstall_ghostty call catches an uninstaller that drops the cask" {
    local mutant="${BATS_TEST_TMPDIR}/ghostty.sh" installed
    sed 's/^    brew uninstall --cask ghostty$/    brew uninstall --cask/' "${SCRIPT_PATH}" > "${mutant}"
    if cmp -s "${SCRIPT_PATH}" "${mutant}"; then
        false
    fi

    run record_brew_calls "${mutant}" install_ghostty
    [ "${status}" -eq 0 ]
    installed="${output#brew install }"
    run record_brew_calls "${mutant}" uninstall_ghostty
    [ "${status}" -eq 0 ]

    # The recorder saw the mutant's call, and the comparison above would refuse it.
    [ "${output}" = "brew uninstall --cask" ]
    [ "${output#brew uninstall }" != "${installed}" ]
}
