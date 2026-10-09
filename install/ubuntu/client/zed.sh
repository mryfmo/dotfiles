#!/usr/bin/env bash

# @file install/ubuntu/client/zed.sh
# @brief Install the Zed editor on Ubuntu client machines from its newest cooled-down GitHub release.
# @description
#   Resolves the newest Zed release that is at least 72 hours old, verifies the
#   Linux tarball against the release's GitHub attestation with an authenticated
#   gh, extracts it under ~/.local, and exposes ~/.local/bin/zed. Runs on every
#   chezmoi apply: it skips when the resolved release is installed, installs
#   nothing (and keeps any installed Zed) when the release cannot be resolved,
#   and installs nothing without an authenticated gh, because Zed publishes no
#   other verification. Only a failed attestation fails the apply.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly ZED_APP_DIR="${HOME}/.local/share/zed.app"
readonly ZED_BIN_LINK="${HOME}/.local/bin/zed"
readonly ZED_RELEASE_REPO="zed-industries/zed"

# The chezmoi script includes scripts/lib/github-release.sh before this file; a direct run sources it.
if ! declare -F github_release_tag > /dev/null; then
    # shellcheck source=scripts/lib/github-release.sh
    source "$(dirname "${BASH_SOURCE[0]}")/../../../scripts/lib/github-release.sh"
fi

#
# @description Print the Zed release artifact name for this architecture.
#
function zed_artifact() {
    case "$(uname -m)" in
    x86_64 | amd64) printf 'zed-linux-x86_64.tar.gz\n' ;;
    aarch64 | arm64) printf 'zed-linux-aarch64.tar.gz\n' ;;
    *)
        printf 'Unsupported Zed architecture: %s\n' "$(uname -m)" >&2
        return 1
        ;;
    esac
}

#
# @description Print the installed Zed version, or nothing when Zed is not installed or cannot
#   report one, so a broken install is replaced like a missing one.
#
function zed_installed_version() {
    [ -x "${ZED_BIN_LINK}" ] || return 0
    { "${ZED_BIN_LINK}" --version 2> /dev/null || true; } | awk '$1 == "Zed" { print $2; exit }'
}

#
# @description Download a Zed release, verify it against the release attestation, and atomically install it.
# @arg $1 string The release tag.
# @exitcode 2 gh is absent or not authenticated, so nothing was installed.
#
function install_zed_release() (
    local tag="$1" artifact download status=0 tmpdir staging="${ZED_APP_DIR}.tmp"
    artifact="$(zed_artifact)" || return
    tmpdir="$(mktemp -d)" || return
    trap 'rm -rf "${tmpdir}" "${staging}"' EXIT
    download="${tmpdir}/${artifact}"

    curl -fsSL "https://github.com/${ZED_RELEASE_REPO}/releases/download/${tag}/${artifact}" -o "${download}" || return
    github_release_attestation "${ZED_RELEASE_REPO}" "${tag}" "${download}" || status=$?
    case "${status}" in
    0) ;;
    2) return 2 ;;
    *)
        printf 'Zed %s failed its GitHub release attestation; nothing was installed.\n' "${tag}" >&2
        return 1
        ;;
    esac

    tar -xzf "${download}" -C "${tmpdir}" || return
    mkdir -p "$(dirname "${ZED_APP_DIR}")" || return
    rm -rf "${staging}"
    mv "${tmpdir}/zed.app" "${staging}" || return
    rm -rf "${ZED_APP_DIR}"
    mv "${staging}" "${ZED_APP_DIR}"
)

#
# @description Point ~/.local/bin/zed at the installed Zed binary.
#
function link_zed_bin() {
    mkdir -p "$(dirname "${ZED_BIN_LINK}")" || return
    ln -sf "${ZED_APP_DIR}/bin/zed" "${ZED_BIN_LINK}"
}

#
# @description Install or update Zed to the newest cooled-down release.
#
function main() {
    local installed status=0 tag
    # gh is a mise tool; its shim serves when no gh is on PATH yet.
    PATH="${PATH}:${HOME}/.local/share/mise/shims"
    installed="$(zed_installed_version)"
    if ! tag="$(github_release_tag "${ZED_RELEASE_REPO}")"; then
        # Offline or rate-limited: never fail the apply over Zed; the next make update retries.
        if [ -n "${installed}" ]; then
            printf 'warning: could not resolve a Zed release; Zed %s stays.\n' "${installed}" >&2
        else
            printf 'zed not installed: could not resolve a %s release; the next make update retries.\n' "${ZED_RELEASE_REPO}" >&2
        fi
        return 0
    fi
    [ "${installed}" != "${tag#v}" ] || return 0
    # Checked before the download: without an authenticated gh nothing can be verified.
    github_attestation_ready || status=2
    [ "${status}" -ne 0 ] || install_zed_release "${tag}" || status=$?
    case "${status}" in
    0) link_zed_bin ;;
    2)
        if [ -n "${installed}" ]; then
            printf 'zed %s stays (not updated to %s): run make gh-auth, then make update; its release attestation cannot be verified without an authenticated gh.\n' "${installed}" "${tag}" >&2
        else
            printf 'zed not installed: run make gh-auth, then make update; its release attestation cannot be verified without an authenticated gh.\n' >&2
        fi
        return 0
        ;;
    *) return "${status}" ;;
    esac
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
