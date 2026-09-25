#!/usr/bin/env bash

# @file install/ubuntu/client/zed.sh
# @brief Install the Zed editor on Ubuntu client machines from a pinned GitHub release.
# @description
#   Downloads and verifies a pinned Zed Linux release tarball for the current
#   architecture, extracts it under ~/.local, and exposes ~/.local/bin/zed.
#   Idempotent: skips the download when the pinned version is already
#   installed. Requires ZED_PIN_VERSION and ZED_LINUX_{AMD64,ARM64}_SHA256
#   from scripts/lib/installer-pins.sh.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

readonly ZED_APP_DIR="${HOME}/.local/share/zed.app"
readonly ZED_BIN_LINK="${HOME}/.local/bin/zed"

#
# @description Print the Zed release artifact name and its expected SHA256 for this architecture.
# @stdout Two lines: artifact name, then its expected SHA256.
#
function zed_artifact() {
    case "$(uname -m)" in
    x86_64 | amd64)
        printf 'zed-linux-x86_64.tar.gz\n%s\n' "${ZED_LINUX_AMD64_SHA256}"
        ;;
    aarch64 | arm64)
        printf 'zed-linux-aarch64.tar.gz\n%s\n' "${ZED_LINUX_ARM64_SHA256}"
        ;;
    *)
        printf 'Unsupported Zed architecture: %s\n' "$(uname -m)" >&2
        return 1
        ;;
    esac
}

#
# @description Report whether the installed Zed already matches the pinned version.
#
function zed_up_to_date() {
    [ -x "${ZED_BIN_LINK}" ] || return 1
    "${ZED_BIN_LINK}" --version 2> /dev/null |
        awk -v expected="${ZED_PIN_VERSION#v}" '$1 == "Zed" && $2 == expected { found = 1 } END { exit !found }'
}

#
# @description Download, verify, and atomically install the pinned Zed release.
#
function install_pinned_zed() (
    local artifact checksum actual download tmpdir staging="${ZED_APP_DIR}.tmp"
    {
        read -r artifact
        read -r checksum
    } < <(zed_artifact) || return

    download="$(mktemp)" || return
    tmpdir="$(mktemp -d)" || return
    trap 'rm -f "${download}"; rm -rf "${tmpdir}" "${staging}"' EXIT

    curl -fsSL "https://github.com/zed-industries/zed/releases/download/${ZED_PIN_VERSION}/${artifact}" -o "${download}" || return
    actual="$(sha256sum "${download}" | awk '{ print $1 }')"
    [ "${actual}" = "${checksum}" ] || {
        printf 'Zed checksum mismatch for %s.\n' "${artifact}" >&2
        return 1
    }

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
# @description Install Zed from a pinned GitHub release, skipping if already current.
#
function main() {
    if zed_up_to_date; then
        return 0
    fi
    install_pinned_zed || return
    link_zed_bin
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
