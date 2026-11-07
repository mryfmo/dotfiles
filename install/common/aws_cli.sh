#!/usr/bin/env bash

# @file install/common/aws_cli.sh
# @brief Install the AWS CLI release that AWS's v2/version.txt names, verified with AWS's GPG signature.
# @description
#   One read of https://awscli.amazonaws.com/v2/version.txt names the release; every download, the skip check
#   and the postcondition derive from that version. On Linux the versioned archive and its .sig, which AWS
#   never rewrites, are verified and installed; the unversioned "latest" pair is not used, because AWS
#   overwrites its two objects minutes apart and a run between the uploads pairs one release's archive with
#   another's signature. On macOS AWS's install.sh is verified, then run under the XDG roots with that
#   version; it downloads the pkg and checks its Apple Developer team id before Apple's installer runs.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

# Rendered from assets.aws-cli in home/dot_agents/agent-config.yaml; change it there.
readonly AWS_CLI_FINGERPRINT="FB5DB77FD5C118B80511ADA8A6310ACC4672475C"
readonly AWS_CLI_KEY_PATH="${AWS_CLI_KEY_PATH:-${HOME}/.local/share/aws-cli-keys/aws-cli-public-key.asc}"
readonly AWS_CLI_INSTALL_DIR="${HOME}/.local/share/aws-cli"
readonly AWS_CLI_BIN_DIR="${HOME}/.local/bin"

#
# @description Print the release version AWS's v2/version.txt names, for example 2.39.6, trimmed.
# @exitcode 1 version.txt could not be read, or what it holds is not a <major>.<minor>.<patch> version.
#
function aws_cli_release_version() {
    local version
    version="$(curl --fail --location --silent --show-error --connect-timeout 30 --speed-limit 1024 --speed-time 60 https://awscli.amazonaws.com/v2/version.txt)" || return
    version="${version//[[:space:]]/}"
    if [[ ! "${version}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        printf 'AWS CLI release check failed: version.txt names "%s", not a <major>.<minor>.<patch> version.\n' "${version}" >&2
        return 1
    fi
    printf '%s\n' "${version}"
}

#
# @description Print the URL of the installer for one AWS CLI release: on Linux the versioned archive for the
#   current supported architecture, an object AWS never rewrites, whose .sig is checked against the pinned
#   key; on macOS v2/install.sh, which installs the version it is given.
# @arg $1 string The release version, for example 2.39.6.
# @stdout The official x86_64 or aarch64 versioned archive URL, or the macOS v2/install.sh URL.
#
function aws_cli_url() {
    local architecture kernel

    kernel="$(uname -s)" || {
        printf 'uname -s failed; no AWS CLI archive was chosen.\n' >&2
        return 1
    }
    if [ "${kernel}" = Darwin ]; then
        printf 'https://awscli.amazonaws.com/v2/install.sh\n'
        return
    fi
    architecture="$(uname -m)"
    case "${architecture}" in
    x86_64 | aarch64)
        printf 'https://awscli.amazonaws.com/awscli-exe-linux-%s-%s.zip\n' "${architecture}" "$1"
        ;;
    *)
        printf 'Unsupported AWS CLI architecture: %s\n' "${architecture}" >&2
        return 1
        ;;
    esac
}

