#!/usr/bin/env bash

# @file install/common/mise.sh
# @brief Install and bootstrap `mise`.
# @description
#   Nothing runs before a check independent of the release page passes. With gpg and gpgv
#   (the release key's signature on SHASUMS256.asc) or an authenticated gh (the GitHub release
#   attestation), it downloads the newest standalone `mise` release that is at least 72 hours old
#   and verifies it that way; without either, as on a fresh macOS, it installs the reviewed
#   fallback release pinned in the manifest. Then it runs `mise install` against the repository
#   tool definitions; `mise self-update` moves mise forward afterwards.

# set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

export MISE_INSTALL_PATH="${HOME}/.local/bin/mise"
readonly MISE_RELEASE_REPO="jdx/mise"
# Rendered from assets.mise in home/dot_agents/agent-config.yaml; change it there.
readonly MISE_GPG_FINGERPRINT="24853EC9F655CE80B48E6C3A8B81C9D17413A06D"
# mise publishes its release key on this keyserver; only the pinned fingerprint makes it trusted.
readonly MISE_GPG_KEY_URL="https://keys.openpgp.org/vks/v1/by-fingerprint/${MISE_GPG_FINGERPRINT}"
# The reviewed release a host without gh or gpg bootstraps, rendered from assets.mise.fallback;
# change them there. Assignments stay non-readonly so tests can override them after sourcing.
MISE_FALLBACK_VERSION="v2026.10.3"
MISE_FALLBACK_MACOS_X64_SHA256="791b92b446729c53e6501acd2b84ea207f541659ca9d0480c9c70c291919a321"
MISE_FALLBACK_MACOS_ARM64_SHA256="28ecc8640b0a28dab52817766f37fecfd898f1dff82e03f36fcb072e971f9246"
MISE_FALLBACK_LINUX_X64_SHA256="04147c68e946902f5226dfdcd54d19907aed3cf54d95b2f27d2b9c778bb26f9e"
MISE_FALLBACK_LINUX_ARM64_SHA256="e79866e32624b346f6854d93ca8a24294516cd7c0b48ce0e80af508fb7c3d8b8"

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
# @description Print the checksums SHASUMS256.asc signs, once gpgv has checked the signature
#   against mise's release key with the pinned fingerprint.
# @arg $1 path SHASUMS256.asc
# @arg $2 path A private scratch directory.
# @stdout The signed checksum lines.
#
function verify_mise_shasums_signature() {
    local key="$2/mise-release-key.asc" key_data fingerprint validity expiration
    curl -fsSL "${MISE_GPG_KEY_URL}" -o "${key}" || return
    mkdir -m 700 "$2/gnupg" || return
    key_data="$(gpg --homedir "$2/gnupg" --batch --with-colons --import-options show-only --import "${key}")" || return
    # Exactly one primary key, and the fingerprint line right after it is the primary's own.
    read -r fingerprint validity expiration <<< "$(awk -F: '
        $1 == "pub" { keys++; validity = $2; expiration = $7; primary = 1; next }
        $1 == "fpr" && primary { fingerprint = $10; primary = 0 }
        END { if (keys == 1) print fingerprint, validity, expiration }' <<< "${key_data}")"
    if [ "${fingerprint}" != "${MISE_GPG_FINGERPRINT}" ] || [ "${validity}" != "-" ] ||
        { [ -n "${expiration}" ] && ! [ "${expiration}" -gt "$(date +%s)" ] 2> /dev/null; }; then
        printf 'mise release key validation failed.\n' >&2
        return 1
    fi
    gpg --homedir "$2/gnupg" --batch --yes --dearmor --output "$2/mise-keyring.gpg" "${key}" || return
    gpgv --keyring "$2/mise-keyring.gpg" --output - "$1"
}

#
# @description Succeed when gpg and gpgv can check the release key's signature on SHASUMS256.asc.
#
function mise_gpg_ready() {
    command -v gpg > /dev/null 2>&1 && command -v gpgv > /dev/null 2>&1
}

