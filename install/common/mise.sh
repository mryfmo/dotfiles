#!/usr/bin/env bash

# @file install/common/mise.sh
# @brief Install and bootstrap `mise`.
# @description
#   Downloads the newest standalone `mise` release that is at least 72 hours old,
#   verifies it, then runs `mise install` against the repository tool definitions.

# set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

export MISE_INSTALL_PATH="${HOME}/.local/bin/mise"
readonly MISE_RELEASE_REPO="jdx/mise"

# The chezmoi script includes scripts/lib/github-release.sh before this file; a direct run sources it.
if ! declare -F github_release_tag > /dev/null; then
    # shellcheck source=scripts/lib/github-release.sh
    source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/lib/github-release.sh"
fi

# @description Print the mise release artifact name for the current platform.
# @arg $1 string The release tag.
function mise_artifact() {
    local os arch
    os="$(uname -s)"
    arch="$(uname -m)"
    case "${os}/${arch}" in
    Darwin/x86_64) printf 'mise-%s-macos-x64.tar.gz\n' "$1" ;;
    Darwin/arm64) printf 'mise-%s-macos-arm64.tar.gz\n' "$1" ;;
    Linux/x86_64) printf 'mise-%s-linux-x64.tar.gz\n' "$1" ;;
    Linux/aarch64 | Linux/arm64) printf 'mise-%s-linux-arm64.tar.gz\n' "$1" ;;
    *)
        printf 'Unsupported mise platform: %s/%s\n' "${os}" "${arch}" >&2
        return 1
        ;;
    esac
}

# @description Verify a release archive against an upstream checksum manifest.
# @arg $1 archive Archive path.
# @arg $2 manifest Checksum manifest path.
# @arg $3 name Artifact name in the manifest.
function verify_mise_archive() {
    local archive="$1" manifest="$2" name="$3" expected actual
    expected="$(awk -v name="./${name}" '$2 == name { print $1 }' "${manifest}")"
    [ -n "${expected}" ] || {
        printf 'Missing checksum for %s\n' "${name}" >&2
        return 1
    }
    if command -v sha256sum > /dev/null 2>&1; then
        actual="$(sha256sum "${archive}" | awk '{ print $1 }')"
    else
        actual="$(shasum -a 256 "${archive}" | awk '{ print $1 }')"
    fi
    [ "${actual}" = "${expected}" ] || {
        printf 'Checksum mismatch for %s\n' "${name}" >&2
        return 1
    }
}

#
# @description Install the newest cooled-down standalone `mise` release, checked against its
#   SHASUMS256.txt and, when an authenticated gh is present, its GitHub release attestation.
#
function _install_mise_binary() (
    local artifact attestation=0 base_url stage="" tag tmpdir
    tag="$(github_release_tag "${MISE_RELEASE_REPO}")" || {
        printf 'Could not resolve a %s release.\n' "${MISE_RELEASE_REPO}" >&2
        return 1
    }
    artifact="$(mise_artifact "${tag}")" || return
    base_url="https://github.com/${MISE_RELEASE_REPO}/releases/download/${tag}"
    tmpdir="$(mktemp -d)" || return
    trap 'rm -rf "${tmpdir}"; [ -z "${stage}" ] || rm -f "${stage}"' EXIT
    mkdir -p "$(dirname "${MISE_INSTALL_PATH}")" || return
    stage="$(mktemp "${MISE_INSTALL_PATH}.tmp.XXXXXX")" || return

    curl -fsSL "${base_url}/${artifact}" -o "${tmpdir}/${artifact}" || return
    curl -fsSL "${base_url}/SHASUMS256.txt" -o "${tmpdir}/SHASUMS256.txt" || return
    verify_mise_archive "${tmpdir}/${artifact}" "${tmpdir}/SHASUMS256.txt" "${artifact}" || return
    github_release_attestation "${MISE_RELEASE_REPO}" "${tag}" "${tmpdir}/${artifact}" || attestation=$?
    case "${attestation}" in
    0) ;;
    2) printf 'gh is absent or not authenticated: mise %s is verified by SHASUMS256.txt only.\n' "${tag}" ;;
    *)
        printf 'GitHub release attestation failed for %s.\n' "${artifact}" >&2
        return 1
        ;;
    esac
    tar -xzf "${tmpdir}/${artifact}" -C "${tmpdir}" || return
    install -m 0755 "${tmpdir}/mise/bin/mise" "${stage}" || return
    mv -f "${stage}" "${MISE_INSTALL_PATH}"
)

#
# @description Install the standalone `mise` binary and activate it for the caller.
#
function install_mise() {
    local activation
    _install_mise_binary || return
    activation="$("${MISE_INSTALL_PATH}" activate bash)" || return
    eval "${activation}"
}

#
# @description Trust the local `mise.toml` before plugin or tool installation.
#
function trust_mise_config() {
    mise trust --yes
}

#
# @description Install all tools declared for this repository through `mise`.
#
function run_mise_install() {
    # `MISE_CURRENT_VERSION` is interpreted by mise as a tool env override for `current`.
    unset MISE_CURRENT_VERSION
    trust_mise_config || return

    # One bare install takes every declared tool under the config's
    # minimum_release_age (~/.npmrc applies the same window) and skips requests
    # already satisfied, so an installed "latest" needs no registry lookup.
    mise install
}

#
# @description Remove the standalone `mise` binary from the local bin dir.
#
function uninstall_mise() {
    rm "${MISE_INSTALL_PATH}"
}

#
# @description Install `mise` and the configured tools.
#
function main() {
    install_mise || return
    run_mise_install
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
