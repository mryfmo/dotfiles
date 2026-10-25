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
# @description Print the path of scripts/pin_records.py, the strict reader of gh's extension manifest: from
#   the dotfiles checkout (update-agent-assets.sh), chezmoi's source directory (the run_once script), or this
#   file's own repository.
# @exitcode 1 When none of them holds it.
#
function pin_records_path() {
    local root
    for root in "${DOTFILES_REPO_SOURCE_DIR:-}" "${CHEZMOI_SOURCE_DIR:+${CHEZMOI_SOURCE_DIR}/..}" "${BASH_SOURCE[0]%/*}/../.."; do
        if [ -n "${root}" ] && [ -f "${root}/scripts/pin_records.py" ]; then
            printf '%s\n' "${root}/scripts/pin_records.py"
            return 0
        fi
    done
    return 1
}

#
# @description Print gh's record of an installed extension as `<tag> <pinned>`, or `absent`.
# @arg $1 string Extension repository, for example seachicken/gh-poi.
# @exitcode 2 When the record cannot be read, has an unknown shape, or names another owner (a fork):
#   such a copy cannot be verified, so the caller reinstalls it pinned.
#
function gh_extension_state() {
    local reader gh_dir

    if ! reader="$(pin_records_path)" || ! gh_dir="$(python3 -I "${reader}" agent-home gh)"; then
        printf 'Cannot find scripts/pin_records.py or the gh data directory; cannot verify %s.\n' "$1" >&2
        return 2
    fi
    python3 -I "${reader}" gh-extension "${gh_dir}" "$1"
}

#
# @description Install one extension pinned at its tag without losing the copy it replaces.
# @description
#   The installed copy (gh's directory for it) is moved aside under the gh extensions directory with a
#   dot name, which `gh extension list` does not read as an extension; the pinned copy is installed;
#   on success the old copy is deleted, on failure the partial install is removed and the old copy put
#   back, so a failed install never leaves the extension missing.
# @arg $1 string Extension repository, for example seachicken/gh-poi.
# @arg $2 string Pinned tag.
# @exitcode 1 When the pinned install fails (the previous copy is restored) or the old copy cannot be moved.
#
function replace_gh_extension() {
    local extension="$1" pin="$2"
    local reader gh_dir root current previous

    # gh's extension directory, resolved as make doctor resolves it (pin_records.py agent-home gh).
    if ! reader="$(pin_records_path)" || ! gh_dir="$(python3 -I "${reader}" agent-home gh)"; then
        printf 'Cannot resolve the gh extension directory; %s was not changed.\n' "${extension}" >&2
        return 1
    fi
    root="${gh_dir}/extensions"
    current="${root}/${1##*/}"
    previous="${root}/.${1##*/}.previous"

    if [ -e "${current}" ] || [ -L "${current}" ]; then
        if ! { rm -rf "${previous}" && mv "${current}" "${previous}"; }; then
            printf 'Cannot move %s aside; %s was not changed.\n' "${current}" "${extension}" >&2
            return 1
        fi
    fi
    if gh extension install "${extension}" --pin "${pin}"; then
        rm -rf "${previous}"
        return 0
    fi
    printf 'gh extension install %s --pin %s failed; restoring the previous copy.\n' "${extension}" "${pin}" >&2
    if [ -e "${previous}" ] || [ -L "${previous}" ]; then
        rm -rf "${current}" && mv "${previous}" "${current}"
    fi
    return 1
}

#
# @description Install every configured extension pinned at its tag, or skip when unauthenticated.
# @description
#   An extension at its tag and pinned is left alone; one at another tag, or installed unpinned (an earlier
#   plain install, which `gh extension upgrade` could move), is installed again with --pin, keeping the old
#   copy until the new one is in place (replace_gh_extension).
# @exitcode 1 When `gh extension list` fails (an unreadable list is never read as "not installed") or a
#   pinned install fails; every other extension is still processed.
#
function install_gh_extensions() {
    local entry extension pin listing installed state failed=0

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
        # gh's own record decides, read strictly; one it cannot verify (unreadable, foreign) is reinstalled.
        state="$(gh_extension_state "${extension}")" || state="unverifiable"
        if [ "${state}" = "${pin} true" ]; then
            continue
        fi
        if [ "${state}" != "absent" ]; then
            printf '%s is %s (listed at %s); reinstalling it pinned at %s.\n' "${extension}" "${state}" "${installed:-no tag}" "${pin}"
        fi
        replace_gh_extension "${extension}" "${pin}" || failed=1
    done
    return "${failed}"
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
