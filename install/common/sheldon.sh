#!/usr/bin/env bash

# @file install/common/sheldon.sh
# @brief Install the Sheldon shell plugin manager.
# @description
#   Builds the newest crates.io release with its packaged Cargo.lock; cargo
#   checks the crate against the registry index checksum. Runs on every chezmoi
#   apply and skips when the newest crate is already installed.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly BIN_DIR="${HOME}/.local/bin"
readonly MISE_BIN="${HOME}/.local/bin/mise"

#
# @description Build and install the crates.io Sheldon release with locked dependencies.
#
function install_sheldon() (
    local stage="" tmpdir
    tmpdir="$(mktemp -d)" || return
    trap 'rm -rf "${tmpdir}"; [ -z "${stage}" ] || rm -f "${stage}"' EXIT
    mkdir -p "${BIN_DIR}" || return
    stage="$(mktemp "${BIN_DIR}/sheldon.tmp.XXXXXX")" || return
    CARGO_INSTALL_ROOT="${tmpdir}" "${MISE_BIN}" exec -- cargo install \
        --locked --features vendored --registry crates-io sheldon || return
    install -m 0755 "${tmpdir}/bin/sheldon" "${stage}" || return
    mv -f "${stage}" "${BIN_DIR}/sheldon"
)

#
# @description Print the installed Sheldon version, or nothing when it is absent or cannot report one.
#
function sheldon_installed_version() {
    [ -x "${BIN_DIR}/sheldon" ] || return 0
    { "${BIN_DIR}/sheldon" --version 2> /dev/null || true; } | awk '$1 == "sheldon" { print $2; exit }'
}

#
# @description Print the newest Sheldon version on crates.io, as cargo's own index search reports it.
#
function sheldon_newest_version() {
    "${MISE_BIN}" exec -- cargo search sheldon --limit 1 2> /dev/null |
        awk -F'"' '$1 == "sheldon = " { print $2; found = 1; exit } END { exit !found }'
}

#
# @description Remove the installed `sheldon` binary.
#
function uninstall_sheldon() {
    rm "${BIN_DIR}/sheldon"
}

#
# @description Install Sheldon, or update it when crates.io has a newer release.
#
function main() {
    local installed newest
    installed="$(sheldon_installed_version)"
    newest="$(sheldon_newest_version)" || newest=""
    if [ -n "${installed}" ]; then
        if [ -z "${newest}" ]; then
            printf 'warning: could not look up the newest sheldon crate; sheldon %s stays.\n' "${installed}" >&2
            return 0
        fi
        [ "${installed}" != "${newest}" ] || return 0
    fi
    install_sheldon
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
