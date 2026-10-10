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
# @exitcode 1 cargo failed for any reason other than a download, a checksum among them; nothing was installed.
# @exitcode 3 cargo could not download the crate or the index, so nothing was installed.
#
function install_sheldon() (
    local stage="" status=0 tmpdir
    tmpdir="$(mktemp -d)" || return
    trap 'rm -rf "${tmpdir}"; [ -z "${stage}" ] || rm -f "${stage}"' EXIT
    mkdir -p "${BIN_DIR}" || return
    stage="$(mktemp "${BIN_DIR}/sheldon.tmp.XXXXXX")" || return
    # cargo's errors still reach stderr; the copy tells a download failure from the rest.
    { CARGO_INSTALL_ROOT="${tmpdir}" "${MISE_BIN}" exec -- cargo install \
        --locked --features vendored --registry crates-io sheldon 2>&1 1>&3 | tee "${tmpdir}/cargo.log" >&2; } 3>&1 || status=$?
    if [ "${status}" -ne 0 ]; then
        # cargo exits 101 for every error. A checksum is verification, even inside a download error.
        grep -qi 'checksum' "${tmpdir}/cargo.log" && return 1
        grep -qiE 'failed to download|resolve host|failed to update registry|spurious network|timed out' "${tmpdir}/cargo.log" && return 3
        return 1
    fi
    install -m 0755 "${tmpdir}/bin/sheldon" "${stage}" || return
    mv -f "${stage}" "${BIN_DIR}/sheldon"
)

#
# @description Print the installed Sheldon version, or nothing when it is absent or cannot report one.
#
function sheldon_installed_version() {
    local output
    [ -x "${BIN_DIR}/sheldon" ] || return 0
    # A binary that exits non-zero is broken whatever it printed, so it reports no version.
    output="$("${BIN_DIR}/sheldon" --version 2> /dev/null)" || return 0
    printf '%s\n' "${output}" | awk '$1 == "sheldon" { print $2; exit }'
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
    local installed newest status=0
    installed="$(sheldon_installed_version)"
    newest="$(sheldon_newest_version)" || newest=""
    if [ -n "${installed}" ]; then
        if [ -z "${newest}" ]; then
            printf 'warning: could not look up the newest sheldon crate; sheldon %s stays.\n' "${installed}" >&2
            return 0
        fi
        [ "${installed}" != "${newest}" ] || return 0
    fi
    install_sheldon || status=$?
    # A failed download keeps a working sheldon; a failed check never does.
    if [ "${status}" -eq 3 ] && [ -n "${installed}" ]; then
        printf 'warning: could not download the sheldon %s crate; sheldon %s stays.\n' "${newest}" "${installed}" >&2
        return 0
    fi
    return "${status}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