#
# @description Verify that an executable runs as the AWS CLI and print the version it reports.
# @arg $1 executable AWS CLI executable path.
# @arg $2 error_prefix Error message prefix.
# @stdout The version token, for example aws-cli/2.37.6.
#
function verify_aws_cli_version() {
    local executable="$1"
    local error_prefix="$2"
    local version_output
    local version_token

    if [[ ! -x "${executable}" ]]; then
        printf '%s: %s is not executable.\n' "${error_prefix}" "${executable}" >&2
        return 1
    fi
    version_output="$("${executable}" --version)" || return
    read -r version_token _ <<< "${version_output}"
    if [[ "${version_token}" != aws-cli/* ]]; then
        printf '%s: expected an aws-cli/<version> banner, got %s.\n' "${error_prefix}" "${version_token}" >&2
        return 1
    fi
    printf '%s\n' "${version_token}"
}

#
# @description Verify that the installer left the staged release as the working AWS CLI and report it.
# @arg $1 string The staged version, for example 2.37.6.
#
function verify_aws_cli_install() {
    local version
    version="$(verify_aws_cli_version "${AWS_CLI_BIN_DIR}/aws" "AWS CLI postcondition failed")" || return
    # An installer that skipped (an existing version directory) can leave an older CLI active.
    if [ "${version}" != "aws-cli/$1" ]; then
        printf 'AWS CLI postcondition failed: %s is active, not the staged aws-cli/%s.\n' "${version}" "$1" >&2
        return 1
    fi
    printf 'Installed %s.\n' "${version}"
}

#
# @description Verify and install one AWS CLI release without modifying a working install on verification
#   failure. On Linux the archive is the versioned one aws_cli_url names, and the CLI it stages must report
#   that version before the upstream installer runs. On macOS the verified file is install.sh, run with
#   --version so it installs that release, and the postcondition expects it.
# @arg $1 string The release version, for example 2.39.6.
# @exitcode 3 A download failed, so nothing was installed.
#
function install_aws_cli() (
    local archive_url
    local archive_path
    local signature_path
    local current_time
    local expiration
    local key_data
    local keyring_path
    local fingerprint
    local inspection_home
    local validity
    local temporary_dir
    local staged_version
    local dist_version
    local same_version_dir
    local active_version
    local kernel
    local macos=""

    kernel="$(uname -s)" || {
        printf 'uname -s failed; the AWS CLI was not installed.\n' >&2
        return 1
    }
    staged_version="$1"
    [ "${kernel}" != Darwin ] || macos=1
    archive_url="$(aws_cli_url "${staged_version}")" || return
    temporary_dir="$(mktemp -d)" || return
    trap 'rm -rf "${temporary_dir}"' EXIT

    archive_path="${temporary_dir}/awscliv2.zip"
    [ -z "${macos}" ] || archive_path="${temporary_dir}/install.sh"
    signature_path="${archive_path}.sig"
    inspection_home="${temporary_dir}/gnupg-inspection"
    keyring_path="${temporary_dir}/aws-cli-keyring.gpg"

    # curl gets 30 s to connect and fails a transfer under 1 KB/s for 60 s, so a stalled download ends.
    curl --fail --location --silent --show-error --connect-timeout 30 --speed-limit 1024 --speed-time 60 \
        "${archive_url}" --output "${archive_path}" || return 3
    curl --fail --location --silent --show-error --connect-timeout 30 --speed-limit 1024 --speed-time 60 \
        "${archive_url}.sig" --output "${signature_path}" || return 3

    mkdir -m 700 "${inspection_home}" || return
    key_data="$(gpg --homedir "${inspection_home}" --batch --with-colons --import-options show-only --import "${AWS_CLI_KEY_PATH}")" || return
    fingerprint="$(awk -F: '$1 == "fpr" { print $10 }' <<< "${key_data}")"
    validity="$(awk -F: '$1 == "pub" { print $2 }' <<< "${key_data}")"
    expiration="$(awk -F: '$1 == "pub" { print $7 }' <<< "${key_data}")"
    current_time="$(date +%s)"
    if [[ "${fingerprint}" != "${AWS_CLI_FINGERPRINT}" || "${validity}" != "-" || ! "${expiration}" =~ ^[0-9]+$ ]] ||
        ((expiration <= current_time)); then
        printf 'AWS CLI signing key validation failed.\n' >&2
        return 1
    fi
    gpg --batch --yes --dearmor --output "${keyring_path}" "${AWS_CLI_KEY_PATH}" || return
    gpgv --keyring "${keyring_path}" "${signature_path}" "${archive_path}" || return

    if [ -n "${macos}" ]; then
        mkdir -p "${AWS_CLI_BIN_DIR}" "$(dirname "${AWS_CLI_INSTALL_DIR}")" || return
        XDG_DATA_HOME="$(dirname "${AWS_CLI_INSTALL_DIR}")" XDG_BIN_HOME="${AWS_CLI_BIN_DIR}" \
            bash "${archive_path}" --version "${staged_version}" || return
        verify_aws_cli_install "${staged_version}"
        return
    fi
    unzip -q "${archive_path}" -d "${temporary_dir}" || return
    # The archive is the one the release version named, so the CLI it holds must be that release.
    dist_version="$(verify_aws_cli_version "${temporary_dir}/aws/dist/aws" "AWS CLI staged artifact verification failed")" || return
    dist_version="${dist_version#aws-cli/}"
    if [ "${dist_version}" != "${staged_version}" ]; then
        printf 'AWS CLI staged artifact verification failed: the archive holds aws-cli/%s, not the release aws-cli/%s.\n' \
            "${dist_version}" "${staged_version}" >&2
        return 1
    fi
    # The upstream installer's --update skips a version directory that already exists, so a broken
    # install of the same version, or an interrupted update that left it beside an older active CLI,
    # would never be repaired. Remove that directory first, after the signature and the staged CLI
    # passed and only when the active CLI does not run as the staged release.
    same_version_dir="${AWS_CLI_INSTALL_DIR}/v2/${staged_version}"
    if [[ "${staged_version}" =~ ^[0-9]+(\.[0-9]+)*$ && -d "${same_version_dir}" ]]; then
        # An active CLI that does not run is not the staged release either, so its failure is the answer.
        active_version="$(verify_aws_cli_version "${AWS_CLI_BIN_DIR}/aws" "AWS CLI check" 2> /dev/null)" || active_version=""
        if [ "${active_version}" != "aws-cli/${staged_version}" ]; then
            rm -rf "${same_version_dir}" || return
        fi
    fi
    mkdir -p "${AWS_CLI_BIN_DIR}" "$(dirname "${AWS_CLI_INSTALL_DIR}")" || return
    "${temporary_dir}/aws/install" \
        --install-dir "${AWS_CLI_INSTALL_DIR}" \
        --bin-dir "${AWS_CLI_BIN_DIR}" \
        --update || return
    verify_aws_cli_install "${staged_version}"
)

#
# @description Install or update the AWS CLI. Runs on every chezmoi apply: reads the release version
#   v2/version.txt names once, skips when the installed AWS CLI already runs as that release, and
#   otherwise installs that release. The skip check and the postcondition are the same predicate, so no
#   state file is kept.
#
function main() {
    local version status=0
    if ! version="$(aws_cli_release_version)"; then
        # Only a CLI that still runs stays; a broken one fails the offline apply instead of passing.
        verify_aws_cli_version "${AWS_CLI_BIN_DIR}/aws" "AWS CLI check" > /dev/null 2>&1 || {
            printf 'Could not read the AWS CLI release version, and no working AWS CLI is installed.\n' >&2
            return 1
        }
        printf 'warning: could not read the AWS CLI release version; the installed AWS CLI stays.\n' >&2
        return 0
    fi
    # An AWS CLI that runs as the release needs nothing; a broken or older one is (re)installed.
    verify_aws_cli_install "${version}" > /dev/null 2>&1 && return 0
    install_aws_cli "${version}" || status=$?
    # A failed download keeps a working AWS CLI (the next apply compares it with version.txt again);
    # a failed signature or postcondition never does.
    if [ "${status}" -eq 3 ] && verify_aws_cli_version "${AWS_CLI_BIN_DIR}/aws" "AWS CLI check" > /dev/null 2>&1; then
        printf 'warning: could not download the AWS CLI archive; the installed AWS CLI stays.\n' >&2
        return 0
    fi
    return "${status}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
