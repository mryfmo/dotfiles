#!/usr/bin/env bash

# @file install/ubuntu/server/starship.sh
# @brief Install the Starship prompt on Ubuntu servers.
# @description
#   Downloads the newest Starship release that is at least 72 hours old and
#   verifies it against the .sha256 file published with it.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly BIN_DIR="${HOME}/.local/bin"
readonly STARSHIP_RELEASE_REPO="starship/starship"

# The chezmoi script includes scripts/lib/github-release.sh before this file; a direct run sources it.
if ! declare -F github_release_tag > /dev/null; then
    # shellcheck source=scripts/lib/github-release.sh
    source "$(dirname "${BASH_SOURCE[0]}")/../../../scripts/lib/github-release.sh"
fi

# @description Print the Starship Linux artifact name for the current architecture.
function starship_artifact() {
    case "$(uname -m)" in
    x86_64) printf 'starship-x86_64-unknown-linux-musl.tar.gz\n' ;;
    aarch64 | arm64) printf 'starship-aarch64-unknown-linux-musl.tar.gz\n' ;;
    *)
        printf 'Unsupported Starship architecture: %s\n' "$(uname -m)" >&2
        return 1
        ;;
    esac
}

#
# @description Download and install the Starship binary.
#
function install_starship() (
    local actual artifact base_url expected stage="" tag tmpdir
    artifact="$(starship_artifact)" || return
    tag="$(github_release_tag "${STARSHIP_RELEASE_REPO}")" || {
        printf 'Could not resolve a %s release.\n' "${STARSHIP_RELEASE_REPO}" >&2
        return 1
    }
    base_url="https://github.com/${STARSHIP_RELEASE_REPO}/releases/download/${tag}"
    tmpdir="$(mktemp -d)" || return
    trap 'rm -rf "${tmpdir}"; [ -z "${stage}" ] || rm -f "${stage}"' EXIT
    mkdir -p "${BIN_DIR}" || return
    stage="$(mktemp "${BIN_DIR}/starship.tmp.XXXXXX")" || return
    curl -fsSL "${base_url}/${artifact}" -o "${tmpdir}/${artifact}" || return
    expected="$(curl -fsSL "${base_url}/${artifact}.sha256")" || return
    [ -n "${expected}" ] || {
        printf 'Missing checksum for %s\n' "${artifact}" >&2
        return 1
    }
    actual="$(sha256sum "${tmpdir}/${artifact}" | awk '{ print $1 }')" || return
    [ "${actual}" = "${expected}" ] || {
        printf 'Checksum mismatch for %s\n' "${artifact}" >&2
        return 1
    }
    tar -xzf "${tmpdir}/${artifact}" -C "${tmpdir}" || return
    install -m 0755 "${tmpdir}/starship" "${stage}" || return
    mv -f "${stage}" "${BIN_DIR}/starship"
)

#
# @description Remove the locally installed Starship binary.
#
function uninstall_starship() {
    rm -f -- "${BIN_DIR}/starship"
}

#
# @description Run the Starship installation flow.
#
function main() {
    install_starship
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
