#!/usr/bin/env bash

# @file install/macos/common/brew.sh
# @brief Install Homebrew and apply repository defaults.
# @description
#   Ensures Homebrew is installed on macOS, trusts untrusted runner-image taps
#   on CI, and disables analytics for the local user.

set -Eeuo pipefail

# Rendered from assets.homebrew-installer in home/dot_agents/agent-config.yaml; change it there.
readonly HOMEBREW_INSTALL_COMMIT="c7952e40b7957268f61643152f4db725379b292e"
readonly HOMEBREW_INSTALL_SHA256="99287f194a8b3c9e6b0203a11a5fa54518be57209343e6bb954dec4635796d9d"

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

#
# @description Check whether Homebrew is already available on `PATH`.
#
function is_homebrew_exists() {
    command -v brew &> /dev/null
}

#
# @description Install Homebrew when it is not present.
#
function install_homebrew() {
    if ! is_homebrew_exists; then
        (
            local actual installer
            installer="$(mktemp)"
            trap 'rm -f "${installer}"' EXIT
            curl -fsSL "https://raw.githubusercontent.com/Homebrew/install/${HOMEBREW_INSTALL_COMMIT}/install.sh" -o "${installer}"
            actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
            [ "${actual}" = "${HOMEBREW_INSTALL_SHA256}" ] || {
                printf 'Homebrew installer checksum mismatch\n' >&2
                return 1
            }
            NONINTERACTIVE=1 /bin/bash "${installer}"
        )
    fi
}

#
# @description Disable Homebrew analytics for the current user.
#
function opt_out_of_analytics() {
    brew analytics off
}

#
# @description On a CI runner, trust the third-party taps that the runner image
#   ships tapped but untrusted, so `brew install` stops warning about them
#   (https://docs.brew.sh/Tap-Trust). The taps come from Homebrew's own
#   `brew untrust --tap` listing. Whole-tap trust is the only remediation in
#   Homebrew's warning that works unattended for every listed tap: Homebrew
#   cannot list installed formulae from an untrusted tap, so item-level trust
#   is not derivable, and `brew untap` refuses a tap with installed kegs.
#   Does nothing unless `CI` is exactly `true`.
#
function handle_ci_untrusted_taps() {
    [ "${CI:-}" = "true" ] || return 0

    local listing taps
    if ! listing="$(brew untrust --tap 2> /dev/null)"; then
        printf 'brew has no tap trust (no brew untrust command); skipping untrusted tap handling\n' >&2
        return 0
    fi
    # The listing is a header line followed by one indented tap name per line.
    taps="$(sed -n 's/^  //p' <<< "${listing}")"
    [ -n "${taps}" ] || return 0

    # shellcheck disable=SC2086 # One tap name per word, word splitting intended.
    brew trust ${taps}
}

#
# @description Install Homebrew and apply repository defaults.
#
function main() {
    install_homebrew
    handle_ci_untrusted_taps
    opt_out_of_analytics
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
