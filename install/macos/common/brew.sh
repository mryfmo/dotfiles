#!/usr/bin/env bash

# @file install/macos/common/brew.sh
# @brief Install Homebrew and apply repository defaults.
# @description
#   Ensures Homebrew is installed on macOS, resolves untrusted runner-image taps
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
# @description On a CI runner, resolve the third-party taps that the runner
#   image ships tapped but untrusted, so `brew install` stops warning about
#   them (https://docs.brew.sh/Tap-Trust). The untrusted taps come from
#   Homebrew's own `brew untrust --tap` listing, and the installed items from
#   `brew list --full-name`, which reads each keg's install receipt and so also
#   lists items from untrusted taps. Least privilege first: trust only the
#   installed formulae and casks of each untrusted tap. A tap with nothing
#   installed has no item to trust; measured on macos-14 (job
#   https://github.com/mryfmo/dotfiles/actions/runs/37030239884/job/110914945531),
#   item-level trust alone cleared azure/bicep and hashicorp/tap but the
#   warning persisted for aws/tap, so only such taps get whole-tap trust.
#   Does nothing unless `CI` is exactly `true`.
#
function handle_ci_untrusted_taps() {
    [ "${CI:-}" = "true" ] || return 0

    local listing taps installed tap name formulae="" casks="" with_items="" whole_taps=""
    if ! listing="$(brew untrust --tap 2> /dev/null)"; then
        printf 'brew has no tap trust (no brew untrust command); skipping untrusted tap handling\n' >&2
        return 0
    fi
    # The listing is a header line followed by one indented tap name per line.
    taps="$(sed -n 's/^  //p' <<< "${listing}")"
    [ -n "${taps}" ] || return 0

    installed="$(brew list --formula --full-name)"
    for name in ${installed}; do
        for tap in ${taps}; do
            if [[ "${name}" == "${tap}/"* ]]; then
                formulae+=" ${name}"
                with_items+=" ${tap} "
            fi
        done
    done
    installed="$(brew list --cask --full-name)"
    for name in ${installed}; do
        for tap in ${taps}; do
            if [[ "${name}" == "${tap}/"* ]]; then
                casks+=" ${name}"
                with_items+=" ${tap} "
            fi
        done
    done
    for tap in ${taps}; do
        if [[ "${with_items}" != *" ${tap} "* ]]; then
            whole_taps+=" ${tap}"
        fi
    done

    # shellcheck disable=SC2086 # Space-separated names, word splitting intended.
    if [ -n "${formulae}" ]; then
        brew trust --formula ${formulae}
    fi
    # shellcheck disable=SC2086 # Space-separated names, word splitting intended.
    if [ -n "${casks}" ]; then
        brew trust --cask ${casks}
    fi
    # shellcheck disable=SC2086 # Space-separated names, word splitting intended.
    if [ -n "${whole_taps}" ]; then
        brew trust ${whole_taps}
    fi
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
