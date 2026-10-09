#!/usr/bin/env bash

# @file install/common/sheldon.sh
# @brief Install the Sheldon shell plugin manager.
# @description
#   Builds the newest crates.io release with its packaged Cargo.lock; cargo
#   checks the crate against the registry index checksum.

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
# @description Remove the installed `sheldon` binary.
#
function uninstall_sheldon() {
    rm "${BIN_DIR}/sheldon"
}

#
# @description Run the Sheldon installation flow.
#
function main() {
    install_sheldon
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