#
# @description Print the reviewed fallback sha256 of a mise release artifact.
# @arg $1 string The artifact name.
#
function mise_fallback_sha256() {
    case "$1" in
    *-macos-x64.tar.gz) printf '%s\n' "${MISE_FALLBACK_MACOS_X64_SHA256}" ;;
    *-macos-arm64.tar.gz) printf '%s\n' "${MISE_FALLBACK_MACOS_ARM64_SHA256}" ;;
    *-linux-x64.tar.gz) printf '%s\n' "${MISE_FALLBACK_LINUX_X64_SHA256}" ;;
    *-linux-arm64.tar.gz) printf '%s\n' "${MISE_FALLBACK_LINUX_ARM64_SHA256}" ;;
    *) return 1 ;;
    esac
}

#
# @description Install standalone `mise`, verified before it runs: the newest cooled-down release
#   when gpg (the signed SHASUMS256.asc) or an authenticated gh (the release attestation) can
#   check it, otherwise the reviewed fallback release and its pinned sha256. The release's own
#   checksum file is checked on every path.
#
function _install_mise_binary() (
    local artifact attestation=0 base_url fallback="" gpg_ready="" stage="" tag tmpdir
    if mise_gpg_ready; then gpg_ready=1; fi
    if [ -n "${gpg_ready}" ] || github_attestation_ready; then
        tag="$(github_release_tag "${MISE_RELEASE_REPO}")" || {
            printf 'Could not resolve a %s release.\n' "${MISE_RELEASE_REPO}" >&2
            return 1
        }
    else
        # Neither check can run before mise does, so the reviewed release installs instead.
        fallback=1
        tag="${MISE_FALLBACK_VERSION}"
        printf 'No gpg and no authenticated gh 2.93.0 or newer: installing the reviewed mise %s (assets.mise.fallback).\n' "${tag}"
    fi
    artifact="$(mise_artifact "${tag}")" || return
    base_url="https://github.com/${MISE_RELEASE_REPO}/releases/download/${tag}"
    tmpdir="$(mktemp -d)" || return
    trap 'rm -rf "${tmpdir}"; [ -z "${stage}" ] || rm -f "${stage}"' EXIT
    mkdir -p "$(dirname "${MISE_INSTALL_PATH}")" || return
    stage="$(mktemp "${MISE_INSTALL_PATH}.tmp.XXXXXX")" || return

    curl -fsSL "${base_url}/${artifact}" -o "${tmpdir}/${artifact}" || return
    if [ -n "${gpg_ready}" ]; then
        # The checksums come from the signed text itself, never from an unsigned SHASUMS256.txt.
        curl -fsSL "${base_url}/SHASUMS256.asc" -o "${tmpdir}/SHASUMS256.asc" || return
        verify_mise_shasums_signature "${tmpdir}/SHASUMS256.asc" "${tmpdir}" > "${tmpdir}/SHASUMS256.txt" || {
            printf 'GPG signature check failed for SHASUMS256.asc of mise %s.\n' "${tag}" >&2
            return 1
        }
    else
        curl -fsSL "${base_url}/SHASUMS256.txt" -o "${tmpdir}/SHASUMS256.txt" || return
    fi
    verify_mise_archive "${tmpdir}/${artifact}" "${tmpdir}/SHASUMS256.txt" "${artifact}" || return
    if [ -n "${fallback}" ]; then
        # The reviewed sha256 is the check here; SHASUMS256.txt above only re-checked the download.
        printf '%s  ./%s\n' "$(mise_fallback_sha256 "${artifact}")" "${artifact}" > "${tmpdir}/reviewed.txt"
        verify_mise_archive "${tmpdir}/${artifact}" "${tmpdir}/reviewed.txt" "${artifact}" || {
            printf 'mise %s does not match its reviewed sha256; nothing was installed.\n' "${tag}" >&2
            return 1
        }
    else
        github_release_attestation "${MISE_RELEASE_REPO}" "${tag}" "${tmpdir}/${artifact}" || attestation=$?
        # Status 2 (gh not ready) is enough only after the GPG signature verified the checksums.
        if [ "${attestation}" -ne 0 ] && { [ "${attestation}" -ne 2 ] || [ -z "${gpg_ready}" ]; }; then
            printf 'GitHub release attestation failed for %s; nothing was installed.\n' "${artifact}" >&2
            return 1
        fi
    fi
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
