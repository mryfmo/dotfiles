#!/usr/bin/env bash

# @file install/common/sheldon.sh
# @brief Install the Sheldon shell plugin manager.
# @description
#   Builds the pinned crates.io release with its packaged Cargo.lock.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly BIN_DIR="${HOME}/.local/bin"
readonly MISE_BIN="${HOME}/.local/bin/mise"
readonly SHELDON_VERSION="0.8.5"
# crates.io API: https://crates.io/api/v1/crates/sheldon/0.8.5
# Registry SHA-256: 43a2d8fc0be4474cfe2d603992c7e9765c9a0f87465aabcfc0603c1de4290b4d

#
# @description Build and install the crates.io Sheldon release with locked dependencies.
#
function install_sheldon() (
    local stage="" tmpdir
    tmpdir="$(mktemp -d)" || return
    trap 'rm -rf "${tmpdir}"; [ -z "${stage}" ] || rm -f "${stage}"' EXIT
    mkdir -p "${BIN_DIR}" || return
    stage="$(mktemp "${BIN_DIR}/sheldon.tmp.XXXXXX")" || return
    CARGO_INSTALL_ROOT="${tmpdir}" "${MISE_BIN}" exec --locked -- cargo install \
        --locked --features vendored --registry crates-io \
        --version "=${SHELDON_VERSION}" sheldon || return
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
