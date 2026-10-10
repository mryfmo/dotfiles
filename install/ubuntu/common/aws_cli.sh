#!/usr/bin/env bash

# @file install/ubuntu/common/aws_cli.sh
# @brief Install the current AWS CLI from its official Linux archive, verified with AWS's GPG signature.

set -Eeuo pipefail

if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

# Rendered from assets.aws-cli in home/dot_agents/agent-config.yaml; change it there.
readonly AWS_CLI_FINGERPRINT="FB5DB77FD5C118B80511ADA8A6310ACC4672475C"
readonly AWS_CLI_KEY_PATH="${AWS_CLI_KEY_PATH:-${HOME}/.local/share/aws-cli-keys/aws-cli-public-key.asc}"
readonly AWS_CLI_INSTALL_DIR="${HOME}/.local/share/aws-cli"
readonly AWS_CLI_BIN_DIR="${HOME}/.local/bin"
# The ETag of the archive the last verified install came from; a changed ETag means a new release.
readonly AWS_CLI_ETAG_FILE="${XDG_STATE_HOME:-${HOME}/.local/state}/dotfiles/aws-cli-archive.etag"

#
# @description Print the AWS CLI archive URL for the current supported architecture.
#   The unversioned archive is AWS's current release; its .sig is checked against the pinned key.
# @stdout The official x86_64 or aarch64 archive URL.
#
function aws_cli_url() {
    local architecture

    architecture="$(uname -m)"
    case "${architecture}" in
    x86_64 | aarch64)
        printf 'https://awscli.amazonaws.com/awscli-exe-linux-%s.zip\n' "${architecture}"
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
# @description Verify and install the current AWS CLI without modifying a working install on verification failure.
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
    local same_version_dir

    archive_url="$(aws_cli_url)" || return
    temporary_dir="$(mktemp -d)" || return
    trap 'rm -rf "${temporary_dir}"' EXIT

    archive_path="${temporary_dir}/awscliv2.zip"
    signature_path="${archive_path}.sig"
    inspection_home="${temporary_dir}/gnupg-inspection"
    keyring_path="${temporary_dir}/aws-cli-keyring.gpg"

    curl --fail --location --silent --show-error "${archive_url}" --output "${archive_path}" || return 3
    curl --fail --location --silent --show-error "${archive_url}.sig" --output "${signature_path}" || return 3

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

    unzip -q "${archive_path}" -d "${temporary_dir}" || return
    staged_version="$(verify_aws_cli_version "${temporary_dir}/aws/dist/aws" "AWS CLI staged artifact verification failed")" || return
    staged_version="${staged_version#aws-cli/}"
    # The upstream installer's --update skips a version directory that already exists, so a broken
    # install of the same version, or an interrupted update that left it beside an older active CLI,
    # would never be repaired. Remove that directory first, after the signature and the staged CLI
    # passed and only when the active CLI does not run as the staged release.
    same_version_dir="${AWS_CLI_INSTALL_DIR}/v2/${staged_version}"
    if [[ "${staged_version}" =~ ^[0-9]+(\.[0-9]+)*$ && -d "${same_version_dir}" ]] &&
        [ "$(verify_aws_cli_version "${AWS_CLI_BIN_DIR}/aws" "AWS CLI check" 2> /dev/null)" != "aws-cli/${staged_version}" ]; then
        rm -rf "${same_version_dir}" || return
    fi
    mkdir -p "${AWS_CLI_BIN_DIR}" "$(dirname "${AWS_CLI_INSTALL_DIR}")" || return
    "${temporary_dir}/aws/install" \
        --install-dir "${AWS_CLI_INSTALL_DIR}" \
        --bin-dir "${AWS_CLI_BIN_DIR}" \
        --update || return
    verify_aws_cli_install "${staged_version}"
)

#
# @description Print the ETag AWS serves for the current archive.
#
function aws_cli_archive_etag() {
    local url
    url="$(aws_cli_url)" || return
    curl --fail --location --silent --show-error --head "${url}" |
        awk 'tolower($1) == "etag:" { etag = $2 } END { sub(/\r$/, "", etag); if (etag == "") exit 1; print etag }'
}

#
# @description Install or update the AWS CLI. Runs on every chezmoi apply and skips when the
#   archive's ETag still matches the one recorded after the last verified install and that
#   AWS CLI still runs.
#
function main() {
    local etag status=0
    if ! etag="$(aws_cli_archive_etag)"; then
        [ -x "${AWS_CLI_BIN_DIR}/aws" ] || {
            printf 'Could not reach the AWS CLI archive.\n' >&2
            return 1
        }
        printf 'warning: could not reach the AWS CLI archive; the installed AWS CLI stays.\n' >&2
        return 0
    fi
    # The recorded ETag counts only for an AWS CLI that still runs; a broken one is reinstalled.
    if [ "$(cat "${AWS_CLI_ETAG_FILE}" 2> /dev/null)" = "${etag}" ] &&
        verify_aws_cli_version "${AWS_CLI_BIN_DIR}/aws" "AWS CLI check" > /dev/null 2>&1; then
        return 0
    fi
    install_aws_cli || status=$?
    # A failed download keeps a working AWS CLI (its ETag stays unrecorded, so the next apply retries);
    # a failed signature or postcondition never does.
    if [ "${status}" -eq 3 ] && verify_aws_cli_version "${AWS_CLI_BIN_DIR}/aws" "AWS CLI check" > /dev/null 2>&1; then
        printf 'warning: could not download the AWS CLI archive; the installed AWS CLI stays.\n' >&2
        return 0
    fi
    [ "${status}" -eq 0 ] || return "${status}"
    mkdir -p "$(dirname "${AWS_CLI_ETAG_FILE}")" && printf '%s\n' "${etag}" > "${AWS_CLI_ETAG_FILE}" ||
        printf 'warning: could not record the AWS CLI archive ETag; the next apply reinstalls it.\n' >&2
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
