#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/macos/common/brew.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

@test "[macos] brew" {
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"

    [ -x "$(command -v brew)" ]
}

@test "[macos] brew resolves untrusted runner taps only when CI is exactly true" {
    function brew() {
        printf '%s\n' "$*" >> "${BATS_TEST_TMPDIR}/brew-calls"
        case "$*" in
            "untrust --tap") printf 'Untrusted taps:\n  aws/tap\n  azure/bicep\n  hashicorp/tap\n' ;;
            "list --formula --full-name") printf 'bash\nazure/bicep/bicep\nhashicorp/tap/packer\n' ;;
            "list --cask --full-name") printf 'hashicorp/tap/vagrant\n' ;;
        esac
    }

    local ci_value
    (
        unset CI
        handle_ci_untrusted_taps
    )
    for ci_value in "" false 1 yes; do
        CI="${ci_value}" handle_ci_untrusted_taps
    done
    [ ! -e "${BATS_TEST_TMPDIR}/brew-calls" ]

    CI=true handle_ci_untrusted_taps

    run cat "${BATS_TEST_TMPDIR}/brew-calls"
    [ "${status}" -eq 0 ]
    [ "${output}" = "untrust --tap
list --formula --full-name
list --cask --full-name
trust --formula azure/bicep/bicep hashicorp/tap/packer
trust --cask hashicorp/tap/vagrant
trust aws/tap" ]
}
