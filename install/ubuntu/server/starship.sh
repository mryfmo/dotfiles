#!/usr/bin/env bash

# @file install/ubuntu/server/starship.sh
# @brief Install the Starship prompt on Ubuntu servers.
# @description
#   Downloads and verifies a pinned Starship release archive.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly BIN_DIR="${HOME}/.local/bin"
readonly STARSHIP_VERSION="v1.25.1"

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
function install_starship() {
    local actual artifact base_url expected stage tmpdir
    artifact="$(starship_artifact)"
    base_url="https://github.com/starship/starship/releases/download/${STARSHIP_VERSION}"
    tmpdir="$(mktemp -d)"
    mkdir -p "${BIN_DIR}"
    stage="$(mktemp "${BIN_DIR}/starship.tmp.XXXXXX")"
    trap 'rm -rf "${tmpdir}"; rm -f "${stage}"' RETURN
    curl -fsSL "${base_url}/${artifact}" -o "${tmpdir}/${artifact}"
    expected="$(curl -fsSL "${base_url}/${artifact}.sha256")"
    [ -n "${expected}" ] || {
        printf 'Missing checksum for %s\n' "${artifact}" >&2
        return 1
    }
    actual="$(sha256sum "${tmpdir}/${artifact}" | awk '{ print $1 }')"
    [ "${actual}" = "${expected}" ] || {
        printf 'Checksum mismatch for %s\n' "${artifact}" >&2
        return 1
    }
    tar -xzf "${tmpdir}/${artifact}" -C "${tmpdir}"
    install -m 0755 "${tmpdir}/starship" "${stage}"
    mv -f "${stage}" "${BIN_DIR}/starship"
}

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
