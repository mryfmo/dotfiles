#!/usr/bin/env bats

readonly SCRIPT_PATH="./install/macos/common/brew.sh"

function setup() {
    source "${SCRIPT_PATH}"
}

@test "[macos] brew" {
    DOTFILES_DEBUG=1 bash "${SCRIPT_PATH}"

    [ -x "$(command -v brew)" ]
}

@test "[macos] brew resolves untrusted runner taps only on a GitHub Actions runner" {
    function brew() {
        printf '%s\n' "$*" >> "${BATS_TEST_TMPDIR}/brew-calls"
        case "$*" in
            "untrust --tap") printf 'Untrusted taps:\n  aws/tap\n  azure/bicep\n  hashicorp/tap\n' ;;
            "list --formula --full-name") printf 'bash\nazure/bicep/bicep\nhashicorp/tap/packer\n' ;;
            "list --cask --full-name") printf 'hashicorp/tap/vagrant\n' ;;
        esac
    }

    # Off the runner, an agent shell's CI=true included, no tap is touched.
    (
        unset GITHUB_ACTIONS RUNNER_TEMP
        CI=true handle_ci_untrusted_taps
        GITHUB_ACTIONS=true handle_ci_untrusted_taps
        GITHUB_ACTIONS=false RUNNER_TEMP="${BATS_TEST_TMPDIR}" handle_ci_untrusted_taps
        GITHUB_ACTIONS=1 RUNNER_TEMP="${BATS_TEST_TMPDIR}" handle_ci_untrusted_taps
    )
    [ ! -e "${BATS_TEST_TMPDIR}/brew-calls" ]

    GITHUB_ACTIONS=true RUNNER_TEMP="${BATS_TEST_TMPDIR}" handle_ci_untrusted_taps

    run cat "${BATS_TEST_TMPDIR}/brew-calls"
    [ "${status}" -eq 0 ]
    [ "${output}" = "untrust --tap
list --formula --full-name
list --cask --full-name
trust --formula azure/bicep/bicep hashicorp/tap/packer
trust --cask hashicorp/tap/vagrant
trust aws/tap" ]
}
