#!/usr/bin/env bash

# @file install/common/gh_extensions.sh
# @brief Install GitHub CLI extensions used by the dotfiles.
# @description
#   Activates `mise` when available and installs the configured `gh`
#   extensions at their reviewed tags, only when GitHub CLI is already
#   authenticated. An extension at another tag is reinstalled at the pin.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly MISE_BIN="${HOME}/.local/bin/mise"

# Rendered from assets.gh-extensions in home/dot_agents/agent-config.yaml; change the pin there.
GH_POI_PIN_VERSION="v0.18.5"

readonly GH_EXTENSIONS=(
    "seachicken/gh-poi=${GH_POI_PIN_VERSION}"
)

#
# @description Activate `mise` so `gh` can resolve the expected toolchain.
#
function activate_mise() {
    local activation
    if [ -x "${MISE_BIN}" ]; then
        activation="$("${MISE_BIN}" activate bash)" || {
            printf '%s activate bash failed; gh extensions were not installed.\n' "${MISE_BIN}" >&2
            return 1
        }
        eval "${activation}"
    fi
}

#
# @description Install every configured extension at its pinned tag, or skip when unauthenticated.
# @exitcode 1 When `gh extension list` fails: an unreadable list is never read as "not installed".
#
function install_gh_extensions() {
    local entry extension pin listing installed

    if ! gh auth status &> /dev/null; then
        printf '%s\n' 'Warning: GitHub CLI is not authenticated. Run setup-gh, then make update to install extensions.' >&2
        return 0
    fi

    if ! listing="$(gh extension list)"; then
        printf '%s\n' 'gh extension list failed; gh extensions were not changed.' >&2
        return 1
    fi
    for entry in "${GH_EXTENSIONS[@]}"; do
        extension="${entry%=*}"
        pin="${entry##*=}"
        installed="$(awk -F '\t' -v expected="${extension}" '$2 == expected { print $3; exit }' <<< "${listing}")"
        if [ "${installed}" = "${pin}" ]; then
            continue
        fi
        if [ -n "${installed}" ]; then
            printf '%s is at %s; reinstalling it at the pinned %s.\n' "${extension}" "${installed}" "${pin}"
            gh extension remove "${extension##*/}"
        fi
        gh extension install "${extension}" --pin "${pin}"
    done
}

#
# @description Run the `gh` extension installation workflow.
#
function main() {
    activate_mise
    install_gh_extensions
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
