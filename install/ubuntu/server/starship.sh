#!/usr/bin/env bash

# @file install/ubuntu/server/starship.sh
# @brief Install the Starship prompt on Ubuntu servers.
# @description
#   Downloads the pinned Starship release and verifies it against its reviewed
#   sha256 and the .sha256 file published with it. Runs on every chezmoi apply
#   and skips when the pinned release is already installed, so a pin bump
#   applies on the next `make update`.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly BIN_DIR="${HOME}/.local/bin"
readonly STARSHIP_RELEASE_REPO="starship/starship"
# Rendered from assets.starship in home/dot_agents/agent-config.yaml; change them there.
# starship's releases are mutable and carry only .sha256 sidecars, so the reviewed sha256 is the check.
readonly STARSHIP_PIN_VERSION="v1.26.0"
readonly STARSHIP_X86_64_SHA256="b7c232b0e8249d8e55a40beb79c5c43a7d370f3f9408bd215deb0170daeaadf3"
readonly STARSHIP_AARCH64_SHA256="dc30189378d2f2e287384e8a692d3f95ad1df64cf0e8c36aa9201516028aed6b"

# @description Print the Starship Linux artifact name and its reviewed sha256 for the current architecture.
function starship_artifact() {
    case "$(uname -m)" in
    x86_64) printf 'starship-x86_64-unknown-linux-musl.tar.gz %s\n' "${STARSHIP_X86_64_SHA256}" ;;
    aarch64 | arm64) printf 'starship-aarch64-unknown-linux-musl.tar.gz %s\n' "${STARSHIP_AARCH64_SHA256}" ;;
    *)
        printf 'Unsupported Starship architecture: %s\n' "$(uname -m)" >&2
        return 1
        ;;
    esac
}

#
# @description Print the installed Starship version, or nothing when it is absent or cannot report one.
#
function starship_installed_version() {
    local output
    [ -x "${BIN_DIR}/starship" ] || return 0
    # A binary that exits non-zero is broken whatever it printed, so it reports no version.
    output="$("${BIN_DIR}/starship" --version 2> /dev/null)" || return 0
    printf '%s\n' "${output}" | awk '$1 == "starship" { print $2; exit }'
}

#
# @description Download the pinned Starship release, verify it, and install the binary.
# @exitcode 1 The checksum did not match, or the install failed; nothing was installed.
# @exitcode 3 A download failed, so nothing was installed.
#
function install_starship() (
    local actual artifact base_url expected line pinned stage="" tmpdir
    line="$(starship_artifact)" || return
    read -r artifact pinned <<< "${line}"
    base_url="https://github.com/${STARSHIP_RELEASE_REPO}/releases/download/${STARSHIP_PIN_VERSION}"
    tmpdir="$(mktemp -d)" || return
    trap 'rm -rf "${tmpdir}"; [ -z "${stage}" ] || rm -f "${stage}"' EXIT
    mkdir -p "${BIN_DIR}" || return
    stage="$(mktemp "${BIN_DIR}/starship.tmp.XXXXXX")" || return
    curl -fsSL "${base_url}/${artifact}" -o "${tmpdir}/${artifact}" || return 3
    expected="$(curl -fsSL "${base_url}/${artifact}.sha256")" || return 3
    [ -n "${expected}" ] || {
        printf 'Missing checksum for %s\n' "${artifact}" >&2
        return 1
    }
    actual="$(sha256sum "${tmpdir}/${artifact}" | awk '{ print $1 }')" || return
    # The reviewed sha256 is the check; the release's own .sha256 only re-checks the download.
    if [ "${actual}" != "${pinned}" ] || [ "${actual}" != "${expected}" ]; then
        printf 'Checksum mismatch for %s\n' "${artifact}" >&2
        return 1
    fi
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
# @description Install or update Starship to the pinned release.
#
function main() {
    local installed status=0
    installed="$(starship_installed_version)"
    [ "${installed}" != "${STARSHIP_PIN_VERSION#v}" ] || return 0
    install_starship || status=$?
    # A failed download keeps a working Starship; a failed check never does.
    if [ "${status}" -eq 3 ] && [ -n "${installed}" ]; then
        printf 'warning: could not download Starship %s; Starship %s stays.\n' "${STARSHIP_PIN_VERSION}" "${installed}" >&2
        return 0
    fi
    return "${status}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
